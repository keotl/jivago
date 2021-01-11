import argparse
import pkgutil
from typing import List


def generate_static_imports(root_app_module: str, outputfile: str):
    """Create a .py file containing all usually automatically imported packages as import my.app.package statements.
    Suitable for bundling the JivagoApplication using PyInstaller.

    :param root_app_module: Fully qualified import name for the app root.
    :param outputfile: The output .py file."""

    packages = __import_package_recursive(__import__(root_app_module, fromlist="dummy-str1"))

    with open(outputfile, 'w') as f:
        f.writelines([f"import {x}\n" for x in packages])


def __import_package_recursive(package) -> List[str]:
    prefix = package.__name__ + "."
    packages = []
    for importer, modname, ispkg in pkgutil.iter_modules(package.__path__, prefix):
        packages.append(modname)
        module = __import__(modname, fromlist="dummy-str1")
        if ispkg:
            packages.extend(__import_package_recursive(module))
    return packages


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="""Create a .py file containing all usually automatically imported packages as import my.app.package statements. 
        Suitable for bundling the JivagoApplication using PyInstaller.""")
    parser.add_argument("--root-app-module", type=str, help="Fully qualified import name for the app root.",
                        dest="root", required=True)
    parser.add_argument("--outputfile", type=str, help="The output .py file.", dest="output", required=True)
    args = parser.parse_args()

    generate_static_imports(args.root, args.output)
