import pygame
from pygame.locals import *
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Basic 2D Shooter")

# Player class
class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.speed = .3
        self.size = 10
        self.is_alive = True
        self.bullet_count = 10
        self.is_reloading = False
        self.reload_time = 3000  # milliseconds
        self.last_reload_time = pygame.time.get_ticks()

    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed

    def draw(self):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.size, self.size))

    def respawn(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.is_alive = True

    def reload(self):
        if not self.is_reloading:
            self.is_reloading = True
            self.last_reload_time = pygame.time.get_ticks()

    def is_reload_complete(self):
        current_time = pygame.time.get_ticks()
        return current_time - self.last_reload_time > self.reload_time

# Bullet class
class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.speed = 1
        self.angle = angle

    def update(self):
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)

    def draw(self):
        pygame.draw.circle(screen, (255, 255, 0), (int(self.x), int(self.y)), 5)

# Enemy class
class Enemy:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.speed = .1
        self.size = random.randint(10, 20)
        self.is_alive = True

    def move(self, player):
        if self.x < player.x:
            self.x += self.speed
        elif self.x > player.x:
            self.x -= self.speed

        if self.y < player.y:
            self.y += self.speed
        elif self.y > player.y:
            self.y -= self.speed

    def draw(self):
        pygame.draw.rect(screen, (0, 0, 255), (self.x, self.y, self.size, self.size))

# Create player
player = Player()

# Bullets list
bullets = []

# Enemy list
enemies = []
enemy_spawn_time = 2000  # milliseconds
last_spawn_time = pygame.time.get_ticks()

# Score
score = 0
score_font = pygame.font.Font(None, 24)

# Game state
is_menu = True
is_game_over = False

# Menu loop
while is_menu:
    screen.fill((0, 0, 0))
    menu_text = score_font.render("Click to Start", True, (255, 255, 255))
    menu_rect = menu_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    credit_text = score_font.render("Demo by Zylenox", True, (255, 255, 255))
    credit_rect = credit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 25))
    screen.blit(menu_text, menu_rect)
    screen.blit(credit_text, credit_rect)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            is_menu = False

# Game loop
while not is_game_over:
    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            is_game_over = True
        if event.type == MOUSEBUTTONDOWN and not player.is_alive:
            player.respawn()
            bullets.clear()
            enemies.clear()
            score = 0

        if event.type == MOUSEBUTTONDOWN and player.is_alive:
            if player.bullet_count > 0 and not player.is_reloading:
                player.bullet_count -= 1
                mouse_x, mouse_y = pygame.mouse.get_pos()
                angle = math.atan2(mouse_y - player.y, mouse_x - player.x)
                bullets.append(Bullet(player.x, player.y, angle))
            elif player.bullet_count == 0 and not player.is_reloading:
                player
                player.reload()

    if player.is_alive:
        # Keyboard controls
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[K_UP]:
            dy -= 1
        if keys[K_DOWN]:
            dy += 1
        if keys[K_LEFT]:
            dx -= 1
        if keys[K_RIGHT]:
            dx += 1
        player.move(dx, dy)

        # Clear the screen
        screen.fill((0, 0, 0))

        # Draw the player
        player.draw()

        # Move and draw bullets
        for bullet in bullets:
            bullet.update()
            bullet.draw()

        # Move and draw enemies
        for enemy in enemies:
            enemy.move(player)
            enemy.draw()

            # Collision detection between bullets and enemies
            for bullet in bullets:
                if (
                    enemy.x < bullet.x < enemy.x + enemy.size
                    and enemy.y < bullet.y < enemy.y + enemy.size
                ):
                    enemy.is_alive = False
                    score += 10

            # Collision detection between player and enemies
            if (
                player.x < enemy.x + enemy.size
                and player.x + player.size > enemy.x
                and player.y < enemy.y + enemy.size
                and player.y + player.size > enemy.y
            ):
                player.is_alive = False

        # Remove dead enemies
        enemies = [enemy for enemy in enemies if enemy.is_alive]

        # Spawn new enemy periodically
        current_time = pygame.time.get_ticks()
        if current_time - last_spawn_time > enemy_spawn_time:
            enemies.append(Enemy())
            last_spawn_time = current_time

        # Reload system
        if player.is_reloading and player.is_reload_complete():
            player.bullet_count = 10
            player.is_reloading = False

        # Display bullet count or "Reloading"
        if player.is_reloading:
            bullet_text = score_font.render("Reloading", True, (255, 255, 255))
            screen.blit(bullet_text, (10, 10))
        else:
            bullet_text = score_font.render("Bullets: " + str(player.bullet_count), True, (255, 255, 255))
            screen.blit(bullet_text, (10, 10))


        # Display score
        score_text = score_font.render("Score: " + str(score), True, (255, 255, 255))
        screen.blit(score_text, (10, 40))

        # Update the display
        pygame.display.flip()

    else:
        # Display game over message and score
        game_over_text = score_font.render("Game Over", True, (255, 255, 255))
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        score_text = score_font.render("Score: " + str(score), True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
        instruction_text = score_font.render("Click to try again", True, (255, 255, 255))
        instruction_rect = instruction_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
        screen.blit(game_over_text, game_over_rect)
        screen.blit(score_text, score_rect)
        screen.blit(instruction_text, instruction_rect)

        # Update the display
        pygame.display.flip()
