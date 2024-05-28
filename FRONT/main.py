########################################################################
## QT GUI BY SPINN TV(YOUTUBE)
########################################################################
import datetime
########################################################################
## IMPORTS
########################################################################
import os
import platform
import shutil
import sys
########################################################################
# IMPORT GUI FILE
from src.ui_interface import *
########################################################################
from src.fnct import *
import psutil
from multiprocessing import cpu_count
import clr  # the pythonnet module

clr.AddReference("LibreHardwareMonitorLib")
from LibreHardwareMonitor import Hardware
########################################################################
# IMPORT Custom widgets
from Custom_Widgets import *
from Custom_Widgets.QAppSettings import QAppSettings
########################################################################
platforms={
    'linux': 'Linux',
    'linux1': 'Linux',
    'linux2': 'Linux',
    'darwin': 'Mac x',
    'win32': 'Windows',
}
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
        self.power()
        self.cpu_ram()
        self.system_info()
        self.processes()
        self.storage()
        self.sensor()
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
    def power(self):
        computer = Hardware.Computer()
        computer.IsCpuEnabled = True
        computer.IsGpuEnabled = True
        computer.Open()

        total_cpu_power = 0.0
        total_igpu_power = 0.0
        total_dgpu_power = 0.0
        # Iterate through hardware components
        for hardware in computer.Hardware:
            if hardware.HardwareType in (
                    Hardware.HardwareType.Cpu, Hardware.HardwareType.GpuNvidia, Hardware.HardwareType.GpuAmd,
                    Hardware.HardwareType.GpuIntel):
                hardware.Update()
                for sensor in hardware.Sensors:
                    if sensor.SensorType == Hardware.SensorType.Power:
                        value = sensor.Value

                        # Sum the CPU power values
                        if hardware.HardwareType == Hardware.HardwareType.Cpu:
                            total_cpu_power += value
                        # Identify iGPU and dGPU power values for Intel and AMD
                        elif hardware.HardwareType == Hardware.HardwareType.GpuIntel:
                            if "UHD" in hardware.Name or "Iris" in hardware.Name:
                                total_igpu_power += value
                            else:
                                total_dgpu_power += value
                        elif hardware.HardwareType == Hardware.HardwareType.GpuAmd:
                            if "Vega" in hardware.Name or "Radeon Graphics" in hardware.Name or "M" in hardware.Name or "S" in hardware.Name:
                                total_igpu_power += value
                            else:
                                total_dgpu_power += value
                        # Sum the dGPU power values for Nvidia
                        elif hardware.HardwareType == Hardware.HardwareType.GpuNvidia:
                            total_dgpu_power += value

        computer.Close()

        self.ui.cpu_consume.setText(f"{total_cpu_power:.2f}")
        if total_igpu_power > 0:
            self.ui.igpu_consume.setText(f"{total_igpu_power:.2f}")
        self.ui.gpu_consume.setText(f"{total_dgpu_power:.2f}")
        avg=(total_dgpu_power+total_cpu_power)/2
        self.ui.avg_consumed.setText("{:.2f}".format(avg))
        self.ui.power_progress.spb_setMinimum((0,0,0))
        self.ui.power_progress.spb_setMaximum((100,100,300))
        self.ui.power_progress.spb_setValue((total_cpu_power,total_dgpu_power,avg))
        self.ui.power_progress.spb_lineColor(((6,233,38),(6,201,233),(233,6,201)))
        self.ui.power_progress.spb_setInitialPos(('West','West','West'))
        self.ui.power_progress.spb_lineWidth(15)
        self.ui.power_progress.spb_lineStyle(('SolidLine','SolidLine','SolidLine'))
        self.ui.power_progress.spb_lineCap(('RoundCap','RoundCap','RoundCap'))
        self.ui.power_progress.spb_setPathHidden(True)
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
        self.ui.system_time.setText(str(time))
        date= datetime.datetime.now().strftime("%Y-%m-%d")
        self.ui.system_date.setText(str(date))

        self.ui.system_machine.setText(platform.machine())
        self.ui.system_version.setText(platform.version())
        self.ui.system_platform.setText(platform.platform())
        self.ui.system_system.setText(platform.system())
        self.ui.system_processor.setText(platform.processor())

    def create_table_widget(self,rowPosition,columnPosition,text,tablename):
        qtablewidgetitem=QTableWidgetItem()
        getattr(self.ui, tablename).setItem(rowPosition,columnPosition,qtablewidgetitem)
        qtablewidgetitem=getattr(self.ui, tablename).item(rowPosition,columnPosition)
        qtablewidgetitem.setText(text)

    def processes(self):
        for x in psutil.pids():
            rowPosition=self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(rowPosition)
            try:
                process=psutil.Process(x)

                self.create_table_widget(rowPosition,0,str(process.pid),"tableWidget")
                self.create_table_widget(rowPosition, 1, process.name(), "tableWidget")
                self.create_table_widget(rowPosition, 2, process.status(), "tableWidget")
                self.create_table_widget(rowPosition, 3, str(datetime.datetime.utcfromtimestamp(process.create_time()).strftime('%Y-%m-%d %H:%M:%S')), "tableWidget")
                suspend_btn=QPushButton(self.ui.tableWidget)
                suspend_btn.setText("Suspend")
                suspend_btn.setStyleSheet("color: brown")
                self.ui.tableWidget.setCellWidget(rowPosition, 4, suspend_btn)

                resume_btn=QPushButton(self.ui.tableWidget)
                resume_btn.setText("Resume")
                resume_btn.setStyleSheet("color: green")
                self.ui.tableWidget.setCellWidget(rowPosition, 5, resume_btn)

                terminate_btn=QPushButton(self.ui.tableWidget)
                terminate_btn.setText("Terminate")
                terminate_btn.setStyleSheet("color: orange")
                self.ui.tableWidget.setCellWidget(rowPosition, 6, terminate_btn)

                kill_btn=QPushButton(self.ui.tableWidget)
                kill_btn.setText("Kill")
                kill_btn.setStyleSheet("color: red")
                self.ui.tableWidget.setCellWidget(rowPosition, 7, kill_btn)
            except Exception as e:
                print(e)
        self.ui.activity_search.textChanged.connect(self.findName)
    def findName(self):
        name=self.ui.activity_search.text().lower()
        for row in range(self.ui.tableWidget.rowCount()):
            item=self.ui.tableWidget.item(row,1)
            self.ui.tableWidget.setRowHidden(row,name not in item.text().lower())
    def storage(self):
        global platforms
        storage_device=psutil.disk_partitions(all=False)
        z=0
        for x in storage_device:
            rowPosition=self.ui.storageTable.rowCount()
            self.ui.storageTable.insertRow(rowPosition)
            self.create_table_widget(rowPosition,0,x.device,"storageTable")
            self.create_table_widget(rowPosition, 1, x.mountpoint, "storageTable")
            self.create_table_widget(rowPosition, 2, x.fstype, "storageTable")
            self.create_table_widget(rowPosition, 3, x.opts, "storageTable")

            if sys.platform == 'linux' or sys.platform == 'linux1' or sys.platform == 'linux2':
                self.create_table_widget(rowPosition, 4, str(x.maxfile), "storageTable")
                self.create_table_widget(rowPosition, 5, str(x.maxpath), "storageTable")
            else:
                self.create_table_widget(rowPosition, 4, "Function not available on " + platforms[sys.platform], "storageTable")
                self.create_table_widget(rowPosition, 5,"Function not available on " + platforms[sys.platform], "storageTable")
            disk_usage = shutil.disk_usage(x.mountpoint)
            self.create_table_widget(rowPosition, 6,str("{:.2f}".format(disk_usage.total / (1024*1024*1024))) + " GB", "storageTable")
            self.create_table_widget(rowPosition,7,str("{:.2f}".format(disk_usage.free / (1024*1024*1024))) + " GB", "storageTable")
            self.create_table_widget(rowPosition,8,str("{:.2f}".format(disk_usage.used / (1024*1024*1024))) + " GB", "storageTable")

            full_disk=(disk_usage.used / disk_usage.total) * 100
            progressBar=QProgressBar(self.ui.storageTable)
            progressBar.setObjectName(u"progressBar")
            progressBar.setValue(full_disk)
            self.ui.storageTable.setCellWidget(rowPosition, 9, progressBar)

    def sensor(self):
        computer = Hardware.Computer()
        computer.IsCpuEnabled = True
        computer.IsGpuEnabled = True
        computer.Open()

        cpu_temps = {}
        gpu_temps = {}
        cpu_average_temps = []
        tjmax_temps = {}

        # Iterate through hardware components
        for hardware in computer.Hardware:
            if hardware.HardwareType in (
                    Hardware.HardwareType.Cpu, Hardware.HardwareType.GpuNvidia, Hardware.HardwareType.GpuAmd,
                    Hardware.HardwareType.GpuIntel):
                hardware.Update()
                for sensor in hardware.Sensors:
                    # Exclude power sensors
                    if sensor.SensorType == Hardware.SensorType.Temperature:
                        temp_value = sensor.Value
                        sensor_name = sensor.Name
                        # Handle CPU Average sensor specifically
                        if hardware.HardwareType == Hardware.HardwareType.Cpu:
                            if sensor_name == "CPU Average":
                                cpu_average_temps.append(temp_value)
                            elif "Tjmax" in sensor_name:
                                if sensor_name not in tjmax_temps:
                                    tjmax_temps[sensor_name] = [temp_value]
                                else:
                                    tjmax_temps[sensor_name].append(temp_value)
                            else:
                                if sensor_name not in cpu_temps:
                                    cpu_temps[sensor_name] = [temp_value]
                                else:
                                    cpu_temps[sensor_name].append(temp_value)
                        # Gather GPU temperature readings
                        elif hardware.HardwareType in (Hardware.HardwareType.GpuIntel, Hardware.HardwareType.GpuAmd, Hardware.HardwareType.GpuNvidia):
                            if "Tjmax" in sensor_name:
                                if sensor_name not in tjmax_temps:
                                    tjmax_temps[sensor_name] = [temp_value]
                                else:
                                    tjmax_temps[sensor_name].append(temp_value)
                            else:
                                if sensor_name not in gpu_temps:
                                    gpu_temps[sensor_name] = [temp_value]
                                else:
                                    gpu_temps[sensor_name].append(temp_value)

        computer.Close()

        # Calculate average temperature per Tjmax sensor
        tjmax_avg_temps = {sensor_name: sum(temp_list) / len(temp_list) for sensor_name, temp_list in tjmax_temps.items()}

        # Create the table for all temperatures
        row = self.ui.storageTable.rowCount()
        # Populate CPU temperatures
        for sensor_name, temps in cpu_temps.items():
            current_temp = temps[-1]
            avg_temp = sum(temps) / len(temps)
            self.create_table_widget(row, 0, sensor_name, 'sensors_table')
            self.create_table_widget(row, 1, f"{current_temp:.2f}", 'sensors_table')
            self.create_table_widget(row, 2, f"{min(temps):.2f}", 'sensors_table')
            self.create_table_widget(row, 3, f"{max(temps):.2f}", 'sensors_table')
            self.create_table_widget(row, 4, f"{avg_temp:.2f}", 'sensors_table')
            row += 1
        if cpu_average_temps:
            self.create_table_widget(row, 0, "CPU Average", 'sensors_table')
            self.create_table_widget(row, 1, f"{cpu_average_temps[-1]:.2f}", 'sensors_table')
            self.create_table_widget(row, 2, f"{min(cpu_average_temps):.2f}", 'sensors_table')
            self.create_table_widget(row, 3, f"{max(cpu_average_temps):.2f}", 'sensors_table')
            self.create_table_widget(row, 4, f"{sum(cpu_average_temps) / len(cpu_average_temps):.2f}", 'sensors_table')
            row += 1
        # Populate Tjmax temperatures
        for sensor_name, temps in tjmax_temps.items():
            current_temp = temps[-1]
            avg_temp = sum(temps) / len(temps)
            self.create_table_widget(row, 0, sensor_name, 'sensors_table')
            self.create_table_widget(row, 1, f"{current_temp:.2f}", 'sensors_table')
            self.create_table_widget(row, 2, f"{min(temps):.2f}", 'sensors_table')
            self.create_table_widget(row, 3, f"{max(temps):.2f}", 'sensors_table')
            self.create_table_widget(row, 4, f"{avg_temp:.2f}", 'sensors_table')
            row += 1
        # Populate GPU temperatures
        for sensor_name, temps in gpu_temps.items():
            current_temp = temps[-1]
            avg_temp = sum(temps) / len(temps)
            self.create_table_widget(row, 0, sensor_name, 'sensors_table')
            self.create_table_widget(row, 1, f"{current_temp:.2f}", 'sensors_table')
            self.create_table_widget(row, 2, f"{min(temps):.2f}", 'sensors_table')
            self.create_table_widget(row, 3, f"{max(temps):.2f}", 'sensors_table')
            self.create_table_widget(row, 4, f"{avg_temp:.2f}", 'sensors_table')
            row += 1

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
