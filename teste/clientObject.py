import sys
import socket
from PySide2.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton,
                               QTextEdit, QLineEdit, QLabel, QHBoxLayout)

class ServerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Server Command Sender")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.output_text = QTextEdit(self)
        self.output_text.setReadOnly(True)
        self.layout.addWidget(self.output_text)

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
        self.output_text.append(f"Command: {command}\nResponse: {response}\n")

    def send_command_to_client(self, command):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(('localhost', 65432))
                s.sendall(command.encode())
                data = s.recv(4096)
                return data.decode()
        except Exception as e:
            return f"Failed to send command: {e}"

def main():
    app = QApplication(sys.argv)
    server_app = ServerApp()
    server_app.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
