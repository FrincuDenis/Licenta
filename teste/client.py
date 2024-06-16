import sys
import subprocess
import winreg
from PySide2.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, \
    QWidget, QMessageBox


def format_date(install_date):
    if len(install_date) == 8:
        return f"{install_date[:4]}-{install_date[4:6]}-{install_date[6:]}"
    return install_date


def get_installed_programs():
    program_list = []

    # Registry paths to check for installed applications (32-bit and 64-bit)
    registry_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    ]

    for path in registry_paths:
        try:
            # Open the registry key
            reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)

            # Enumerate through the subkeys
            for i in range(0, winreg.QueryInfoKey(reg_key)[0]):
                sub_key_name = winreg.EnumKey(reg_key, i)
                sub_key = winreg.OpenKey(reg_key, sub_key_name)
                try:
                    # Fetch the program name
                    program_name = winreg.QueryValueEx(sub_key, "DisplayName")[0]
                    try:
                        program_version = winreg.QueryValueEx(sub_key, "DisplayVersion")[0]
                    except FileNotFoundError:
                        program_version = "Unknown Version"
                    try:
                        install_date = winreg.QueryValueEx(sub_key, "InstallDate")[0]
                        install_date = format_date(install_date)
                    except FileNotFoundError:
                        install_date = "Unknown Date"
                    try:
                        publisher = winreg.QueryValueEx(sub_key, "Publisher")[0]
                    except FileNotFoundError:
                        publisher = "Unknown Publisher"
                    program_list.append({
                        "Name": program_name,
                        "Version": program_version,
                        "Install Date": install_date,
                        "Publisher": publisher
                    })
                except FileNotFoundError:
                    # If DisplayName does not exist, skip the entry
                    continue
                finally:
                    sub_key.Close()
            reg_key.Close()
        except FileNotFoundError:
            # If the registry path does not exist, skip it
            continue

    return program_list


def install_program(package_name):
    try:
        result = subprocess.run(["choco", "install", package_name, "-y"], capture_output=True, text=True)
        if result.returncode == 0:
            return f"Successfully installed {package_name}."
        else:
            return f"Failed to install {package_name}.\n{result.stderr}"
    except Exception as e:
        return f"An error occurred: {str(e)}"


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Installed Programs and Chocolatey Installer')

        layout = QVBoxLayout()

        self.program_list = QListWidget()
        layout.addWidget(self.program_list)

        self.refresh_button = QPushButton('Refresh Installed Programs')
        self.refresh_button.clicked.connect(self.refresh_programs)
        layout.addWidget(self.refresh_button)

        install_layout = QHBoxLayout()
        self.package_input = QLineEdit()
        self.package_input.setPlaceholderText('Enter package name to install')
        install_layout.addWidget(self.package_input)
        self.install_button = QPushButton('Install')
        self.install_button.clicked.connect(self.install_package)
        install_layout.addWidget(self.install_button)
        layout.addLayout(install_layout)

        self.setLayout(layout)
        self.refresh_programs()

    def refresh_programs(self):
        self.program_list.clear()
        programs = get_installed_programs()
        for program in programs:
            self.program_list.addItem(
                f"Name: {program['Name']}, Version: {program['Version']}, Install Date: {program['Install Date']}, Publisher: {program['Publisher']}")

    def install_package(self):
        package_name = self.package_input.text()
        if package_name:
            message = install_program(package_name)
            QMessageBox.information(self, 'Install Result', message)
        else:
            QMessageBox.warning(self, 'Input Error', 'Please enter a package name.')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
