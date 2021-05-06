from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import sys, pygame, math, time, random
import numpy as np
from visualisation.simulationState import State

AGENTS_WANDER_STRENGTH = None 
AGENT_RADIUS = None
AGENT_STEER_STRENGTH = None 
BASIC_SPEED = None 
BLACK = None 
FPS = None 
HEIGHT = None 
SCREEN = None 
SIZE = None 
WHITE = None 
WIDTH = None 

def init_engine():
    pygame.init()

    global WIDTH 
    WIDTH = 900
    global HEIGHT 
    HEIGHT = 600
    global SIZE 
    SIZE = (WIDTH, HEIGHT)
    global SCREEN 
    SCREEN = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Survival")

    global FPS 
    FPS = 60
    global BLACK 
    BLACK = (0, 0, 0)
    global WHITE 
    WHITE = (255, 255, 255)

    global AGENT_STEER_STRENGTH 
    AGENT_STEER_STRENGTH = 4
    global AGENTS_WANDER_STRENGTH 
    AGENTS_WANDER_STRENGTH = 0.5
    global AGENT_RADIUS
    AGENT_RADIUS = 5
    global BASIC_SPEED 
    BASIC_SPEED = 4

    global font 
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

def message_to_screen(msg, x, y, color=None):
    if color == None:
        color = WHITE
    screen_txt = font.render(msg, False, color)
    SCREEN.blit(screen_txt, [x, y])

def draw_speed(speed):
    message_to_screen("x " + str(speed), 875, 20)

def draw_controls(play):
    if play:
        pygame.draw.polygon(SCREEN, WHITE, [(850, 20), (850, 40), (865, 30)])
    else:
        rect = pygame.Rect(850, 20, 5, 20)
        pygame.draw.rect(SCREEN, WHITE, rect)
        rect = pygame.Rect(860, 20, 5, 20)
        pygame.draw.rect(SCREEN, WHITE, rect)
    

def draw_stats(time, survivors):
    message_to_screen("Day n°: " + str(time), 10, 10)
    message_to_screen("Survivors: " + str(survivors), 10, 25)

#drawing on the screen : we draw each cells and each agent
def draw_window(state, play=True):
    for cell in state.cells:
        drawCell(cell, state.max_water_capacity, state.pit_max_radius)
    for agent in state.agents:
        drawAgent(agent, state.max_inventory)
    draw_stats(state.time, len(state.agents))
    draw_controls(play)
    draw_speed(state.speed)


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

# checks whether an agent is inside a square of center c, width w and height h
def check_pos(a_pos, c, w, h):
    hdist = math.fabs(a_pos[0] - c[0])
    vdist = math.fabs(a_pos[1] - c[1])
    return hdist < w and vdist < h

def insideUnitCircle():
    t = 2 * math.pi * random.random()
    u = random.random() + random.random()
    r = u
    if u > 1:
        r = 2 - u
    return np.array([r * math.cos(t), r * math.sin(t)])

def new_pos(agent, speed):
    desiredVelocity = agent.desired_dir * speed
    desiredSteeringForce = (desiredVelocity - agent.vel) * AGENT_STEER_STRENGTH
    acceleration = clamp_norm(desiredSteeringForce, AGENT_STEER_STRENGTH) / 1

    agent.vel = clamp_norm(agent.vel + acceleration, speed) / 1
    agent.pos = agent.pos + agent.vel

def updateAgent(state):
    for agent in state.agents:
        # we check if the agent is near water
        is_near_water = False
        cell_pos = np.array([0, 0])
        cell_water = 0
        for cell in state.cells:
            if cell.water != 0 and check_pos(agent.pos, cell.pos, state.tile_width/2, state.tile_height/2):
                is_near_water = True
                cell_pos = cell.pos
                cell_water = cell.water
                break
        # case 1) agent is near water...
        if is_near_water:
            # 1.1) ...and wants to stay
            if (cell_pos == agent.desired_pos).all():
                # then he will stick to the water pit
                dist = math.hypot(agent.pos[0] - cell_pos[0], agent.pos[1] - cell_pos[1])
                # if the distance between the agent and the center of the pit is smaller than the radius, we stop
                if dist <= pit_radius(state.pit_max_radius, cell_water / float(state.max_water_capacity)):
                    # deal with the start state where the agent is in the middle of the lake
                    if (agent.pos == cell_pos).all():
                        agent.pos[0] = agent.pos[0] - pit_radius(state.pit_max_radius, cell_water / float(state.max_water_capacity))
                    agent.desired_dir = np.array([0, 0])
                else:
                    temp = agent.desired_pos - agent.pos
                    agent.desired_dir = temp / np.linalg.norm(temp)
            # 1.2) ...and wants to leave
            else:
                temp = agent.desired_pos - agent.pos
                agent.desired_dir = temp / np.linalg.norm(temp)
        # case 2) agent is not near water...
        else:
            # 2.1) ...and wants to stay
            if check_pos(agent.pos, agent.desired_pos, state.tile_width/4, state.tile_height/4):
                agent.desired_dir = agent.desired_dir + insideUnitCircle() * AGENTS_WANDER_STRENGTH
                if (agent.desired_dir != np.array([0, 0])).all():
                    agent.desired_dir = agent.desired_dir / np.linalg.norm(agent.desired_dir)
            # 2.2) ...and wants to leave
            else:
                temp = agent.desired_pos - agent.pos
                agent.desired_dir = temp / np.linalg.norm(temp)
        new_pos(agent, state.speed)

def stats(agent, x, y, max_inventory):
    message_to_screen("Agent id : " + str(agent.id), agent.pos[0] + x, agent.pos[1] + y)
    message_to_screen("Water left : " + str(math.floor((agent.inventory/max_inventory)*100)) + "%", agent.pos[0] + x, agent.pos[1] + y + 15)

def paused(state) :

    paused = True

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                paused = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = False
        if paused:
            pos = pygame.mouse.get_pos()
            SCREEN.fill(BLACK)
            draw_window(state, False)
            for agent in state.agents:
                #computing the distance between water pit's center and agent's center
                dist = math.hypot(agent.pos[0]-pos[0], agent.pos[1]-pos[1])
                #if the distance is lower than the radius, then again change the direction
                if dist < AGENT_RADIUS:
                    if agent.pos[0] > WIDTH - 50:
                        stats(agent, -90, -30, state.max_inventory)
                    elif agent.pos[1] < 50:
                        stats(agent, 15, 13, state.max_inventory)
                    else:
                        stats(agent, 15, -30, state.max_inventory)
            pygame.display.update()
        

def run_replay(log_path):
    init_engine()
    state = State(log_path)

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
                if event.key == pygame.K_RIGHT and state.speed < 4:
                    state.speed *= 2
                    iteration = 0
                if event.key == pygame.K_LEFT and state.speed > 1:
                    state.speed = math.floor(state.speed / 2)
                    iteration = 0
        if run:
            if iteration == BASIC_SPEED / state.speed:
                state.load()
                iteration = 0
            else:
                iteration += 1

            SCREEN.fill(BLACK)
            draw_window(state)
            pygame.display.update()
            updateAgent(state)
        
    pygame.quit()

def main():
    if len(sys.argv) != 2:
        log_path = "/Users/tancrede/Desktop/projects/survival_simulation/test.json"
        print(f"No log file specified, using default: {log_path}")
        print(f"Run --help to see usage")
        run_replay(log_path)
    elif sys.argv[1] == "-h" or sys.argv[1] == "--help":
        print("Usage: python main.py PATH_TO_SIMULATION_LOG")
        return
    else:
        run_replay(sys.argv[1])

if __name__ == "__main__":
    main()
