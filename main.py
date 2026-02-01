import sys
import threading
import GPUtil
import psutil
import pystray as ps
from PIL import Image
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QCheckBox, QSlider, QPushButton, QDialog, QFrame
from PySide6.QtGui import QPainter, QPen, QBrush, QColor, QFont, QIcon
from PySide6.QtCore import Qt, QTimer, QPoint, QRect, QSize

from pystray import Icon as TrayIcon

from settings import (
    loadProfile,
    saveProfile,
    getDefaultProfile,
    showSettingsWindow,
    resource_path
)

WIDGET_H = 40
UPDATE_MS = 1000

LABEL_WIDTH = 100
SIDE_PADDING = 20

ICON_LOW    = resource_path("assets/logo-low.ico")
ICON_MEDIUM = resource_path("assets/logo-medium.ico")
ICON_HIGH   = resource_path("assets/logo-high.ico")


def getUsage():
    cpu = psutil.cpu_percent(interval=None)
    ram = psutil.virtual_memory().percent
    gpus = GPUtil.getGPUs()
    gpu = int(gpus[0].load * 100) if gpus else None
    return cpu, ram, gpu


def updateTrayIcon(tray: TrayIcon, cpu: float):
    if cpu > 80:
        tray.icon = Image.open(ICON_HIGH)
    elif cpu > 50:
        tray.icon = Image.open(ICON_MEDIUM)
    else:
        tray.icon = Image.open(ICON_LOW)
    tray.title = f"CPU: {int(cpu)}%"


def createTrayIcon(onOpenSettings, onQuit) -> TrayIcon:
    return ps.Icon(
        "sysmon",
        Image.open(ICON_LOW),
        "System Monitor",
        menu=ps.Menu(
            ps.MenuItem("Settings", onOpenSettings),
            ps.MenuItem("Quit", onQuit)
        )
    )


class WidgetWindow(QWidget):
    def __init__(self, profile: dict, tray: TrayIcon | None = None):
        super().__init__()
        self.profile = profile
        self.tray = tray
        self.cpu = 0
        self.ram = 0
        self.gpu = None
        self.open_settings = False
        self.quit_app = False

        self._update_size()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.8)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        screen = QApplication.primaryScreen().geometry()
        self._center_on_screen(screen)

        self.current_geom = self.geometry()
        self.target_geom = self.geometry()
        self.anim_timer = QTimer(self)
        self.anim_timer.setInterval(16)  # ~60fps
        self.anim_timer.timeout.connect(self._anim_step)
        self.smooth_factor = 0.1

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update)
        self.timer.start(UPDATE_MS)

    def _update_size(self):
        showCpu, showGpu, showRam = self.profile.get("showValues", [True, True, True])
        num_shown = sum([showCpu, showGpu, showRam])
        fontSize = self.profile.get("fontSize", 12)
        gap = int(fontSize * 0.8)
        if num_shown == 0:
            width = 64
        else:
            width = SIDE_PADDING * 2 + LABEL_WIDTH * num_shown + gap * (num_shown - 1)
        self.setFixedSize(width, WIDGET_H)

    def _center_on_screen(self, screen):
        x = (screen.width() - self.width()) // 2
        self.move(x, 0)

    def _anim_step(self):
        diff_x = self.target_geom.x() - self.current_geom.x()
        diff_y = self.target_geom.y() - self.current_geom.y()
        diff_w = self.target_geom.width() - self.current_geom.width()
        diff_h = self.target_geom.height() - self.current_geom.height()

        if abs(diff_x) < 1 and abs(diff_y) < 1 and abs(diff_w) < 1 and abs(diff_h) < 1:
            self.current_geom = QRect(self.target_geom)
            self.setGeometry(self.current_geom)
            self.anim_timer.stop()
            self.update()
        else:
            self.current_geom.setX(int(self.current_geom.x() + diff_x * self.smooth_factor))
            self.current_geom.setY(int(self.current_geom.y() + diff_y * self.smooth_factor))
            self.current_geom.setWidth(int(self.current_geom.width() + diff_w * self.smooth_factor))
            self.current_geom.setHeight(int(self.current_geom.height() + diff_h * self.smooth_factor))
            self.setGeometry(self.current_geom)
            self.update()

    def _update(self):
        try:
            self.cpu, self.ram, self.gpu = getUsage()
            if self.tray:
                updateTrayIcon(self.tray, self.cpu)
            self.update()
        except Exception:
            pass

        if self.open_settings:
            self.open_settings = False
            showSettingsWindow(
                currentProfile=self.profile,
                onSave=self.refresh,
                parent=None
            )

        if self.quit_app:
            self.quit_app = False
            if self.tray:
                self.tray.stop()
            QApplication.quit()

    def refresh(self, newProfile: dict):
        old_profile = self.profile
        self.profile = newProfile
        self._update_size()
        screen = QApplication.primaryScreen().geometry()
        new_x = (screen.width() - self.width()) // 2
        new_y = self.y()
        self.target_geom = QRect(new_x, new_y, self.width(), self.height())

        if self.current_geom != self.target_geom:
            if not self.anim_timer.isActive():
                self.anim_timer.start()
        else:
            self.update()
        self.raise_()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width = self.width()
        bg_color = QColor(self.profile.get("bgColor", "#1e1e1e"))
        bg_color.setAlpha(225)
        painter.setBrush(QBrush(bg_color))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(3, 3, width - 6, WIDGET_H - 6, 16, 16)

        fg_color = QColor(self.profile.get("fgColor", "#ffffff"))
        painter.setPen(QPen(fg_color))
        font = QFont(self.profile.get("font", "Roboto"), self.profile.get("fontSize", 12))
        painter.setFont(font) 

        showCpu, showGpu, showRam = self.profile.get("showValues", [True, True, True])
        labels = []
        if showCpu:
            labels.append(f"CPU: {int(self.cpu)}%")
        if showGpu:
            txt = f"GPU: {self.gpu}%" if self.gpu is not None else "GPU: —"
            labels.append(txt)
        if showRam:
            labels.append(f"RAM: {int(self.ram)}%")

        num_shown = len(labels)
        if num_shown == 0:
            return

        inner_width = width - SIDE_PADDING * 2
        fontSize = self.profile.get("fontSize", 12)
        gap = int(fontSize * 1)
        labels_span = LABEL_WIDTH * num_shown + gap * (num_shown - 1)
        start_x = SIDE_PADDING + (inner_width - labels_span) / 2

        x = start_x
        for text in labels:
            rect = QRect(int(x), 3, LABEL_WIDTH, WIDGET_H - 6)
            painter.drawText(rect, Qt.AlignCenter, text)
            x += LABEL_WIDTH + gap


def run():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    profile = loadProfile()

    if profile is None:
        profile = getDefaultProfile()
        saveProfile(profile)

    tray = None

    def openSettings(*_):
        widget.open_settings = True

    def quitApp(*_):
        widget.quit_app = True

    tray = createTrayIcon(openSettings, quitApp)
    threading.Thread(target=tray.run, daemon=True).start()

    widget = WidgetWindow(profile, tray)
    widget.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    run()