from queue_ds import Queue


class Lane:
    def __init__(self, lane_id):
        self.lane_id = lane_id
        self.queue = Queue()
        self.light = None

    def add_vehicle(self, vehicle):
        self.queue.enqueue(vehicle)

    def remove_vehicle(self):
        self.queue.dequeue()

    def size(self):
        return self.queue.size()
