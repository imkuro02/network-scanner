#sudo nmap -sn 10.0.0.1/24
#https://stackoverflow.com/questions/34315334/printing-hostnames-of-pcs-on-the-network-using-nmap-python
#socket.gethostbyaddr("10.0.0.15") 

import datetime

begin_time = datetime.datetime.now()

#import nmap3
#nmap = nmap3.Nmap()

import socket

def get_own_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return(ip)

def get_devices():
    my_ip = get_own_ip()
    ip_start = my_ip[:my_ip.rfind('.')]
    #devices = nmap.scan_top_ports(f'{my_ip}/24')
    #devices = ipaddress.ip_network(f'{my_ip}/24')
    devices = []
    for i in range(0,255+1):
        try:
            devices.append(socket.gethostbyaddr(f'{ip_start}.{i}'))
        except:
            pass

    for d in devices:
        print(d[2],d[0])
    

    '''
    device_names=[]
    for d in devices:
        try:
            print(d,socket.gethostbyaddr(str(d)))
            device_names.append(d)
        except Exception as e:
            print(d,' - ',e)

    return()
    '''


if __name__ == '__main__':
    get_devices()    

    print(datetime.datetime.now() - begin_time)

