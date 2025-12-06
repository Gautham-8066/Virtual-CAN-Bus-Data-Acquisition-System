import can
import struct
import matplotlib
matplotlib.use('Qt5Agg') 
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import statistics # Standard library for mean

# 1. SETUP CONNECTION
try:
    bus = can.interface.Bus(channel='vcan0', interface='socketcan')
except OSError:
    print("CRITICAL: vcan0 not found.")
    exit(1)

# 2. CONFIGURATION
max_len = 200 # Show more history
window_size = 20 # How many samples to average (Higher = Smoother but Slower)

# 3. DATA BUFFERS
# Raw Data
raw_rpms = deque([0]*max_len, maxlen=max_len)
raw_speeds = deque([0]*max_len, maxlen=max_len)

# Filtered Data
clean_rpms = deque([0]*max_len, maxlen=max_len)
clean_speeds = deque([0]*max_len, maxlen=max_len)

# 4. SETUP PLOT
fig, (ax1, ax2) = plt.subplots(2, 1)
fig.canvas.manager.set_window_title('Project Stark: Signal Processing')

# Plot 1: RPM
# The 'alpha=0.3' makes the raw line faint and transparent
line_rpm_raw, = ax1.plot(raw_rpms, 'r-', linewidth=1, alpha=0.3, label='Raw Sensor')
line_rpm_clean, = ax1.plot(clean_rpms, 'r-', linewidth=2, label='Filtered')
ax1.set_ylabel('RPM')
ax1.set_ylim(0, 6000)
ax1.legend(loc='upper right')
ax1.grid(True, linestyle='--', alpha=0.5)

# Plot 2: Speed
line_speed_raw, = ax2.plot(raw_speeds, 'c-', linewidth=1, alpha=0.3, label='Raw Sensor')
line_speed_clean, = ax2.plot(clean_speeds, 'c-', linewidth=2, label='Filtered')
ax2.set_ylabel('Speed (km/h)')
ax2.set_ylim(0, 200)
ax2.legend(loc='upper right')
ax2.grid(True, linestyle='--', alpha=0.5)

def get_moving_average(data_deque, new_val):
    # Helper math function
    # 1. Get the last N items (window)
    # 2. Add the new value temporarily to calculate
    # (Simplified for real-time: We just take the mean of the current buffer tail)
    if len(data_deque) < window_size:
        return new_val # Not enough data yet
    
    # Slice the last 'window_size' items
    recent_data = list(data_deque)[-window_size:] 
    return statistics.mean(recent_data)

def read_can():
    while True:
        msg = bus.recv(timeout=0)
        if msg is None: break
        
        if msg.arbitration_id == 0x100:
            unpacked = struct.unpack('>HH', msg.data)
            new_rpm = unpacked[0]
            new_speed = unpacked[1]

            # Store Raw
            raw_rpms.append(new_rpm)
            raw_speeds.append(new_speed)

            # CALC FILTER
            # We calculate the average of the raw buffer's tail
            avg_rpm = get_moving_average(raw_rpms, new_rpm)
            avg_speed = get_moving_average(raw_speeds, new_speed)

            # Store Clean
            clean_rpms.append(avg_rpm)
            clean_speeds.append(avg_speed)

def animate(i):
    read_can()
    
    # Update all 4 lines
    line_rpm_raw.set_ydata(raw_rpms)
    line_rpm_clean.set_ydata(clean_rpms)
    
    line_speed_raw.set_ydata(raw_speeds)
    line_speed_clean.set_ydata(clean_speeds)
    
    return line_rpm_raw, line_rpm_clean, line_speed_raw, line_speed_clean

ani = animation.FuncAnimation(fig, animate, interval=50, blit=True, cache_frame_data=False)
plt.show()
