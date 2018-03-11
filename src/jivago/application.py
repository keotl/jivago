import pkgutil


class JivagoApplication(object):

    def __init__(self, root_module):
        self.__importPackage(root_module)

    def __importPackage(self, package):
        prefix = package.__name__ + "."
        for importer, modname, ispkg in pkgutil.iter_modules(package.__path__, prefix):
            print("Found submodule %s (is a package: %s)" % (modname, ispkg))
            module = __import__(modname, fromlist="dummy")
            if ispkg:
                self.__importPackage(module)
            print("Imported", module)
