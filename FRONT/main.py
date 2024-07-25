import csv
import datetime
import logging
import os
import sys
import time
import traceback
from functools import partial
from logging_config import setup_logging
from server import Server
import db_connect
########################################################################
# IMPORT GUI FILE
from src.ui_interface import *
########################################################################
from src.fnct import *
from PySide2.QtCore import *
import clr  # the pythonnet module
import faulthandler
from Custom_Widgets import *
from Custom_Widgets.QAppSettings import QAppSettings
sensor_data_history = {}
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
    update_data = Signal(str, dict,str)
    status_proc = Signal(dict)

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
        client_name, cmd, data = command
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
                "set_hwid": self.main.data['set_hwid'],
                "hardware": self.main.data['hardware'],
                "installed_programs": self.main.data['installed_programs'],
                "powershell_result": self.main.data['PSH']
            }
            if cmd in command_map:
                command_map[cmd][client_name].append(data)
                self.signals.update_data.emit(cmd, data,client_name)
            elif cmd in ["suspend", "resume", "terminate", "kill"]:
                self.signals.status_proc.emit(data)

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


class PingWorker(QRunnable):
    def __init__(self, server, client_name):
        super().__init__()
        self.server = server
        self.client_name = client_name

    @Slot()
    def run(self):
        try:
            self.send_ping(self.client_name)
        except Exception as e:
            print(f"Ping error: {e}")

    def send_ping(self, client_name):
        if not client_name:
            print("No client selected.")
            return

        message = {"ping": "ping"}
        time.sleep(20)
        self.server.data_send(message, client_name, "ping")

class StatusUpdateWorker(QRunnable):
    def __init__(self, main_window, db_connection):
        super().__init__()
        self.main_window = main_window
        self.db_connection = db_connection

    @Slot()
    def run(self):
        clients = db_connect.selectare_inregistrari(self.db_connection, 'client')
        for client in clients:
            client_name = client[1]
            client_status = client[2] 


            if client_status == 'Connected':
                self.main_window.send_ping(client_name)  

            self.main_window.set_client_status(client_name, client_status)

        QMetaObject.invokeMethod(self.main_window, "populate_clients_list")


