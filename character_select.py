import os
import pygame
import sys
import random
import math

def get_player_name(screen, font, IMG_DIR, WIDTH, HEIGHT):
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
    idle_img = pygame.image.load(os.path.join(IMG_DIR, "idle.png"))
    idle_img = pygame.transform.scale(idle_img, (200, 200))
    prompt_full = "Welcome, hero!"
    subprompt_full = "Enter your name to begin your quest:"
    prompt_shown = ''
    subprompt_shown = ''
    prompt_idx = 0
    subprompt_idx = 0
    prompt_speed = 2
    subprompt_speed = 2
    name_anim_idx = 0
    name_anim_timer = 0
    name_anim_delay = 2
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
        anim_angle += 2
        char_anim_angle += 0.12
        for y in range(HEIGHT):
            c = int(30 + 60 * (y / HEIGHT) + 20 * math.sin(anim_angle*0.01 + y*0.01))
            pygame.draw.line(screen, (c, c, 80 + c//3), (0, y), (WIDTH, y))
        for i in range(30):
            star_x = int((WIDTH//30)*i + 30*math.sin(anim_angle*0.01 + i))
            star_y = int((HEIGHT//30)*i + 20*math.cos(anim_angle*0.012 + i + anim_angle*0.01))
            pygame.draw.circle(screen, (255,255,255,120), (star_x, star_y), 2)
        glow_color = (100, 100, 255, 80)
        glow_surf = pygame.Surface((400, 120), pygame.SRCALPHA)
        pygame.draw.ellipse(glow_surf, glow_color, glow_surf.get_rect())
        screen.blit(glow_surf, (WIDTH//2 - 200, HEIGHT//2 + 90))
        char_y = HEIGHT//2 - 40 + int(18 * math.sin(char_anim_angle))
        screen.blit(idle_img, (WIDTH//2 - 100, char_y))
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
        screen.blit(prompt, (WIDTH//2 - prompt.get_width()//2, HEIGHT//2 - 200))
        screen.blit(subprompt, (WIDTH//2 - subprompt.get_width()//2, HEIGHT//2 - 140))
        funny_font = pygame.font.SysFont(None, 32, italic=True)
        funny = funny_font.render(funny_msg, True, (180, 180, 255))
        screen.blit(funny, (WIDTH//2 - funny.get_width()//2, HEIGHT//2 + 70))
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
        txt_surface = font.render(text, True, (255,255,0))
        width = max(300, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+10))
        pygame.draw.rect(screen, color, input_box, 3)
        pygame.display.flip()
        clock.tick(60)
    return text.strip()