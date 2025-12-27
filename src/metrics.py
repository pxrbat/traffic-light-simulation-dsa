"""
This module keeps track of some very basic traffic stats.

Kept intentionally simple.
"""


class Metrics:
    def __init__(self, time_per_vehicle=1):
        # Rough guess (in seconds) for how long one vehicle takes to pass.
        self.time_per_vehicle = time_per_vehicle
        # Overall count across every lane we've seen so far
        self.total_vehicles_served = 0

        # Per-lane breakdown.
        self.vehicles_served_per_lane = {}

        # Thought about tracking timestamps here, but that's probably beyond the scope
        # for this assignment, so leaving it out for now.
        # self.last_served_time = None

    def record_vehicle_served(self, lane_id):
        """
        Called whenever a vehicle passes through a lane.
        """
        self.total_vehicles_served += 1

        if lane_id not in self.vehicles_served_per_lane:
            self.vehicles_served_per_lane[lane_id] = 0

        # Increment the per-lane count
        self.vehicles_served_per_lane[lane_id] += 1

    def estimate_green_time(self, vehicles_count):
        """
        Estimate how long the green light should last.
        T = number_of_vehicles * time_per_vehicle
        """
        estimated_time = vehicles_count * self.time_per_vehicle
        return estimated_time

    def print_summary(self):
        """
        Dump a simple summary of collected metrics.
        Mostly for debugging only.
        """
        print("\n[METRICS SUMMARY]")
        print(f"Total vehicles served: {self.total_vehicles_served}")

        for lane_id, count in self.vehicles_served_per_lane.items():
            print(f"Lane {lane_id}: {count} vehicles served")

