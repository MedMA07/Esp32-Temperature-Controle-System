import serial
import tkinter as tk
from tkinter import ttk
from collections import deque
import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# ===== الإعدادات الأساسية =====
try:
    ser = serial.Serial('COM4', 115200, timeout=1)
except:
    ser = None
    print("Error: ESP32 not found.")

data = deque(maxlen=100)

root = tk.Tk()
root.title("Thermal Control Dashboard")
root.geometry("1100x800")
root.configure(bg="#1a1a2e")

# ===== HEADER (العنوان العلوي) =====
header = tk.Frame(root, bg="#16213e", height=50)
header.pack(side=tk.TOP, fill=tk.X)

# اللوجو
try:
    img = tk.PhotoImage(file="logo.png").subsample(3,3)
    lbl_img = tk.Label(header, image=img, bg="#16213e")
    lbl_img.pack(side=tk.LEFT, padx=10)
except:
    pass

# عنوان المشروع
tk.Label(header, text="SYSTEM MONITORING Temp esp32 v1.0", fg="#e94560", 
         bg="#16213e", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=10)

# حالة النظام (بشكل بارز)
state_var = tk.StringVar(value="WAITING...")
state_lbl = tk.Label(header, textvariable=state_var, font=("Consolas", 16, "bold"), 
                     bg="#16213e", fg="#ffffff", padx=20)
state_lbl.pack(side=tk.RIGHT, padx=20)

# ===== MAIN CONTENT =====
main_container = tk.Frame(root, bg="#1a1a2e")
main_container.pack(fill=tk.BOTH, expand=True)

# 1. Left Panel (Control - 25%)
control_panel = tk.Frame(main_container, bg="#16213e", width=250, padx=15, pady=20)
control_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

T_HIGH = tk.DoubleVar(value=27.0)
T_LOW  = tk.DoubleVar(value=24.0)
HYST   = tk.DoubleVar(value=2.0)

def send_v(n, v):
    if ser: ser.write(f"{n}:{v.get()}\n".encode()); update_limit_lines()

def add_ui(label, var, name, color):
    tk.Label(control_panel, text=label, fg="#95a5a6", bg="#16213e", font=("Arial", 8)).pack(anchor="w", pady=(10,0))
    ent = tk.Entry(control_panel, textvariable=var, font=("Consolas", 14), bg="#0f3460", fg="white", borderwidth=0)
    ent.pack(fill=tk.X, pady=5)
    btn = tk.Button(control_panel, text=f"SET {name}", bg=color, fg="white", font=("Arial", 9, "bold"), 
                    relief=tk.FLAT, cursor="hand2", command=lambda: send_v(name, var))
    btn.pack(fill=tk.X, pady=(0,10))

add_ui("UPPER LIMIT", T_HIGH, "T_HIGH", "#e94560")
add_ui("LOWER LIMIT", T_LOW, "T_LOW", "#4ecc71")
add_ui("HYSTERESIS", HYST, "HYST", "#533483")

# 2. Right Panel (Graph - 75%)
graph_panel = tk.Frame(main_container, bg="#1a1a2e")
graph_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

fig = Figure(figsize=(10, 8), facecolor='#1a1a2e')
ax = fig.add_subplot(111)
ax.set_facecolor('#1a1a2e')

ax.tick_params(colors='white', labelsize=9)
ax.set_ylim(15, 45)
ax.set_yticks(range(15, 46, 2))
ax.grid(True, color='#16213e', linestyle='--', linewidth=0.5)

line, = ax.plot([], [], color="#00d4ff", linewidth=3, label="Temperature")
hline_h = ax.axhline(T_HIGH.get(), color='#e94560', linestyle='--', linewidth=1.5, label="High Limit")
hline_l = ax.axhline(T_LOW.get(), color='#4ecc71', linestyle='--', linewidth=1.5, label="Low Limit")

ax.legend(facecolor='#16213e', labelcolor='white', loc='upper right', fontsize='small')

canvas = FigureCanvasTkAgg(fig, master=graph_panel)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def update_limit_lines():
    hline_h.set_ydata([T_HIGH.get(), T_HIGH.get()])
    hline_l.set_ydata([T_LOW.get(), T_LOW.get()])
    canvas.draw()

# ===== دالة التحديث ومطابقة حالة النظام =====
def update():
    try:
        if ser and ser.in_waiting > 0:
            line_s = ser.readline().decode().strip()
            if "Temp:" in line_s:
                # استخراج درجة الحرارة
                val = float(line_s.split("|")[0].split(":")[1].strip())
                data.append(val)
                line.set_data(range(len(data)), list(data))
                
                # --- منطق حالة النظام (State Logic) ---
                # نطبق نفس شروط الـ ESP32 لضمان التطابق
                high_threshold = T_HIGH.get() + HYST.get()
                low_threshold = T_LOW.get() - HYST.get()

                if val >= high_threshold:
                    state_var.set("HEATER: OFF")
                    state_lbl.config(fg="#e94560") # أحمر عند الوصول للحد الأقصى
                elif val <= low_threshold:
                    state_var.set("HEATER: ON")
                    state_lbl.config(fg="#4ecc71") # أخضر عند الحاجة للتسخين
                
                ax.relim()
                ax.autoscale_view(scalex=True, scaley=False)
                canvas.draw()
    except Exception as e:
        print(f"Error: {e}")
        
    root.after(100, update)

update()
root.mainloop()
