import os

from jivago.templating.no_such_template_exception import NoSuchTemplateException


class ViewTemplateRepository(object):

    def __init__(self, view_template_folder: str):
        self.view_template_folder = view_template_folder

    def get_template(self, filename: str) -> str:
        try:
            with open(os.path.join(self.view_template_folder, filename), 'r') as f:
                return "\n".join(f.readlines())
        except FileNotFoundError:
            raise NoSuchTemplateException()
