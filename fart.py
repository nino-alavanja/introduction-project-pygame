import pygame


class FartAnimation(pygame.sprite.Sprite):
    def __init__(self, x, y, images):
        super().__init__()
        self.images = images  # List of fart animation frames
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.animation_speed = 5  # Controls the speed of animation
        self.counter = 0

    def update(self, screen_scroll):
        # Update position based on screen scroll
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

        # Update animation frame
        self.counter += 1
        if self.counter >= self.animation_speed:
            self.counter = 0
            self.frame_index += 1
            if self.frame_index < len(self.images):
                self.image = self.images[self.frame_index]
            else:
                self.kill()  # Remove sprite when animation is complete
