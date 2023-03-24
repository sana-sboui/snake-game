import pygame
from pygame.locals import *
import time
import random

SIZE = 40
BACKGROUND_COLOR = (110, 110, 5)

class Apple:

    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/apple.jpg").convert()
        # self.x= SIZE*3 so apple and snake can be in the same line
        self.x = 120
        self.y = 120

    def draw(self):
        # pos of the block in the surface
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0, 24)*SIZE
        self.y = random.randint(0, 19)*SIZE

class Snake:

    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        # load an image
        # if image not in the same folder with python it should be declared this way else just write the image name.jpg
        self.image = pygame.image.load("resources/block.jpg").convert()
        # initialize an empty array of size length
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        self.direction = 'down'

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        # pos of the block in the surface
        for i in range(self.length):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))
        pygame.display.flip()

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw()

class Game:

    def __init__(self):
        # initialize the module
        pygame.init()
        # pygame.display.set_caption("Code basics Snake And Apple Game")
        # creat the surface
        # set_mode is initializing your window (width, height)
        self.surface = pygame.display.set_mode((1000, 800))
        # initialize to play music
        pygame.mixer.init()
        self.play_background_music()
        # surface.fill((255, 255, 255)) gives white color (red, green, blue)
        self.surface.fill((110, 110, 5))
        # creat obj of the Snake class
        self.snake= Snake(self.surface,1)
        self.snake.draw()
        self.apple= Apple(self.surface)
        self.apple.draw()

    def is_collision(self, x1, y1, x2, y2):
        if (x1 >= x2) and (x1 < x2+SIZE):
            if (y1 >= y2) and (y1 < y2 + SIZE):
                return True
        return False

    def is_collision_1(self, x, y):
        if (x == 0) or (x == 1000):
            return True
        if (y == 0) or (y == 800):
            return True
        return False

    def play_background_music(self):
        # diff between Sound (one time) and music (long)
        pygame.mixer.music.load("resources/bg_music_1.mp3")
        pygame.mixer.music.play()

    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg, (0, 0))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # snake colliding with apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound('ding')
            self.snake.increase_length()
            self.apple.move()

        # snake colliding with itself
        for i in range(2, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('crash')
                # print("game over")
                # # exit game
                # exit(0)
                raise "Game over"

        # snake colliding with window
        if self.is_collision_1(self.snake.x[0], self.snake.y[0]):
            self.play_sound('crash')
            raise "Game over"

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('ariel', 30)
        line1 = font.render(f"Game is over loser! Your score is {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("to play again press Enter. To exit press Escape", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.display.flip()
        pygame.mixer.music.pause()

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        # store font into a variable
        score = font.render(f"Score: {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(score, (800,10))

    def run(self):
        running = True
        pause = False

        while running:
            # this will give you all kind of event (keyboard, mouse...)
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                        pause = True
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False
                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(.2)

if __name__ == "__main__":
    game = Game()
    game.run()


