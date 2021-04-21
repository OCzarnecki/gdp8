# For all other strategy files, assume this one is at the top of the file

from random import randint

done = False # has the agent acted this turn yet?
t = 1 # tick length
def on_receive_tick(tick):
    done = False
    store_tick_info() # agents remember what the tick gives
    init() # set up variables based on tick info
    broadcast() # broadcast info once and only once
    delay(2*t/3., finally) # receive messages for this long
    # the function finally is called, then no more messages are received
    # note: 2*t/3. is a reasonable time I think, I don't know the internals of the AEA framework

def store_tick_info(): pass # is common across all these strategies.

def uniform_walk():
    d = randint(1, 4)
    if d == 1:
        walk(up) # walk sends a walk reply to the tick
    elif d == 2:
        walk(right)
    elif d == 3:
        walk(down)
    elif d == 4:
        walk(left)
    else:
        raise ValueError()
