import unittest

from jivago.inject.registry import Registry, ParametrizedAnnotation


class ParametrizedAnnotationTest(unittest.TestCase):

    def setUp(self):
        self.registry = Registry()

    def test_whenUsingParametrizedAnnotation_thenWrappedTypesAreSavedInTheRegistry(self):
        wrapped_function = self.registry.get_annotated_in_package(myAnnotation, "")[0].registered

        self.assertEqual(some_wrapped_function, wrapped_function)


@ParametrizedAnnotation
def myAnnotation(message: str):
    def wrapper(wrapped):
        return wrapped

    return wrapper


@myAnnotation("A MESSAGE")
def some_wrapped_function():
    return "something"


if __name__ == '__main__':
    unittest.main()
