import random
import time
import os

from intersection import Intersection
from vehicle import Vehicle
from metrics import Metrics

DATA_DIR = "lane_data"

# Kept this function intact as a helper just in case even though I don't need it. 
# MEMO: Remove this later
def add_random_vehicles(intersection):
    """
    Randomly adding 0-2 vehicles for L2 lane of each road each step to simulate arrivals to L2 lanes
    """
    for road in intersection.roads.values():
        if random.random() < 0.8:  # 80% chance of adding a vehicle
            vehicle_id = f"{road.L2.lane_id}_{int(time.time() * 1000) % 100000}"  # creating random vehicle id's
            road.L2.add_vehicle(Vehicle(vehicle_id))
        if random.random() < 0.4:  # smaller chance of adding a second vehicle
            vehicle_id = f"{road.L2.lane_id}_{int(time.time() * 1000) % 100000 + 1}"
            road.L2.add_vehicle(Vehicle(vehicle_id))
    """
    Add 1 Vehicle to each L2 lane every step for testing
    """
    # for road in intersection.roads.values():
    #     vehicle_id = f"{road.L2.lane_id}_{int(time.time() * 1000) % 100000}"
    #     road.L2.add_vehicle(Vehicle(vehicle_id))

def load_vehicles_from_files(intersection):
    """
    Pull vehicle IDs from lane files and push them into the queues. Once read, wipe the files so we don't process the same cars again
    """
    added_any = False
    for road in intersection.roads.values():
        lane = road.L2
        file_path = os.path.join(DATA_DIR,f"{lane.lane_id}.txt")

        if not os.path.exists(file_path):
            continue

        with open(file_path, "r") as f:
            lines = f.readlines()
        
        if not lines:
            continue

        for line in lines:
            vehicle_id = line.strip()
            if vehicle_id:
                lane.add_vehicle(Vehicle(vehicle_id))
        
        #Clear file after reading data
        open(file_path, "w").close()
    
    # Just a safeguard feature to know when the generator stopped adding vehicles
    if not added_any:
        print("[LOG] No new vehicles added this step")
    
    return added_any

def print_status(intersection, step_count):
    """
    Prints L2 lane sizes, vehicles queue, and traffic light states
    """
    print(f"\n\t\t\tSimulation Step {step_count}\t\t\t\n")
    for road_id, road in intersection.roads.items():
        lane = road.L2
        vehicles_container = []
        for v in lane.queue.items:
            vehicles_container.append(v.vehicle_id)
        vehicles_str = ", ".join(vehicles_container)
        print(
            f"{lane.lane_id}: size= {lane.size()}, light={lane.light}, vehicles= [{vehicles_str}]"
        )
    active_priority = intersection.get_active_priority_lane()
    if active_priority:
        print(f"Active priority lane: {active_priority.lane_id}")
    else:
        print("Active priority lane: None")
    print("=" * 60)  # divider only


def run_simulation():
    #Create metrics object
    metrics = Metrics(time_per_vehicle=1)

    #Pass metrics to Intersection class
    intersection = Intersection(metrics = metrics)
    step_count = 0
    print("Starting simulation for L2 lanes. Press Ctrl + C to stop.")
    try:
        while True:
            step_count += 1

            # Load vehicles data stored in files
            load_vehicles_from_files(intersection)

            # execute intersection step (priority first, else normal)
            intersection.step()

            # print current lane status
            print_status(intersection, step_count)

            #Print metrics summary every 5 steps
            if step_count%5==0:
                metrics.print_summary()

            # wait for next simulation
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nSimulation stopped.")
        # print final metrics summary after simulation stops
        metrics.print_summary()


if __name__ == "__main__":
    run_simulation()
