import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the window
window_width = 800
window_height = 600
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Grid Movement")

# Grid settings
grid_size = 20
grid_width = window_width // grid_size
grid_height = window_height // grid_size
grid_color = (128, 128, 128)

# Player settings
player_size = 20
player_color = (255, 0, 0)
player_x = grid_width // 2
player_y = grid_height // 2

# Green square settings
green_squares = []
for _ in range(40):
    new_x = random.randint(0, grid_width - 1)
    new_y = random.randint(0, grid_height - 1)
    green_squares.append((new_x, new_y))
green_square_size = 16
green_square_color = (0, 255, 0)

# Score settings
score = 0
score_font = pygame.font.Font(None, 36)
score_color = (255, 255, 255)
score_x = 10
score_y = 10

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= 1
    elif keys[pygame.K_RIGHT] and player_x < grid_width - 1:
        player_x += 1
    elif keys[pygame.K_UP] and player_y > 0:
        player_y -= 1
    elif keys[pygame.K_DOWN] and player_y < grid_height - 1:
        player_y += 1

    # Check for player collisions with green squares
    for i, (green_x, green_y) in enumerate(green_squares):
        if player_x == green_x and player_y == green_y:
            green_squares.pop(i)
            score += 1

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the grid
    for x in range(grid_width):
        for y in range(grid_height):
            rect = pygame.Rect(x * grid_size, y * grid_size, grid_size, grid_size)
            pygame.draw.rect(screen, grid_color, rect, 1)

    # Draw the green squares
    for green_x, green_y in green_squares:
        green_rect = pygame.Rect(green_x * grid_size + (grid_size - green_square_size) // 2,
                                green_y * grid_size + (grid_size - green_square_size) // 2,
                                green_square_size, green_square_size)
        pygame.draw.rect(screen, green_square_color, green_rect)

    # Draw the player
    player_rect = pygame.Rect(player_x * grid_size, player_y * grid_size, player_size, player_size)
    pygame.draw.rect(screen, player_color, player_rect)

    # Draw the score
    score_text = score_font.render(f"Score: {score}", True, score_color)
    screen.blit(score_text, (score_x, score_y))

    # Update the display
    pygame.display.flip()

    # Add a small delay to slow down the movement
    pygame.time.delay(100)

# Quit Pygame
pygame.quit()