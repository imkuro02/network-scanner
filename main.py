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

    def __init__(self, MainWindow, scanning = True, threads = 8, scan_range = 255, devices = []):
        self.MainWindow = MainWindow
        self.scanning = scanning
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
                self.devices.append(device)
                self.MainWindow.addItem(device_ip,device_name)
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

        for thread in created_threads:
            thread.join()

        self.scanning = False # set scanning to false when finished

def runScan(MainWindow):
    begin_time = datetime.datetime.now()
    MainWindow.pushButton.setEnabled(False)
    scan = Scanner(MainWindow) # num o' threads and range
    scan.start()
    devices = scan.devices # sorted(scan.devices)
    for d in devices:
        print(f'{d["ip"]}/{d["name"]}')

    print('full scan time:', datetime.datetime.now() - begin_time)

    MainWindow.pushButton.setEnabled(True)
    return(None)

class Ui_MainWindow(object):
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

    def addItem(self, name='', ip=''):
        _translate = QtCore.QCoreApplication.translate
        '''
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        self.treeWidget.topLevelItem(0).setText(0, _translate("MainWindow", "Phone"))
        self.treeWidget.topLevelItem(0).setText(1, _translate("MainWindow", "10.0.0.2"))
        '''
        item = QtWidgets.QTreeWidgetItem(self.treeWidget, [name, ip])
        self.treeWidget.addTopLevelItem(item)
        #print(name,ip)

    def startScan(self): # runScan disbles button until done scanning
        self.treeWidget.clear()
        print('starting scan')
        t = Thread(target=runScan,args=(self,)) # passing in self object
        t.daemon = True
        t.start() 
        #runScan(self)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

        self.treeWidget.headerItem().setText(0, _translate("MainWindow", "Name"))
        self.treeWidget.headerItem().setText(1, _translate("MainWindow", "IP"))

        self.treeWidget.clear() # used to clear all items

        self.pushButton.clicked.connect(self.startScan)

        #self.pushButton.clicked.connect(lambda : self.addItem('l','l'))
        #__sortingEnabled = self.treeWidget.isSortingEnabled()
        #self.treeWidget.setSortingEnabled(False)
        #self.treeWidget.topLevelItem(0).setText(0, _translate("MainWindow", "Phone"))
        #self.treeWidget.topLevelItem(0).setText(1, _translate("MainWindow", "10.0.0.2"))
        #self.treeWidget.setSortingEnabled(__sortingEnabled)

        self.pushButton.setText(_translate("MainWindow", "Search"))
        #self.pushButton.clicked.connect()

        ip = get_own_ip()
        self.label.setText(_translate("MainWindow", f'device : [{ip}]'))

def rungui():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    # ui.startScan() # be ready
    MainWindow.show()
    sys.exit(app.exec())

if __name__ == "__main__":
  rungui()

