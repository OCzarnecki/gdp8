import sys, pygame, json
from simulationState import State
"""
Plan:
to do for first iteration:
1. Include user interface (a basic version, lower 1/3 of screen) √
    Features may include:
        labels for simulation time and how many agents survive
        a way to reset the visualiser
2. Interface with JSON to implement State.load
    create some simulation logs to make sure the visuals are working
3. Make the initial SCREEN not be noise
4. Make main loop play the simulation forward in a simple way √
    ideas:
        press a button to advance by one time step
        let the time tick forward every x seconds
5. Make WorldPainting reflect the water levels of cells and agents

Notes:
1. coordinates are (0, 0) on topleft in pygame. We may want to flip y coordinates if we want (0, 0) to be bottom left
2. There is a bug where sometimes pressing left or right crashes with a memory error.
"""
pygame.init()
pygame.display.set_caption('AEA Desert')
pygame.font.init()
WIDTH = 900
HEIGHT = 600
SIZE = (WIDTH, HEIGHT)
SCREEN = pygame.display.set_mode(SIZE)

def colorPercentage(n):
    return 255 * (n / 100.0)

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
            self.drawCell(cell, state.max_water_capacity)
        for agent in state.agents:
            self.drawAgent(agent)

    def drawCell(self, cell, max_water_capacity):
        if (max_water_capacity != 0):
            x = cell.x * self.tileWidth
            y = cell.y * self.tileWidth
            rect = pygame.Rect(x, y, self.tileWidth, self.tileWidth)
            pygame.draw.rect(self.surface, (0, 0, colorPercentage((cell.water/max_water_capacity)*100)), rect)

    def drawAgent(self, agent):
        center_x = (agent.x + 0.5) * self.tileWidth
        center_y = (agent.y + 0.5) * self.tileWidth
        center = (center_x, center_y)
        pygame.draw.circle(self.surface,
            (colorPercentage(100 - agent.inventory), colorPercentage(agent.inventory), 0),
            center, self.tileWidth / 3.)

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

class Slider():

    def __init__(self, length, pos, left_text, right_text, head_text=""):
        self.length = length
        self.pos = pos # 0 to 1, left to right position of slider head
        self.left_text = left_text
        self.right_text = right_text
        self.head_text = head_text
        self.slider_text = pygame.font.SysFont("Times New Roman", 18)

        self.left_label = self.slider_text.render(self.left_text, False, (0,0,0))
        self.right_label = self.slider_text.render(self.right_text, False, (0,0,0))
        self.head_label = self.slider_text.render(self.head_text, False, (0,0,0))

    def render(self):
        length = self.length
        pos = self.pos
        slider_text = self.slider_text

        left_text_width, left_text_height = self.slider_text.size(self.left_text)
        right_text_width, right_text_height = self.slider_text.size(self.right_text)
        bar_length = length - left_text_width - right_text_width
        head_text_width, head_text_height = self.slider_text.size(self.head_text)

        # transparent surface
        ret = pygame.Surface((length, 100), pygame.SRCALPHA, 32)
        ret = ret.convert_alpha()

        slider_bar = pygame.Rect(left_text_width, 35, bar_length, 30)
        pygame.draw.rect(ret, (0,0,0), slider_bar)

        head_width = 10 # may be better in instance variable
        head_height = 50
        real_head_pos = left_text_width + round(pos * bar_length)
        head_x = real_head_pos - (head_width // 2)
        head_y = 50 - (head_height // 2)
        slider_head = pygame.Rect(head_x, head_y, head_width, head_height)
        pygame.draw.rect(ret, (0,0,0), slider_head)

        head_label_x = real_head_pos - (head_text_width // 2)
        head_label_y = 50 + (head_height // 2)
        ret.blit(self.head_label, (head_label_x, head_label_y))

        left_label_y = 50 - (left_text_height // 2)
        right_label_y = 50 - (right_text_height // 2)
        ret.blit(self.left_label, (0, right_label_y))
        ret.blit(self.right_label, (length-right_text_width, right_label_y))
        return ret


class UserInterface():

    def __init__(self):
        self.rect_background = pygame.Rect(0, 400, WIDTH, 200)
        self.K_L_DOWN = False
        self.K_R_DOWN = False


    def draw(self, screen, state):
        beige = (240, 209, 116)
        pygame.draw.rect(screen, beige, self.rect_background)

        self.draw_tutorial_label(screen, state)
        self.draw_time_slider(screen, state)
        self.draw_agent_slider(screen, state)

    def draw_tutorial_label(self, screen, state):
            small_text = pygame.font.SysFont("Times New Roman", 16)
            tutorial_text = "Left/Right keys to change time"
            tutorial_label = small_text.render(tutorial_text, False, (0,0,0))
            screen.blit(tutorial_label, (0, 400))

    def draw_time_slider(self, screen, state):
        time_prop = state.time / state.max_time
        time_slider = Slider(
            300,
            time_prop,
            "time: ",
            " {}".format(state.max_time),
            str(state.time)
        )
        screen.blit(time_slider.render(), (0, 500))

    def draw_agent_slider(self, screen, state):
        agent_prop = state.count_survivors() / state.max_agent

        agent_slider = Slider(
            300,
            agent_prop,
            "survivors: ",
            " {}".format(state.max_agent),
            str(state.count_survivors())
        )
        screen.blit(agent_slider.render(), (0, 420))


    def process(self, event, state): # updates state time based on pygame.event
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and not self.K_L_DOWN:
                self.K_L_DOWN = True
                state.load(max(0, state.time-1))
                print("Time {}".format(state.time))
            elif event.key == pygame.K_RIGHT and not self.K_R_DOWN:
                self.K_R_DOWN = True
                state.load(min(state.max_time, state.time+1))
                print("Time {}".format(state.time))
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and self.K_L_DOWN:
                self.K_L_DOWN = False
            if event.key == pygame.K_RIGHT and self.K_R_DOWN:
                self.K_R_DOWN = False


if __name__ == "__main__":

    state = State("example_logs/spiral.json")

    painting = WorldPainting(state)
    camera = Camera()
    ui = UserInterface()

    """
    Main loop, shows how the classes interact.
    """
    while 1:

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            ui.process(event, state)

        painting.draw(state)

        SCREEN.fill((0,0,0))
        camera.draw(SCREEN, painting)
        ui.draw(SCREEN, state)
        pygame.display.flip()
