import unittest
from typing import Callable

from jivago.inject.registry import Registry, ParametrizedAnnotation

A_MESSAGE = "A MESSAGE"
A_ROUTE = "/route"


class ParametrizedAnnotationTest(unittest.TestCase):

    def setUp(self):
        self.registry = Registry()

    def test_whenUsingParametrizedAnnotation_thenWrappedObjectsAreSavedInTheRegistry(self):
        wrapped_function = self.registry.get_annotated_in_package(myAnnotation, "")[0].registered

        self.assertEqual(some_wrapped_function, wrapped_function)

    def test_whenUsingParametrizedAnnotation_thenParametersAreStoredInTheRegistration(self):
        registration = self.registry.get_annotated_in_package(myAnnotation, "")[0]

        self.assertEqual(A_MESSAGE, registration.arguments['message'])
        self.assertFalse("value" in registration.arguments)

    def test_givenImplicitParameterName_whenUsingParametrizedAnnotation_thenParameterIsImplicitlyNamedValue(self):
        registration = self.registry.get_annotated_in_package(implicit_parameter_annotation, "")[0]

        self.assertEqual(A_MESSAGE, registration.arguments['value'])

    def test_givenKeywordOnlyArguments_whenUsingParametrizedAnnotation_thenParametersAreSavedInTheRegistration(self):
        registration = self.registry.get_annotated_in_package(multipleParameterAnnotation, "")[0]

        self.assertEqual(A_MESSAGE, registration.arguments['message'])
        self.assertEqual(A_ROUTE, registration.arguments['route'])


@ParametrizedAnnotation
def myAnnotation(message: str) -> Callable:
    def wrapper(wrapped: Callable) -> "foo":
        return wrapped

    return wrapper


@myAnnotation(message=A_MESSAGE)
def some_wrapped_function():
    return "something"


@ParametrizedAnnotation
def implicit_parameter_annotation(value: str) -> Callable:
    def wrapper(auie):
        return auie

    return wrapper


@implicit_parameter_annotation(A_MESSAGE)
def implicit_wrapped_function():
    return "something"


@ParametrizedAnnotation
def multipleParameterAnnotation(*, message: str, route: str):
    return lambda x: x


@multipleParameterAnnotation(route=A_ROUTE, message=A_MESSAGE)
class AnnotatedWithMultipleParameters(object):
    pass


if __name__ == '__main__':
    unittest.main()
