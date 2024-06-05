########################################################################
## QT GUI BY SPINN TV(YOUTUBE)
########################################################################
import datetime
import json
########################################################################
## IMPORTS
########################################################################
import os
import platform
import shutil
import sys
import time
import traceback
from json import JSONDecodeError

from server import Server
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
platforms = {
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
        self.server = Server("localhost", 8080)
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
        self.psutil_thread()

        ########################################################################
        # UPDATE APP SETTINGS LOADED FROM JSON STYLESHEET
        # ITS IMPORTANT TO RUN THIS AFTER SHOWING THE WINDOW
        # THIS PROCESS WILL RUN ON A SEPARATE THREAD WHEN GENERATING NEW ICONS
        # TO PREVENT THE WINDOW FROM BEING UNRESPONSIVE
        ########################################################################
        QAppSettings.updateAppSettings(self)



    def psutil_thread(self):

        serv = Worker(self.server.start(), args=(), kwargs={})
        serv.signals.result.connect(self.print_output)
        serv.signals.finished.connect(self.thread_complete)

        self.threadpool.start(serv)

        worker = Worker(self.response, args=(), kwargs={})
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)

        self.threadpool.start(worker)
        '''
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

    def response(self,progress_callback):
        self.system_info()
        #self.storage()
        while True:
            self.cpu_ram()
            time.sleep(0.5)
            self.power()
            time.sleep(0.5)
            self.battery()
            time.sleep(0.5)
            self.update_net_if_stats()
            time.sleep(0.5)
            self.update_net_io_counters()
            time.sleep(0.5)
            self.update_net_if_addrs()
            time.sleep(0.5)
            self.update_net_connections()
            time.sleep(0.5)
            self.sensor()
            # time.sleep(0.5)
            # self.processes()
    def cpu_ram(self):
            self.server.options("1")
            responsee = self.server.receive_chunks(self.server.return_client_socket())
            responses = responsee.decode('utf-8')  # Decode the byte string
            try:
                response = json.loads(responses)  # Parse JSON data
                if 'total_ram' in response:
                    # Extract the data from the response
                    core_count = response['core_count']
                    cpu_percentage = response['cpu_percentage']
                    main_core_count = response['main_core_count']
                    total_ram = response['total_ram']
                    available_ram = response['available_ram']
                    ram_usage = response['ram_usage']
                    used_ram = response['used_ram']
                    ram_free = response['ram_free']


                    # Update the UI elements
                    self.ui.total_ram.setText(str("{:.2f}".format(total_ram) + ' GB'))
                    self.ui.available_ram.setText(f"{available_ram:.2f} GB")
                    self.ui.ram_usage.setText(f"{ram_usage:.2f}%")
                    self.ui.used_ram.setText(f"{used_ram:.2f} GB")
                    self.ui.free_ram.setText(f"{ram_free:.2f} GB")
                    self.ui.cpu_cont.setText(str(core_count))
                    self.ui.cpu_per.setText(f"{cpu_percentage}%")
                    self.ui.cpu_main_core.setText(str(main_core_count))

                    # Update CPU progress bar
                    self.ui.CPU_PROGRESS.rpb_setMaximum(100)
                    self.ui.CPU_PROGRESS.rpb_setValue(cpu_percentage)
                    self.ui.CPU_PROGRESS.rpb_setBarStyle('Hybrid2')
                    self.ui.CPU_PROGRESS.rpb_setLineColor((255, 30, 99))
                    self.ui.CPU_PROGRESS.rpb_setPieColor((45, 74, 83))
                    self.ui.CPU_PROGRESS.rpb_setInitialPos('West')
                    self.ui.CPU_PROGRESS.rpb_setTextFormat('Percentage')
                    self.ui.CPU_PROGRESS.rpb_setTextFont('Asus Font')
                    self.ui.CPU_PROGRESS.rpb_setLineWidth(15)
                    self.ui.CPU_PROGRESS.rpb_setPathWidth(15)
                    self.ui.CPU_PROGRESS.rpb_setLineCap('RoundCap')

                    # Update RAM progress bar
                    self.ui.RAM_PROGRESS.spb_setMinimum((0, 0, 0))
                    self.ui.RAM_PROGRESS.spb_setMaximum((total_ram, total_ram, total_ram))
                    self.ui.RAM_PROGRESS.spb_setValue((available_ram, used_ram, ram_free))
                    self.ui.RAM_PROGRESS.spb_lineColor(((6, 233, 38), (6, 201, 233), (233, 6, 201)))
                    self.ui.RAM_PROGRESS.spb_setInitialPos(('West', 'West', 'West'))
                    self.ui.RAM_PROGRESS.spb_lineWidth(15)
                    self.ui.RAM_PROGRESS.spb_lineStyle(('SolidLine', 'SolidLine', 'SolidLine'))
                    self.ui.RAM_PROGRESS.spb_lineCap(('RoundCap', 'RoundCap', 'RoundCap'))
                    self.ui.RAM_PROGRESS.spb_setPathHidden(True)
            except JSONDecodeError:
                print(JSONDecodeError)
                pass
    def power(self):
            self.server.options("2")
            response = self.server.receive_chunks(self.server.return_client_socket())
            response = response.decode('utf-8')
            try:
                response = json.loads(response)
                if "cpu_power" in response:
                    cpu_power = response["cpu_power"]
                    igpu_power = response["igpu_power"]
                    dgpu_power = response["dgpu_power"]
                    self.ui.cpu_consume.setText(f"{cpu_power:.2f}")
                    if igpu_power > 0:
                         self.ui.igpu_consume.setText(f"{igpu_power:.2f}")
                    self.ui.gpu_consume.setText(f"{dgpu_power:.2f}")
                    avg = (dgpu_power + cpu_power) / 2
                    self.ui.avg_consumed.setText("{:.2f}".format(avg))
                    self.ui.power_progress.spb_setMinimum((0, 0, 0))
                    self.ui.power_progress.spb_setMaximum((100, 100, 300))
                    self.ui.power_progress.spb_setValue((cpu_power, dgpu_power, avg))
                    self.ui.power_progress.spb_lineColor(((6, 233, 38), (6, 201, 233), (233, 6, 201)))
                    self.ui.power_progress.spb_setInitialPos(('West', 'West', 'West'))
                    self.ui.power_progress.spb_lineWidth(15)
                    self.ui.power_progress.spb_lineStyle(('SolidLine', 'SolidLine', 'SolidLine'))
                    self.ui.power_progress.spb_lineCap(('RoundCap', 'RoundCap', 'RoundCap'))
                    self.ui.power_progress.spb_setPathHidden(True)
            except JSONDecodeError:
                print(JSONDecodeError)
                pass
    def battery(self):
        self.server.options("3")
        responsee = self.server.receive_chunks(self.server.return_client_socket())
        responses = responsee.decode('utf-8')  # Decode the byte string
        try:
            battery_info = json.loads(responses)  # Parse JSON data
            if 'charge' in battery_info:
                if battery_info["status"] == "Platform not supported":
                    self.ui.battery_status.setText("Platform not supported")
                    self.ui.battery_usage.rpb_setValue(100)
                else:
                    self.ui.battery_charge.setText(str(battery_info["charge"]) + "%")
                    self.ui.battery_time_left.setText(battery_info["time_left"])
                    self.ui.battery_plugged.setText(battery_info["plugged"])

                    if battery_info["status"] == "Charging" or battery_info["status"] == "Fully Charged":
                        self.ui.battery_status.setText(battery_info["status"])
                    else:
                        self.ui.battery_status.setText("Discharging")

                    self.ui.battery_usage.rpb_setValue(battery_info["charge"])
        except JSONDecodeError:
            print(JSONDecodeError)
            pass

    def system_info(self):
        self.server.options("4")
        responsee = self.server.receive_chunks(self.server.return_client_socket())
        responses = responsee.decode('utf-8')  # Decode the byte string
        try:
                system_info = json.loads(responses)  # Parse JSON data
                self.ui.system_time.setText(system_info["time"])
                self.ui.system_date.setText(system_info["date"])
                self.ui.system_machine.setText(system_info["machine"])
                self.ui.system_version.setText(system_info["version"])
                self.ui.system_platform.setText(system_info["platform"])
                self.ui.system_system.setText(system_info["system"])
                self.ui.system_processor.setText(system_info["processor"])
        except JSONDecodeError:
            print(JSONDecodeError)
            pass
    #####################################################
    #               NU FUNCTIONEAZA                     #
    #####################################################
    def processes(self):
        self.server.options("5")
        responsee = self.server.receive_chunks(self.server.return_client_socket())
        responses = responsee.decode('utf-8')  # Decode the byte string

        try:
            process_data = json.loads(responses)  # Parse JSON data
            existing_pids = set()

            # Update existing processes
            for row in range(self.ui.tableWidget.rowCount()):
                pid_item = self.ui.tableWidget.item(row, 0)
                if pid_item is None:
                    continue
                pid = int(pid_item.text())
                existing_pids.add(pid)
                for process_info in process_data:
                    if 'status' in process_info:
                        if process_info["pid"] == str(pid):
                            self.ui.tableWidget.item(row, 1).setText(process_info["name"])
                            self.ui.tableWidget.item(row, 2).setText(process_info["status"])
                            self.ui.tableWidget.item(row, 3).setText(process_info["create_time"])
                            break

            # Add new processes
            for process_info in process_data:
                if 'status' in process_info:
                    pid = int(process_info["pid"])
                    if pid not in existing_pids:
                        rowPosition = self.ui.tableWidget.rowCount()
                        self.ui.tableWidget.insertRow(rowPosition)
                        self.create_table_widget(rowPosition, 0, str(pid), "tableWidget")
                        self.create_table_widget(rowPosition, 1, process_info["name"], "tableWidget")
                        self.create_table_widget(rowPosition, 2, process_info["status"], "tableWidget")
                        self.create_table_widget(rowPosition, 3, process_info["create_time"], "tableWidget")
                        self.add_buttons(rowPosition)
        except JSONDecodeError:
            print(JSONDecodeError)
            pass
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

    def storage(self):
        self.server.options("7")
        responsee = self.server.receive_chunks(self.server.return_client_socket())
        responses = responsee.decode('utf-8')  # Decode the byte string
        try:
            storage_infos = json.loads(responses)  # Parse JSON data
            self.ui.storageTable.setRowCount(0)  # Clear the table
            for row, storage_info in enumerate(storage_infos):
                if 'mountpoint' in storage_info:
                    self.ui.storageTable.insertRow(row)
                    self.create_table_widget(row, 0, storage_info['device'], "storageTable")
                    self.create_table_widget(row, 1, storage_info["mountpoint"], "storageTable")
                    self.create_table_widget(row, 2, storage_info["fstype"], "storageTable")
                    self.create_table_widget(row, 3, storage_info["opts"], "storageTable")
                    self.create_table_widget(row, 4, storage_info["maxfile"], "storageTable")
                    self.create_table_widget(row, 5, storage_info["maxpath"], "storageTable")
                    self.create_table_widget(row, 6, storage_info["total_space"], "storageTable")
                    self.create_table_widget(row, 7, storage_info["free_space"], "storageTable")
                    self.create_table_widget(row, 8, storage_info["used_space"], "storageTable")

                    total_space = float(storage_info["total_space"].split()[0])
                    used_space = float(storage_info["used_space"].split()[0])
                    full_disk = (used_space / total_space) * 100
                    progressBar = QProgressBar(self.ui.storageTable)
                    progressBar.setObjectName(u"progressBar")
                    progressBar.setValue(full_disk)
                    self.ui.storageTable.setCellWidget(row, 9, progressBar)
        except JSONDecodeError:
            print(JSONDecodeError)
            pass
    #####################################################
    #               NU FUNCTIONEAZA                     #
    #####################################################


    def create_table_widget(self, rowPosition, columnPosition, text, tablename):
        qtablewidgetitem = QTableWidgetItem()
        getattr(self.ui, tablename).setItem(rowPosition, columnPosition, qtablewidgetitem)
        qtablewidgetitem = getattr(self.ui, tablename).item(rowPosition, columnPosition)
        qtablewidgetitem.setText(text)

    def sensor(self):
            self.server.options("6")
            responsee = self.server.receive_chunks(self.server.return_client_socket())
            responses = responsee.decode('utf-8')  # Decode the byte string
            try:
                sensor_data = json.loads(responses)  # Parse JSON data
                self.ui.sensors_table.setRowCount(0)
                cpu_temps = {}
                gpu_temps = {}
                row=0
                # Extract sensor data from the provided sensor_data
                for sensor_entry in sensor_data:
                    if sensor_entry["sensor_type"] == "CPU":
                        temps = sensor_entry["value"]
                        current_temp = temps[-1]
                        avg_temp = sum(temps) / len(temps)
                        min_temp = min(temps)
                        max_temp = max(temps)
                        self.ui.sensors_table.insertRow(row)
                        self.create_table_widget(row, 0, sensor_entry["sensor_name"], 'sensors_table')
                        self.create_table_widget(row, 1, f"{current_temp:.2f}", 'sensors_table')
                        self.create_table_widget(row, 2, f"{min_temp:.2f}", 'sensors_table')
                        self.create_table_widget(row, 3, f"{max_temp:.2f}", 'sensors_table')
                        self.create_table_widget(row, 4, f"{avg_temp:.2f}", 'sensors_table')
                        row+=1
                    elif sensor_entry["sensor_type"] == "GPU":
                        temps = sensor_entry["value"]
                        current_temp = temps[-1]
                        avg_temp = sum(temps) / len(temps)
                        min_temp = min(temps)
                        max_temp = max(temps)
                        self.ui.sensors_table.insertRow(row)
                        self.create_table_widget(row, 0, sensor_entry["sensor_name"],
                                                 'sensors_table')
                        self.create_table_widget(row, 1, f"{current_temp:.2f}",
                                                 'sensors_table')
                        self.create_table_widget(row, 2, f"{min_temp:.2f}", 'sensors_table')
                        self.create_table_widget(row, 3, f"{max_temp:.2f}", 'sensors_table')
                        self.create_table_widget(row, 4, f"{avg_temp:.2f}", 'sensors_table')
                        row+=1
            except Exception as e:
                print(f"Error in monitoring loop: {e}")
                pass

    #######################################################
    #           NETWORK                                   #
    #######################################################

    def update_net_if_stats(self):
        self.server.options("8")
        responsee = self.server.receive_chunks(self.server.return_client_socket())
        responses = responsee.decode('utf-8')  # Decode the byte string
        try:
            stats_infos = json.loads(responses)  # Parse JSON data
            self.ui.storageTable.setRowCount(0)  # Clear the table
            for row, stats_info in enumerate(stats_infos):
                if "interface" in stats_info:
                    self.ui.stats_table.insertRow(row)
                    self.create_table_widget(row, 0, stats_info["interface"], "stats_table")
                    self.create_table_widget(row, 1, str(stats_info["is_up"]), "stats_table")
                    self.create_table_widget(row, 2, str(stats_info["duplex"]), "stats_table")
                    self.create_table_widget(row, 3, str(stats_info["speed"]), "stats_table")
                    self.create_table_widget(row, 4, str(stats_info["mtu"]), "stats_table")
        except JSONDecodeError:
            print(JSONDecodeError)
            pass
    def update_net_io_counters(self):
        self.server.options("9")
        responsee = self.server.receive_chunks(self.server.return_client_socket())
        responses = responsee.decode('utf-8')  # Decode the byte string
        try:
            io_counters_data = json.loads(responses)  # Parse JSON data
            self.ui.storageTable.setRowCount(0)  # Clear the table
            for row, (interface, counters) in enumerate(io_counters_data.items()):
                if "bytes_sent" in counters:
                    self.ui.IO_counters_table.insertRow(row)
                    self.create_table_widget(row, 0, str(interface), "IO_counters_table")
                    self.create_table_widget(row, 1, str(counters["bytes_sent"]), "IO_counters_table")
                    self.create_table_widget(row, 2, str(counters["bytes_recv"]), "IO_counters_table")
                    self.create_table_widget(row, 3, str(counters["packets_sent"]), "IO_counters_table")
                    self.create_table_widget(row, 4, str(counters["packets_recv"]), "IO_counters_table")
                    self.create_table_widget(row, 5, str(counters["errin"]), "IO_counters_table")
                    self.create_table_widget(row, 6, str(counters["errout"]), "IO_counters_table")
                    self.create_table_widget(row, 7, str(counters["dropin"]), "IO_counters_table")
                    self.create_table_widget(row, 8, str(counters["dropout"]), "IO_counters_table")
        except JSONDecodeError:
            print(JSONDecodeError)
            pass
    def update_net_if_addrs(self):
        self.server.options("10")
        responsee = self.server.receive_chunks(self.server.return_client_socket())
        responses = responsee.decode('utf-8')  # Decode the byte string
        try:
            io_counters_data = json.loads(responses)  # Parse JSON data
            self.ui.addresses_table.setRowCount(0)  # Clear the table before updating
            for interface, addrs in io_counters_data.items():
                for addr in addrs:
                    if "family" in addr:
                        rowPosition = self.ui.addresses_table.rowCount()
                        self.ui.addresses_table.insertRow(rowPosition)
                        self.create_table_widget(rowPosition, 0, str(interface), "addresses_table")
                        self.create_table_widget(rowPosition, 1, str(addr["family"]), "addresses_table")
                        self.create_table_widget(rowPosition, 2, str(addr["address"]), "addresses_table")
                        self.create_table_widget(rowPosition, 3, str(addr["netmask"]), "addresses_table")
                        self.create_table_widget(rowPosition, 4, str(addr["broadcast"]), "addresses_table")
                        self.create_table_widget(rowPosition, 5, str(addr["ptp"]), "addresses_table")
        except JSONDecodeError:
            print(JSONDecodeError)
            pass
    def update_net_connections(self):
        self.server.options("11")
        responsee = self.server.receive_chunks(self.server.return_client_socket())
        responses = responsee.decode('utf-8')  # Decode the byte string
        try:
            connections_data = json.loads(responses)  # Parse JSON data
            self.ui.connections_table.setRowCount(0)  # Clear the table
            for row, connection_info in enumerate(connections_data):
                if "laddr" in connection_info:
                    self.ui.connections_table.insertRow(row)
                    self.create_table_widget(row, 0, str(connection_info["fd"]), "connections_table")
                    self.create_table_widget(row, 1, str(connection_info["family"]), "connections_table")
                    self.create_table_widget(row, 2, str(connection_info["type"]), "connections_table")
                    self.create_table_widget(row, 3, str(connection_info["laddr"]), "connections_table")
                    self.create_table_widget(row, 4, str(connection_info["raddr"]), "connections_table")
                    self.create_table_widget(row, 5, str(connection_info["status"]), "connections_table")
                    self.create_table_widget(row, 6, str(connection_info["pid"]), "connections_table")
        except JSONDecodeError:
            print(JSONDecodeError)
            pass

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
    def print_output(self, s):
        print(s)

    def thread_complete(self):
        print("Thread Completed")

    def progress_fn(self, i):
        print("%d%% done" % i)

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
