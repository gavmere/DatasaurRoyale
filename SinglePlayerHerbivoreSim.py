import pygame
import random
import Dinosaur
import DinoFunctions
import GameFunctions

# make sure dinosaurs dont populate on grass
# fix randomized dino coords

class SinglePlayerHerbivoreSim:
    def __init__(self):
        # Initialize Pygame 
        pygame.init()

        self.dinoList = GameFunctions.populateDinoList(20)

        # Set up the window
        self.window_width = 800
        self.window_height = 800
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Grid Movement")

        # Grid settings
        self.grid_size = 20
        self.grid_width = self.window_width // self.grid_size
        self.grid_height = self.window_height // self.grid_size
        self.grid_color = (128, 128, 128)

        self.dinoPos = {}
        self.dino_x = random.sample(range(1, self.grid_width-2), len(self.dinoList))
        self.dino_y = random.sample(range(1, self.grid_height-2), len(self.dinoList))
        for i in range(len(self.dinoList)):
            self.dinoPos[self.dinoList[i]] = (self.dino_x[i], self.dino_y[i])

        # Player settings
        self.player_size = 20
        self.player_color = (255, 0, 0)
        self.player_x = 1
        self.player_y = 1

        # Wall settings
        self.wall_size = 20
        self.wall_color = (0, 0, 0)
        self.walls = [(0, i) for i in range(self.grid_height)]
        self.walls.extend([(self.grid_width - 1, i) for i in range(self.grid_height)])
        self.walls.extend([(i, 0) for i in range(self.grid_width)])
        self.walls.extend([(i, self.grid_height - 1) for i in range(self.grid_width)])

        # Green square settings
        self.green_squares = []
        for _ in range(40):
            new_x = random.randint(0, self.grid_width - 1)
            new_y = random.randint(0, self.grid_height - 1)
            self.green_squares.append((new_x, new_y))
        self.green_square_size = 16
        self.green_square_color = (0, 255, 0)

        # Score settings
        self.score = 0
        self.score_font = pygame.font.Font(None, 36)
        self.score_color = (255, 255, 255)
        self.score_x = 10
        self.score_y = 10

        # Game loop
        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def handle_player_movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.player_x > 0:
            self.actionV -= 2*self.actionC
            self.player_x -= self.speed
        elif keys[pygame.K_RIGHT] and self.player_x < self.grid_width - 1:
            self.actionV -= 2*self.actionC
            self.player_x += self.speed
        elif keys[pygame.K_UP] and self.player_y > 0:
            self.actionV -= 2*self.actionC
            self.player_y -= self.speed
        elif keys[pygame.K_DOWN] and self.player_y < self.grid_height - 1:
            self.actionV -= 2*self.actionC
            self.player_y += self.speed

    def check_collisions(self):
        for i, (green_x, green_y) in enumerate(self.green_squares):
            if self.player_x == green_x and self.player_y == green_y:
                self.green_squares.pop(i)
                self.score += 1
                DinoFunctions.eatPlant(self,10)

        if (self.player_x, self.player_y) in self.walls:
            self.player_x = self.grid_width // 2
            self.player_y = self.grid_height // 2

    def draw_grid(self):
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                rect = pygame.Rect(x * self.grid_size, y * self.grid_size, self.grid_size, self.grid_size)
                pygame.draw.rect(self.screen, self.grid_color, rect, 1)

    def draw_green_squares(self):
        for green_x, green_y in self.green_squares:
            green_rect = pygame.Rect(green_x * self.grid_size + (self.grid_size - self.green_square_size) // 2,
                                     green_y * self.grid_size + (self.grid_size - self.green_square_size) // 2,
                                     self.green_square_size, self.green_square_size)
            pygame.draw.rect(self.screen, self.green_square_color, green_rect)

    def draw_walls(self):
        for wallX, wallY in self.walls:
            wallRect = pygame.Rect(wallX * self.grid_size, wallY * self.grid_size, self.grid_size, self.grid_size)
            pygame.draw.rect(self.screen, self.wall_color, wallRect)

    def draw_players(self):
        for i in self.dinoList:
            self.player_x = self.dinoPos[i][0]
            self.player_y = self.dinoPos[i][1]
            player_rect = pygame.Rect(self.player_x * self.grid_size, self.player_y * self.grid_size,
                                    self.player_size, self.player_size)
            pygame.draw.rect(self.screen, self.player_color, player_rect)

    def draw_score(self):
        score_text = self.score_font.render(f"Score: {self.score}", True, self.score_color)
        self.screen.blit(score_text, (self.score_x, self.score_y))

    def update_display(self):
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.handle_player_movement()
            self.check_collisions()

            self.screen.fill((0, 0, 0))
            self.draw_grid()
            self.draw_green_squares()
            self.draw_walls()
            self.draw_players()
            self.draw_score()
            self.update_display()

            pygame.time.delay(100)

        pygame.quit()

# Create an instance of the SinglePlayerHerbivoreSim class and run the game
game = SinglePlayerHerbivoreSim()
game.run()
