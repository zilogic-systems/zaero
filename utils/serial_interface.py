import serial
from robot.api.deco import keyword
from zaero.bridge.database_module import DatabaseModule
import zaero.utils.zi_logger as zi_logger


class SerialInterface(DatabaseModule):

    ROBOT_AUTO_KEYWORDS = False
    ROBOT_LIBRARY_SCOPE = 'global'

    __objects = {}
    __alias = None
    __instance = None

    def __new__(cls, *args, **kwargs):
        zi_logger.print_context()
        if cls.__instance is None:
            zi_logger.log("SerialInterface Instance created")
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        zi_logger.print_context()
        DatabaseModule.__init__(self)
        self.__db_obj = self.get_database_module_object()
        zi_logger.log(f"==== db_obj : {self.__db_obj}")
        zi_logger.log("utila.serial_interface.__init__() : END")


    def __open_connection(self,
                            serial_port: str,
                            alias: str = None,
                            baudrate: int = 115200,
                            timeout: int = 2,
                            write_timeout: int =2):
        zi_logger.print_context()
        if alias is not None and alias in SerialInterface.__objects:
            raise RuntimeError(f"ERROR : Given alias name {alias} is already created")

        zi_logger.log(f"========= ALIAS IS : {alias}")
        SerialInterface.__objects[alias] = {}
        SerialInterface.__objects[alias]["serial_port"] = serial_port
        SerialInterface.__objects[alias]["baudrate"] = baudrate
        SerialInterface.__objects[alias]["timeout"] = timeout

        SerialInterface.__objects[alias]["serial"] = serial.Serial(
                                                                port=serial_port,
                                                                baudrate=baudrate,
                                                                timeout=timeout,
                                                                write_timeout=write_timeout,
                                                                parity=serial.PARITY_NONE,
                                                                bytesize=serial.EIGHTBITS,
                                                                stopbits=serial.STOPBITS_ONE)
        SerialInterface.__alias = alias

        zi_logger.log(f"========= ALIAS List : {SerialInterface.__objects.keys()}")


    def connect_with_device_serial(self,
                             device: str):

        zi_logger.print_context()

        try:
            serial_port = self.__db_obj.read_from_database(device,"serial_port")
            baudrate = self.__db_obj.read_from_database(device,"serial_baudrate")
            self.__open_connection(serial_port=serial_port,alias=device,baudrate=baudrate)
            zi_logger.log(f"Connected with device : {device}")
            return True
        except Exception as err: # pylint: disable=broad-except
            zi_logger.log(f"Could not login into the device : {device}")
            return False


    def execute_command(self,
                        device: str,
                        command: str,
                        prompt: str = "#"):

        zi_logger.print_context()
        if device not in SerialInterface.__objects:
            raise RuntimeError(f"Device {device} is not connected")
        try:
            ser = SerialInterface.__objects[device]["serial"]
            ser.reset_input_buffer()
            ser.write(f"{command}\n".encode())
            output = ser.read_until(prompt.encode())
            output = output.decode("utf-8",errors="ignore")
            lines = output.strip().splitlines()
            lines = lines[1:-1]
            output = "\n".join(lines).strip()
            zi_logger.log(f"Output :\n{output}")
            return output
        except Exception as err:
            raise RuntimeError(err) from err

    def close_connection(self,
                         device: str):

        zi_logger.print_context()
        if device not in SerialInterface.__objects:
            raise RuntimeError(f"Device {device} is not connected")
        try:
            SerialInterface.__objects[device]["serial"].close()
            del SerialInterface.__objects[device]
            zi_logger.log(f"Closed connection : {device}")
        except Exception as err:
            raise RuntimeError(err) from err

    def close_all_connections(self):

        zi_logger.print_context()
        aliases = list(SerialInterface.__objects.keys())
        if len(aliases) >= 1:
            for alias in aliases:
                try:
                    SerialInterface.__objects[alias]["serial"].close()
                except Exception as err: # pylint: disable=broad-except
                        zi_logger.log(f"ERROR: {err}")
                        zi_logger.log(f"Could not close the serial connection for the alias : {alias}")
            SerialInterface.__objects = {}
            zi_logger.log("All serial connections closed")




