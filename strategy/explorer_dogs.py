# loyal, daring, a bit stubborn
# the 'smartest' of the 3 strategies

from enum import Enum, auto

class State(Enum):
    SEEKING = auto()
    RETURNING = auto()

# remember 3 bits of information
# direction is interpreted in binary
# 1s digit is 0 east, 1 west
# 2s digit is 0 north, 1 south
# direction points to where we think water is
direction = randint(0, 3)
# state is either State.SEEKING or State.RETURNING
# SEEKING is finding water going opposite of direction, RETURNING is following direction
state = State.SEEKING

def init():
    # update state. note magic numbers .5 and .9, they can and should be tweaked to make the simulations interesting
    if state == State.SEEKING:
        if self.water <= max_water_capacity * .5:
            state = State.RETURNING
    elif state == State.RETURNING:
        if self.water > max_water_capacity * .9:
            state = State.SEEKING

def broadcast():
    water_broadcast()
    direction_broadcast()

def on_receive_water_broadcast(cell, water):
    # NOTE: it's the same as the altruistic_goldfish, except for the extra state condition
    # We only beg for water when returning, otherwise we want to go as far as possible
    if state == State.RETURNING and water > self.water:
        diff = (water - self.water) // 2
        drink(request(diff))
        # diff is meant to be fair. after, we should have the same water
        done = True

def on_receive_direction_broadcast(d):
    if state == State.RETURNING:
        # we might follow our neighbor
        # only if we're returning, because we're less stubborn and desperate for water
        change = randint(0, 1)
        if change:
            direction = d

def finally():
    if not done:
        if cell_has_water:
            drink(offer(self.water//3))
            # randomise direction because it's cool. To be adventurous next time we set off for water.
            direction = randint(0,3)
        else:
            d = direction
            if state == State.SEEKING:
                # go opposite of where the water is
                d = 0b11 - d
            direction_walk(d)
        done = True

def direction_walk(d):
    # random walk following the direction. e.g. if NE go N, E with probability 1/2 each.
    # 0 is left/right, 1 is up/down
    choice = randint(0, 1)
    if choice == 0:
        if d & 0b01 == 0b00:
            walk(right)
        elif d & 0b01 == 0b01:
            walk(left)
        else:
            raise ValueError()
    elif choice == 1:
        if d & 0b10 == 0b00:
            walk(up)
        elif d & 0b10 == 0b10:
            walk(down)
        else:
            raise ValueError()
    else:
        raise ValueError()
