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
import time
import traceback

########################################################################
# IMPORT GUI FILE
from src.ui_interface import *
########################################################################
from src.fnct import *
from PySide2.QtCore import QRunnable, Slot, QThreadPool
import psutil
from multiprocessing import cpu_count
import clr  # the pythonnet module
from time import sleep
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
class WorkerSignals(QObject):
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(int)

class Worker(QRunnable):
    def __init__(self, function, args=(), kwargs=None):
        super().__init__()
        self.function = function
        self.args = args
        self.kwargs = kwargs or {}
        self.signals = WorkerSignals()
        self.kwargs['progress_callback'] = self.signals.progress

    @Slot()
    def run(self):
        try:
            result = self.function(*self.args, **self.kwargs)
        except Exception as e:
            traceback.print_exc()
            self.signals.error.emit((type(e), e, traceback.format_exc()))
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()
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
        self.threadpool = QThreadPool()
        self.show()
        #self.power()
        #self.cpu_ram()
        #self.system_info()
        self.psutil_thread()
        #self.processes()
        #self.storage()
        #self.sensor()
        #self.network()
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
    def psutil_thread(self):
        '''
        worker = Worker(self.cpu_ram, args=(), kwargs={})
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)

        self.threadpool.start(worker)

        battery_worker=Worker(self.battery, args=(), kwargs={})
        battery_worker.signals.result.connect(self.print_output)
        battery_worker.signals.finished.connect(self.thread_complete)
        battery_worker.signals.progress.connect(self.progress_fn)
        self.threadpool.start(battery_worker)

        power_worker=Worker(self.power, args=(), kwargs={})
        power_worker.signals.result.connect(self.print_output)
        power_worker.signals.finished.connect(self.thread_complete)
        power_worker.signals.progress.connect(self.progress_fn)
        self.threadpool.start(power_worker)

        processes_worker=Worker(self.processes, args=(), kwargs={})
        processes_worker.signals.result.connect(self.print_output)
        processes_worker.signals.finished.connect(self.thread_complete)
        processes_worker.signals.progress.connect(self.progress_fn)
        self.threadpool.start(processes_worker)


        storage_worker=Worker(self.storage, args=(), kwargs={})
        storage_worker.signals.result.connect(self.print_output)
        storage_worker.signals.finished.connect(self.thread_complete)
        storage_worker.signals.progress.connect(self.progress_fn)
        self.threadpool.start(storage_worker)
      
        
        sensor_worker=Worker(self.sensor, args=(), kwargs={})
        sensor_worker.signals.result.connect(self.print_output)
        sensor_worker.signals.finished.connect(self.thread_complete)
        sensor_worker.signals.progress.connect(self.progress_fn)
        self.threadpool.start(sensor_worker)
        
        network_worker=Worker(self.update_network_info)
        network_worker.signals.result.connect(self.print_output)
        network_worker.signals.finished.connect(self.thread_complete)
        network_worker.signals.progress.connect(self.progress_fn)
        self.threadpool.start(network_worker)
        '''
    def print_output(self,s):
        print(s)
    def thread_complete(self):
        print("Thread Completed")
    def progress_fn(self,i):
        print("%d%% done" % i)
    def cpu_ram(self, progress_callback):
        while True:
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
            time.sleep(1)
    def power(self,progress_callback):
        while True:
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
                                if value is not None:
                                    total_cpu_power += value
                            # Identify iGPU and dGPU power values for Intel and AMD
                            elif hardware.HardwareType == Hardware.HardwareType.GpuIntel:
                                if "UHD" in hardware.Name or "Iris" in hardware.Name:
                                    total_igpu_power += value
                                else:
                                    total_dgpu_power += value
                            elif hardware.HardwareType == Hardware.HardwareType.GpuAmd:
                                if "Vega" in hardware.Name or "Radeon Graphics" in hardware.Name:
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
            avg = (total_dgpu_power + total_cpu_power) / 2
            self.ui.avg_consumed.setText("{:.2f}".format(avg))
            self.ui.power_progress.spb_setMinimum((0, 0, 0))
            self.ui.power_progress.spb_setMaximum((100, 100, 300))
            self.ui.power_progress.spb_setValue((total_cpu_power, total_dgpu_power, avg))
            self.ui.power_progress.spb_lineColor(((6, 233, 38), (6, 201, 233), (233, 6, 201)))
            self.ui.power_progress.spb_setInitialPos(('West', 'West', 'West'))
            self.ui.power_progress.spb_lineWidth(15)
            self.ui.power_progress.spb_lineStyle(('SolidLine', 'SolidLine', 'SolidLine'))
            self.ui.power_progress.spb_lineCap(('RoundCap', 'RoundCap', 'RoundCap'))
            self.ui.power_progress.spb_setPathHidden(True)
            time.sleep(1)
    def battery(self,progress_callback):
            battery = psutil.sensors_battery()
            if not hasattr(psutil, 'sensors_battery'):
                self.ui.battery_status.setText("Platform not supported")
            self.ui.battery_usage.rpb_setMaximum(100)

            self.ui.battery_usage.rpb_setBarStyle('Hybrid2')
            self.ui.battery_usage.rpb_setLineColor((255, 30, 99))
            self.ui.battery_usage.rpb_setPieColor((45, 74, 83))
            self.ui.battery_usage.rpb_setTextColor((255, 255, 255))
            self.ui.battery_usage.rpb_setInitialPos('West')
            self.ui.battery_usage.rpb_setTextFormat('Percentage')
            self.ui.battery_usage.rpb_setLineWidth(15)
            self.ui.battery_usage.rpb_setPathWidth(15)
            self.ui.battery_usage.rpb_setLineCap('RoundCap')
            if battery is None:
                self.ui.battery_status.setText("Does not have battery")
                self.ui.battery_usage.rpb_setValue(100)
            else:
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
                self.ui.battery_usage.rpb_setValue(battery.percent)
            time.sleep(1)

    def secs2hours(selfself,secs):
        mm,ss=divmod(secs,60)
        hh,mm=divmod(mm,60)
        return "%d:%02d:%02d (H:M:S)" % (hh,mm,ss)

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
#####################################################
#               NU FUNCTIONEAZA                     #
#####################################################
    def processes(self,progress_callback):
        while True:
            current_pids = set(psutil.pids())
            existing_pids = set()

            # Update existing processes
            for row in range(self.ui.tableWidget.rowCount()):
                pid_item = self.ui.tableWidget.item(row, 0)
                if pid_item is None:
                    continue
                pid = int(pid_item.text())
                existing_pids.add(pid)
                if pid in current_pids:
                    try:
                        process = psutil.Process(pid)
                        self.ui.tableWidget.item(row, 1).setText(process.name())
                        self.ui.tableWidget.item(row, 2).setText(process.status())
                        self.ui.tableWidget.item(row, 3).setText(
                            datetime.datetime.utcfromtimestamp(process.create_time()).strftime('%Y-%m-%d %H:%M:%S'))
                    except Exception as e:
                        print(e)

            # Add new processes
            new_pids = current_pids - existing_pids
            for pid in new_pids:
                rowPosition = self.ui.tableWidget.rowCount()
                self.ui.tableWidget.insertRow(rowPosition)
                try:
                    process = psutil.Process(pid)
                    self.create_table_widget(rowPosition, 0, str(process.pid), "tableWidget")
                    self.create_table_widget(rowPosition, 1, process.name(), "tableWidget")
                    self.create_table_widget(rowPosition, 2, process.status(), "tableWidget")
                    self.create_table_widget(rowPosition, 3,
                                             datetime.datetime.utcfromtimestamp(process.create_time()).strftime(
                                                 '%Y-%m-%d %H:%M:%S'), "tableWidget")
                    self.add_buttons(rowPosition)
                except Exception as e:
                    print(e)
            time.sleep(10)

    def findName(self):
        name = self.ui.activity_search.text().lower()
        for row in range(self.ui.tableWidget.rowCount()):
            item = self.ui.tableWidget.item(row, 1)
            self.ui.tableWidget.setRowHidden(row, name not in item.text().lower())

    def add_buttons(self, rowPosition):
        suspend_btn = QPushButton("Suspend")
        suspend_btn.setStyleSheet("color: brown")
        self.ui.tableWidget.setCellWidget(rowPosition, 4, suspend_btn)

        resume_btn = QPushButton("Resume")
        resume_btn.setStyleSheet("color: green")
        self.ui.tableWidget.setCellWidget(rowPosition, 5, resume_btn)

        terminate_btn = QPushButton("Terminate")
        terminate_btn.setStyleSheet("color: orange")
        self.ui.tableWidget.setCellWidget(rowPosition, 6, terminate_btn)

        kill_btn = QPushButton("Kill")
        kill_btn.setStyleSheet("color: red")
        self.ui.tableWidget.setCellWidget(rowPosition, 7, kill_btn)
    def suspend_process(self, process):
        try:
            process.suspend()
            print(f"Process {process.pid} suspended")
        except Exception as e:
            print(f"Error suspending process {process.pid}: {e}")

    def resume_process(self, process):
        try:
            process.resume()
            print(f"Process {process.pid} resumed")
        except Exception as e:
            print(f"Error resuming process {process.pid}: {e}")

    def terminate_process(self, process):
        try:
            process.terminate()
            print(f"Process {process.pid} terminated")
        except Exception as e:
            print(f"Error terminating process {process.pid}: {e}")

    def kill_process(self, process):
        try:
            process.kill()
            print(f"Process {process.pid} killed")
        except Exception as e:
            print(f"Error killing process {process.pid}: {e}")

    def add_storage_row(self, x, rowPosition):
        self.create_table_widget(rowPosition, 0, x.device, "storageTable")
        self.create_table_widget(rowPosition, 1, x.mountpoint, "storageTable")
        self.create_table_widget(rowPosition, 2, x.fstype, "storageTable")
        self.create_table_widget(rowPosition, 3, x.opts, "storageTable")

        if sys.platform.startswith('linux'):
            self.create_table_widget(rowPosition, 4, str(x.maxfile), "storageTable")
            self.create_table_widget(rowPosition, 5, str(x.maxpath), "storageTable")
        else:
            platform_msg = f"Function not available on {platforms.get(sys.platform, 'this platform')}"
            self.create_table_widget(rowPosition, 4, platform_msg, "storageTable")
            self.create_table_widget(rowPosition, 5, platform_msg, "storageTable")

        disk_usage = shutil.disk_usage(x.mountpoint)
        self.create_table_widget(rowPosition, 6, f"{disk_usage.total / (1024 ** 3):.2f} GB", "storageTable")
        self.create_table_widget(rowPosition, 7, f"{disk_usage.free / (1024 ** 3):.2f} GB", "storageTable")
        self.create_table_widget(rowPosition, 8, f"{disk_usage.used / (1024 ** 3):.2f} GB", "storageTable")

        full_disk = (disk_usage.used / disk_usage.total) * 100
        progressBar = QProgressBar(self.ui.storageTable)
        progressBar.setObjectName(u"progressBar")
        progressBar.setValue(full_disk)
        self.ui.storageTable.setCellWidget(rowPosition, 9, progressBar)

    def storage(self, progress_callback):
        self.storage_device = psutil.disk_partitions(all=False)
        for x in self.storage_device:
            rowPosition = self.ui.storageTable.rowCount()
            self.ui.storageTable.insertRow(rowPosition)
            self.add_storage_row(x, rowPosition)

    #####################################################
    #               NU FUNCTIONEAZA                     #
    #####################################################
    def update_storage(self):
        self.ui.storageTable.setRowCount(0)  # Clear the table
        self.storage()  # Re-populate the table
    def create_table_widget(self,rowPosition,columnPosition,text,tablename):
        qtablewidgetitem=QTableWidgetItem()
        getattr(self.ui, tablename).setItem(rowPosition,columnPosition,qtablewidgetitem)
        qtablewidgetitem=getattr(self.ui, tablename).item(rowPosition,columnPosition)
        qtablewidgetitem.setText(text)
    def update_sensor_row(self, sensor_name, temps, row):
        current_temp = temps[-1]
        avg_temp = sum(temps) / len(temps)
        self.create_table_widget(row, 0, sensor_name, 'sensors_table')
        self.create_table_widget(row, 1, f"{current_temp:.2f}", 'sensors_table')
        self.create_table_widget(row, 2, f"{min(temps):.2f}", 'sensors_table')
        self.create_table_widget(row, 3, f"{max(temps):.2f}", 'sensors_table')
        self.create_table_widget(row, 4, f"{avg_temp:.2f}", 'sensors_table')

    def sensor(self, progress_callback):
        try:
            computer = Hardware.Computer()
            computer.IsCpuEnabled = True
            computer.IsGpuEnabled = True
            computer.Open()

            cpu_temps = {}
            gpu_temps = {}
            cpu_average_temps = []
            tjmax_temps = {}

            while True:
                try:
                    for hardware in computer.Hardware:
                        if hardware.HardwareType in (Hardware.HardwareType.Cpu, Hardware.HardwareType.GpuNvidia,
                                                     Hardware.HardwareType.GpuAmd, Hardware.HardwareType.GpuIntel):
                            hardware.Update()
                            for sensor in hardware.Sensors:
                                if sensor.SensorType == Hardware.SensorType.Temperature and sensor.Value is not None:
                                    temp_value = sensor.Value
                                    sensor_name = sensor.Name

                                    if hardware.HardwareType == Hardware.HardwareType.Cpu:
                                        if sensor_name == "CPU Average":
                                            cpu_average_temps.append(temp_value)
                                        elif "Tjmax" in sensor_name:
                                            tjmax_temps.setdefault(sensor_name, []).append(temp_value)
                                        else:
                                            cpu_temps.setdefault(sensor_name, []).append(temp_value)
                                    elif hardware.HardwareType in (Hardware.HardwareType.GpuIntel, Hardware.HardwareType.GpuAmd,
                                                                   Hardware.HardwareType.GpuNvidia):
                                        if "Tjmax" in sensor_name:
                                            tjmax_temps.setdefault(sensor_name, []).append(temp_value)
                                        else:
                                            gpu_temps.setdefault(sensor_name, []).append(temp_value)

                    # Ensure updates to the table are done in the main thread
                    self.ui.sensors_table.setRowCount(0)
                    row = 0
                    for sensor_name, temps in cpu_temps.items():
                        self.ui.sensors_table.insertRow(row)
                        self.update_sensor_row(sensor_name, temps, row)
                        row += 1
                    if cpu_average_temps:
                        self.ui.sensors_table.insertRow(row)
                        self.update_sensor_row("CPU Average", cpu_average_temps, row)
                        row += 1

                    for sensor_name, temps in tjmax_temps.items():
                        self.ui.sensors_table.insertRow(row)
                        self.update_sensor_row(sensor_name, temps, row)
                        row += 1

                    for sensor_name, temps in gpu_temps.items():
                        self.ui.sensors_table.insertRow(row)
                        self.update_sensor_row(sensor_name, temps, row)
                        row += 1

                    time.sleep(5)
                except Exception as e:
                    print(f"Error in monitoring loop: {e}")

        except Exception as e:
            print(f"Error initializing hardware monitor: {e}")
        finally:
            computer.Close()

    #######################################################
    #           NETWORK                                   #
    #######################################################
    def update_network_info(self,progress_callback):
        while True:
            self.update_net_if_stats()
            self.update_net_io_counters()
            self.update_net_if_addrs()
            self.update_net_connections()
            time.sleep(10)


    def update_net_if_stats(self):
        for x in psutil.net_if_stats():
            z = psutil.net_if_stats()
            rowPosition = self.ui.stats_table.rowCount()
            self.ui.stats_table.insertRow(rowPosition)
            self.create_table_widget(rowPosition, 0, x, "stats_table")
            self.create_table_widget(rowPosition, 1, str(z[x].isup), "stats_table")
            self.create_table_widget(rowPosition, 2, str(z[x].duplex), "stats_table")
            self.create_table_widget(rowPosition, 3, str(z[x].speed), "stats_table")
            self.create_table_widget(rowPosition, 4, str(z[x].mtu), "stats_table")


    def update_net_io_counters(self):
        for x in psutil.net_io_counters(pernic=True):
            z = psutil.net_io_counters(pernic=True)
            rowPosition = self.ui.IO_counters_table.rowCount()
            self.ui.IO_counters_table.insertRow(rowPosition)
            self.create_table_widget(rowPosition, 0, x, "IO_counters_table")
            self.create_table_widget(rowPosition, 1, str(z[x].bytes_sent), "IO_counters_table")
            self.create_table_widget(rowPosition, 2, str(z[x].bytes_recv), "IO_counters_table")
            self.create_table_widget(rowPosition, 3, str(z[x].packets_sent), "IO_counters_table")
            self.create_table_widget(rowPosition, 4, str(z[x].packets_recv), "IO_counters_table")
            self.create_table_widget(rowPosition, 5, str(z[x].errin), "IO_counters_table")
            self.create_table_widget(rowPosition, 6, str(z[x].errout), "IO_counters_table")
            self.create_table_widget(rowPosition, 7, str(z[x].dropin), "IO_counters_table")
            self.create_table_widget(rowPosition, 8, str(z[x].dropout), "IO_counters_table")


    def update_net_if_addrs(self):
        for x in psutil.net_if_addrs():
            z = psutil.net_if_addrs()
            for y in z[x]:
                rowPosition = self.ui.addresses_table.rowCount()
                self.ui.addresses_table.insertRow(rowPosition)
                self.create_table_widget(rowPosition, 0, str(x), "addresses_table")
                self.create_table_widget(rowPosition, 1, str(y.family), "addresses_table")
                self.create_table_widget(rowPosition, 2, str(y.address), "addresses_table")
                self.create_table_widget(rowPosition, 3, str(y.netmask), "addresses_table")
                self.create_table_widget(rowPosition, 4, str(y.broadcast), "addresses_table")
                self.create_table_widget(rowPosition, 5, str(y.ptp), "addresses_table")


    def update_net_connections(self):
        for x in psutil.net_connections():
            rowPosition = self.ui.connections_table.rowCount()
            self.ui.connections_table.insertRow(rowPosition)
            self.create_table_widget(rowPosition, 0, str(x.fd), "connections_table")
            self.create_table_widget(rowPosition, 1, str(x.family), "connections_table")
            self.create_table_widget(rowPosition, 2, str(x.type), "connections_table")
            self.create_table_widget(rowPosition, 3, str(x.laddr), "connections_table")
            self.create_table_widget(rowPosition, 4, str(x.raddr), "connections_table")
            self.create_table_widget(rowPosition, 5, str(x.status), "connections_table")
            self.create_table_widget(rowPosition, 6, str(x.pid), "connections_table")

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
