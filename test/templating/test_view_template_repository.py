import unittest

import os

import test_data
from jivago.templating.no_such_template_exception import NoSuchTemplateException
from jivago.templating.view_template_repository import ViewTemplateRepository

TEMPLATE_CONTENT = "{{ data }}\n"


class ViewTemplateRepositoryTest(unittest.TestCase):

    def setUp(self):
        self.templateRepository = ViewTemplateRepository(os.path.dirname(test_data.__file__))

    def test_whenGettingTemplate_thenReturnCorrespondingFileContent(self):
        template = self.templateRepository.get_template("template.txt")

        self.assertEqual(TEMPLATE_CONTENT, template)

    def test_givenInexistentTemplateFile_whenGettingTemplate_thenThrowNoSuchTemplateException(self):
        with self.assertRaises(NoSuchTemplateException):
            self.templateRepository.get_template("inexistent-file.html")
