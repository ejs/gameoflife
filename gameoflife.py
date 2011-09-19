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
            yield ''.join(self.character_for_cell((x, y)) for y in range(ymin, ymax+1))

    def character_for_cell(self, position):
        return '*' if position in self else '.'

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

    def display(self):
        for x in range(self.height):
            yield ''.join(self.character_for_cell((x, y)) for y in range(self.width))


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
            yield ''.join(self.character_for_cell(x+y*1j) for y in range(ymin, ymax+1))


class SeethroughDonut(ToridLife):
    def neighbours(self, (x, y)):
        for nx, ny in super(ToridLife, self).neighbours((x, y)):
            yield nx%self.width, ny%self.height
        yield (x+self.width/2)%self.width, y

    def display(self):
        for x in range(self.height/2):
            yield ''.join(self.character_for_cell((x, y)) for y in range(self.width))

    def character_for_cell(self, (x, y)):
        negx = (self.width-x)%self.width
        if (x, y) in self and (negx, y) in self:
            return '*'
        if (x, y) in self:
            return '+'
        if (negx, y) in self:
            return 'x'
        return '.'


if __name__ == '__main__':
    import optparse
    #world = ComplexWorld((1+1j), (2+2j), (3+3j), (2+3j))

    parser = optparse.OptionParser()
    parser.add_option('-i', dest='world', action='store_const', const=World, default=World)
    parser.add_option('-t', dest='world', action='store_const', const=ToridLife)
    parser.add_option('-s', dest='world', action='store_const', const=SeethroughDonut)
    parser.add_option('-f', dest='file', action='store')
    parser.add_option('-n', dest='number', action='store', type='int', default=10)
    options, args = parser.parse_args()

    if options.file:
        start = [eval(line) for line in open(options.file)]
        world = options.world(*start)
    else:
        world = options.world((4, 4), (1, 1), (2, 2), (3, 3), (2, 3))

    for i in range(options.number):
        if not len(world):
            break
        for line in world.display():
            print line
        world.tick()
        print
