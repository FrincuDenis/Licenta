import sys
import socket
import json
import time
from PySide2.QtCore import QThread, Signal
from PySide2.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem, QLabel, QVBoxLayout, QWidget

class SystemInfoWorker(QThread):
    info_signal = Signal(dict)

    def __init__(self):
        super().__init__()
        self.running = True

    def run(self):
        while self.running:
            system_info = self.get_system_info_from_server()
            if system_info:
                self.info_signal.emit(system_info)
            time.sleep(5)  # Update every 5 seconds

    def stop(self):
        self.running = False

    def get_system_info_from_server(self):
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(('127.0.0.1', 9999))
            client.send(b"GET_SYSTEM_INFO")
            response = client.recv(4096)
            client.close()
            system_info = json.loads(response.decode('utf-8'))
            return system_info
        except Exception as e:
            print(f"Error: {e}")
            return None

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Client UI")

        # Create a central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Create a QVBoxLayout
        self.layout = QVBoxLayout(self.central_widget)

        # Create a QTreeWidget
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabels(["Clients"])

        # Add sample clients to the QTreeWidget
        clients = ["Server 1"]
        for client in clients:
            item = QTreeWidgetItem([client])
            self.tree_widget.addTopLevelItem(item)

        # Connect the selection change signal to a slot function
        self.tree_widget.itemSelectionChanged.connect(self.on_client_selected)

        # Add QTreeWidget to the layout
        self.layout.addWidget(self.tree_widget)

        # Create a QLabel to display selected client details
        self.client_label = QLabel("Select a client")
        self.layout.addWidget(self.client_label)

        # Initialize the worker thread
        self.worker = SystemInfoWorker()
        self.worker.info_signal.connect(self.update_label)

    def update_label(self, info):
        info_text = (
            f"Time: {info['time']}\n"
            f"Date: {info['date']}\n"
            f"Machine: {info['machine']}\n"
            f"Version: {info['version']}\n"
            f"Platform: {info['platform']}\n"
            f"System: {info['system']}\n"
            f"Processor: {info['processor']}"
        )
        self.client_label.setText(info_text)

    def on_client_selected(self):
        selected_items = self.tree_widget.selectedItems()
        if selected_items and selected_items[0].text(0) == "Server 1":
            self.worker.start()
        else:
            self.worker.stop()
            self.client_label.setText("No client selected")

    def closeEvent(self, event):
        self.worker.stop()
        self.worker.wait()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
