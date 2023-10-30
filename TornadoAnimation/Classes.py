class Tornado():
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.current = start
        self.alpha = 255
        self.done = False
        self.count = 0
        self.add_x = (self.end[0] - self.start[0]) * .1
        self.add_y = (self.end[1] - self.start[1]) * .1

    def update(self):
        if self.count < 10:
            self.current = (self.current[0] + self.add_x, self.current[1] + self.add_y)
            self.count += 1
        if self.count == 10:
            self.current = self.end
        if self.current == self.end:
            self.alpha = max(0, self.alpha - 5)
            if self.alpha == 0:
                self.done = True
