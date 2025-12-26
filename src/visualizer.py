import pygame
import random
import os
import math 

# ---------------- CONFIG ----------------
# Screen stuff
WIDTH, HEIGHT = 1000, 800
FPS = 60

# Road / lane sizing
LANE_WIDTH = 50
ROAD_WIDTH = LANE_WIDTH * 3

# Vehicle physics (not realistic, just for demo)
MAX_SPEED = 3.5
ACCEL = 0.12
BRAKE = 0.2

# ---- COLORS (dark-ish aesthetic) ----
BG_GREEN = (24, 45, 24)        # background grass
ROAD_COLOR = (33, 33, 33)
CENTER_LINE = (255, 214, 0)

GLOW_RED = (255, 50, 50)
GLOW_GREEN = (50, 255, 150)

WHITE = (240, 240, 240)
TEXT_COLOR = (200, 200, 200)

DATA_DIR = "lane_data"


class PhysicalVehicle:
    """
    This class is intentionally a bit chunky. It handles both the vehicle's
    state and its rendering. This is just for simplicity since this is a small
    demo project.
    """

    def __init__(self, vehicle_id, road_id, lane_type="L2"):
        self.id = vehicle_id
        self.road_id = road_id
        self.lane_type = lane_type

        self.speed = 0
        self.crossed_line = False

        # Left-hand traffic logic for Nepal
        if lane_type == "L3":
            self.turn_dir = "LEFT"
        elif lane_type == "L1":
            self.turn_dir = "RIGHT"
        else:
            self.turn_dir = "STRAIGHT"

        self.is_free_turn = (self.turn_dir == "LEFT")

        cx, cy = WIDTH // 2, HEIGHT // 2

        # lane offset mapping (hardcoded but works fine)
        lane_offsets = {
            "L3": LANE_WIDTH,
            "L2": 0,
            "L1": -LANE_WIDTH
        }
        off = lane_offsets[self.lane_type]

        # Initial spawn + stop line per road
        if road_id == 'A':   # North
            self.pos = pygame.Vector2(cx + LANE_WIDTH // 2 + off, -50)
            self.angle = 270
            self.stop_line = cy - ROAD_WIDTH // 2

        elif road_id == 'B':  # East
            self.pos = pygame.Vector2(WIDTH + 50, cy + LANE_WIDTH // 2 + off)
            self.angle = 180
            self.stop_line = cx + ROAD_WIDTH // 2

        elif road_id == 'C':  # South
            self.pos = pygame.Vector2(cx - LANE_WIDTH // 2 - off, HEIGHT + 50)
            self.angle = 90
            self.stop_line = cy + ROAD_WIDTH // 2

        elif road_id == 'D':  # West
            self.pos = pygame.Vector2(-50, cy - LANE_WIDTH // 2 - off)
            self.angle = 0
            self.stop_line = cx - ROAD_WIDTH // 2

        # Random car color just for visual variety
        self.body_color = random.choice([
            (60, 120, 255),
            (255, 80, 80),
            (220, 220, 220),
            (180, 100, 255)
        ])

    def update(self, lead_vehicle, is_green):
        target_speed = MAX_SPEED

        # ---- basic car-following logic ----
        if lead_vehicle is not None:
            dist = self.pos.distance_to(lead_vehicle.pos)

            if dist < 70:
                target_speed = lead_vehicle.speed * 0.5

            if dist < 45:
                target_speed = 0

        # ---- traffic light logic ----
        dist_to_line = self.get_dist_line()

        if not self.crossed_line:
            if not self.is_free_turn and not is_green:
                if 0 < dist_to_line < 40:
                    target_speed = 0

            if dist_to_line < -5:
                self.crossed_line = True

        # ---- acceleration / braking ----
        if self.speed < target_speed:
            self.speed += ACCEL
        elif self.speed > target_speed:
            self.speed -= BRAKE

        if self.speed < 0:
            self.speed = 0

        # ---- movement ----
        if not self.crossed_line:
            move_vec = pygame.Vector2(self.speed, 0).rotate(-self.angle)
            self.pos += move_vec
        else:
            self.apply_turn()

    def apply_turn(self):
        """
        This is definitely the messiest part of the code.
        """
        cx, cy = WIDTH // 2, HEIGHT // 2
        s = self.speed

        if self.road_id == 'A':
            if self.turn_dir == 'LEFT':
                self.pos.x -= s
                self.pos.y = cy + 25
                self.angle = 180
            elif self.turn_dir == 'RIGHT':
                self.pos.x += s
                self.pos.y = cy - 25
                self.angle = 0
            else:
                self.pos.y += s

        elif self.road_id == 'B':
            if self.turn_dir == 'LEFT':
                self.pos.y -= s
                self.pos.x = cx - 25
                self.angle = 90
            elif self.turn_dir == 'RIGHT':
                self.pos.y += s
                self.pos.x = cx + 25
                self.angle = 270
            else:
                self.pos.x -= s

        elif self.road_id == 'C':
            if self.turn_dir == 'LEFT':
                self.pos.x += s
                self.pos.y = cy - 25
                self.angle = 0
            elif self.turn_dir == 'RIGHT':
                self.pos.x -= s
                self.pos.y = cy + 25
                self.angle = 180
            else:
                self.pos.y -= s

        elif self.road_id == 'D':
            if self.turn_dir == 'LEFT':
                self.pos.y += s
                self.pos.x = cx + 25
                self.angle = 270
            elif self.turn_dir == 'RIGHT':
                self.pos.y -= s
                self.pos.x = cx - 25
                self.angle = 90
            else:
                self.pos.x += s

    def get_dist_line(self):
        # Distance from current stop line (sign depends on road)
        if self.road_id == 'A':
            return self.stop_line - self.pos.y
        if self.road_id == 'B':
            return self.pos.x - self.stop_line
        if self.road_id == 'C':
            return self.pos.y - self.stop_line
        if self.road_id == 'D':
            return self.stop_line - self.pos.x

        return 9999   # should never happen

    def draw(self, surf):
        # Create a small surface so rotation looks clean
        car_surf = pygame.Surface((42, 26), pygame.SRCALPHA)

        # Shadow first to give depth
        pygame.draw.rect(
            car_surf, (0, 0, 0, 80),
            (2, 2, 40, 24),
            border_radius=5
        )

        # Main body
        pygame.draw.rect(
            car_surf, self.body_color,
            (0, 0, 40, 24),
            border_radius=5
        )

        # Windshield detail
        pygame.draw.rect(
            car_surf, (40, 40, 40),
            (28, 3, 8, 18),
            border_radius=2
        )

        rotated = pygame.transform.rotate(car_surf, self.angle)
        surf.blit(rotated, rotated.get_rect(center=(self.pos.x, self.pos.y)))


class Simulation:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Traffic Light Visualizer")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Outfit", 36)

        # Vehicles grouped by road
        self.vehicles = {
            "A": [],
            "B": [],
            "C": [],
            "D": []
        }

        self.current_green = "A"
        self.timer = 0

    def draw_aesthetic_bg(self):
        self.screen.fill(BG_GREEN)
        cx, cy = WIDTH // 2, HEIGHT // 2

        # Road shadows (prob not needed but looks nice)
        pygame.draw.rect(
            self.screen, (20, 20, 20),
            (cx - ROAD_WIDTH // 2 - 5, 0, ROAD_WIDTH + 10, HEIGHT)
        )
        pygame.draw.rect(
            self.screen, (20, 20, 20),
            (0, cy - ROAD_WIDTH // 2 - 5, WIDTH, ROAD_WIDTH + 10)
        )

        # Main roads
        pygame.draw.rect(
            self.screen, ROAD_COLOR,
            (cx - ROAD_WIDTH // 2, 0, ROAD_WIDTH, HEIGHT)
        )
        pygame.draw.rect(
            self.screen, ROAD_COLOR,
            (0, cy - ROAD_WIDTH // 2, WIDTH, ROAD_WIDTH)
        )

        # Dotted yellow center lines
        def draw_dotted_line(start, end, vertical=True):
            length = end - start
            for i in range(0, length, 40):
                if vertical:
                    pygame.draw.rect(self.screen, CENTER_LINE, (cx - 1, start + i, 3, 20))
                else:
                    pygame.draw.rect(self.screen, CENTER_LINE, (start + i, cy - 1, 20, 3))

        draw_dotted_line(0, cy - ROAD_WIDTH // 2)
        draw_dotted_line(cy + ROAD_WIDTH // 2, HEIGHT)
        draw_dotted_line(0, cx - ROAD_WIDTH // 2, False)
        draw_dotted_line(cx + ROAD_WIDTH // 2, WIDTH, False)

        # Road labels (just to recognize the roads)
        labels = {
            "A": (cx + 100, 20),
            "B": (WIDTH - 100, cy + 90),
            "C": (cx - 180, HEIGHT - 50),
            "D": (20, cy - 110)
        }

        for road, pos in labels.items():
            txt = self.font.render(f"ROAD {road}", True, TEXT_COLOR)
            self.screen.blit(txt, pos)

        # Traffic lights w/ glow
        lights = {
            "A": (cx + ROAD_WIDTH // 2 + 25, cy - ROAD_WIDTH // 2 - 25),
            "B": (cx + ROAD_WIDTH // 2 + 25, cy + ROAD_WIDTH // 2 + 25),
            "C": (cx - ROAD_WIDTH // 2 - 25, cy + ROAD_WIDTH // 2 + 25),
            "D": (cx - ROAD_WIDTH // 2 - 25, cy - ROAD_WIDTH // 2 - 25)
        }

        for rid, pos in lights.items():
            is_active = (rid == self.current_green)
            color = GLOW_GREEN if is_active else GLOW_RED

            # Glow layers
            for r in range(1, 15, 3):
                glow = pygame.Surface((60, 60), pygame.SRCALPHA)
                pygame.draw.circle(glow, (*color, 100 // r), (30, 30), 10 + r)
                self.screen.blit(glow, (pos[0] - 30, pos[1] - 30))

            pygame.draw.circle(self.screen, color, pos, 10)

    def run(self):
        while True:
            # --- file-based vehicle injection ---
            # not super efficient, but easy to debug
            for rid in ["A", "B", "C", "D"]:
                path = os.path.join(DATA_DIR, f"{rid}L2.txt")
                if os.path.exists(path) and os.path.getsize(path) > 0:
                    with open(path, "r") as f:
                        for line in f:
                            vid = line.strip()
                            self.vehicles[rid].append(
                                PhysicalVehicle(vid, rid)
                            )
                    open(path, "w").close()

            # --- traffic signal timer ---
            self.timer += 1
            if self.timer > 300:
                order = ["A", "D", "C", "B"]
                idx = order.index(self.current_green)
                self.current_green = order[(idx + 1) % 4]
                self.timer = 0

            self.draw_aesthetic_bg()

            # --- update + draw vehicles ---
            for rid, v_list in self.vehicles.items():
                for i, car in enumerate(v_list):
                    lead_car = v_list[i - 1] if i > 0 else None
                    car.update(lead_car, rid == self.current_green)
                    car.draw(self.screen)

                # cleanup offscreen cars
                self.vehicles[rid] = [
                    v for v in v_list
                    if -100 < v.pos.x < WIDTH + 100
                    and -100 < v.pos.y < HEIGHT + 100
                ]

            # --- events ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            pygame.display.flip()
            self.clock.tick(FPS)


if __name__ == "__main__":
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    Simulation().run()
