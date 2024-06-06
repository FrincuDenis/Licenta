########################################################################
## QT GUI BY SPINN TV(YOUTUBE)
########################################################################
import datetime
import pdb
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
import debugpy
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
import faulthandler
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

sleep=1.5
########################################################################
## MAIN WINDOW CLASS
########################################################################


class ProcessWorkerSignals(QObject):
    result = Signal(object)

class ProcessWorker(QRunnable):
    def __init__(self, process_info):
        super(ProcessWorker, self).__init__()
        self.process_info = process_info
        self.signals = ProcessWorkerSignals()

    @Slot()
    def run(self):
        try:
            pid = int(self.process_info["pid"])
            name = self.process_info["name"]
            status = self.process_info["status"]
            create_time = self.process_info["create_time"]
            result_data = (pid, name, status, create_time)
            self.signals.result.emit(result_data)
        except Exception as e:
            traceback.print_exc()
            self.signals.error.emit((type(e), e, traceback.format_exc()))

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
        self._stop_requested = False
        self.kwargs['stop_requested'] = lambda: self._stop_requested

    @Slot()
    def run(self):
        try:
            result = self.function(*self.args, **self.kwargs)
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.signals.error.emit((type(e), e, traceback.format_exc()))
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()

    def stop(self):
        self._stop_requested = True

class NetworkWorkerSignals(QObject):
    started = Signal()  # Semnal pentru a indica că lucrătorul a început
    finished = Signal()  # Semnal pentru a indica că lucrătorul a terminat

