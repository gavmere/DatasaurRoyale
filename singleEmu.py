import pygame
import random

class SinglePlayerHerbivoreSim:
    def __init__(self, autonomous = False):
        # Initialize Pygame 
        pygame.init()
        self.isAuto= autonomous

        # Set up the window
        self.window_width = 800
        self.window_height = 600
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Behavior tester")

        # Grid settings
        self.grid_size = 20
        self.grid_width = self.window_width // self.grid_size
        self.grid_height = self.window_height // self.grid_size
        self.grid_color = (128, 128, 128)

        # Player settings
        self.player_size = 20
        self.player_color = (255, 0, 0)
        self.player_x = self.grid_width // 4
        self.player_y = self.grid_width // 4
        
        # Enemy Settings
        self.enemy_size = 20
        self.enemy_color = (0, 0, 255)
        self.enemy_x = self.grid_width // 2
        self.enemy_y = self.grid_width // 2 

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
            new_x = random.randint(0, self.grid_width - 2)
            new_y = random.randint(0, self.grid_height - 2)
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
                
    def report_observation(self):
        empty_spaces = []
        red_box_spaces = []
        wall_spaces = []

        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if (x, y) not in self.green_squares and (x, y) != (self.player_x, self.player_y):
                    empty_spaces.append((x, y))
                elif (x, y) == (self.player_x, self.player_y):
                    red_box_spaces.append((x, y))
                elif (x, y) in self.walls:
                    wall_spaces.append((x, y))

        observation = {
            'empty_spaces': empty_spaces,
            'red_box_spaces': red_box_spaces,
            'wall_spaces': wall_spaces
        }
        
        return observation

    def handle_player_movement(self, action=None):
        if not self.isAuto:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.player_x > 0:
                self.player_x -= 1
            elif keys[pygame.K_RIGHT] and self.player_x < self.grid_width - 1:
                self.player_x += 1
            elif keys[pygame.K_UP] and self.player_y > 0:
                self.player_y -= 1
            elif keys[pygame.K_DOWN] and self.player_y < self.grid_height - 1:
                self.player_y += 1
        else:
            if not action:
                Exception('YOU FUCKIN DUMBASS')
            if action == 'left' and self.player_x > 0:
                self.player_x -= 1
            elif action == 'right' and self.player_x < self.grid_width - 1:
                self.player_x += 1
            elif action == 'up' and self.player_y > 0:
                self.player_y -= 1
            elif action == 'down' and self.player_y < self.grid_height - 1:
                self.player_y += 1
            

    def handle_user_behavior(self):
        if not self.isAuto:
            self.handle_player_movement()

        possible_actions = ['left', 'right', 'up', 'down']
        valid_actions = []

        for action in possible_actions:
            if (action == 'left' and (self.player_x-1, self.player_y) not in self.walls) or \
               (action == 'right' and (self.player_x+1, self.player_y) not in self.walls) or \
               (action == 'up' and (self.player_x, self.player_y-1) not in self.walls) or \
               (action == 'down' and (self.player_x, self.player_y+1) not in self.walls):
                valid_actions.append(action)

        if valid_actions:
            action = random.choice(valid_actions)
            self.handle_player_movement(action)

    def check_collisions(self):
        for i, (green_x, green_y) in enumerate(self.green_squares):
            if self.player_x == green_x and self.player_y == green_y:
                self.green_squares.pop(i)
                self.score += 1

        if (self.player_x, self.player_y) in self.walls:
            self.player_x = self.grid_width // 2
            self.player_y = self.grid_height // 2

        if self.player_x == self.enemy_x and self.player_y == self.enemy_y:
            self.running = False

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

    def draw_player(self):
        player_rect = pygame.Rect(self.player_x * self.grid_size, self.player_y * self.grid_size,
                                  self.player_size, self.player_size)
        pygame.draw.rect(self.screen, self.player_color, player_rect)
    
    def draw_enemy(self):
        enemy_rect = pygame.Rect(self.enemy_x * self.grid_size, self.enemy_y * self.grid_size,
                                 self.enemy_size, self.enemy_size)
        pygame.draw.rect(self.screen, self.enemy_color, enemy_rect)

    def draw_score(self):
        score_text = self.score_font.render(f"Score: {self.score}", True, self.score_color)
        self.screen.blit(score_text, (self.score_x, self.score_y))

    def update_display(self):
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.handle_user_behavior()  # Call the new method to handle user-defined behavior
            self.check_collisions()

            self.screen.fill((0, 0, 0))
            self.draw_grid()
            self.draw_green_squares()
            self.draw_walls()
            self.draw_player()
            self.draw_enemy() 
            self.draw_score()
            self.update_display()

            pygame.time.delay(1)

        pygame.quit()

# Create an instance of the SinglePlayerHerbivoreSim class and run the game
game = SinglePlayerHerbivoreSim(autonomous=True)
game.run()
