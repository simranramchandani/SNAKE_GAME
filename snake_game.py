# snake_game.py
# ------------------------------------------------------------
# This script implements a classic Snake game using Pygame.
# It supports keyboard control or an optional external callback
# (e.g., camera-based gesture control) to change direction.
#
# The game includes:
# - A start screen
# - A main game loop
# - A game over screen
# - Grid rendering, food spawning, and collision detection
# ------------------------------------------------------------

import pygame
import random

# Game configuration
GAME_WIDTH, GAME_HEIGHT = 600, 400
SPEED = 2               # Game speed (frames per second)
SPACE_SIZE = 20         # Size of each grid cell
BODY_PARTS = 2          # Initial snake length

# Colors (R, G, B)
SNAKE_COLOR = (0, 255, 0)   #neon green
FOOD_COLOR = (255, 0, 150)  #pinkish red
BG_COLOR = (10, 10, 10)     #dark background
GRID_COLOR = (0, 255, 255)  #cyan grid lines

# Initial movement direction
direction = "right"


# ------------------------------------------------------------
# Snake Class
# ------------------------------------------------------------
class Snake:
    def __init__(self):
        """
        Initialize the snake body as a list of grid-aligned coordinates.
        The snake starts with BODY_PARTS segments in a straight line.
        """
        self.coordinates = [[100 - i * SPACE_SIZE, 100] for i in range(BODY_PARTS)]

    def move(self):
        """
        Move the snake by inserting a new head based on the direction
        and removing the last segment (unless growing).
        """
        x, y = self.coordinates[0]

        # Movement vectors for each direction
        dx, dy = {
            "up": (0, -SPACE_SIZE),
            "down": (0, SPACE_SIZE),
            "left": (-SPACE_SIZE, 0),
            "right": (SPACE_SIZE, 0)
        }[direction]

        # Insert new head and remove tail
        self.coordinates.insert(0, [x + dx, y + dy])
        self.coordinates.pop()

    def grow(self):
        """
        Extend the snake by duplicating the last segment.
        """
        self.coordinates.append(self.coordinates[-1])


# ------------------------------------------------------------
# Food Class
# ------------------------------------------------------------
class Food:
    def __init__(self):
        """
        Spawn food at a random grid-aligned position.
        """
        self.x = random.randrange(0, GAME_WIDTH, SPACE_SIZE)
        self.y = random.randrange(0, GAME_HEIGHT, SPACE_SIZE)


# ------------------------------------------------------------
# Direction Handling
# ------------------------------------------------------------
def change_direction(new_dir):
    """
    Change direction unless the new direction is the opposite
    of the current one (prevents reversing into yourself).
    """
    global direction
    opposites = {"up": "down", "down": "up", "left": "right", "right": "left"}

    if new_dir and opposites[direction] != new_dir:
        direction = new_dir


# ------------------------------------------------------------
# Collision Detection
# ------------------------------------------------------------
def check_collision(snake):
    """
    Returns True if the snake hits the wall or its own body.
    """
    head = snake.coordinates[0]

    # Wall collision
    if head[0] < 0 or head[0] >= GAME_WIDTH or head[1] < 0 or head[1] >= GAME_HEIGHT:
        return True

    # Self collision
    if head in snake.coordinates[1:]:
        return True

    return False


# ------------------------------------------------------------
# Start Screen
# ------------------------------------------------------------
def start_screen(screen):
    """
    Display a simple start screen that waits for the player
    to press SPACE before beginning the game.
    """
    title_font = pygame.font.SysFont("Arial", 40)
    small_font = pygame.font.SysFont("Arial", 25)

    while True:
        screen.fill((10, 10, 10))

        title = title_font.render("SNAKE GAME", True, (0, 255, 0))
        prompt = small_font.render("Press SPACE to Start", True, (0, 255, 255))

        screen.blit(title, (GAME_WIDTH // 2 - title.get_width() // 2, 120))
        screen.blit(prompt, (GAME_WIDTH // 2 - prompt.get_width() // 2, 200))

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                return True


# ------------------------------------------------------------
# Game Over Screen
# ------------------------------------------------------------
def game_over_screen(screen):
    """
    Display a game over screen with options to restart (R)
    or quit (Q).
    """
    title_font = pygame.font.SysFont("Arial", 40)
    small_font = pygame.font.SysFont("Arial", 25)

    while True:
        screen.fill((10, 10, 10))

        over = title_font.render("GAME OVER", True, (255, 0 , 150))
        prompt = small_font.render("Press R to Restart or Q to Quit", True, (0, 255, 0))

        screen.blit(over, (GAME_WIDTH // 2 - over.get_width() // 2, 120))
        screen.blit(prompt, (GAME_WIDTH // 2 - prompt.get_width() // 2, 200))

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "quit"
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:
                    return "restart"
                if e.key == pygame.K_q:
                    return "quit"


# ------------------------------------------------------------
# Main Game Loop
# ------------------------------------------------------------
def run_game(direction_callback=None):
    """
    Runs the Snake game. If a direction_callback is provided,
    it overrides keyboard input (e.g., camera gesture control).
    """
    global direction

    pygame.init()
    screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
    clock = pygame.time.Clock()

    # Show start screen
    if not start_screen(screen):
        pygame.quit()
        return

    # Game restart loop
    while True:
        direction = "right"
        snake = Snake()
        food = Food()
        running = True

        # Main gameplay loop
        while running:
            # Handle keyboard input
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                elif e.type == pygame.KEYDOWN:
                    keys = {
                        pygame.K_UP: "up",
                        pygame.K_DOWN: "down",
                        pygame.K_LEFT: "left",
                        pygame.K_RIGHT: "right"
                    }
                    change_direction(keys.get(e.key))

            # Optional camera-based direction override
            if direction_callback:
                change_direction(direction_callback() or direction)

            # Move snake
            snake.move()

            # Check for collisions
            if check_collision(snake):
                break

            # Check if food is eaten
            if snake.coordinates[0] == [food.x, food.y]:
                snake.grow()
                food = Food()

            # Draw background
            screen.fill(BG_COLOR)

            # Draw grid
            for x in range(0, GAME_WIDTH, SPACE_SIZE):
                pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, GAME_HEIGHT))
            for y in range(0, GAME_HEIGHT, SPACE_SIZE):
                pygame.draw.line(screen, GRID_COLOR, (0, y), (GAME_WIDTH, y))

            # Draw snake
            for x, y in snake.coordinates:
                pygame.draw.rect(screen, SNAKE_COLOR, (x, y, SPACE_SIZE, SPACE_SIZE))

            # Draw food
            pygame.draw.rect(screen, FOOD_COLOR, (food.x, food.y, SPACE_SIZE, SPACE_SIZE))

            pygame.display.flip()
            clock.tick(SPEED)

        # Show game over screen
        action = game_over_screen(screen)
        if action == "quit":
            break

    pygame.quit()


# Run game normally if executed directly
if __name__ == "__main__":
    run_game()