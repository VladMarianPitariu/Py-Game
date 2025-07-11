import os
import pygame
import sys
import random
import math
from character import Character
from character_select import get_player_name


# Initialize Pygame
pygame.init()

# Paths
IMG_DIR = os.path.join(os.path.dirname(__file__), "img")

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Game: Main Character vs Boss")

# Font
font = pygame.font.SysFont(None, 48)

# Get player name before starting game loop
player_name = get_player_name(screen, font, IMG_DIR, WIDTH, HEIGHT)

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

# Boss setup
boss_rect = boss_img.get_rect(midright=(WIDTH - 50, HEIGHT // 2))
boss_health = 100
boss_max_health = 100
boss_speed = 3
boss_direction = -1  # -1 = left, 1 = right
boss_move_timer = 0
BOSS_MOVE_INTERVAL = 1200  # ms
enemy_felled = False

# Player health
player_health = 100
player_max_health = 100

# Red balls (projectiles) thrown by boss
projectiles = []  # Each projectile: {'rect': pygame.Rect, 'vx': float, 'vy': float}
PROJECTILE_SPEED = 4  # px per frame (aprox 240 px/sec at 60fps)
PROJECTILE_SIZE = 20
PROJECTILE_COOLDOWN = 1200  # ms
last_projectile_time = 0

# Clock
clock = pygame.time.Clock()
FPS = 120


# Font
font = pygame.font.SysFont(None, 48)

# Get player name before starting game loop
#player_name = get_player_name(screen, font, IMG_DIR, WIDTH, HEIGHT)

## Tutorial removed as requested

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

PLAYER_HIT_DURATION = 400  # ms
player_hit = False
player_hit_timer = 0

# Game loop
while True:
    screen.blit(background_img, (0, 0))

    keys = pygame.key.get_pressed()
    # Foloseste dt pentru smooth movement si allow_attack True in bossfight
    dt = clock.get_time() / 16.67  # 1 frame = 16.67ms la 60fps
    # Viteza mai mica in bossfight (ex: 22)
    character.update(keys, dt=dt * 0.55, allow_attack=True)

    # Boss random movement
    if boss_health > 0:
        now = pygame.time.get_ticks()
        if now - boss_move_timer > BOSS_MOVE_INTERVAL:
            boss_speed = random.randint(2, 4)  # much slower, px per frame
            boss_direction = random.choice([-1, 1])
            boss_move_timer = now
        boss_rect.x += boss_speed * boss_direction
        boss_rect.y += random.choice([-1, 0, 1]) * random.randint(0, 1)  # less jitter
        # Keep boss in screen
        if boss_rect.left < 0:
            boss_rect.left = 0
            boss_direction = 1
        if boss_rect.right > WIDTH:
            boss_rect.right = WIDTH
            boss_direction = -1
        if boss_rect.top < 0:
            boss_rect.top = 0
        if boss_rect.bottom > HEIGHT:
            boss_rect.bottom = HEIGHT

    # Boss throws projectiles that follow the player
    now = pygame.time.get_ticks()
    if boss_health > 0 and now - last_projectile_time > PROJECTILE_COOLDOWN:
        proj_x = boss_rect.centerx - PROJECTILE_SIZE // 2
        proj_y = boss_rect.centery
        # Calculate direction vector towards player
        dx = character.rect.centerx - proj_x
        dy = character.rect.centery - proj_y
        dist = max((dx ** 2 + dy ** 2) ** 0.5, 1)
        vx = PROJECTILE_SPEED * dx / dist
        vy = PROJECTILE_SPEED * dy / dist
        projectile_rect = pygame.Rect(proj_x, proj_y, PROJECTILE_SIZE, PROJECTILE_SIZE)
        projectiles.append({'rect': projectile_rect, 'vx': vx, 'vy': vy})
        last_projectile_time = now

    # Move projectiles and check collision with player
    for proj in projectiles[:]:
        proj['rect'].x += proj['vx'] * 0.7  # reduce projectile speed
        proj['rect'].y += proj['vy'] * 0.7
        # Remove if off screen
        if (proj['rect'].right < 0 or proj['rect'].left > WIDTH or
            proj['rect'].bottom < 0 or proj['rect'].top > HEIGHT):
            projectiles.remove(proj)
            continue
        # Collision with player (damage only if not recently hit)
        if (proj['rect'].colliderect(character.rect) and boss_health > 0
            and not player_hit):
            player_health -= 10
            player_hit = True
            player_hit_timer = pygame.time.get_ticks()
            projectiles.remove(proj)
            if player_health < 0:
                player_health = 0

    # Player hit effect timer (immunity)
    if player_hit and pygame.time.get_ticks() - player_hit_timer > PLAYER_HIT_DURATION:
        player_hit = False

    # Kick attack
    if (keys[pygame.K_x] or keys[pygame.K_f]) and boss_health > 0:
        character.kick()
        if character.rect.colliderect(boss_rect):
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

        # Draw boss health bar at the top center
        bar_width = 400
        bar_height = 20
        bar_x = (WIDTH - bar_width) // 2
        bar_y = 30
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(
            screen,
            (0, 255, 0),
            (bar_x, bar_y, int(bar_width * (boss_health / boss_max_health)), bar_height)
        )
        boss_label = font.render("Costin", True, (255, 255, 255))
        label_rect = boss_label.get_rect()
        label_rect.midright = (bar_x - 10, bar_y + bar_height // 2)
        screen.blit(boss_label, label_rect)
    else:
        # Boss defeated
        text = font.render("Enemy Felled!", True, (255, 215, 0))
        screen.blit(text, (WIDTH//2 - 100, HEIGHT//2 - 50))

    # Draw player health bar above player
    pbar_width = 80
    pbar_height = 12
    pbar_x = character.rect.centerx - pbar_width // 2
    pbar_y = character.rect.top - 20
    pygame.draw.rect(screen, (255, 0, 0), (pbar_x, pbar_y, pbar_width, pbar_height))
    pygame.draw.rect(
        screen,
        (0, 255, 0),
        (pbar_x, pbar_y, int(pbar_width * (player_health / player_max_health)), pbar_height)
    )
    # Show player name above healthbar
    player_label = font.render(player_name, True, (255, 255, 255))
    plabel_rect = player_label.get_rect()
    plabel_rect.midbottom = (character.rect.centerx, pbar_y)
    screen.blit(player_label, plabel_rect)

    # Player hit visual effect (tint red only on sprite)
    if player_hit:
        # Get current player image
        player_img = character.get_image().copy()
        red_overlay = pygame.Surface(player_img.get_size(), pygame.SRCALPHA)
        red_overlay.fill((255, 0, 0, 90))
        player_img.blit(red_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        screen.blit(player_img, character.rect)
    else:
        character.draw(screen)

    # Draw projectiles
    for proj in projectiles:
        pygame.draw.ellipse(screen, (255, 0, 0), proj['rect'])

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Draw player (only if not hit, otherwise drawn above)
    # ...existing code...

    pygame.display.flip()
    clock.tick(FPS)
