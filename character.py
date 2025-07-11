import pygame

class Character:
    def __init__(self, idle_img, fight_img, kick_img, facing_left=False, pos=(0, 0), stamina = 100):
        self.images = {
            "idle": idle_img,
            "fight": fight_img,
            "kick": kick_img,
            "idle_flipped": pygame.transform.flip(idle_img, True, False),
            "fight_flipped": pygame.transform.flip(fight_img, True, False),
            "kick_flipped": pygame.transform.flip(kick_img, True, False),
        }
        self.stamina = stamina
        self.facing_left = facing_left
        self.state = "idle"
        self.rect = self.images["idle"].get_rect(center=pos)
        # Edge detection flags for attacks
        self.prev_kick_key = False
        self.prev_punch_key = False
        self.attack_timer = 0  # ms
        self.attack_state = None

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
            # La miscare, imaginea trebuie sa fie idle (sau walk daca ai)
            self.state = "idle"
            moved = True
        if not moved:
            self.state = "idle"
        return moved

    def handle_event(self, event, allow_attack=True):
        if not allow_attack:
            return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                self.kick()
            elif event.key == pygame.K_f:
                self.punch()

    def kick(self):
        if self.stamina >= 20:
            self.state = "kick"
            self.attack_state = "kick"
            self.attack_timer = pygame.time.get_ticks()
            self.stamina -= 20
            if self.stamina < 0:
                self.stamina = 0

    def punch(self):
        if self.stamina >= 10:
            self.state = "fight"
            self.attack_state = "fight"
            self.attack_timer = pygame.time.get_ticks()
            self.stamina -= 10
            if self.stamina < 0:
                self.stamina = 0
            print(self.stamina)

    def get_image(self):
        key = self.state
        if self.facing_left:
            key += "_flipped"
        return self.images[key]

    def update(self, keys, dt=1.0, allow_attack=True):
        self.handle_input(keys, dt, allow_attack=allow_attack)
        # Animatie de atac ramane vizibila scurt timp
        if self.attack_state:
            now = pygame.time.get_ticks()
            if now - self.attack_timer < 180:  # ms
                self.state = self.attack_state
            else:
                self.attack_state = None
        # Regenerare stamina doar cand playerul e idle si stamina < 100
        if self.state == "idle" and self.stamina < 100:
            self.stamina += 1  # regen lent
            if self.stamina > 100:
                self.stamina = 100

    def draw(self, surface):
        surface.blit(self.get_image(), self.rect)

        
    def regenerate_stamina(self, amount):
        self.stamina += amount
        if self.stamina > 100:
            self.stamina = 100