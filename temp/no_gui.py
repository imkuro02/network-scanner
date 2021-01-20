from threading import Thread
import scan 
from time import sleep
import datetime
from tkinter import *

begin_time = datetime.datetime.now()

class Scanner: # start scan.Scanner and grab results from scan.Scanner.devices
    def __init__(self, threads = 8):
        self.threads = threads

    def fetch(self,scanner):
        devices = scanner.devices
        logged_devices = []
        while True:
            sleep(.0001) # have to wait a little between every scan or else python will focus too much on this function
            '''
            devices = scanner.devices
            
            if len(logged_devices) != len(devices):
                logged_devices = devices
                print(devices[-1])

            '''
            for d in devices:
                if d not in logged_devices:
                    logged_devices.append(d)
                    print(f'{d["ip"]} - {d["name"]}')

            if not scanner.scanning:
                break


    def start(self):
        scanner = scan.Scanner(self.threads)

        t = Thread(target=self.fetch,args=(scanner,))
        t.daemon =True
        t.start()

        scanner.start()

        #print(scanner.devices)
        
        t.join()



if __name__ == '__main__':
    t = Scanner(8)
    t.start()

print(datetime.datetime.now() - begin_time)


