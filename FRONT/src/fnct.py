import psutil

def battery(self):
    battery = psutil.sensors_battery()
    if not hasattr(psutil, 'sensors_battery'):
        self.ui.battery_status.setText("Platform not supported")
    if battery is None:
        self.ui.battery_status.setText("Does not have battery")
    if battery.power_plugged:
        self.ui.battery_charge.setText(str(round(battery.percent, 2))+"%")
        self.ui.battery_time_left.setText("N/A")
        if battery.percent < 100:
            self.ui.battery_time_left.setText("Charging")
        else:
            self.ui.battery_time_left.setText("Fully Charged")
        self.ui.battery_plugged.setText("Yes")
    else:
        self.ui.battery_charge.setText(str(round(battery.percent, 2))+"%")
        self.ui.battery_time_left.setText(self.secs2hours(battery.secsleft))
        if battery.percent < 100:
            self.ui.battery_status.setText("Discharging")
        else:
            self.ui.battery_status.setText("Fully Charged")
        self.ui.battery_plugged.setText("No")
    self.ui.battery_usage.rpb_setMaximum(100)
    self.ui.battery_usage.rpb_setValue(battery.percent)
    self.ui.battery_usage.rpb_setBarStyle('Hybrid2')
    self.ui.battery_usage.rpb_setLineColor((255,30,99))
    self.ui.battery_usage.rpb_setPieColor((45,74,83))
    self.ui.battery_usage.rpb_setTextColor((255,255,255))
    self.ui.battery_usage.rpb_setInitialPos('West')
    self.ui.battery_usage.rpb_setTextFormat('Percentage')
    self.ui.battery_usage.rpb_setLineWidth(15)
    self.ui.battery_usage.rpb_setPathWidth(15)
    self.ui.battery_usage.rpb_setLineCap('RoundCap')