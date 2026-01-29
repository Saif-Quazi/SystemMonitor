import threading
import tkinter as tk

import GPUtil
import psutil
import pystray as ps
from PIL import Image

widgetW = 250
widgetH = 30
updateInterval = 1000
iconLow = "icons/logo-low.ico"
iconMedium = "icons/logo-medium.ico"
iconHigh = "icons/logo-high.ico"

def getUsage():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    gpus = GPUtil.getGPUs()
    gpu = int(gpus[0].load * 100) if gpus else None
    return cpu, ram, gpu

def createTrayIcon(onQuit):
    return ps.Icon(
        "SystemMonitor",
        Image.open(iconLow),
        "System Monitor",
        menu=ps.Menu(ps.MenuItem("Quit", onQuit)),
    )

def updateTrayIcon(icon, cpu):
    if cpu > 80:
        icon.icon = Image.open(iconHigh)
    elif cpu > 50:
        icon.icon = Image.open(iconMedium)
    else:
        icon.icon = Image.open(iconLow)
    icon.title = f"CPU Usage: {cpu}%"

root = tk.Tk()
root.overrideredirect(True)
root.attributes("-topmost", True)

screenWidth = root.winfo_screenwidth()
x = (screenWidth // 2) - (widgetW // 2)
root.geometry(f"{widgetW}x{widgetH}+{x}+0")
root.resizable(False, False)

container = tk.Frame(root)
container.pack(padx=2, pady=2)

statsFrame = tk.Frame(container)
statsFrame.pack(anchor="w", pady=(4, 0))

cpuLabel = tk.Label(statsFrame, text="CPU: --%")
cpuLabel.pack(side=tk.LEFT, padx=(0, 10))

gpuLabel = tk.Label(statsFrame, text="GPU: --%")
gpuLabel.pack(side=tk.LEFT, padx=(0, 10))

ramLabel = tk.Label(statsFrame, text="RAM: --%")
ramLabel.pack(side=tk.LEFT)

def update():
    cpu, ram, gpu = getUsage()
    cpuLabel.config(text=f"CPU: {cpu}%")
    ramLabel.config(text=f"RAM: {ram}%")
    gpuLabel.config(text=f"GPU: {gpu}%" if gpu is not None else "GPU: N/A")
    updateTrayIcon(trayIcon, cpu)
    root.after(updateInterval, update)

def quitApp(icon=None, item=None):
    trayIcon.stop()
    root.quit()

trayIcon = createTrayIcon(quitApp)
threading.Thread(target=trayIcon.run, daemon=True).start()

update()
root.mainloop()

