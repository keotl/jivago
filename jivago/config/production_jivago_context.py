from typing import List

from jivago.config.abstract_context import AbstractContext
from jivago.inject.annoted_class_binder import AnnotatedClassBinder
from jivago.inject.provider_binder import ProviderBinder
from jivago.inject.registry import Singleton, Component, Registry
from jivago.inject.scope_cache import ScopeCache
from jivago.lang.annotations import Override, BackgroundWorker
from jivago.lang.stream import Stream
from jivago.wsgi.annotations import Resource
from jivago.wsgi.filters.exception_filter import ExceptionFilter
from jivago.wsgi.filters.json_serialization_filter import JsonSerializationFilter


class ProductionJivagoContext(AbstractContext):

    def __init__(self, root_package: str, registry: Registry):
        self.rootPackage = root_package
        self.registry = registry
        super().__init__()

    @Override
    def configure_service_locator(self):
        AnnotatedClassBinder(self.rootPackage, self.registry, Component).bind(self.serviceLocator)
        AnnotatedClassBinder(self.rootPackage, self.registry, Resource).bind(self.serviceLocator)
        AnnotatedClassBinder(self.rootPackage, self.registry, BackgroundWorker).bind(self.serviceLocator)
        ProviderBinder(self.rootPackage, self.registry).bind(self.serviceLocator)
        for scope in self.scopes():
            scoped_classes = Stream(self.registry.get_annotated_in_package(scope, self.rootPackage)).map(
                lambda registration: registration.registered).toList()
            cache = ScopeCache(scope, scoped_classes)
            self.serviceLocator.register_scope(cache)

        Stream(self.filter_chain()).forEach(lambda f: self.serviceLocator.bind(f, f))

    def filter_chain(self) -> List[type]:
        return [ExceptionFilter, JsonSerializationFilter]

    def scopes(self) -> List[type]:
        return [Singleton, BackgroundWorker]
