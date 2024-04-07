import pygame
import random
from Dinosaur import Dinosaur
import DinoFunctions
import GameFunctions


class SinglePlayerHerbivoreSim(Dinosaur):
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Populates environment
        self.dinoList = GameFunctions.populateDinoList(1)
        self.dinoOpp = GameFunctions.populateDinoList(20)
        self.coords = []

        # Set up the window
        self.window_width = 800
        self.window_height = 800
        self.screen = pygame.display.set_mode(
            (self.window_width, self.window_height))
        pygame.display.set_caption("Grid Movement")

        # Grid settings
        self.grid_size = 20
        self.grid_width = self.window_width // self.grid_size
        self.grid_height = self.window_height // self.grid_size
        self.grid_color = (128, 128, 128)

        # Player settings
        self.player_size = 20
        self.player_color = (255, 0, 0)
        self.player_x = 1
        self.player_y = 1

        # Enemy Settings
        self.enemy_size = 20
        self.enemy_color = (0, 0, 255)
        self.enemy_x = self.grid_width // 2
        self.enemy_y = self.grid_width // 2

        # Wall settings
        self.wall_size = 20
        self.wall_color = (0, 0, 0)
        self.walls = [(0, i) for i in range(self.grid_height)]
        self.walls.extend([(self.grid_width - 1, i)
                          for i in range(self.grid_height)])
        self.walls.extend([(i, 0) for i in range(self.grid_width)])
        self.walls.extend([(i, self.grid_height - 1)
                          for i in range(self.grid_width)])

        # Green square settings
        self.green_squares = []
        for _ in range(40):
            new_x = random.randint(0, self.grid_width - 1)
            new_y = random.randint(0, self.grid_height - 1)
            self.coords.append((new_x, new_y))
            self.green_squares.append((new_x, new_y))
        self.green_square_size = 16
        self.green_square_color = (0, 255, 0)

        # Dinosaur settings
        self.dinoPos = {}
        for i in range(len(self.dinoList)):
            self.dino_x = random.randint(1, self.grid_width - 2)
            self.dino_y = random.randint(1, self.grid_height - 2)
            while (self.dino_x, self.dino_y) in self.coords:
                self.dino_x = random.randint(1, self.grid_width - 2)
                self.dino_y = random.randint(1, self.grid_height - 2)
            self.coords.append((self.dino_x, self.dino_y))
            self.dinoPos[self.dinoList[i]] = (self.dino_x, self.dino_y)

        # Enemy settings
        self.dinoOppPos = {}
        for i in range(len(self.dinoOpp)):
            self.dinoOpp_x = random.randint(1, self.grid_width - 2)
            self.dinoOpp_y = random.randint(1, self.grid_height - 2)
            while (self.dinoOpp_x, self.dinoOpp_y) in self.coords:
                self.dinoOpp_x = random.randint(1, self.grid_width - 2)
                self.dinoOpp_y = random.randint(1, self.grid_height - 2)
            self.coords.append((self.dinoOpp_x, self.dinoOpp_y))
            self.dinoOppPos[self.dinoOpp[i]] = (self.dinoOpp_x, self.dinoOpp_y)

        # Score settings
        self.score = 0
        self.score_font = pygame.font.Font(None, 36)
        self.score_color = (255, 255, 255)
        self.score_x = 10
        self.score_y = 10

        # Energy settings
        self.energy = self.dinoList[0].energy
        self.energy_font = pygame.font.Font(None, 36)
        self.energy_color = (255, 255, 255)
        self.energy_x = 10
        self.energy_y = 35

        # Game loop
        self.running = True
        self.reset = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def handle_player_movement(self):
        keys = pygame.key.get_pressed()
        for i in self.dinoList:
            if self.dinoList[0].energy == 0:
                self.dinoPos.pop(i)
                self.dinoList.remove(i)
            elif keys[pygame.K_LEFT] and self.player_x > 0:
                self.newDino_x = self.dinoPos[i][0] - 1
                self.dinoPos[i] = (self.newDino_x, self.dinoPos[i][1])
                self.dinoList[0].energy -= 1
            elif keys[pygame.K_RIGHT] and self.player_x < self.grid_width - 1:
                self.newDino_x = self.dinoPos[i][0] + 1
                self.dinoPos[i] = (self.newDino_x, self.dinoPos[i][1])
                self.dinoList[0].energy -= 1
            elif keys[pygame.K_UP] and self.player_y > 0:
                self.newDino_y = self.dinoPos[i][1] - 1
                self.dinoPos[i] = (self.dinoPos[i][0], self.newDino_y)
                self.dinoList[0].energy -= 1
            elif keys[pygame.K_DOWN] and self.player_y < self.grid_height - 1:
                self.newDino_y = self.dinoPos[i][1] + 1
                self.dinoPos[i] = (self.dinoPos[i][0], self.newDino_y)
                self.dinoList[0].energy -= 1
            elif keys[pygame.K_ESCAPE]:
                self.running = False
                '''print(self.dinoList[0].currHealth)
                print(self.dinoList[0].totalHealth)
                print(self.dinoList[0].carnVal)
                print(self.dinoList[0].herbVal)
                print(self.dinoList[0].energy)
                print(self.dinoList[0].energyConsumption)
                print(self.dinoList[0].power)'''

    def check_collisions(self):
        for i, (green_x, green_y) in enumerate(self.green_squares):
            for j in self.dinoList:
                if self.dinoPos[j][0] == green_x and self.dinoPos[j][1] == green_y:
                    self.green_squares.pop(i)
                    self.score += 1
                    self.dinoList[0].energy += 4

        for i in self.dinoList:
            if self.dinoPos[i] in self.walls:
                self.dinoPos.pop(i)
                self.dinoList.remove(i)

        for i in self.dinoOpp:
            if self.player_x == self.dinoOppPos[i][0] and self.player_y == self.dinoOppPos[i][1]:
                DinoFunctions.combatSimulation(self.dinoList[0], self.dinoOpp[0])
                if not self.dinoList[0].isAlive:
                    self.reset = True
                    print("YOU DIED !!")
                    print("dino stats")
                    print(self.dinoList[0].currHealth)
                    print(self.dinoList[0].totalHealth)
                    print(self.dinoList[0].carnVal)
                    print(self.dinoList[0].herbVal)
                    print(self.dinoList[0].energy)
                    print(self.dinoList[0].energyConsumption)
                    print(self.dinoList[0].power)
                    print()
                    print("dinoOpp stats")
                    print(self.dinoOpp[0].currHealth)
                    print(self.dinoOpp[0].totalHealth)
                    print(self.dinoOpp[0].carnVal)
                    print(self.dinoOpp[0].herbVal)
                    print(self.dinoOpp[0].energy)
                    print(self.dinoOpp[0].energyConsumption)
                    print(self.dinoOpp[0].power)
                elif not self.dinoOpp[0].isAlive:
                    self.dinoOpp.pop()
                    print("OPP DOWN !!")

    def draw_grid(self):
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                rect = pygame.Rect(x * self.grid_size, y *
                                   self.grid_size, self.grid_size, self.grid_size)
                pygame.draw.rect(self.screen, self.grid_color, rect, 1)

    def draw_green_squares(self):
        for green_x, green_y in self.green_squares:
            green_rect = pygame.Rect(green_x * self.grid_size + (self.grid_size - self.green_square_size) // 2,
                                     green_y * self.grid_size +
                                     (self.grid_size - self.green_square_size) // 2,
                                     self.green_square_size, self.green_square_size)
            pygame.draw.rect(self.screen, self.green_square_color, green_rect)

    def draw_walls(self):
        for wallX, wallY in self.walls:
            wallRect = pygame.Rect(
                wallX * self.grid_size, wallY * self.grid_size, self.grid_size, self.grid_size)
            pygame.draw.rect(self.screen, self.wall_color, wallRect)

    def draw_players(self):
        for i in self.dinoList:
            self.player_x = self.dinoPos[i][0]
            self.player_y = self.dinoPos[i][1]
            player_rect = pygame.Rect(self.player_x * self.grid_size, self.player_y * self.grid_size,
                                      self.player_size, self.player_size)
            pygame.draw.rect(self.screen, self.player_color, player_rect)

    def draw_enemy(self):
        for i in self.dinoOpp:
            self.enemy_x = self.dinoOppPos[i][0]
            self.enemy_y = self.dinoOppPos[i][1]
            enemy_rect = pygame.Rect(self.enemy_x * self.grid_size, self.enemy_y * self.grid_size,
                                     self.enemy_size, self.enemy_size)
            pygame.draw.rect(self.screen, self.enemy_color, enemy_rect)

    def draw_score(self):
        score_text = self.score_font.render(
            f"Score: {self.score}", True, self.score_color)
        self.screen.blit(score_text, (self.score_x, self.score_y))

    def draw_energy(self):
        energy_text = self.energy_font.render(
            f"Energy: {self.dinoList[0].energy}", True, self.energy_color)
        self.screen.blit(energy_text, (self.energy_x, self.energy_y))

    def update_display(self):
        pygame.display.flip()

    def resetPos(self):
        self.dinoList = GameFunctions.populateDinoList(1)

        # Dinosaur settings
        self.dinoPos = {}
        for i in range(len(self.dinoList)):
            self.dino_x = random.randint(1, self.grid_width - 2)
            self.dino_y = random.randint(1, self.grid_height - 2)
            while (self.dino_x, self.dino_y) in self.coords:
                self.dino_x = random.randint(1, self.grid_width - 2)
                self.dino_y = random.randint(1, self.grid_height - 2)
            self.coords.append((self.dino_x, self.dino_y))
            self.dinoPos[self.dinoList[i]] = (self.dino_x, self.dino_y)


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
            self.draw_enemy()
            self.draw_score()
            self.draw_energy()
            self.update_display()

            if self.reset:
                self.dinoList.pop()
                self.resetPos()
                self.reset = False

            pygame.time.delay(100)

        pygame.quit()


# Create an instance of the SinglePlayerHerbivoreSim class and run the game
game = SinglePlayerHerbivoreSim()
game.run()
