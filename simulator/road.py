from typing import Optional

from lane import Lane
from traffic_light import TrafficLight


class Road:
    def __init__(self, road_id):
        self.road_id = road_id

        self.L1 = Lane(f"{road_id}L1")  # incoming lane

        self.L2 = Lane(f"{road_id}L2")  # priority lane
        self.L2.light = TrafficLight()

        self.L3 = Lane(f"{road_id}L3")  # free lane

    def is_priority_lane(self):
        """Checking if L2 should be treated as priority lane"""
        return self.L2.size() > 10

    def total_normal_lane_vehicles(self, active_priority_lane=None):
        """Counting vehicles in L2 if not currently active priority lane"""
        total = 0
        if self.L2 is not active_priority_lane:
            total += self.L2.size()
        return total
