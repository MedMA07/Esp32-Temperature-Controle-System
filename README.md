# 🌡️ Smart ESP32 Temperature Control System

A modular temperature regulation system using an **ESP32**. It implements **Hysteresis Control** to maintain stable thermal conditions, featuring a triple-interface monitoring system (OLED, Web, and Python).

<p align="center">
  <img src="Assets/logo.png" alt="Project Logo" width="250"/>
</p>

## 📁 Project Structure
The repository is organized as follows:
- `/Assets/`: Contains project logo and circuit diagrams.
- `/Shema sur Proteus/`: Contains the simulation file and schematic of the circuit.
- `/Esp32 Pyhton interface/`: Contains `miniprojet.py` for real-time monitoring.
- `/Esp32Temp ino/`: Contains `Esp32Temp.ino` for the hardware control logic.

## 🚀 Features
- **Hysteresis Regulation:** Precise On/Off control between $T_{low}$ and $T_{high}$.
- **Multi-Platform Monitoring:**
  - **Local:** SSD1306 OLED display with menu navigation.
  - **Web:** Embedded Web Server (WiFi) for remote parameter tuning.
  - **PC:** Real-time Python GUI (Tkinter & Matplotlib).

## 📋 Pinout Configuration
| Component | ESP32 GPIO | Function |
| :--- | :--- | :--- |
| NTC Sensor | GPIO 34 | Analog Input |
| Heater Control | GPIO 15 | ON/OFF Output |
| I2C (SDA/SCL) | GPIO 21 / 22 | OLED Communication |
| Buttons | 32, 33, 25, 26 | Menu / Plus / Minus / Select |

<p align="center">
  <img src="Assets/circuit.png" alt="Circuit Diagram" width="700"/>
</p>
## ⚙️ Getting Started
To run the Python interface on your computer, execute the following commands in your terminal:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the interface
python "Esp32 Python Interface/miniprojet.py"
```

## ⚙️ Software & Dependencies
### Firmware (Arduino IDE)
- `Adafruit_SSD1306` & `Adafruit_GFX`
- `WiFi.h`, `WebServer.h`, `Wire.h`

### PC Dashboard (Python)
- `pyserial`: Serial communication.
- `matplotlib`: Real-time graphing.
- `tkinter`: Graphical interface.

## 💡 Technical Specs
- **Sampling Frequency:** 5 Hz (200ms loop delay).
- **Communication:** 115200 baud.
- **Power:** ~0.83W heating power @ 5V.

---

---
## 📬 Connect with me

<p align="left">
  <a href="https://github.com/MedMA07" target="_blank">
    <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" />
  </a>
  <a href="https://linktr.ee/el.amine.m" target="_blank">
    <img src="https://img.shields.io/badge/Linktree-39E09B?style=for-the-badge&logo=linktree&logoColor=white" alt="Linktree" />
  </a>
  <a href="https://www.facebook.com/el.aminem07/" target="_blank">
    <img src="https://img.shields.io/badge/Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white" alt="Facebook" />
  </a>
  <a href="https://www.instagram.com/el.amine.m/" target="_blank">
    <img src="https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white" alt="Instagram" />
  </a>
  <a href="https://www.snapchat.com/@med_ma7" target="_blank">
    <img src="https://img.shields.io/badge/Snapchat-FFFC00?style=for-the-badge&logo=snapchat&logoColor=black" alt="Snapchat" />
  </a>
</p>
*Developed as a comprehensive project for Embedded Systems & IoT monitoring.*
