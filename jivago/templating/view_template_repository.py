import os


class ViewTemplateRepository(object):

    def __init__(self, view_template_folder: str):
        self.view_template_folder = view_template_folder

    def get_template(self, filename: str) -> str:
        with open(os.path.join(self.view_template_folder, filename), 'r') as f:
            return "\n".join(f.readlines())
