import sys
import os
import subprocess
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QCheckBox, QPushButton, QFileDialog, \
    QMessageBox

# Predefined list of software packages and their silent install arguments
software_packages = [
    {'name': 'winrar', 'args': '--install-arguments="/S"'},
    {'name': 'microsoft-office-deployment', 'args': '--install-arguments="/quiet"'},
    {'name': 'googlechrome', 'args': '--install-arguments="/silent /install"'},
    {'name': 'adobereader', 'args': '--install-arguments="/sAll /msi /norestart"'},
    {'name': 'vlc', 'args': '--install-arguments="--quiet"'},
    {'name': 'zoom', 'args': '--install-arguments="/quiet"'},
    {'name': 'googledrive', 'args': '--install-arguments="/silent"'},
    {'name': 'teamviewer', 'args': '--install-arguments="/S"'},
    {'name': 'anydesk', 'args': '--install-arguments="/S"'},
]


class ChocoPackageGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Chocolatey Package Generator')
        self.layout = QVBoxLayout()

        self.label = QLabel('Select the programs to include in the package:')
        self.layout.addWidget(self.label)

        self.checkboxes = []
        for software in software_packages:
            checkbox = QCheckBox(software['name'])
            self.layout.addWidget(checkbox)
            self.checkboxes.append(checkbox)

        self.generateButton = QPushButton('Generate Package')
        self.generateButton.clicked.connect(self.generatePackage)
        self.layout.addWidget(self.generateButton)

        self.setLayout(self.layout)

    def generatePackage(self):
        selected_packages = [software_packages[i] for i, checkbox in enumerate(self.checkboxes) if checkbox.isChecked()]

        if not selected_packages:
            QMessageBox.warning(self, 'No Selection', 'Please select at least one program.')
            return

        directory = QFileDialog.getExistingDirectory(self, 'Select Directory to Save Package')

        if not directory:
            return

        package_id = "custom-software-package"
        package_version = "1.0.0"
        package_title = "Custom Software Package"
        authors = "Your Name"
        description = "Installs selected software"
        release_notes = "Initial release"
        tags = "software installation automation"

        package_path = os.path.join(directory, package_id)

        # Create the package directory structure
        os.makedirs(os.path.join(package_path, 'tools'), exist_ok=True)

        # Create the .nuspec file
        nuspec_content = f"""<?xml version="1.0"?>
<package xmlns="http://schemas.microsoft.com/packaging/2013/05/nuspec.xsd">
  <metadata>
    <id>{package_id}</id>
    <version>{package_version}</version>
    <title>{package_title}</title>
    <authors>{authors}</authors>
    <owners>{authors}</owners>
    <description>{description}</description>
    <releaseNotes>{release_notes}</releaseNotes>
    <tags>{tags}</tags>
  </metadata>
  <files>
    <file src="tools\\chocolateyInstall.ps1" target="tools\\chocolateyInstall.ps1" />
  </files>
</package>
"""

        with open(os.path.join(package_path, f"{package_id}.nuspec"), 'w') as file:
            file.write(nuspec_content)

        # Create the chocolateyInstall.ps1 script
        install_script_content = """# Chocolatey package names for the software with silent install arguments
$packages = @(
"""

        for software in selected_packages:
            install_script_content += f"    @{'{'}\n"
            install_script_content += f"        name = '{software['name']}'\n"
            install_script_content += f"        args = '{software['args']}'\n"
            install_script_content += f"    {'}'},\n"

        install_script_content += """)

foreach ($package in $packages) {
    Write-Host "Installing $($package.name)..."
    choco install $($package.name) -y $($package.args)
}

Write-Host "All applications have been installed."
"""

        with open(os.path.join(package_path, 'tools', 'chocolateyInstall.ps1'), 'w') as file:
            file.write(install_script_content)

        # Package the files using nuget
        subprocess.run(['nuget', 'pack', f"{package_id}.nuspec"], cwd=package_path)

        QMessageBox.information(self, 'Package Created',
                                f"Chocolatey package '{package_id}' has been created successfully at {directory}.")


def main():
    app = QApplication(sys.argv)
    generator = ChocoPackageGenerator()
    generator.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
