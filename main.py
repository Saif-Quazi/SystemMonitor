import tkinter as tk
import pystray as ps
import psutil
import GPUtil

root = tk.Tk()
root.overrideredirect(True)
root.attributes("-topmost", True)
root.geometry("320x80")
root.geometry("+800+400")
root.resizable(False, False)

label = tk.Label(root, text="System Usage Stats")
label.pack(padx=5, pady=5)

cpuLabel = tk.Label(root, text="CPU: 0%")
cpuLabel.pack(side=tk.LEFT, padx=10)

gpuLabel = tk.Label(root, text="GPU: 0%")
gpuLabel.pack(side=tk.LEFT, padx=10)

ramLabel = tk.Label(root, text="RAM: 0%")
ramLabel.pack(side=tk.LEFT, padx=10)

def getUsage():
    CPU = psutil.cpu_percent()
    gpus = GPUtil.getGPUs()
    GPU = gpus[0].load * 100 if gpus else None
    RAM = psutil.virtual_memory().percent
    return [CPU, GPU, RAM]

def updateUsage():
    usageValues = getUsage()
    cpuLabel.config(text=f"CPU: {usageValues[0]}%")
    if usageValues[1] is not None:
        gpuLabel.config(text=f"GPU: {usageValues[1]}%")
    else:
        gpuLabel.config(text="GPU: N/A")
    ramLabel.config(text=f"RAM: {usageValues[2]}%")
    print(usageValues[0], usageValues[1], usageValues[2])
    root.after(1000, updateUsage)

updateUsage()

root.mainloop()
