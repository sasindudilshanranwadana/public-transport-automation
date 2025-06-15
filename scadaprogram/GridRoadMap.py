import random


class GridRoadMap:
    def __init__(self, canvas, width, height, spacing):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.spacing = spacing

    def draw(self):
        for x in range(0, self.width, self.spacing):
            self.canvas.create_line(x, 0, x, self.height, fill="black", width=8)
        for y in range(0, self.height, self.spacing):
            self.canvas.create_line(0, y, self.width, y, fill="black", width=8)

    def random_grid_point(self):
        return random.choice(range(0, self.width, self.spacing)), random.choice(range(0, self.height, self.spacing))

    def create_random_route(self, steps=8):
        route = [self.random_grid_point()]
        for _ in range(steps):
            last_x, last_y = route[-1]
            possible_moves = [
                (last_x, last_y - self.spacing) if last_y - self.spacing >= 0 else None,
                (last_x, last_y + self.spacing) if last_y + self.spacing < self.height else None,
                (last_x - self.spacing, last_y) if last_x - self.spacing >= 0 else None,
                (last_x + self.spacing, last_y) if last_x + self.spacing < self.width else None
            ]
            possible_moves = [move for move in possible_moves if move]
            route.append(random.choice(possible_moves))
        return route

    def generate_grid_route(self, start, end):
        route = [start]
        x0, y0 = start
        x1, y1 = end

        while x0 != x1:
            x0 += self.spacing if x1 > x0 else -self.spacing
            route.append((x0, y0))

        while y0 != y1:
            y0 += self.spacing if y1 > y0 else -self.spacing
            route.append((x0, y0))

        return route