import unittest

from jivago.lang.registration import Registration


class RegistrationTest(unittest.TestCase):

    def setUp(self):
        self.classRegistration = Registration(AClass)
        self.functionRegistration = Registration(aFunction)
        self.methodRegistration = Registration(AClass.a_method)

    def test_isClassRegistration(self):
        self.assertTrue(self.classRegistration.is_class_registration())
        self.assertFalse(self.functionRegistration.is_class_registration())
        self.assertFalse(self.methodRegistration.is_class_registration())

    def test_isFunctionRegistration(self):
        self.assertTrue(self.functionRegistration.is_function_registration())
        self.assertFalse(self.classRegistration.is_function_registration())
        self.assertFalse(self.methodRegistration.is_function_registration())

    def test_isMethodRegistration(self):
        self.assertTrue(self.methodRegistration.is_method_registration())
        self.assertFalse(self.classRegistration.is_method_registration())
        self.assertFalse(self.functionRegistration.is_method_registration())



class AClass(object):

    def a_method(self):
        pass


def aFunction():
    pass
