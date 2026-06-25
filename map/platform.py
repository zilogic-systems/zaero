import importlib
import inspect
from zaero.bridge.database_module import DatabaseModule

class platform(DatabaseModule):

    def __init__(self):
        print("zaero.platform.__init__")
        DatabaseModule.__init__(self)
        self.db_obj = self.get_database_module_object()

    @classmethod
    def configure_platform(cls, os_name : str, external=True):
        if external:
            imp_module = importlib.import_module(f"{os_name}")
        else:
            imp_module = importlib.import_module(f"zaero.{os_name}")
        classes = inspect.getmembers(imp_module, inspect.isclass)
        for name, imp_cls in classes:
            print(f"****************PM.CLASS NAME : {name}")
            if name == os_name and imp_cls.__module__ == imp_module.__name__:
                cls.__bases__ = (imp_cls,) + cls.__bases__
                break
        else:
            raise Exception("Class - {os_name} Not found in the platform module : {os_name}")
