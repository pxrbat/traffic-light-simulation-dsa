from typing import Optional

from queue_ds import Queue
from traffic_light import TrafficLight


class Lane:
    def __init__(self, lane_id):
        self.lane_id = lane_id
        self.queue = Queue()
        self.light: Optional[TrafficLight] = None

    def add_vehicle(self, vehicle):
        self.queue.enqueue(vehicle)

    def remove_vehicle(self):
        return self.queue.dequeue()

    def size(self):
        return self.queue.size()

    def next_vehicle(self):
        if not self.queue.is_empty():
            return self.queue.peek()
        return None
