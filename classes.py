import pygame 
import constants

class Slider:
    def __init__(self, position, size, value, min_value, max_value):
        self.rect = pygame.Rect(position, size)
        self.value = value
        self.min_value = min_value
        self.max_value = max_value
        self.handle_rect = pygame.Rect(0, 0, size[1], size[1])
        self.handle_rect.center = (position[0] + (value / max_value) * size[0], position[1] + size[1] // 2)
        self.dragging = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.handle_rect.collidepoint(event.pos):
            self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            new_x = min(max(event.pos[0], self.rect.left), self.rect.right)
            self.handle_rect.centerx = new_x
            self.value = self.min_value + (new_x - self.rect.left) / self.rect.width * (self.max_value - self.min_value)

    def move_slider(self):
        return self.value

    def render(self, surface):
        pygame.draw.rect(surface, (200, 200, 200), self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)
        pygame.draw.ellipse(surface, (100, 100, 255), self.handle_rect)

class KeyboardLayout:
    def __init__(self, surface, x, y):
        self.surface = surface
        self.x = x
        self.y = y

    def draw(self):
        layout_text = pygame.font.Font(None, 36).render("Keyboard Layout: " + constants.KEYBOARD_LAYOUT, True, "black")
        layout_rect = layout_text.get_rect(center=(self.x, self.y))
        self.surface.blit(layout_text, layout_rect)

    def event(self):
        action = False
        #Gets the position of the cursor on the app
        pos = pygame.mouse.get_pos()
        #Checks to see if the mouse is hovering over the image
        if self.container_rect.collidepoint(pos):
            print("HORAY")
            #checks to see if the mouse clicked on the image
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
            #checks to see if the mouse is no longer clicked on the image
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        return action
