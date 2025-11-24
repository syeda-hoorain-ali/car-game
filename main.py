import pygame
import random
import sys
from typing import List

pygame.init()

# Constants
WIDTH, HEIGHT = 1280, 720
ROAD_WIDTH = 400
ROAD_X = (WIDTH - ROAD_WIDTH) // 2
FPS = 60
CAR_WIDTH, CAR_HEIGHT = 50, 100 # Adjusted height for typical car images
ENEMY_COUNT = 4
LANE_LINE_HEIGHT = 100

# Colors
WHITE = (255, 255, 255)
GREY = (45, 52, 54)
LIGHT_GREY = (85, 102, 104)
PINK = (255, 105, 180)
RED = (255, 0, 0)

# Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Game 🚗")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# --- MODIFIED: LOAD IMAGES FROM FILES ---
try:
    # Load background image
    background_img = pygame.image.load("background.jpg").convert()
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

    # Load player car image
    player_car_img = pygame.image.load("car.png").convert_alpha()
    player_car_img = pygame.transform.scale(player_car_img, (CAR_WIDTH, CAR_HEIGHT))

    # Load enemy car images into a list
    enemy_car_imgs = [
        pygame.transform.scale(pygame.image.load("car-1.png").convert_alpha(), (CAR_WIDTH, CAR_HEIGHT)),
        pygame.transform.scale(pygame.image.load("car-2.png").convert_alpha(), (CAR_WIDTH, CAR_HEIGHT)),
        pygame.transform.scale(pygame.image.load("car-3.png").convert_alpha(), (CAR_WIDTH, CAR_HEIGHT)),
    ]
except pygame.error as e:
    print(f"Image load nahi ho saki: {e}")
    print("Please make sure 'background.jpg', 'car.png', 'car-1.png', 'car-2.png', and 'car-3.png' files folder mein mojood hain.")
    sys.exit()


class Car(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, img: pygame.Surface, *groups: pygame.sprite.Group) -> None:
        super().__init__(*groups)
        self.image = img
        # Using a more accurate collider by shrinking the rect slightly
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5

    def update(self, *args, **kwargs) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
        if keys[pygame.K_LEFT] and self.rect.left > ROAD_X:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < ROAD_X + ROAD_WIDTH:
            self.rect.x += self.speed


class Enemy(Car):
    def __init__(self, *groups: pygame.sprite.Group) -> None:
        # --- MODIFIED: RANDOMLY CHOOSE AN ENEMY IMAGE ---
        img = random.choice(enemy_car_imgs)
        x = random.randint(ROAD_X, ROAD_X + ROAD_WIDTH - CAR_WIDTH)
        y = random.randint(-800, -100)
        super().__init__(x, y, img, *groups)
        self.speed = random.randint(4, 8)

    def update(self, *args, **kwargs) -> None:
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            # --- MODIFIED: CHANGE IMAGE ON RESPAWN ---
            self.image = random.choice(enemy_car_imgs)
            self.rect.y = random.randint(-800, -100)
            self.rect.x = random.randint(ROAD_X, ROAD_X + ROAD_WIDTH - CAR_WIDTH)


class LaneLine:
    def __init__(self, y: int) -> None:
        self.rect = pygame.Rect(WIDTH // 2 - 5, y, 10, LANE_LINE_HEIGHT)
        self.y = y

    def update(self, speed: int) -> None:
        self.y += speed
        if self.y > HEIGHT:
            self.y = -LANE_LINE_HEIGHT
        self.rect.y = self.y

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, WHITE, self.rect)


def draw_score(score: int) -> None:
    pygame.draw.rect(screen, PINK, (50, 50, 150, 40))
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (70, 55))

def draw_road() -> None:
    pygame.draw.rect(screen, GREY, (ROAD_X, 0, ROAD_WIDTH, HEIGHT))
    for i in range(11):
        pygame.draw.rect(screen, LIGHT_GREY, (ROAD_X, i * 70, 8, 40))
    for i in range(11):
        pygame.draw.rect(screen, LIGHT_GREY, (ROAD_X + ROAD_WIDTH - 8, i * 70, 8, 40))
    


def start_screen() -> None:
    waiting = True
    while waiting:
        clock.tick(FPS)
        screen.blit(background_img, (0, 0))
        draw_road()
        # pygame.draw.rect(screen, RED, (WIDTH // 2 - 250, HEIGHT // 2 - 75, 500, 150))

        title_font = pygame.font.SysFont("Arial", 60, bold=True)
        instr_font = pygame.font.SysFont("Arial", 30)
        title_text = title_font.render("Car Game", True, WHITE)
        instr_text = instr_font.render("Click or press any key to start", True, WHITE)
        
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 100))
        screen.blit(instr_text, (WIDTH // 2 - instr_text.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False


def game_over_screen(score: int) -> None:
    waiting = True
    while waiting:
        clock.tick(FPS)
        screen.fill(RED)
        
        msg_font = pygame.font.SysFont("Arial", 50)
        restart_font = pygame.font.SysFont("Arial", 30)
        msg_text = msg_font.render(f"Game Over! Score: {score}", True, WHITE)
        restart_text = restart_font.render("Click or press any key to restart", True, WHITE)

        screen.blit(msg_text, (WIDTH // 2 - msg_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 20))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False


def game_loop() -> None:
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    
    player = Car(WIDTH // 2 - CAR_WIDTH // 2, HEIGHT - CAR_HEIGHT - 20, player_car_img, all_sprites)
    for _ in range(ENEMY_COUNT):
        Enemy(all_sprites, enemies)

    lane_lines: List[LaneLine] = [LaneLine(i * 165) for i in range(int(HEIGHT / 150) + 1)]
    score = 0
    last_score_time = pygame.time.get_ticks()

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        all_sprites.update()
        for line in lane_lines:
            line.update(player.speed)

        if pygame.sprite.spritecollide(player, enemies, False, pygame.sprite.collide_mask):
            game_over_screen(score)
            return

        current_time = pygame.time.get_ticks()
        if current_time - last_score_time > 300:
            score += 1
            last_score_time = current_time

        screen.blit(background_img, (0, 0))
        draw_road()
        
        for line in lane_lines:
            line.draw(screen)
        all_sprites.draw(screen)
        draw_score(score)
        
        pygame.display.flip()


if __name__ == "__main__":
    while True:
        start_screen()
        game_loop()