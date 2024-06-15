import sys
import time
import traceback
from functools import partial

from server import Server
########################################################################
# IMPORT GUI FILE
from src.ui_interface import *
########################################################################
from src.fnct import *
from PySide2.QtCore import QRunnable, Slot, QThreadPool
import clr  # the pythonnet module
import faulthandler
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
    status_proc= Signal(dict)

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
        client_name = command[0]
        if client_name not in self.main.data['cpu_ram_com']:
            for key in self.main.data:
                self.main.data[key][client_name] = []
        if command:
            print(f"Commands: {command}")
            command_map = {
                "cpu_ram": self.main.data['cpu_ram_com'],
                "power": self.main.data['power_com'],
                "battery": self.main.data['battery_com'],
                "processes": self.main.data['processes_com'],
                "sensor_data": self.main.data['sensor_com'],
                "storage_info": self.main.data['storage_com'],
                "network_data": self.main.data['update_net_if_stats_com'],
                "io": self.main.data['update_net_io_counters_com'],
                "if_addr": self.main.data['update_net_if_addrs_com'],
                "system_info": self.main.data['system_info_com'],
                "connects": self.main.data['update_net_connections_com'],
                "is_in_domain": self.main.data['statusD'],
                "fetch_all_user_info": self.main.data['users'],
                "get_group": self.main.data['grp'],
                "set_hwid": self.main.data['set_hwid']
            }
            if command[1] in command_map:
                command_map[command[1]][client_name].append(command[2])
                self.signals.update_data.emit(command[1], command[2])
            elif command[1] in ["suspend", "resume", "terminate", "kill"]:
                self.signals.status_proc.emit(command[2])



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
        self.is_loading_data = False
        self.server = Server("192.168.0.227", 9000)  # Initialize server before setup_ui_elements
        self.server.new_client_connected.connect(self.populate_clients_list)  # Connect signal to slot

        self.setup_ui_elements()  # Setup UI elements
        self.threadpool = QThreadPool()
        self.network_worker = NetworkWorker(self.server)
        self.sorter = CommandWorker(self, self.server)
        self.sorter.signals.update_data.connect(self.handle_update_data)
        self.sorter.signals.status_proc.connect(self.handle_client_response)
        self.start_threads()

        loadJsonStyle(self, self.ui, jsonFiles={
            "json-styles/style.json"
        })
        QAppSettings.updateAppSettings(self)

    def initialize_variables(self):
        self.data = {
            'cpu_ram_com': {},
            'power_com': {},
            'system_info_com': {},
            'battery_com': {},
            'processes_com': {},
            'sensor_com': {},
            'storage_com': {},
            'users': {},
            'update_net_if_stats_com': {},
            'update_net_io_counters_com': {},
            'update_net_if_addrs_com': {},
            'update_net_connections_com': {},
            'statusD': {},
            'grp': {},
            'set_hwid': {}
        }

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

        # Initialize clients_list QTreeWidget
        self.populate_clients_list()
        self.ui.clients_list.itemSelectionChanged.connect(self.client_selection_changed)

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
        #for worker in workers:
       #     self.threadpool.start(worker)
        self.threadpool.start(self.network_worker)
        self.threadpool.start(self.sorter)

    @Slot()
    def populate_clients_list(self):
        self.ui.clients_list.clear()  # Clear the existing items
        for client_name in self.server.clients.keys():
            item = QTreeWidgetItem([client_name])
            self.ui.clients_list.addTopLevelItem(item)

    def client_selection_changed(self):
        selected_items = self.ui.clients_list.selectedItems()
        if selected_items:
            client_name = selected_items[0].text(0)
            self.refresh_ui_data(client_name)

    def refresh_ui_data(self, client_name):
        if self.is_loading_data:
            print("Data loading is already in progress. Queuing the update.")
            QTimer.singleShot(500, lambda: self.refresh_ui_data(client_name))
            return

        self.is_loading_data = True
        self.system_info(client_name)
        self.cpu_ram(client_name)
        self.power(client_name)
        self.battery(client_name)
        self.processes(client_name)
        self.sensor(client_name)
        self.storage(client_name)
        self.update_net_if_stats(client_name)
        self.update_net_io_counters(client_name)
        self.update_net_if_addrs(client_name)
        self.update_net_connections(client_name)
        self.set_users(client_name)
        self.is_loading_data = False

    def hardware(self, progress_callback):
        while True:
            for client_name in self.server.clients.keys():
                self.system_info(client_name)
                self.update_hardware_status(client_name)
                time.sleep(1)

    def update_hardware_status(self, client_name):
        self.cpu_ram(client_name)
        self.battery(client_name)
        self.power(client_name)
        self.sensor(client_name)
        self.update_net_if_stats(client_name)
        self.update_net_io_counters(client_name)
        self.update_net_if_addrs(client_name)
        self.update_net_connections(client_name)

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
        self.server.stop()
       # self.threadpool.waitForDone()  # Wait for all threads to finish
        self.close()

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

    def get_selected_client_name(self):
        selected_items = self.ui.clients_list.selectedItems()
        if selected_items:
            return selected_items[0].text(0)
        return None

    def system_info(self, client_name):
        if client_name in self.data['system_info_com']:
            self.pop_and_handle(self.data['system_info_com'][client_name], self.handle_system_info)

    def cpu_ram(self, client_name):
        if client_name in self.data['cpu_ram_com']:
            self.pop_and_handle(self.data['cpu_ram_com'][client_name], self.handle_cpu_ram)

    def power(self, client_name):
        if client_name in self.data['power_com']:
            self.pop_and_handle(self.data['power_com'][client_name], self.handle_power)

    def battery(self, client_name):
        if client_name in self.data['battery_com']:
            self.pop_and_handle(self.data['battery_com'][client_name], self.handle_battery)

    def processes(self, client_name):
        if client_name in self.data['processes_com']:
            self.pop_and_handle(self.data['processes_com'][client_name], self.handle_processes)

    def sensor(self, client_name):
        if client_name in self.data['sensor_com']:
            self.pop_and_handle(self.data['sensor_com'][client_name], self.handle_sensor)

    def storage(self, client_name):
        if client_name in self.data['storage_com']:
            self.pop_and_handle(self.data['storage_com'][client_name], self.handle_storage)

    def set_users(self, client_name):
        if client_name in self.data['users']:
            self.pop_and_handle(self.data['users'][client_name], self.handle_set_users)

    def update_net_if_stats(self, client_name):
        if client_name in self.data['update_net_if_stats_com']:
            self.pop_and_handle(self.data['update_net_if_stats_com'][client_name], self.handle_update_net_if_stats)

    def update_net_io_counters(self, client_name):
        if client_name in self.data['update_net_io_counters_com']:
            self.pop_and_handle(self.data['update_net_io_counters_com'][client_name],
                                self.handle_update_net_io_counters)

    def update_net_if_addrs(self, client_name):
        if client_name in self.data['update_net_if_addrs_com']:
            self.pop_and_handle(self.data['update_net_if_addrs_com'][client_name], self.handle_update_net_if_addrs)

    def update_net_connections(self, client_name):
        if client_name in self.data['update_net_connections_com']:
            self.pop_and_handle(self.data['update_net_connections_com'][client_name],
                                self.handle_update_net_connections)

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

    def handle_system_info(self, system_info):
        self.update_ui_element(self.ui.system_time, system_info["time"], "{}")
        self.update_ui_element(self.ui.system_date, system_info["date"], "{}")
        self.update_ui_element(self.ui.system_machine, system_info["machine"], "{}")
        self.update_ui_element(self.ui.system_version, system_info["version"], "{}")
        self.update_ui_element(self.ui.system_platform, system_info["platform"], "{}")
        self.update_ui_element(self.ui.system_system, system_info["system"], "{}")
        self.update_ui_element(self.ui.system_processor, system_info["processor"], "{}")

    def handle_client_response(self, response):
        print(f"Client response: {response}")
        if isinstance(response, dict) and "pid" in response and "status" in response:
            self.update_process_table(response["pid"], response["status"])

    def update_process_table(self, pid, status):
        for row in range(self.ui.tableWidget.rowCount()):
            pid_item = self.ui.tableWidget.item(row, 0)
            if pid_item and int(pid_item.text()) == pid:
                if status in ["terminated", "killed"]:
                    self.ui.tableWidget.removeRow(row)
                elif status == "suspended":
                    self.ui.tableWidget.item(row, 2).setText("suspended")
                elif status == "resumed":
                    self.ui.tableWidget.item(row, 2).setText("running")
                break
        self.filter_processes()  # Reapply filtering after updating the table


    def handle_processes(self, process_data):
        if not process_data:
            print("No process data received.")
            return
        print(f"Received process data: {process_data}")
        scroll_bar_value = self.ui.tableWidget.verticalScrollBar().value()

        # Clear the existing table content
        self.ui.tableWidget.setRowCount(0)

        for process_info in process_data:
            self.update_table_widget(process_info)

        self.ui.tableWidget.verticalScrollBar().setValue(scroll_bar_value)

    def update_table_widget(self, process_info):
        pid = int(process_info["pid"])
        name = process_info["name"]
        status = process_info["status"]
        create_time = process_info["create_time"]

        print(f"Updating table with PID: {pid}, Name: {name}, Status: {status}, Create Time: {create_time}")

        rowPosition = self.ui.tableWidget.rowCount()
        self.ui.tableWidget.insertRow(rowPosition)
        self.create_table_widget(rowPosition, 0, str(pid), "tableWidget")
        self.create_table_widget(rowPosition, 1, name, "tableWidget")
        self.create_table_widget(rowPosition, 2, status, "tableWidget")
        self.create_table_widget(rowPosition, 3, create_time, "tableWidget")
        self.add_buttons(rowPosition)
        print(f"Added new process row: PID={pid}, Name={name}")

    def add_buttons(self, rowPosition):
        actions = [("Suspend", "brown"), ("Resume", "green"), ("Terminate", "orange"), ("Kill", "red")]
        for i, (label, color) in enumerate(actions, start=4):
            btn = QPushButton(label)
            btn.setStyleSheet(f"color: {color}")
            btn.clicked.connect(lambda pid=rowPosition, action=label.lower(): self.handle_process_action(pid, action))
            self.ui.tableWidget.setCellWidget(rowPosition, i, btn)

    def handle_process_action(self, row, action):
        pid_item = self.ui.tableWidget.item(row, 0)
        if not pid_item:
            return

        pid = int(pid_item.text())
        self.send_process_action_to_client(pid, action)

    def send_process_action_to_client(self, pid, action):
        client_name = self.get_selected_client_name()
        if not client_name:
            print("No client selected.")
            return

        message = {
            "action": action,
            "pid": pid
        }
        self.server.data_send(message, client_name, action)

    def suspend_process(self, process):
        self.process_action(process, "suspend", "suspended")

    def resume_process(self, process):
        self.process_action(process, "resume", "resumed")

    def terminate_process(self, process, row):
        self.process_action(process, "terminate", "terminated")
        self.remove_process_row(row)
        self.filter_processes()  # Reapply filtering

    def kill_process(self, process, row):
        self.process_action(process, "kill", "killed")
        self.remove_process_row(row)
        self.filter_processes()  # Reapply filtering

    def process_action(self, process, action, past_tense_action):
        try:
            getattr(process, action)()
            print(f"Process {process.pid} {past_tense_action}")
        except Exception as e:
            print(f"Error {action} process {process.pid}: {e}")

    def remove_process_row(self, row):
        self.ui.tableWidget.removeRow(row)
        print(f"Removed row {row} from the table")

    def filter_processes(self):
        filter_text = self.ui.activity_search.text().lower()
        for row in range(self.ui.tableWidget.rowCount()):
            process_name_item = self.ui.tableWidget.item(row, 1)  # Assuming the process name is in the second column
            process_status_item = self.ui.tableWidget.item(row, 2)  # Assuming the process status is in the third column
            if process_name_item and process_status_item:
                process_name = process_name_item.text().lower()
                process_status = process_status_item.text().lower()
                if filter_text in process_name or filter_text in process_status:
                    self.ui.tableWidget.setRowHidden(row, False)
                else:
                    self.ui.tableWidget.setRowHidden(row, True)

    def handle_update_net_if_stats(self, stats_infos):
        self.update_table(self.ui.stats_table, stats_infos, ["interface", "is_up", "duplex", "speed", "mtu"])


    def handle_update_net_io_counters(self, io_counters_data):
        self.update_table(self.ui.IO_counters_table, io_counters_data.items(), [
            "interface", "bytes_sent", "bytes_recv", "packets_sent", "packets_recv", "errin", "errout", "dropin",
            "dropout"
        ], key_transform=lambda k, v: {"interface": k, **v})


    def handle_update_net_if_addrs(self, if_addr_data):
        transformed_data = []
        for interface, addrs in if_addr_data.items():
            for addr in addrs:
                entry = {"interface": interface}
                entry.update(addr)
                transformed_data.append(entry)
        self.update_table(self.ui.addresses_table, transformed_data, [
            "interface", "family", "address", "netmask", "broadcast", "ptp"
        ])


    def handle_update_net_connections(self, connections_data):
        self.update_table(self.ui.connections_table, connections_data, [
            "fd", "family", "type", "laddr", "raddr", "status", "pid"
        ])

    def update_table(self, table, data, columns, key_transform=None):
        scroll_bar_value = table.verticalScrollBar().value()
        table.setRowCount(0)  # Clear the table

        if key_transform:
            data_items = [key_transform(key, value) for key, value in data]
        else:
            data_items = data

        for row, item in enumerate(data_items):
            table.insertRow(row)
            for col, column in enumerate(columns):
                value = item.get(column, "") if isinstance(item, dict) else item[col]
                self.create_table_widget(row, col, str(value), table.objectName())

        table.verticalScrollBar().setValue(scroll_bar_value)

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
        stat_activ = self.ui.acc_status.currentText()
        group = self.ui.group_status.currentText()

        if not user_text:
            return []

        if not password_text and not password_confirm_text:
            return [user_text]

        if password_text == password_confirm_text:
            return [user_text, self.ui.fullname_text.text(), self.ui.description_text.text(), password_text, stat_activ,
                    group]
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


    def handle_set_domain(self, dom_data):
        dom = dom_data.get('is_in_domain')
        if dom:
            self.ui.status_domain.setText(
                "Computer is in a domain" if dom.get("PartOfDomain") else "Computer is not in a domain")
            self.ui.name_domain.setText(dom.get("DomainName", ""))

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

    def grupe(self):
        client_name = self.get_selected_client_name()
        if client_name and client_name in self.data['grp']:
            unique_groups = set()
            for item in self.data['grp'][client_name]:
                groups = item.get('Name of the group', [])
                for group in groups:
                    unique_groups.add(group)

            unique_groups_list = sorted(unique_groups)

            self.ui.group_status.clear()
            self.ui.group_status.addItems(unique_groups_list)

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
        client_name = command[0]
        if client_name not in self.data['cpu_ram_com']:
            for key in self.data:
                self.data[key][client_name] = []

        command_map = {
            "cpu_ram": lambda: self.data['cpu_ram_com'][client_name].append(data),
            "power": lambda: self.data['power_com'][client_name].append(data),
            "battery": lambda: self.data['battery_com'][client_name].append(data),
            "processes": lambda: self.data['processes_com'][client_name].append(data),
            "sensor_data": lambda: self.data['sensor_com'][client_name].append(data),
            "storage_info": lambda: self.data['storage_com'][client_name].append(data),
            "network_data": lambda: self.data['update_net_if_stats_com'][client_name].append(data),
            "io": lambda: self.data['update_net_io_counters_com'][client_name].append(data),
            "if_addr": lambda: self.data['update_net_if_addrs_com'][client_name].append(data),
            "system_info": lambda: self.data['system_info_com'][client_name].append(data),
            "connects": lambda: self.data['update_net_connections_com'][client_name].append(data),
            "is_in_domain": lambda: self.data['statusD'][client_name].append(data),
            "fetch_all_user_info": lambda: self.data['users'][client_name].append(data),
            "get_group": lambda: self.data['grp'][client_name].append(data),
            "set_hwid": lambda: self.data['set_hwid'][client_name].append(data)
        }

        if command[1] in command_map:
            command_map[command[1]]()

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
    # TODO:INSTALLER,LISTA PROGRAME
    # WIDGET PT BAZA DE DATE DE ADAUGAT LOCATII
    # BUTON INVENTAR,BUTON RAPORT CURENT
    # FIX TABEL PROCESE
    # MIN AND MAX VALUE SENSORI
    # REFRESH UI ELEMENTS WHEN CLIENTS ARE ALREADY SELECTED

########################################################################
## END===>
########################################################################