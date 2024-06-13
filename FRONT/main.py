########################################################################
## QT GUI BY SPINN TV(YOUTUBE)
########################################################################

########################################################################
## IMPORTS
########################################################################

import sys
import time
import traceback
from server import Server
########################################################################
# IMPORT GUI FILE
from src.ui_interface import *
########################################################################
from src.fnct import *
from PySide2.QtCore import QRunnable, Slot, QThreadPool
import clr  # the pythonnet module
import faulthandler

clr.AddReference("LibreHardwareMonitorLib")
from LibreHardwareMonitor import Hardware
########################################################################
# IMPORT Custom widgets
from Custom_Widgets import *
from Custom_Widgets.QAppSettings import QAppSettings

########################################################################
########################################################################
# Platform Mapping
platforms = {
    'linux': 'Linux',
    'linux1': 'Linux',
    'linux2': 'Linux',
    'darwin': 'Mac x',
    'win32': 'Windows',
}

class CommandWorkerSignals(QObject):
    finished = Signal()
    update_data = Signal(str, dict)

class CommandWorker(QRunnable):
    def __init__(self, main, server):
        super().__init__()
        self.server = server
        self.main = main
        self.signals = CommandWorkerSignals()

    def run(self):
        while True:
            try:
                command = self.server.get_next_command()
                if command:
                    self.process_command(command)
            except Exception as e:
                print(f"Sorter error: {e}")
            finally:
                self.signals.finished.emit()

    def process_command(self, command):
        if not self.main.set_name:
            self.main.set_name = command[0]
        if command:
            print(f"Commands: {command}")
            command_map = {
                "cpu_ram": self.main.cpu_ram_com,
                "power": self.main.power_com,
                "battery": self.main.battery_com,
                "processes": self.main.processes_com,
                "sensor_data": self.main.sensor_com,
                "storage_info": self.main.storage_com,
                "network_data": self.main.update_net_if_stats_com,
                "io": self.main.update_net_io_counters_com,
                "if_addr": self.main.update_net_if_addrs_com,
                "system_info": self.main.system_info_com,
                "connects": self.main.update_net_connections_com,
                "is_in_domain": self.main.statusD,
                "fetch_all_user_info": self.main.users,
            }
            if command[1] in command_map:
                command_map[command[1]].append(command[2])
                self.signals.update_data.emit(command[1], command[2])

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

class NetworkWorkerSignals(QObject):
    started = Signal()
    finished = Signal()

