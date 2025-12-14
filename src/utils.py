from math import sqrt

class Timer:
    def __init__(self, amount: float, autostart: bool = True):
        self.t = 0
        self.amt = amount
        self.stopped = not autostart
        self.elapsed = False

    def tick(self, delta: float):
        if self.stopped:
            return

        self.t += delta
        if self.t >= self.amt:
            self.stopped = True
            self.elapsed = True

    def is_elapsed(self) -> bool:
        return self.elapsed

    def is_running(self) -> bool:
        return not self.stopped

    def start(self):
        self.stopped = False
        self.t = 0
        self.elapsed = False

    def stop(self):
        self.stopped = True
        self.elapsed = False

def perpendicular_dir(dir_a_x: int, dir_a_y: int, dir_b_x: int, dir_b_y: int) -> bool:
    return (dir_a_x == 0 and dir_b_y == 0) or (dir_a_y == 0 and dir_b_x == 0)

def dist(p1: tuple[int, int], p2: tuple[int, int]) -> float:
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def clamp(v, min_, max_):
    if v < min_:
        return min_
    elif v > max_:
        return max_
    else:
        return v
