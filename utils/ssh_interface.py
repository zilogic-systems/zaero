# Copyright 2024 Zilogic Systems
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""
Author: Zilogic Systems <code@zilogic.com>
"""

import string
import random

import paramiko

from scp import SCPClient
from robot.api.deco import keyword

from zaero.bridge.database_module import DatabaseModule
import zaero.utils.zi_logger as zi_logger

class SshInterface(DatabaseModule):
    """A library provides keywords to establish SSH connections
    into devices from different platforms
    """

    ROBOT_AUTO_KEYWORDS = False
    ROBOT_LIBRARY_SCOPE = 'Global'

    __objects = {}
    __alias = None
    __instance = None

    def __new__(cls, *args, **kwargs):
        zi_logger.print_context()
        if cls.__instance is None:
            zi_logger.log("SshInterface Instance created")
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        zi_logger.print_context()
        DatabaseModule.__init__(self)
        self.__db_obj = self.get_database_module_object()
        zi_logger.log(f"==== db_obj : {self.__db_obj}")
        zi_logger.log("utila.ssh_interface.__init__() : END")

    def __create_ssh_client(self) -> object:
        """
        Create a ssh client object

        ``returns`` the create ssh client object

        ``raise`` an exception if the client object could not be crated

        Example:
        | Create Ssh Client |
        """
        zi_logger.print_context()
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            return client
        except Exception as err: # pylint: disable=broad-except
            zi_logger.log("Could not create new ssh client")
            raise RuntimeError(err) from err

    def __open_connection(self,
                          host : str,
                          alias : str = None,
                          port: int = 22,
                          timeout: int = 10,
                          sock = None):
        """
        Register SSH connection parameters for the given host under an alias.
        Creates the underlying Paramiko client object but does not connect yet;
        call login() afterwards to authenticate.

        ``host`` is the IP address of the remote device and ``alias`` is the reference
        name for this connection (auto-generated if None) and ``port`` is the SSH port
        on the remote device and ``timeout`` is the connection timeout in seconds

        ``raise`` RuntimeError if the given alias is already registered
        """
        zi_logger.print_context()

        if alias is not None and alias in SshInterface.__objects:
            raise RuntimeError(f"ERROR : Given alias name {alias} is already created")
        if alias is None:
            raise RuntimeError(f"ERROR: Given alias is None")

        zi_logger.log(f"========= ALIAS IS : {alias}")
        SshInterface.__objects[alias] = {}
        SshInterface.__objects[alias]['host'] = host
        SshInterface.__objects[alias]['port'] = port
        SshInterface.__objects[alias]['timeout'] = timeout
        SshInterface.__objects[alias]['sock'] = sock
        SshInterface.__objects[alias]['client'] = self.__create_ssh_client()
        SshInterface.__alias = alias
        zi_logger.log(f"========= ALIAS List : {SshInterface.__objects.keys()}")

    
    def __login(self,
                username: str,
                password: str = None):
        """
        Login into the remote device

        This will be executed after the `Open Connection` keyword in order
        to use the alias name assigned to ssh client object to proceed further

        ``username`` is the username using to login into the remote
        device and ``password`` password associated with the corresponding
        username and ``raise`` Runtime error if could not login into the remote device

        Example:
        | Ssh Login | user | user |
        | Ssh Login | root | root |
        """
        zi_logger.print_context()
        SshInterface.__objects[SshInterface.__alias]['username'] = username
        SshInterface.__objects[SshInterface.__alias]['password'] = password
        host = SshInterface.__objects[SshInterface.__alias]['host']
        port = SshInterface.__objects[SshInterface.__alias]['port']
        timeout = SshInterface.__objects[SshInterface.__alias]['timeout']
        sock = SshInterface.__objects[SshInterface.__alias].get("sock")
        try:
            if not sock:
                SshInterface.__objects[SshInterface.__alias]['client'].connect(hostname=host,
                                                                               port=port,
                                                                               username=username,
                                                                               password=password,
                                                                               timeout=timeout,
                                                                               banner_timeout = 60,
                                                                               auth_timeout = 30,
                                                                               look_for_keys = False,
                                                                               allow_agent = False)
            else:
                SshInterface.__objects[SshInterface.__alias]['client'].connect(hostname=host,
                                                                               username=username,
                                                                               password=password,
                                                                               timeout=timeout,
                                                                               banner_timeout = 60,
                                                                               sock = sock,
                                                                               look_for_keys = False,
                                                                               allow_agent = False)
            transport = SshInterface.__objects[SshInterface.__alias]['client'].get_transport()
            #trasnport.set_keepalive(5)
            if transport is None or not transport.is_active():
                raise Exception("SSH transport is not active")
            transport.sock.settimeout(5)
            transport.set_keepalive(3)
            zi_logger.log(f"Succesfully login into the device - {SshInterface.__alias}")
            self.__db_obj.write_into_database(SshInterface.__alias, 
                                              "connection_status",
                                              True)
            return True

        except Exception as err: # pylint: disable=broad-except
            zi_logger.log(f"Could not login into the device - {SshInterface.__alias} \nhost: {host}\n\
username: {username}\npassword:{password}")
            self.__db_obj.write_into_database(SshInterface.__alias,
                                              "connection_status",
                                              False)
            zi_logger.log(f"ERROR : {err}")
            SshInterface.__objects.pop(SshInterface.__alias, None)
            raise RuntimeError(f"RuntimeError: {err}") from err
            #return False
            
    
    def is_device_alive(self,
                        device: str):
        zi_logger.print_context()
        if device not in SshInterface.__objects:
            raise RuntimeError(f"Given alias - {device} is not present")
        try:
            transport = SshInterface.__objects[device]['client'].get_transport()
            if transport is None or not transport.is_active():
                return False

            stdin, stdout, stderr = SshInterface.__objects[device]['client'].exec_command("echo alive", timeout=5)
            stdout.channel.settimeout(5)
            stdout.channel.recv_exit_status()
            self.__db_obj.write_into_database(device, "connection_status", True)
            return True
        except Exception as err:
            zi_logger.log(f"is_device_alive ERROR is : {err}")
            self.__db_obj.write_into_database(device, "connection_status", False)
            return False

    
    # def connect_with_device(self,
    #                         device: str):
    #     """
    #     To connect with a remote device using SSH protocol

    #     Internally it will using the keywords `Open Connection` and `Login`

    #     ``device`` name of the remote device and it will be used as alias name
    #     to refer the remote device further. The details of the device will be read
    #     from config files.

    #     ``raise`` Runtime error if could not connect with the given device
    #     """
    #     zi_logger.print_context()
    #     try:
    #         host = self.__db_obj.read_from_database(device, 'login_ip')
    #         username = self.__db_obj.read_from_database(device, 'username')
    #         password = self.__db_obj.read_from_database(device, 'password')
    #         port = self.__db_obj.read_from_database(device, 'port')
    #         self.__open_connection(host, alias=device, timeout=10, port=port)
    #         self.login(username, password)
    #         zi_logger.log(f"SSH connection successfully established with the device : {device}")
    #         return True
    #     except Exception as err: # pylint: disable=broad-except
    #         zi_logger.log(f"Could not login into the device : {device}")
    #         return False

    def connect_with_device(self,
                            device: str):
        """
        Connect to the given device.

        If ssh_tunnel is False:
            Direct SSH connection.

        If ssh_tunnel is True:
            Connect through the configured tunnel device.
        """

        zi_logger.print_context()

        try:
            host = self.__db_obj.read_from_database(device, 'login_ip')
            username = self.__db_obj.read_from_database(device, 'username')
            password = self.__db_obj.read_from_database(device, 'password')
            port = self.__db_obj.read_from_database(device, 'port')
            ssh_tunnel = self.__db_obj.read_from_database(device, 'ssh_tunnel')
            
            if not ssh_tunnel:
                self.__open_connection(host=host, alias= device, timeout=10, port=port)
                self.__login(username, password)
                zi_logger.log(f"SSH connection established with {device}")
                return True

            #SSH Tunnel
            tunnel_device = self.__db_obj.read_from_database(device, "tunnel_device")
            if tunnel_device not in SshInterface.__objects:
                raise RuntimeError(f'SSH to the Tunneling Parent device "{tunnel_device}" has to be extablished first')
            
            tunnel_client = SshInterface.__objects[tunnel_device]["client"]
            transport = tunnel_client.get_transport()
            if transport is None or not transport.is_active():
                raise RuntimeError(f"{tunnel_device} transport is not active")

            channel = transport.open_channel("direct-tcpip",(host, port),("127.0.0.1", 0),timeout=5)
            if channel is None:
                raise RuntimeError(f"Could not create SSH tunnel to {device}")

            zi_logger.log(f"Creating SSH tunnel: {tunnel_device} --> {device}")
            self.__open_connection(host = host,
                                   alias = device,
                                   timeout = 10,
                                   port = port,
                                   sock=channel)
            self.__login(username , password)
            zi_logger.log(f"SSH connection established with {device}")
            return True

        except Exception as err:
            zi_logger.log(f"could not login with {device}")
            zi_logger.log(f"ERROR: {err}")
            return False
        

    def switch_connection(self,
                          alias: str):
        """
        Switch the SSH connection into the specifice device

        ``alias`` the reference name assigned to the ssh client object
        of the remote device

        ``raise`` a runtime error if the reference alias name is not
        present in the database dictionary

        Example:
        | Switch To Connection | ap                        |
        | Switch To Connection | ap_lan_client_01          |
        | Switch To Connection | ap_wlan_client_02         |
        | Switch To Connection | repeate_01
        | Switch To Connection | repeater_01_lan_client_01 |
        """
        zi_logger.print_context()
        if alias not in SshInterface.__objects:
            raise RuntimeError(f"Given alias - {alias} is not present")        
        zi_logger.log(f"utils.ssh_interface.switch_connection : device - {alias}")
        SshInterface.__alias = alias

    
    def execute_command(self, # pylint: disable=R0913
                        command: str,
                        return_stdout: bool =True,
                        return_stderr: bool =False,
                        return_rc:bool =False,
                        blocking_call:bool =True):
        """
        Execute the given command in the remote device

        we may use ``Swtich Connection`` keyword to select the remote device

        ``command`` is the command to be executed in the remote device
        and ``return_stdout`` is to return the stdout of the command executed
        and ``return_stderr`` is to return the stderr of the command executed
        and ``return_rc`` is to return the return code of the command executed
        and ``blocking_call`` is to select whether the command has to be executed
        in background or not

        ``returns`` the combination of stdout, std_err, and return code based on
        the arguments provided

        ``raise`` a runtime error if could not execute the command in remote device

        Example:
        | Execute Ssh Command | ls -l /                        | return_stderr=True |
        | Execute Ssh Command | uci set wireless.0.channel=11  | return_rc = True   |
        """
        zi_logger.print_context()
        device = SshInterface.__alias
        if not self.is_device_alive(device):
            raise RuntimeError(f"Could not execute the command since the device {device} is not alive")
        try:
            out = None
            if blocking_call:
                _stdin, stdout, stderr = SshInterface.__objects[SshInterface.__alias]['client'].exec_command(command, timeout=10)
                output = stdout.read().decode('utf-8').strip()
                error = stderr.read().decode('utf-8').strip()
                return_code = stdout.channel.recv_exit_status()
                if return_stdout and not return_stderr and not return_rc:
                    out = output
                elif return_stdout and not return_stderr and return_rc:
                    out =  output, return_code
                elif return_stdout and return_stderr and not return_rc:
                    out =  output, error
                elif return_stdout and return_stderr and return_rc:
                    out =  output, error, return_code
                elif not return_stdout and not return_stderr and not return_rc:
                    out =  None
                elif not return_stdout and not return_stderr and return_rc:
                    out =  return_code
                elif not return_stdout and return_stderr and not return_rc:
                    out =  error
                elif not return_stdout and return_stderr and return_rc:
                    out =  error, return_code
            if not blocking_call:
                channel = SshInterface.__objects[SshInterface.__alias]['client'].get_transport().open_session()
                channel.exec_command(command)
                out =  None
            zi_logger.log(f"utils.ssh_interface.execute_command - OUTPUT : {out}")
            return out
        except Exception as err: # pylint: disable=broad-except
            zi_logger.log(f"Could not execute the command - {command}")
            raise RuntimeError(err) from err

    
    def close_all_connections(self):
        """
        Close all the established SSH connections

        Example:
        | Close All Ssh Connections |
        """
        zi_logger.print_context()
        aliases = SshInterface.__objects.keys()
        if len(aliases) >= 1:
            for alias in aliases:
                try:
                    SshInterface.__objects[alias]['client'].close()
                    SshInterface.__objects.pop(alias, None)
                except Exception as err: # pylint: disable=broad-except
                    zi_logger.log(f"ERROR: {err}")
                    zi_logger.log(f"Could not close the ssh connection for the alias : {alias}")
            SshInterface.__objects = {}

    
    def close_connection(self,
                         alias: str):
        """
        Close a SSH connection established with a device

        ``alias`` is the reference name assigned to the device

        Example:
        | Close Ssh Connection | ap                         |
        | Close Ssh Connection | repeater_01                |
        | Close Ssh Connection | ap_wlan_client_01          |
        | Close Ssh Connection | repeater_01_wlan_client_01 |
        """
        zi_logger.print_context()
        try:
            SshInterface.__objects[alias]['client'].close()
            #del SshInterface.__objects[alias]
            SshInterface.__objects.pop(alias, None)
        except Exception as err: # pylint: disable=broad-except
            zi_logger.log(f"ERROR: {err}")
            zi_logger.log(f"Could not close the ssh connection for the alias : {alias}")

    
    def get_file(self,
                 remote_file: str,
                 local_file: str):
        """
        Retrieve a file from the remote machine.

        ``remote_file`` location of the source file in the remote machine
        and ``local_file`` destination path in the local machine

        ``raise`` runtime error if SFTP is not created or not
                  able to copy the file

        Example:
        | Ssh Get File | /home/user/output.xml | /home/user/local/output
        """
        zi_logger.print_context()
        scp = SCPClient(SshInterface.__objects[SshInterface.__alias]['client'].get_transport())
        if scp is None:
            raise Exception("Error: SFTP Not Created")
        try:
            scp.get(remote_path=remote_file,
                    local_path=local_file,
                    recursive=False)
        except Exception as err:
            zi_logger.log(f"Error: {err}")
            raise RuntimeError(f"Could not copy the file - {remote_file} \
                               from the device - {SshInterface.__alias}") from err
        finally:
            scp.close()

    
    def put_file(self,
                 local_file: str,
                 remote_file: str):
        """
        Transfer a file from the local machine to the remote machine.

        ``local_file`` location of the source file in the local machine
        and ``remote_file`` destination file path in the remote machine

        ``raise`` runtime error if SFTP is not created or
                  not able to copy the file

        Example:
        | Ssh Put File | /home/user/top.sh | /home/user/remote/scripts
        """
        zi_logger.print_context()
        scp = SCPClient(SshInterface.__objects[SshInterface.__alias]['client'].get_transport())
        if scp is None:
            raise Exception("Error: SFTP Not Created")
        try:
            scp.put(local_file,
                    remote_file,
                    recursive=False)
        except Exception as err:
            zi_logger.log(f"Error: {err}")
            raise Exception(f"Could not copy the file - {local_file} into \
                            the device - {SshInterface.__alias}") from err
        finally:
            scp.close()
        
