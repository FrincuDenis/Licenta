import datetime
import os
import pickle
import sys
import time
from functools import partial
import db_connect
import psutil

from server import Server
########################################################################
# IMPORT GUI FILE
from src.ui_interface import *
########################################################################
from PySide2.QtCore import *
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

sensor_data_history = {}

class ProcessLoaderWorker(QObject):
    finished = Signal()
    process_data_loaded = Signal(list)

    def run(self):
        process_data = self.load_process_data()
        self.process_data_loaded.emit(process_data)
        self.finished.emit()

    def load_process_data(self):
        process_data = []
        for proc in psutil.process_iter(['pid', 'name', 'status', 'create_time']):
            try:
                process_info = proc.info
                process_info['create_time'] = self.format_time(process_info['create_time'])
                process_data.append(process_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return process_data

    def format_time(self, timestamp):
        return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

class CommandWorkerSignals(QObject):
    finished = Signal()
    update_data = Signal(str, dict, str)
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
        client_name, cmd, data, client_hwid = command
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
                "powershell_result":self.main.data['PSH']
            }
            if cmd in command_map:
                command_map[cmd][client_name].append(data)
                self.signals.update_data.emit(cmd, data, client_name)
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
            import traceback
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
    update_ui_signal = Signal(str, dict, str)  # Define the signal here

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.initialize_variables()
        self.is_loading_data = False
        self.current_client_name = None
        self.server = Server("localhost", 9000)
        self.server.new_client_connected.connect(self.populate_clients_list_from_db)
        self.ui.activity_search.textChanged.connect(self.filter_processes)
        self.db_connection = db_connect.conectare_bd(
            host="localhost",
            user="root",
            password="rOOt",
            database="licenta"
        )
        self.setup_ui_elements()
        self.threadpool = QThreadPool()
        self.network_worker = NetworkWorker(self.server)
        self.sorter = CommandWorker(self, self.server)
        self.sorter.signals.update_data.connect(self.handle_update_data)
        self.sorter.signals.status_proc.connect(self.handle_client_response)
        self.update_ui_signal.connect(self.update_ui_elements)  # Connect the signal here
        self.process_loader_thread = QThread()
        self.process_loader_worker = ProcessLoaderWorker()
        self.process_loader_worker.moveToThread(self.process_loader_thread)
        self.process_loader_worker.process_data_loaded.connect(self.handle_process_data_loaded)
        self.process_loader_worker.finished.connect(self.process_loader_thread.quit)
        self.process_loader_thread.started.connect(self.process_loader_worker.run)
        self.start_threads()

        loadJsonStyle(self, self.ui, jsonFiles={"json-styles/style.json"})
        QAppSettings.updateAppSettings(self)

        self.initialize_buttons()

        # Establish database connection


        # Set up signals for buttons
        self.ui.load_clienti.clicked.connect(self.load_clients)
        self.ui.load_locatii.clicked.connect(self.load_locations)
        self.ui.load_incaperi.clicked.connect(self.load_rooms)
        self.ui.add_button.clicked.connect(self.add_to_db)

        # Set up the QTableWidget with two columns
        self.ui.db_table.setColumnCount(2)
        self.ui.db_table.setHorizontalHeaderLabels(["General Name", "Status"])

        # Enable drag and drop
        self.ui.db_table.setDragEnabled(True)
        self.ui.db_table.setAcceptDrops(True)
        self.ui.db_table.setDropIndicatorShown(True)
        self.ui.db_table.setDragDropMode(QAbstractItemView.InternalMove)
        self.ui.db_table.dropEvent = self.drop_event

        # Restore the state of the QTableWidget
        self.restore_clients_list_state()

        # Ensure save state on close
        self.ui.close_button.clicked.connect(self.save_clients_list_state)
        self.ui.resize_button.clicked.connect(self.save_clients_list_state)

        # Populate the client list from the database
        self.populate_clients_list_from_db()

        self.ui.db_table.customContextMenuRequested.connect(self.open_menu)


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

        self.server.data_send(full_command, client_name, "powershell_command")


    def handle_update_data(self, command, data, client_name):
        print(f"handle_update_data called with command: {command}, data: {data}, client_name: {client_name}")

        self.update_ui_signal.emit(command, data, client_name)
        if command == "hardware":
            self.handle_hardware_info_response(client_name)
        elif command == "powershell_result":
            self.handle_powershell_result(data)


    def handle_powershell_result(self, response):
        self.ui.updates_table.clear()

        # Assuming response is a plain text string
        response_text = response.strip()
        lines = response_text.splitlines()

        # Debugging line to inspect lines
        print(f"lines: {lines}")

        if not lines or len(lines) < 2:
            return

        # Extract headers dynamically
        headers_line = lines[0].strip()
        headers = headers_line.split()

        # Calculate start positions of each column based on header line
        header_positions = []
        last_pos = 0
        for header in headers:
            header_start = headers_line.index(header, last_pos)
            header_positions.append(header_start)
            last_pos = header_start + len(header)
        header_positions.append(len(headers_line))  # Add end position of the last column

        # Debugging lines to inspect headers and their positions
        print(f"headers: {headers}")
        print(f"header_positions: {header_positions}")

        self.ui.updates_table.setColumnCount(len(headers))
        self.ui.updates_table.setHorizontalHeaderLabels(headers)

        self.ui.updates_table.setRowCount(len(lines) - 2)
        for row_idx, line in enumerate(lines[2:]):
            for col_idx in range(len(headers)):
                col_start = header_positions[col_idx]
                if col_idx == len(headers) - 1:
                    # For the last column, take the rest of the line
                    item_text = line[col_start:].strip()
                else:
                    col_end = header_positions[col_idx + 1]
                    item_text = line[col_start:col_end].strip()
                self.ui.updates_table.setItem(row_idx, col_idx, QTableWidgetItem(item_text))

        self.ui.updates_table.resizeColumnsToContents()


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
            'hardware': {},
            'installed_programs': {},
            'PSH': {}
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
        self.restore_clients_list_state()
        self.populate_clients_list_from_db()
        self.ui.clients_list.itemSelectionChanged.connect(self.client_selection_changed)
        self.ui.clients_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.clients_list.customContextMenuRequested.connect(self.open_menu)
        self.ui.interval_avg.currentIndexChanged.connect(self.update_info_label)
        self.ui.update_int.currentIndexChanged.connect(self.update_csv_timer)
        self.ui.update_int.currentTextChanged.connect(self.update_info_label)
        self.status_update_timer = QTimer(self)
        self.status_update_timer.timeout.connect(self.update_client_status)
        self.status_update_timer.start(5000)



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

        menu.exec_(self.ui.clients_list.viewport().mapToGlobal(position))


    def edit_client(self, index):
        item = self.ui.clients_list.itemFromIndex(index)
        client_name = item.text(0)
        new_client_name, ok = QInputDialog.getText(self, 'Edit Client', 'Enter new client name:', text=client_name)
        if ok and new_client_name:
            db_connect.actualizare_inregistrare(self.db_connection, 'clients', {'name': new_client_name},
                                                f"name='{client_name}'")
            self.populate_clients_list_from_db()


    def update_client_status(self, client_name, client_hwid, client_address, status):
        existing_client = db_connect.selectare_inregistrari(
            self.db_connection, 'clients', conditie=f"name='{client_name}'"
        )
        if existing_client:
            db_connect.actualizare_inregistrare(
                self.db_connection, 'clients',
                {'hwid': client_hwid, 'address': client_address[0], 'port': client_address[1], 'status': status},
                f"name='{client_name}'"
            )
        else:
            db_connect.adaugare_inregistrare(
                self.db_connection, 'clients',
                {'name': client_name, 'hwid': client_hwid, 'address': client_address[0], 'port': client_address[1],
                 'status': status}
            )


    def start_threads(self):
        self.threadpool.start(self.network_worker)
        self.threadpool.start(self.sorter)

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

        self.store_power_data(self.current_client_name, response["cpu_power"], response["dgpu_power"],
                              response["igpu_power"])

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
            conditie=f"client_name='{client_name}' AND timestamp BETWEEN '{start_date}' AND '{end_date}'"
        )

        if power_data:
            cpu_power_avg = sum(float(data[2]) for data in power_data) / len(power_data)
            dgpu_power_avg = sum(float(data[3]) for data in power_data) / len(power_data)
            igpu_power_avg = sum(float(data[4]) for data in power_data) / len(power_data)
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

    def store_power_data(self, client_name, cpu_power, dgpu_power, igpu_power):
        data = {
            'client_name': client_name,
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'cpu_power': cpu_power,
            'dgpu_power': dgpu_power,
            'igpu_power': igpu_power
        }
        db_connect.adaugare_inregistrare(self.db_connection, 'power_data', data)

    def store_hardware_data(self, client_name, hardware_info):
        for key, value in hardware_info.items():
            data = {
                'client_name': client_name,
                'hardware_key': key,
                'hardware_value': value,
                'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            db_connect.adaugare_inregistrare(self.db_connection, 'hardware_data', data)

    def get_hardware_info_from_db(self, client_name):
        hardware_data = db_connect.selectare_inregistrari(
            self.db_connection,
            'hardware_data',
            conditie=f"client_name='{client_name}'"
        )
        return hardware_data

    def update_csv_timer(self):
        interval = self.ui.update_int.currentText()
        if interval == "every minute":
            self.csv_timer.start(60 * 1000)
        elif interval == "5 minutes":
            self.csv_timer.start(5 * 60 * 1000)
        elif interval == "10 minutes":
            self.csv_timer.start(10 * 60 * 1000)
        elif interval == "30 minutes":
            self.csv_timer.start(30 * 60 * 1000)
        elif interval == "1 hour":
            self.csv_timer.start(60 * 60 * 1000)


    @Slot()
    def populate_clients_list_from_db(self):
        self.ui.clients_list.clear()  # Clear the existing items
        clients = db_connect.selectare_inregistrari(self.db_connection, 'client')

        locations = {}

        for client in clients:
            client_name = client[1]
            client_status = client[5]  # Assuming the status is stored in the 6th column
            location = client[6]  # Assuming location is stored in the 7th column
            classroom = client[7]  # Assuming classroom is stored in the 8th column

            if location not in locations:
                location_item = QTreeWidgetItem([location])
                self.ui.clients_list.addTopLevelItem(location_item)
                locations[location] = location_item
            else:
                location_item = locations[location]

            classroom_items = {location_item.child(i).text(0): location_item.child(i) for i in
                               range(location_item.childCount())}

            if classroom not in classroom_items:
                classroom_item = QTreeWidgetItem([classroom])
                location_item.addChild(classroom_item)
            else:
                classroom_item = classroom_items[classroom]

            client_item = QTreeWidgetItem([client_name, client_status])
            classroom_item.addChild(client_item)

    def drop_event(self, event):
        source_item = self.ui.db_table.currentItem()
        target_item = self.ui.db_table.itemAt(event.pos())

        if source_item and target_item:
            # Ensure the source item is a client and target item is a classroom
            if source_item.columnCount() == 2 and target_item.columnCount() == 1:
                new_location = target_item.text(0)
                new_classroom = target_item.text(0)
                client_name = source_item.text(0)

                location_id = \
                db_connect.selectare_inregistrari(self.db_connection, 'locatii', conditie=f"name='{new_location}'")[0][
                    0]
                room_id = db_connect.selectare_inregistrari(self.db_connection, 'incaperi',
                                                            conditie=f"name='{new_classroom}' AND location_id={location_id}")[
                    0][0]

                db_connect.actualizare_inregistrare(
                    self.db_connection, 'client',
                    {'location_id': location_id, 'room_id': room_id},
                    f"name='{client_name}'"
                )

                self.populate_clients_list_from_db()

        super().dropEvent(event)

    def update_client_status(self):
        clients = self.server.get_all_clients()
        for client in clients:
            client_name = client[1]
            client_status = client[2]  # Assuming the status is stored in the 3rd column
            self.set_client_status(client_name, client_status)

    def set_client_status(self, client_name, status):
        for row in range(self.ui.db_table.rowCount()):
            if self.ui.db_table.item(row, 0).text() == client_name:
                self.ui.db_table.setItem(row, 1, QTableWidgetItem(status))
                break

    def client_selection_changed(self):
        selected_items = self.ui.clients_list.selectedItems()
        if selected_items:
            self.current_client_name = selected_items[0].text(0)

    def save_clients_list_state(self):
        state = {
            "selected_items": [self.ui.db_table.item(row, 0).text() for row in range(self.ui.db_table.rowCount()) if
                               self.ui.db_table.isItemSelected(self.ui.db_table.item(row, 0))],
            # QTableWidget doesn't have expandable items, so we skip expanded items
        }
        with open("clients_list_state.pkl", "wb") as f:
            pickle.dump(state, f)

    def restore_clients_list_state(self):
        try:
            with open("clients_list_state.pkl", "rb") as f:
                state = pickle.load(f)
                self.set_selected_items(self.ui.db_table, state["selected_items"])
        except FileNotFoundError:
            pass

    def set_selected_items(self, table_widget, selected_items):
        for row in range(table_widget.rowCount()):
            if table_widget.item(row, 0).text() in selected_items:
                table_widget.selectRow(row)

    def remove_client(self, index):
        client_name = self.ui.db_table.item(index.row(), 0).text()
        print(f"Remove {client_name}")

    def delete_client(self, index):
        client_name = self.ui.db_table.item(index.row(), 0).text()
        self.server.data_send("shutdown", client_name, "shutdown")
        client = db_connect.selectare_inregistrari(self.db_connection, 'client', conditie=f"name='{client_name}'")[0]
        self.server.cleanup_client(client, client_name)
        self.ui.db_table.removeRow(index.row())
        print(f"Deleted {client_name}")

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

    def add_to_db(self):
        location = self.ui.location_input.text().strip()
        room = self.ui.room_input.text().strip()

        if location and room:
            # Add both location and room to the database
            db_connect.adaugare_inregistrare(self.db_connection, 'locatii', {'name': location})
            location_id = \
            db_connect.selectare_inregistrari(self.db_connection, 'locatii', conditie=f"name='{location}'")[0][0]
            db_connect.adaugare_inregistrare(self.db_connection, 'incaperi', {'name': room, 'location_id': location_id})
        elif location:
            # Add only location to the database
            db_connect.adaugare_inregistrare(self.db_connection, 'locatii', {'name': location})
        elif room:
            # Add only room to the database (assuming room needs a location)
            location = self.ui.db_table.currentItem().text() if self.ui.db_table.currentItem() else ""
            location_id = \
            db_connect.selectare_inregistrari(self.db_connection, 'locatii', conditie=f"name='{location}'")[0][0]
            db_connect.adaugare_inregistrare(self.db_connection, 'incaperi', {'name': room, 'location_id': location_id})

        # Clear input fields
        self.ui.location_input.clear()
        self.ui.room_input.clear()

        # Refresh the relevant list
        if location and room:
            self.load_locations()
            self.load_rooms()
        elif location:
            self.load_locations()
        elif room:
            self.load_rooms()


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
            "installed_programs": self.installed_programs,
            "powershell_result": self.handle_powershell_result,
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


    def get_item_path(self, item):
        path = []
        while item is not None:
            path.append(item.text(0))
            item = item.parent()
        return ' > '.join(reversed(path))


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
        self.update_table(self.ui.installed_table, installed_program, ["Name", "Version", "Install Date", "Publisher"])


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
                    self.create_table_widget(row, 2, f"{current_temp:.2f}", 'sensors_table')
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
        self.process_loader_thread.start()


    def handle_process_data_loaded(self, process_data):
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

        rowPosition = self.ui.tableWidget.rowCount()
        self.ui.tableWidget.insertRow(rowPosition)
        self.create_table_widget(rowPosition, 0, str(pid), "tableWidget")
        self.create_table_widget(rowPosition, 1, name, "tableWidget")
        self.create_table_widget(rowPosition, 2, status, "tableWidget")
        self.create_table_widget(rowPosition, 3, create_time, "tableWidget")
        self.add_buttons(rowPosition)


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
            self.update_process_table(process.pid, past_tense_action)
        except Exception as e:
            print(f"Error {action} process {process.pid}: {e}")


    def remove_process_row(self, row):
        self.ui.tableWidget.removeRow(row)
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
        data = self.data['hardware'][client_name]
        self.write_hardware_info_to_db(data[0], client_name)


    def write_hardware_info_to_db(self, data, client_name):
        for key, value in data.items():
            db_connect.adaugare_inregistrare(self.db_connection, 'hardware_info', {
                'client_name': client_name,
                'hardware_key': key,
                'hardware_value': value,
                'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        print(f"Hardware info for {client_name} has been written to the database.")


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
        self.save_clients_list_state()
        if event:
            event.accept()
        self.close()


    def dropEvent(self, event):
        source_item = self.ui.clients_list.currentItem()
        if source_item:
            event.accept()
        else:
            event.ignore()
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
    # TODO:DB
    # WIDGET PT BAZA DE DATE DE ADAUGAT LOCATII
    # BUTON INVENTAR(pe viitor de adaugat locatii)
    # sa salvez treewidged-ul(need to fix,after db work)
    # adaugare imprimante
    # INSTALLER
########################################################################
## END===>
########################################################################