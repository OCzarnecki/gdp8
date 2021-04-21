# they're trusting and helpful, but don't remember
# the second smartest strategy

def init(): pass

def broadcast():
    water_broadcast() # tell neighbors how much water I have

def on_receive_water_broadcast(cell, water):
    if water > self.water:
        diff = (water - self.water) // 2
        drink(request(diff))
        # diff is meant to be fair. after, we should have the same water
        done = True

def finally():
    if not done:
        if cell_has_water:
            # offer 1/3 of my water
            drink(offer(self.water//3))
            # originally I wanted to offer the water difference between me and the thirstiest neighbor, but that requires remembering neighbor info. This gets close, without needing to remember.
            # 1/3 is a nice round value where we are still selfish. 1/2 means our neighbors get more water than us, which is in my opinion too selfless
        else:
            uniform_walk()
        done = True
