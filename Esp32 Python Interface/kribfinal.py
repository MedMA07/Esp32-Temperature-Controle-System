import serial
import tkinter as tk
from tkinter import ttk
from collections import deque
import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# ===== SERIAL =====
ser = serial.Serial('COM4', 115200, timeout=1)

# ===== DATA =====
data = deque(maxlen=60)

# ===== WINDOW =====
root = tk.Tk()
root.title("Smart Dashboard")
root.geometry("800x600")

# ===== TOP =====
top = tk.Frame(root)
top.pack(side=tk.TOP, fill=tk.X, pady=10)

try:
    img = tk.PhotoImage(file="logo.png")
    lbl_img = tk.Label(top, image=img)
    lbl_img.pack(side=tk.LEFT, padx=10)
except:
    lbl_img = tk.Label(top, text="[LOGO]")
    lbl_img.pack(side=tk.LEFT, padx=10)

title = tk.Label(top, text="Temperature Control", font=("Arial", 16, "bold"))
title.pack(side=tk.LEFT, padx=20)

state_var = tk.StringVar(value="SYSTEM: ---")
state_lbl = tk.Label(top, textvariable=state_var, font=("Arial", 12))
state_lbl.pack(side=tk.RIGHT, padx=20)

# ===== PARAMETERS =====
frame = tk.Frame(root)
frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

T_HIGH = tk.DoubleVar(value=27)
T_LOW  = tk.DoubleVar(value=24)
HYST   = tk.DoubleVar(value=2)

def send_value(name, var):
    ser.write(f"{name}:{var.get()}\n".encode())

tk.Label(frame, text="T_HIGH").grid(row=0, column=0)
tk.Entry(frame, textvariable=T_HIGH, width=6).grid(row=0, column=1)
tk.Button(frame, text="Set", command=lambda: send_value("T_HIGH", T_HIGH)).grid(row=0, column=2)

tk.Label(frame, text="T_LOW").grid(row=1, column=0)
tk.Entry(frame, textvariable=T_LOW, width=6).grid(row=1, column=1)
tk.Button(frame, text="Set", command=lambda: send_value("T_LOW", T_LOW)).grid(row=1, column=2)

tk.Label(frame, text="HYST").grid(row=2, column=0)
tk.Entry(frame, textvariable=HYST, width=6).grid(row=2, column=1)
tk.Button(frame, text="Set", command=lambda: send_value("HYST", HYST)).grid(row=2, column=2)

# ===== GRAPH (TEMP ONLY) =====
fig = Figure(figsize=(6, 3), dpi=100)
ax = fig.add_subplot(111)

ax.set_ylim(0, 50)                     # plage température
ax.get_xaxis().set_visible(False)     # cacher axe X
ax.set_ylabel("Temperature (°C)")
ax.set_title("Temperature", fontsize=14, fontweight="bold")
ax.grid(True, linestyle="--", alpha=0.7)

# ligne plus visible
line, = ax.plot([], [], color="red", linewidth=2, marker='o', markersize=4)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

# ===== UPDATE LOOP =====
def update():
    try:
        line_serial = ser.readline().decode().strip()
    except:
        line_serial = ""

    if line_serial:
        try:
            # format attendu: Temp:24.5 | T_HIGH:27 | T_LOW:24 | HYST:2
            temp = float(line_serial.split("|")[0].split(":")[1])
            data.append(temp)

            line.set_xdata(range(len(data)))
            line.set_ydata(list(data))

            ax.relim()
            ax.autoscale_view()
            canvas.draw()

            # system state
            if "ON" in line_serial:
                state_var.set("SYSTEM: ON")
            else:
                state_var.set("SYSTEM: OFF")

        except:
            pass

    root.after(200, update)

update()
root.mainloop()