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
