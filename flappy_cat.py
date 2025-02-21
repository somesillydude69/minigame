import pygame
import random

# Initialize Pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 400, 600
GRAVITY = 0.5
FLAP_STRENGTH = -8
PIPE_GAP = 170
PIPE_WIDTH = 70
PIPE_VELOCITY = 3
MAX_FALL_SPEED = 10
BIRD_JUMP_SOUND = 'jump.wav'
GAME_OVER_SOUND = 'game_over.wav'

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Load Sounds
pygame.mixer.init()
jump_sound = pygame.mixer.Sound(BIRD_JUMP_SOUND)
game_over_sound = pygame.mixer.Sound(GAME_OVER_SOUND)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Load Bird Image
cat_image = pygame.image.load('cat.png')
cat_image = pygame.transform.scale(cat_image, (40, 30))

# cat class
class Cat:
    def __init__(self):
        self.x = 100
        self.y = HEIGHT // 2
        self.velocity = 0
        self.angle = 0
    
    def flap(self):
        self.velocity = FLAP_STRENGTH
        jump_sound.play()
    
    def move(self):
        self.velocity += GRAVITY
        if self.velocity > MAX_FALL_SPEED:
            self.velocity = MAX_FALL_SPEED
        self.y += self.velocity
        self.angle = min(max(self.velocity * -3, -30), 30)
    
    def draw(self):
        rotated_cat = pygame.transform.rotate(cat_image, self.angle)
        screen.blit(rotated_cat, (self.x, int(self.y)))
    
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
    
# Main Menu Function
def main_menu():
    alpha = 0
    menu_running = True
    while menu_running:
        screen.fill(WHITE)
        title_text = font.render("Flappy Bird", True, BLACK)
        start_text = font.render("Press SPACE to Start", True, BLACK)
        title_text.set_alpha(alpha)
        start_text.set_alpha(alpha)
        screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//3))
        screen.blit(start_text, (WIDTH//2 - start_text.get_width()//2, HEIGHT//2))
        pygame.display.update()
        alpha = min(alpha + 5, 255)
        pygame.time.delay(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                menu_running = False

# Game Loop
def game_loop():
    cat = Cat()
    pipes = [Pipe(WIDTH + i * 200) for i in range(3)]
    score = 0
    running = True
    
    while running:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                cat.flap()
        
        cat.move()
        cat.draw()
        
        
        for pipe in pipes:
            pipe.move()
            pipe.draw()
            if pipe.x + PIPE_WIDTH < 0:
                pipes.remove(pipe)
                pipes.append(Pipe(WIDTH + random.randint(50, 150)))
                score += 1
            
            if (cat.x + 20 > pipe.x and cat.x - 20 < pipe.x + PIPE_WIDTH and
                (cat.y - 15 < pipe.height or cat.y + 15 > pipe.height + PIPE_GAP)):
                game_over_sound.play()
                pygame.time.delay(1000)
                return  # Restart the game
        
        if cat.y + 15 > HEIGHT or cat.y - 15 < 0:
            game_over_sound.play()
            pygame.time.delay(1000)
            return  # Restart the game
        
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        
        pygame.display.update()
        clock.tick(30)

# Credits Screen
def credits_screen():
    screen.fill(WHITE)
    credits_text = font.render("Made by /home/green_cat", True, BLACK)
    screen.blit(credits_text, (WIDTH//2 - credits_text.get_width()//2, HEIGHT//2))
    pygame.display.update()
    pygame.time.delay(2000)  # Show credits for 2 seconds

while True:
    main_menu()
    game_loop()
    credits_screen()

pygame.quit()