class MainWindow(QMainWindow):
    update_ui_signal = Signal(str, dict, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.initialize_variables()
        self.current_client_name = None
        
        db_host = os.getenv('DB_HOST', '192.168.31.56')
        db_user = os.getenv('DB_USER', 'admin')
        db_password = os.getenv('DB_PASSWORD', 'EmI2@2A')
        db_name = os.getenv('DB_NAME', 'licenta')

        try:
            self.db_connection = db_connect.conectare_bd(
                host=db_host,
                user=db_user,
                password=db_password,
                database=db_name
            )
            setup_logging().info("Database connection successful")

        except Exception as e:
            logging.error(f"Failed to connect to the database: {e}")
            self.db_connection = None
        self.initialize_buttons()
        self.server = Server("192.168.31.162", 9000,self.db_connection)
        self.server.new_client_connected.connect(self.populate_clients_list())
        self.power_data_timer = QTimer(self)
        self.ui.update_int.currentIndexChanged.connect(self.update_timer_interval)
        self.setup_ui_elements()
        self.threadpool = QThreadPool()
        self.network_worker = NetworkWorker(self.server)
        self.worker = StatusUpdateWorker(self, self.db_connection)
        self.sorter = CommandWorker(self, self.server)
        self.sorter.signals.update_data.connect(self.handle_update_data)
        self.sorter.signals.status_proc.connect(self.handle_client_response)
        self.update_ui_signal.connect(self.update_ui_elements)
        self.start_threads()
        self.ui.clients_list.setColumnCount(2)
        self.ui.clients_list.setHeaderLabels(["Clients", "Status"])
        self.ui.load_client.clicked.connect(self.load_clients)
        self.ui.load_locatii.clicked.connect(self.load_locations)
        self.ui.load_incaperi.clicked.connect(self.load_rooms)
        self.ui.add_button.clicked.connect(self.add_to_db)
        self.ui.load_hardware.clicked.connect(self.load_hardware_data)
        self.ui.load_power.clicked.connect(self.load_power_data)

        loadJsonStyle(self, self.ui, jsonFiles={
            "json-styles/style.json"
        })
        QAppSettings.updateAppSettings(self)

    def send_pings(self, client_name):
        worker = PingWorker(self.server, client_name)
     #   self.threadpool.start(worker)
    def send_ping(self, client_name):
        if not client_name:
            print("No client selected.")
            return

        message = {"ping": "ping"}
        self.server.data_send(message, client_name, "ping")
    def update_client(self):
        worker = StatusUpdateWorker(self, self.db_connection)
     #   self.threadpool.start(worker)
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
            'set_hwid': {},
            'hardware':{},
            'installed_programs':{},
            'PSH': {}
        }
    def initialize_buttons(self):
        button_names = [
            "offline_sync",
            "history",
            "settings",
            "uninstall",
            "update_service",
            "set_target",
            "check",
            "schedule",
            "install",
            "history_24h",
            "hide",
        ]

        commands = {
            "offline_sync": "add-offline-sync-service",
            "history": "get-update-history",
            "settings": "get-update-settings",
            "uninstall": "uninstall-update",
            "update_service": "add-microsoft-update-service",
            "set_target": "set-target-version",
            "check": "check-updates",
            "schedule": "schedule-update",
            "install": "install-updates",
            "history_24h": "get-update-history-24h",
            "hide": "hide-update",
        }

        for button_name in button_names:
            button = getattr(self.ui, f"{button_name}")
            button.clicked.connect(partial(self.send_command, commands[button_name]))
        self.ui.help.clicked.connect(self.show_help)

    def send_command(self, command):
        print(f"full_command: {command}")
        args = self.ui.args.text().strip()
        full_command = command
        if args:
            full_command += f" {args}"
        client_name = self.current_client_name

        self.server.data_send(full_command,client_name,"powershell_command" )
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
        self.ui.clients_list.customContextMenuRequested.connect(self.open_menu)
        self.ui.interval_avg.currentIndexChanged.connect(self.update_info_label)
        self.ui.update_int.currentTextChanged.connect(self.update_info_label)
        self.status_update_timer = QTimer(self)
        self.status_update_timer.timeout.connect(self.update_client_status)
        self.status_update_timer.start(5000)
        self.connect_buttons()
        self.clickPosition = QPoint()
        self.ui.header_frame.mousePressEvent = self.mousePressEvent
        self.ui.header_frame.mouseMoveEvent = self.moveWindow

        self.populate_clients_list()
        self.ui.clients_list.itemSelectionChanged.connect(self.client_selection_changed)
        self.ui.clients_list.dropEvent = self.drop_event
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
            self.ui.db_table: self.ui.DB_tab,
            self.ui.DB: self.ui.DB_tab,
            self.ui.program: self.ui.Programs_tab,
            self.ui.updates: self.ui.Updates_tab
        }
        for button, tab in button_connections.items():
            button.clicked.connect(self.make_tab_switcher(tab))
        self.ui.add_user.clicked.connect(lambda: self.user())
        self.ui.add_domain.clicked.connect(lambda: self.domain())
        self.ui.get_hardware_info.clicked.connect(self.get_hardware_info)

    def make_tab_switcher(self, tab):
        return lambda: self.ui.stackedWidget.setCurrentWidget(tab)

    def start_threads(self):
        self.threadpool.start(self.worker)
        self.threadpool.start(self.network_worker)

        self.threadpool.start(self.sorter)

    def open_menu(self, position):
        indexes = self.ui.clients_list.selectedIndexes()
        menu = QMenu()

        if indexes:
            action_edit = QAction("Edit", self)
            action_edit.triggered.connect(lambda: self.edit_client(indexes[0]))
            menu.addAction(action_edit)

            action_remove = QAction("Remove", self)
            action_remove.triggered.connect(lambda: self.delete_client(indexes[0]))
            menu.addAction(action_remove)

            action_refresh = QAction("Refresh", self)
            action_refresh.triggered.connect(lambda: self.populate_clients_list())
            menu.addAction(action_refresh)
        menu.exec_(self.ui.clients_list.viewport().mapToGlobal(position))

    def edit_client(self, index):
        item = self.ui.clients_list.itemFromIndex(index)
        client_name = item.text(0)
        new_client_name, ok = QInputDialog.getText(self, 'Edit Client', 'Enter new client name:', text=client_name)
        if ok and new_client_name:
            db_connect.actualizare_inregistrare(self.db_connection, 'client', {'name': new_client_name},
                                                f"name='{client_name}'")
            self.populate_clients_list()

    def delete_client(self, index):
        item = self.ui.clients_list.itemFromIndex(index)
        client_name = item.text(0)
        db_connect.stergere_inregistrare(self.db_connection, 'client',
                                                f"name='{client_name}'")
        self.populate_clients_list()
    @Slot()
    def populate_clients_list(self):
        
        selected_items = self.get_selected_items()
        expanded_items = self.get_expanded_items()

        self.ui.clients_list.clear()

       
        clients_without_location = db_connect.selectare_inregistrari(self.db_connection, 'client',
                                                                     conditie="location_id IS NULL OR room_id IS NULL")
        for client in clients_without_location:
            client_name = client[1]
            client_status = client[2]
            client_item = QTreeWidgetItem(self.ui.clients_list, [client_name, client_status])
            client_item.setData(0, Qt.UserRole, client_name)  

        
        locations = db_connect.selectare_inregistrari(self.db_connection, 'locatii')

        for location in locations:
            location_id = location[0]
            location_name = location[1]
            location_item = QTreeWidgetItem(self.ui.clients_list, [location_name])
            location_item.setData(0, Qt.UserRole, location_id)  

            classrooms = db_connect.selectare_inregistrari(self.db_connection, 'incaperi',
                                                           conditie=f"location_id={location_id}")

            for classroom in classrooms:
                classroom_id = classroom[0]
                classroom_name = classroom[1]
                classroom_item = QTreeWidgetItem(location_item, [classroom_name])
                classroom_item.setData(0, Qt.UserRole, classroom_id)  

                clients = db_connect.selectare_inregistrari(self.db_connection, 'client',
                                                            conditie=f"room_id={classroom_id} AND location_id={location_id}")

                for client in clients:
                    client_name = client[1]
                    client_status = client[2]
                    client_item = QTreeWidgetItem(classroom_item, [client_name, client_status])
                    client_item.setData(0, Qt.UserRole, client_name)  

        
        self.restore_selected_items(selected_items)
        self.restore_expanded_items(expanded_items)

    '''
    def populate_clients_list(self):
        self.ui.clients_list.clear()
        for client_name in self.server.clients.keys():
            item = QTreeWidgetItem([client_name])
            self.ui.clients_list.addTopLevelItem(item)
    '''
    def restore_selected_items(self, selected_items):
        for i in range(self.ui.clients_list.topLevelItemCount()):
            top_item = self.ui.clients_list.topLevelItem(i)
            self.select_items_recursive(top_item, selected_items)
    def get_selected_items(self):
        selected_items = []
        for item in self.ui.clients_list.selectedItems():
            selected_items.append(item.data(0, Qt.UserRole))
        return selected_items
    def select_items_recursive(self, item, selected_items):
        if item.data(0, Qt.UserRole) in selected_items:
            item.setSelected(True)
        for i in range(item.childCount()):
            self.select_items_recursive(item.child(i), selected_items)

    def get_expanded_items(self):
        expanded_items = []
        for i in range(self.ui.clients_list.topLevelItemCount()):
            top_item = self.ui.clients_list.topLevelItem(i)
            self.collect_expanded_items_recursive(top_item, expanded_items)
        return expanded_items

    def collect_expanded_items_recursive(self, item, expanded_items):
        if item.isExpanded():
            expanded_items.append(item.data(0, Qt.UserRole))
        for i in range(item.childCount()):
            self.collect_expanded_items_recursive(item.child(i), expanded_items)

    def restore_expanded_items(self, expanded_items):
        for i in range(self.ui.clients_list.topLevelItemCount()):
            top_item = self.ui.clients_list.topLevelItem(i)
            self.expand_items_recursive(top_item, expanded_items)

    def expand_items_recursive(self, item, expanded_items):
        if item.data(0, Qt.UserRole) in expanded_items:
            item.setExpanded(True)
        for i in range(item.childCount()):
            self.expand_items_recursive(item.child(i), expanded_items)

    def update_client_status(self):
        clients = self.server.get_all_clients()
        for client in clients:
            client_name = client[1]
            client_status = client[2]  
           # self.send_ping(client_name)  
            self.set_client_status(client_name, client_status)
        self.populate_clients_list()  
    def set_client_status(self, client_name, status):
        for index in range(self.ui.clients_list.topLevelItemCount()):
            item = self.ui.clients_list.topLevelItem(index)
            if item.text(0) == client_name:
                item.setText(1, status)
                break
    def client_selection_changed(self):
        selected_items = self.ui.clients_list.selectedItems()
        if selected_items:
            self.current_client_name = selected_items[0].text(0)

    def handle_update_data(self, command, data,client_name):
        print(f"Name of the client:{client_name}")

        self.update_ui_signal.emit(command, data, client_name)
        if command == "hardware":
            self.handle_hardware_info_response(client_name)
        elif command == "powershell_result":
            print(data)
            self.handle_powershell_result(data)
    def handle_powershell_result(self, response):
        self.ui.updates_table.clear()
        response_text = response.strip()
        lines = response_text.splitlines()

        if not lines or len(lines) < 2:
            return

        headers_line = lines[0].strip()
        headers = headers_line.split()

        header_positions = []
        last_pos = 0
        for header in headers:
            header_start = headers_line.index(header, last_pos)
            header_positions.append(header_start)
            last_pos = header_start + len(header)
        header_positions.append(len(headers_line))

        self.ui.updates_table.setColumnCount(len(headers))
        self.ui.updates_table.setHorizontalHeaderLabels(headers)

        self.ui.updates_table.setRowCount(len(lines) - 2)
        for row_idx, line in enumerate(lines[2:]):
            for col_idx in range(len(headers)):
                col_start = header_positions[col_idx]
                if col_idx == len(headers) - 1:
                    item_text = line[col_start:].strip()
                else:
                    col_end = header_positions[col_idx + 1]
                    item_text = line[col_start:col_end].strip()
                self.ui.updates_table.setItem(row_idx, col_idx, QTableWidgetItem(item_text))

        self.ui.updates_table.resizeColumnsToContents()\

    def show_help(self):
        help_info = {
            "Command": [
                "add-offline-sync-service",
                "get-update-history",
                "get-update-settings",
                "uninstall-update",
                "add-microsoft-update-service",
                "set-target-version",
                "check-updates",
                "schedule-update",
                "install-updates",
                "get-update-history-24h",
                "hide-update"
            ],
            "Description": [
                "Register Offline Sync Service from a file",
                "Get Windows Update history",
                "Get current Windows Update Client configuration",
                "Uninstall a specific update by KBArticleID",
                "Register Microsoft Update service as Service Manager",
                "Set the target version for feature updates",
                "Check for Windows updates",
                "Schedule an update installation",
                "Install available Windows updates",
                "Get Windows Update history for the last 24 hours",
                "Hide a specific update by KBArticleID"
            ],
            "Arguments": [
                "FILE_PATH",
                "None",
                "None",
                "KBID",
                "None",
                "PRODUCT_VERSION TARGET_VERSION",
                "None",
                "UPDATE_ID REVISION HOUR MINUTE",
                "None",
                "None",
                "KBID"
            ],
            "Example": [
                "add-offline-sync-service C:\\path\\to\\syncfile",
                "get-update-history",
                "get-update-settings",
                "uninstall-update KB1234567",
                "add-microsoft-update-service",
                "set-target-version Windows 10",
                "check-updates",
                "schedule-update 1234567 1 12 30",
                "install-updates",
                "get-update-history-24h",
                "hide-update KB1234567"
            ]
        }

        self.display_help_in_table(help_info)

    def display_help_in_table(self, help_info):
        self.ui.updates_table.clear()
        headers = ["Command", "Description", "Arguments", "Example"]
        self.ui.updates_table.setColumnCount(len(headers))
        self.ui.updates_table.setHorizontalHeaderLabels(headers)

        row_count = len(help_info["Command"])
        self.ui.updates_table.setRowCount(row_count)

        for row in range(row_count):
            for col, header in enumerate(headers):
                item_text = help_info[header][row]
                self.ui.updates_table.setItem(row, col, QTableWidgetItem(item_text))

        self.ui.updates_table.resizeColumnsToContents()

    def load_clients(self):
        self.ui.db_table.clear()
        self.ui.db_table.setRowCount(0)
        clients = db_connect.selectare_inregistrari(self.db_connection, 'client')
        self.ui.db_table.setColumnCount(2)
        self.ui.db_table.setHorizontalHeaderLabels(["Client Name", "Status"])

        for client in clients:
            client_name = client[1]
            client_status = client[2]
            row_position = self.ui.db_table.rowCount()
            self.ui.db_table.insertRow(row_position)
            self.ui.db_table.setItem(row_position, 0, QTableWidgetItem(client_name))
            self.ui.db_table.setItem(row_position, 1, QTableWidgetItem(client_status))

    def load_locations(self):
        self.ui.db_table.clear()
        self.ui.db_table.setRowCount(0)
        locations = db_connect.selectare_inregistrari(self.db_connection, 'locatii')
        self.ui.db_table.setColumnCount(1)
        self.ui.db_table.setHorizontalHeaderLabels(["Location"])

        for location in locations:
            location_name = location[1]
            row_position = self.ui.db_table.rowCount()
            self.ui.db_table.insertRow(row_position)
            self.ui.db_table.setItem(row_position, 0, QTableWidgetItem(location_name))

    def load_rooms(self):
        self.ui.db_table.clear()
        self.ui.db_table.setRowCount(0)
        rooms = db_connect.selectare_inregistrari(self.db_connection, 'incaperi')
        self.ui.db_table.setColumnCount(1)
        self.ui.db_table.setHorizontalHeaderLabels(["Room"])

        for room in rooms:
            room_name = room[1]
            row_position = self.ui.db_table.rowCount()
            self.ui.db_table.insertRow(row_position)
            self.ui.db_table.setItem(row_position, 0, QTableWidgetItem(room_name))

    def load_hardware_data(self):
        self.ui.db_table.clear()
        self.ui.db_table.setRowCount(0)
        hardware_data = db_connect.selectare_inregistrari(self.db_connection, 'hardware_data')

        if hardware_data:
            columns = ['pc_name', 'mac_address_ethernet', 'ip_address_ethernet', 'mac_address_wifi',
                       'ip_address_wifi', 'drive', 'drive_size', 'used_drive', 'ram', 'ram_type',
                       'ram_size_gb', 'cpu_model', 'dgpu_names', 'igpu_names', 'os', 'os_version']
            self.ui.db_table.setColumnCount(len(columns))
            self.ui.db_table.setHorizontalHeaderLabels(columns)

            for row_data in hardware_data:
                row_position = self.ui.db_table.rowCount()
                self.ui.db_table.insertRow(row_position)
                for col_index, col_data in enumerate(row_data[1:]): 
                    self.ui.db_table.setItem(row_position, col_index, QTableWidgetItem(str(col_data)))
        else:
            self.ui.db_table.setColumnCount(0)

    def load_power_data(self):
        self.ui.db_table.clear()
        self.ui.db_table.setRowCount(0)
        power_data = db_connect.selectare_inregistrari(self.db_connection, 'power_data')

        if power_data:
            columns = ['timestamp', 'device_id', 'cpu', 'igpu', 'gpu', 'location', 'room']
            self.ui.db_table.setColumnCount(len(columns))
            self.ui.db_table.setHorizontalHeaderLabels(columns)

            for row_data in power_data:
                row_position = self.ui.db_table.rowCount()
                self.ui.db_table.insertRow(row_position)
                for col_index, col_data in enumerate(row_data[1:]):
                    self.ui.db_table.setItem(row_position, col_index, QTableWidgetItem(str(col_data)))
        else:
            self.ui.db_table.setColumnCount(0)

    def add_to_db(self):
        location = self.ui.location_input.text().strip()
        room = self.ui.room_input.text().strip()

        if location and room:
           
            db_connect.adaugare_inregistrare(self.db_connection, 'locatii', {'name': location})
            location_id = db_connect.selectare_inregistrari(self.db_connection, 'locatii',
                                                            conditie=f"name='{location}'")[0][0]
            db_connect.adaugare_inregistrare(self.db_connection, 'incaperi', {'name': room, 'location_id': location_id})
        elif location:
            
            db_connect.adaugare_inregistrare(self.db_connection, 'locatii', {'name': location})
        elif room:
           
            location_id = self.ui.clients_list.currentItem().data(0, Qt.UserRole)
            db_connect.adaugare_inregistrare(self.db_connection, 'incaperi', {'name': room, 'location_id': location_id})

        
        self.ui.location_input.clear()
        self.ui.room_input.clear()

        
        self.populate_clients_list()
    @Slot(str, dict, str)
    def update_ui_elements(self, command, data, client_name):
        if client_name != self.current_client_name:
            print(f"Deny of the client: {client_name} != {self.current_client_name}") 
            return
        command_map = {
            "cpu_ram": self.handle_cpu_ram,
            "power": self.handle_power,
            "battery": self.handle_battery,
            "processes": self.handle_processes,
            "sensor_data": self.handle_sensor,
            "storage_info": self.handle_storage,
            "network_data": self.handle_update_net_if_stats,
            "io": self.handle_update_net_io_counters,
            "if_addr": self.handle_update_net_if_addrs,
            "system_info": self.handle_system_info,
            "connects": self.handle_update_net_connections,
            "is_in_domain": self.handle_set_domain,
            "fetch_all_user_info": self.handle_set_users,
            "get_group": self.grupe,
            "installed_programs":self.installed_programs
        }

        if command in command_map:
            command_map[command](data)



    def handle_system_info(self, system_info):
        self.update_ui_element(self.ui.system_time, system_info["time"], "{}")
        self.update_ui_element(self.ui.system_date, system_info["date"], "{}")
        self.update_ui_element(self.ui.system_machine, system_info["machine"], "{}")
        self.update_ui_element(self.ui.system_version, system_info["version"], "{}")
        self.update_ui_element(self.ui.system_platform, system_info["platform"], "{}")
        self.update_ui_element(self.ui.system_system, system_info["system"], "{}")
        self.update_ui_element(self.ui.system_processor, system_info["processor"], "{}")

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
        self.power_data_timer.timeout.connect(self.store_power_data_timer(response))

    def calculate_avg_power(self, client_name, time_range):
        end_date = datetime.datetime.now()
        if time_range == "24h":
            start_date = end_date - datetime.timedelta(hours=24)
        elif time_range == "1 week":
            start_date = end_date - datetime.timedelta(weeks=1)
        elif time_range == "1 month":
            start_date = end_date - datetime.timedelta(days=30)
        else:
            start_date = end_date - datetime.timedelta(hours=24)

        power_data = db_connect.selectare_inregistrari(
            self.db_connection,
            'power_data',
            conditie=f"device_id='{client_name}' AND timestamp BETWEEN '{start_date}' AND '{end_date}'"
        )

        if power_data:
            cpu_power_avg = sum(float(data[3]) for data in power_data) / len(power_data)
            dgpu_power_avg = sum(float(data[4]) for data in power_data) / len(power_data)
            igpu_power_avg = sum(float(data[5]) for data in power_data) / len(power_data)
            avg = (cpu_power_avg + dgpu_power_avg + igpu_power_avg) / 3
        else:
            avg = 0

        return avg

    def update_info_label(self):
        time_range = self.ui.interval_avg.currentText()
        interval = self.ui.update_int.currentText()
        avg_power = self.calculate_avg_power(self.current_client_name, time_range)
        self.ui.intervals.setText(f"Avg power consumed in the past {time_range} is: {avg_power:.2f} W. "
                                  f"Power Consumption results will be saved in {interval}.")

    def store_power_data_timer(self, response):
        if self.current_client_name:
            if response:
                self.store_power_data(self.current_client_name, response["cpu_power"], response["dgpu_power"],
                                      response["igpu_power"])
            else:
                pass

    def store_hardware_data(self, client_name, hardware_info):
        client_info = db_connect.selectare_inregistrari(
            self.db_connection, 'client', conditie=f"name='{client_name}'"
        )

        if client_info:
            location = client_info[0][3]  
            room = client_info[0][4]  
            setup_logging().info(f"Location: {location}, Room: {room}")

            
            db_connect.adaugare_inregistrare(self.db_connection, 'hardware_data', {
                'pc_name': hardware_info['PCName'],
                'mac_address_ethernet': hardware_info['MAC_AddressEthernet'],
                'ip_address_ethernet': hardware_info['IPAddressEthernet'],
                'mac_address_wifi': hardware_info['MAC_AddressWifi'],
                'ip_address_wifi': hardware_info['IPAddressWifi'],
                'drive': hardware_info['Drive'],
                'drive_size': hardware_info['Drive_Size'],
                'used_drive': hardware_info['Used_Drive'],
                'ram': hardware_info['RAM'],
                'ram_type': hardware_info['RamType'],
                'ram_size_gb': hardware_info['RAMSizeGB'],
                'cpu_model': hardware_info['CPUModel'],
                'dgpu_names': hardware_info['GPU'],  
                'igpu_names': hardware_info['IGPU'],  
                'os': hardware_info['OS'],
                'os_version': hardware_info['OSVersion']
            })
            setup_logging().info(f"Hardware data for {client_name} has been written to the database.")
        else:
            setup_logging().info(f"No location and room information found for client {client_name}.")

    def store_power_data(self, client_name, cpu_power, dgpu_power, igpu_power):
        client_info = db_connect.selectare_inregistrari(
            self.db_connection, 'client', conditie=f"name='{client_name}'"
        )

        if client_info:
            location = client_info[0][3]  
            room = client_info[0][4]  
            setup_logging().info(f"Location: {location}, Room: {room}")
            
            db_connect.adaugare_inregistrare(self.db_connection, 'power_data', {
                'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'device_id': client_name,
                'cpu': cpu_power,
                'igpu': igpu_power,
                'gpu': dgpu_power,
                'location': location,
                'room': room
            })
            setup_logging().info(f"Power data for {client_name} has been written to the database.")
        else:
            setup_logging().info(f"No location and room information found for client {client_name}.")
    def update_timer_interval(self):
        interval_text = self.ui.update_int.currentText()
        if interval_text == "5 seconds":
            interval_ms = 5000
        elif interval_text == "1 minute":
            interval_ms = 60000
        elif interval_text == "5 minutes":
            interval_ms = 300000
        elif interval_text == "10 minutes":
            interval_ms = 600000
        elif interval_text == "30 minutes":
            interval_ms = 1800000
        elif interval_text == "1 hour":
            interval_ms = 3600000
        else:
            interval_ms = 0  

        if interval_ms > 0:
            self.power_data_timer.start(interval_ms)
        else:
            self.power_data_timer.stop()

    def handle_storage(self, storage_infos):
        scroll_bar_value = self.ui.storageTable.verticalScrollBar().value()
        self.ui.storageTable.setRowCount(0)
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
    def installed_programs(self, installed_program):
        self.update_table(self.ui.installed_table, installed_program, ["Name","Version", "Install Date", "Publisher"])


    def handle_sensor(self, sensor_data):
        scroll_bar_value = self.ui.sensors_table.verticalScrollBar().value()
        self.ui.sensors_table.setRowCount(0)
        row = 0
        for sensor_entry in sensor_data:
            sensor_name = sensor_entry["sensor_name"]
            sensor_type = sensor_entry["sensor_type"]
            new_temp = sensor_entry["value"][0]  

            if sensor_type in ["CPU", "GPU"]:
                if sensor_name not in sensor_data_history:
                    sensor_data_history[sensor_name] = {
                        "temps": [],
                        "min_temp": float('inf'),
                        "max_temp": float('-inf')
                    }

               
                sensor_data_history[sensor_name]["temps"].append(new_temp)
                if len(sensor_data_history[sensor_name]["temps"]) > 5:
                    sensor_data_history[sensor_name]["temps"].pop(0)

                
                if new_temp < sensor_data_history[sensor_name]["min_temp"]:
                    sensor_data_history[sensor_name]["min_temp"] = new_temp
                if new_temp > sensor_data_history[sensor_name]["max_temp"]:
                    sensor_data_history[sensor_name]["max_temp"] = new_temp

                temps = sensor_data_history[sensor_name]["temps"]
                if len(temps) > 0:
                    current_temp = temps[-1]
                    avg_temp = sum(temps) / len(temps)
                    min_temp = sensor_data_history[sensor_name]["min_temp"]
                    max_temp = sensor_data_history[sensor_name]["max_temp"]

                    self.ui.sensors_table.insertRow(row)
                    self.create_table_widget(row, 0, sensor_name, 'sensors_table')
                    self.create_table_widget(row, 1, f"{min_temp:.2f}", 'sensors_table')
                    self.create_table_widget(row, 2, f"{current_temp:.2f}" , 'sensors_table')
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
                else:
                    status_item = self.ui.tableWidget.item(row, 2)
                    if status_item:
                        status_item.setText(status)
                break
        self.filter_processes() 

    def handle_processes(self, process_data):
        if not process_data:
            print("No process data received.")
            return
        print(f"Received process data: {process_data}")
        scroll_bar_value = self.ui.tableWidget.verticalScrollBar().value()

       
        self.ui.tableWidget.setRowCount(0)

        for process_info in process_data:
            self.update_table_widget(process_info)

        self.ui.tableWidget.verticalScrollBar().setValue(scroll_bar_value)
        self.filter_processes()  

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
            btn.clicked.connect(lambda action=label.lower(), row=rowPosition: self.handle_process_action(row, action))
            self.ui.tableWidget.setCellWidget(rowPosition, i, btn)

    def handle_process_action(self, row, action):
        pid_item = self.ui.tableWidget.item(row, 0)
        if not pid_item:
            return

        pid = int(pid_item.text())
        self.send_process_action_to_client(pid, action)

        
        if action == "suspend":
            self.update_process_table(pid, "suspended")
        elif action == "resume":
            self.update_process_table(pid, "resumed")
        elif action in ["terminate", "kill"]:
            self.update_process_table(pid, "terminated" if action == "terminate" else "killed")

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
        self.filter_processes()  
    def kill_process(self, process, row):
        self.process_action(process, "kill", "killed")
        self.remove_process_row(row)
        self.filter_processes()  

    def process_action(self, process, action, past_tense_action):
        try:
            getattr(process, action)()
            print(f"Process {process.pid} {past_tense_action}")
            self.update_process_table(process.pid, past_tense_action)
        except Exception as e:
            print(f"Error {action} process {process.pid}: {e}")

    def remove_process_row(self, row):
        self.ui.tableWidget.removeRow(row)
        print(f"Removed row {row} from the table")
        self.filter_processes()  

    def filter_processes(self):
        filter_text = self.ui.activity_search.text().lower()
        for row in range(self.ui.tableWidget.rowCount()):
            process_name_item = self.ui.tableWidget.item(row, 1)  
            process_status_item = self.ui.tableWidget.item(row, 2)  
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
        table.setRowCount(0)

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
        self.server.data_send(data, self.get_selected_client_name(), action)

    def get_hardware_info(self):
         self.server.data_send({"action": "hardware"}, self.get_selected_client_name(), "hardware")

    def handle_hardware_info_response(self, client_name):
        data =self.data['hardware'][client_name]
        print(data)
        self.store_hardware_data(client_name,data[0])

    def write_hardware_info_to_csv(self, data, client_name):
        folder_path = os.path.join(os.getcwd(), "hardware_info")
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        file_path = os.path.join(folder_path, f"{client_name}_hardware_info.csv")
        file_exists = os.path.isfile(file_path)

        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(data.keys())
            writer.writerow(data.values())
            print(f"Hardware info for {client_name} has been written to {file_path}")
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
        self.server.data_send(data, self.get_selected_client_name(), action)

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
        self.ui.user_table.setRowCount(0)
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

    def grupe(self, data=None):
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

    def closer(self, event):
        self.server.stop()
        if self.db_connection:
            self.db_connection.close()  
        self.threadpool.clear()  
        if event:
            event.accept()
        self.close()

    def mouseMoveEvent(self, event):
        if not event.buttons() & Qt.LeftButton:
            return

        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return

        item = self.clients_list.currentItem()
        if item is None:
            return

        mime_data = QMimeData()
        mime_data.setText(item.text(0))

        drag = QDrag(self)
        drag.setMimeData(mime_data)

        action = drag.exec_(Qt.MoveAction)

    def drop_event(self, event):
        source_item = self.ui.clients_list.currentItem()
        target_item = self.ui.clients_list.itemAt(event.pos())

        if source_item and target_item:
            
            client_name = source_item.text(0)
            new_location_id = None
            new_room_id = None

            if target_item.parent() is None:
                
                new_location_id = target_item.data(0, Qt.UserRole)
                new_room_id = None
            elif target_item.parent() is not None:
                
                new_room_id = target_item.data(0, Qt.UserRole)
                new_location_id = target_item.parent().data(0, Qt.UserRole)

            db_connect.actualizare_inregistrare(
                self.db_connection, 'client',
                {'location_id': new_location_id, 'room_id': new_room_id},
                f"name='{client_name}'"
            )

            self.populate_clients_list()  

        super().dropEvent(event)


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
    # INSTALLER
    # WIDGET PT BAZA DE DATE DE ADAUGAT LOCATII
    # BUTON INVENTAR(pe viitor de adaugat locatii),BUTON RAPORT CURENT consumat
    # update-uri
    # sa salvez treewidged-ul
########################################################################
## END===>
########################################################################