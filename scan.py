from threading import Thread
from time import sleep
import socket 
import datetime

begin_time = datetime.datetime.now()

class Scanner:
 
    def __init__(self,scanning = True, threads = 8, scan_range = 255, devices = []):
        self.scanning = scanning
        self.threads = threads
        self.scan_range = scan_range
        self.devices = devices
    
    def get_own_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return(ip)

    def scan(self,thread_index):
        
        my_ip = self.get_own_ip() # my own ip, aka 10.0.0.15 in my case
        ip_start = my_ip[:my_ip.rfind('.')] # delete last digits so its 10.0.0]

        end_address = (list(range(
            thread_index,
            self.scan_range,
            self.threads)))

        for d in end_address:
            try:
                
                device_name, _, device_ip = socket.gethostbyaddr(f'{ip_start}.{d}')
                device_ip = ''.join(c for c in device_ip if c not in '[]\'')
                device = {
                        'name' : device_name,
                        'ip' : device_ip
                        }
                self.devices.append(device)
                '''
                self.devices.append(
                        socket.gethostbyaddr(f'10.0.0.{d}')
                        )
                '''
            except:
                pass
        #print(thread_index,'<=thread',self.threads,self.scan_range)
        

    def start(self):
        created_threads = []
        for index, thread in enumerate(range(self.threads),start=0):
            t = Thread(target=self.scan,args=(index,))
            t.daemon = True
            t.start()
            created_threads.append(t)

        for thread in created_threads:
            thread.join()
            
        self.scanning = False # set scanning to false when finished

if __name__ == '__main__':
    a = Scanner(8,255) # num of threads, how far to check
    a.start()

    devices = a.devices#sorted(a.devices)
    # print(devices)
    for d in devices:
        print(f'{d["ip"]} - {d["name"]}')

    print(datetime.datetime.now() - begin_time)


