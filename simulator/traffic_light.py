class TrafficLight:
    def __init__(self):
        self.state = 1  # 1 represents Green, 0 represents Red

    def set_green(self):
        self.state = 1

    def set_red(self):
        self.state = 0

    def is_green(self):
        return self.state == 1
