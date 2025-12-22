from typing import Optional

from queue_ds import Queue
from traffic_light import TrafficLight


class Lane:
    """
    This class represents a single traffic lane.
    Dumb by design - responsible for only managing its vehicle queue and traffic light reference.
    """
    def __init__(self, lane_id):
        self.lane_id = lane_id
        self.queue = Queue()
        self.light: Optional[TrafficLight] = None

    def add_vehicle(self, vehicle):
        """
        Add a vehicle to the end of the lane queue
        """
        self.queue.enqueue(vehicle)

    def remove_vehicle(self):
        """
        Remove and return the front vehicle from the queue.
        """
        return self.queue.dequeue()

    def size(self):
        """
        Returns the number of vehicles currently in the lane
        """
        return self.queue.size()

    def next_vehicle(self):
        """
        Peek at the next vehicle in the queue without removing it
        """
        if not self.queue.is_empty():
            return self.queue.peek()
        return None
