import tkinter as tk

root = tk.Tk()

root.title("System Monitor")
root.geometry("400x200")

label = tk.Label(root, text="System Usage Stats")
label.pack(padx=25, pady=25)

root.mainloop()
