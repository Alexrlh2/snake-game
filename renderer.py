import pygame

class Renderer():
    """renderer object handles converting grid positions into pixel positions and interaction with pygame module"""

    def __init__(self, window_size, grid_dimensions):
        self.window_size = window_size
        self.grid_dimensions = grid_dimensions
        self.cell_size = (self.window_size[0] / self.grid_dimensions[0], self.window_size[1] / self.grid_dimensions[1])
        self.surface = pygame.display.set_mode(window_size)
        pygame.display.update()
        pygame.display.set_caption('SNAKE!!!')
        pygame.font.init()

    def render_blocks(self, blocks):
        """takes a list of block objects and renders them as squares on the screen"""
        for block in blocks:
            # N.B. pygame coordinates start from top left

            pygame.draw.rect(self.surface, block.colour, [block.posx * self.cell_size[0],
                                                          self.window_size[1] - (block.posy + 1) * self.cell_size[1],
                                                          self.cell_size[0], self.cell_size[1]])

    def update_display(self, blocks):
        """redraws all game elements. takes a list of game objects to be drawn"""
        # currently only configured to render block objects
        self.surface.fill((0, 0, 0))
        self.render_blocks(blocks)
        pygame.display.update()

    def game_over_message(self, level):
        myfont = pygame.font.SysFont('Arial', 38)
        textsurface = myfont.render(f'GAME OVER!!! - LEVEL {level} REACHED', False, (0, 0, 255))
        self.surface.blit(textsurface, ((self.window_size[0] / 2) - (textsurface.get_width() / 2),
                                        (self.window_size[1] / 2) - (textsurface.get_height() / 2)))
        pygame.display.update()

    def new_level_caption(self, level):
        """updates the window caption with new game level"""
        pygame.display.set_caption(f'SNAKE!!! - LEVEL {level}')


def handle_events(snake=None):
    """handles any user input events in the queue. Takes a snake object to direct in response keyboard events.
    Returns "quit" if game has been quit."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "quit"
        if event.type == pygame.KEYDOWN and snake:
            if event.key == pygame.K_UP:
                snake.receive_direction('NORTH')
            elif event.key == pygame.K_RIGHT:
                snake.receive_direction('EAST')
            elif event.key == pygame.K_DOWN:
                snake.receive_direction('SOUTH')
            elif event.key == pygame.K_LEFT:
                snake.receive_direction('WEST')
