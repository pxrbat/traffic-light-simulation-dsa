from road import Road


class Intersection:
    def __init__(self):
        # Initializing 4 roads
        self.roads = {"A": Road("A"), "B": Road("B"), "C": Road("C"), "D": Road("D")}

    def get_active_priority_lane(self):
        candidates = []
        """
        Adding all the possible candidate roads with >10
        vehicles to the list.
        """
        for road in self.roads.values():
            if road.is_priority_lane():
                candidates.append(road.L2)
        # If no road is priority return None
        if len(candidates) == 0:
            return None
        """
        If more than one road has >10 vehicles, then
        road with most vehicles is priority
        """
        return max(candidates, key=lambda k: k.size())

    def total_normal_vehicles_count(self, active_priority_lane=None):
        """
        Computing total number of vehicles across all normal lanes
        (excluding active priority lane)
        """
        total = 0
        for road in self.roads.values():
            total += road.total_normal_lane_vehicles(active_priority_lane)
        return total

    def normal_service_count(self, active_priority_lane=None):
        """Computing number of vehicles to serve from normal lanes"""
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

    def serve_priority_lane(self, lane):
        """ "Serve priority lane until there are less than 5 vehicles"""
        self.set_green_lane(lane)
        while lane.size() > 5:
            lane.remove_vehicle()

    def serve_normal_lanes(self):
        """
        Serve all normal lanes according to normal service formula
        """
        active_priority = self.get_active_priority_lane()
        v = self.normal_service_count(active_priority_lane=active_priority)
        for road in self.roads.values():
            lane = road.L2
            if lane is not active_priority and lane.size() > 0:
                self.set_green_lane(lane)
                for _ in range(v):
                    if lane.size() > 0:
                        lane.remove_vehicle()

    def step(self):
        """
        Simulation step: priority lane first if active, else normal lanes
        """
        active_priority = self.get_active_priority_lane()
        if active_priority:
            self.serve_priority_lane(active_priority)
        else:
            self.serve_normal_lanes()
