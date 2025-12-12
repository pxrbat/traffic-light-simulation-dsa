class Vehicle:
    """
    Simple vehicle representation for the simulation with each vehicle having it's own ID
    """

    def __init__(self, vehicle_id):
        self.vehicle_id = vehicle_id

    def __str__(self):
        return f"Vehicle({self.vehicle_id})"
