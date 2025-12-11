class TrafficLight:
    def __init__(self):
        self.state = 1  # 1 represents RED, 2 represents GREEN

    def set_green(self):
        self.state = 2

    def set_red(self):
        self.state = 1

    def is_green(self):
        return self.state == 2

    def __str__(self):
        return "GREEN" if self.state == 2 else "RED"
