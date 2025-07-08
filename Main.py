import os
import pygame
import sys
from character import Character

# Initialize Pygame
pygame.init()

# Paths
IMG_DIR = os.path.join(os.path.dirname(__file__), "img")

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Game: Main Character vs Boss")

# Load images from img folder
background_img = pygame.image.load(os.path.join(IMG_DIR, "background.png"))
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

idle_img = pygame.image.load(os.path.join(IMG_DIR, "idle.png"))
fight_img = pygame.image.load(os.path.join(IMG_DIR, "fight-v2.png"))
kick_img = pygame.image.load(os.path.join(IMG_DIR, "kick-v1.png"))
boss_img = pygame.image.load(os.path.join(IMG_DIR, "king.png"))  # Boss image

# Resize images
idle_img = pygame.transform.scale(idle_img, (200, 200))
fight_img = pygame.transform.scale(fight_img, (200, 200))
kick_img = pygame.transform.scale(kick_img, (200, 200))
boss_img = pygame.transform.scale(boss_img, (300, 300))

# Character setup
character = Character(
    idle_img=idle_img,
    fight_img=fight_img,
    kick_img=kick_img,
    facing_left=False,
    pos=(WIDTH // 2, HEIGHT // 2)
)

# Boss setup
boss_rect = boss_img.get_rect(midright=(WIDTH - 50, HEIGHT // 2))
boss_health = 100
boss_max_health = 100
enemy_felled = False

# Clock
clock = pygame.time.Clock()
FPS = 60

# Font
font = pygame.font.SysFont(None, 48)

# Add this function to tint a surface red (for boss)
def tint_surface_red(surface, intensity=0.4):
    """Return a copy of the surface tinted red by the given intensity (0-1)."""
    tinted = surface.copy()
    red_overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    red_overlay.fill((255, 0, 0, int(255 * intensity)))
    tinted.blit(red_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
    return tinted

# Add a flag and timer for boss hit effect
boss_hit = False
boss_hit_timer = 0
BOSS_HIT_DURATION = 200  # milliseconds

# Game loop
while True:
    screen.blit(background_img, (0, 0))

    keys = pygame.key.get_pressed()
    character.update(keys)

    # Kick attack
    if keys[pygame.K_x]:
        character.kick()
        if character.rect.colliderect(boss_rect) and boss_health > 0:
            boss_health -= 1  # Deal damage
            boss_hit = True
            boss_hit_timer = pygame.time.get_ticks()
            if boss_health <= 0:
                enemy_felled = True

    # Draw boss if alive
    if boss_health > 0:
        # Draw boss with red tint if just hit
        if boss_hit and pygame.time.get_ticks() - boss_hit_timer <= BOSS_HIT_DURATION:
            screen.blit(tint_surface_red(boss_img, 0.4), boss_rect)
        else:
            boss_hit = False
            screen.blit(boss_img, boss_rect)

        # Draw health bar at the top center of the screen
        bar_width = 400
        bar_height = 20
        bar_x = (WIDTH - bar_width) // 2
        bar_y = 30
        # Red background
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        # Green foreground (current health)
        pygame.draw.rect(
            screen,
            (0, 255, 0),
            (bar_x, bar_y, int(bar_width * (boss_health / boss_max_health)), bar_height)
        )
        # Optional: Boss label
        boss_label = font.render("Costin", True, (255, 255, 255))
        label_rect = boss_label.get_rect()
        label_rect.midright = (bar_x - 10, bar_y + bar_height // 2)
        screen.blit(boss_label, label_rect)
    else:
        # Boss defeated
        text = font.render("Enemy Felled!", True, (255, 215, 0))
        screen.blit(text, (WIDTH//2 - 100, HEIGHT//2 - 50))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Draw player
    character.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)
