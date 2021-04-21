import sys, pygame, math, time
import numpy as np
from new_simulationState import State

pygame.init()

WIDTH = 900
HEIGHT = 600
SIZE = (WIDTH, HEIGHT)
SCREEN = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Survival")

FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

AGENT_MAX_SPEED = 2
AGENT_STEER_STRENGTH = 2
AGENTS_WANDER_STRENGTH = 0.5
AGENT_RADIUS = 6

font = pygame.font.SysFont("Times New Roman", 13)

def colorPercentage(n, scale):
    return 255 * (n / scale)

def pit_radius(pit_max_radius, water_percentage):
    return pit_max_radius * water_percentage

def clamp_norm(v, n_max):
    vx = v[0]
    vy = v[1]
    n = math.sqrt(vx**2 + vy**2)
    if n == 0:
        return np.array([0, 0])
    f = min(n, n_max) / n
    return np.array([f * vx, f * vy])

def message_to_screen(msg, x, y, color=WHITE):
    screen_txt = font.render(msg, False, color)
    SCREEN.blit(screen_txt, [x, y])

def draw_stats(time, survivors):
    message_to_screen("Day n°: " + str(time), 10, 10)
    message_to_screen("Survivors: " + str(survivors), 10, 25)

#drawing on the screen : we draw each cells and each agent
def draw_window(state):
    for cell in state.cells:
        drawCell(cell, state.max_water_capacity, state.pit_max_radius)
    for agent in state.agents:
        drawAgent(agent, state.max_inventory)
    draw_stats(state.time, len(state.agents))


#drawing the cells : we are drawing the water resources on the map
def drawCell(cell, max_water_capacity, pit_max_radius):
        #drawing a water pit, its radius depends on the number of left water
        pygame.draw.circle(SCREEN, (0, 0, 255), cell.pos, pit_radius(pit_max_radius, cell.water / float(max_water_capacity)))

#drawing the agents : 
def drawAgent(agent, max_inventory):
    #an agent will be represented as a circle on the screen
    pygame.draw.circle(SCREEN,
        (colorPercentage(max_inventory - agent.inventory, max_inventory), colorPercentage(agent.inventory, max_inventory), 0),
        agent.pos, AGENT_RADIUS)

#updating the states will be done with the logs from the simulation.
# For visualisation we will for now simulate a very simple behaviour...
def updateAgent(state):
    for agent in state.agents:
        #verify that agent can still move in its current direction : he does not hit a border
        #if (agent.pos + agent.vel).any() > np.array([WIDTH, HEIGHT]).any() or (agent.pos + agent.vel).any() < np.array([0, 0]).any():
            #if so, the agent goes in opposit direction (as I said it's very simple only to visualise...)
            #agent.vel = -agent.vel
        #we now must verify that the agent does not hit a water pit
        #for cell in state.cells:
            #computing the distance between water pit's center and agent's center
            #dist = math.hypot(agent.pos[0]-cell.pos[0], agent.pos[1]-cell.pos[1])
            #if the distance is lower than the radius, then again change the direction
            #if dist < pit_radius(cell.water / state.max_water_capacity):
                #agent.vel[0] = -agent.vel[0]
                #agent.vel[1] = -agent.vel[1]
        #finally update the new positions
        temp = agent.desired_pos - agent.pos
        desiredDirection = np.array([0, 0])
        if temp.all() != desiredDirection.all():
            desiredDirection = temp / np.linalg.norm(temp)

        desiredVelocity = desiredDirection * AGENT_MAX_SPEED
        desiredSteeringForce = (desiredVelocity - agent.vel) * AGENT_STEER_STRENGTH
        acceleration = clamp_norm(desiredSteeringForce, AGENT_STEER_STRENGTH) / 1

        agent.vel = clamp_norm(agent.vel + acceleration, AGENT_MAX_SPEED) / 1
        agent.pos = agent.pos + agent.vel

def stats(agent, x, y):
    message_to_screen("Agent id : " + str(agent.id), agent.pos[0] + x, agent.pos[1] + y)
    message_to_screen("Water left : " + str(agent.inventory), agent.pos[0] + x, agent.pos[1] + y + 15)

def paused(state) :

    paused = True

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = False
        pos = pygame.mouse.get_pos()
        SCREEN.fill(BLACK)
        draw_window(state)
        for agent in state.agents:
            #computing the distance between water pit's center and agent's center
            dist = math.hypot(agent.pos[0]-pos[0], agent.pos[1]-pos[1])
            #if the distance is lower than the radius, then again change the direction
            if dist < AGENT_RADIUS:
                if agent.pos[0] > WIDTH - 50:
                    stats(agent, -90, -30)
                elif agent.pos[1] < 50:
                    stats(agent, 15, 13)
                else:
                    stats(agent, 15, -30)
        pygame.display.update()
        

def main():

    state = State("/Users/tancrede/Desktop/projects/survival_simulation/test.json")

    clock = pygame.time.Clock()
    iteration = 0
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused(state)

        if iteration == 2:
            state.load()
            iteration = 0
        else:
            iteration += 1

        SCREEN.fill(BLACK)
        draw_window(state)
        pygame.display.update()
        updateAgent(state)
        
        
    pygame.quit()


if __name__ == "__main__":
    main()