class NetworkWorker(QRunnable):
    def __init__(self, server):
        super().__init__()
        self.server = server
        self.signals = NetworkWorkerSignals()

    def run(self):
        self.server.start()

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.initialize_variables()
        self.setup_ui_elements()
        self.threadpool = QThreadPool()
        self.server = Server("127.0.0.1", 8081)
        self.network_worker = NetworkWorker(self.server)
        self.sorter = CommandWorker(self, self.server)
        self.sorter.signals.update_data.connect(self.handle_update_data)
        self.start_threads()

        loadJsonStyle(self, self.ui, jsonFiles={
            "json-styles/style.json"
        })
        QAppSettings.updateAppSettings(self)

    def initialize_variables(self):
        self.cpu_ram_com = []
        self.power_com = []
        self.system_info_com = []
        self.battery_com = []
        self.processes_com = []
        self.sensor_com = []
        self.storage_com = []
        self.users = []
        self.update_net_if_stats_com = []
        self.update_net_io_counters_com = []
        self.update_net_if_addrs_com = []
        self.update_net_connections_com = []
        self.set_name = ""
        self.statusD = []

    def setup_ui_elements(self):
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
        self.connect_buttons()
        self.clickPosition = QPoint()
        self.ui.header_frame.mousePressEvent = self.mousePressEvent
        self.ui.header_frame.mouseMoveEvent = self.moveWindow

    def connect_buttons(self):
        button_connections = {
            self.ui.Domain: self.ui.Domain_tab,
            self.ui.LocalAcc: self.ui.Local_accounts,
            self.ui.CPU: self.ui.cpu_memory,
            self.ui.power: self.ui.Power,
            self.ui.Sysinfo: self.ui.sysinfo,
            self.ui.Activities: self.ui.activities,
            self.ui.Storage: self.ui.storage,
            self.ui.Sensors: self.ui.sensors,
            self.ui.Network: self.ui.network,
        }
        for button, tab in button_connections.items():
            button.clicked.connect(self.make_tab_switcher(tab))
        self.ui.add_user.clicked.connect(lambda: self.user())
        self.ui.add_domain.clicked.connect(lambda: self.domain())

    def make_tab_switcher(self, tab):
        return lambda: self.ui.stackedWidget.setCurrentWidget(tab)

    def start_threads(self):
        workers = [
            Worker(self.hardware),
            Worker(self.hardware1),
            Worker(self.process),
            Worker(self.network),
            Worker(self.computer_man),
        ]
        for worker in workers:
            self.threadpool.start(worker)
        self.threadpool.start(self.network_worker)
        self.threadpool.start(self.sorter)

    def hardware(self, progress_callback):
        self.system_info()
        while True:
            self.update_hardware_status()
            time.sleep(1)

    def update_hardware_status(self):
        self.cpu_ram()
        self.battery()
        self.power()
        self.sensor()
        self.update_net_if_stats()
        self.update_net_io_counters()
        self.update_net_if_addrs()
        self.update_net_connections()

    def hardware1(self, progress_callback):
        self.storage()
        while True:
            self.set_domain()
            self.set_users()
            time.sleep(20)

    def process(self, progress_callback):
        while True:
            self.processes()
            time.sleep(1)

    def network(self, progress_callback):
        while True:
            self.update_net_if_stats()
            self.update_net_io_counters()
            self.update_net_if_addrs()
            self.update_net_connections()
            time.sleep(1)

    def computer_man(self, progress_callback):
        while True:
            self.set_domain()
            self.set_users()
            time.sleep(1)

    def closer(self):
        self.close()
        self.server.stop()
        self.stop_worker()

    def stop_worker(self):
        if hasattr(self, 'worker'):
            self.worker.stop()

    def print_output(self, s):
        print(s)

    def thread_complete(self):
        print("Thread completed")

    def progress_fn(self, n):
        print(f"Progress: {n}%")

    def create_table_widget(self, rowPosition, columnPosition, text, tablename):
        table_widget = getattr(self.ui, tablename)
        qtablewidgetitem = QTableWidgetItem()
        table_widget.setItem(rowPosition, columnPosition, qtablewidgetitem)
        qtablewidgetitem.setText(text)

    def update_table_widget(self, result_data):
        pid, name, status, create_time = result_data
        for row in range(self.ui.tableWidget.rowCount()):
            pid_item = self.ui.tableWidget.item(row, 0)
            if pid_item and int(pid_item.text()) == pid:
                self.ui.tableWidget.item(row, 1).setText(name)
                self.ui.tableWidget.item(row, 2).setText(status)
                self.ui.tableWidget.item(row, 3).setText(create_time)
                return
        self.add_process_row(pid, name, status, create_time)

    def add_process_row(self, pid, name, status, create_time):
        rowPosition = self.ui.tableWidget.rowCount()
        self.ui.tableWidget.insertRow(rowPosition)
        self.create_table_widget(rowPosition, 0, str(pid), "tableWidget")
        self.create_table_widget(rowPosition, 1, name, "tableWidget")
        self.create_table_widget(rowPosition, 2, status, "tableWidget")
        self.create_table_widget(rowPosition, 3, create_time, "tableWidget")
        self.add_buttons(rowPosition)

    #######################################################
    #                    INFO HARDWARE                    #
    #######################################################

    def cpu_ram(self):
        self.pop_and_handle(self.cpu_ram_com, self.handle_cpu_ram)

    def handle_cpu_ram(self, response):
        self.update_ui_element(self.ui.total_ram, response['total_ram'], suffix=' GB')
        self.update_ui_element(self.ui.available_ram, response['available_ram'], suffix=' GB')
        self.update_ui_element(self.ui.ram_usage, response['ram_usage'], suffix='%')
        self.update_ui_element(self.ui.used_ram, response['used_ram'], suffix=' GB')
        self.update_ui_element(self.ui.free_ram, response['ram_free'], suffix=' GB')
        self.update_ui_element(self.ui.cpu_cont, response['core_count'])
        self.update_ui_element(self.ui.cpu_per, response['cpu_percentage'], suffix='%')
        self.update_ui_element(self.ui.cpu_main_core, response['main_core_count'])
        self.update_progress_bar(self.ui.CPU_PROGRESS, 100, response['cpu_percentage'])
        self.update_split_progress_bar(self.ui.RAM_PROGRESS,
                                       (response['total_ram'], response['total_ram'], response['total_ram']),
                                       (response['available_ram'], response['used_ram'], response['ram_free']),
                                       ((6, 233, 38), (6, 201, 233), (233, 6, 201)), ('West', 'West', 'West'))

    def power(self):
        self.pop_and_handle(self.power_com, self.handle_power)

    def handle_power(self, response):
        self.update_ui_element(self.ui.cpu_consume, response["cpu_power"])
        if response["igpu_power"] > 0:
            self.update_ui_element(self.ui.igpu_consume, response["igpu_power"])
        self.update_ui_element(self.ui.gpu_consume, response["dgpu_power"])
        avg = (response["dgpu_power"] + response["cpu_power"]) / 2
        self.update_ui_element(self.ui.avg_consumed, avg)
        self.update_split_progress_bar(self.ui.power_progress, (100, 100, 300),
                                       (response["cpu_power"], response["dgpu_power"], avg),
                                       ((6, 233, 38), (6, 201, 233), (233, 6, 201)),
                                       ('West', 'West', 'West'))

    def storage(self):
        self.pop_and_handle(self.storage_com, self.handle_storage)

    def handle_storage(self, storage_infos):
        scroll_bar_value = self.ui.storageTable.verticalScrollBar().value()
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
        self.ui.storageTable.verticalScrollBar().setValue(scroll_bar_value)

    def sensor(self):
        self.pop_and_handle(self.sensor_com, self.handle_sensor)

    def handle_sensor(self, sensor_data):
        scroll_bar_value = self.ui.sensors_table.verticalScrollBar().value()
        self.ui.sensors_table.setRowCount(0)
        row = 0
        for sensor_entry in sensor_data:
            if sensor_entry["sensor_type"] in ["CPU", "GPU"]:
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
                row += 1
        self.ui.sensors_table.verticalScrollBar().setValue(scroll_bar_value)

    def battery(self):
        self.pop_and_handle(self.battery_com, self.handle_battery)

    def handle_battery(self, battery_info):
        if battery_info["status"] == "Platform not supported":
            self.ui.battery_status.setText("Platform not supported")
            self.ui.battery_usage.rpb_setValue(100)
        else:
            self.ui.battery_charge.setText(str(battery_info["charge"]) + "%")
            self.ui.battery_time_left.setText(battery_info["time_left"])
            self.ui.battery_plugged.setText(battery_info["plugged"])

            status_text = "Discharging"
            if battery_info["status"] in ["Charging", "Fully Charged"]:
                status_text = battery_info["status"]
            self.ui.battery_status.setText(status_text)

            self.ui.battery_usage.rpb_setValue(battery_info["charge"])

    def system_info(self):
        self.pop_and_handle(self.system_info_com, self.handle_system_info)

    def handle_system_info(self, system_info):
        self.update_ui_element(self.ui.system_time, system_info["time"], "{}")
        self.update_ui_element(self.ui.system_date, system_info["date"], "{}")
        self.update_ui_element(self.ui.system_machine, system_info["machine"], "{}")
        self.update_ui_element(self.ui.system_version, system_info["version"], "{}")
        self.update_ui_element(self.ui.system_platform, system_info["platform"], "{}")
        self.update_ui_element(self.ui.system_system, system_info["system"], "{}")
        self.update_ui_element(self.ui.system_processor, system_info["processor"], "{}")

    #######################################################
    #                    PROCESSES                        #
    #######################################################

    def processes(self):
        self.pop_and_handle(self.processes_com, self.handle_processes)

    def handle_processes(self, process_data):
        scroll_bar_value = self.ui.tableWidget.verticalScrollBar().value()
        existing_pids = self.get_existing_pids()

        for process_info in process_data:
            if "pid" in process_info:
                self.update_table_widget(process_info)

        self.remove_old_processes(existing_pids)
        self.ui.tableWidget.verticalScrollBar().setValue(scroll_bar_value)

    def get_existing_pids(self):
        existing_pids = set()
        for row in range(self.ui.tableWidget.rowCount()):
            pid_item = self.ui.tableWidget.item(row, 0)
            if pid_item:
                existing_pids.add(int(pid_item.text()))
        return existing_pids

    def remove_old_processes(self, existing_pids):
        for row in reversed(range(self.ui.tableWidget.rowCount())):
            pid_item = self.ui.tableWidget.item(row, 0)
            if pid_item and int(pid_item.text()) not in existing_pids:
                self.ui.tableWidget.removeRow(row)

    def handle_error(self, error):
        print("Error:", error)

    def find_name(self):
        name = self.ui.activity_search.text().lower()
        for row in range(self.ui.tableWidget.rowCount()):
            item = self.ui.tableWidget.item(row, 1)
            if item:
                self.ui.tableWidget.setRowHidden(row, name not in item.text().lower())

    def add_buttons(self, rowPosition):
        actions = [("Suspend", "brown"), ("Resume", "green"), ("Terminate", "orange"), ("Kill", "red")]
        for i, (label, color) in enumerate(actions, start=4):
            btn = QPushButton(label)
            btn.setStyleSheet(f"color: {color}")
            self.ui.tableWidget.setCellWidget(rowPosition, i, btn)

    def suspend_process(self, process):
        self.process_action(process, "suspend", "suspended")

    def resume_process(self, process):
        self.process_action(process, "resume", "resumed")

    def terminate_process(self, process):
        self.process_action(process, "terminate", "terminated")

    def kill_process(self, process):
        self.process_action(process, "kill", "killed")

    def process_action(self, process, action, past_tense_action):
        try:
            getattr(process, action)()
            print(f"Process {process.pid} {past_tense_action}")
        except Exception as e:
            print(f"Error {action} process {process.pid}: {e}")

    def update_table_widget(self, process_info):
        pid = process_info["pid"]
        name = process_info["name"]
        status = process_info["status"]
        create_time = process_info["create_time"]

        for row in range(self.ui.tableWidget.rowCount()):
            pid_item = self.ui.tableWidget.item(row, 0)
            if pid_item and int(pid_item.text()) == pid:
                self.ui.tableWidget.item(row, 1).setText(name)
                self.ui.tableWidget.item(row, 2).setText(status)
                self.ui.tableWidget.item(row, 3).setText(create_time)
                return

        self.add_process_row(pid, name, status, create_time)

    def add_process_row(self, pid, name, status, create_time):
        rowPosition = self.ui.tableWidget.rowCount()
        self.ui.tableWidget.insertRow(rowPosition)
        self.create_table_widget(rowPosition, 0, str(pid), "tableWidget")
        self.create_table_widget(rowPosition, 1, name, "tableWidget")
        self.create_table_widget(rowPosition, 2, status, "tableWidget")
        self.create_table_widget(rowPosition, 3, create_time, "tableWidget")
        self.add_buttons(rowPosition)

    #######################################################
    #                    NETWORK                          #
    #######################################################

    def update_net_if_stats(self):
        self.pop_and_handle(self.update_net_if_stats_com, self.handle_update_net_if_stats)

    def handle_update_net_if_stats(self, stats_infos):
        self.update_table(self.ui.stats_table, stats_infos, ["interface", "is_up", "duplex", "speed", "mtu"])

    def update_net_io_counters(self):
        self.pop_and_handle(self.update_net_io_counters_com, self.handle_update_net_io_counters)

    def handle_update_net_io_counters(self, io_counters_data):
        self.update_table(self.ui.IO_counters_table, io_counters_data, [
            "bytes_sent", "bytes_recv", "packets_sent", "packets_recv", "errin", "errout", "dropin", "dropout"
        ])

    def update_net_if_addrs(self):
        self.pop_and_handle(self.update_net_if_addrs_com, self.handle_update_net_if_addrs)

    def handle_update_net_if_addrs(self, if_addr_data):
        self.update_table(self.ui.addresses_table, if_addr_data, [
            "family", "address", "netmask", "broadcast", "ptp"
        ], key_transform=lambda k, v: [(k, a) for a in v])

    def update_net_connections(self):
        self.pop_and_handle(self.update_net_connections_com, self.handle_update_net_connections)

    def handle_update_net_connections(self, connections_data):
        self.update_table(self.ui.connections_table, connections_data, [
            "fd", "family", "type", "laddr", "raddr", "status", "pid"
        ])

    def update_table(self, table, data, columns, key_transform=None):
        scroll_bar_value = table.verticalScrollBar().value()
        table.setRowCount(0)  # Clear the table

        if key_transform:
            data_items = [item for key, value in data.items() for item in key_transform(key, value)]
        else:
            data_items = data

        for row, item in enumerate(data_items):
            table.insertRow(row)
            for col, column in enumerate(columns):
                value = item.get(column, "") if isinstance(item, dict) else item[col]
                self.create_table_widget(row, col, str(value), table.objectName())

        table.verticalScrollBar().setValue(scroll_bar_value)

    #######################################################
    #                    DATA COLLECT                     #
    #######################################################

    def user(self):
        data = self.collect_user_data()
        if not data:
            return

        action = "remove_user" if len(data) == 1 else "add_user"
        self.server.data_send(data, self.set_name, action)

    def collect_user_data(self):
        user_text = self.ui.user_text.text()
        password_text = self.ui.password_text.text()
        password_confirm_text = self.ui.passwordconfirm_text.text()

        if not user_text:
            return []

        if not password_text and not password_confirm_text:
            return [user_text]

        if password_text == password_confirm_text:
            return [user_text, self.ui.fullname_text.text(), self.ui.description_text.text(), password_text]

        print("Passwords do not match.")
        return []

    def domain(self):
        data = self.collect_domain_data()
        if not data:
            return

        action = "remove_from_domain" if len(data) == 2 else "add_to_domain"
        self.server.data_send(data, self.set_name, action)

    def collect_domain_data(self):
        domain_text = self.ui.domain_text.text()
        acc_text = self.ui.acc_text.text()
        pass_text = self.ui.pass_text.text()

        if not domain_text:
            if acc_text and pass_text:
                return [acc_text, pass_text]
            return []

        return [domain_text, acc_text, pass_text]

    def set_domain(self):
        self.pop_and_handle(self.statusD, self.handle_set_domain)

    def handle_set_domain(self, dom_data):
        dom = dom_data.get('is_in_domain')
        if dom:
            self.ui.status_domain.setText("Computer is in a domain" if dom.get("PartOfDomain") else "Computer is not in a domain")
            self.ui.name_domain.setText(dom.get("DomainName", ""))

    def set_users(self):
        self.pop_and_handle(self.users, self.handle_set_users)

    def handle_set_users(self, users_table):
        scroll_bar_value = self.ui.user_table.verticalScrollBar().value()
        self.ui.user_table.setRowCount(0)  # Clear the table
        for row, (username, user_info) in enumerate(users_table.items()):
            self.ui.user_table.insertRow(row)
            self.update_user_table(row, user_info)
        self.ui.user_table.verticalScrollBar().setValue(scroll_bar_value)

    def update_user_table(self, row, user_info):
        columns = [
            'Name', 'Full Name', 'Comment', "User's comment", 'Account active',
            'Account expires', 'Local Group Memberships', 'Password last set',
            'Password expires', 'Password changeable', 'Password required', 'Last logon'
        ]
        for col, field in enumerate(columns):
            self.create_table_widget(row, col, user_info.get(field, ""), "user_table")

    def pop_and_handle(self, data_list, handler):
        try:
            data = data_list.pop(0)
            if data:
                handler(data)
        except IndexError as e:
            if str(e) != "pop from empty list":
                print(f"Error {handler.__name__}: {e}")
        except Exception as e:
            print(f"Error {handler.__name__}: {e}")

    def handle_update_data(self, command, data):
        command_map = {
            "cpu_ram": self.cpu_ram,
            "power": self.power,
            "battery": self.battery,
            "processes": self.processes,
            "sensor_data": self.sensor,
            "storage_info": self.storage,
            "network_data": self.update_net_if_stats,
            "io": self.update_net_io_counters,
            "if_addr": self.update_net_if_addrs,
            "system_info": self.system_info,
            "connects": self.update_net_connections,
            "is_in_domain": self.set_domain,
            "fetch_all_user_info": self.set_users,
        }
        if command in command_map:
            command_map[command]()

    #######################################################
    #                    STYLE                            #
    #######################################################

    def applyButtonStyle(self):
        for w in self.ui.menu.findChildren(QPushButton):
            if w.objectName() != self.sender().objectName():
                w.setStyleSheet("border-bottom: none;")
        self.sender().setStyleSheet("border-bottom: 2px solid;")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clickPosition = event.globalPos()

    def moveWindow(self, event):
        if not self.isMaximized() and event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.clickPosition)
            self.clickPosition = event.globalPos()
            event.accept()

    def update_ui_element(self, ui_element, value, format_str="{:.2f}", suffix=""):
        ui_element.setText(f"{format_str.format(value)}{suffix}")

    def update_progress_bar(self, progress_bar, max_value, value, bar_style='Hybrid2', line_color=(255, 30, 99),
                            pie_color=(45, 74, 83), initial_pos='West', text_format='Percentage', text_font='Asus Font',
                            line_width=15, path_width=15, line_cap='RoundCap'):
        progress_bar.rpb_setMaximum(max_value)
        progress_bar.rpb_setValue(value)
        progress_bar.rpb_setBarStyle(bar_style)
        progress_bar.rpb_setLineColor(line_color)
        progress_bar.rpb_setPieColor(pie_color)
        progress_bar.rpb_setInitialPos(initial_pos)
        progress_bar.rpb_setTextFormat(text_format)
        progress_bar.rpb_setTextFont(text_font)
        progress_bar.rpb_setLineWidth(line_width)
        progress_bar.rpb_setPathWidth(path_width)
        progress_bar.rpb_setLineCap(line_cap)

    def update_split_progress_bar(self, progress_bar, max_values, values, line_colors, initial_positions, line_width=15,
                                  line_styles=('SolidLine', 'SolidLine', 'SolidLine'),
                                  line_caps=('RoundCap', 'RoundCap', 'RoundCap'),
                                  path_hidden=True):
        progress_bar.spb_setMinimum((0, 0, 0))
        progress_bar.spb_setMaximum(max_values)
        progress_bar.spb_setValue(values)
        progress_bar.spb_lineColor(line_colors)
        progress_bar.spb_setInitialPos(initial_positions)
        progress_bar.spb_lineWidth(line_width)
        progress_bar.spb_lineStyle(line_styles)
        progress_bar.spb_lineCap(line_caps)
        progress_bar.spb_setPathHidden(path_hidden)

######################################  ##################################
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