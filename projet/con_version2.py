from netmiko import *

def connection(host, username, password, comand):
        machine= {
                'device_type': 'linux',
                'host': host,
                'username': username,
                'password': password
                 }
        connect = ConnectHandler(**machine)
        output = connect.send_command(comand)
        connect.disconnect()
        return output