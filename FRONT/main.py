########################################################################
## QT GUI BY SPINN TV(YOUTUBE)
########################################################################
import datetime
########################################################################
## IMPORTS
########################################################################
import os
import platform
import sys
########################################################################
# IMPORT GUI FILE
from src.ui_interface import *
########################################################################
from src.fnct import *
import psutil
from multiprocessing import cpu_count

########################################################################
# IMPORT Custom widgets
from Custom_Widgets import *
from Custom_Widgets.QAppSettings import QAppSettings
########################################################################

########################################################################
## MAIN WINDOW CLASS
########################################################################
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(50)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 92, 157, 550))
        self.ui.centralwidget.setGraphicsEffect(self.shadow)
        QSizeGrip(self.ui.size_grip)
        # Connecting buttons to their respective methods
        self.ui.minimize_button.clicked.connect(self.showMinimized)
        self.ui.close_button.clicked.connect(self.close)
        self.ui.resize_button.clicked.connect(self.restore_or_maximize_window)
        self.ui.CPU.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.cpu_memory))
        self.ui.power.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.Power))
        self.ui.Sysinfo.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.sysinfo))
        self.ui.Activities.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.activities))
        self.ui.Storage.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.storage))
        self.ui.Sensors.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.sensors))
        self.ui.Network.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.network))
        self.ui.Clientlist.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.clientslist))
        self.ui.Domain.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.Domain_status))
        self.clickPosition = QPoint()

        # Set mouse event handlers
        self.ui.header_frame.mousePressEvent = self.mousePressEvent
        self.ui.header_frame.mouseMoveEvent = self.moveWindow
        for w in self.ui.menu.findChildren(QPushButton):
            w.clicked.connect(self.applyButtonStyle)
        ########################################################################
        # APPLY JSON STYLESHEET
        ########################################################################
        loadJsonStyle(self, self.ui, jsonFiles={
            "json-styles/style.json"
        })

        #######################################################################
        # SHOW WINDOW
        #######################################################################
        self.show()
        self.battery()
        self.cpu_ram()
        self.system_info()
        ########################################################################
        # UPDATE APP SETTINGS LOADED FROM JSON STYLESHEET
        # ITS IMPORTANT TO RUN THIS AFTER SHOWING THE WINDOW
        # THIS PROCESS WILL RUN ON A SEPARATE THREAD WHEN GENERATING NEW ICONS
        # TO PREVENT THE WINDOW FROM BEING UNRESPONSIVE
        ########################################################################
        QAppSettings.updateAppSettings(self)

    def applyButtonStyle(self):
        for w in self.ui.menu.findChildren(QPushButton):
            if w.objectName() != self.sender().objectName():
                w.setStyleSheet("border-bottom: none;")

        self.sender().setStyleSheet("border-bottom: 2px solid;")
        return
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clickPosition = event.globalPos()

    def moveWindow(self, event):
        if not self.isMaximized():  # Only allow moving when not maximized
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.clickPosition)
                self.clickPosition = event.globalPos()
                event.accept()
    def secs2hours(selfself,secs):
        mm,ss=divmod(secs,60)
        hh,mm=divmod(mm,60)
        return "%d:%02d:%02d (H:M:S)" % (hh,mm,ss)
    def battery(self):
        battery = psutil.sensors_battery()
        if not hasattr(psutil, 'sensors_battery'):
            self.ui.battery_status.setText("Platform not supported")
        if battery is None:
            self.ui.battery_status.setText("Does not have battery")
        if battery.power_plugged:
            self.ui.battery_charge.setText(str(round(battery.percent, 2)) + "%")
            self.ui.battery_time_left.setText("N/A")
            if battery.percent < 100:
                self.ui.battery_status.setText("Charging")
            else:
                self.ui.battery_status.setText("Fully Charged")
            self.ui.battery_plugged.setText("Yes")
        else:
            self.ui.battery_charge.setText(str(round(battery.percent, 2)) + "%")
            self.ui.battery_time_left.setText(self.secs2hours(battery.secsleft))
            if battery.percent < 100:
                self.ui.battery_status.setText("Discharging")
            else:
                self.ui.battery_status.setText("Fully Charged")
            self.ui.battery_plugged.setText("No")
        self.ui.battery_usage.rpb_setMaximum(100)
        self.ui.battery_usage.rpb_setValue(battery.percent)
        self.ui.battery_usage.rpb_setBarStyle('Hybrid2')
        self.ui.battery_usage.rpb_setLineColor((255, 30, 99))
        self.ui.battery_usage.rpb_setPieColor((45, 74, 83))
        self.ui.battery_usage.rpb_setTextColor((255, 255, 255))
        self.ui.battery_usage.rpb_setInitialPos('West')
        self.ui.battery_usage.rpb_setTextFormat('Percentage')
        self.ui.battery_usage.rpb_setLineWidth(15)
        self.ui.battery_usage.rpb_setPathWidth(15)
        self.ui.battery_usage.rpb_setLineCap('RoundCap')
    def cpu_ram(self):
        totalRam= 1.0
        totalRam=psutil.virtual_memory()[0] * totalRam
        totalRam=totalRam/(1024*1024*1024)
        self.ui.total_ram.setText(str("{:.2f}".format(totalRam) + ' GB'))


        availableRam= 1.0
        availableRam= psutil.virtual_memory()[1] * availableRam
        availableRam=availableRam/(1024*1024*1024)
        self.ui.available_ram.setText(str("{:.2f}".format(availableRam) + ' GB'))

        ramUsages = psutil.virtual_memory().percent
        self.ui.ram_usage.setText("{:.2f}%".format(ramUsages))

        usedRam= 1.0
        usedRam= psutil.virtual_memory()[3] * usedRam
        usedRam=usedRam/(1024*1024*1024)
        self.ui.used_ram.setText(str("{:.2f}".format(usedRam) + ' GB'))

        ramFREE= 1.0
        ramFREE=psutil.virtual_memory()[4] * ramFREE
        ramFREE=ramFREE/(1024*1024*1024)
        self.ui.free_ram.setText(str("{:.2f}".format(ramFREE) + ' GB'))

        core=cpu_count()
        self.ui.cpu_cont.setText(str(core))

        cpuPer=psutil.cpu_percent()
        self.ui.cpu_per.setText(str(cpuPer) + "%")

        cpuMainCore=psutil.cpu_count(logical=False)
        self.ui.cpu_main_core.setText(str(cpuMainCore))


        self.ui.CPU_PROGRESS.rpb_setMaximum(100)
        self.ui.CPU_PROGRESS.rpb_setValue(cpuPer)
        self.ui.CPU_PROGRESS.rpb_setBarStyle('Hybrid2')
        self.ui.CPU_PROGRESS.rpb_setLineColor((255, 30, 99))
        self.ui.CPU_PROGRESS.rpb_setPieColor((45, 74, 83))
        self.ui.CPU_PROGRESS.rpb_setInitialPos('West')
        self.ui.CPU_PROGRESS.rpb_setTextFormat('Percentage')
        self.ui.CPU_PROGRESS.rpb_setTextFont('Asus Font')
        self.ui.CPU_PROGRESS.rpb_setLineWidth(15)
        self.ui.CPU_PROGRESS.rpb_setPathWidth(15)
        self.ui.CPU_PROGRESS.rpb_setLineCap('RoundCap')



        self.ui.RAM_PROGRESS.spb_setMinimum((0,0,0))
        self.ui.RAM_PROGRESS.spb_setMaximum((totalRam,totalRam,totalRam))
        self.ui.RAM_PROGRESS.spb_setValue((availableRam,usedRam,ramFREE))
        self.ui.RAM_PROGRESS.spb_lineColor(((6,233,38),(6,201,233),(233,6,201)))
        self.ui.RAM_PROGRESS.spb_setInitialPos(('West','West','West'))
        self.ui.RAM_PROGRESS.spb_lineWidth(15)
        self.ui.RAM_PROGRESS.spb_lineStyle(('SolidLine','SolidLine','SolidLine'))
        self.ui.RAM_PROGRESS.spb_lineCap(('RoundCap','RoundCap','RoundCap'))
        self.ui.RAM_PROGRESS.spb_setPathHidden(True)
    def system_info(self):
        time=datetime.datetime.now().strftime("%I:%M:%S %p")
        self.ui.system_date.setText(str(time))
        date= datetime.datetime.now().strftime("%I:%M:%S %p")
        self.ui.system_time.setText(str(date))

        self.ui.system_machine.setText(platform.machine())
        self.ui.system_version.setText(platform.version())
        self.ui.system_platform.setText(platform.platform())
        self.ui.system_system.setText(platform.system())
        self.ui.system_processor.setText(platform.processor())


########################################################################
## EXECUTE APP
########################################################################
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ########################################################################
    ## 
    ########################################################################
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
########################################################################
## END===>
########################################################################  
