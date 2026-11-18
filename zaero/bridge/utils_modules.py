"""
Factory for the utility modules.

Author: Zilogic Systems <code@zilogic.com>
"""

from zaero.utils.packet_sniffer import PacketSniffer
from zaero.utils.packet_capture import PacketCapture
from zaero.utils.pdu_controller import PduController
from zaero.utils.traffic_generator import TrafficGenerator
import zaero.utils.zi_logger as zi_logger

class UtilsModules:
    """
    Singleton factory that returns the utility object for a name.
    Supported names are ``sniffer`` (PacketSniffer), ``capture``
    (PacketCapture), ``pdu`` (PduController) and ``traffic_generator``
    (TrafficGenerator). One object is created per name.
    """

    __instance = None
    __modules = {'sniffer': PacketSniffer,
                 'capture': PacketCapture,
		 'pdu': PduController,
		 'traffic_generator': TrafficGenerator}
    __module_objects = {}

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            zi_logger.log("UtilsModules Instance created")
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        zi_logger.log("UtilsModules __init__")

    def get_utils_module_object(self, module):
        """
        Get the utility object for the given name, creating it on first use.

        - ``module`` is one of ``sniffer``, ``capture``, ``pdu`` or
          ``traffic_generator``

        - ``Returns`` the shared utility object

        - ``Raises`` KeyError if the name is not supported
        """
        zi_logger.log(f"lib.bridge.utils_modules.get_utils_module_object({module})")
        if module not in UtilsModules.__module_objects:
            zi_logger.log(f"UtilsModules.modules : {UtilsModules.__modules}")
            UtilsModules.__module_objects[module] = UtilsModules.__modules[module]()
        return UtilsModules.__module_objects[module]
