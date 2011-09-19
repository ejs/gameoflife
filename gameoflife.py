class World(object):
    """ Default world, infinate in all dimensons
        Neighbours looked for in 2d square grid plain
        Defaults to standard Conways Game of Life rules
    """

    def __init__(self, *positions, **rules):
        self.b = rules.get('b', set([3])) # born if b neighbours
        self.s = rules.get('s', set([2, 3])) # surivies if s neighbours
        self.cells = {}
        for p in positions:
            self += p
        self.step_time()

    def tick(self):
        self.evolve()
        self.step_time()

    def __len__(self):
        return len(list(self))

    def __iter__(self):
        for position in self.cells:
            if position in self:
                yield position

    ####
    # manipulate state
    def step_time(self):
        for position in dict(self.cells):
            if self[position] == 'child':
                self[position] = 'adult'
            elif self[position] == 'wounded':
                del self[position]

    def __iadd__(self, position):
        if position not in self:
            self[position] = 'child'
        return self

    def __isub__(self, position):
        if position in self:
            self[position] = 'wounded'
        return self

    def __contains__(self, position):
        """ Check if the cell at position is currently
            an alive adult
        """
        return self.cells.get(position) in ('adult', 'wounded')

    ######
    # shape of space
    def neighbours(self, (x, y)):
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx or dy:
                    yield (x+dx, y+dy)

    def display(self):
        xmin = min(x for x, y in self)
        xmax = max(x for x, y in self)
        ymin = min(y for x, y in self)
        ymax = max(y for x, y in self)
        for x in range(xmin, xmax+1):
            yield ''.join(('*' if (x, y) in self else '.') for y in range(ymin, ymax+1))

    def __getitem__(self, position):
        return self.cells[position]
    
    def __setitem__(self, position, state):
        self.cells[position] = state

    def __delitem__(self, position):
        del self.cells[position]

    ######
    # rules of life
    def live_neighbours(self, position):
        return sum(1 for p in self.neighbours(position) if p in self)

    def evolve(self):
        for position in self:
            if self.live_neighbours(position) not in self.s:
                self -= position
        for position in set(p for c in self for p in self.neighbours(c) if p not in self):
            if self.live_neighbours(position) in self.b:
                self += position


class ToridLife(World):
    def __init__(self, (width, height), *args, **kwargs):
        self.width = width
        self.height = height
        super(ToridLife, self).__init__(*args, **kwargs)

    def neighbours(self, (x, y)):
        for nx, ny in super(ToridLife, self).neighbours((x, y)):
            yield nx%self.width, ny%self.height


class ComplexWorld(World):
    def neighbours(self, position):
        for dx in (-1, 0, 1):
            for dy in(-1j, 0, 1j):
                if dx or dy:
                    yield position + dx + dy

    def display(self):
        xmin = min(p.real for p in self)
        xmax = max(p.real for p in self)
        ymin = min(p.imag for p in self)
        ymax = max(p.imag for p in self)
        for x in range(xmin, xmax+1):
            yield ''.join(('*' if x+y*1jin self else '.') for y in range(ymin, ymax+1))


if __name__ == '__main__':
    #world = ComplexWorld((1+1j), (2+2j), (3+3j), (2+3j))
    #world = World((1, 1), (2, 2), (3, 3), (2, 3))
    world = ToridLife((4, 4), (1, 1), (2, 2), (3, 3), (2, 3))
    for i in range(10):
        if not len(world):
            break
        for line in world.display():
            print line
        world.tick()
        print
