from robot.api.deco import keyword
from zaero.bridge.database_module import DatabaseModule
from zaero.bridge.connection_modules import ConnectionModules
import zaero.utils.zi_logger as zi_logger
from robot.api import SkipExecution

class Serial(DatabaseModule,
            ConnectionModules):


    ROBOT_AUTO_KEYWORDS = False
    ROBOT_LIBRARY_SCOPE = 'Global'

    def __init__(self):
        zi_logger.print_context()
        DatabaseModule.__init__(self)
        ConnectionModules.__init__(self)
        self.db_obj = self.get_database_module_object()
        zi_logger.log(f"==== db_obj : {self.db_obj}")
        zi_logger.log("Serial __init__ : END")

    @keyword("Connect With Device")
    def connect_with_device(self,
                                    device: str):
        """
        Establish a remote connection with the specified device.
        Skips execution if the device is marked as not present in the database.

        - ``device`` is the name given to the device as mentioned
                     in the dut.yaml config file

        - ``Raises`` SkipExecution if the connection cannot be established

        Example:
        | Connect With Device | ap             |
        | Connect With Device | ap_lan_client_1 |
        """
        zi_logger.print_context()
        state = self.db_obj.read_from_database(device,'device_present')
        zi_logger.log(f"State: {state}")

        if state:
            connection = self.db_obj.read_device_connection(device)
            zi_logger.log(f"Connection : {connection}")
            connection_obj = self.get_connection_module_object(connection)
            zi_logger.log(f"connection_obj: {connection_obj}")
            status = connection_obj.connect_with_device_serial(device)
            if not status:
                raise SkipExecution(
                    f"Could not established remote connection with device: {device}")


    @keyword("Execute Command")
    def execute_command(self,
                        device: str,
                        command: str,
                        prompt: str = "#"):

        zi_logger.print_context()
        connection = self.db_obj.read_device_connection(device)
        connection_obj = self.get_connection_module_object(connection)
        out = connection_obj.execute_command(device=device,
                                            command=command,
                                            prompt=prompt)
        return out


    @keyword("Close Connection")
    def close_connection(self, device: str):
        zi_logger.print_context()
        connection = self.db_obj.read_device_connection(device)
        connection_obj = self.get_connection_module_object(connection)
        connection_obj.close_connection(device) 

