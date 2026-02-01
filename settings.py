import json
import os
import sys
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QDialog, QFrame, QComboBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


PROFILE_FILE = "profile.json"


def get_dark_palette():
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(34, 34, 34))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(34, 34, 34))
    palette.setColor(QPalette.AlternateBase, QColor(34, 34, 34))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(34, 34, 34))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(0, 150, 136))
    palette.setColor(QPalette.Highlight, QColor(0, 150, 136))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    return palette


def get_dark_styles():
    return f"""
    QCheckBox::indicator {{
        width: 16px;
        height: 16px;
        border: 1px solid #888;
        background: #404040;
        border-radius: 4px;
    }}
    QCheckBox::indicator:checked {{
        background: #009688;
        border: 1px solid #009688;
    }}
    QCheckBox {{
        color: white;
        font-size: 12px;
    }}
    QComboBox {{
        border: 1px solid #888;
        border-radius: 6px;
        padding: 4px 8px;
        background: #404040;
        color: white;
        font-size: 14px;
    }}
    QComboBox::drop-down {{
        subcontrol-origin: padding;
        subcontrol-position: center right;
        width: 30px;
        border-left: 1px solid #888;
        border-radius: 0px;
    }}
    QComboBox::down-arrow {{
        image: url({resource_path('assets/icons/arrow.svg')});
        width: 12px;
        height: 12px;
    }}
    QComboBox QAbstractItemView {{
        background: #404040;
        color: white;
        border: 1px solid #888;
        border-radius: 4px;
        selection-background-color: #009688;
    }}
    QPushButton {{
        background-color: #2a2a2a;
        color: white;
        border: 1px solid #888;
        padding: 8px 16px;
        border-radius: 6px;
        font-size: 14px;
    }}
    QPushButton:hover {{
        background-color: #404040;
    }}
    QPushButton:checked {{
        background-color: #00796b;
        color: white;
        border: 1px solid #00796b;
    }}
    QPushButton:checked:hover {{
        background-color: #005a4f;
    }}
    QPushButton:disabled {{
        background-color: #666;
        color: #999;
    }}
    QLabel {{
        color: white;
    }}
    QFrame {{
        border: none;
    }}
    """

