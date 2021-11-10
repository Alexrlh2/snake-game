import random

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Block:
    """block objects are placed on the grid and represented visually by a coloured square"""

    def __init__(self, pos=(0,0), colour=RED):
        self.colour = colour
        self.posx = pos[0]
        self.posy = pos[1]

    def collides_with(self, other_block):
        if (self.posx, self.posy) == (other_block.posx, other_block.posy):
            return True
        else:
            return False


class Snack(Block):
    def __init__(self, snake, grid_dimensions, colour=GREEN):
        """places snack object randomly. takes a snake object to avoid placing snack under snake. takes grid dimensions tuple to select random location within
        :type grid_dimensions: tuple
        """
        self.replace(snake, grid_dimensions)
        super().__init__((self.posx, self.posy), colour)

    def replace(self,snake, grid_dimensions):
        """Replaces the block randomly. Takes a snake object to avoid placing snack under snake. Called when snack is
        eaten and in snack initialisation. Takes grid dimensions tuple to select random location within grid """
        unavailable_locations = []
        for block in snake.body:
            unavailable_locations.append((block.posx, block.posy))
        collision = True
        while collision:
            self.posx = random.randrange(grid_dimensions[0]-1)
            self.posy = random.randrange(grid_dimensions[1]-1)
            print(f'snack at {self.posx, self.posy}')
            if (self.posx, self.posy) not in unavailable_locations:
                collision = False

class Snake:
    """Snake objects are composed of block objects"""

    NORTH = (0, 1)
    EAST = (1, 0)
    SOUTH = (0, -1)
    WEST = (-1, 0)

    def __init__(self, pos=(1, 1), length=1, dirn=EAST):
        self.dirn = dirn
        self.posx = pos[0]
        self.posy = pos[1]
        self.last_move = (0, 0)
        self.body = []
        # append blocks to the body, positioned sequentially in reverse of snake direction
        for i in range(length):
            self.body.append(
                Block((self.posx + i * -self.dirn[0], self.posy + i * -self.dirn[1]), colour=RED))

    def grow(self):
        """appends a new block to the body"""
        # adding the block over the tail block gives correct functionality. This made sense but I can't remember why.
        self.body.append(Block((self.body[-1].posx, self.body[-1].posy), colour=RED))

    def move(self, grid_dimensions):
        """moves the head in the current direction. Other body blocks follow their anterior. Takes grid dimensions so
        blocks can teleport edge to edge """
        # iterate from tail to head, moving each block to the position of its anterior. Head moves with direction
        for i in range(len(self.body) - 1, -1, -1):
            if i == 0:
                self.body[i].posx += self.dirn[0]
                self.body[i].posy += self.dirn[1]
            else:
                self.body[i].posx = self.body[i - 1].posx
                self.body[i].posy = self.body[i - 1].posy
        self.last_move = self.dirn
        for block in self.body:
            if block.posx < 0:
                block.posx += grid_dimensions[0]
            if block.posy < 0:
                block.posy += grid_dimensions[1]
            if block.posx >= grid_dimensions[0]:
                block.posx -= grid_dimensions[0]
            if block.posy >= grid_dimensions[1]:
                block.posy -= grid_dimensions[1]

    def is_ourobouros(self):
        """returns true if snake is biting its tail."""
        if len(self.body) < 4:
            return False
        for block in self.body[2:]:
            if block.collides_with(self.body[0]):
                print('peter bites his tail!')
                return True
        else:
            return False

    def receive_direction(self, direction_command):
        """takes a direction tuple and updates snake direction unless new direction is inverse of current direction (
        snake cannot turn 180 degrees!) """
        if direction_command =='NORTH':new_dirn = Snake.NORTH
        elif direction_command == 'EAST': new_dirn = Snake.EAST
        elif direction_command == 'SOUTH': new_dirn = Snake.SOUTH
        elif direction_command == 'WEST': new_dirn = Snake.WEST
        if new_dirn[0] + self.last_move[0] != 0 and new_dirn[1] + self.last_move[1] != 0:
            self.dirn = new_dirn

    def check_if_eating(self, snack):
        """takes a snack object. Returns true and grows the snake if snack has passed through body (touching tail)."""
        if self.body[-1].collides_with(snack):
            self.grow()
            print('peter is eating the snack!')
            return True
        return False






