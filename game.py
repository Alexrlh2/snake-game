import pygame
import items
import userio
import math


class Game:
    """The game object coordinates the game and liaises between all objects"""

    def __init__(self, window_size=(800, 600), grid_dimensions=(40, 30), base_game_speed=6):
        pygame.init()
        self.window_size = window_size
        self.grid_dimensions = grid_dimensions
        self.clock = pygame.time.Clock()
        self.snake = items.Snake(length=3)
        self.run = True
        self.current_snack = items.Snack(self.snake, grid_dimensions)
        self.my_renderer = userio.Renderer(window_size, grid_dimensions)
        self.base_game_speed = base_game_speed
        self.game_speed = self.base_game_speed
        self.level = 0
        # perhaps it is not normal and proper to require so many 'self's

    def increase_game_speed(self):
        """increases the game speed with a function found to give a pleasant speed curve and difficulty"""
        self.game_speed = self.base_game_speed + math.log(2 * self.level,1.5) + 0.2

    def game_loop(self):
        """runs the central game-loop"""
        while self.run:
            if self.snake.check_if_eating(self.current_snack):
                self.current_snack.replace(self.snake, self.grid_dimensions)
                self.level += 1
                self.increase_game_speed()
                self.my_renderer.new_level_caption(self.level)
            if userio.handle_events(self.snake) == 'quit':
                self.run = False
            self.snake.move(self.grid_dimensions)
            if self.snake.is_ourobouros():
                self.game_over()  # something iffy about having to pass the renderer object to this function. Perhaps whole game coordinator should be an object
            self.my_renderer.update_display([self.current_snack] + self.snake.body)
            self.clock.tick(self.game_speed)

    def game_over(self):
        """displays a game over message and remains in a loop until user quits"""
        self.my_renderer.game_over_message(self.level)
        while self.run:
            if userio.handle_events() == 'quit':
                self.run = False
