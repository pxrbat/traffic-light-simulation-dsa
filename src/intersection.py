from priority_queue import LanePriorityQueue
from road import Road
from metrics import Metrics

class Intersection:
    def __init__(self, metrics: Metrics = None):
        # Initializing 4 roads
        self.roads = {"A": Road("A"), "B": Road("B"), "C": Road("C"), "D": Road("D")}

        # Priority Queue for AL2 lane only
        self.priority_queue = LanePriorityQueue()
        self.priority_queue.register_lane(self.roads["A"].L2)

        # Metrics object
        self.metrics = metrics
        

    def total_normal_vehicles_count(self, active_priority_lane=None):
        """
        Computing total number of vehicles across all normal lanes
        (excluding active priority lane)
        """
        total = 0
        for road in self.roads.values():
            lane = road.L2
            if lane is not active_priority_lane:
                total += lane.size()
        return total

    def normal_service_count(self, active_priority_lane=None):
        """
        Computing number of vehicles to serve from normal lanes
        """
        total = self.total_normal_vehicles_count(active_priority_lane)
        n = 0
        # Counting number of normal lanes
        for road in self.roads.values():
            if road.L2 is not active_priority_lane:
                n += 1
        if n == 0:
            return 1  # always serve at least 1
        avg = total // n
        return max(avg, 1)

    def set_green_lane(self, lane):
        """
        Sets the given lane's light to GREEN while setting all others
        to RED
        """
        for road in self.roads.values():
            if road.L2.light:
                road.L2.light.set_red()
        if lane.light:
            lane.light.set_green()

        # Log to track lane receiving green light
        print(f"[LOG] Green light set for {lane.lane_id}")

    def serve_priority_lane(self, lane=None):
        """
        Serve AL2 lane if it is priority until it has <= 5 vehicles
        """
        active_lane = self.priority_queue.peek()
        if active_lane and active_lane.size() > 5:
            self.set_green_lane(active_lane)
            while active_lane.size() > 5:
                removed_vehicle = active_lane.remove_vehicle()
                # Metrics record if provided
                if self.metrics and removed_vehicle:
                    self.metrics.record_vehicle_served(active_lane.lane_id)
                # Log to track when a vehicle is removed from priority lane
                print(
                    f"[LOG] Removed {removed_vehicle.vehicle_id} from {active_lane.lane_id}"
                )
            return True
        return False

    def serve_normal_lanes(self):
        """
        Serve all normal lanes according to normal service formula
        """
        v = self.normal_service_count()
        for road in self.roads.values():
            lane = road.L2
            if lane is self.priority_queue.peek():
                continue #skip AL2
            if lane.size() > 0:
                self.set_green_lane(lane)
                for _ in range(v):
                    if lane.size() > 0:
                        removed_vehicle = lane.remove_vehicle()
                        # Metrics record if provided
                        if self.metrics and removed_vehicle:
                            self.metrics.record_vehicle_served(lane.lane_id)
                        if removed_vehicle is not None:
                            # Log to track when a vehicle is removed from normal lane
                            print(
                                f"[LOG] Removed {removed_vehicle.vehicle_id} from {lane.lane_id}"
                            )

    def get_active_priority_lane(self):
        lane = self.priority_queue.peek()
        if lane and lane.size() > 5:
            return lane
        return None

    def step(self):
        """
        Simulation step: Serve priority lane first if active, else normal lanes
        """
        if not self.serve_priority_lane():
            self.serve_normal_lanes()