def loadProfile() -> dict | None:
    if not os.path.exists(PROFILE_FILE):
        return None
    try:
        with open(PROFILE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("profile")
    except Exception:
        return None

def saveProfile(profile: dict) -> None:
    with open(PROFILE_FILE, "w", encoding="utf-8") as f:
        json.dump({"profile": profile}, f, indent=4)

def getDefaultProfile() -> dict:
    return {
        "name": "default",
        "showValues": [True, True, True],  # cpu, gpu, ram
        "bgColor": "#1e1e1e",
        "fgColor": "#ffffff",
        "font": "Roboto",
        "fontSize": 12
    }

def showSettingsWindow(currentProfile: dict, onSave: callable, parent=None):
    win = QDialog(parent)
    win.setWindowTitle("System Monitor | Widget Settings")
    win.setFixedSize(300, 500)

    screen = QApplication.primaryScreen().geometry()
    win.move((screen.width() - 300) // 2, (screen.height() - 500) // 2)

    win.setPalette(get_dark_palette())
    win.setStyleSheet(get_dark_styles())

    layout = QVBoxLayout()
    layout.setSpacing(20)
    layout.setContentsMargins(15, 20, 15, 20)

    title = QLabel("Widget Settings")
    title.setStyleSheet("font-size: 24px; font-weight: bold;")
    layout.addWidget(title)

    layout.addStretch()

    frame = QFrame()
    frame.setFrameStyle(QFrame.Box)
    frame_layout = QVBoxLayout()
    frame_layout.setSpacing(20)

    varCpu = QPushButton("SHOW CPU USAGE")
    varCpu.setCheckable(True)
    varCpu.setChecked(currentProfile["showValues"][0])
    varCpu.setFixedWidth(243)

    varGpu = QPushButton("SHOW GPU USAGE")
    varGpu.setCheckable(True)
    varGpu.setChecked(currentProfile["showValues"][1])
    varGpu.setFixedWidth(243)

    varRam = QPushButton("SHOW RAM USAGE")
    varRam.setCheckable(True)
    varRam.setChecked(currentProfile["showValues"][2])
    varRam.setFixedWidth(243)

    cpu_layout = QHBoxLayout()
    cpu_layout.addStretch()
    cpu_layout.addWidget(varCpu)
    cpu_layout.addStretch()
    frame_layout.addLayout(cpu_layout)

    gpu_layout = QHBoxLayout()
    gpu_layout.addStretch()
    gpu_layout.addWidget(varGpu)
    gpu_layout.addStretch()
    frame_layout.addLayout(gpu_layout)

    ram_layout = QHBoxLayout()
    ram_layout.addStretch()
    ram_layout.addWidget(varRam)
    ram_layout.addStretch()
    frame_layout.addLayout(ram_layout)

    # Spacer line
    spacer_layout = QHBoxLayout()
    spacer_layout.addStretch(10)
    spacer_line = QFrame()
    spacer_line.setFrameStyle(QFrame.HLine)
    spacer_line.setFixedHeight(4)
    spacer_line.setStyleSheet("QFrame { color: #ccc; }")
    spacer_layout.addWidget(spacer_line, 80)
    spacer_layout.addStretch(10)
    frame_layout.addLayout(spacer_layout)

    label_layout = QHBoxLayout()
    label_layout.addStretch()
    size_label = QLabel("Font size:")
    size_label.setStyleSheet("font-size: 16px;")
    label_layout.addWidget(size_label)
    label_layout.addStretch()
    frame_layout.addLayout(label_layout)

    dropdown_layout = QHBoxLayout()
    dropdown_layout.addStretch()
    varSize = QComboBox()
    varSize.addItems(["8", "10", "12", "14", "16"])
    varSize.setCurrentText(str(currentProfile["fontSize"]))
    varSize.setFixedWidth(243)
    dropdown_layout.addWidget(varSize)
    dropdown_layout.addStretch()
    frame_layout.addLayout(dropdown_layout)

    frame.setLayout(frame_layout)
    layout.addWidget(frame)

    layout.addStretch()

    def saveAndApply():
        newProfile = currentProfile.copy()
        newProfile["showValues"] = [varCpu.isChecked(), varGpu.isChecked(), varRam.isChecked()]
        newProfile["fontSize"] = int(varSize.currentText())
        saveProfile(newProfile)
        onSave(newProfile)

    save_button = QPushButton("Save")
    save_button.setFixedWidth(80)
    save_button.clicked.connect(saveAndApply)

    close_button = QPushButton("Close")
    close_button.setFixedWidth(80)
    close_button.setStyleSheet("background-color: #444; color: white; border: none; padding: 8px 16px; border-radius: 6px; font-size: 12px;")
    close_button.clicked.connect(win.reject)

    buttons_layout = QHBoxLayout()
    buttons_layout.addStretch()
    buttons_layout.addWidget(close_button)
    buttons_layout.addWidget(save_button)
    layout.addLayout(buttons_layout)

    def update_save_button():
        enabled = varCpu.isChecked() or varGpu.isChecked() or varRam.isChecked()
        save_button.setEnabled(enabled)
        if enabled:
            save_button.setStyleSheet("background-color: #009688; color: white; border: none; padding: 8px 16px; border-radius: 6px; font-size: 12px;")
        else:
            save_button.setStyleSheet("background-color: #666; color: #999; border: none; padding: 8px 16px; border-radius: 6px; font-size: 12px;")

    varCpu.toggled.connect(update_save_button)
    varGpu.toggled.connect(update_save_button)
    varRam.toggled.connect(update_save_button)
    update_save_button()

    win.setLayout(layout)
    win.exec()