import os
from typing import List, Type

from jivago.config.abstract_context import AbstractContext
from jivago.config.exception_mapper_binder import ExceptionMapperBinder
from jivago.config.startup_hooks import Init, PreInit, PostInit
from jivago.inject.annoted_class_binder import AnnotatedClassBinder
from jivago.inject.provider_binder import ProviderBinder
from jivago.inject.scope_cache import ScopeCache
from jivago.lang.annotations import Override, BackgroundWorker
from jivago.lang.registry import Singleton, Component, Registry
from jivago.lang.stream import Stream
from jivago.scheduling.annotations import Scheduled
from jivago.scheduling.task_scheduler import TaskScheduler
from jivago.templating.template_filter import TemplateFilter
from jivago.templating.view_template_repository import ViewTemplateRepository
from jivago.wsgi.annotations import Resource
from jivago.wsgi.dto_serialization_handler import DtoSerializationHandler
from jivago.wsgi.filters.body_serialization_filter import BodySerializationFilter
from jivago.wsgi.filters.exception.application_exception_filter import ApplicationExceptionFilter
from jivago.wsgi.filters.exception.unknown_exception_filter import UnknownExceptionFilter
from jivago.wsgi.filters.filter import Filter
from jivago.wsgi.http_status_code_resolver import HttpStatusCodeResolver
from jivago.wsgi.partial_content_handler import PartialContentHandler
from jivago.wsgi.request.http_form_deserialization_filter import HttpFormDeserializationFilter
from jivago.wsgi.request.json_serialization_filter import JsonSerializationFilter
from jivago.wsgi.request.url_encoded_query_parser import UrlEncodedQueryParser


class ProductionJivagoContext(AbstractContext):

    def __init__(self, root_package: "Module", registry: Registry):
        self.root_package_name = root_package.__name__ if root_package else ''
        self.root_package = root_package
        self.registry = registry
        super().__init__()

    @Override
    def configure_service_locator(self):
        AnnotatedClassBinder(self.root_package_name, self.registry, Component).bind(self.serviceLocator)
        AnnotatedClassBinder(self.root_package_name, self.registry, Resource).bind(self.serviceLocator)
        AnnotatedClassBinder(self.root_package_name, self.registry, BackgroundWorker).bind(self.serviceLocator)
        AnnotatedClassBinder(self.root_package_name, self.registry, Scheduled).bind(self.serviceLocator)
        AnnotatedClassBinder(self.root_package_name, self.registry, Init).bind(self.serviceLocator)
        AnnotatedClassBinder(self.root_package_name, self.registry, PreInit).bind(self.serviceLocator)
        AnnotatedClassBinder(self.root_package_name, self.registry, PostInit).bind(self.serviceLocator)

        ProviderBinder(self.root_package_name, self.registry).bind(self.serviceLocator)
        for scope in self.scopes():
            scoped_classes = Stream(self.registry.get_annotated_in_package(scope, self.root_package_name)).map(lambda registration: registration.registered).toList()
            cache = ScopeCache(scope, scoped_classes)
            self.serviceLocator.register_scope(cache)

        Stream(self.get_filters("")).forEach(lambda f: self.serviceLocator.bind(f, f))

        # TODO better way to handle Jivago Dependencies
        self.serviceLocator.bind(TaskScheduler, TaskScheduler(self.serviceLocator))
        self.serviceLocator.bind(DtoSerializationHandler,
                                 DtoSerializationHandler(Registry(), self.root_package_name))
        self.serviceLocator.bind(ViewTemplateRepository, ViewTemplateRepository(self.get_views_folder_path()))
        self.serviceLocator.bind(UrlEncodedQueryParser, UrlEncodedQueryParser)
        self.serviceLocator.bind(BodySerializationFilter, BodySerializationFilter)
        self.serviceLocator.bind(PartialContentHandler, PartialContentHandler)
        self.serviceLocator.bind(HttpStatusCodeResolver, HttpStatusCodeResolver)

        ExceptionMapperBinder().bind(self.serviceLocator)

    def scopes(self) -> List[type]:
        return [Singleton, BackgroundWorker]

    @Override
    def get_filters(self, path: str) -> List[Type[Filter]]:
        return [UnknownExceptionFilter, TemplateFilter, JsonSerializationFilter, HttpFormDeserializationFilter, BodySerializationFilter,
                ApplicationExceptionFilter]

    @Override
    def get_views_folder_path(self) -> str:
        return os.path.join(os.path.dirname(self.root_package.__file__), "views") if self.root_package else ''

    @Override
    def get_config_file_locations(self) -> List[str]:
        return ["application.yml", "application.json", "properties.yml", "properties.json"]
