import game

WINDOW_SIZE = (800, 600)
GRID_DIMENSIONS = (40, 30)


def main():
    new_game = game.Game()
    new_game.game_loop()


if __name__ == '__main__':
    main()
