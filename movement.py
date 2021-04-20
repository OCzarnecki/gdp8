from typing import List, Tuple

Pos = Tuple[int, int]
def occupied(pos: Pos) -> bool:
    # returns if there is an agent at pos. Dynamically updates throughout event processing.
    pass 
def move(a: Pos, b: Pos):
    # moves the agent at a to b
    pass

def process_movements(events: List[Tuple[Pos, Pos]]):
    """
    events is a list of movement commands (current_location, new_location) in time order
    the algorithm repeatedly executes the first command that can be executed
    this means in principle the timing of an agent's reply matters. thinking too long means movement may be blocked.
    it terminates as the length of events is strictly decreasing with each loop
    it does not handle cycles where all movement needs to happen at once
    """
    while events != []:
        try:
            i, (x1, x2) = find_first_movable(events)
            move(x1, x2)
            events.pop(i)
        except ValueError:
            events = []

def find_first_movable(events: List[Pos]):
    for i, (x1, x2) in enumerate(events):
        if not occupied(x2): return i, (x1, x2)
    raise ValueError()
