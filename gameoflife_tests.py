from gameoflife import *

def test_initialise_empty_world():
    w = World()
    assert len(w) == 0

def test_initialise_simple_world():
    w = World((0, 0), (1, 1))
    assert len(w) == 2

#####
# unit tests
def test_add_items_to_world():
    w = World()
    w += 0, 0
    assert len(w) == 0
    assert list(w) == []
    assert (0, 0) not in w
    w.step_time()
    assert len(w) == 1
    assert list(w) == [(0, 0)]
    assert (0, 0) in w

def test_remove_items_from_world():
    w = World((1, 1))
    w -= 1, 1
    assert len(w) == 1
    w.step_time()
    assert len(w) == 0

def test_step_time():
    w = World()
    w += 0, 0
    assert len(w) == 0
    assert list(w) == []
    w.step_time()
    assert len(w) == 1
    assert list(w) == [(0, 0)]
    w += 0, 0
    assert len(w) == 1
    assert list(w) == [(0, 0)]
    w.step_time()
    assert len(w) == 1
    assert list(w) == [(0, 0)]
    w.step_time()
    assert len(w) == 1
    assert list(w) == [(0, 0)]

def test_infinite_world_neighbours():
    w = World()
    n = list(w.neighbours((1, 1)))
    assert n == [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]

def test_evolve():
    w = World((1, 1))
    w.evolve()
    assert len(w) == 1
    w.step_time()
    assert len(w) == 0

# TODO: test live_neighbours

#####
# Functional tests
def test_lone_cell_dies():
    w = World((1, 1))
    w.tick()
    assert len(w) == 0

def test_square_lives():
    w = World(*[(x, y) for x in (1, 2) for y in (1, 2)])
    w.tick()
    assert len(w) == 4

def test_triangle_breeds():
    w = World((1, 1), (2, 2), (1, 2))
    w.tick()
    assert len(w) == 4

def test_line_moves():
    w = World((2, 1), (2, 2), (2, 3))
    w.tick()
    assert len(w) == 3
    assert (2, 1) not in w
    assert (1, 2) in w
    assert (2, 3) not in w
    assert (3, 2) in w
    assert (2, 2) in w

def test_beacon():
    w = World((1, 1), (1, 2), (2, 1), (4, 4), (4, 3), (3, 4))
    w.tick()
    assert len(w) == 8
    assert (2, 2) in w
    w.tick()
    assert len(w) == 6
    assert (2, 2) not in w
    w.tick()
    assert len(w) == 8
    assert (2, 2) in w

# TODO: test alternate GoL like worlds
# TODO: graphical output
# TODO: create and test von Neumann automata
# TODO: alternate world shapes
