import pygame
import random

# Initialize Pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 1920, 1080
GRAVITY = 0.5
FLAP_STRENGTH = -8
PIPE_GAP = 200
PIPE_WIDTH = random.randint(60, 100)  # Pipes have varying widths
PIPE_VELOCITY = 3
MAX_FALL_SPEED = 10
Cat_JUMP_SOUND = 'jump.wav'
GAME_OVER_SOUND = 'game_over.wav'

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Load Sounds
pygame.mixer.init()
jump_sound = pygame.mixer.Sound(Cat_JUMP_SOUND)
game_over_sound = pygame.mixer.Sound(GAME_OVER_SOUND)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 72)

# Load Car Images
skins = ['cat1.png', 'cat2.png', 'cat3.png', 'cat4.png', 'cat5.png']
skin_index = 0
cat_image = pygame.image.load(skins[skin_index])
cat_image = pygame.transform.scale(cat_image, (80, 60))

# Pause Function
def pause_menu():
    paused = True
    while paused:
        screen.fill(WHITE)
        pause_text = font.render("Paused - Press ESC to Resume", True, BLACK)
        screen.blit(pause_text, (WIDTH//2 - pause_text.get_width()//2, HEIGHT//2))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                paused = False

# Skin Selection Menu
def skin_menu():
    global skin_index, cat_image
    menu_running = True
    while menu_running:
        screen.fill(WHITE)
        title_text = font.render("Select Your Cat", True, BLACK)
        next_text = font.render("Press N to change skin", True, BLACK)
        start_text = font.render("Press SPACE to Start", True, BLACK)
        screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//4))
        screen.blit(next_text, (WIDTH//2 - next_text.get_width()//2, HEIGHT//2))
        screen.blit(start_text, (WIDTH//2 - start_text.get_width()//2, HEIGHT//1.5))
        
        selected_cat = pygame.image.load(skins[skin_index])
        selected_cat = pygame.transform.scale(selected_cat, (160, 120))
        screen.blit(selected_cat, (WIDTH//2 - 80, HEIGHT//3))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    skin_index = (skin_index + 1) % len(skins)
                    cat_image = pygame.image.load(skins[skin_index])
                    cat_image = pygame.transform.scale(cat_image, (80, 60))
                if event.key == pygame.K_SPACE:
                    menu_running = False

# Cat class
class Cat:
    def __init__(self):
        self.x = 200
        self.y = HEIGHT // 2
        self.velocity = 0
        self.angle = 0
        self.width = 80
        self.height = 60
    
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
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# Pipe class
class Pipe:
    def __init__(self, x):
        self.x = x
        min_height = 200
        max_height = HEIGHT - PIPE_GAP - min_height
        self.height = random.randint(min_height, max_height)
        self.width = random.randint(60, 100)
        self.moving = random.choice([True, False])
        self.direction = 1 if random.random() > 0.5 else -1
    
    def move(self):
        self.x -= PIPE_VELOCITY
        if self.moving:
            self.height += self.direction * 2
            if self.height < 150 or self.height > HEIGHT - PIPE_GAP - 150:
                self.direction *= -1
    
    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.x, 0, self.width, self.height))
        pygame.draw.rect(screen, GREEN, (self.x, self.height + PIPE_GAP, self.width, HEIGHT))
    
    def get_rects(self):
        return [
            pygame.Rect(self.x, 0, self.width, self.height),
            pygame.Rect(self.x, self.height + PIPE_GAP, self.width, HEIGHT - self.height - PIPE_GAP)
        ]

# Game Loop
def game_loop():
    cat = Cat()
    pipes = [Pipe(WIDTH + i * 400) for i in range(3)]
    score = 0
    running = True
    
    while running:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    cat.flap()
                if event.key == pygame.K_ESCAPE:
                    pause_menu()
        
        cat.move()
        cat.draw()
        
        for pipe in pipes:
            pipe.move()
            pipe.draw()
            if pipe.x + pipe.width < 0:
                pipes.remove(pipe)
                pipes.append(Pipe(WIDTH + random.randint(400, 600)))
                score += 1
            
            if cat.get_rect().collidelist(pipe.get_rects()) != -1:
                game_over_sound.play()
                pygame.time.delay(1000)
                return
        
        if cat.y + 30 > HEIGHT or cat.y - 30 < 0:
            game_over_sound.play()
            pygame.time.delay(1000)
            return
        
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (50, 50))
        
        pygame.display.update()
        clock.tick(60)

while True:
    skin_menu()
    game_loop()

pygame.quit()
