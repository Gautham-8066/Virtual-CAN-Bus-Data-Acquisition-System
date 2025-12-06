import can
import time
import struct
import random

# CONNECT
bus = can.interface.Bus(channel='vcan0', interface='socketcan')

def send_telemetry(rpm, speed):
    # Add the "Noise" we developed earlier
    r_noise = rpm + random.randint(-50, 50)
    s_noise = speed + random.uniform(-1, 1)
    
    # Pack and Fire
    data = struct.pack('>HH', int(r_noise), int(s_noise))
    msg = can.Message(arbitration_id=0x100, data=data, is_extended_id=False)
    bus.send(msg)

def run_track_test():
    print("ENGINE: Track Mode Engaged. 5-Speed Transmission active.")
    
    # CONFIGURATION
    gear = 1
    rpm = 900 # Idle
    speed = 0
    # Gear Ratios (How much speed you get per 1 RPM)
    ratios = [0, 0.010, 0.016, 0.023, 0.032, 0.045] 
    
    while True:
        # 1. PHYSICS: The engine revs up
        rpm += random.randint(60, 80) 
        
        # 2. MATH: Speed is strictly defined by Gear Ratio
        speed = rpm * ratios[gear]
        
        # 3. TRANSMISSION LOGIC (The State Machine)
        if rpm > 5500: # Redline hit!
            if gear < 5:
                print(f"  -> SHIFTING to Gear {gear+1}...")
                gear += 1
                # CRITICAL: Speed stays same, RPM drops to match new gear
                # New RPM = Current Speed / New Ratio
                rpm = int(speed / ratios[gear])
            else:
                # We are in Top Gear, bounce off the limiter
                rpm = 5400 

        # 4. RESET (Simulate coming to a stop at the end of the straight)
        if speed > 220:
            print("  << BRAKING ZONE >>")
            # Rapid deceleration loop
            while speed > 10:
                speed -= 3
                # Calculate RPM based on current gear
                rpm = int(speed / ratios[gear])
                
                # Automatic Downshifting
                if rpm < 2000 and gear > 1:
                    gear -= 1
                    print(f"  <- Downshift to Gear {gear}")
                    # Rev match (RPM jumps up on downshift)
                    rpm = int(speed / ratios[gear])
                
                send_telemetry(rpm, speed)
                time.sleep(0.02)
            
            # Reset to start line
            gear = 1
            rpm = 900
            print("  -- IDLE --")
            time.sleep(1)

        # Send the packet
        send_telemetry(rpm, speed)
        time.sleep(0.05) # 20Hz refresh

if __name__ == "__main__":
    try:
        run_track_test()
    except KeyboardInterrupt:
        print("Track Test Ended.")
