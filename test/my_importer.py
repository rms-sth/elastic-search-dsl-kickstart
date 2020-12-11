# # import os, pkgutil

# # __all__ = list(
# #     module for _, module, _ in pkgutil.iter_modules([os.path.dirname(__file__)]) if module != 'my_importer'
# # )


# from os.path import dirname, basename, isfile, join
# import glob

# modules = glob.glob(join(dirname(__file__), "*.py"))
# __all__ = [
#     basename(f)[:-3] for f in modules if isfile(f) and not f.endswith("__init__.py" )
# ]

# print(__all__)


import pkgutil
import sys


def load_all_modules_from_dir(dirname):
    for importer, package_name, _ in pkgutil.iter_modules([dirname]):
        full_package_name = "%s.%s" % (dirname, package_name)
        if full_package_name not in sys.modules:
            print(package_name)
            # module = importer.find_module(package_name).load_module(full_package_name)
            # print(module)


load_all_modules_from_dir("tasks")