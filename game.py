import pygame
import objects
import userio


class Game:
    """The game object coordinates the game and liaises between all objects"""

    def __init__(self, window_size=(800, 600), grid_dimensions=(40, 30)):
        pygame.init()
        self.window_size = window_size
        self.grid_dimensions = grid_dimensions
        self.clock = pygame.time.Clock()
        self.peter = objects.Snake(length=3)
        self.run = True
        self.current_snack = objects.Snack(self.peter, grid_dimensions)
        self.my_renderer = userio.Renderer(window_size, grid_dimensions)
        self.game_speed = 5
        self.level = 0
        # perhaps it is not normal and proper to require so many 'self's

    def game_loop(self):
        """runs the central game-loop"""
        while self.run:
            if self.peter.check_if_eating(self.current_snack):
                self.current_snack.replace(self.peter, self.grid_dimensions)
                self.game_speed = self.game_speed * 1.1
                self.level += 1
                self.my_renderer.new_level_caption(self.level)
            if userio.handle_events(self.peter) == 'quit':
                self.run = False
            self.peter.move(self.grid_dimensions)
            if self.peter.is_ourobouros():
                self.game_over()  # something iffy about having to pass the renderer object to this function. Perhaps whole game coordinator should be an object
            self.my_renderer.update_display([self.current_snack] + self.peter.body)
            self.clock.tick(self.game_speed)

    def game_over(self):
        """displays a game over message and remains in a loop until user quits"""
        self.my_renderer.game_over_message(self.level)
        while self.run:
            if userio.handle_events() == 'quit':
                self.run = False
