# System Monitor

A lightweight, always-on-top system monitoring widget for Windows.
Displays CPU, GPU, and RAM usage in real time.

<b>This project does NOT release executables.</b> [Why?](#why-no-executable)

## Quick start (recommended)

1. Install <b>Python 3.10+</b>
2. Download and extract from [releases](https://github.com/Saif-Quazi/SystemMonitor/releases)
3. Open a terminal in the project folder  
4. Run:

```
pip install -r requirements.txt
pythonw main.py
```


## Why no executable?

Unsigned executables are flagged by antivirus software and some browsers.
Running from source avoids those issues and ensures transparency.

## Dependencies

- psutil  
- GPUtil  
- pystray  
- Pillow  
- PySide6  

## Usage

The widget appears at the top of the screen.
Use the system tray icon to access settings or quit the app.

## Author

Made by Saif Quazi  
https://saifq.co
