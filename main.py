from PyQt5 import QtCore, QtGui, QtWidgets
import sys

from threading import Thread
from time import sleep
import socket
import datetime

def get_own_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

class Scanner:

    def __init__(self, MainWindow, threads = 256, scan_range = 256, devices = []):
        self.MainWindow = MainWindow
        self.threads = threads
        self.scan_range = scan_range
        self.devices = devices

    def scan(self,thread_index):

        my_ip = get_own_ip() # my own ip, aka 10.0.0.15 in my case
        ip_start = my_ip[:my_ip.rfind('.')] # delete last digits so its 10.0.0]

        end_address = (list(range(
            thread_index,
            self.scan_range,
            self.threads)))

        for d in end_address:
            try:
                #sleep(1)
                device_name, _, device_ip = socket.gethostbyaddr(f'{ip_start}.{d}')
                device_ip = ''.join(c for c in device_ip if c not in '[]\'')
                device = {
                        'name' : device_name,
                        'ip' : device_ip
                        }
                #if self.start_time == self.MainWindow.last_scan:
                self.devices.append(device)
                self.MainWindow.addItem(device_ip,device_name)
                #else:
                #    print('late')
                '''
                self.devices.append(
                        socket.gethostbyaddr(f'10.0.0.{d}')
                        )
                '''
            except Exception as e:
                pass #print(e)
        #print(thread_index,'<=thread',self.threads,self.scan_range)


    def start(self):
        created_threads = []
        for index, thread in enumerate(range(self.threads),start=0):
            t = Thread(target=self.scan,args=(index,))
            t.daemon = True
            t.start()
            created_threads.append(t)
            #print(t.is_alive())
            
        new_progress = 0
        completion = self.threads
            
        def count(self):
            while True:
                sleep(.1)
                progress = 0
                for thread in created_threads:
                    #print(thread)
                    if not thread.is_alive():
                        progress += 1
                
                new_progress = int((progress / completion) * 100)
                #print(progress,new_progress)
                #self.MainWindow.addItem(str(progress),str(new_progress))
                self.MainWindow.progressBarUpdate(new_progress)
                #self.MainWindow.progressBar.setProperty("value", new_progress)
                
                if new_progress == 100:
                    print('break progress counting')
                    break
                #print(len(created_threads))
        
        t = Thread(target=count,args=(self,))
        t.daemon = True
        t.start()
      
        for thread in created_threads:
            #print(thread.is_alive())
            thread.join()
  
    def runScan(self,MainWindow):
        def thread():
            MainWindow.pushButton.setEnabled(False)
            self.start()
            MainWindow.pushButton.setEnabled(True)
        t = Thread(target=thread)
        t.daemon = True
        t.start()

class Ui_MainWindow(object):
    
    def addItem(self, name='', ip=''):
        _translate = QtCore.QCoreApplication.translate
        item = QtWidgets.QTreeWidgetItem(self.treeWidget, [name, ip])
        self.treeWidget.addTopLevelItem(item)
        #print(name,ip)

    def startScan(self): # runScan disbles button until done scanning
        print('starting scan')
        self.treeWidget.clear()
        self.scanner.runScan(self)

    def progressBarUpdate(self,val):
        self.progressBar.setProperty("value",val)
                

    def __init__(self,last_scan):
        self.scanner = Scanner(self)
        self.last_scan = last_scan
        print(self.last_scan)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(599, 400)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.treeWidget = QtWidgets.QTreeWidget(self.centralwidget)
        self.treeWidget.setGeometry(QtCore.QRect(10, 60, 581, 311))
        self.treeWidget.setAcceptDrops(False)
        self.treeWidget.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.treeWidget.setLineWidth(1)
        self.treeWidget.setIndentation(15)
        self.treeWidget.setRootIsDecorated(False)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.header().setVisible(True)
        self.treeWidget.header().setHighlightSections(False)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 10, 99, 38))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(120, 20, 441, 22))
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        self.progressBar = QtWidgets.QProgressBar(MainWindow)
        self.progressBar.setGeometry(QtCore.QRect(10, 371, 581, 20))
        self.progressBar.setProperty("value", 100)
        self.progressBar.setObjectName("progressBar")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.treeWidget.headerItem().setText(0, _translate("MainWindow", "IP"))
        self.treeWidget.headerItem().setText(1, _translate("MainWindow", "Name"))
        self.treeWidget.clear() # used to clear all items
        self.pushButton.clicked.connect(self.startScan)
        self.pushButton.setText(_translate("MainWindow", "Search"))
        ip = get_own_ip()
        self.label.setText(_translate("MainWindow", f'device : [{ip}]'))

def rungui():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(datetime.datetime.now())
    ui.setupUi(MainWindow)
    # ui.startScan() # be ready
    MainWindow.show()
    sys.exit(app.exec())

if __name__ == "__main__":
  rungui()

