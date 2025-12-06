# 🏎️ Virtual CAN Bus Data Acquisition System (Digital Twin)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20WSL2-orange)
![Protocol](https://img.shields.io/badge/Protocol-CAN%202.0A-green)

A simulation of an automotive **CAN (Controller Area Network)** architecture running entirely in software. This project implements a **Digital Twin** of a vehicle's telemetry system, featuring a simulated Engine Control Unit (ECU) and a real-time Dashboard with Signal Processing.Recognizing that real-world sensor data is never clean, we intentionally injected random noise into the simulation to mimic physical interference. The dashboard then processes this raw, jittery stream through a Moving Average Filter to recover and visualize a smooth, accurate signal.
<img width="812" height="533" alt="Screenshot from 2025-12-06 16-18-33" src="https://github.com/user-attachments/assets/bb25bcc8-b706-48cb-9c72-194b9174e4a6" />

<img width="634" height="529" alt="Screenshot from 2025-12-06 16-19-00" src="https://github.com/user-attachments/assets/c1259380-447d-46b0-a3ed-3ac8ae729756" />

## Project Overview

In automotive engineering, testing software on real vehicles is dangerous and expensive. This project solves that by emulating the hardware layer in Linux RAM.

* **The Engine:** A Python script acting as an ECU, generating telemetry data (RPM, Speed) with realistic physics (gear shifts, acceleration) and simulated sensor noise.
* **The Network:** Uses the Linux Kernel's `vcan` (Virtual CAN) module to create a virtual twisted-pair copper wire.
* **The Dashboard:** A real-time plotting tool that listens to the bus, decodes binary packets, and applies a **Moving Average Filter** to smooth out the simulated sensor noise.

## 🛠️ Architecture

The system follows a decoupled **Producer-Consumer** architecture:

```mermaid
graph LR
    A[Engine Simulator] -- CAN Frame (ID 0x100) --> B((vcan0 Bus))
    B -- Raw Binary --> C[Dashboard DAQ]
    C -- Filtered Data --> D[Real-time Graph]
