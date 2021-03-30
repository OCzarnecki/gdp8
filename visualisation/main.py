import sys, pygame
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
pygame.init()
SIZE = (300, 600)
SCREEN = pygame.display.set_mode(SIZE)

class WorldPainting():
    """
    contains a surface with everything simulation drawn on
    relies on State only
    drawn through camera
    """
    def __init__(self, state):
        self.tileWidth = 64
        surfaceSize = (self.tileWidth * state.x_size, self.tileWidth * state.y_size)
        self.surface = pygame.Surface(surfaceSize)

    def draw(self, state):
        for cell in state.cells:
            self.drawCell(cell)
        for agent in state.agents:
            self.drawAgent(agent)

    def drawCell(self, cell): # just draws blue
        x = cell.x * self.tileWidth
        y = cell.y * self.tileWidth
        rect = pygame.Rect(x, y, self.tileWidth, self.tileWidth)
        pygame.draw.rect(self.surface, (0, 0, 255), rect)

    def drawAgent(self, agent):
        center_x = (agent.x + 0.5) * self.tileWidth
        center_y = (agent.y + 0.5) * self.tileWidth
        center = (center_x, center_y)
        pygame.draw.circle(self.surface, (127, 127, 0), center, self.tileWidth / 3.)

class Camera():
    """
    How the world painting is drawn on the window.
    Top 2/3 of screen.
    Features can include movement, zoom, filters.
    """

    def __init__(self, x=0., y=0.):
        self.x = x # relative to world painting
        self.y = y
        self.size = SIZE

    def draw(self, screen, painting):
        # int because blit only allows int
        paintingLocation = (int(0-self.x), int(0-self.y))
        screen.blit(painting.surface, paintingLocation)

if __name__ == "__main__":

    time = 0
    state = State("")
    painting = WorldPainting(state)
    camera = Camera()

    """
    Main loop, shows how the classes interact.
    """
    while 1:

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        state.load(time)
        painting.draw(state)

        SCREEN.fill((0,0,0))
        camera.draw(SCREEN, painting)
        pygame.display.flip()
