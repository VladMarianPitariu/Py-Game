import pygame

class Character:
    def __init__(self, idle_img, fight_img, kick_img, facing_left=False, pos=(0, 0)):
        self.images = {
            "idle": idle_img,
            "fight": fight_img,
            "kick": kick_img,
            "idle_flipped": pygame.transform.flip(idle_img, True, False),
            "fight_flipped": pygame.transform.flip(fight_img, True, False),
            "kick_flipped": pygame.transform.flip(kick_img, True, False),
        }
        self.facing_left = facing_left
        self.state = "idle"
        self.rect = self.images["idle"].get_rect(center=pos)

    def handle_input(self, keys, dt=1.0, allow_attack=True):
        moved = False
        speed = 20 * dt  # viteza marita pentru bossfight, ajustabil
        dx = 0
        dy = 0
        # Miscare combinata (diagonala, smooth, nu se anuleaza sus/jos sau stanga/dreapta)
        left = keys[pygame.K_LEFT] or keys[pygame.K_a]
        right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
        up = keys[pygame.K_UP] or keys[pygame.K_w]
        down = keys[pygame.K_DOWN] or keys[pygame.K_s]
        if left:
            dx -= 1
            self.facing_left = True
        if right:
            dx += 1
            self.facing_left = False
        if up:
            dy -= 1
        if down:
            dy += 1
        # Normalizeaza pentru diagonala (dar permite miscarea simultana sus/jos si stanga/dreapta)
        if dx != 0 or dy != 0:
            length = (dx**2 + dy**2) ** 0.5
            if length > 0:
                dx = dx / length * speed
                dy = dy / length * speed
            self.rect.x += int(dx)
            self.rect.y += int(dy)
            self.state = "fight"
            moved = True
        # Atac (X sau F) - doar daca allow_attack e True
        if allow_attack and (keys[pygame.K_x] or keys[pygame.K_f]):
            self.kick()
            moved = True
        if not moved:
            self.state = "idle"
        return moved

    def kick(self):
        self.state = "kick"

    def get_image(self):
        key = self.state
        if self.facing_left:
            key += "_flipped"
        return self.images[key]

    def update(self, keys, dt=1.0, allow_attack=True):
        self.handle_input(keys, dt, allow_attack=allow_attack)

    def draw(self, surface):
        surface.blit(self.get_image(), self.rect)