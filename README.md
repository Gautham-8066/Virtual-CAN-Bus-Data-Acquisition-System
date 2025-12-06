Virtual CAN Bus Data Acquisition System (Digital Twin)
A simulation of an automotive CAN (Controller Area Network) architecture running entirely in software. This project implements a Digital Twin of a vehicle's telemetry system, featuring a simulated Engine Control Unit (ECU) and a real-time Dashboard with Signal Processing.

🚀 Project Overview
In automotive engineering, testing software on real vehicles is dangerous and expensive. This project solves that by emulating the hardware layer.

The Engine: A Python script acting as an ECU, generating telemetry data (RPM, Speed) with realistic physics (gear shifts, acceleration) and simulated sensor noise.

The Network: Uses the Linux Kernel's vcan (Virtual CAN) module to create a virtual twisted-pair copper wire in RAM.

The Dashboard: A real-time plotting tool that listens to the bus, decodes binary packets, and applies a Moving Average Filter to smooth out the simulated sensor noise.

🛠️ Architecture
The system follows a decoupled Producer-Consumer architecture:

[Engine Sim] --(Packets ID 0x100)--> [vcan0 Bus] --(Decode)--> [Dashboard]

Protocol: CAN 2.0A (11-bit Identifier)

Data Frame: ID 0x100, Payload: 4 Bytes

Encoding: Big-Endian Unsigned Short (>HH)

⚡ Prerequisites
OS: Linux (Native or WSL2)

Python: 3.8+

System Tools: can-utils, net-tools

📦 Installation
Clone the Repository

Bash

git clone https://github.com/YOUR_USERNAME/Virtual-CAN-DAQ.git
cd Virtual-CAN-DAQ
Set up Virtual Environment

Bash

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Initialize the Virtual CAN Interface Note: This resets the simulation network.

Bash

sudo modprobe vcan
sudo ip link add dev vcan0 type vcan
sudo ip link set up vcan0
🖥️ Usage
You need two terminal windows. Ensure the virtual environment is active in both (source venv/bin/activate).

Terminal 1: Start the Engine This script simulates a 5-speed transmission car on a track.

Bash

python3 src/engine_sim.py
Terminal 2: Start the Dashboard This visualizes the data. (For WSL2 users, we force the XCB backend).

Bash

export QT_QPA_PLATFORM=xcb
python3 src/dashboard.py
🧠 Technical Highlights
1. Data Serialization
We compress human-readable values into binary for bandwidth efficiency, mimicking real embedded systems.

Python

# Packing 3000 RPM and 100 km/h into 4 bytes
data = struct.pack('>HH', 3000, 100) 
# Result: b'\x0b\xb8\x00\x64'
2. Signal Processing
The simulation intentionally injects "Gaussian Noise" into the sensors to mimic real-world interference. The Dashboard implements a Moving Average Filter to recover the clean signal.

Raw Data: Faint lines (High frequency jitter)

Filtered Data: Bold lines (Smooth trend)

Python

# Moving Average Logic
recent_data = list(data_deque)[-window_size:] 
smooth_val = statistics.mean(recent_data)
🔮 Future Improvements
[ ] Implement "Error Frames" to simulate engine overheating.

[ ] Hardware integration: Porting the "Engine" code to an ESP32 microcontroller with a physical MCP2515 CAN Transceiver.

[ ] Database Support: Logging the session data to a CSV or SQL database for post-run analysis.

Step 4: Final Touch (Optional)
Take a screenshot of your running dashboard (the one with the two graphs). Save it as demo.png in your folder and add this line under the "Project Overview" in the README:

![Dashboard Demo](demo.png)
