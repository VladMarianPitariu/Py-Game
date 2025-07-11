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
door_img = pygame.image.load(os.path.join(IMG_DIR, "USA.png"))  # Door image
# Load and resize key sprite (very small)
key_img = pygame.image.load(os.path.join(IMG_DIR, "cheie.png"))
key_img = pygame.transform.scale(key_img, (100, 100))


# Dead sprite for player
dead_img = pygame.image.load(os.path.join(IMG_DIR, "Dead.png"))
dead_img = pygame.transform.scale(dead_img, (200, 200))

# Resize images
idle_img = pygame.transform.scale(idle_img, (200, 200))
fight_img = pygame.transform.scale(fight_img, (200, 200))
kick_img = pygame.transform.scale(kick_img, (200, 200))
boss_img = pygame.transform.scale(boss_img, (300, 300))
# Resize door image
door_img = pygame.transform.scale(door_img, (200, 300))

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
boss_speed = 1  # mai incet
boss_direction = -1  # -1 = left, 1 = right
boss_move_timer = 0
BOSS_MOVE_INTERVAL = 1200  # ms
enemy_felled = False



# Player health
player_health = 100
player_max_health = 100

# Red balls (projectiles) thrown by boss
projectiles = []  # Each projectile: {'rect': pygame.Rect, 'vx': float, 'vy': float}
PROJECTILE_SPEED = 8  # px per frame (aprox 480 px/sec la 60fps, mai rapid)
PROJECTILE_SIZE = 20
PROJECTILE_COOLDOWN = 2200  # ms, delay mai mare
last_projectile_time = 0

# Clock
clock = pygame.time.Clock()
FPS = 60


# Font
font = pygame.font.SysFont(None, 48)


# Get player name before starting game loop
player_name = get_player_name(screen, font)


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

# Add a timer for boss contact damage
BOSS_CONTACT_COOLDOWN = 1200  # ms
boss_contact_last_time = 0

