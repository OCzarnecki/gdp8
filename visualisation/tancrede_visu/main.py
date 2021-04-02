import sys, pygame, math
from simulationState import State
"""
Plan:
to do for first iteration:
1. Include user interface (a basic version, lower 1/3 of screen)
    Features may include:
        labels for simulation time and how many agents survive
        a way to reset the visualiser
2. Interface with JSON to implement State.load
    create some simulation logs to make sure the visuals are working
3. Make the initial SCREEN not be noise
4. Make main loop play the simulation forward in a simple way
    ideas:
        press a button to advance by one time step
        let the time tick forward every x seconds
5. Make WorldPainting reflect the water levels of cells and agents

Notes:
1. coordinates are (0, 0) on topleft in pygame. We may want to flip y coordinates if we want (0, 0) to be bottom left
2. how to split the
"""

WIDTH = 900
HEIGHT = 600
SIZE = (WIDTH, HEIGHT)
SCREEN = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Survival")

FPS = 60
BLACK = (0, 0, 0)


#drawing on the screen : we draw each cells and each agent
def draw_window(state):
    for cell in state.cells:
        drawCell(cell)
    for agent in state.agents:
        drawAgent(agent)
    pygame.display.update()


#drawing the cells : we are drawing the water resources on the map
def drawCell(cell):
        x = cell.x
        y = cell.y
        #drawing a water pit, its radius depends on the number of left water
        pygame.draw.circle(SCREEN, (0, 0, 255), (x, y), cell.water)

#drawing the agents : 
def drawAgent(agent):
    center = (agent.x, agent.y)
    #an agent will be represented as a circle on the screen
    pygame.draw.circle(SCREEN, (127, 127, 0), center, 2)

#updating the states will be done with the logs from the simulation.
# For visualisation we will for now simulate a very simple behaviour...
def updateState(state):
    for agent in state.agents:
        #verify that agent can still move in its current direction : he does not hit a border
        if agent.x + agent.vx > WIDTH or agent.x + agent.vx < 0:
            #if so, the agent goes in opposit direction (as I said it's very simple only to visualise...)
            agent.vx = -agent.vx
        #same thing for y direction
        if agent.y + agent.vy > HEIGHT or agent.y + agent.vy < 0:
            agent.vy = -agent.vy
        #we now must verify that the agent does not hit a water pit
        for cell in state.cells:
            #computing the distance between water pit's center and agent's center
            dist = math.hypot(agent.x-cell.x, agent.y-cell.y)
            #if the distance is lower than the radius (which is cell.water for us), then again change the direction
            if dist < cell.water:
                agent.vx = -agent.vx
                agent.vy = -agent.vy
        #finally update the new positions
        agent.x += agent.vx
        agent.y += agent.vy

def main():


    time = 0
    state = State("")

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        #state.load(time)
        draw_window(state)
        updateState(state)
        SCREEN.fill(BLACK)
        
    pygame.quit()


if __name__ == "__main__":
    main()
