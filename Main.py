

import os
import pygame
import sys
import random
import math
from character import Character


# Initialize Pygame
pygame.init()

# --- Player name input screen ---

def get_player_name(screen, font):
    input_box = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 + 120, 300, 60)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False
    anim_angle = 0
    char_anim_angle = 0
    clock = pygame.time.Clock()
    funny_msgs = [
        "Don't be shy, type your legendary name!",
        "Your hero needs a name!",
        "The boss is waiting...",
        "No numbers, no symbols, just pure style!",
        "You can be anything. Even 'GIGACHAD'."
    ]
    funny_msg = random.choice(funny_msgs)
    # Load character idle image for intro (use same as in game)
    idle_img = pygame.image.load(os.path.join(IMG_DIR, "idle.png"))
    idle_img = pygame.transform.scale(idle_img, (200, 200))
    # For typing effect
    prompt_full = "Welcome, hero!"
    subprompt_full = "Enter your name to begin your quest:"
    prompt_shown = ''
    subprompt_shown = ''
    prompt_idx = 0
    subprompt_idx = 0
    prompt_speed = 2  # chars per frame
    subprompt_speed = 2
    name_anim_idx = 0
    name_anim_timer = 0
    name_anim_delay = 2  # frames per letter
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        if text.strip():
                            done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                        name_anim_idx = max(0, name_anim_idx - 1)
                    else:
                        if len(text) < 16 and event.unicode.isprintable():
                            text += event.unicode
        # Animated background: smooth vertical gradient + floating stars
        anim_angle += 2
        char_anim_angle += 0.12
        # Gradient background
        for y in range(HEIGHT):
            c = int(30 + 60 * (y / HEIGHT) + 20 * math.sin(anim_angle*0.01 + y*0.01))
            pygame.draw.line(screen, (c, c, 80 + c//3), (0, y), (WIDTH, y))
        # Floating stars
        for i in range(30):
            star_x = int((WIDTH//30)*i + 30*math.sin(anim_angle*0.01 + i))
            star_y = int((HEIGHT//30)*i + 20*math.cos(anim_angle*0.012 + i + anim_angle*0.01))
            pygame.draw.circle(screen, (255,255,255,120), (star_x, star_y), 2)
        # Draw a glowing circle behind the input box
        glow_color = (100, 100, 255, 80)
        glow_surf = pygame.Surface((400, 120), pygame.SRCALPHA)
        pygame.draw.ellipse(glow_surf, glow_color, glow_surf.get_rect())
        screen.blit(glow_surf, (WIDTH//2 - 200, HEIGHT//2 + 90))
        # Animate character idle (bounce up and down)
        char_y = HEIGHT//2 - 40 + int(18 * math.sin(char_anim_angle))
        screen.blit(idle_img, (WIDTH//2 - 100, char_y))
        # Typing effect for prompts
        if prompt_idx < len(prompt_full):
            prompt_idx += prompt_speed
            prompt_shown = prompt_full[:prompt_idx]
        else:
            prompt_shown = prompt_full
        if subprompt_idx < len(subprompt_full):
            subprompt_idx += subprompt_speed
            subprompt_shown = subprompt_full[:subprompt_idx]
        else:
            subprompt_shown = subprompt_full
        prompt = font.render(prompt_shown, True, (255,215,0))
        subprompt = font.render(subprompt_shown, True, (255,255,255))
        # Prompts
        screen.blit(prompt, (WIDTH//2 - prompt.get_width()//2, HEIGHT//2 - 200))
        screen.blit(subprompt, (WIDTH//2 - subprompt.get_width()//2, HEIGHT//2 - 140))
        # Funny message
        funny_font = pygame.font.SysFont(None, 32, italic=True)
        funny = funny_font.render(funny_msg, True, (180, 180, 255))
        screen.blit(funny, (WIDTH//2 - funny.get_width()//2, HEIGHT//2 + 70))
        # Name typing animation above character
        if name_anim_idx < len(text):
            name_anim_timer += 1
            if name_anim_timer >= name_anim_delay:
                name_anim_idx += 1
                name_anim_timer = 0
        elif name_anim_idx > len(text):
            name_anim_idx -= 1
            name_anim_timer = 0
        name_to_show = text[:name_anim_idx]
        name_font = pygame.font.SysFont(None, 54, bold=True)
        name_surface = name_font.render(name_to_show, True, (255,255,0))
        name_x = WIDTH//2 - name_surface.get_width()//2
        name_y = char_y - 60
        screen.blit(name_surface, (name_x, name_y))
        # Input box
        txt_surface = font.render(text, True, (255,255,0))
        width = max(300, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+10))
        pygame.draw.rect(screen, color, input_box, 3)
        pygame.display.flip()
        clock.tick(60)
    return text.strip()

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
player_name = get_player_name(screen, font)

# --- Tutorial screen ---
def run_tutorial(screen, font, character):
    # Fundal animat cu gradient si stele mari si mici
    tutorial_bg = pygame.Surface((WIDTH, HEIGHT))
    def draw_animated_bg(surface, t):
        # Gradient vertical cu nuante mov-albastru si valuri animate
        for y in range(HEIGHT):
            c = int(40 + 80 * (y / HEIGHT) + 60 * math.sin(t*0.008 + y*0.025))
            c = max(0, min(255, c))
            blue = max(0, min(255, 120 + c//2))
            pygame.draw.line(surface, (c//2, c, blue), (0, y), (WIDTH, y))
        # Valuri colorate animate
        for i in range(3):
            wave_color = [(120,120,255,60), (180,120,255,60), (120,255,255,60)][i]
            wave_surf = pygame.Surface((WIDTH, 80), pygame.SRCALPHA)
            for x in range(WIDTH):
                y = int(30 + 18*math.sin(t*0.012 + x*0.02 + i*1.5))
                pygame.draw.circle(wave_surf, wave_color, (x, y+30), 2)
            surface.blit(wave_surf, (0, 120 + i*60), special_flags=pygame.BLEND_RGBA_ADD)
        # Stele mari cu glow
        for i in range(10):
            star_x = int((WIDTH//10)*i + 80*math.sin(t*0.008 + i))
            star_y = int((HEIGHT//10)*i + 60*math.cos(t*0.009 + i + t*0.01))
            for r in range(8,0,-2):
                alpha = int(30 + 25*r)
                pygame.draw.circle(surface, (255,255,220,alpha), (star_x, star_y), r)
        # Stele mici
        for i in range(30):
            star_x = int((WIDTH//30)*i + 30*math.sin(t*0.012 + i))
            star_y = int((HEIGHT//30)*i + 20*math.cos(t*0.014 + i + t*0.01))
            pygame.draw.circle(surface, (180,220,255), (star_x, star_y), 2)
    # Door sprite (simple rectangle for now)
    door_rect = pygame.Rect(WIDTH-80, HEIGHT//2-60, 60, 120)
    door_color = (120, 80, 40)
    door_glow = (200, 180, 80)
    # Tutorial state
    running = True
    show_door = False
    show_ready = False
    ready_confirmed = False
    move_done = False
    kick_done = False
    clock = pygame.time.Clock()
    char_start_pos = (WIDTH//6, HEIGHT//2)
    character.rect.center = char_start_pos
    # Particule pentru efecte vizuale
    particles = []
    # Mini-obstacol: cutie pe care trebuie s-o "lovesti" cu X/F
    box_rect = pygame.Rect(WIDTH//2 + 60, HEIGHT//2 + 40, 50, 50)
    box_alive = True
    box_hit_anim = 0
    # Animatie text
    instr_anim = 0
    instr_anim_dir = 1
    while running:
        t = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if show_ready and event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_y):
                    ready_confirmed = True
        keys = pygame.key.get_pressed()
        prev_pos = character.rect.topleft
        # Miscare smooth si diagonala in tutorial, viteza mai mica
        character.handle_input(keys, dt=0.5, allow_attack=not show_door)
        if character.rect.topleft != prev_pos:
            move_done = True
            # Efect de particule la miscare
            for _ in range(3):
                particles.append({
                    'x': character.rect.centerx,
                    'y': character.rect.bottom,
                    'vx': random.uniform(-1,1),
                    'vy': random.uniform(1,2),
                    'life': random.randint(12,18),
                    'color': (180,180,255)
                })
        # Detecteaza atac pe cutie
        if box_alive and (keys[pygame.K_x] or keys[pygame.K_f]) and character.rect.colliderect(box_rect):
            box_alive = False
            box_hit_anim = 12
            # Efect de particule la cutie
            for _ in range(18):
                particles.append({
                    'x': box_rect.centerx,
                    'y': box_rect.centery,
                    'vx': random.uniform(-2,2),
                    'vy': random.uniform(-2,2),
                    'life': random.randint(16,24),
                    'color': (255,200,80)
                })
            kick_done = True
        # Show door if both actions done
        if move_done and kick_done:
            show_door = True
        # If at door, show ready prompt
        if show_door and character.rect.colliderect(door_rect):
            show_ready = True
        # Update particule
        for p in particles[:]:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] += 0.12  # gravitate
            p['life'] -= 1
            if p['life'] <= 0:
                particles.remove(p)
        # Draw animated background
        draw_animated_bg(tutorial_bg, t)
        screen.blit(tutorial_bg, (0, 0))
        # Draw box obstacle cu efect de glow si bounce
        if box_alive:
            pulse = 1.0 + 0.08*math.sin(t*0.02)
            box_rect_anim = box_rect.inflate(int(8*pulse), int(8*pulse))
            glow_surf = pygame.Surface((box_rect_anim.width+24, box_rect_anim.height+24), pygame.SRCALPHA)
            for r in range(18,0,-4):
                alpha = int(18 + 12*r)
                rect = glow_surf.get_rect().inflate(-r, -r)
                pygame.draw.ellipse(glow_surf, (255,220,80,alpha), rect)
            screen.blit(glow_surf, (box_rect_anim.x-12, box_rect_anim.y-12), special_flags=pygame.BLEND_RGBA_ADD)
            pygame.draw.rect(screen, (200,140,60), box_rect_anim, border_radius=10)
            pygame.draw.rect(screen, (255,220,120), box_rect_anim, 3, border_radius=10)
            # Animatie "pulse" la instructiune
            if not kick_done and move_done:
                pygame.draw.rect(screen, (255,255,80,80), box_rect_anim.inflate(16,16), border_radius=14)
        elif box_hit_anim > 0:
            # Cutia "explodeaza" in particule
            box_hit_anim -= 1
        # Draw door cu efect de glow si animatie de deschidere
        if show_door:
            door_anim = 1.0 + 0.08*math.sin(t*0.018)
            door_rect_anim = door_rect.inflate(int(8*door_anim), int(8*door_anim))
            glow = pygame.Surface((door_rect_anim.width+30, door_rect_anim.height+30), pygame.SRCALPHA)
            for r in range(24,0,-6):
                alpha = int(18 + 10*r)
                rect = glow.get_rect().inflate(-r, -r)
                pygame.draw.ellipse(glow, door_glow + (alpha,), rect)
            screen.blit(glow, (door_rect_anim.x-15, door_rect_anim.y-15), special_flags=pygame.BLEND_RGBA_ADD)
            pygame.draw.rect(screen, door_color, door_rect_anim, border_radius=14)
            pygame.draw.rect(screen, (255,220,120), door_rect_anim, 4, border_radius=14)
        # Draw character
        character.draw(screen)
        # Draw particles
        for p in particles:
            pygame.draw.circle(screen, p['color'], (int(p['x']), int(p['y'])), 3)
        # Animated tutorial instructions
        instr_font = pygame.font.SysFont(None, 38, bold=True)
        instr_anim += 0.12 * instr_anim_dir
        if instr_anim > 1.5 or instr_anim < -1.5:
            instr_anim_dir *= -1
        # Efect de glow la text
        def draw_glow_text(txt, pos, color, glow_color=(255,255,120)):
            for dx in range(-2,3):
                for dy in range(-2,3):
                    if dx==0 and dy==0: continue
                    surf = instr_font.render(txt, True, glow_color)
                    screen.blit(surf, (pos[0]+dx, pos[1]+dy))
            surf = instr_font.render(txt, True, color)
            screen.blit(surf, pos)
        if not move_done:
            instr = "Foloseste sagetile sau WASD pentru a te misca"
            draw_glow_text(instr, (WIDTH//2 - instr_font.size(instr)[0]//2, 60 + int(10*math.sin(instr_anim))), (255,255,200))
        elif not kick_done:
            instr = "Apasa X sau F pentru a ataca cutia!"
            draw_glow_text(instr, (WIDTH//2 - instr_font.size(instr)[0]//2, 60 + int(10*math.sin(instr_anim))), (255,255,200))
        elif not show_ready:
            instr = "Mergi la usa pentru a continua!"
            draw_glow_text(instr, (WIDTH//2 - instr_font.size(instr)[0]//2, 60 + int(10*math.sin(instr_anim))), (255,255,200))
        if show_ready:
            # Fade in effect
            ready_font = pygame.font.SysFont(None, 60, bold=True)
            ready_msg = "Are you ready?"
            ready = ready_font.render(ready_msg, True, (255, 215, 0))
            screen.blit(ready, (WIDTH//2 - ready.get_width()//2, HEIGHT//2 - 120))
            sub = instr_font.render("Apasa ENTER sau SPACE pentru a incepe lupta!", True, (255,255,255))
            screen.blit(sub, (WIDTH//2 - sub.get_width()//2, HEIGHT//2 - 60))
        pygame.display.flip()
        clock.tick(60)
        if ready_confirmed:
            running = False

# Rulare tutorial inainte de boss fight
run_tutorial(screen, font, character)

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