# Game loop
last_attack_time = 0  # ms
ATTACK_COOLDOWN = 300  # ms
while True:
    screen.blit(background_img, (0, 0))
    keys = pygame.key.get_pressed()
    dt = clock.get_time() / 16.67  # 1 frame = 16.67ms la 60fps
    now = pygame.time.get_ticks()

    # Nu mai permite miscarea daca playerul e mort
    if player_health > 0:
        # Miscare player: nu mai bloca la boss, doar margini
        character.update(keys, dt=dt * 0.55, allow_attack=True)
        # Limiteaza playerul la marginea ecranului (in "mapa")
        margin_left = 0
        margin_right = WIDTH
        margin_top = 85  # mai mare sus
        margin_bottom = HEIGHT
        if character.rect.left < margin_left:
            character.rect.left = margin_left
        if character.rect.right > margin_right:
            character.rect.right = margin_right
        if character.rect.top < margin_top:
            character.rect.top = margin_top
        if character.rect.bottom > margin_bottom:
            character.rect.bottom = margin_bottom
        # Nu mai bloca playerul la boss, poate trece peste (doar damage la coliziune)

    
   
    # Boss random movement (mai incet)
    if boss_health > 0:
        now = pygame.time.get_ticks()
        if now - boss_move_timer > BOSS_MOVE_INTERVAL:
            boss_speed = random.randint(1, 2)  # mult mai incet, px per frame
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

    # Boss throws projectiles with different abilities (viteza mai mica)
    now = pygame.time.get_ticks()
    if boss_health > 0 and now - last_projectile_time > PROJECTILE_COOLDOWN:
        proj_x = boss_rect.centerx - PROJECTILE_SIZE // 2
        proj_y = boss_rect.centery
        dx = character.rect.centerx - proj_x
        dy = character.rect.centery - proj_y
        dist = max((dx ** 2 + dy ** 2) ** 0.5, 1)
        vx = (PROJECTILE_SPEED * 0.5) * dx / dist  # viteza mai mica
        vy = (PROJECTILE_SPEED * 0.5) * dy / dist

        # Randomize ability type
        ability = random.choice([
            {'color': (255, 0, 0), 'size': 20, 'damage': 10},      # rosu, mic, damage mic
            {'color': (255, 140, 0), 'size': 32, 'damage': 18},    # portocaliu, mediu, damage mediu
            {'color': (0, 200, 255), 'size': 36, 'damage': 25},    # albastru, mare, damage mare
            {'color': (255, 0, 255), 'size': 26, 'damage': 14},    # mov, mic, damage mediu
            {'color': (255, 255, 0), 'size': 40, 'damage': 30},    # galben, foarte mare, damage foarte mare
        ])
        projectile_rect = pygame.Rect(proj_x, proj_y, ability['size'], ability['size'])
        projectiles.append({'rect': projectile_rect, 'vx': vx, 'vy': vy, 'color': ability['color'], 'damage': ability['damage']})
        last_projectile_time = now

    # Move projectiles and check collision with player
    for proj in projectiles[:]:
        proj['rect'].x += proj['vx'] * 1.2  # mai rapid
        proj['rect'].y += proj['vy'] * 1.2
        # Remove if off screen
        if (proj['rect'].right < 0 or proj['rect'].left > WIDTH or
            proj['rect'].bottom < 0 or proj['rect'].top > HEIGHT):
            projectiles.remove(proj)
            continue
        # Collision with player (damage only if not recently hit)
        if (proj['rect'].colliderect(character.rect) and boss_health > 0 and not player_hit):
            # Damage in functie de tip
            dmg = proj.get('damage', 10)
            player_health -= dmg
            player_hit = True
            player_hit_timer = pygame.time.get_ticks()
            projectiles.remove(proj)
            if player_health < 0:
                player_health = 0

    # Player hit effect timer (immunity)
    if player_hit and pygame.time.get_ticks() - player_hit_timer > PLAYER_HIT_DURATION:
        player_hit = False

    # Kick/punch attack moved to event handling below


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
        # Draw key falling from above after boss defeated (simulate key drop)
        global key_y, key_obtained
        if 'key_y' not in globals():
            key_y = 0
            key_obtained = False
        if not key_obtained:
            key_x = boss_rect.centerx
            key_y = min(key_y + 6, HEIGHT - 80)  # falls down
            # Draw key sprite (small, falling)
            key_falling_rect = key_img.get_rect(center=(key_x, key_y + 12))
            screen.blit(key_img, key_falling_rect)
            # Detect collision with player (only for falling key)
            if character.rect.colliderect(key_falling_rect):
                key_obtained = True
        # Draw key as held by player (right hand area) ONLY if obtained
        if key_obtained:
            # Draw door much further to the right ONLY if key is obtained
            door_offset = 120  # cât de mult "iese" din ecran
            # SPAWN DOOR VISIBLE ON SCREEN, NOT OUTSIDE
            door_x = min(WIDTH - 160, WIDTH + door_offset)  # asigură-te că e vizibilă
            door_rect = door_img.get_rect(midleft=(door_x, HEIGHT // 2))
            screen.blit(door_img, door_rect)
            # Make a much smaller collider for the door (centered on the door)
            door_collider = pygame.Rect(0, 0, 18, 36)  # și mai mic collider
            door_collider.center = door_rect.center
            # Draw key much closer to player's hand (overlap palm area)
            key_hand_rect = key_img.get_rect(topleft=(character.rect.right - 75, character.rect.centery - 100))
            screen.blit(key_img, key_hand_rect)

            # Player can enter door ONLY if has key and is near door
            if character.rect.colliderect(door_collider):
                # Placeholder: clear screen and show new map message
                screen.fill((30, 30, 60))
                msg = font.render("MAPA 2 - Coming soon!", True, (255, 255, 0))
                screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - 40))
                pygame.display.flip()
                pygame.time.wait(2000)
                # Reset for demo: move player to center, remove key, respawn boss/door
                character.rect.center = (WIDTH // 2, HEIGHT // 2)
                key_y = 0
                key_obtained = False
                boss_health = boss_max_health
                boss_rect.midright = (WIDTH - 50, HEIGHT // 2)
                enemy_felled = False

    # Draw player health bar above player
    pbar_width = 80
    pbar_height = 12
    pbar_x = character.rect.centerx - pbar_width // 2
    pbar_y = character.rect.top - 20
    # Health bar
    pygame.draw.rect(screen, (255, 0, 0), (pbar_x, pbar_y, pbar_width, pbar_height))
    pygame.draw.rect(
        screen,
        (0, 255, 0),
        (pbar_x, pbar_y, int(pbar_width * (player_health / player_max_health)), pbar_height)
    )
    # Stamina bar (portocaliu) sub healthbar
    sbar_width = pbar_width
    sbar_height = 8
    sbar_x = pbar_x
    sbar_y = pbar_y + pbar_height + 4  # 4px sub healthbar
    pygame.draw.rect(screen, (180, 90, 0), (sbar_x, sbar_y, sbar_width, sbar_height))  # background portocaliu inchis
    pygame.draw.rect(
        screen,
        (255, 140, 0),  # portocaliu
        (sbar_x, sbar_y, int(sbar_width * (character.stamina / 100)), sbar_height)
    )
    # Show player name above healthbar
    player_label = font.render(player_name, True, (255, 255, 255))
    plabel_rect = player_label.get_rect()
    plabel_rect.midbottom = (character.rect.centerx, pbar_y)
    screen.blit(player_label, plabel_rect)

    # Player mort: doar sprite-ul mort si mesajul, fara miscare sau efecte
    if player_health <= 0:
        dead_rect = dead_img.get_rect(center=character.rect.center)
        screen.blit(dead_img, dead_rect)
        game_over_font = pygame.font.SysFont(None, 80, bold=True)
        game_over_text = game_over_font.render("YOU DIED", True, (200, 0, 0))
        screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 120))
        sub_font = pygame.font.SysFont(None, 40)
        sub_text = sub_font.render("Press R to restart or ESC to quit", True, (255, 255, 255))
        screen.blit(sub_text, (WIDTH//2 - sub_text.get_width()//2, HEIGHT//2 - 40))
    else:
        # Player hit visual effect (tint red only on sprite)
        if player_hit:
            player_img = character.get_image().copy()
            red_overlay = pygame.Surface(player_img.get_size(), pygame.SRCALPHA)
            red_overlay.fill((255, 0, 0, 90))
            player_img.blit(red_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
            screen.blit(player_img, character.rect)
        else:
            character.draw(screen)

    # Draw projectiles (diferite culori si dimensiuni)
    for proj in projectiles:
        pygame.draw.ellipse(screen, proj.get('color', (255, 0, 0)), proj['rect'])

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Procesare atacuri pe eveniment
        if player_health > 0 and boss_health > 0:
            # Boss damage logic la kick/punch + animatie corecta + verificare stamina + directie + cooldown
            if event.type == pygame.KEYDOWN and character.rect.colliderect(boss_rect):
                boss_is_right = boss_rect.centerx > character.rect.centerx
                boss_is_left = boss_rect.centerx < character.rect.centerx
                now = pygame.time.get_ticks()
                if now - last_attack_time >= ATTACK_COOLDOWN:
                    if event.key == pygame.K_x:
                        if character.stamina >= 20:
                            # Verifica directia
                            if (boss_is_right and not character.facing_left) or (boss_is_left and character.facing_left):
                                character.kick()  # seteaza animatia corecta
                                boss_health -= 5  # Deal damage
                                if boss_is_right:
                                    boss_rect.x += 20
                                else:
                                    boss_rect.x -= 20
                                boss_speed = max(1, boss_speed - 1)
                                boss_hit = True
                                boss_hit_timer = pygame.time.get_ticks()
                                last_attack_time = now
                                if boss_health <= 0:
                                    enemy_felled = True
                    elif event.key == pygame.K_f:
                        if character.stamina >= 10:
                            # Verifica directia
                            if (boss_is_right and not character.facing_left) or (boss_is_left and character.facing_left):
                                character.punch()  # seteaza animatia corecta
                                boss_health -= 2.5  # Deal damage
                                if boss_is_right:
                                    boss_rect.x += 20
                                else:
                                    boss_rect.x -= 20
                                boss_speed = max(1, boss_speed - 1)
                                boss_hit = True
                                boss_hit_timer = pygame.time.get_ticks()
                                last_attack_time = now
                                if boss_health <= 0:
                                    enemy_felled = True
            else:
                character.handle_event(event)
        # Allow quitting with ESC or restart with R on game over
        if player_health <= 0 and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_r:
                # Reset all relevant game state
                player_health = player_max_health
                boss_health = boss_max_health
                character.rect.center = (WIDTH // 2, HEIGHT // 2)
                projectiles.clear()
                boss_rect.midright = (WIDTH - 50, HEIGHT // 2)
                boss_speed = 3
                boss_direction = -1
                boss_move_timer = 0
                enemy_felled = False
                player_hit = False
                player_hit_timer = 0
                boss_hit = False
                boss_hit_timer = 0



    pygame.display.flip()
    clock.tick(FPS)