class NetworkWorker(QRunnable):
    def __init__(self, server):
        super().__init__()
        self.server = server
        self.signals = NetworkWorkerSignals()

    def run(self):
        self.server.start()
        self.signals.started.emit()  # Emiterea semnalului pentru a indica că lucrătorul a început

        while True:
            # Aici poți face operațiuni de rețea periodice
            # Exemplu: self.server.receive_chunks(self.server.return_client_socket())
            time.sleep(1)  # Așteaptă 1 secundă între operații

        self.signals.finished.emit()  # Emiterea semnalului pentru a indica că lucrătorul a terminat

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.server = Server("localhost", 8080)
        self.network_worker = NetworkWorker(self.server)
        self.worker = Worker(self.response, args=(), kwargs={})
        self.worker.signals.result.connect(self.print_output)
        self.worker.signals.finished.connect(self.thread_complete)
        self.worker.signals.progress.connect(self.progress_fn)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(50)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 92, 157, 550))
        self.ui.centralwidget.setGraphicsEffect(self.shadow)
        QSizeGrip(self.ui.size_grip)
        self.ui.minimize_button.clicked.connect(self.showMinimized)
        self.ui.close_button.clicked.connect(self.closer)
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

        self.ui.header_frame.mousePressEvent = self.mousePressEvent
        self.ui.header_frame.mouseMoveEvent = self.moveWindow
        for w in self.ui.menu.findChildren(QPushButton):
            w.clicked.connect(self.applyButtonStyle)

        loadJsonStyle(self, self.ui, jsonFiles={
            "json-styles/style.json"
        })

        self.threadpool = QThreadPool()
        self.network_worker.signals.started.connect(
            self.start_worker)  # Conectează pornirea lucrătorului la semnalul de start al rețelei
        self.threadpool.start(self.network_worker)

        QAppSettings.updateAppSettings(self)
    def start_worker(self):
        self.threadpool.start(self.worker)
    def response_test(self):
            self.ready_semaphore.acquire()
            self.system_info()
            while True:
                self.storage()
                self.processes()
                self.cpu_ram()
                #time.sleep(0.5)
                self.power()
                #time.sleep(0.5)
                self.battery()
                #time.sleep(0.5)
                self.update_net_if_stats()
               # time.sleep(0.5)
                self.update_net_io_counters()
               # time.sleep(0.5)
                self.update_net_if_addrs()
               # time.sleep(0.5)
                self.update_net_connections()
               # time.sleep(0.5)
                self.sensor()

    def response(self, progress_callback, stop_requested):
        self.system_info()
        while not stop_requested():
            self.cpu_ram()
            self.power()
            self.battery()
            self.processes()
            self.sensor()
            self.storage()
            self.update_net_if_stats()
            self.update_net_io_counters()
            self.update_net_if_addrs()
            self.update_net_connections()
            time.sleep(sleep)
            if stop_requested():
                break

    def stop_worker(self):
        if hasattr(self, 'worker'):
            self.worker.stop()

    def print_output(self, s):
        print(s)

    def thread_complete(self):
        print("Thread completed")

    def progress_fn(self, n):
        print(f"Progress: {n}%")

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
    def processes(self):
        scroll_bar_value = self.ui.tableWidget.verticalScrollBar().value()

        self.server.options("5")
        response = self.server.receive_chunks(self.server.return_client_socket())
        responses = response.decode('utf-8')  # Decode the byte string

        try:
            process_data = json.loads(responses)  # Parse JSON data
            existing_pids = set()

            for row in range(self.ui.tableWidget.rowCount()):
                pid_item = self.ui.tableWidget.item(row, 0)
                if pid_item is None:
                    continue
                pid = int(pid_item.text())
                existing_pids.add(pid)

            for process_info in process_data:
                if "pid" in process_info:
                    worker = ProcessWorker(process_info)
                    worker.signals.result.connect(self.update_table_widget)
                    self.threadpool.start(worker)

            # Remove processes that are not in the response
            for row in range(self.ui.tableWidget.rowCount()):
                pid_item = self.ui.tableWidget.item(row, 0)
                if pid_item is None:
                    continue
                pid = int(pid_item.text())
                if pid not in existing_pids:
                    self.ui.tableWidget.removeRow(row)
            self.ui.tableWidget.verticalScrollBar().setValue(scroll_bar_value)
        except json.JSONDecodeError as e:
            print(e)

    def update_table_widget(self, result_data):
        pid, name, status, create_time = result_data
        for row in range(self.ui.tableWidget.rowCount()):
            pid_item = self.ui.tableWidget.item(row, 0)
            if pid_item is None:
                continue
            if int(pid_item.text()) == pid:
                self.ui.tableWidget.item(row, 1).setText(name)
                self.ui.tableWidget.item(row, 2).setText(status)
                self.ui.tableWidget.item(row, 3).setText(create_time)
                return

        rowPosition = self.ui.tableWidget.rowCount()
        self.ui.tableWidget.insertRow(rowPosition)
        self.create_table_widget(rowPosition, 0, str(pid), "tableWidget")
        self.create_table_widget(rowPosition, 1, name, "tableWidget")
        self.create_table_widget(rowPosition, 2, status, "tableWidget")
        self.create_table_widget(rowPosition, 3, create_time, "tableWidget")
        self.add_buttons(rowPosition)

    def handle_error(self, error):
        print("Error:", error)
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
        scroll_bar_value = self.ui.storageTable.verticalScrollBar().value()
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
               #     self.ui.storageTable.setCellWidget(row, 9, progressBar)
            self.ui.storageTable.verticalScrollBar().setValue(scroll_bar_value)
        except JSONDecodeError:
            print(JSONDecodeError)
            pass

    def sensor(self):
            scroll_bar_value = self.ui.sensors_table.verticalScrollBar().value()
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
                self.ui.sensors_table.verticalScrollBar().setValue(scroll_bar_value)
            except Exception as e:
                print(f"Error in monitoring loop: {e}")
                pass

    #######################################################
    #           NETWORK                                   #
    #######################################################

    def update_net_if_stats(self):
        scroll_bar_value = self.ui.stats_table.verticalScrollBar().value()
        self.server.options("8")
        responsee = self.server.receive_chunks(self.server.return_client_socket())
        responses = responsee.decode('utf-8')  # Decode the byte string
        try:
            stats_infos = json.loads(responses)  # Parse JSON data
            self.ui.stats_table.setRowCount(0)  # Clear the table
            for row, stats_info in enumerate(stats_infos):
                if "interface" in stats_info:
                    self.ui.stats_table.insertRow(row)
                    self.create_table_widget(row, 0, stats_info["interface"], "stats_table")
                    self.create_table_widget(row, 1, str(stats_info["is_up"]), "stats_table")
                    self.create_table_widget(row, 2, str(stats_info["duplex"]), "stats_table")
                    self.create_table_widget(row, 3, str(stats_info["speed"]), "stats_table")
                    self.create_table_widget(row, 4, str(stats_info["mtu"]), "stats_table")
            self.ui.stats_table.verticalScrollBar().setValue(scroll_bar_value)
        except JSONDecodeError:
            print(JSONDecodeError)
            pass
    def update_net_io_counters(self):
        scroll_bar_value = self.ui.IO_counters_table.verticalScrollBar().value()
        self.server.options("9")
        responsee = self.server.receive_chunks(self.server.return_client_socket())
        responses = responsee.decode('utf-8')  # Decode the byte string
        try:
            io_counters_data = json.loads(responses)  # Parse JSON data
            self.ui.IO_counters_table.setRowCount(0)  # Clear the table
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
            self.ui.IO_counters_table.verticalScrollBar().setValue(scroll_bar_value)
        except JSONDecodeError:
            print(JSONDecodeError)
            pass
    def update_net_if_addrs(self):
        scroll_bar_value = self.ui.addresses_table.verticalScrollBar().value()
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
            self.ui.addresses_table.verticalScrollBar().setValue(scroll_bar_value)
        except JSONDecodeError:
            print(JSONDecodeError)
            pass
    def update_net_connections(self):
        scroll_bar_value = self.ui.connections_table.verticalScrollBar().value()
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
            self.ui.connections_table.verticalScrollBar().setValue(scroll_bar_value)
        except JSONDecodeError:
            print(JSONDecodeError)
            pass

    #######################################################
    #           NETWORK                                   #
    #######################################################
    def create_table_widget(self, rowPosition, columnPosition, text, tablename):
        qtablewidgetitem = QTableWidgetItem()
        getattr(self.ui, tablename).setItem(rowPosition, columnPosition, qtablewidgetitem)
        qtablewidgetitem = getattr(self.ui, tablename).item(rowPosition, columnPosition)
        qtablewidgetitem.setText(text)

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
    def closer(self):
        self.close()
        self.server.options("12")
        self.stop_worker()
########################################################################
## EXECUTE APP
########################################################################
if __name__ == "__main__":
    faulthandler.enable()
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
