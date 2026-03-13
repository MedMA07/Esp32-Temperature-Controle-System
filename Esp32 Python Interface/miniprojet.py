import serial
import tkinter as tk
from collections import deque
import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.ticker as ticker

# ===== SERIAL =====
ser = serial.Serial('COM4', 115200, timeout=1)

# ===== DATA =====
data = deque(maxlen=100)

# ===== WINDOW =====
root = tk.Tk()
root.title("Smart Dashboard")
root.geometry("900x650")

# ===== TOP =====
top = tk.Frame(root)
top.pack(side=tk.TOP, fill=tk.X, pady=8)

title = tk.Label(top, text="Temperature Control", font=("Arial", 16, "bold"))
title.pack()

state_var = tk.StringVar(value="SYSTEM: ---")
state_lbl = tk.Label(top, textvariable=state_var, font=("Arial", 12))
state_lbl.pack()

# ===== PARAMETERS FRAME =====
frame = tk.LabelFrame(root, text="Parameters", padx=10, pady=10)
frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

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

# ===== GRAPH (Y de 0 à 32°C) =====
graph_frame = tk.Frame(root)
graph_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=5, pady=5)

fig = Figure(figsize=(7,4), dpi=120)
ax = fig.add_subplot(111)

ax.set_ylim(0, 32)  # <-- ici axe Y limité à 0-32
ax.set_ylabel("Temperature (°C)")
ax.set_title("Temperature (real time)", fontsize=14, fontweight="bold")

# grid principal
ax.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)

# graduation axe Y précise
ax.yaxis.set_major_locator(ticker.MultipleLocator(1))   # chaque 1°C
ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.5))  # mini grid
ax.grid(True, which='minor', linestyle=':', linewidth=0.4, alpha=0.5)

# ligne
line, = ax.plot([], [], color="red", linewidth=2, marker='o', markersize=4)

canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# ===== UPDATE LOOP =====
def update():
    try:
        line_serial = ser.readline().decode().strip()
    except:
        line_serial = ""

    if line_serial:
        try:
            temp = float(line_serial.split("|")[0].split(":")[1])
            data.append(temp)

            line.set_xdata(range(len(data)))
            line.set_ydata(list(data))

            ax.relim()
            ax.autoscale_view()
            canvas.draw()

            if "ON" in line_serial:
                state_var.set("SYSTEM: ON")
            else:
                state_var.set("SYSTEM: OFF")

        except:
            pass

    root.after(200, update)

update()
root.mainloop()