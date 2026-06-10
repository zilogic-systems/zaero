from zaero.utils.packet_sniffer import PacketSniffer
import zaero.utils.zi_logger as zi_logger

class UtilsModules:

    __instance = None
    __modules = {'sniffer': PacketSniffer}
    __module_objects = {}

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            zi_logger.log("UtilsModules Instance created")
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        zi_logger.log("UtilsModules __init__")

    def get_utils_module_object(self, module):
        zi_logger.log(f"lib.bridge.utils_modules.get_utils_module_object({module})")
        if module not in UtilsModules.__module_objects:
            zi_logger.log(f"UtilsModules.modules : {UtilsModules.__modules}")
            UtilsModules.__module_objects[module] = UtilsModules.__modules[module]()
        return UtilsModules.__module_objects[module]
