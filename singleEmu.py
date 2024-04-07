import pygame
import random
import DinoFunctions
from GameFunctions import populateDinoList
from Dinosaur import goToGreensOnly, goToNearestDino, fiftyFftydinoPlans, cowardDino, randomBehav, paralyzed, getStats, copDino, colorblindDino


class Fullsimulation:
    window_width = 1920
    window_height = 1080
    grid_size = 20
    grid_color = (128, 128, 128)
    green_square_size = 16
    green_square_color = (0, 255, 0)
    wall_color = (255, 255, 255)
    score_color = (255, 255, 255)
    score_x = 10
    score_y = 10
    defaultNumPlants = 40

    def __init__(self, autonomous=False, funmode = False):
        self.funmode = funmode
        self.green_square_image = pygame.image.load("image.png")
        self.green_square_image = pygame.transform.scale(self.green_square_image, (self.green_square_size, self.green_square_size))
        self.isAuto = autonomous
        self.screen = pygame.display.set_mode(
            (self.window_width, self.window_height))
        pygame.init()
        pygame.display.set_caption("Behavior tester")
        self.grid_width = self.window_width // self.grid_size
        self.grid_height = self.window_height // self.grid_size
        self.score_font = pygame.font.Font(None, 36)
        self.running = True
        self.dinos = populateDinoList(16)
        self.dino_pos = []
        self.death = []
        self.behaviors = [goToGreensOnly, goToNearestDino, fiftyFftydinoPlans, cowardDino, randomBehav, paralyzed, copDino, colorblindDino]
        self.dino_behaviorFunc = {i: random.choice(
            self.behaviors) for i in self.dinos}
        for i in self.dino_behaviorFunc.items():
            i[0].dino_behavior = i[1]
        self.walls = [(0, i) for i in range(self.grid_height)] + [(self.grid_width - 1, i) for i in range(self.grid_height)] + \
            [(i, 0) for i in range(self.grid_width)] + \
            [(i, self.grid_height - 1) for i in range(self.grid_width)]
        for dino in self.dinos:
            dino.dino_walls = self.walls
        self.green_squares = []
        self.generate_new_plants(self.defaultNumPlants)
        self.score = 0
        self.currGeneration = 0
        self.logfile = open('winnerlog.txt', 'w')

    def generate_new_plants(self, numPlants=None):
        if not numPlants:
            numPlants = self.defaultNumPlants
        for _ in range(numPlants):
            new_x = random.randint(1, self.grid_width - 2)
            new_y = random.randint(1, self.grid_height - 2)
            self.green_squares.append((new_x, new_y))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def report_observation(self):
        observation = {
            'dino_spaces': [(x, y) for x, y in self.dino_pos],
            'empty_spaces': [(x, y) for x in range(self.grid_width) for y in range(self.grid_height) if (x, y) not in self.green_squares and (x, y) not in self.dino_pos],
            'red_box_spaces': [(self.dino_x, self.dino_y)],
            'wall_spaces': self.walls
        }
        return observation

    def handle_dino_movement(self, dino, action=None):
        if not self.isAuto:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and dino.dino_x > 0:
                dino.dino_x -= 1
                dino.energy -= 1
            elif keys[pygame.K_RIGHT] and dino.dino_x < self.grid_width - 1:
                dino.dino_x += 1
                dino.energy -= 1
            elif keys[pygame.K_UP] and dino.dino_y > 0:
                dino.dino_y -= 1
                dino.energy -= 1
            elif keys[pygame.K_DOWN] and dino.dino_y < self.grid_height - 1:
                dino.dino_y += 1
                dino.energy -= 1
        else:
            if not action or action == "stay":
                dino.energy -= 1
                return
            if action == 'left' and dino.dino_x > 0:
                dino.dino_x -= 1
                dino.energy -= 1
            elif action == 'right' and dino.dino_x < self.grid_width - 1:
                dino.dino_x += 1
                dino.energy -= 1
            elif action == 'up' and dino.dino_y > 0:
                dino.dino_y -= 1
                dino.energy -= 1
            elif action == 'down' and dino.dino_y < self.grid_height - 1:
                dino.dino_y += 1
                dino.energy -= 1

    def handle_dino_behavior(self, dino, observations):
        if not self.isAuto:
            self.handle_dino_movement(dino)
        self.handle_dino_movement(dino, dino.calculateNextStep(
            observations, self.dino_behaviorFunc[dino]))

    def update_all_Dino_pos(self):
        self.dino_pos = [(dino.dino_x, dino.dino_y) for dino in self.dinos]

    def checkEnergy(self, dino):
        if dino.energy <= 0:
            self.death.append(dino)
            self.dinos.remove(dino)

    def check_collisions(self, dino):
        for i, (green_x, green_y) in enumerate(self.green_squares):
            if dino.dino_x == green_x and dino.dino_y == green_y:
                self.green_squares.remove((green_x, green_y))
                self.score += 1
                dino.energy += 5 * dino.herbVal

        if (dino.dino_x, dino.dino_y) in self.walls and dino in self.dinos:
            self.death.append(dino)
            self.dinos.remove(dino)
        if dino in self.dinos:
            for new_dino in [self.dinos[i] for i, (x,y) in enumerate(self.dino_pos) if x == dino.dino_x and y == dino.dino_y and dino != self.dinos[i]]:
                DinoFunctions.combatSimulation(dino,new_dino)
                if not dino.isAlive:
                    new_dino.energy += dino.energyConsumption * new_dino.carnVal
                    self.death.append(dino)
                    self.dinos.remove(dino)
                elif not new_dino.isAlive:
                    dino.energy += new_dino.energyConsumption * dino.carnVal
                    self.death.append(new_dino)
                    self.dinos.remove(new_dino)
    
    def draw_grid(self):
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                rect = pygame.Rect(x * self.grid_size, y *
                                   self.grid_size, self.grid_size, self.grid_size)
                pygame.draw.rect(self.screen, self.grid_color, rect, 1)

    def draw_green_squares_spritemode(self):
        for green_x, green_y in self.green_squares:
            green_rect = pygame.Rect(green_x * self.grid_size + (self.grid_size - self.green_square_size) // 2,
                                    green_y * self.grid_size + (self.grid_size - self.green_square_size) // 2,
                                    self.green_square_size, self.green_square_size)
            self.screen.blit(self.green_square_image, green_rect)
    def draw_green_squares(self):
        for green_x, green_y in self.green_squares:
            green_rect = pygame.Rect(green_x * self.grid_size + (self.grid_size - self.green_square_size) // 2,
                                    green_y * self.grid_size + (self.grid_size - self.green_square_size) // 2,
                                    self.green_square_size, self.green_square_size)
            self.screen.blit(self.green_square_image, green_rect)
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

    def draw_dino(self, dino):
        player_rect = pygame.Rect(dino.dino_x * self.grid_size,
                                  dino.dino_y * self.grid_size, self.grid_size, self.grid_size)
        pygame.draw.rect(self.screen, dino.dino_color, player_rect)

    def draw_score(self):
        score_text = self.score_font.render(f"Score: {self.score}", True, self.score_color)
        self.screen.blit(score_text, (self.score_x, self.score_y))
    def draw_generation(self):
        score_text = self.score_font.render(f"Generation: {self.currGeneration}", True, self.score_color)
        self.screen.blit(score_text, (self.score_x, self.score_y))
        
    def update_display(self):
        pygame.display.flip()
    
    def reset_game(self):
        print(f'generation {self.currGeneration}:' + getStats(self.dinos[0]), file=self.logfile)
        self.dinos = populateDinoList(12)
        self.dino_pos = []
        self.behaviors = [goToGreensOnly, goToNearestDino, fiftyFftydinoPlans, cowardDino, randomBehav, paralyzed]
        self.dino_behaviorFunc = {i: random.choice(self.behaviors) for i in self.dinos}
        for i in self.dino_behaviorFunc.items():
            i[0].dino_behavior = i[1]
        self.old_gen = self.death[-8:]
        self.death = []
        for i in range(0,7,2):
            self.dinos.append(self.old_gen[i+1].child(self.old_gen[i]))
        for i in self.dinos[-4:]:
            self.dino_behaviorFunc[i] = i.dino_behavior
        for dino in self.dinos:
            dino.dino_walls = self.walls
        self.green_squares = []
        self.generate_new_plants(self.defaultNumPlants)
        self.currGeneration += 1

    def observeState(self, currDino):
        other_dino_positions = []
        other_dino_powers = []
        other_dino_colors = []
        other_dino_energy_consumption = []
        other_dino_energy = []
        other_dino_herb = []
        other_dino_carn = []

        for dino in self.dinos:
            if (dino.dino_x, dino.dino_y) != (currDino.dino_x, currDino.dino_y):
                other_dino_positions.append((dino.dino_x, dino.dino_y))
                other_dino_powers.append(dino.power)
                other_dino_colors.append((dino.dino_color, (dino.dino_x, dino.dino_y)))
                other_dino_energy_consumption.append(dino.energyConsumption)
                other_dino_energy.append(dino.energy)
                other_dino_carn.append(dino.carnVal)
                other_dino_carn.append(dino.herbVal)
                other_dino_carn.append(dino.dino_behavior)

        observation = {
            'empty_spaces': [(x, y) for x in range(self.grid_width) for y in range(self.grid_height) if (x, y) not in self.green_squares and (x, y) != (currDino.dino_x, currDino.dino_y)],
            'green_spaces': list(self.green_squares),
            'wall_spaces': self.walls,
            'other_dino_positions': other_dino_positions,
            'other_dino_powers': other_dino_powers,
            'other_dino_colors': other_dino_colors,
            'other_dino_energy_consumption': other_dino_energy_consumption,
            'other_dino_energy': other_dino_energy,
            'other_dino_herb': other_dino_herb,
            'other_dino_carn': other_dino_carn
        }

        return observation

    def run(self):
        while self.running:
            self.screen.fill((0, 0, 0))
            self.draw_walls()
            self.draw_grid()
            self.handle_events()
            for dino in self.dinos:
                self.handle_dino_behavior(dino, self.observeState(dino))
                self.checkEnergy(dino)
                self.update_all_Dino_pos()
                self.check_collisions(dino)
                if len(self.green_squares) == 0:
                    self.generate_new_plants()
                if len(self.dinos) <= 1:
                    self.reset_game()
                self.draw_dino(dino)
                
                if self.funmode:
                    self.draw_green_squares_spritemode()
                else:
                    self.draw_green_squares()
                self.draw_generation()
                self.update_all_Dino_pos()
            self.update_display()
            pygame.time.delay(16)
        self.logfile.close()
        pygame.quit()


# Create an instance of the Fullsimulation class and run the game
game = Fullsimulation(autonomous=True, funmode=True)
game.run()


