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

    def handle_input(self, keys):
        moved = False
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
            self.facing_left = True
            self.state = "fight"
            moved = True
        elif keys[pygame.K_RIGHT]:
            self.rect.x += 5
            self.facing_left = False
            self.state = "fight"
            moved = True
        elif keys[pygame.K_UP]:
            self.rect.y -= 5
            self.state = "fight"
            moved = True
        elif keys[pygame.K_DOWN]:
            self.rect.y += 5
            self.state = "fight"
            moved = True
        else:
            self.state = "idle"
        return moved

    def kick(self):
        self.state = "kick"

    def get_image(self):
        key = self.state
        if self.facing_left:
            key += "_flipped"
        return self.images[key]

    def update(self, keys):
        self.handle_input(keys)

    def draw(self, surface):
        surface.blit(self.get_image(), self.rect)