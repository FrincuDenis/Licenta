import sys

from PySide6.QtGui import QPen, QColor
from PySide6.QtWidgets import QWidget, QApplication, QProgressBar, QLabel, QHBoxLayout, QStyle
from PySide6.QtCore import Qt

from PySide6.QtGui import QWidget, QPainter, QStyleOptionProgress


class RoundProgressBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.value = 0
        self.maximum = 100

    def paintEvent(self, event):
        painter = QPainter(self)
        option = QStyleOptionProgress()
        option.initFrom(self)
        option.progress = self.value
        option.maximum = self.maximum
        option.rect = self.rect()
        option.state |= QStyle.State_Active

        # Adjust these values for size and color
        progress_width = 5
        progress_color = "#673AB7"

        # Draw background circle
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("#ddd"))
        painter.drawEllipse(option.rect)

        # Draw progress segment
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(progress_color))
        painter.drawPie(option.rect, 0, 360 * (self.value / self.maximum))

        # Draw progress bar outline (optional)
        pen = QPen(QColor(progress_color), progress_width)
        painter.setPen(pen)
        painter.drawEllipse(option.rect.adjusted(progress_width // 2, progress_width // 2, -progress_width // 2, -progress_width // 2))

        self.style().drawControl(QStyle.Ctl_ProgressBar, option, painter)


    def set_value(self, value):
        self.value = value
        self.update()

    def set_maximum(self, maximum):
        self.maximum = maximum

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RoundProgressBar()
    window.show()
    sys.exit(app.exec())
