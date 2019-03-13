import os
from typing import List, Type, Union

from jivago.config.abstract_context import AbstractContext
from jivago.config.exception_mapper_binder import ExceptionMapperBinder
from jivago.config.router.filtering.annotation import RequestFilter
from jivago.config.router.filtering.auto_discovering_filtering_rule import AutoDiscoveringFilteringRule
from jivago.config.router.filtering.filtering_rule import FilteringRule
from jivago.config.router.router_builder import RouterBuilder
from jivago.config.startup_hooks import Init, PreInit, PostInit
from jivago.event.async_event_bus import AsyncEventBus
from jivago.event.config.annotations import EventHandlerClass
from jivago.event.config.reflective_event_bus_initializer import ReflectiveEventBusInitializer
from jivago.event.config.runnable_event_handler_binder import RunnableEventHandlerBinder
from jivago.event.event_bus import EventBus
from jivago.event.synchronous_event_bus import SynchronousEventBus
from jivago.inject.annotation import Component, Singleton
from jivago.inject.annoted_class_binder import AnnotatedClassBinder
from jivago.inject.provider_binder import ProviderBinder
from jivago.inject.scope_cache import ScopeCache
from jivago.lang.annotations import Override, BackgroundWorker
from jivago.lang.registry import Registry
from jivago.lang.stream import Stream
from jivago.scheduling.annotations import Scheduled
from jivago.scheduling.task_scheduler import TaskScheduler
from jivago.serialization.deserializer import Deserializer
from jivago.serialization.object_mapper import ObjectMapper
from jivago.serialization.serializer import Serializer
from jivago.templating.template_filter import TemplateFilter
from jivago.templating.view_template_repository import ViewTemplateRepository
from jivago.wsgi.annotations import Resource
from jivago.wsgi.filter.filter import Filter
from jivago.wsgi.filter.system_filters.body_serialization_filter import BodySerializationFilter
from jivago.wsgi.filter.system_filters.error_handling.application_exception_filter import ApplicationExceptionFilter
from jivago.wsgi.filter.system_filters.error_handling.unknown_exception_filter import UnknownExceptionFilter
from jivago.wsgi.filter.system_filters.jivago_banner_filter import JivagoBannerFilter
from jivago.wsgi.request.http_form_deserialization_filter import HttpFormDeserializationFilter
from jivago.wsgi.request.http_status_code_resolver import HttpStatusCodeResolver
from jivago.wsgi.request.json_serialization_filter import JsonSerializationFilter
from jivago.wsgi.request.partial_content_handler import PartialContentHandler
from jivago.wsgi.routing.routing_rule import RoutingRule
from jivago.wsgi.routing.table.auto_discovering_routing_table import AutoDiscoveringRoutingTable


class ProductionJivagoContext(AbstractContext):

    def __init__(self, root_package: "Module", registry: Registry, banner: bool = True):
        self.banner = banner
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
        AnnotatedClassBinder(self.root_package_name, self.registry, EventHandlerClass).bind(self.serviceLocator)
        AnnotatedClassBinder(self.root_package_name, self.registry, RequestFilter).bind(self.serviceLocator)

        ProviderBinder(self.root_package_name, self.registry).bind(self.serviceLocator)
        for scope in self.scopes():
            scoped_classes = Stream(self.registry.get_annotated_in_package(scope, self.root_package_name)).map(
                lambda registration: registration.registered).toList()
            cache = ScopeCache(scope, scoped_classes)
            self.serviceLocator.register_scope(cache)

        Stream(self.get_default_filters()).forEach(lambda f: self.serviceLocator.bind(f, f))

        # TODO better way to handle Jivago Dependencies
        self.serviceLocator.bind(Registry, Registry.INSTANCE)
        self.serviceLocator.bind(TaskScheduler, TaskScheduler(self.serviceLocator))
        self.serviceLocator.bind(Deserializer, Deserializer(Registry.INSTANCE))
        self.serviceLocator.bind(Serializer, Serializer())
        self.serviceLocator.bind(ViewTemplateRepository, ViewTemplateRepository(self.get_views_folder_path()))
        self.serviceLocator.bind(BodySerializationFilter, BodySerializationFilter)
        self.serviceLocator.bind(PartialContentHandler, PartialContentHandler)
        self.serviceLocator.bind(HttpStatusCodeResolver, HttpStatusCodeResolver)
        self.serviceLocator.bind(ObjectMapper, ObjectMapper)
        self.serviceLocator.bind(EventBus, self.create_event_bus())
        self.serviceLocator.bind(SynchronousEventBus, self.serviceLocator.get(EventBus))
        self.serviceLocator.bind(AsyncEventBus, AsyncEventBus(self.serviceLocator.get(EventBus)))

        RunnableEventHandlerBinder(self.root_package_name, self.registry).bind(self.service_locator())

        ExceptionMapperBinder().bind(self.serviceLocator)

    def scopes(self) -> List[type]:
        return [Singleton, BackgroundWorker]

    @Override
    def get_views_folder_path(self) -> str:
        return os.path.join(os.path.dirname(self.root_package.__file__), "views") if self.root_package else ''

    @Override
    def get_config_file_locations(self) -> List[str]:
        return ["application.yml", "application.json", "properties.yml", "properties.json"]

    @Override
    def create_router_config(self) -> RouterBuilder:
        return RouterBuilder() \
            .add_rule(FilteringRule("*", self.get_default_filters())) \
            .add_rule(AutoDiscoveringFilteringRule("*", self.registry, self.root_package_name)) \
            .add_rule(RoutingRule("/", AutoDiscoveringRoutingTable(self.registry, self.root_package_name)))

    def get_default_filters(self) -> List[Union[Filter, Type[Filter]]]:
        default_filters = [UnknownExceptionFilter, TemplateFilter, JsonSerializationFilter,
                           HttpFormDeserializationFilter,
                           BodySerializationFilter, ApplicationExceptionFilter]
        if self.banner:
            default_filters.append(JivagoBannerFilter)

        return default_filters

    def create_event_bus(self) -> EventBus:
        return ReflectiveEventBusInitializer(self.service_locator(), self.registry,
                                             self.root_package_name).create_message_bus()
