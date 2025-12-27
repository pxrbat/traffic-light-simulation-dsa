import random
import time
import os

LANES = ["AL2", "BL2", "CL2", "DL2"]

# Folder where lane text files live
DATA_DIR = 'lane_data'

def ensure_lane_files():
    """
    Makes sure data directory and lane files are present. Probably not needed, but safer this way.
    """
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    for lane_name in LANES:
        lane_file = os.path.join(DATA_DIR, lane_name + ".txt")
        if not os.path.isfile(lane_file):
            f = open(lane_file, "w")
            f.close()

def generate_vehicles():
    """
    Randomly decide how many vehicles show up per lane and append them to the corresponding file.
    """
    ensure_lane_files()

    for lane in LANES:
        path = os.path.join(DATA_DIR, f"{lane}.txt")

        vehicle_to_add = 0

        # High-ish chance of at least one vehicle
        if random.random()<0.8:
            vehicle_to_add = vehicle_to_add + 1
        
        # Lower chance of a second one
        if random.random()<0.4:
            vehicle_to_add+=1
        
        # Nothing to do for this lane
        if vehicle_to_add<=0:
            continue
        
        # Append new vehicle IDs
        with open(path, "a") as lane_file:
            for i in range(vehicle_to_add):
                # Using time based IDs; not perfect but good enough
                timestamp = int(time.time() * 1000)
                vehicle_id = f"{lane}_{timestamp}"
                lane_file.write(vehicle_id)
                lane_file.write("\n")
        
        print(f"[GENERATOR] Added {vehicle_to_add} vehicle(s) to {lane}")

def run_generator_loop():
    print("Traffic generator started. Press Ctrl + C to stop it.")

    try:
        while True:
            generate_vehicles()
            # Sleeping for 5 second feels realistic to me
            time.sleep(5)
    
    except KeyboardInterrupt:
        print("\nTraffic generator stopped by user.")

# Entry point
if __name__ == "__main__":
    run_generator_loop()
