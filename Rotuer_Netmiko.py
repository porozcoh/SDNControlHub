
from netmiko import ConnectHandler

CSR1000v = {
'device_type' : 'cisco_xe',
'host' : '192.168.124.128',
'username' : 'cisco',
'password' : 'Cisco.12345',
}

#net_connect = ConnectHandler(**CSR1000v)
#net_connect.send_config_from_file(config_file="comandos.txt")
#net_connect.send_config_set
#output  = net_connect.send_command('show ip int brief')
#print(output)
#net_connect.disconnect()