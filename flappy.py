import pygame
import random

# Initialize Pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 400, 600
GRAVITY = 0.5
FLAP_STRENGTH = -10
PIPE_GAP = 150
PIPE_WIDTH = 70
PIPE_VELOCITY = 3

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Bird class
class Bird:
    def __init__(self):
        self.x = 100
        self.y = HEIGHT // 2
        self.velocity = 0
        self.radius = 20
    
    def flap(self):
        self.velocity = FLAP_STRENGTH
    
    def move(self):
        self.velocity += GRAVITY
        self.y += self.velocity
    
    def draw(self):
        pygame.draw.circle(screen, BLUE, (self.x, int(self.y)), self.radius)
    
# Pipe class
class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, HEIGHT - PIPE_GAP - 100)
    
    def move(self):
        self.x -= PIPE_VELOCITY
    
    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.x, 0, PIPE_WIDTH, self.height))
        pygame.draw.rect(screen, GREEN, (self.x, self.height + PIPE_GAP, PIPE_WIDTH, HEIGHT))
    
# Game Loop
bird = Bird()
pipes = [Pipe(WIDTH + i * 200) for i in range(3)]
score = 0
running = True

while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bird.flap()
    
    bird.move()
    bird.draw()
    
    for pipe in pipes:
        pipe.move()
        pipe.draw()
        if pipe.x + PIPE_WIDTH < 0:
            pipes.remove(pipe)
            pipes.append(Pipe(WIDTH))
            score += 1
        
        if (bird.x + bird.radius > pipe.x and bird.x - bird.radius < pipe.x + PIPE_WIDTH and
            (bird.y - bird.radius < pipe.height or bird.y + bird.radius > pipe.height + PIPE_GAP)):
            running = False  # Collision detection
    
    if bird.y + bird.radius > HEIGHT or bird.y - bird.radius < 0:
        running = False  # Bird hits the ground or ceiling
    
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    
    pygame.display.update()
    clock.tick(30)

pygame.quit()
