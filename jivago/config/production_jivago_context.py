from typing import List, Type

import os

from jivago.config.abstract_context import AbstractContext
from jivago.inject.annoted_class_binder import AnnotatedClassBinder
from jivago.inject.provider_binder import ProviderBinder
from jivago.lang.registry import Singleton, Component, Registry
from jivago.inject.scope_cache import ScopeCache
from jivago.lang.annotations import Override, BackgroundWorker
from jivago.lang.stream import Stream
from jivago.templating.template_filter import TemplateFilter
from jivago.templating.view_template_repository import ViewTemplateRepository
from jivago.wsgi.annotations import Resource
from jivago.wsgi.dto_serialization_handler import DtoSerializationHandler
from jivago.wsgi.filters.exception.application_exception_filter import ApplicationExceptionFilter
from jivago.wsgi.filters.exception.unknown_exception_filter import UnknownExceptionFilter
from jivago.wsgi.filters.filter import Filter
from jivago.wsgi.request.http_form_deserialization_filter import HttpFormDeserializationFilter
from jivago.wsgi.request.json_serialization_filter import JsonSerializationFilter
from jivago.wsgi.request.url_encoded_query_parser import UrlEncodedQueryParser


class ProductionJivagoContext(AbstractContext):

    def __init__(self, root_package, registry: Registry):
        self.rootPackage = root_package
        self.registry = registry
        super().__init__()

    @Override
    def configure_service_locator(self):
        AnnotatedClassBinder(self.rootPackage.__name__, self.registry, Component).bind(self.serviceLocator)
        AnnotatedClassBinder(self.rootPackage.__name__, self.registry, Resource).bind(self.serviceLocator)
        AnnotatedClassBinder(self.rootPackage.__name__, self.registry, BackgroundWorker).bind(self.serviceLocator)
        ProviderBinder(self.rootPackage.__name__, self.registry).bind(self.serviceLocator)
        for scope in self.scopes():
            scoped_classes = Stream(self.registry.get_annotated_in_package(scope, self.rootPackage.__name__)).map(
                lambda registration: registration.registered).toList()
            cache = ScopeCache(scope, scoped_classes)
            self.serviceLocator.register_scope(cache)

        Stream(self.get_filters("")).forEach(lambda f: self.serviceLocator.bind(f, f))

        # TODO better way to handle Jivago Dependencies
        self.serviceLocator.bind(DtoSerializationHandler,
                                 DtoSerializationHandler(Registry(), self.rootPackage.__name__))
        self.serviceLocator.bind(ViewTemplateRepository, ViewTemplateRepository(self.get_views_folder_path()))
        self.serviceLocator.bind(UrlEncodedQueryParser, UrlEncodedQueryParser)

    def scopes(self) -> List[type]:
        return [Singleton, BackgroundWorker]

    @Override
    def get_filters(self, path: str) -> List[Type[Filter]]:
        return [UnknownExceptionFilter, TemplateFilter, JsonSerializationFilter, HttpFormDeserializationFilter,
                ApplicationExceptionFilter]

    @Override
    def get_views_folder_path(self) -> str:
        return os.path.join(os.path.dirname(self.rootPackage.__file__), "views")
