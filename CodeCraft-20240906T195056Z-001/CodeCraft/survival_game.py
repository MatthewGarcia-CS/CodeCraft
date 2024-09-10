import pgzrun
import pygame
import random
import os

# Game constants
MIN_WIDTH = 1280  # Minimum window width
MIN_HEIGHT = 720  # Minimum window height
TARGET_WIDTH = 1280
TARGET_HEIGHT = 720
PLAYER_SPEED = 5
OBSTACLE_WIDTH = 50
OBSTACLE_FREQ = 30
MIN_OBSTACLE_SPEED = 10
MAX_OBSTACLE_SPEED = 15

# Initialize game variables
alien = Actor('alien')
obstacles = []
score = 0
game_over = False
frame_count = 0

def setup():
    global WIDTH, HEIGHT
    
    # Center the window
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    
    # Set up the display
    pygame.init()
    screen_info = pygame.display.Info()
    screen_width, screen_height = screen_info.current_w, screen_info.current_h
    
    # Adjust game window size if it's larger than the screen
    WIDTH = max(MIN_WIDTH, min(TARGET_WIDTH, screen_width - 100))
    HEIGHT = max(MIN_HEIGHT, min(TARGET_HEIGHT, screen_height - 100))
    
    # Set the window size
    os.environ['SDL_VIDEO_WINDOW_POS'] = '%d,%d' % ((screen_width - WIDTH) // 2, (screen_height - HEIGHT) // 2)
    pygame.display.set_mode((WIDTH, HEIGHT))
    
    # Position the alien
    alien.pos = WIDTH // 2, HEIGHT - 50

def draw():
    screen.clear()  # Clear the screen with the default background color
    if not game_over:
        alien.draw()
        for obstacle in obstacles:
            obstacle.draw()
        screen.draw.text(f"Score: {score}", topleft=(10, 10), fontsize=30, color="white")
    else:
        screen.draw.text("Game Over", center=(WIDTH // 2, HEIGHT // 2), fontsize=50, color="red")
        screen.draw.text(f"Final Score: {score}", center=(WIDTH // 2, HEIGHT // 2 + 60), fontsize=30, color="white")

def create_obstacle():
    obstacle = Actor('astroid')
    obstacle.width = OBSTACLE_WIDTH
    obstacle.height = int(obstacle.height * (OBSTACLE_WIDTH / obstacle.width))  # Maintain aspect ratio
    return obstacle

def update():
    global frame_count, score, game_over
    
    if not game_over:
        if keyboard.left and alien.left > 0:
            alien.x -= PLAYER_SPEED
        if keyboard.right and alien.right < WIDTH:
            alien.x += PLAYER_SPEED
        
        for obstacle in obstacles:
            obstacle.y += obstacle.speed
            if obstacle.colliderect(alien):
                game_over = True
            elif obstacle.top > HEIGHT:
                obstacles.remove(obstacle)
                score += 1
        
        # Add new obstacles
        frame_count += 1
        if frame_count % OBSTACLE_FREQ == 0:
            new_obstacle = Actor('alien')
            new_obstacle.width = min(OBSTACLE_WIDTH, WIDTH - 1)
            new_obstacle.height = new_obstacle.height * (new_obstacle.width / new_obstacle.width)
            new_obstacle.x = random.randint(0, max(0, WIDTH - new_obstacle.width))
            new_obstacle.y = -new_obstacle.height
            new_obstacle.speed = random.uniform(MIN_OBSTACLE_SPEED, MAX_OBSTACLE_SPEED)
            obstacles.append(new_obstacle)
            frame_count = 0

def on_mouse_down(pos):
    if alien.collidepoint(pos):
        alien.image = 'alien_hurt'
        clock.schedule_unique(lambda: alien.update(), 1.0)  # Reset image after 1 second
    else:
        print("You missed me!")

setup()
pgzrun.go()