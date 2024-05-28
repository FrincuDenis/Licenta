# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'interfacekqkPJR.ui'
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


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1075, 607)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setStyleSheet(u"*{\n"
"border: none;\n"
"background-color:#1E1E1E;\n"
"}\n"
"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.header_frame = QFrame(self.centralwidget)
        self.header_frame.setObjectName(u"header_frame")
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
        self.header_left.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_7 = QHBoxLayout(self.header_left)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.menu_bt = QPushButton(self.header_left)
        self.menu_bt.setObjectName(u"menu_bt")
        font = QFont()
        font.setFamily(u"Asus Rog")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.menu_bt.setFont(font)
        icon = QIcon()
        icon.addFile(u":/feather/icons/feather/menu.png", QSize(), QIcon.Normal, QIcon.Off)
        self.menu_bt.setIcon(icon)
        self.menu_bt.setIconSize(QSize(32, 32))

        self.horizontalLayout_7.addWidget(self.menu_bt, 0, Qt.AlignLeft)


        self.horizontalLayout_4.addWidget(self.header_left)

        self.header_center = QFrame(self.header_frame)
        self.header_center.setObjectName(u"header_center")
        self.header_center.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_3 = QHBoxLayout(self.header_center)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.title_icon = QLabel(self.header_center)
        self.title_icon.setObjectName(u"title_icon")
        self.title_icon.setMaximumSize(QSize(30, 30))
        self.title_icon.setAutoFillBackground(False)
        self.title_icon.setPixmap(QPixmap(u":/material_design/icons/material_design/important_devices.png"))
        self.title_icon.setScaledContents(True)

        self.horizontalLayout_3.addWidget(self.title_icon)

        self.title = QLabel(self.header_center)
        self.title.setObjectName(u"title")
        font1 = QFont()
        font1.setFamily(u"Asus Rog")
        font1.setPointSize(12)
        font1.setBold(True)
        font1.setWeight(75)
        self.title.setFont(font1)

        self.horizontalLayout_3.addWidget(self.title)


        self.horizontalLayout_4.addWidget(self.header_center)

        self.header_right = QFrame(self.header_frame)
        self.header_right.setObjectName(u"header_right")
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
        self.Sensors = QPushButton(self.menu)
        self.Sensors.setObjectName(u"Sensors")
        icon4 = QIcon()
        icon4.addFile(u":/font_awesome_solid/icons/font_awesome/solid/temperature-empty.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Sensors.setIcon(icon4)
        self.Sensors.setIconSize(QSize(30, 30))

        self.gridLayout.addWidget(self.Sensors, 7, 0, 1, 1, Qt.AlignLeft)

        self.Activities = QPushButton(self.menu)
        self.Activities.setObjectName(u"Activities")
        icon5 = QIcon()
        icon5.addFile(u":/feather/icons/feather/activity.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Activities.setIcon(icon5)
        self.Activities.setIconSize(QSize(30, 30))

        self.gridLayout.addWidget(self.Activities, 5, 0, 1, 1, Qt.AlignLeft)

        self.label_9 = QLabel(self.menu)
        self.label_9.setObjectName(u"label_9")
        font2 = QFont()
        font2.setFamily(u"ROG Fonts")
        self.label_9.setFont(font2)

        self.gridLayout.addWidget(self.label_9, 0, 1, 1, 1)

        self.label_4 = QLabel(self.menu)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font2)
        self.label_4.setMargin(5)

        self.gridLayout.addWidget(self.label_4, 4, 1, 1, 1)

        self.label_23 = QLabel(self.menu)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setFont(font2)

        self.gridLayout.addWidget(self.label_23, 1, 1, 1, 1)

        self.Clientlist = QPushButton(self.menu)
        self.Clientlist.setObjectName(u"Clientlist")
        icon6 = QIcon()
        icon6.addFile(u":/material_design/icons/material_design/person.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Clientlist.setIcon(icon6)
        self.Clientlist.setIconSize(QSize(30, 30))

        self.gridLayout.addWidget(self.Clientlist, 0, 0, 1, 1, Qt.AlignLeft)

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

        self.label_3 = QLabel(self.menu)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font2)
        self.label_3.setMargin(5)

        self.gridLayout.addWidget(self.label_3, 3, 1, 1, 1)

        self.CPU = QPushButton(self.menu)
        self.CPU.setObjectName(u"CPU")
        icon7 = QIcon()
        icon7.addFile(u":/feather/icons/feather/cpu.png", QSize(), QIcon.Normal, QIcon.Off)
        self.CPU.setIcon(icon7)
        self.CPU.setIconSize(QSize(30, 30))

        self.gridLayout.addWidget(self.CPU, 2, 0, 1, 1, Qt.AlignLeft)

        self.label_5 = QLabel(self.menu)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font2)
        self.label_5.setMargin(5)

        self.gridLayout.addWidget(self.label_5, 5, 1, 1, 1)

        self.Domain = QPushButton(self.menu)
        self.Domain.setObjectName(u"Domain")
        icon8 = QIcon()
        icon8.addFile(u":/material_design/icons/material_design/domain.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Domain.setIcon(icon8)
        self.Domain.setIconSize(QSize(32, 32))

        self.gridLayout.addWidget(self.Domain, 1, 0, 1, 1, Qt.AlignLeft)

        self.Sysinfo = QPushButton(self.menu)
        self.Sysinfo.setObjectName(u"Sysinfo")
        icon9 = QIcon()
        icon9.addFile(u":/feather/icons/feather/monitor.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Sysinfo.setIcon(icon9)
        self.Sysinfo.setIconSize(QSize(30, 30))

        self.gridLayout.addWidget(self.Sysinfo, 4, 0, 1, 1, Qt.AlignLeft)

        self.label_18 = QLabel(self.menu)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setFont(font2)

        self.gridLayout.addWidget(self.label_18, 8, 1, 1, 1)

        self.power = QPushButton(self.menu)
        self.power.setObjectName(u"power")
        icon10 = QIcon()
        icon10.addFile(u":/feather/icons/feather/zap.png", QSize(), QIcon.Normal, QIcon.Off)
        self.power.setIcon(icon10)
        self.power.setIconSize(QSize(30, 30))

        self.gridLayout.addWidget(self.power, 3, 0, 1, 1, Qt.AlignLeft)

        self.Storage = QPushButton(self.menu)
        self.Storage.setObjectName(u"Storage")
        icon11 = QIcon()
        icon11.addFile(u":/feather/icons/feather/disc.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Storage.setIcon(icon11)
        self.Storage.setIconSize(QSize(30, 30))

        self.gridLayout.addWidget(self.Storage, 6, 0, 1, 1, Qt.AlignLeft)

        self.label_2 = QLabel(self.menu)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font2)
        self.label_2.setMargin(5)

        self.gridLayout.addWidget(self.label_2, 2, 1, 1, 1)

        self.Network = QPushButton(self.menu)
        self.Network.setObjectName(u"Network")
        icon12 = QIcon()
        icon12.addFile(u":/font_awesome_solid/icons/font_awesome/solid/network-wired.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Network.setIcon(icon12)
        self.Network.setIconSize(QSize(30, 30))

        self.gridLayout.addWidget(self.Network, 8, 0, 1, 1, Qt.AlignLeft)

        self.label_8 = QLabel(self.menu)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setEnabled(False)
        font3 = QFont()
        font3.setFamily(u"Asus Rog")
        self.label_8.setFont(font3)
        self.label_8.setMargin(5)

        self.gridLayout.addWidget(self.label_8, 8, 2, 1, 1)


        self.verticalLayout_18.addWidget(self.menu, 0, Qt.AlignLeft)


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
        self.cpu_per.setFont(font3)

        self.gridLayout_2.addWidget(self.cpu_per, 1, 1, 1, 1)

        self.label_11 = QLabel(self.cpu_info)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font3)

        self.gridLayout_2.addWidget(self.label_11, 1, 0, 1, 1)

        self.cpu_cont = QLabel(self.cpu_info)
        self.cpu_cont.setObjectName(u"cpu_cont")
        self.cpu_cont.setFont(font3)

        self.gridLayout_2.addWidget(self.cpu_cont, 0, 1, 1, 1)

        self.label_12 = QLabel(self.cpu_info)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setFont(font3)

        self.gridLayout_2.addWidget(self.label_12, 2, 0, 1, 1)

        self.cpu_main_core = QLabel(self.cpu_info)
        self.cpu_main_core.setObjectName(u"cpu_main_core")
        self.cpu_main_core.setFont(font3)

        self.gridLayout_2.addWidget(self.cpu_main_core, 2, 1, 1, 1)

        self.label_10 = QLabel(self.cpu_info)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font3)

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
        self.total_ram.setFont(font3)

        self.gridLayout_3.addWidget(self.total_ram, 0, 3, 1, 1)

        self.label_14 = QLabel(self.ram_info)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setFont(font3)

        self.gridLayout_3.addWidget(self.label_14, 0, 2, 1, 1, Qt.AlignLeft)

        self.label_16 = QLabel(self.ram_info)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setFont(font3)

        self.gridLayout_3.addWidget(self.label_16, 1, 2, 1, 1, Qt.AlignLeft)

        self.available_ram = QLabel(self.ram_info)
        self.available_ram.setObjectName(u"available_ram")
        self.available_ram.setFont(font3)

        self.gridLayout_3.addWidget(self.available_ram, 1, 3, 1, 1)

        self.label_13 = QLabel(self.ram_info)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setFont(font3)

        self.gridLayout_3.addWidget(self.label_13, 4, 2, 1, 1, Qt.AlignLeft)

        self.used_ram = QLabel(self.ram_info)
        self.used_ram.setObjectName(u"used_ram")
        self.used_ram.setFont(font3)

        self.gridLayout_3.addWidget(self.used_ram, 2, 3, 1, 1)

        self.RAM_PROGRESS = spiralProgressBar(self.ram_info)
        self.RAM_PROGRESS.setObjectName(u"RAM_PROGRESS")
        self.RAM_PROGRESS.setMaximumSize(QSize(150, 150))

        self.gridLayout_3.addWidget(self.RAM_PROGRESS, 0, 4, 5, 1)

        self.ram_usage = QLabel(self.ram_info)
        self.ram_usage.setObjectName(u"ram_usage")
        self.ram_usage.setFont(font3)

        self.gridLayout_3.addWidget(self.ram_usage, 4, 3, 1, 1)

        self.label_15 = QLabel(self.ram_info)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setFont(font3)

        self.gridLayout_3.addWidget(self.label_15, 2, 2, 1, 1, Qt.AlignLeft)

        self.label_17 = QLabel(self.ram_info)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setFont(font3)

        self.gridLayout_3.addWidget(self.label_17, 3, 2, 1, 1)

        self.free_ram = QLabel(self.ram_info)
        self.free_ram.setObjectName(u"free_ram")
        self.free_ram.setFont(font3)

        self.gridLayout_3.addWidget(self.free_ram, 3, 3, 1, 1)


        self.verticalLayout_6.addWidget(self.ram_info)

        self.stackedWidget.addWidget(self.cpu_memory)
        self.Domain_status = QWidget()
        self.Domain_status.setObjectName(u"Domain_status")
        self.stackedWidget.addWidget(self.Domain_status)
        self.Power = QWidget()
        self.Power.setObjectName(u"Power")
        self.verticalLayout_3 = QVBoxLayout(self.Power)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_39 = QLabel(self.Power)
        self.label_39.setObjectName(u"label_39")
        self.label_39.setFont(font1)

        self.verticalLayout_3.addWidget(self.label_39)

        self.Battery = QFrame(self.Power)
        self.Battery.setObjectName(u"Battery")
        sizePolicy1.setHeightForWidth(self.Battery.sizePolicy().hasHeightForWidth())
        self.Battery.setSizePolicy(sizePolicy1)
        self.Battery.setFrameShape(QFrame.NoFrame)
        self.gridLayout_4 = QGridLayout(self.Battery)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_25 = QLabel(self.Battery)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setFont(font3)

        self.gridLayout_4.addWidget(self.label_25, 0, 0, 1, 1)

        self.label_27 = QLabel(self.Battery)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setFont(font3)

        self.gridLayout_4.addWidget(self.label_27, 2, 0, 1, 1)

        self.label_26 = QLabel(self.Battery)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setFont(font3)

        self.gridLayout_4.addWidget(self.label_26, 1, 0, 1, 1)

        self.battery_status = QLabel(self.Battery)
        self.battery_status.setObjectName(u"battery_status")
        self.battery_status.setFont(font3)

        self.gridLayout_4.addWidget(self.battery_status, 0, 1, 1, 1)

        self.battery_plugged = QLabel(self.Battery)
        self.battery_plugged.setObjectName(u"battery_plugged")
        self.battery_plugged.setFont(font3)

        self.gridLayout_4.addWidget(self.battery_plugged, 3, 1, 1, 1)

        self.label_37 = QLabel(self.Battery)
        self.label_37.setObjectName(u"label_37")
        self.label_37.setFont(font3)

        self.gridLayout_4.addWidget(self.label_37, 3, 0, 1, 1)

        self.battery_time_left = QLabel(self.Battery)
        self.battery_time_left.setObjectName(u"battery_time_left")
        self.battery_time_left.setFont(font3)

        self.gridLayout_4.addWidget(self.battery_time_left, 2, 1, 1, 1)

        self.battery_charge = QLabel(self.Battery)
        self.battery_charge.setObjectName(u"battery_charge")
        self.battery_charge.setFont(font3)

        self.gridLayout_4.addWidget(self.battery_charge, 1, 1, 1, 1)

        self.battery_usage = roundProgressBar(self.Battery)
        self.battery_usage.setObjectName(u"battery_usage")

        self.gridLayout_4.addWidget(self.battery_usage, 0, 2, 4, 1)


        self.verticalLayout_3.addWidget(self.Battery)

        self.Consumed = QFrame(self.Power)
        self.Consumed.setObjectName(u"Consumed")
        sizePolicy1.setHeightForWidth(self.Consumed.sizePolicy().hasHeightForWidth())
        self.Consumed.setSizePolicy(sizePolicy1)
        self.Consumed.setFrameShape(QFrame.NoFrame)
        self.gridLayout_5 = QGridLayout(self.Consumed)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.avg_consumed = QLabel(self.Consumed)
        self.avg_consumed.setObjectName(u"avg_consumed")
        self.avg_consumed.setFont(font3)

        self.gridLayout_5.addWidget(self.avg_consumed, 3, 1, 1, 1)

        self.label_32 = QLabel(self.Consumed)
        self.label_32.setObjectName(u"label_32")
        self.label_32.setFont(font3)

        self.gridLayout_5.addWidget(self.label_32, 2, 0, 1, 1)

        self.cpu_consume = QLabel(self.Consumed)
        self.cpu_consume.setObjectName(u"cpu_consume")
        self.cpu_consume.setFont(font3)

        self.gridLayout_5.addWidget(self.cpu_consume, 2, 1, 1, 1)

        self.igpu_consume = QLabel(self.Consumed)
        self.igpu_consume.setObjectName(u"igpu_consume")
        self.igpu_consume.setFont(font3)

        self.gridLayout_5.addWidget(self.igpu_consume, 1, 1, 1, 1)

        self.label_31 = QLabel(self.Consumed)
        self.label_31.setObjectName(u"label_31")
        self.label_31.setFont(font3)

        self.gridLayout_5.addWidget(self.label_31, 0, 0, 1, 1)

        self.label_40 = QLabel(self.Consumed)
        self.label_40.setObjectName(u"label_40")
        self.label_40.setFont(font3)

        self.gridLayout_5.addWidget(self.label_40, 1, 0, 1, 1)

        self.gpu_consume = QLabel(self.Consumed)
        self.gpu_consume.setObjectName(u"gpu_consume")
        self.gpu_consume.setFont(font3)

        self.gridLayout_5.addWidget(self.gpu_consume, 0, 1, 1, 1)

        self.label_33 = QLabel(self.Consumed)
        self.label_33.setObjectName(u"label_33")
        self.label_33.setFont(font3)

        self.gridLayout_5.addWidget(self.label_33, 3, 0, 1, 1)

        self.power_progress = spiralProgressBar(self.Consumed)
        self.power_progress.setObjectName(u"power_progress")

        self.gridLayout_5.addWidget(self.power_progress, 0, 2, 4, 1)


        self.verticalLayout_3.addWidget(self.Consumed)

        self.stackedWidget.addWidget(self.Power)
        self.storage = QWidget()
        self.storage.setObjectName(u"storage")
        self.verticalLayout_9 = QVBoxLayout(self.storage)
        self.verticalLayout_9.setSpacing(10)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.label_57 = QLabel(self.storage)
        self.label_57.setObjectName(u"label_57")
        font4 = QFont()
        font4.setFamily(u"Asus Rog")
        font4.setPointSize(12)
        font4.setBold(False)
        font4.setWeight(50)
        self.label_57.setFont(font4)

        self.verticalLayout_9.addWidget(self.label_57)

        self.storageTable = QTableWidget(self.storage)
        if (self.storageTable.columnCount() < 10):
            self.storageTable.setColumnCount(10)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setFont(font3);
        self.storageTable.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setFont(font3);
        self.storageTable.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        __qtablewidgetitem2.setFont(font3);
        self.storageTable.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        __qtablewidgetitem3.setFont(font3);
        self.storageTable.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        __qtablewidgetitem4.setFont(font3);
        self.storageTable.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        __qtablewidgetitem5.setFont(font3);
        self.storageTable.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        __qtablewidgetitem6.setFont(font3);
        self.storageTable.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        __qtablewidgetitem7.setFont(font3);
        self.storageTable.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        __qtablewidgetitem8.setFont(font3);
        self.storageTable.setHorizontalHeaderItem(8, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.storageTable.setHorizontalHeaderItem(9, __qtablewidgetitem9)
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
        self.label_56.setFont(font1)

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
        self.activity_search.setFont(font3)

        self.horizontalLayout_12.addWidget(self.activity_search)

        self.pushButton_11 = QPushButton(self.frame_5)
        self.pushButton_11.setObjectName(u"pushButton_11")
        icon13 = QIcon()
        icon13.addFile(u":/feather/icons/feather/search.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_11.setIcon(icon13)

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
        __qtablewidgetitem10 = QTableWidgetItem()
        __qtablewidgetitem10.setFont(font3);
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        __qtablewidgetitem11.setFont(font3);
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        __qtablewidgetitem12.setFont(font3);
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        __qtablewidgetitem13.setFont(font3);
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        __qtablewidgetitem14.setFont(font3);
        self.tableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        __qtablewidgetitem15.setFont(font3);
        self.tableWidget.setHorizontalHeaderItem(5, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        __qtablewidgetitem16.setFont(font3);
        self.tableWidget.setHorizontalHeaderItem(6, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        __qtablewidgetitem17.setFont(font3);
        self.tableWidget.setHorizontalHeaderItem(7, __qtablewidgetitem17)
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
        self.pushButton_12.setFont(font3)

        self.horizontalLayout_13.addWidget(self.pushButton_12)

        self.pushButton_13 = QPushButton(self.frame_4)
        self.pushButton_13.setObjectName(u"pushButton_13")
        self.pushButton_13.setFont(font3)

        self.horizontalLayout_13.addWidget(self.pushButton_13)

        self.pushButton_14 = QPushButton(self.frame_4)
        self.pushButton_14.setObjectName(u"pushButton_14")
        self.pushButton_14.setFont(font3)

        self.horizontalLayout_13.addWidget(self.pushButton_14)

        self.pushButton_15 = QPushButton(self.frame_4)
        self.pushButton_15.setObjectName(u"pushButton_15")
        self.pushButton_15.setFont(font3)

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
        self.title_sensor.setFont(font1)

        self.verticalLayout_8.addWidget(self.title_sensor)

        self.sensors_table = QTableWidget(self.sensors)
        if (self.sensors_table.columnCount() < 5):
            self.sensors_table.setColumnCount(5)
        __qtablewidgetitem18 = QTableWidgetItem()
        __qtablewidgetitem18.setFont(font3);
        self.sensors_table.setHorizontalHeaderItem(0, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        __qtablewidgetitem19.setFont(font3);
        self.sensors_table.setHorizontalHeaderItem(1, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        __qtablewidgetitem20.setFont(font3);
        self.sensors_table.setHorizontalHeaderItem(2, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        __qtablewidgetitem21.setFont(font3);
        self.sensors_table.setHorizontalHeaderItem(3, __qtablewidgetitem21)
        __qtablewidgetitem22 = QTableWidgetItem()
        __qtablewidgetitem22.setFont(font3);
        self.sensors_table.setHorizontalHeaderItem(4, __qtablewidgetitem22)
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
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 776, 1076))
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
        __qtablewidgetitem23 = QTableWidgetItem()
        self.stats_table.setHorizontalHeaderItem(0, __qtablewidgetitem23)
        __qtablewidgetitem24 = QTableWidgetItem()
        __qtablewidgetitem24.setFont(font3);
        self.stats_table.setHorizontalHeaderItem(1, __qtablewidgetitem24)
        __qtablewidgetitem25 = QTableWidgetItem()
        __qtablewidgetitem25.setFont(font3);
        self.stats_table.setHorizontalHeaderItem(2, __qtablewidgetitem25)
        __qtablewidgetitem26 = QTableWidgetItem()
        __qtablewidgetitem26.setFont(font3);
        self.stats_table.setHorizontalHeaderItem(3, __qtablewidgetitem26)
        __qtablewidgetitem27 = QTableWidgetItem()
        __qtablewidgetitem27.setFont(font3);
        self.stats_table.setHorizontalHeaderItem(4, __qtablewidgetitem27)
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
        __qtablewidgetitem28 = QTableWidgetItem()
        __qtablewidgetitem28.setFont(font3);
        self.IO_counters_table.setHorizontalHeaderItem(0, __qtablewidgetitem28)
        __qtablewidgetitem29 = QTableWidgetItem()
        __qtablewidgetitem29.setFont(font3);
        self.IO_counters_table.setHorizontalHeaderItem(1, __qtablewidgetitem29)
        __qtablewidgetitem30 = QTableWidgetItem()
        __qtablewidgetitem30.setFont(font3);
        self.IO_counters_table.setHorizontalHeaderItem(2, __qtablewidgetitem30)
        __qtablewidgetitem31 = QTableWidgetItem()
        __qtablewidgetitem31.setFont(font3);
        self.IO_counters_table.setHorizontalHeaderItem(3, __qtablewidgetitem31)
        __qtablewidgetitem32 = QTableWidgetItem()
        __qtablewidgetitem32.setFont(font3);
        self.IO_counters_table.setHorizontalHeaderItem(4, __qtablewidgetitem32)
        __qtablewidgetitem33 = QTableWidgetItem()
        __qtablewidgetitem33.setFont(font3);
        self.IO_counters_table.setHorizontalHeaderItem(5, __qtablewidgetitem33)
        __qtablewidgetitem34 = QTableWidgetItem()
        __qtablewidgetitem34.setFont(font3);
        self.IO_counters_table.setHorizontalHeaderItem(6, __qtablewidgetitem34)
        __qtablewidgetitem35 = QTableWidgetItem()
        __qtablewidgetitem35.setFont(font3);
        self.IO_counters_table.setHorizontalHeaderItem(7, __qtablewidgetitem35)
        __qtablewidgetitem36 = QTableWidgetItem()
        __qtablewidgetitem36.setFont(font3);
        self.IO_counters_table.setHorizontalHeaderItem(8, __qtablewidgetitem36)
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
        __qtablewidgetitem37 = QTableWidgetItem()
        __qtablewidgetitem37.setFont(font3);
        self.addresses_table.setHorizontalHeaderItem(0, __qtablewidgetitem37)
        __qtablewidgetitem38 = QTableWidgetItem()
        __qtablewidgetitem38.setFont(font3);
        self.addresses_table.setHorizontalHeaderItem(1, __qtablewidgetitem38)
        __qtablewidgetitem39 = QTableWidgetItem()
        __qtablewidgetitem39.setFont(font3);
        self.addresses_table.setHorizontalHeaderItem(2, __qtablewidgetitem39)
        __qtablewidgetitem40 = QTableWidgetItem()
        __qtablewidgetitem40.setFont(font3);
        self.addresses_table.setHorizontalHeaderItem(3, __qtablewidgetitem40)
        __qtablewidgetitem41 = QTableWidgetItem()
        __qtablewidgetitem41.setFont(font3);
        self.addresses_table.setHorizontalHeaderItem(4, __qtablewidgetitem41)
        __qtablewidgetitem42 = QTableWidgetItem()
        __qtablewidgetitem42.setFont(font3);
        self.addresses_table.setHorizontalHeaderItem(5, __qtablewidgetitem42)
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
        self.label_63.setFont(font1)

        self.verticalLayout_16.addWidget(self.label_63)

        self.connections_table = QTableWidget(self.frame_9)
        if (self.connections_table.columnCount() < 7):
            self.connections_table.setColumnCount(7)
        __qtablewidgetitem43 = QTableWidgetItem()
        __qtablewidgetitem43.setFont(font3);
        self.connections_table.setHorizontalHeaderItem(0, __qtablewidgetitem43)
        __qtablewidgetitem44 = QTableWidgetItem()
        __qtablewidgetitem44.setFont(font3);
        self.connections_table.setHorizontalHeaderItem(1, __qtablewidgetitem44)
        __qtablewidgetitem45 = QTableWidgetItem()
        __qtablewidgetitem45.setFont(font3);
        self.connections_table.setHorizontalHeaderItem(2, __qtablewidgetitem45)
        __qtablewidgetitem46 = QTableWidgetItem()
        __qtablewidgetitem46.setFont(font3);
        self.connections_table.setHorizontalHeaderItem(3, __qtablewidgetitem46)
        __qtablewidgetitem47 = QTableWidgetItem()
        __qtablewidgetitem47.setFont(font3);
        self.connections_table.setHorizontalHeaderItem(4, __qtablewidgetitem47)
        __qtablewidgetitem48 = QTableWidgetItem()
        __qtablewidgetitem48.setFont(font3);
        self.connections_table.setHorizontalHeaderItem(5, __qtablewidgetitem48)
        __qtablewidgetitem49 = QTableWidgetItem()
        __qtablewidgetitem49.setFont(font3);
        self.connections_table.setHorizontalHeaderItem(6, __qtablewidgetitem49)
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
        self.label_42 = QLabel(self.frame)
        self.label_42.setObjectName(u"label_42")
        self.label_42.setFont(font1)

        self.gridLayout_6.addWidget(self.label_42, 0, 0, 1, 1)

        self.system_date = QLabel(self.frame)
        self.system_date.setObjectName(u"system_date")
        self.system_date.setFont(font3)

        self.gridLayout_6.addWidget(self.system_date, 4, 4, 1, 1)

        self.label_51 = QLabel(self.frame)
        self.label_51.setObjectName(u"label_51")
        self.label_51.setFont(font3)

        self.gridLayout_6.addWidget(self.label_51, 3, 3, 1, 1)

        self.system_version = QLabel(self.frame)
        self.system_version.setObjectName(u"system_version")
        self.system_version.setFont(font3)

        self.gridLayout_6.addWidget(self.system_version, 3, 2, 1, 1)

        self.label_47 = QLabel(self.frame)
        self.label_47.setObjectName(u"label_47")
        self.label_47.setFont(font3)

        self.gridLayout_6.addWidget(self.label_47, 4, 0, 1, 1)

        self.label_44 = QLabel(self.frame)
        self.label_44.setObjectName(u"label_44")
        self.label_44.setFont(font3)

        self.gridLayout_6.addWidget(self.label_44, 2, 0, 1, 1, Qt.AlignLeft)

        self.system_time = QLabel(self.frame)
        self.system_time.setObjectName(u"system_time")
        self.system_time.setFont(font3)

        self.gridLayout_6.addWidget(self.system_time, 4, 2, 1, 1)

        self.label_50 = QLabel(self.frame)
        self.label_50.setObjectName(u"label_50")
        self.label_50.setFont(font3)

        self.gridLayout_6.addWidget(self.label_50, 2, 3, 1, 1)

        self.system_processor = QLabel(self.frame)
        self.system_processor.setObjectName(u"system_processor")
        self.system_processor.setFont(font3)

        self.gridLayout_6.addWidget(self.system_processor, 2, 4, 1, 1)

        self.label_45 = QLabel(self.frame)
        self.label_45.setObjectName(u"label_45")
        self.label_45.setFont(font3)

        self.gridLayout_6.addWidget(self.label_45, 3, 0, 1, 1)

        self.system_system = QLabel(self.frame)
        self.system_system.setObjectName(u"system_system")
        self.system_system.setFont(font3)

        self.gridLayout_6.addWidget(self.system_system, 1, 0, 1, 1)

        self.system_machine = QLabel(self.frame)
        self.system_machine.setObjectName(u"system_machine")
        self.system_machine.setFont(font3)

        self.gridLayout_6.addWidget(self.system_machine, 3, 4, 1, 1)

        self.label_52 = QLabel(self.frame)
        self.label_52.setObjectName(u"label_52")
        self.label_52.setFont(font3)

        self.gridLayout_6.addWidget(self.label_52, 4, 3, 1, 1)

        self.system_platform = QLabel(self.frame)
        self.system_platform.setObjectName(u"system_platform")
        self.system_platform.setFont(font3)

        self.gridLayout_6.addWidget(self.system_platform, 2, 2, 1, 1)


        self.verticalLayout_10.addWidget(self.frame)

        self.stackedWidget.addWidget(self.sysinfo)
        self.clientslist = QWidget()
        self.clientslist.setObjectName(u"clientslist")
        self.verticalLayout_5 = QVBoxLayout(self.clientslist)
        self.verticalLayout_5.setSpacing(10)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.label_59 = QLabel(self.clientslist)
        self.label_59.setObjectName(u"label_59")
        self.label_59.setFont(font4)

        self.verticalLayout_5.addWidget(self.label_59)

        self.tableWidget_4 = QTableWidget(self.clientslist)
        if (self.tableWidget_4.columnCount() < 3):
            self.tableWidget_4.setColumnCount(3)
        __qtablewidgetitem50 = QTableWidgetItem()
        __qtablewidgetitem50.setFont(font3);
        self.tableWidget_4.setHorizontalHeaderItem(0, __qtablewidgetitem50)
        __qtablewidgetitem51 = QTableWidgetItem()
        __qtablewidgetitem51.setFont(font3);
        self.tableWidget_4.setHorizontalHeaderItem(1, __qtablewidgetitem51)
        __qtablewidgetitem52 = QTableWidgetItem()
        __qtablewidgetitem52.setFont(font3);
        self.tableWidget_4.setHorizontalHeaderItem(2, __qtablewidgetitem52)
        self.tableWidget_4.setObjectName(u"tableWidget_4")
        self.tableWidget_4.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.verticalLayout_5.addWidget(self.tableWidget_4)

        self.stackedWidget.addWidget(self.clientslist)

        self.verticalLayout_2.addWidget(self.stackedWidget)


        self.horizontalLayout_8.addWidget(self.center_main)

        self.right_main = QFrame(self.main_body_frame)
        self.right_main.setObjectName(u"right_main")
        self.right_main.setMinimumSize(QSize(0, 200))
        self.right_main.setMaximumSize(QSize(0, 16777215))
        self.right_main.setStyleSheet(u"*{\n"
"background-color:#24374B;\n"
"}")
        self.right_main.setFrameShape(QFrame.NoFrame)
        self.verticalLayout_17 = QVBoxLayout(self.right_main)
        self.verticalLayout_17.setSpacing(0)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.verticalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.treeWidget = QTreeWidget(self.right_main)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setFont(0, font3);
        self.treeWidget.setHeaderItem(__qtreewidgetitem)
        __qtreewidgetitem1 = QTreeWidgetItem(self.treeWidget)
        __qtreewidgetitem1.setFont(0, font3);
        QTreeWidgetItem(__qtreewidgetitem1)
        QTreeWidgetItem(__qtreewidgetitem1)
        QTreeWidgetItem(__qtreewidgetitem1)
        QTreeWidgetItem(__qtreewidgetitem1)
        QTreeWidgetItem(__qtreewidgetitem1)
        QTreeWidgetItem(__qtreewidgetitem1)
        QTreeWidgetItem(__qtreewidgetitem1)
        QTreeWidgetItem(__qtreewidgetitem1)
        QTreeWidgetItem(__qtreewidgetitem1)
        QTreeWidgetItem(__qtreewidgetitem1)
        QTreeWidgetItem(__qtreewidgetitem1)
        QTreeWidgetItem(__qtreewidgetitem1)
        QTreeWidgetItem(__qtreewidgetitem1)
        QTreeWidgetItem(__qtreewidgetitem1)
        QTreeWidgetItem(__qtreewidgetitem1)
        QTreeWidgetItem(__qtreewidgetitem1)
        QTreeWidgetItem(__qtreewidgetitem1)
        QTreeWidgetItem(__qtreewidgetitem1)
        QTreeWidgetItem(__qtreewidgetitem1)
        QTreeWidgetItem(__qtreewidgetitem1)
        QTreeWidgetItem(__qtreewidgetitem1)
        QTreeWidgetItem(__qtreewidgetitem1)
        self.treeWidget.setObjectName(u"treeWidget")

        self.verticalLayout_17.addWidget(self.treeWidget)


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

        self.horizontalLayout_6.addWidget(self.pushButton_3)


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

        self.stackedWidget.setCurrentIndex(3)


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
        self.Sensors.setText("")
        self.Activities.setText("")
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"List Clients", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"System Information", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"Domain", None))
        self.Clientlist.setText("")
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Storage", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Sensors", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Power", None))
        self.CPU.setText("")
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Activities", None))
        self.Domain.setText("")
        self.Sysinfo.setText("")
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"Network", None))
        self.power.setText("")
        self.Storage.setText("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"CPU", None))
        self.Network.setText("")
        self.label_8.setText("")
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
        self.label_39.setText(QCoreApplication.translate("MainWindow", u"Power information", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"Status", None))
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"Time Left", None))
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"Charge", None))
        self.battery_status.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.battery_plugged.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_37.setText(QCoreApplication.translate("MainWindow", u"Plugged In", None))
        self.battery_time_left.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.battery_charge.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.avg_consumed.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_32.setText(QCoreApplication.translate("MainWindow", u"CPU Power", None))
        self.cpu_consume.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.igpu_consume.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_31.setText(QCoreApplication.translate("MainWindow", u"GPU Power", None))
        self.label_40.setText(QCoreApplication.translate("MainWindow", u"IGPU Power", None))
        self.gpu_consume.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_33.setText(QCoreApplication.translate("MainWindow", u"AVG Power", None))
        self.label_57.setText(QCoreApplication.translate("MainWindow", u"Disk Partition", None))
        ___qtablewidgetitem = self.storageTable.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Device", None));
        ___qtablewidgetitem1 = self.storageTable.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Mount Point", None));
        ___qtablewidgetitem2 = self.storageTable.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Drive type", None));
        ___qtablewidgetitem3 = self.storageTable.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"OPTS", None));
        ___qtablewidgetitem4 = self.storageTable.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Max File", None));
        ___qtablewidgetitem5 = self.storageTable.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"Max Path", None));
        ___qtablewidgetitem6 = self.storageTable.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"Total Storage", None));
        ___qtablewidgetitem7 = self.storageTable.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"Free Storage", None));
        ___qtablewidgetitem8 = self.storageTable.horizontalHeaderItem(8)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"Used Storage", None));
        self.label_56.setText(QCoreApplication.translate("MainWindow", u"Activities", None))
        self.activity_search.setInputMask("")
        self.activity_search.setText("")
        self.activity_search.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Search Processes", None))
        self.pushButton_11.setText("")
        ___qtablewidgetitem9 = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"Process ID", None));
        ___qtablewidgetitem10 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"Process Name", None));
        ___qtablewidgetitem11 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"Process Status", None));
        ___qtablewidgetitem12 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("MainWindow", u"Started", None));
        ___qtablewidgetitem13 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("MainWindow", u"Suspend", None));
        ___qtablewidgetitem14 = self.tableWidget.horizontalHeaderItem(5)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("MainWindow", u"Resume", None));
        ___qtablewidgetitem15 = self.tableWidget.horizontalHeaderItem(6)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("MainWindow", u"Terminate", None));
        ___qtablewidgetitem16 = self.tableWidget.horizontalHeaderItem(7)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("MainWindow", u"Kill", None));
        self.pushButton_12.setText(QCoreApplication.translate("MainWindow", u"Suspend", None))
        self.pushButton_13.setText(QCoreApplication.translate("MainWindow", u"Resume", None))
        self.pushButton_14.setText(QCoreApplication.translate("MainWindow", u"Terminate", None))
        self.pushButton_15.setText(QCoreApplication.translate("MainWindow", u"Kill", None))
        self.title_sensor.setText(QCoreApplication.translate("MainWindow", u"Sensors", None))
        ___qtablewidgetitem17 = self.sensors_table.horizontalHeaderItem(0)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("MainWindow", u"Sensor Name", None));
        ___qtablewidgetitem18 = self.sensors_table.horizontalHeaderItem(1)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("MainWindow", u"Min Value", None));
        ___qtablewidgetitem19 = self.sensors_table.horizontalHeaderItem(2)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("MainWindow", u"Current Value", None));
        ___qtablewidgetitem20 = self.sensors_table.horizontalHeaderItem(3)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("MainWindow", u"Max Value", None));
        ___qtablewidgetitem21 = self.sensors_table.horizontalHeaderItem(4)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("MainWindow", u"AVG Value", None));
        self.label_60.setText(QCoreApplication.translate("MainWindow", u"Stats", None))
        ___qtablewidgetitem22 = self.stats_table.horizontalHeaderItem(1)
        ___qtablewidgetitem22.setText(QCoreApplication.translate("MainWindow", u"IS UP", None));
        ___qtablewidgetitem23 = self.stats_table.horizontalHeaderItem(2)
        ___qtablewidgetitem23.setText(QCoreApplication.translate("MainWindow", u"DUPLEX", None));
        ___qtablewidgetitem24 = self.stats_table.horizontalHeaderItem(3)
        ___qtablewidgetitem24.setText(QCoreApplication.translate("MainWindow", u"SPEED", None));
        ___qtablewidgetitem25 = self.stats_table.horizontalHeaderItem(4)
        ___qtablewidgetitem25.setText(QCoreApplication.translate("MainWindow", u"MTU", None));
        self.label_61.setText(QCoreApplication.translate("MainWindow", u"Network IO Counters", None))
        ___qtablewidgetitem26 = self.IO_counters_table.horizontalHeaderItem(0)
        ___qtablewidgetitem26.setText(QCoreApplication.translate("MainWindow", u"Adapter", None));
        ___qtablewidgetitem27 = self.IO_counters_table.horizontalHeaderItem(1)
        ___qtablewidgetitem27.setText(QCoreApplication.translate("MainWindow", u"BYTES SEND", None));
        ___qtablewidgetitem28 = self.IO_counters_table.horizontalHeaderItem(2)
        ___qtablewidgetitem28.setText(QCoreApplication.translate("MainWindow", u"BYTES RECEIVED", None));
        ___qtablewidgetitem29 = self.IO_counters_table.horizontalHeaderItem(3)
        ___qtablewidgetitem29.setText(QCoreApplication.translate("MainWindow", u"PACKETS SEND", None));
        ___qtablewidgetitem30 = self.IO_counters_table.horizontalHeaderItem(4)
        ___qtablewidgetitem30.setText(QCoreApplication.translate("MainWindow", u"PACKETS RECEIVED", None));
        ___qtablewidgetitem31 = self.IO_counters_table.horizontalHeaderItem(5)
        ___qtablewidgetitem31.setText(QCoreApplication.translate("MainWindow", u"ERR IN", None));
        ___qtablewidgetitem32 = self.IO_counters_table.horizontalHeaderItem(6)
        ___qtablewidgetitem32.setText(QCoreApplication.translate("MainWindow", u"ERR OUT", None));
        ___qtablewidgetitem33 = self.IO_counters_table.horizontalHeaderItem(7)
        ___qtablewidgetitem33.setText(QCoreApplication.translate("MainWindow", u"DROP IN", None));
        ___qtablewidgetitem34 = self.IO_counters_table.horizontalHeaderItem(8)
        ___qtablewidgetitem34.setText(QCoreApplication.translate("MainWindow", u"DROP OUT", None));
        self.label_62.setText(QCoreApplication.translate("MainWindow", u"Network Addresses", None))
        ___qtablewidgetitem35 = self.addresses_table.horizontalHeaderItem(0)
        ___qtablewidgetitem35.setText(QCoreApplication.translate("MainWindow", u"Adaptor", None));
        ___qtablewidgetitem36 = self.addresses_table.horizontalHeaderItem(1)
        ___qtablewidgetitem36.setText(QCoreApplication.translate("MainWindow", u"FAMILY", None));
        ___qtablewidgetitem37 = self.addresses_table.horizontalHeaderItem(2)
        ___qtablewidgetitem37.setText(QCoreApplication.translate("MainWindow", u"ADDRESS", None));
        ___qtablewidgetitem38 = self.addresses_table.horizontalHeaderItem(3)
        ___qtablewidgetitem38.setText(QCoreApplication.translate("MainWindow", u"NETMASK", None));
        ___qtablewidgetitem39 = self.addresses_table.horizontalHeaderItem(4)
        ___qtablewidgetitem39.setText(QCoreApplication.translate("MainWindow", u"New Column", None));
        ___qtablewidgetitem40 = self.addresses_table.horizontalHeaderItem(5)
        ___qtablewidgetitem40.setText(QCoreApplication.translate("MainWindow", u"PTP", None));
        self.label_63.setText(QCoreApplication.translate("MainWindow", u"Network Connections", None))
        ___qtablewidgetitem41 = self.connections_table.horizontalHeaderItem(0)
        ___qtablewidgetitem41.setText(QCoreApplication.translate("MainWindow", u"FD", None));
        ___qtablewidgetitem42 = self.connections_table.horizontalHeaderItem(1)
        ___qtablewidgetitem42.setText(QCoreApplication.translate("MainWindow", u"FAMILY", None));
        ___qtablewidgetitem43 = self.connections_table.horizontalHeaderItem(2)
        ___qtablewidgetitem43.setText(QCoreApplication.translate("MainWindow", u"FAMILY", None));
        ___qtablewidgetitem44 = self.connections_table.horizontalHeaderItem(3)
        ___qtablewidgetitem44.setText(QCoreApplication.translate("MainWindow", u"LADDR", None));
        ___qtablewidgetitem45 = self.connections_table.horizontalHeaderItem(4)
        ___qtablewidgetitem45.setText(QCoreApplication.translate("MainWindow", u"RADDR", None));
        ___qtablewidgetitem46 = self.connections_table.horizontalHeaderItem(5)
        ___qtablewidgetitem46.setText(QCoreApplication.translate("MainWindow", u"STATUS", None));
        ___qtablewidgetitem47 = self.connections_table.horizontalHeaderItem(6)
        ___qtablewidgetitem47.setText(QCoreApplication.translate("MainWindow", u"PID", None));
        self.label_42.setText(QCoreApplication.translate("MainWindow", u"System information", None))
        self.system_date.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_51.setText(QCoreApplication.translate("MainWindow", u"Machine", None))
        self.system_version.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_47.setText(QCoreApplication.translate("MainWindow", u"System Date", None))
        self.label_44.setText(QCoreApplication.translate("MainWindow", u"Platform", None))
        self.system_time.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_50.setText(QCoreApplication.translate("MainWindow", u"CPU Model", None))
        self.system_processor.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_45.setText(QCoreApplication.translate("MainWindow", u"Version", None))
        self.system_system.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.system_machine.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_52.setText(QCoreApplication.translate("MainWindow", u"System time", None))
        self.system_platform.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_59.setText(QCoreApplication.translate("MainWindow", u"Clients List", None))
        ___qtablewidgetitem48 = self.tableWidget_4.horizontalHeaderItem(0)
        ___qtablewidgetitem48.setText(QCoreApplication.translate("MainWindow", u"New Column", None));
        ___qtablewidgetitem49 = self.tableWidget_4.horizontalHeaderItem(1)
        ___qtablewidgetitem49.setText(QCoreApplication.translate("MainWindow", u"Client_ID", None));
        ___qtablewidgetitem50 = self.tableWidget_4.horizontalHeaderItem(2)
        ___qtablewidgetitem50.setText(QCoreApplication.translate("MainWindow", u"IP", None));
        ___qtreewidgetitem = self.treeWidget.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"FEAA", None));

        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        ___qtreewidgetitem1 = self.treeWidget.topLevelItem(0)
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("MainWindow", u"Lab 101", None));
        ___qtreewidgetitem2 = ___qtreewidgetitem1.child(0)
        ___qtreewidgetitem2.setText(0, QCoreApplication.translate("MainWindow", u"1", None));
        ___qtreewidgetitem3 = ___qtreewidgetitem1.child(1)
        ___qtreewidgetitem3.setText(0, QCoreApplication.translate("MainWindow", u"2", None));
        ___qtreewidgetitem4 = ___qtreewidgetitem1.child(2)
        ___qtreewidgetitem4.setText(0, QCoreApplication.translate("MainWindow", u"3", None));
        ___qtreewidgetitem5 = ___qtreewidgetitem1.child(3)
        ___qtreewidgetitem5.setText(0, QCoreApplication.translate("MainWindow", u"4", None));
        ___qtreewidgetitem6 = ___qtreewidgetitem1.child(4)
        ___qtreewidgetitem6.setText(0, QCoreApplication.translate("MainWindow", u"5", None));
        ___qtreewidgetitem7 = ___qtreewidgetitem1.child(5)
        ___qtreewidgetitem7.setText(0, QCoreApplication.translate("MainWindow", u"6", None));
        ___qtreewidgetitem8 = ___qtreewidgetitem1.child(6)
        ___qtreewidgetitem8.setText(0, QCoreApplication.translate("MainWindow", u"7", None));
        ___qtreewidgetitem9 = ___qtreewidgetitem1.child(7)
        ___qtreewidgetitem9.setText(0, QCoreApplication.translate("MainWindow", u"8", None));
        ___qtreewidgetitem10 = ___qtreewidgetitem1.child(8)
        ___qtreewidgetitem10.setText(0, QCoreApplication.translate("MainWindow", u"9", None));
        ___qtreewidgetitem11 = ___qtreewidgetitem1.child(9)
        ___qtreewidgetitem11.setText(0, QCoreApplication.translate("MainWindow", u"10", None));
        ___qtreewidgetitem12 = ___qtreewidgetitem1.child(10)
        ___qtreewidgetitem12.setText(0, QCoreApplication.translate("MainWindow", u"11", None));
        ___qtreewidgetitem13 = ___qtreewidgetitem1.child(11)
        ___qtreewidgetitem13.setText(0, QCoreApplication.translate("MainWindow", u"12", None));
        ___qtreewidgetitem14 = ___qtreewidgetitem1.child(12)
        ___qtreewidgetitem14.setText(0, QCoreApplication.translate("MainWindow", u"13", None));
        ___qtreewidgetitem15 = ___qtreewidgetitem1.child(13)
        ___qtreewidgetitem15.setText(0, QCoreApplication.translate("MainWindow", u"14", None));
        ___qtreewidgetitem16 = ___qtreewidgetitem1.child(14)
        ___qtreewidgetitem16.setText(0, QCoreApplication.translate("MainWindow", u"15", None));
        ___qtreewidgetitem17 = ___qtreewidgetitem1.child(15)
        ___qtreewidgetitem17.setText(0, QCoreApplication.translate("MainWindow", u"16", None));
        ___qtreewidgetitem18 = ___qtreewidgetitem1.child(16)
        ___qtreewidgetitem18.setText(0, QCoreApplication.translate("MainWindow", u"17", None));
        ___qtreewidgetitem19 = ___qtreewidgetitem1.child(17)
        ___qtreewidgetitem19.setText(0, QCoreApplication.translate("MainWindow", u"18", None));
        ___qtreewidgetitem20 = ___qtreewidgetitem1.child(18)
        ___qtreewidgetitem20.setText(0, QCoreApplication.translate("MainWindow", u"19", None));
        ___qtreewidgetitem21 = ___qtreewidgetitem1.child(19)
        ___qtreewidgetitem21.setText(0, QCoreApplication.translate("MainWindow", u"20", None));
        ___qtreewidgetitem22 = ___qtreewidgetitem1.child(20)
        ___qtreewidgetitem22.setText(0, QCoreApplication.translate("MainWindow", u"21", None));
        ___qtreewidgetitem23 = ___qtreewidgetitem1.child(21)
        ___qtreewidgetitem23.setText(0, QCoreApplication.translate("MainWindow", u"22", None));
        self.treeWidget.setSortingEnabled(__sortingEnabled)

        self.label.setText(QCoreApplication.translate("MainWindow", u"Version 1.0", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"?", None))
    # retranslateUi

