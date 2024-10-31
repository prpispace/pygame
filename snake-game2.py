import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Initialize the game window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Snake Game')

class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH//2, GRID_HEIGHT//2)]
        self.direction = 'RIGHT'
        self.length = 1
        
    def get_head_position(self):
        return self.positions[0]
    
    def update(self):
        cur = self.get_head_position()
        x, y = cur
        
        if self.direction == 'UP':
            y -= 1
        elif self.direction == 'DOWN':
            y += 1
        elif self.direction == 'LEFT':
            x -= 1
        elif self.direction == 'RIGHT':
            x += 1
            
        if x < 0:
            x = GRID_WIDTH - 1
        elif x >= GRID_WIDTH:
            x = 0
        if y < 0:
            y = GRID_HEIGHT - 1
        elif y >= GRID_HEIGHT:
            y = 0
            
        self.positions.insert(0, (x, y))
        if len(self.positions) > self.length:
            self.positions.pop()
            
    def reset(self):
        self.positions = [(GRID_WIDTH//2, GRID_HEIGHT//2)]
        self.direction = 'RIGHT'
        self.length = 1

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.spawn()
        
    def spawn(self):
        self.position = (random.randint(0, GRID_WIDTH-1),
                        random.randint(0, GRID_HEIGHT-1))

def main():
    clock = pygame.time.Clock()
    snake = Snake()
    food = Food()
    score = 0
    game_over = False
    
    # Display controls at start
    font = pygame.font.Font(None, 36)
    controls_displayed = True
    start_time = time.time()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if game_over:
                    snake.reset()
                    food.spawn()
                    score = 0
                    game_over = False
                else:
                    # Support both arrow keys and WASD
                    if event.key in [pygame.K_UP, pygame.K_w] and snake.direction != 'DOWN':
                        snake.direction = 'UP'
                    elif event.key in [pygame.K_DOWN, pygame.K_s] and snake.direction != 'UP':
                        snake.direction = 'DOWN'
                    elif event.key in [pygame.K_LEFT, pygame.K_a] and snake.direction != 'RIGHT':
                        snake.direction = 'LEFT'
                    elif event.key in [pygame.K_RIGHT, pygame.K_d] and snake.direction != 'LEFT':
                        snake.direction = 'RIGHT'
        
        if not game_over:
            snake.update()
            
            # Check if snake eats food
            if snake.get_head_position() == food.position:
                snake.length += 1
                score += 10
                food.spawn()
            
            # Check for collision with self
            if snake.get_head_position() in snake.positions[1:]:
                game_over = True
        
        # Drawing
        window.fill(BLACK)
        
        # Draw snake
        for position in snake.positions:
            rect = pygame.Rect(position[0]*GRID_SIZE, position[1]*GRID_SIZE,
                             GRID_SIZE-2, GRID_SIZE-2)
            pygame.draw.rect(window, GREEN, rect)
            
        # Draw food
        food_rect = pygame.Rect(food.position[0]*GRID_SIZE, food.position[1]*GRID_SIZE,
                              GRID_SIZE-2, GRID_SIZE-2)
        pygame.draw.rect(window, RED, food_rect)
        
        # Draw score
        score_text = font.render(f'Score: {score}', True, WHITE)
        window.blit(score_text, (10, 10))
        
        # Display controls for first 5 seconds
        if controls_displayed and time.time() - start_time < 5:
            controls_text = [
                "Controls:",
                "W or ↑ : Move Up",
                "S or ↓ : Move Down",
                "A or ← : Move Left",
                "D or → : Move Right"
            ]
            for i, text in enumerate(controls_text):
                control_text = font.render(text, True, WHITE)
                window.blit(control_text, (WINDOW_WIDTH/2 - 100, WINDOW_HEIGHT/2 - 50 + i*30))
        
        if game_over:
            game_over_text = font.render('Game Over! Press any key to restart', True, WHITE)
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
            window.blit(game_over_text, text_rect)
        
        pygame.display.flip()
        clock.tick(10)

if __name__ == '__main__':
    main()
