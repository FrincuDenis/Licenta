import sys
import socket
from PySide2.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton,
                               QLineEdit, QHBoxLayout, QTableWidget, QTableWidgetItem)
from PySide2.QtCore import Qt

CHUNK_SIZE = 4096
END_OF_MESSAGE = b'<<END_OF_MESSAGE>>'

class ServerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Server Command Sender")
        self.setGeometry(100, 100, 1000, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.output_table = QTableWidget(self)
        self.layout.addWidget(self.output_table)

        self.input_layout = QHBoxLayout()
        self.command_input = QLineEdit(self)
        self.input_layout.addWidget(self.command_input)
        self.send_button = QPushButton("Send Command", self)
        self.send_button.clicked.connect(self.send_command)
        self.input_layout.addWidget(self.send_button)
        self.layout.addLayout(self.input_layout)

        self.commands = [
            "check-updates", "install-updates", "hide-update <KBID>",
            "schedule-update <UPDATE_ID> <REVISION> <HOUR> <MINUTE>",
            "add-microsoft-update-service", "add-offline-sync-service <FILE_PATH>",
            "get-update-history", "get-update-history-24h", "uninstall-update <KBID>",
            "get-update-settings", "set-target-version <PRODUCT_VERSION> <TARGET_VERSION>"
        ]

        for command in self.commands:
            button = QPushButton(command, self)
            button.clicked.connect(self.create_command_handler(command))
            self.layout.addWidget(button)

    def create_command_handler(self, command):
        def handler():
            if "<" in command and ">" in command:
                self.command_input.setText(command)
            else:
                self.send_command(command)
        return handler

    def send_command(self, command=None):
        if command is None:
            command = self.command_input.text()

        self.command_input.clear()
        response = self.send_command_to_client(command)
        self.display_response_in_table(response)

    def send_command_to_client(self, command):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(('localhost', 65432))
                s.sendall(command.encode())

                response = []
                while True:
                    data = s.recv(CHUNK_SIZE)
                    print(data.decode())
                    if END_OF_MESSAGE in data:
                        response.append(data.replace(END_OF_MESSAGE, b'').decode())
                        break
                    response.append(data.decode())
                return ''.join(response)
        except Exception as e:
            return f"Failed to send command: {e}"

    def display_response_in_table(self, response):
        self.output_table.clear()
        lines = response.splitlines()

        if not lines:
            return

        # Extract headers from the first line and determine column widths
        headers = lines[1].split()
        self.output_table.setColumnCount(len(headers))
        self.output_table.setHorizontalHeaderLabels(headers)

        # Find the indices for splitting based on header positions
        col_indices = [lines[1].index(header) for header in headers] + [len(lines[0])]

        # Add rows
        self.output_table.setRowCount(len(lines) - 2)
        for row_idx, line in enumerate(lines[2:]):
            for col_idx in range(len(headers)):
                item_text = line[col_indices[col_idx]:col_indices[col_idx + 1]].strip()
                self.output_table.setItem(row_idx, col_idx, QTableWidgetItem(item_text))

        self.output_table.resizeColumnsToContents()

def main():
    app = QApplication(sys.argv)
    server_app = ServerApp()
    server_app.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
