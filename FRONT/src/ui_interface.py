# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_interface.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from Custom_Widgets.QCustomSlideMenu import QCustomSlideMenu
from PySide2extn.RoundProgressBar import roundProgressBar
from PySide2extn.SpiralProgressBar import spiralProgressBar
from Custom_Widgets.Theme import QPushButton
from Custom_Widgets.Theme import QLabel

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1217, 850)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setStyleSheet(u"*{\n"
"border: none;\n"
"}\n"
"QLineEdit{\n"
"	background-color: rgb(255, 255, 255);\n"
"	color:rgb(0,0,0);\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.header_frame = QFrame(self.centralwidget)
        self.header_frame.setObjectName(u"header_frame")
        self.header_frame.setMinimumSize(QSize(300, 0))
        self.header_frame.setStyleSheet(u"*{\n"
"background-color:#24374B;\n"
"}")
        self.header_frame.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_4 = QHBoxLayout(self.header_frame)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.header_left = QFrame(self.header_frame)
        self.header_left.setObjectName(u"header_left")
        self.header_left.setMaximumSize(QSize(600, 16777215))
        self.header_left.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_7 = QHBoxLayout(self.header_left)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.menu_bt = QPushButton(self.header_left)
        self.menu_bt.setObjectName(u"menu_bt")
        font = QFont()
        font.setFamily(u"ROG Fonts")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.menu_bt.setFont(font)
        icon = QIcon()
        icon.addFile(u":/feather/icons/feather/menu.png", QSize(), QIcon.Normal, QIcon.Off)
        self.menu_bt.setIcon(icon)
        self.menu_bt.setIconSize(QSize(32, 32))

        self.horizontalLayout_7.addWidget(self.menu_bt, 0, Qt.AlignLeft)


        self.horizontalLayout_4.addWidget(self.header_left)

        self.header_center = QFrame(self.header_frame)
        self.header_center.setObjectName(u"header_center")
        self.header_center.setMinimumSize(QSize(300, 0))
        self.header_center.setMaximumSize(QSize(300, 16777215))
        self.header_center.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_3 = QHBoxLayout(self.header_center)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.title_icon = QLabel(self.header_center)
        self.title_icon.setObjectName(u"title_icon")
        self.title_icon.setMaximumSize(QSize(30, 30))
        self.title_icon.setAutoFillBackground(False)
        self.title_icon.setPixmap(QPixmap(u":/material_design/icons/material_design/important_devices.png"))
        self.title_icon.setScaledContents(True)

        self.horizontalLayout_3.addWidget(self.title_icon)

        self.title = QLabel(self.header_center)
        self.title.setObjectName(u"title")
        self.title.setMaximumSize(QSize(16777215, 16777215))
        font1 = QFont()
        font1.setFamily(u"ROG Fonts")
        font1.setPointSize(12)
        font1.setBold(False)
        font1.setWeight(50)
        self.title.setFont(font1)

        self.horizontalLayout_3.addWidget(self.title, 0, Qt.AlignLeft)


        self.horizontalLayout_4.addWidget(self.header_center, 0, Qt.AlignHCenter)

        self.header_right = QFrame(self.header_frame)
        self.header_right.setObjectName(u"header_right")
        self.header_right.setMinimumSize(QSize(100, 0))
        self.header_right.setMaximumSize(QSize(100, 16777215))
        self.header_right.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_2 = QHBoxLayout(self.header_right)
        self.horizontalLayout_2.setSpacing(20)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.minimize_button = QPushButton(self.header_right)
        self.minimize_button.setObjectName(u"minimize_button")
        icon1 = QIcon()
        icon1.addFile(u":/feather/icons/feather/window_minimize.png", QSize(), QIcon.Normal, QIcon.Off)
        self.minimize_button.setIcon(icon1)

        self.horizontalLayout_2.addWidget(self.minimize_button)

        self.resize_button = QPushButton(self.header_right)
        self.resize_button.setObjectName(u"resize_button")
        icon2 = QIcon()
        icon2.addFile(u":/font_awesome_regular/icons/font_awesome/regular/window-restore.png", QSize(), QIcon.Normal, QIcon.Off)
        self.resize_button.setIcon(icon2)

        self.horizontalLayout_2.addWidget(self.resize_button)

        self.close_button = QPushButton(self.header_right)
        self.close_button.setObjectName(u"close_button")
        icon3 = QIcon()
        icon3.addFile(u":/feather/icons/feather/window_close.png", QSize(), QIcon.Normal, QIcon.Off)
        self.close_button.setIcon(icon3)

        self.horizontalLayout_2.addWidget(self.close_button)


        self.horizontalLayout_4.addWidget(self.header_right, 0, Qt.AlignRight)


        self.verticalLayout.addWidget(self.header_frame)

        self.main_body_frame = QFrame(self.centralwidget)
        self.main_body_frame.setObjectName(u"main_body_frame")
        sizePolicy.setHeightForWidth(self.main_body_frame.sizePolicy().hasHeightForWidth())
        self.main_body_frame.setSizePolicy(sizePolicy)
        self.main_body_frame.setMinimumSize(QSize(0, 0))
        self.main_body_frame.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_8 = QHBoxLayout(self.main_body_frame)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.left_main = QCustomSlideMenu(self.main_body_frame)
        self.left_main.setObjectName(u"left_main")
        self.verticalLayout_18 = QVBoxLayout(self.left_main)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.verticalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.menu = QFrame(self.left_main)
        self.menu.setObjectName(u"menu")
        self.menu.setMinimumSize(QSize(210, 0))
        self.menu.setFrameShape(QFrame.NoFrame)
        self.gridLayout = QGridLayout(self.menu)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, -1, -1, -1)
        self.label_23 = QLabel(self.menu)
        self.label_23.setObjectName(u"label_23")
        font2 = QFont()
        font2.setFamily(u"ROG Fonts")
        self.label_23.setFont(font2)

        self.gridLayout.addWidget(self.label_23, 1, 1, 1, 1)

        self.Storage = QPushButton(self.menu)
        self.Storage.setObjectName(u"Storage")
        icon4 = QIcon()
        icon4.addFile(u":/feather/icons/feather/disc.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Storage.setIcon(icon4)
        self.Storage.setIconSize(QSize(40, 40))

        self.gridLayout.addWidget(self.Storage, 6, 0, 1, 1)

        self.DB = QPushButton(self.menu)
        self.DB.setObjectName(u"DB")
        icon5 = QIcon()
        icon5.addFile(u":/feather/icons/feather/table.png", QSize(), QIcon.Normal, QIcon.Off)
        self.DB.setIcon(icon5)
        self.DB.setIconSize(QSize(40, 40))

        self.gridLayout.addWidget(self.DB, 9, 0, 1, 1)

        self.LocalAcc = QPushButton(self.menu)
        self.LocalAcc.setObjectName(u"LocalAcc")
        icon6 = QIcon()
        icon6.addFile(u":/material_design/icons/material_design/person.png", QSize(), QIcon.Normal, QIcon.Off)
        self.LocalAcc.setIcon(icon6)
        self.LocalAcc.setIconSize(QSize(40, 40))

        self.gridLayout.addWidget(self.LocalAcc, 0, 0, 1, 1)

        self.label_3 = QLabel(self.menu)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font2)
        self.label_3.setMargin(5)

        self.gridLayout.addWidget(self.label_3, 3, 1, 1, 1)

        self.Sysinfo = QPushButton(self.menu)
        self.Sysinfo.setObjectName(u"Sysinfo")
        icon7 = QIcon()
        icon7.addFile(u":/feather/icons/feather/monitor.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Sysinfo.setIcon(icon7)
        self.Sysinfo.setIconSize(QSize(40, 40))

        self.gridLayout.addWidget(self.Sysinfo, 4, 0, 1, 1)

        self.power = QPushButton(self.menu)
        self.power.setObjectName(u"power")
        icon8 = QIcon()
        icon8.addFile(u":/feather/icons/feather/zap.png", QSize(), QIcon.Normal, QIcon.Off)
        self.power.setIcon(icon8)
        self.power.setIconSize(QSize(40, 40))

        self.gridLayout.addWidget(self.power, 3, 0, 1, 1)

        self.label_8 = QLabel(self.menu)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setEnabled(False)
        font3 = QFont()
        font3.setFamily(u"Asus Rog")
        self.label_8.setFont(font3)
        self.label_8.setMargin(5)

        self.gridLayout.addWidget(self.label_8, 8, 2, 1, 1)

        self.Activities = QPushButton(self.menu)
        self.Activities.setObjectName(u"Activities")
        icon9 = QIcon()
        icon9.addFile(u":/feather/icons/feather/activity.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Activities.setIcon(icon9)
        self.Activities.setIconSize(QSize(40, 40))

        self.gridLayout.addWidget(self.Activities, 5, 0, 1, 1)

        self.Sensors = QPushButton(self.menu)
        self.Sensors.setObjectName(u"Sensors")
        icon10 = QIcon()
        icon10.addFile(u":/font_awesome_solid/icons/font_awesome/solid/temperature-empty.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Sensors.setIcon(icon10)
        self.Sensors.setIconSize(QSize(40, 40))

        self.gridLayout.addWidget(self.Sensors, 7, 0, 1, 1)

        self.label_9 = QLabel(self.menu)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font2)

        self.gridLayout.addWidget(self.label_9, 0, 1, 1, 1)

        self.program = QPushButton(self.menu)
        self.program.setObjectName(u"program")
        icon11 = QIcon()
        icon11.addFile(u":/material_design/icons/material_design/install_desktop.png", QSize(), QIcon.Normal, QIcon.Off)
        self.program.setIcon(icon11)
        self.program.setIconSize(QSize(40, 40))

        self.gridLayout.addWidget(self.program, 11, 0, 1, 1)

        self.updates = QPushButton(self.menu)
        self.updates.setObjectName(u"updates")
        icon12 = QIcon()
        icon12.addFile(u":/feather/icons/feather/alert-triangle.png", QSize(), QIcon.Normal, QIcon.Off)
        self.updates.setIcon(icon12)
        self.updates.setIconSize(QSize(40, 40))

        self.gridLayout.addWidget(self.updates, 12, 0, 1, 1)

        self.label_46 = QLabel(self.menu)
        self.label_46.setObjectName(u"label_46")
        self.label_46.setFont(font2)

        self.gridLayout.addWidget(self.label_46, 9, 1, 1, 1)

        self.label_48 = QLabel(self.menu)
        self.label_48.setObjectName(u"label_48")
        self.label_48.setFont(font2)

        self.gridLayout.addWidget(self.label_48, 11, 1, 1, 1)

        self.Network = QPushButton(self.menu)
        self.Network.setObjectName(u"Network")
        icon13 = QIcon()
        icon13.addFile(u":/font_awesome_solid/icons/font_awesome/solid/network-wired.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Network.setIcon(icon13)
        self.Network.setIconSize(QSize(40, 40))

        self.gridLayout.addWidget(self.Network, 8, 0, 1, 1)

        self.label_5 = QLabel(self.menu)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font2)
        self.label_5.setMargin(5)

        self.gridLayout.addWidget(self.label_5, 5, 1, 1, 1)

        self.CPU = QPushButton(self.menu)
        self.CPU.setObjectName(u"CPU")
        icon14 = QIcon()
        icon14.addFile(u":/feather/icons/feather/cpu.png", QSize(), QIcon.Normal, QIcon.Off)
        self.CPU.setIcon(icon14)
        self.CPU.setIconSize(QSize(40, 40))

        self.gridLayout.addWidget(self.CPU, 2, 0, 1, 1)

        self.label_4 = QLabel(self.menu)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font2)
        self.label_4.setMargin(5)

        self.gridLayout.addWidget(self.label_4, 4, 1, 1, 1)

        self.Domain = QPushButton(self.menu)
        self.Domain.setObjectName(u"Domain")
        icon15 = QIcon()
        icon15.addFile(u":/material_design/icons/material_design/domain.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Domain.setIcon(icon15)
        self.Domain.setIconSize(QSize(40, 40))

        self.gridLayout.addWidget(self.Domain, 1, 0, 1, 1)

        self.label_2 = QLabel(self.menu)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font2)
        self.label_2.setMargin(5)

        self.gridLayout.addWidget(self.label_2, 2, 1, 1, 1)

        self.label_18 = QLabel(self.menu)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setFont(font2)

        self.gridLayout.addWidget(self.label_18, 8, 1, 1, 1)

        self.label_6 = QLabel(self.menu)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font2)
        self.label_6.setMargin(5)

        self.gridLayout.addWidget(self.label_6, 6, 1, 1, 1)

        self.label_7 = QLabel(self.menu)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font2)
        self.label_7.setMargin(5)

        self.gridLayout.addWidget(self.label_7, 7, 1, 1, 1)

        self.label_49 = QLabel(self.menu)
        self.label_49.setObjectName(u"label_49")
        self.label_49.setFont(font2)

        self.gridLayout.addWidget(self.label_49, 12, 1, 1, 1)


        self.verticalLayout_18.addWidget(self.menu)


        self.horizontalLayout_8.addWidget(self.left_main)

        self.center_main = QFrame(self.main_body_frame)
        self.center_main.setObjectName(u"center_main")
        self.center_main.setFrameShape(QFrame.NoFrame)
        self.verticalLayout_2 = QVBoxLayout(self.center_main)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.stackedWidget = QStackedWidget(self.center_main)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.cpu_memory = QWidget()
        self.cpu_memory.setObjectName(u"cpu_memory")
        self.verticalLayout_6 = QVBoxLayout(self.cpu_memory)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.cpu_info = QFrame(self.cpu_memory)
        self.cpu_info.setObjectName(u"cpu_info")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.cpu_info.sizePolicy().hasHeightForWidth())
        self.cpu_info.setSizePolicy(sizePolicy1)
        self.cpu_info.setFrameShape(QFrame.NoFrame)
        self.gridLayout_2 = QGridLayout(self.cpu_info)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.cpu_per = QLabel(self.cpu_info)
        self.cpu_per.setObjectName(u"cpu_per")
        self.cpu_per.setFont(font2)

        self.gridLayout_2.addWidget(self.cpu_per, 1, 1, 1, 1)

        self.label_11 = QLabel(self.cpu_info)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font2)

        self.gridLayout_2.addWidget(self.label_11, 1, 0, 1, 1)

        self.cpu_cont = QLabel(self.cpu_info)
        self.cpu_cont.setObjectName(u"cpu_cont")
        self.cpu_cont.setFont(font2)

        self.gridLayout_2.addWidget(self.cpu_cont, 0, 1, 1, 1)

        self.label_12 = QLabel(self.cpu_info)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setFont(font2)

        self.gridLayout_2.addWidget(self.label_12, 2, 0, 1, 1)

        self.cpu_main_core = QLabel(self.cpu_info)
        self.cpu_main_core.setObjectName(u"cpu_main_core")
        self.cpu_main_core.setFont(font2)

        self.gridLayout_2.addWidget(self.cpu_main_core, 2, 1, 1, 1)

        self.label_10 = QLabel(self.cpu_info)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font2)

        self.gridLayout_2.addWidget(self.label_10, 0, 0, 1, 1)

        self.CPU_PROGRESS = roundProgressBar(self.cpu_info)
        self.CPU_PROGRESS.setObjectName(u"CPU_PROGRESS")
        self.CPU_PROGRESS.setMaximumSize(QSize(150, 150))

        self.gridLayout_2.addWidget(self.CPU_PROGRESS, 0, 2, 3, 1)


        self.verticalLayout_6.addWidget(self.cpu_info)

        self.ram_info = QFrame(self.cpu_memory)
        self.ram_info.setObjectName(u"ram_info")
        sizePolicy1.setHeightForWidth(self.ram_info.sizePolicy().hasHeightForWidth())
        self.ram_info.setSizePolicy(sizePolicy1)
        self.ram_info.setFrameShape(QFrame.NoFrame)
        self.gridLayout_3 = QGridLayout(self.ram_info)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.total_ram = QLabel(self.ram_info)
        self.total_ram.setObjectName(u"total_ram")
        self.total_ram.setFont(font2)

        self.gridLayout_3.addWidget(self.total_ram, 0, 3, 1, 1)

        self.label_14 = QLabel(self.ram_info)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setFont(font2)

        self.gridLayout_3.addWidget(self.label_14, 0, 2, 1, 1)

        self.label_16 = QLabel(self.ram_info)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setFont(font2)

        self.gridLayout_3.addWidget(self.label_16, 1, 2, 1, 1)

        self.available_ram = QLabel(self.ram_info)
        self.available_ram.setObjectName(u"available_ram")
        self.available_ram.setFont(font2)

        self.gridLayout_3.addWidget(self.available_ram, 1, 3, 1, 1)

        self.label_13 = QLabel(self.ram_info)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setFont(font2)

        self.gridLayout_3.addWidget(self.label_13, 4, 2, 1, 1)

        self.used_ram = QLabel(self.ram_info)
        self.used_ram.setObjectName(u"used_ram")
        self.used_ram.setFont(font2)

        self.gridLayout_3.addWidget(self.used_ram, 2, 3, 1, 1)

        self.RAM_PROGRESS = spiralProgressBar(self.ram_info)
        self.RAM_PROGRESS.setObjectName(u"RAM_PROGRESS")
        self.RAM_PROGRESS.setMaximumSize(QSize(150, 150))

        self.gridLayout_3.addWidget(self.RAM_PROGRESS, 0, 4, 5, 1)

        self.ram_usage = QLabel(self.ram_info)
        self.ram_usage.setObjectName(u"ram_usage")
        self.ram_usage.setFont(font2)

        self.gridLayout_3.addWidget(self.ram_usage, 4, 3, 1, 1)

        self.label_15 = QLabel(self.ram_info)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setFont(font2)

        self.gridLayout_3.addWidget(self.label_15, 2, 2, 1, 1)

        self.label_17 = QLabel(self.ram_info)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setFont(font2)

        self.gridLayout_3.addWidget(self.label_17, 3, 2, 1, 1)

        self.free_ram = QLabel(self.ram_info)
        self.free_ram.setObjectName(u"free_ram")
        self.free_ram.setFont(font2)

        self.gridLayout_3.addWidget(self.free_ram, 3, 3, 1, 1)


        self.verticalLayout_6.addWidget(self.ram_info)

        self.stackedWidget.addWidget(self.cpu_memory)
        self.Local_accounts = QWidget()
        self.Local_accounts.setObjectName(u"Local_accounts")
        self.verticalLayout_19 = QVBoxLayout(self.Local_accounts)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.frame_19 = QFrame(self.Local_accounts)
        self.frame_19.setObjectName(u"frame_19")
        self.frame_19.setFrameShape(QFrame.NoFrame)
        self.verticalLayout_22 = QVBoxLayout(self.frame_19)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.scrollArea_2 = QScrollArea(self.frame_19)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 636, 281))
        self.horizontalLayout_19 = QHBoxLayout(self.scrollAreaWidgetContents_2)
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.frame_20 = QFrame(self.scrollAreaWidgetContents_2)
        self.frame_20.setObjectName(u"frame_20")
        self.frame_20.setFrameShape(QFrame.NoFrame)
        self.verticalLayout_23 = QVBoxLayout(self.frame_20)
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.user_table = QTableWidget(self.frame_20)
        if (self.user_table.columnCount() < 12):
            self.user_table.setColumnCount(12)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setFont(font2);
        self.user_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setFont(font2);
        self.user_table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        __qtablewidgetitem2.setFont(font2);
        self.user_table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        __qtablewidgetitem3.setFont(font2);
        self.user_table.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        __qtablewidgetitem4.setFont(font2);
        self.user_table.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        __qtablewidgetitem5.setFont(font2);
        self.user_table.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        __qtablewidgetitem6.setFont(font2);
        self.user_table.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        __qtablewidgetitem7.setFont(font2);
        self.user_table.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        __qtablewidgetitem8.setFont(font2);
        self.user_table.setHorizontalHeaderItem(8, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        __qtablewidgetitem9.setFont(font2);
        self.user_table.setHorizontalHeaderItem(9, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        __qtablewidgetitem10.setFont(font2);
        self.user_table.setHorizontalHeaderItem(10, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        __qtablewidgetitem11.setFont(font2);
        self.user_table.setHorizontalHeaderItem(11, __qtablewidgetitem11)
        self.user_table.setObjectName(u"user_table")

        self.verticalLayout_23.addWidget(self.user_table)


        self.horizontalLayout_19.addWidget(self.frame_20)

        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)

        self.verticalLayout_22.addWidget(self.scrollArea_2)


        self.verticalLayout_19.addWidget(self.frame_19)

        self.label_34 = QLabel(self.Local_accounts)
        self.label_34.setObjectName(u"label_34")
        self.label_34.setFont(font2)

        self.verticalLayout_19.addWidget(self.label_34)

        self.frame_10 = QFrame(self.Local_accounts)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setMinimumSize(QSize(0, 130))
        self.frame_10.setMaximumSize(QSize(16777215, 130))
        self.frame_10.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_17 = QHBoxLayout(self.frame_10)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.frame_12 = QFrame(self.frame_10)
        self.frame_12.setObjectName(u"frame_12")
        self.frame_12.setMinimumSize(QSize(0, 50))
        self.frame_12.setMaximumSize(QSize(16777215, 50))
        self.frame_12.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_9 = QHBoxLayout(self.frame_12)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_19 = QLabel(self.frame_12)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setFont(font2)

        self.horizontalLayout_9.addWidget(self.label_19)

        self.user_text = QLineEdit(self.frame_12)
        self.user_text.setObjectName(u"user_text")

        self.horizontalLayout_9.addWidget(self.user_text)


        self.horizontalLayout_17.addWidget(self.frame_12)

        self.frame_13 = QFrame(self.frame_10)
        self.frame_13.setObjectName(u"frame_13")
        self.frame_13.setMinimumSize(QSize(0, 50))
        self.frame_13.setMaximumSize(QSize(16777215, 50))
        self.frame_13.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_10 = QHBoxLayout(self.frame_13)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_20 = QLabel(self.frame_13)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setFont(font2)

        self.horizontalLayout_10.addWidget(self.label_20)

        self.fullname_text = QLineEdit(self.frame_13)
        self.fullname_text.setObjectName(u"fullname_text")

        self.horizontalLayout_10.addWidget(self.fullname_text)


        self.horizontalLayout_17.addWidget(self.frame_13)


        self.verticalLayout_19.addWidget(self.frame_10)

        self.frame_14 = QFrame(self.Local_accounts)
        self.frame_14.setObjectName(u"frame_14")
        self.frame_14.setMinimumSize(QSize(0, 130))
        self.frame_14.setMaximumSize(QSize(16777215, 130))
        self.frame_14.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_22 = QHBoxLayout(self.frame_14)
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.frame_18 = QFrame(self.frame_14)
        self.frame_18.setObjectName(u"frame_18")
        self.frame_18.setMaximumSize(QSize(480, 16777215))
        self.frame_18.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_15 = QHBoxLayout(self.frame_18)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.label_21 = QLabel(self.frame_18)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setMaximumSize(QSize(100, 16777215))
        self.label_21.setFont(font2)

        self.horizontalLayout_15.addWidget(self.label_21, 0, Qt.AlignLeft)

        self.description_text = QLineEdit(self.frame_18)
        self.description_text.setObjectName(u"description_text")
        self.description_text.setMinimumSize(QSize(190, 0))
        self.description_text.setMaximumSize(QSize(190, 16777215))

        self.horizontalLayout_15.addWidget(self.description_text, 0, Qt.AlignLeft)


        self.horizontalLayout_22.addWidget(self.frame_18, 0, Qt.AlignLeft)

        self.frame_25 = QFrame(self.frame_14)
        self.frame_25.setObjectName(u"frame_25")
        self.frame_25.setFrameShape(QFrame.NoFrame)
        self.verticalLayout_21 = QVBoxLayout(self.frame_25)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.frame_26 = QFrame(self.frame_25)
        self.frame_26.setObjectName(u"frame_26")
        self.frame_26.setFrameShape(QFrame.StyledPanel)
        self.frame_26.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_20 = QHBoxLayout(self.frame_26)
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.label_41 = QLabel(self.frame_26)
        self.label_41.setObjectName(u"label_41")
        self.label_41.setMinimumSize(QSize(0, 0))
        self.label_41.setFont(font2)

        self.horizontalLayout_20.addWidget(self.label_41, 0, Qt.AlignLeft)

        self.acc_status = QComboBox(self.frame_26)
        self.acc_status.addItem("")
        self.acc_status.addItem("")
        self.acc_status.setObjectName(u"acc_status")
        self.acc_status.setMinimumSize(QSize(70, 0))
        self.acc_status.setMaximumSize(QSize(70, 16777215))
        self.acc_status.setFont(font2)

        self.horizontalLayout_20.addWidget(self.acc_status, 0, Qt.AlignLeft)


        self.verticalLayout_21.addWidget(self.frame_26, 0, Qt.AlignLeft)

        self.frame_28 = QFrame(self.frame_25)
        self.frame_28.setObjectName(u"frame_28")
        self.frame_28.setFrameShape(QFrame.StyledPanel)
        self.frame_28.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_21 = QHBoxLayout(self.frame_28)
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.label_43 = QLabel(self.frame_28)
        self.label_43.setObjectName(u"label_43")
        self.label_43.setFont(font2)

        self.horizontalLayout_21.addWidget(self.label_43, 0, Qt.AlignLeft)

        self.group_status = QComboBox(self.frame_28)
        self.group_status.setObjectName(u"group_status")
        self.group_status.setMinimumSize(QSize(200, 0))
        self.group_status.setMaximumSize(QSize(200, 16777215))
        self.group_status.setFont(font2)

        self.horizontalLayout_21.addWidget(self.group_status, 0, Qt.AlignLeft)


        self.verticalLayout_21.addWidget(self.frame_28, 0, Qt.AlignLeft)


        self.horizontalLayout_22.addWidget(self.frame_25)


        self.verticalLayout_19.addWidget(self.frame_14)

        self.frame_11 = QFrame(self.Local_accounts)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setMinimumSize(QSize(0, 120))
        self.frame_11.setMaximumSize(QSize(16777215, 120))
        self.frame_11.setFrameShape(QFrame.NoFrame)
        self.verticalLayout_20 = QVBoxLayout(self.frame_11)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.frame_15 = QFrame(self.frame_11)
        self.frame_15.setObjectName(u"frame_15")
        self.frame_15.setMinimumSize(QSize(0, 0))
        self.frame_15.setMaximumSize(QSize(16777215, 16777215))
        self.frame_15.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_14 = QHBoxLayout(self.frame_15)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.frame_16 = QFrame(self.frame_15)
        self.frame_16.setObjectName(u"frame_16")
        self.frame_16.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_16 = QHBoxLayout(self.frame_16)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.label_22 = QLabel(self.frame_16)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setFont(font2)

        self.horizontalLayout_16.addWidget(self.label_22)

        self.password_text = QLineEdit(self.frame_16)
        self.password_text.setObjectName(u"password_text")
        self.password_text.setEchoMode(QLineEdit.Normal)

        self.horizontalLayout_16.addWidget(self.password_text)


        self.horizontalLayout_14.addWidget(self.frame_16)

        self.frame_17 = QFrame(self.frame_15)
        self.frame_17.setObjectName(u"frame_17")
        self.frame_17.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_18 = QHBoxLayout(self.frame_17)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.label_24 = QLabel(self.frame_17)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setFont(font2)

        self.horizontalLayout_18.addWidget(self.label_24)

        self.passwordconfirm_text = QLineEdit(self.frame_17)
        self.passwordconfirm_text.setObjectName(u"passwordconfirm_text")
        self.passwordconfirm_text.setEchoMode(QLineEdit.Normal)

        self.horizontalLayout_18.addWidget(self.passwordconfirm_text)


        self.horizontalLayout_14.addWidget(self.frame_17)


        self.verticalLayout_20.addWidget(self.frame_15)

        self.add_user = QPushButton(self.frame_11)
        self.add_user.setObjectName(u"add_user")
        self.add_user.setFont(font2)

        self.verticalLayout_20.addWidget(self.add_user)


        self.verticalLayout_19.addWidget(self.frame_11)

        self.stackedWidget.addWidget(self.Local_accounts)
        self.Power = QWidget()
        self.Power.setObjectName(u"Power")
        self.verticalLayout_39 = QVBoxLayout(self.Power)
        self.verticalLayout_39.setObjectName(u"verticalLayout_39")
        self.label_39 = QLabel(self.Power)
        self.label_39.setObjectName(u"label_39")
        font4 = QFont()
        font4.setFamily(u"ROG Fonts")
        font4.setPointSize(12)
        font4.setBold(True)
        font4.setWeight(75)
        self.label_39.setFont(font4)

        self.verticalLayout_39.addWidget(self.label_39)

        self.Battery = QFrame(self.Power)
        self.Battery.setObjectName(u"Battery")
        sizePolicy1.setHeightForWidth(self.Battery.sizePolicy().hasHeightForWidth())
        self.Battery.setSizePolicy(sizePolicy1)
        self.Battery.setFrameShape(QFrame.NoFrame)
        self.gridLayout_4 = QGridLayout(self.Battery)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_25 = QLabel(self.Battery)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setFont(font2)

        self.gridLayout_4.addWidget(self.label_25, 0, 0, 1, 1)

        self.label_27 = QLabel(self.Battery)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setFont(font2)

        self.gridLayout_4.addWidget(self.label_27, 2, 0, 1, 1)

        self.label_26 = QLabel(self.Battery)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setFont(font2)

        self.gridLayout_4.addWidget(self.label_26, 1, 0, 1, 1)

        self.battery_status = QLabel(self.Battery)
        self.battery_status.setObjectName(u"battery_status")
        self.battery_status.setFont(font2)

        self.gridLayout_4.addWidget(self.battery_status, 0, 1, 1, 1)

        self.battery_plugged = QLabel(self.Battery)
        self.battery_plugged.setObjectName(u"battery_plugged")
        self.battery_plugged.setFont(font2)

        self.gridLayout_4.addWidget(self.battery_plugged, 3, 1, 1, 1)

        self.label_37 = QLabel(self.Battery)
        self.label_37.setObjectName(u"label_37")
        self.label_37.setFont(font2)

        self.gridLayout_4.addWidget(self.label_37, 3, 0, 1, 1)

        self.battery_time_left = QLabel(self.Battery)
        self.battery_time_left.setObjectName(u"battery_time_left")
        self.battery_time_left.setFont(font2)

        self.gridLayout_4.addWidget(self.battery_time_left, 2, 1, 1, 1)

        self.battery_charge = QLabel(self.Battery)
        self.battery_charge.setObjectName(u"battery_charge")
        self.battery_charge.setFont(font2)

        self.gridLayout_4.addWidget(self.battery_charge, 1, 1, 1, 1)

        self.battery_usage = roundProgressBar(self.Battery)
        self.battery_usage.setObjectName(u"battery_usage")

        self.gridLayout_4.addWidget(self.battery_usage, 0, 2, 4, 1)


        self.verticalLayout_39.addWidget(self.Battery)

        self.Consumed = QFrame(self.Power)
        self.Consumed.setObjectName(u"Consumed")
        sizePolicy1.setHeightForWidth(self.Consumed.sizePolicy().hasHeightForWidth())
        self.Consumed.setSizePolicy(sizePolicy1)
        self.Consumed.setFrameShape(QFrame.NoFrame)
        self.gridLayout_5 = QGridLayout(self.Consumed)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.label_32 = QLabel(self.Consumed)
        self.label_32.setObjectName(u"label_32")
        self.label_32.setFont(font2)

        self.gridLayout_5.addWidget(self.label_32, 2, 0, 1, 1)

        self.cpu_consume = QLabel(self.Consumed)
        self.cpu_consume.setObjectName(u"cpu_consume")
        self.cpu_consume.setFont(font2)

        self.gridLayout_5.addWidget(self.cpu_consume, 2, 1, 1, 1)

        self.igpu_consume = QLabel(self.Consumed)
        self.igpu_consume.setObjectName(u"igpu_consume")
        self.igpu_consume.setFont(font2)

        self.gridLayout_5.addWidget(self.igpu_consume, 1, 1, 1, 1)

        self.label_33 = QLabel(self.Consumed)
        self.label_33.setObjectName(u"label_33")
        self.label_33.setFont(font2)

        self.gridLayout_5.addWidget(self.label_33, 3, 0, 1, 1)

        self.gpu_consume = QLabel(self.Consumed)
        self.gpu_consume.setObjectName(u"gpu_consume")
        self.gpu_consume.setFont(font2)

        self.gridLayout_5.addWidget(self.gpu_consume, 0, 1, 1, 1)

        self.power_progress = spiralProgressBar(self.Consumed)
        self.power_progress.setObjectName(u"power_progress")

        self.gridLayout_5.addWidget(self.power_progress, 0, 2, 4, 1)

        self.label_31 = QLabel(self.Consumed)
        self.label_31.setObjectName(u"label_31")
        self.label_31.setFont(font2)

        self.gridLayout_5.addWidget(self.label_31, 0, 0, 1, 1)

        self.avg_consumed = QLabel(self.Consumed)
        self.avg_consumed.setObjectName(u"avg_consumed")
        self.avg_consumed.setFont(font2)

        self.gridLayout_5.addWidget(self.avg_consumed, 3, 1, 1, 1)

        self.label_40 = QLabel(self.Consumed)
        self.label_40.setObjectName(u"label_40")
        self.label_40.setFont(font2)

        self.gridLayout_5.addWidget(self.label_40, 1, 0, 1, 1)


        self.verticalLayout_39.addWidget(self.Consumed)

        self.frame_39 = QFrame(self.Power)
        self.frame_39.setObjectName(u"frame_39")
        self.frame_39.setFrameShape(QFrame.StyledPanel)
        self.frame_39.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_39)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.frame_38 = QFrame(self.frame_39)
        self.frame_38.setObjectName(u"frame_38")
        self.frame_38.setFrameShape(QFrame.StyledPanel)
        self.frame_38.setFrameShadow(QFrame.Raised)
        self.gridLayout_12 = QGridLayout(self.frame_38)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.interval_avg = QComboBox(self.frame_38)
        self.interval_avg.addItem("")
        self.interval_avg.addItem("")
        self.interval_avg.addItem("")
        self.interval_avg.setObjectName(u"interval_avg")
        self.interval_avg.setMinimumSize(QSize(0, 20))
        self.interval_avg.setMaximumSize(QSize(16777215, 20))
        self.interval_avg.setFont(font2)

        self.gridLayout_12.addWidget(self.interval_avg, 1, 1, 1, 1)

        self.update_int = QComboBox(self.frame_38)
        self.update_int.addItem("")
        self.update_int.addItem("")
        self.update_int.addItem("")
        self.update_int.addItem("")
        self.update_int.addItem("")
        self.update_int.addItem("")
        self.update_int.setObjectName(u"update_int")
        self.update_int.setMinimumSize(QSize(0, 20))
        self.update_int.setMaximumSize(QSize(16777215, 100))
        self.update_int.setFont(font2)

        self.gridLayout_12.addWidget(self.update_int, 0, 1, 1, 1)

        self.label_69 = QLabel(self.frame_38)
        self.label_69.setObjectName(u"label_69")
        self.label_69.setFont(font2)

        self.gridLayout_12.addWidget(self.label_69, 0, 0, 1, 1)

        self.label_70 = QLabel(self.frame_38)
        self.label_70.setObjectName(u"label_70")
        self.label_70.setFont(font2)

        self.gridLayout_12.addWidget(self.label_70, 1, 0, 1, 1)


        self.verticalLayout_3.addWidget(self.frame_38)

        self.intervals = QLabel(self.frame_39)
        self.intervals.setObjectName(u"intervals")
        self.intervals.setFont(font2)

        self.verticalLayout_3.addWidget(self.intervals, 0, Qt.AlignHCenter)


        self.verticalLayout_39.addWidget(self.frame_39)

        self.stackedWidget.addWidget(self.Power)
        self.storage = QWidget()
        self.storage.setObjectName(u"storage")
        self.verticalLayout_9 = QVBoxLayout(self.storage)
        self.verticalLayout_9.setSpacing(10)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.label_57 = QLabel(self.storage)
        self.label_57.setObjectName(u"label_57")
        font5 = QFont()
        font5.setFamily(u"Asus Rog")
        font5.setPointSize(12)
        font5.setBold(False)
        font5.setWeight(50)
        self.label_57.setFont(font5)

        self.verticalLayout_9.addWidget(self.label_57)

        self.storageTable = QTableWidget(self.storage)
        if (self.storageTable.columnCount() < 10):
            self.storageTable.setColumnCount(10)
        __qtablewidgetitem12 = QTableWidgetItem()
        __qtablewidgetitem12.setFont(font2);
        self.storageTable.setHorizontalHeaderItem(0, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        __qtablewidgetitem13.setFont(font2);
        self.storageTable.setHorizontalHeaderItem(1, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        __qtablewidgetitem14.setFont(font2);
        self.storageTable.setHorizontalHeaderItem(2, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        __qtablewidgetitem15.setFont(font2);
        self.storageTable.setHorizontalHeaderItem(3, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        __qtablewidgetitem16.setFont(font2);
        self.storageTable.setHorizontalHeaderItem(4, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        __qtablewidgetitem17.setFont(font2);
        self.storageTable.setHorizontalHeaderItem(5, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        __qtablewidgetitem18.setFont(font2);
        self.storageTable.setHorizontalHeaderItem(6, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        __qtablewidgetitem19.setFont(font2);
        self.storageTable.setHorizontalHeaderItem(7, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        __qtablewidgetitem20.setFont(font2);
        self.storageTable.setHorizontalHeaderItem(8, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        self.storageTable.setHorizontalHeaderItem(9, __qtablewidgetitem21)
        self.storageTable.setObjectName(u"storageTable")
        self.storageTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.verticalLayout_9.addWidget(self.storageTable)

        self.stackedWidget.addWidget(self.storage)
        self.activities = QWidget()
        self.activities.setObjectName(u"activities")
        self.verticalLayout_4 = QVBoxLayout(self.activities)
        self.verticalLayout_4.setSpacing(10)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.frame_2 = QFrame(self.activities)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_11 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_11.setSpacing(0)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(0, 10, 0, 0)
        self.label_56 = QLabel(self.frame_2)
        self.label_56.setObjectName(u"label_56")
        font6 = QFont()
        font6.setFamily(u"Asus Rog")
        font6.setPointSize(12)
        font6.setBold(True)
        font6.setWeight(75)
        self.label_56.setFont(font6)

        self.horizontalLayout_11.addWidget(self.label_56)

        self.frame_5 = QFrame(self.frame_2)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_12 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_12.setSpacing(0)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.activity_search = QLineEdit(self.frame_5)
        self.activity_search.setObjectName(u"activity_search")
        self.activity_search.setMinimumSize(QSize(200, 0))
        self.activity_search.setFont(font3)

        self.horizontalLayout_12.addWidget(self.activity_search)

        self.pushButton_11 = QPushButton(self.frame_5)
        self.pushButton_11.setObjectName(u"pushButton_11")
        icon16 = QIcon()
        icon16.addFile(u":/feather/icons/feather/search.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_11.setIcon(icon16)

        self.horizontalLayout_12.addWidget(self.pushButton_11)


        self.horizontalLayout_11.addWidget(self.frame_5)


        self.verticalLayout_4.addWidget(self.frame_2)

        self.frame_3 = QFrame(self.activities)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.verticalLayout_7 = QVBoxLayout(self.frame_3)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 10, 0, 0)
        self.tableWidget = QTableWidget(self.frame_3)
        if (self.tableWidget.columnCount() < 8):
            self.tableWidget.setColumnCount(8)
        __qtablewidgetitem22 = QTableWidgetItem()
        __qtablewidgetitem22.setFont(font2);
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem22)
        __qtablewidgetitem23 = QTableWidgetItem()
        __qtablewidgetitem23.setFont(font2);
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem23)
        __qtablewidgetitem24 = QTableWidgetItem()
        __qtablewidgetitem24.setFont(font2);
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem24)
        __qtablewidgetitem25 = QTableWidgetItem()
        __qtablewidgetitem25.setFont(font2);
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem25)
        __qtablewidgetitem26 = QTableWidgetItem()
        __qtablewidgetitem26.setFont(font2);
        self.tableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem26)
        __qtablewidgetitem27 = QTableWidgetItem()
        __qtablewidgetitem27.setFont(font2);
        self.tableWidget.setHorizontalHeaderItem(5, __qtablewidgetitem27)
        __qtablewidgetitem28 = QTableWidgetItem()
        __qtablewidgetitem28.setFont(font2);
        self.tableWidget.setHorizontalHeaderItem(6, __qtablewidgetitem28)
        __qtablewidgetitem29 = QTableWidgetItem()
        __qtablewidgetitem29.setFont(font2);
        self.tableWidget.setHorizontalHeaderItem(7, __qtablewidgetitem29)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setFont(font3)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.verticalLayout_7.addWidget(self.tableWidget)


        self.verticalLayout_4.addWidget(self.frame_3)

        self.frame_4 = QFrame(self.activities)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_13 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_13.setSpacing(0)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(0, 10, 0, 0)
        self.pushButton_12 = QPushButton(self.frame_4)
        self.pushButton_12.setObjectName(u"pushButton_12")
        self.pushButton_12.setFont(font2)

        self.horizontalLayout_13.addWidget(self.pushButton_12)

        self.pushButton_13 = QPushButton(self.frame_4)
        self.pushButton_13.setObjectName(u"pushButton_13")
        self.pushButton_13.setFont(font2)

        self.horizontalLayout_13.addWidget(self.pushButton_13)

        self.pushButton_14 = QPushButton(self.frame_4)
        self.pushButton_14.setObjectName(u"pushButton_14")
        self.pushButton_14.setFont(font2)

        self.horizontalLayout_13.addWidget(self.pushButton_14)

        self.pushButton_15 = QPushButton(self.frame_4)
        self.pushButton_15.setObjectName(u"pushButton_15")
        self.pushButton_15.setFont(font2)

        self.horizontalLayout_13.addWidget(self.pushButton_15)


        self.verticalLayout_4.addWidget(self.frame_4)

        self.stackedWidget.addWidget(self.activities)
        self.sensors = QWidget()
        self.sensors.setObjectName(u"sensors")
        self.verticalLayout_8 = QVBoxLayout(self.sensors)
        self.verticalLayout_8.setSpacing(10)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.title_sensor = QLabel(self.sensors)
        self.title_sensor.setObjectName(u"title_sensor")
        self.title_sensor.setFont(font6)

        self.verticalLayout_8.addWidget(self.title_sensor)

        self.sensors_table = QTableWidget(self.sensors)
        if (self.sensors_table.columnCount() < 5):
            self.sensors_table.setColumnCount(5)
        __qtablewidgetitem30 = QTableWidgetItem()
        __qtablewidgetitem30.setFont(font2);
        self.sensors_table.setHorizontalHeaderItem(0, __qtablewidgetitem30)
        __qtablewidgetitem31 = QTableWidgetItem()
        __qtablewidgetitem31.setFont(font2);
        self.sensors_table.setHorizontalHeaderItem(1, __qtablewidgetitem31)
        __qtablewidgetitem32 = QTableWidgetItem()
        __qtablewidgetitem32.setFont(font2);
        self.sensors_table.setHorizontalHeaderItem(2, __qtablewidgetitem32)
        __qtablewidgetitem33 = QTableWidgetItem()
        __qtablewidgetitem33.setFont(font2);
        self.sensors_table.setHorizontalHeaderItem(3, __qtablewidgetitem33)
        __qtablewidgetitem34 = QTableWidgetItem()
        __qtablewidgetitem34.setFont(font2);
        self.sensors_table.setHorizontalHeaderItem(4, __qtablewidgetitem34)
        self.sensors_table.setObjectName(u"sensors_table")
        self.sensors_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.verticalLayout_8.addWidget(self.sensors_table)

        self.stackedWidget.addWidget(self.sensors)
        self.network = QWidget()
        self.network.setObjectName(u"network")
        self.verticalLayout_12 = QVBoxLayout(self.network)
        self.verticalLayout_12.setSpacing(10)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.scrollArea = QScrollArea(self.network)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 655, 1076))
        self.verticalLayout_11 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_11.setSpacing(20)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 100)
        self.frame_6 = QFrame(self.scrollAreaWidgetContents)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.NoFrame)
        self.verticalLayout_13 = QVBoxLayout(self.frame_6)
        self.verticalLayout_13.setSpacing(10)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.label_60 = QLabel(self.frame_6)
        self.label_60.setObjectName(u"label_60")
        self.label_60.setFont(font1)

        self.verticalLayout_13.addWidget(self.label_60)

        self.stats_table = QTableWidget(self.frame_6)
        if (self.stats_table.columnCount() < 5):
            self.stats_table.setColumnCount(5)
        __qtablewidgetitem35 = QTableWidgetItem()
        self.stats_table.setHorizontalHeaderItem(0, __qtablewidgetitem35)
        __qtablewidgetitem36 = QTableWidgetItem()
        __qtablewidgetitem36.setFont(font2);
        self.stats_table.setHorizontalHeaderItem(1, __qtablewidgetitem36)
        __qtablewidgetitem37 = QTableWidgetItem()
        __qtablewidgetitem37.setFont(font2);
        self.stats_table.setHorizontalHeaderItem(2, __qtablewidgetitem37)
        __qtablewidgetitem38 = QTableWidgetItem()
        __qtablewidgetitem38.setFont(font2);
        self.stats_table.setHorizontalHeaderItem(3, __qtablewidgetitem38)
        __qtablewidgetitem39 = QTableWidgetItem()
        __qtablewidgetitem39.setFont(font2);
        self.stats_table.setHorizontalHeaderItem(4, __qtablewidgetitem39)
        self.stats_table.setObjectName(u"stats_table")
        self.stats_table.setMinimumSize(QSize(0, 200))
        self.stats_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.verticalLayout_13.addWidget(self.stats_table)


        self.verticalLayout_11.addWidget(self.frame_6)

        self.frame_7 = QFrame(self.scrollAreaWidgetContents)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.NoFrame)
        self.verticalLayout_14 = QVBoxLayout(self.frame_7)
        self.verticalLayout_14.setSpacing(10)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.label_61 = QLabel(self.frame_7)
        self.label_61.setObjectName(u"label_61")
        self.label_61.setFont(font1)

        self.verticalLayout_14.addWidget(self.label_61)

        self.IO_counters_table = QTableWidget(self.frame_7)
        if (self.IO_counters_table.columnCount() < 9):
            self.IO_counters_table.setColumnCount(9)
        __qtablewidgetitem40 = QTableWidgetItem()
        __qtablewidgetitem40.setFont(font2);
        self.IO_counters_table.setHorizontalHeaderItem(0, __qtablewidgetitem40)
        __qtablewidgetitem41 = QTableWidgetItem()
        __qtablewidgetitem41.setFont(font2);
        self.IO_counters_table.setHorizontalHeaderItem(1, __qtablewidgetitem41)
        __qtablewidgetitem42 = QTableWidgetItem()
        __qtablewidgetitem42.setFont(font2);
        self.IO_counters_table.setHorizontalHeaderItem(2, __qtablewidgetitem42)
        __qtablewidgetitem43 = QTableWidgetItem()
        __qtablewidgetitem43.setFont(font2);
        self.IO_counters_table.setHorizontalHeaderItem(3, __qtablewidgetitem43)
        __qtablewidgetitem44 = QTableWidgetItem()
        __qtablewidgetitem44.setFont(font2);
        self.IO_counters_table.setHorizontalHeaderItem(4, __qtablewidgetitem44)
        __qtablewidgetitem45 = QTableWidgetItem()
        __qtablewidgetitem45.setFont(font2);
        self.IO_counters_table.setHorizontalHeaderItem(5, __qtablewidgetitem45)
        __qtablewidgetitem46 = QTableWidgetItem()
        __qtablewidgetitem46.setFont(font2);
        self.IO_counters_table.setHorizontalHeaderItem(6, __qtablewidgetitem46)
        __qtablewidgetitem47 = QTableWidgetItem()
        __qtablewidgetitem47.setFont(font2);
        self.IO_counters_table.setHorizontalHeaderItem(7, __qtablewidgetitem47)
        __qtablewidgetitem48 = QTableWidgetItem()
        __qtablewidgetitem48.setFont(font2);
        self.IO_counters_table.setHorizontalHeaderItem(8, __qtablewidgetitem48)
        self.IO_counters_table.setObjectName(u"IO_counters_table")
        self.IO_counters_table.setMinimumSize(QSize(0, 200))
        self.IO_counters_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.verticalLayout_14.addWidget(self.IO_counters_table)


        self.verticalLayout_11.addWidget(self.frame_7)

        self.frame_8 = QFrame(self.scrollAreaWidgetContents)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setFrameShape(QFrame.NoFrame)
        self.verticalLayout_15 = QVBoxLayout(self.frame_8)
        self.verticalLayout_15.setSpacing(10)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.label_62 = QLabel(self.frame_8)
        self.label_62.setObjectName(u"label_62")
        self.label_62.setFont(font1)

        self.verticalLayout_15.addWidget(self.label_62)

        self.addresses_table = QTableWidget(self.frame_8)
        if (self.addresses_table.columnCount() < 6):
            self.addresses_table.setColumnCount(6)
        __qtablewidgetitem49 = QTableWidgetItem()
        __qtablewidgetitem49.setFont(font2);
        self.addresses_table.setHorizontalHeaderItem(0, __qtablewidgetitem49)
        __qtablewidgetitem50 = QTableWidgetItem()
        __qtablewidgetitem50.setFont(font2);
        self.addresses_table.setHorizontalHeaderItem(1, __qtablewidgetitem50)
        __qtablewidgetitem51 = QTableWidgetItem()
        __qtablewidgetitem51.setFont(font2);
        self.addresses_table.setHorizontalHeaderItem(2, __qtablewidgetitem51)
        __qtablewidgetitem52 = QTableWidgetItem()
        __qtablewidgetitem52.setFont(font2);
        self.addresses_table.setHorizontalHeaderItem(3, __qtablewidgetitem52)
        __qtablewidgetitem53 = QTableWidgetItem()
        __qtablewidgetitem53.setFont(font2);
        self.addresses_table.setHorizontalHeaderItem(4, __qtablewidgetitem53)
        __qtablewidgetitem54 = QTableWidgetItem()
        __qtablewidgetitem54.setFont(font2);
        self.addresses_table.setHorizontalHeaderItem(5, __qtablewidgetitem54)
        self.addresses_table.setObjectName(u"addresses_table")
        self.addresses_table.setMinimumSize(QSize(0, 200))
        self.addresses_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.verticalLayout_15.addWidget(self.addresses_table)


        self.verticalLayout_11.addWidget(self.frame_8)

        self.frame_9 = QFrame(self.scrollAreaWidgetContents)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setFrameShape(QFrame.NoFrame)
        self.verticalLayout_16 = QVBoxLayout(self.frame_9)
        self.verticalLayout_16.setSpacing(10)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.verticalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.label_63 = QLabel(self.frame_9)
        self.label_63.setObjectName(u"label_63")
        self.label_63.setFont(font6)

        self.verticalLayout_16.addWidget(self.label_63)

        self.connections_table = QTableWidget(self.frame_9)
        if (self.connections_table.columnCount() < 7):
            self.connections_table.setColumnCount(7)
        __qtablewidgetitem55 = QTableWidgetItem()
        __qtablewidgetitem55.setFont(font3);
        self.connections_table.setHorizontalHeaderItem(0, __qtablewidgetitem55)
        __qtablewidgetitem56 = QTableWidgetItem()
        __qtablewidgetitem56.setFont(font3);
        self.connections_table.setHorizontalHeaderItem(1, __qtablewidgetitem56)
        __qtablewidgetitem57 = QTableWidgetItem()
        __qtablewidgetitem57.setFont(font3);
        self.connections_table.setHorizontalHeaderItem(2, __qtablewidgetitem57)
        __qtablewidgetitem58 = QTableWidgetItem()
        __qtablewidgetitem58.setFont(font3);
        self.connections_table.setHorizontalHeaderItem(3, __qtablewidgetitem58)
        __qtablewidgetitem59 = QTableWidgetItem()
        __qtablewidgetitem59.setFont(font3);
        self.connections_table.setHorizontalHeaderItem(4, __qtablewidgetitem59)
        __qtablewidgetitem60 = QTableWidgetItem()
        __qtablewidgetitem60.setFont(font3);
        self.connections_table.setHorizontalHeaderItem(5, __qtablewidgetitem60)
        __qtablewidgetitem61 = QTableWidgetItem()
        __qtablewidgetitem61.setFont(font3);
        self.connections_table.setHorizontalHeaderItem(6, __qtablewidgetitem61)
        self.connections_table.setObjectName(u"connections_table")
        self.connections_table.setMinimumSize(QSize(0, 200))
        self.connections_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.verticalLayout_16.addWidget(self.connections_table)


        self.verticalLayout_11.addWidget(self.frame_9)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_12.addWidget(self.scrollArea)

        self.stackedWidget.addWidget(self.network)
        self.sysinfo = QWidget()
        self.sysinfo.setObjectName(u"sysinfo")
        self.verticalLayout_10 = QVBoxLayout(self.sysinfo)
        self.verticalLayout_10.setSpacing(10)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.sysinfo)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.NoFrame)
        self.gridLayout_6 = QGridLayout(self.frame)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.label_52 = QLabel(self.frame)
        self.label_52.setObjectName(u"label_52")
        self.label_52.setFont(font2)

        self.gridLayout_6.addWidget(self.label_52, 4, 3, 1, 1)

        self.label_45 = QLabel(self.frame)
        self.label_45.setObjectName(u"label_45")
        self.label_45.setFont(font2)

        self.gridLayout_6.addWidget(self.label_45, 3, 0, 1, 1)

        self.label_47 = QLabel(self.frame)
        self.label_47.setObjectName(u"label_47")
        self.label_47.setFont(font2)

        self.gridLayout_6.addWidget(self.label_47, 4, 0, 1, 1)

        self.system_time = QLabel(self.frame)
        self.system_time.setObjectName(u"system_time")
        self.system_time.setFont(font2)

        self.gridLayout_6.addWidget(self.system_time, 4, 2, 1, 1)

        self.label_42 = QLabel(self.frame)
        self.label_42.setObjectName(u"label_42")
        self.label_42.setFont(font4)

        self.gridLayout_6.addWidget(self.label_42, 0, 0, 1, 1)

        self.system_platform = QLabel(self.frame)
        self.system_platform.setObjectName(u"system_platform")
        self.system_platform.setFont(font2)

        self.gridLayout_6.addWidget(self.system_platform, 2, 2, 1, 1)

        self.system_system = QLabel(self.frame)
        self.system_system.setObjectName(u"system_system")
        self.system_system.setFont(font2)

        self.gridLayout_6.addWidget(self.system_system, 1, 0, 1, 1)

        self.system_machine = QLabel(self.frame)
        self.system_machine.setObjectName(u"system_machine")
        self.system_machine.setFont(font2)

        self.gridLayout_6.addWidget(self.system_machine, 3, 4, 1, 1)

        self.system_version = QLabel(self.frame)
        self.system_version.setObjectName(u"system_version")
        self.system_version.setFont(font2)

        self.gridLayout_6.addWidget(self.system_version, 3, 2, 1, 1)

        self.label_50 = QLabel(self.frame)
        self.label_50.setObjectName(u"label_50")
        self.label_50.setFont(font2)

        self.gridLayout_6.addWidget(self.label_50, 2, 3, 1, 1)

        self.system_date = QLabel(self.frame)
        self.system_date.setObjectName(u"system_date")
        self.system_date.setFont(font2)

        self.gridLayout_6.addWidget(self.system_date, 4, 4, 1, 1)

        self.label_44 = QLabel(self.frame)
        self.label_44.setObjectName(u"label_44")
        self.label_44.setFont(font2)

        self.gridLayout_6.addWidget(self.label_44, 2, 0, 1, 1)

        self.system_processor = QLabel(self.frame)
        self.system_processor.setObjectName(u"system_processor")
        self.system_processor.setFont(font2)

        self.gridLayout_6.addWidget(self.system_processor, 2, 4, 1, 1)

        self.label_51 = QLabel(self.frame)
        self.label_51.setObjectName(u"label_51")
        self.label_51.setFont(font2)

        self.gridLayout_6.addWidget(self.label_51, 3, 3, 1, 1)

        self.get_hardware_info = QPushButton(self.frame)
        self.get_hardware_info.setObjectName(u"get_hardware_info")
        self.get_hardware_info.setFont(font2)

        self.gridLayout_6.addWidget(self.get_hardware_info, 1, 3, 1, 2)


        self.verticalLayout_10.addWidget(self.frame)

        self.stackedWidget.addWidget(self.sysinfo)
        self.Domain_tab = QWidget()
        self.Domain_tab.setObjectName(u"Domain_tab")
        self.verticalLayout_5 = QVBoxLayout(self.Domain_tab)
        self.verticalLayout_5.setSpacing(10)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.frame_21 = QFrame(self.Domain_tab)
        self.frame_21.setObjectName(u"frame_21")
        self.frame_21.setFrameShape(QFrame.NoFrame)
        self.verticalLayout_24 = QVBoxLayout(self.frame_21)
        self.verticalLayout_24.setObjectName(u"verticalLayout_24")
        self.frame_23 = QFrame(self.frame_21)
        self.frame_23.setObjectName(u"frame_23")
        self.frame_23.setMinimumSize(QSize(500, 0))
        self.frame_23.setFrameShape(QFrame.NoFrame)
        self.verticalLayout_26 = QVBoxLayout(self.frame_23)
        self.verticalLayout_26.setObjectName(u"verticalLayout_26")
        self.gridLayout_7 = QGridLayout()
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.status_domain = QLabel(self.frame_23)
        self.status_domain.setObjectName(u"status_domain")
        self.status_domain.setMaximumSize(QSize(16777215, 16777215))
        self.status_domain.setFont(font2)

        self.gridLayout_7.addWidget(self.status_domain, 0, 1, 1, 1)

        self.name_domain = QLabel(self.frame_23)
        self.name_domain.setObjectName(u"name_domain")
        self.name_domain.setFont(font2)

        self.gridLayout_7.addWidget(self.name_domain, 1, 1, 1, 1)

        self.label_35 = QLabel(self.frame_23)
        self.label_35.setObjectName(u"label_35")
        self.label_35.setMaximumSize(QSize(150, 16777215))
        self.label_35.setFont(font2)

        self.gridLayout_7.addWidget(self.label_35, 0, 0, 1, 1)

        self.label_38 = QLabel(self.frame_23)
        self.label_38.setObjectName(u"label_38")
        self.label_38.setFont(font2)

        self.gridLayout_7.addWidget(self.label_38, 1, 0, 1, 1)


        self.verticalLayout_26.addLayout(self.gridLayout_7)


        self.verticalLayout_24.addWidget(self.frame_23)

        self.label_36 = QLabel(self.frame_21)
        self.label_36.setObjectName(u"label_36")
        self.label_36.setMinimumSize(QSize(0, 30))
        self.label_36.setMaximumSize(QSize(16777215, 30))
        self.label_36.setFont(font2)

        self.verticalLayout_24.addWidget(self.label_36)

        self.frame_22 = QFrame(self.frame_21)
        self.frame_22.setObjectName(u"frame_22")
        self.frame_22.setMinimumSize(QSize(0, 200))
        self.frame_22.setMaximumSize(QSize(550, 200))
        self.frame_22.setFrameShape(QFrame.NoFrame)
        self.verticalLayout_25 = QVBoxLayout(self.frame_22)
        self.verticalLayout_25.setObjectName(u"verticalLayout_25")
        self.gridLayout_8 = QGridLayout()
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.label_29 = QLabel(self.frame_22)
        self.label_29.setObjectName(u"label_29")
        self.label_29.setMaximumSize(QSize(16777215, 40))
        self.label_29.setFont(font2)

        self.gridLayout_8.addWidget(self.label_29, 1, 0, 1, 1, Qt.AlignLeft)

        self.frame_24 = QFrame(self.frame_22)
        self.frame_24.setObjectName(u"frame_24")
        self.frame_24.setMinimumSize(QSize(0, 10))
        self.frame_24.setFrameShape(QFrame.NoFrame)
        self.verticalLayout_28 = QVBoxLayout(self.frame_24)
        self.verticalLayout_28.setSpacing(0)
        self.verticalLayout_28.setObjectName(u"verticalLayout_28")
        self.verticalLayout_28.setContentsMargins(0, 0, 0, 0)
        self.label_28 = QLabel(self.frame_24)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setFont(font2)

        self.verticalLayout_28.addWidget(self.label_28, 0, Qt.AlignLeft)


        self.gridLayout_8.addWidget(self.frame_24, 0, 0, 1, 1)

        self.domain_text = QLineEdit(self.frame_22)
        self.domain_text.setObjectName(u"domain_text")
        self.domain_text.setMinimumSize(QSize(250, 0))
        self.domain_text.setMaximumSize(QSize(250, 16777215))

        self.gridLayout_8.addWidget(self.domain_text, 0, 1, 1, 1, Qt.AlignLeft)

        self.label_30 = QLabel(self.frame_22)
        self.label_30.setObjectName(u"label_30")
        self.label_30.setMaximumSize(QSize(16777215, 40))
        self.label_30.setFont(font2)

        self.gridLayout_8.addWidget(self.label_30, 2, 0, 1, 1, Qt.AlignLeft)

        self.pass_text = QLineEdit(self.frame_22)
        self.pass_text.setObjectName(u"pass_text")
        self.pass_text.setMinimumSize(QSize(250, 0))
        self.pass_text.setMaximumSize(QSize(250, 16777215))
        self.pass_text.setEchoMode(QLineEdit.Password)

        self.gridLayout_8.addWidget(self.pass_text, 2, 1, 1, 1, Qt.AlignLeft)

        self.acc_text = QLineEdit(self.frame_22)
        self.acc_text.setObjectName(u"acc_text")
        self.acc_text.setMinimumSize(QSize(250, 0))
        self.acc_text.setMaximumSize(QSize(250, 16777215))

        self.gridLayout_8.addWidget(self.acc_text, 1, 1, 1, 1, Qt.AlignLeft)


        self.verticalLayout_25.addLayout(self.gridLayout_8)


        self.verticalLayout_24.addWidget(self.frame_22)

        self.frame_29 = QFrame(self.frame_21)
        self.frame_29.setObjectName(u"frame_29")
        self.frame_29.setMinimumSize(QSize(0, 70))
        self.frame_29.setMaximumSize(QSize(16777215, 70))
        self.frame_29.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_24 = QHBoxLayout(self.frame_29)
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.frame_27 = QFrame(self.frame_29)
        self.frame_27.setObjectName(u"frame_27")
        self.frame_27.setMinimumSize(QSize(0, 70))
        self.frame_27.setMaximumSize(QSize(200, 70))
        self.frame_27.setFrameShape(QFrame.NoFrame)
        self.verticalLayout_27 = QVBoxLayout(self.frame_27)
        self.verticalLayout_27.setObjectName(u"verticalLayout_27")
        self.add_domain = QPushButton(self.frame_27)
        self.add_domain.setObjectName(u"add_domain")
        self.add_domain.setMaximumSize(QSize(16777215, 16777215))
        self.add_domain.setFont(font2)

        self.verticalLayout_27.addWidget(self.add_domain)


        self.horizontalLayout_24.addWidget(self.frame_27)


        self.verticalLayout_24.addWidget(self.frame_29)


        self.verticalLayout_5.addWidget(self.frame_21)

        self.stackedWidget.addWidget(self.Domain_tab)
        self.DB_tab = QWidget()
        self.DB_tab.setObjectName(u"DB_tab")
        self.verticalLayout_35 = QVBoxLayout(self.DB_tab)
        self.verticalLayout_35.setObjectName(u"verticalLayout_35")
        self.frame_35 = QFrame(self.DB_tab)
        self.frame_35.setObjectName(u"frame_35")
        self.frame_35.setFrameShape(QFrame.StyledPanel)
        self.frame_35.setFrameShadow(QFrame.Raised)
        self.verticalLayout_38 = QVBoxLayout(self.frame_35)
        self.verticalLayout_38.setObjectName(u"verticalLayout_38")
        self.frame_40 = QFrame(self.frame_35)
        self.frame_40.setObjectName(u"frame_40")
        self.frame_40.setMaximumSize(QSize(16777215, 400))
        self.frame_40.setFrameShape(QFrame.StyledPanel)
        self.frame_40.setFrameShadow(QFrame.Raised)
        self.verticalLayout_37 = QVBoxLayout(self.frame_40)
        self.verticalLayout_37.setObjectName(u"verticalLayout_37")
        self.db_table = QTableWidget(self.frame_40)
        self.db_table.setObjectName(u"db_table")
        self.db_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.verticalLayout_37.addWidget(self.db_table)


        self.verticalLayout_38.addWidget(self.frame_40)

        self.frame_41 = QFrame(self.frame_35)
        self.frame_41.setObjectName(u"frame_41")
        self.frame_41.setFrameShape(QFrame.StyledPanel)
        self.frame_41.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_25 = QHBoxLayout(self.frame_41)
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.load_client = QPushButton(self.frame_41)
        self.load_client.setObjectName(u"load_client")
        self.load_client.setFont(font2)

        self.horizontalLayout_25.addWidget(self.load_client)

        self.load_locatii = QPushButton(self.frame_41)
        self.load_locatii.setObjectName(u"load_locatii")
        self.load_locatii.setFont(font2)

        self.horizontalLayout_25.addWidget(self.load_locatii)

        self.load_incaperi = QPushButton(self.frame_41)
        self.load_incaperi.setObjectName(u"load_incaperi")
        self.load_incaperi.setFont(font2)

        self.horizontalLayout_25.addWidget(self.load_incaperi)

        self.load_power = QPushButton(self.frame_41)
        self.load_power.setObjectName(u"load_power")
        self.load_power.setFont(font2)

        self.horizontalLayout_25.addWidget(self.load_power)

        self.load_hardware = QPushButton(self.frame_41)
        self.load_hardware.setObjectName(u"load_hardware")
        self.load_hardware.setFont(font2)

        self.horizontalLayout_25.addWidget(self.load_hardware)


        self.verticalLayout_38.addWidget(self.frame_41)

        self.frame_37 = QFrame(self.frame_35)
        self.frame_37.setObjectName(u"frame_37")
        self.frame_37.setFrameShape(QFrame.StyledPanel)
        self.frame_37.setFrameShadow(QFrame.Raised)
        self.gridLayout_11 = QGridLayout(self.frame_37)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.label_68 = QLabel(self.frame_37)
        self.label_68.setObjectName(u"label_68")
        self.label_68.setFont(font2)

        self.gridLayout_11.addWidget(self.label_68, 1, 0, 1, 1)

        self.label_67 = QLabel(self.frame_37)
        self.label_67.setObjectName(u"label_67")
        self.label_67.setFont(font2)

        self.gridLayout_11.addWidget(self.label_67, 0, 0, 1, 1)

        self.location_input = QLineEdit(self.frame_37)
        self.location_input.setObjectName(u"location_input")

        self.gridLayout_11.addWidget(self.location_input, 0, 1, 1, 1)

        self.room_input = QLineEdit(self.frame_37)
        self.room_input.setObjectName(u"room_input")

        self.gridLayout_11.addWidget(self.room_input, 1, 1, 1, 1)


        self.verticalLayout_38.addWidget(self.frame_37)

        self.frame_36 = QFrame(self.frame_35)
        self.frame_36.setObjectName(u"frame_36")
        self.frame_36.setMaximumSize(QSize(16777215, 150))
        self.frame_36.setFrameShape(QFrame.StyledPanel)
        self.frame_36.setFrameShadow(QFrame.Raised)
        self.verticalLayout_36 = QVBoxLayout(self.frame_36)
        self.verticalLayout_36.setObjectName(u"verticalLayout_36")
        self.add_button = QPushButton(self.frame_36)
        self.add_button.setObjectName(u"add_button")
        self.add_button.setFont(font2)

        self.verticalLayout_36.addWidget(self.add_button)


        self.verticalLayout_38.addWidget(self.frame_36)


        self.verticalLayout_35.addWidget(self.frame_35)

        self.stackedWidget.addWidget(self.DB_tab)
        self.Programs_tab = QWidget()
        self.Programs_tab.setObjectName(u"Programs_tab")
        self.verticalLayout_29 = QVBoxLayout(self.Programs_tab)
        self.verticalLayout_29.setObjectName(u"verticalLayout_29")
        self.frame_31 = QFrame(self.Programs_tab)
        self.frame_31.setObjectName(u"frame_31")
        self.frame_31.setMaximumSize(QSize(16777215, 300))
        self.frame_31.setFrameShape(QFrame.StyledPanel)
        self.frame_31.setFrameShadow(QFrame.Raised)
        self.verticalLayout_31 = QVBoxLayout(self.frame_31)
        self.verticalLayout_31.setObjectName(u"verticalLayout_31")
        self.installed_table = QTableWidget(self.frame_31)
        if (self.installed_table.columnCount() < 4):
            self.installed_table.setColumnCount(4)
        __qtablewidgetitem62 = QTableWidgetItem()
        __qtablewidgetitem62.setFont(font2);
        self.installed_table.setHorizontalHeaderItem(0, __qtablewidgetitem62)
        __qtablewidgetitem63 = QTableWidgetItem()
        __qtablewidgetitem63.setFont(font2);
        self.installed_table.setHorizontalHeaderItem(1, __qtablewidgetitem63)
        __qtablewidgetitem64 = QTableWidgetItem()
        __qtablewidgetitem64.setFont(font2);
        self.installed_table.setHorizontalHeaderItem(2, __qtablewidgetitem64)
        __qtablewidgetitem65 = QTableWidgetItem()
        __qtablewidgetitem65.setFont(font2);
        self.installed_table.setHorizontalHeaderItem(3, __qtablewidgetitem65)
        self.installed_table.setObjectName(u"installed_table")
        self.installed_table.setContextMenuPolicy(Qt.CustomContextMenu)

        self.verticalLayout_31.addWidget(self.installed_table)


        self.verticalLayout_29.addWidget(self.frame_31)

        self.frame_32 = QFrame(self.Programs_tab)
        self.frame_32.setObjectName(u"frame_32")
        self.frame_32.setMaximumSize(QSize(16777215, 0))
        self.frame_32.setFrameShape(QFrame.StyledPanel)
        self.frame_32.setFrameShadow(QFrame.Raised)
        self.verticalLayout_30 = QVBoxLayout(self.frame_32)
        self.verticalLayout_30.setObjectName(u"verticalLayout_30")
        self.gridLayout_9 = QGridLayout()
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.label_53 = QLabel(self.frame_32)
        self.label_53.setObjectName(u"label_53")

        self.gridLayout_9.addWidget(self.label_53, 2, 0, 1, 1)

        self.label_58 = QLabel(self.frame_32)
        self.label_58.setObjectName(u"label_58")

        self.gridLayout_9.addWidget(self.label_58, 1, 0, 1, 1)

        self.label_55 = QLabel(self.frame_32)
        self.label_55.setObjectName(u"label_55")

        self.gridLayout_9.addWidget(self.label_55, 0, 0, 1, 1)

        self.label_64 = QLabel(self.frame_32)
        self.label_64.setObjectName(u"label_64")

        self.gridLayout_9.addWidget(self.label_64, 1, 1, 1, 1)

        self.label_54 = QLabel(self.frame_32)
        self.label_54.setObjectName(u"label_54")

        self.gridLayout_9.addWidget(self.label_54, 3, 0, 1, 1)

        self.label_59 = QLabel(self.frame_32)
        self.label_59.setObjectName(u"label_59")

        self.gridLayout_9.addWidget(self.label_59, 0, 1, 1, 1)


        self.verticalLayout_30.addLayout(self.gridLayout_9)


        self.verticalLayout_29.addWidget(self.frame_32)

        self.frame_30 = QFrame(self.Programs_tab)
        self.frame_30.setObjectName(u"frame_30")
        self.frame_30.setEnabled(False)
        self.frame_30.setFrameShape(QFrame.StyledPanel)
        self.frame_30.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_23 = QHBoxLayout(self.frame_30)
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.pushButton_2 = QPushButton(self.frame_30)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setMaximumSize(QSize(16777215, 0))
        self.pushButton_2.setFont(font2)

        self.horizontalLayout_23.addWidget(self.pushButton_2)

        self.pushButton_4 = QPushButton(self.frame_30)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setMaximumSize(QSize(16777215, 0))
        self.pushButton_4.setFont(font2)

        self.horizontalLayout_23.addWidget(self.pushButton_4)


        self.verticalLayout_29.addWidget(self.frame_30)

        self.stackedWidget.addWidget(self.Programs_tab)
        self.Updates_tab = QWidget()
        self.Updates_tab.setObjectName(u"Updates_tab")
        self.verticalLayout_32 = QVBoxLayout(self.Updates_tab)
        self.verticalLayout_32.setObjectName(u"verticalLayout_32")
        self.frame_33 = QFrame(self.Updates_tab)
        self.frame_33.setObjectName(u"frame_33")
        self.frame_33.setMaximumSize(QSize(16777215, 250))
        self.frame_33.setFrameShape(QFrame.StyledPanel)
        self.frame_33.setFrameShadow(QFrame.Raised)
        self.verticalLayout_34 = QVBoxLayout(self.frame_33)
        self.verticalLayout_34.setObjectName(u"verticalLayout_34")
        self.updates_table = QTableWidget(self.frame_33)
        self.updates_table.setObjectName(u"updates_table")

        self.verticalLayout_34.addWidget(self.updates_table)


        self.verticalLayout_32.addWidget(self.frame_33)

        self.frame_34 = QFrame(self.Updates_tab)
        self.frame_34.setObjectName(u"frame_34")
        self.frame_34.setFrameShape(QFrame.StyledPanel)
        self.frame_34.setFrameShadow(QFrame.Raised)
        self.verticalLayout_33 = QVBoxLayout(self.frame_34)
        self.verticalLayout_33.setObjectName(u"verticalLayout_33")
        self.label_65 = QLabel(self.frame_34)
        self.label_65.setObjectName(u"label_65")
        self.label_65.setMaximumSize(QSize(16777215, 50))
        self.label_65.setFont(font2)

        self.verticalLayout_33.addWidget(self.label_65)

        self.args = QLineEdit(self.frame_34)
        self.args.setObjectName(u"args")

        self.verticalLayout_33.addWidget(self.args)

        self.gridLayout_10 = QGridLayout()
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.hide = QPushButton(self.frame_34)
        self.hide.setObjectName(u"hide")
        self.hide.setFont(font2)

        self.gridLayout_10.addWidget(self.hide, 3, 0, 1, 1)

        self.offline_sync = QPushButton(self.frame_34)
        self.offline_sync.setObjectName(u"offline_sync")
        self.offline_sync.setFont(font2)

        self.gridLayout_10.addWidget(self.offline_sync, 2, 1, 1, 1)

        self.history = QPushButton(self.frame_34)
        self.history.setObjectName(u"history")
        self.history.setFont(font2)

        self.gridLayout_10.addWidget(self.history, 4, 0, 1, 1)

        self.settings = QPushButton(self.frame_34)
        self.settings.setObjectName(u"settings")
        self.settings.setFont(font2)

        self.gridLayout_10.addWidget(self.settings, 3, 1, 1, 1)

        self.uninstall = QPushButton(self.frame_34)
        self.uninstall.setObjectName(u"uninstall")
        self.uninstall.setFont(font2)

        self.gridLayout_10.addWidget(self.uninstall, 2, 0, 1, 1)

        self.update_service = QPushButton(self.frame_34)
        self.update_service.setObjectName(u"update_service")
        self.update_service.setFont(font2)

        self.gridLayout_10.addWidget(self.update_service, 1, 1, 1, 1)

        self.set_target = QPushButton(self.frame_34)
        self.set_target.setObjectName(u"set_target")
        self.set_target.setFont(font2)

        self.gridLayout_10.addWidget(self.set_target, 4, 1, 1, 1)

        self.check = QPushButton(self.frame_34)
        self.check.setObjectName(u"check")
        self.check.setFont(font2)

        self.gridLayout_10.addWidget(self.check, 0, 0, 1, 1)

        self.schedule = QPushButton(self.frame_34)
        self.schedule.setObjectName(u"schedule")
        self.schedule.setFont(font2)

        self.gridLayout_10.addWidget(self.schedule, 0, 1, 1, 1)

        self.install = QPushButton(self.frame_34)
        self.install.setObjectName(u"install")
        self.install.setFont(font2)

        self.gridLayout_10.addWidget(self.install, 1, 0, 1, 1)

        self.history_24h = QPushButton(self.frame_34)
        self.history_24h.setObjectName(u"history_24h")
        self.history_24h.setFont(font2)

        self.gridLayout_10.addWidget(self.history_24h, 5, 0, 1, 1)

        self.help = QPushButton(self.frame_34)
        self.help.setObjectName(u"help")
        self.help.setFont(font2)

        self.gridLayout_10.addWidget(self.help, 5, 1, 1, 1)


        self.verticalLayout_33.addLayout(self.gridLayout_10)


        self.verticalLayout_32.addWidget(self.frame_34)

        self.stackedWidget.addWidget(self.Updates_tab)

        self.verticalLayout_2.addWidget(self.stackedWidget)


        self.horizontalLayout_8.addWidget(self.center_main)

        self.right_main = QFrame(self.main_body_frame)
        self.right_main.setObjectName(u"right_main")
        self.right_main.setMinimumSize(QSize(250, 200))
        self.right_main.setMaximumSize(QSize(250, 16777215))
        self.right_main.setStyleSheet(u"*{\n"
"background-color:#24374B;\n"
"}")
        self.right_main.setFrameShape(QFrame.NoFrame)
        self.verticalLayout_17 = QVBoxLayout(self.right_main)
        self.verticalLayout_17.setSpacing(0)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.verticalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.clients_list = QTreeWidget(self.right_main)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.clients_list.setHeaderItem(__qtreewidgetitem)
        self.clients_list.setObjectName(u"clients_list")
        self.clients_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.clients_list.setDragEnabled(True)
        self.clients_list.setDragDropOverwriteMode(True)
        self.clients_list.setDragDropMode(QAbstractItemView.InternalMove)
        self.clients_list.setDefaultDropAction(Qt.MoveAction)

        self.verticalLayout_17.addWidget(self.clients_list)


        self.horizontalLayout_8.addWidget(self.right_main)


        self.verticalLayout.addWidget(self.main_body_frame)

        self.footer_frame = QFrame(self.centralwidget)
        self.footer_frame.setObjectName(u"footer_frame")
        self.footer_frame.setMinimumSize(QSize(0, 0))
        self.footer_frame.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout = QHBoxLayout(self.footer_frame)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.footer_left = QFrame(self.footer_frame)
        self.footer_left.setObjectName(u"footer_left")
        self.footer_left.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_5 = QHBoxLayout(self.footer_left)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label = QLabel(self.footer_left)
        self.label.setObjectName(u"label")
        self.label.setFont(font3)

        self.horizontalLayout_5.addWidget(self.label)


        self.horizontalLayout.addWidget(self.footer_left)

        self.footer_right = QFrame(self.footer_frame)
        self.footer_right.setObjectName(u"footer_right")
        self.footer_right.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_6 = QHBoxLayout(self.footer_right)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.pushButton_3 = QPushButton(self.footer_right)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setMinimumSize(QSize(60, 30))
        self.pushButton_3.setStyleSheet(u"*{\n"
"border: none;\n"
"\n"
"}\n"
"")

        self.horizontalLayout_6.addWidget(self.pushButton_3, 0, Qt.AlignRight)


        self.horizontalLayout.addWidget(self.footer_right)

        self.size_grip = QFrame(self.footer_frame)
        self.size_grip.setObjectName(u"size_grip")
        self.size_grip.setMinimumSize(QSize(10, 10))
        self.size_grip.setMaximumSize(QSize(10, 10))
        self.size_grip.setFrameShape(QFrame.NoFrame)

        self.horizontalLayout.addWidget(self.size_grip)


        self.verticalLayout.addWidget(self.footer_frame)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(11)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.menu_bt.setText(QCoreApplication.translate("MainWindow", u"Menu", None))
        self.title_icon.setText("")
        self.title.setText(QCoreApplication.translate("MainWindow", u"RMM MANAGER", None))
        self.minimize_button.setText("")
        self.resize_button.setText("")
        self.close_button.setText("")
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"Domain", None))
        self.Storage.setText("")
        self.DB.setText("")
        self.LocalAcc.setText("")
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Power", None))
        self.Sysinfo.setText("")
        self.power.setText("")
        self.label_8.setText("")
        self.Activities.setText("")
        self.Sensors.setText("")
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Local Account", None))
        self.program.setText("")
        self.updates.setText("")
        self.label_46.setText(QCoreApplication.translate("MainWindow", u"DataBase", None))
        self.label_48.setText(QCoreApplication.translate("MainWindow", u"Programs", None))
        self.Network.setText("")
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Activities", None))
        self.CPU.setText("")
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"System Information", None))
        self.Domain.setText("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"CPU", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"Network", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Storage", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Sensors", None))
        self.label_49.setText(QCoreApplication.translate("MainWindow", u"Updates", None))
        self.cpu_per.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"CPU Load", None))
        self.cpu_cont.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"CPU Main Core", None))
        self.cpu_main_core.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"CPU Count", None))
        self.total_ram.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"total ram\n"
"", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"available ram\n"
"", None))
        self.available_ram.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"ram usage", None))
        self.used_ram.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.ram_usage.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"used ram\n"
"", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Free Ram", None))
        self.free_ram.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        ___qtablewidgetitem = self.user_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"User name", None));
        ___qtablewidgetitem1 = self.user_table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Description", None));
        ___qtablewidgetitem2 = self.user_table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Full Name", None));
        ___qtablewidgetitem3 = self.user_table.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"User comment", None));
        ___qtablewidgetitem4 = self.user_table.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Active", None));
        ___qtablewidgetitem5 = self.user_table.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"Expire", None));
        ___qtablewidgetitem6 = self.user_table.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"Group", None));
        ___qtablewidgetitem7 = self.user_table.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"Password Last Set", None));
        ___qtablewidgetitem8 = self.user_table.horizontalHeaderItem(8)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"Password Expires", None));
        ___qtablewidgetitem9 = self.user_table.horizontalHeaderItem(9)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"Password Changeable", None));
        ___qtablewidgetitem10 = self.user_table.horizontalHeaderItem(10)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"Password Required", None));
        ___qtablewidgetitem11 = self.user_table.horizontalHeaderItem(11)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"Last Logon", None));
        self.label_34.setText(QCoreApplication.translate("MainWindow", u"CAN DELETE A USER IF ONLY USERNAME IS SET", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"User name :", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"Full name :", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"Description :", None))
        self.label_41.setText(QCoreApplication.translate("MainWindow", u"Active", None))
        self.acc_status.setItemText(0, QCoreApplication.translate("MainWindow", u"Yes", None))
        self.acc_status.setItemText(1, QCoreApplication.translate("MainWindow", u"No", None))

        self.label_43.setText(QCoreApplication.translate("MainWindow", u"Group", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"Password :", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"Pssword Confirm :", None))
        self.add_user.setText(QCoreApplication.translate("MainWindow", u"ADD", None))
        self.label_39.setText(QCoreApplication.translate("MainWindow", u"Power information", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"Status", None))
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"Time Left", None))
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"Charge", None))
        self.battery_status.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.battery_plugged.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_37.setText(QCoreApplication.translate("MainWindow", u"Plugged In", None))
        self.battery_time_left.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.battery_charge.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_32.setText(QCoreApplication.translate("MainWindow", u"CPU Power", None))
        self.cpu_consume.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.igpu_consume.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_33.setText(QCoreApplication.translate("MainWindow", u"Current AVG Power", None))
        self.gpu_consume.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_31.setText(QCoreApplication.translate("MainWindow", u"GPU Power", None))
        self.avg_consumed.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_40.setText(QCoreApplication.translate("MainWindow", u"IGPU Power", None))
        self.interval_avg.setItemText(0, QCoreApplication.translate("MainWindow", u"24h", None))
        self.interval_avg.setItemText(1, QCoreApplication.translate("MainWindow", u"1 week", None))
        self.interval_avg.setItemText(2, QCoreApplication.translate("MainWindow", u"1 month", None))

        self.update_int.setItemText(0, QCoreApplication.translate("MainWindow", u"5 seconds", None))
        self.update_int.setItemText(1, QCoreApplication.translate("MainWindow", u"1 minute", None))
        self.update_int.setItemText(2, QCoreApplication.translate("MainWindow", u"5 minutes", None))
        self.update_int.setItemText(3, QCoreApplication.translate("MainWindow", u"10 minutes", None))
        self.update_int.setItemText(4, QCoreApplication.translate("MainWindow", u"30 minutes", None))
        self.update_int.setItemText(5, QCoreApplication.translate("MainWindow", u"1 hour", None))

        self.label_69.setText(QCoreApplication.translate("MainWindow", u"Update interval:", None))
        self.label_70.setText(QCoreApplication.translate("MainWindow", u"Avg power interval:", None))
        self.intervals.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_57.setText(QCoreApplication.translate("MainWindow", u"Disk Partition", None))
        ___qtablewidgetitem12 = self.storageTable.horizontalHeaderItem(0)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("MainWindow", u"Device", None));
        ___qtablewidgetitem13 = self.storageTable.horizontalHeaderItem(1)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("MainWindow", u"Mount Point", None));
        ___qtablewidgetitem14 = self.storageTable.horizontalHeaderItem(2)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("MainWindow", u"Drive type", None));
        ___qtablewidgetitem15 = self.storageTable.horizontalHeaderItem(3)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("MainWindow", u"OPTS", None));
        ___qtablewidgetitem16 = self.storageTable.horizontalHeaderItem(4)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("MainWindow", u"Max File", None));
        ___qtablewidgetitem17 = self.storageTable.horizontalHeaderItem(5)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("MainWindow", u"Max Path", None));
        ___qtablewidgetitem18 = self.storageTable.horizontalHeaderItem(6)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("MainWindow", u"Total Storage", None));
        ___qtablewidgetitem19 = self.storageTable.horizontalHeaderItem(7)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("MainWindow", u"Free Storage", None));
        ___qtablewidgetitem20 = self.storageTable.horizontalHeaderItem(8)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("MainWindow", u"Used Storage", None));
        self.label_56.setText(QCoreApplication.translate("MainWindow", u"Activities", None))
        self.activity_search.setInputMask("")
        self.activity_search.setText("")
        self.activity_search.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Search Processes", None))
        self.pushButton_11.setText("")
        ___qtablewidgetitem21 = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("MainWindow", u"Process ID", None));
        ___qtablewidgetitem22 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem22.setText(QCoreApplication.translate("MainWindow", u"Process Name", None));
        ___qtablewidgetitem23 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem23.setText(QCoreApplication.translate("MainWindow", u"Process Status", None));
        ___qtablewidgetitem24 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem24.setText(QCoreApplication.translate("MainWindow", u"Started", None));
        ___qtablewidgetitem25 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem25.setText(QCoreApplication.translate("MainWindow", u"Suspend", None));
        ___qtablewidgetitem26 = self.tableWidget.horizontalHeaderItem(5)
        ___qtablewidgetitem26.setText(QCoreApplication.translate("MainWindow", u"Resume", None));
        ___qtablewidgetitem27 = self.tableWidget.horizontalHeaderItem(6)
        ___qtablewidgetitem27.setText(QCoreApplication.translate("MainWindow", u"Terminate", None));
        ___qtablewidgetitem28 = self.tableWidget.horizontalHeaderItem(7)
        ___qtablewidgetitem28.setText(QCoreApplication.translate("MainWindow", u"Kill", None));
        self.pushButton_12.setText(QCoreApplication.translate("MainWindow", u"Suspend", None))
        self.pushButton_13.setText(QCoreApplication.translate("MainWindow", u"Resume", None))
        self.pushButton_14.setText(QCoreApplication.translate("MainWindow", u"Terminate", None))
        self.pushButton_15.setText(QCoreApplication.translate("MainWindow", u"Kill", None))
        self.title_sensor.setText(QCoreApplication.translate("MainWindow", u"Sensors", None))
        ___qtablewidgetitem29 = self.sensors_table.horizontalHeaderItem(0)
        ___qtablewidgetitem29.setText(QCoreApplication.translate("MainWindow", u"Sensor Name", None));
        ___qtablewidgetitem30 = self.sensors_table.horizontalHeaderItem(1)
        ___qtablewidgetitem30.setText(QCoreApplication.translate("MainWindow", u"Min Value", None));
        ___qtablewidgetitem31 = self.sensors_table.horizontalHeaderItem(2)
        ___qtablewidgetitem31.setText(QCoreApplication.translate("MainWindow", u"Current Value", None));
        ___qtablewidgetitem32 = self.sensors_table.horizontalHeaderItem(3)
        ___qtablewidgetitem32.setText(QCoreApplication.translate("MainWindow", u"Max Value", None));
        ___qtablewidgetitem33 = self.sensors_table.horizontalHeaderItem(4)
        ___qtablewidgetitem33.setText(QCoreApplication.translate("MainWindow", u"AVG Value", None));
        self.label_60.setText(QCoreApplication.translate("MainWindow", u"Stats", None))
        ___qtablewidgetitem34 = self.stats_table.horizontalHeaderItem(1)
        ___qtablewidgetitem34.setText(QCoreApplication.translate("MainWindow", u"IS UP", None));
        ___qtablewidgetitem35 = self.stats_table.horizontalHeaderItem(2)
        ___qtablewidgetitem35.setText(QCoreApplication.translate("MainWindow", u"DUPLEX", None));
        ___qtablewidgetitem36 = self.stats_table.horizontalHeaderItem(3)
        ___qtablewidgetitem36.setText(QCoreApplication.translate("MainWindow", u"SPEED", None));
        ___qtablewidgetitem37 = self.stats_table.horizontalHeaderItem(4)
        ___qtablewidgetitem37.setText(QCoreApplication.translate("MainWindow", u"MTU", None));
        self.label_61.setText(QCoreApplication.translate("MainWindow", u"Network IO Counters", None))
        ___qtablewidgetitem38 = self.IO_counters_table.horizontalHeaderItem(0)
        ___qtablewidgetitem38.setText(QCoreApplication.translate("MainWindow", u"Adapter", None));
        ___qtablewidgetitem39 = self.IO_counters_table.horizontalHeaderItem(1)
        ___qtablewidgetitem39.setText(QCoreApplication.translate("MainWindow", u"BYTES SEND", None));
        ___qtablewidgetitem40 = self.IO_counters_table.horizontalHeaderItem(2)
        ___qtablewidgetitem40.setText(QCoreApplication.translate("MainWindow", u"BYTES RECEIVED", None));
        ___qtablewidgetitem41 = self.IO_counters_table.horizontalHeaderItem(3)
        ___qtablewidgetitem41.setText(QCoreApplication.translate("MainWindow", u"PACKETS SEND", None));
        ___qtablewidgetitem42 = self.IO_counters_table.horizontalHeaderItem(4)
        ___qtablewidgetitem42.setText(QCoreApplication.translate("MainWindow", u"PACKETS RECEIVED", None));
        ___qtablewidgetitem43 = self.IO_counters_table.horizontalHeaderItem(5)
        ___qtablewidgetitem43.setText(QCoreApplication.translate("MainWindow", u"ERR IN", None));
        ___qtablewidgetitem44 = self.IO_counters_table.horizontalHeaderItem(6)
        ___qtablewidgetitem44.setText(QCoreApplication.translate("MainWindow", u"ERR OUT", None));
        ___qtablewidgetitem45 = self.IO_counters_table.horizontalHeaderItem(7)
        ___qtablewidgetitem45.setText(QCoreApplication.translate("MainWindow", u"DROP IN", None));
        ___qtablewidgetitem46 = self.IO_counters_table.horizontalHeaderItem(8)
        ___qtablewidgetitem46.setText(QCoreApplication.translate("MainWindow", u"DROP OUT", None));
        self.label_62.setText(QCoreApplication.translate("MainWindow", u"Network Addresses", None))
        ___qtablewidgetitem47 = self.addresses_table.horizontalHeaderItem(0)
        ___qtablewidgetitem47.setText(QCoreApplication.translate("MainWindow", u"Adaptor", None));
        ___qtablewidgetitem48 = self.addresses_table.horizontalHeaderItem(1)
        ___qtablewidgetitem48.setText(QCoreApplication.translate("MainWindow", u"FAMILY", None));
        ___qtablewidgetitem49 = self.addresses_table.horizontalHeaderItem(2)
        ___qtablewidgetitem49.setText(QCoreApplication.translate("MainWindow", u"ADDRESS", None));
        ___qtablewidgetitem50 = self.addresses_table.horizontalHeaderItem(3)
        ___qtablewidgetitem50.setText(QCoreApplication.translate("MainWindow", u"NETMASK", None));
        ___qtablewidgetitem51 = self.addresses_table.horizontalHeaderItem(4)
        ___qtablewidgetitem51.setText(QCoreApplication.translate("MainWindow", u"Broadcast", None));
        ___qtablewidgetitem52 = self.addresses_table.horizontalHeaderItem(5)
        ___qtablewidgetitem52.setText(QCoreApplication.translate("MainWindow", u"PTP", None));
        self.label_63.setText(QCoreApplication.translate("MainWindow", u"Network Connections", None))
        ___qtablewidgetitem53 = self.connections_table.horizontalHeaderItem(0)
        ___qtablewidgetitem53.setText(QCoreApplication.translate("MainWindow", u"FD", None));
        ___qtablewidgetitem54 = self.connections_table.horizontalHeaderItem(1)
        ___qtablewidgetitem54.setText(QCoreApplication.translate("MainWindow", u"FAMILY", None));
        ___qtablewidgetitem55 = self.connections_table.horizontalHeaderItem(2)
        ___qtablewidgetitem55.setText(QCoreApplication.translate("MainWindow", u"FAMILY", None));
        ___qtablewidgetitem56 = self.connections_table.horizontalHeaderItem(3)
        ___qtablewidgetitem56.setText(QCoreApplication.translate("MainWindow", u"LADDR", None));
        ___qtablewidgetitem57 = self.connections_table.horizontalHeaderItem(4)
        ___qtablewidgetitem57.setText(QCoreApplication.translate("MainWindow", u"RADDR", None));
        ___qtablewidgetitem58 = self.connections_table.horizontalHeaderItem(5)
        ___qtablewidgetitem58.setText(QCoreApplication.translate("MainWindow", u"STATUS", None));
        ___qtablewidgetitem59 = self.connections_table.horizontalHeaderItem(6)
        ___qtablewidgetitem59.setText(QCoreApplication.translate("MainWindow", u"PID", None));
        self.label_52.setText(QCoreApplication.translate("MainWindow", u"System time", None))
        self.label_45.setText(QCoreApplication.translate("MainWindow", u"Version", None))
        self.label_47.setText(QCoreApplication.translate("MainWindow", u"System Date", None))
        self.system_time.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_42.setText(QCoreApplication.translate("MainWindow", u"System information", None))
        self.system_platform.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.system_system.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.system_machine.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.system_version.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_50.setText(QCoreApplication.translate("MainWindow", u"CPU Model", None))
        self.system_date.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_44.setText(QCoreApplication.translate("MainWindow", u"Platform", None))
        self.system_processor.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_51.setText(QCoreApplication.translate("MainWindow", u"Machine", None))
        self.get_hardware_info.setText(QCoreApplication.translate("MainWindow", u"Get hardware information", None))
        self.status_domain.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.name_domain.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_35.setText(QCoreApplication.translate("MainWindow", u"Status Domain:", None))
        self.label_38.setText(QCoreApplication.translate("MainWindow", u"Name Domain:", None))
        self.label_36.setText(QCoreApplication.translate("MainWindow", u"IF DOMAIN IS EMPTY CLIENT WILL LEAVE DOMAIN,USE LOCAL ADMINISTRATOR ACOUNT", None))
        self.label_29.setText(QCoreApplication.translate("MainWindow", u"Administrator Domain Account:", None))
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"Domain:", None))
        self.label_30.setText(QCoreApplication.translate("MainWindow", u"Administrator Domain Password:", None))
        self.add_domain.setText(QCoreApplication.translate("MainWindow", u"Add to domain", None))
        self.load_client.setText(QCoreApplication.translate("MainWindow", u"Clienti", None))
        self.load_locatii.setText(QCoreApplication.translate("MainWindow", u"Locatii", None))
        self.load_incaperi.setText(QCoreApplication.translate("MainWindow", u"Incaperi", None))
        self.load_power.setText(QCoreApplication.translate("MainWindow", u"Power", None))
        self.load_hardware.setText(QCoreApplication.translate("MainWindow", u"Hardware", None))
        self.label_68.setText(QCoreApplication.translate("MainWindow", u"Incapere", None))
        self.label_67.setText(QCoreApplication.translate("MainWindow", u"Locatie:", None))
        self.add_button.setText(QCoreApplication.translate("MainWindow", u"Add ", None))
        ___qtablewidgetitem60 = self.installed_table.horizontalHeaderItem(0)
        ___qtablewidgetitem60.setText(QCoreApplication.translate("MainWindow", u"Name", None));
        ___qtablewidgetitem61 = self.installed_table.horizontalHeaderItem(1)
        ___qtablewidgetitem61.setText(QCoreApplication.translate("MainWindow", u"Version", None));
        ___qtablewidgetitem62 = self.installed_table.horizontalHeaderItem(2)
        ___qtablewidgetitem62.setText(QCoreApplication.translate("MainWindow", u"Install Date", None));
        ___qtablewidgetitem63 = self.installed_table.horizontalHeaderItem(3)
        ___qtablewidgetitem63.setText(QCoreApplication.translate("MainWindow", u"Publisher", None));
        self.label_53.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_58.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_55.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_64.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_54.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_59.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Install", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"Uninstall", None))
        self.label_65.setText(QCoreApplication.translate("MainWindow", u"OPTIONS", None))
        self.args.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Argument", None))
        self.hide.setText(QCoreApplication.translate("MainWindow", u"Hide-Updates", None))
        self.offline_sync.setText(QCoreApplication.translate("MainWindow", u"add-offline-sync-service ", None))
        self.history.setText(QCoreApplication.translate("MainWindow", u"get-update-history", None))
        self.settings.setText(QCoreApplication.translate("MainWindow", u"get-update-settings", None))
        self.uninstall.setText(QCoreApplication.translate("MainWindow", u"uninstall-update", None))
        self.update_service.setText(QCoreApplication.translate("MainWindow", u"add-microsoft-update-service", None))
        self.set_target.setText(QCoreApplication.translate("MainWindow", u"set-target-version ", None))
        self.check.setText(QCoreApplication.translate("MainWindow", u"Check for updates", None))
        self.schedule.setText(QCoreApplication.translate("MainWindow", u"schedule-update ", None))
        self.install.setText(QCoreApplication.translate("MainWindow", u"Install updates", None))
        self.history_24h.setText(QCoreApplication.translate("MainWindow", u"get-update-history-24h", None))
        self.help.setText(QCoreApplication.translate("MainWindow", u"Help", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Version 1.0", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"?", None))
    # retranslateUi

