# priority_queue.py


class LanePriorityQueue:
    """
    Lanes that have more than 10 vehicles are treated as highest priority.
    """

    def __init__(self):
        self.items = []

    def enqueue(self, lane):
        # Add a lane if it's not already in the queue
        if lane not in self.items:
            self.items.append(lane)

    def dequeue(self):
        # Remove and return the front item in the queue
        if not self.items:
            return None
        return self.items.pop(0)

    def update_priority(self):
        """
        Promotes the lane with queue size > 10 to the front of the queue.
        If multiple lanes qualify, promotes the first one encountered.
        """
        for i, lane in enumerate(self.items):
            if lane.size() > 10:
                # move it to the front
                self.items.insert(0, self.items.pop(i))
                break

    def peek(self):
        # Returns lane at the front of the queue without removing it
        if not self.items:
            return None
        return self.items[0]

    def is_empty(self):
        return len(self.items) == 0

    def __str__(self):
        # Print function for debugging purpose
        id = []
        for lane in self.items:
            id.append(lane.lane_id)
        return "[" + ", ".join(id) + "]"
