import pygame

class Keyboard_layout():
    def __init__(self, surface, width, height):
        self.surface = surface
        self.width = width
        self.height = height
        self.container_rect = pygame.Rect(self.width - 125, self.height - 150, 250, 100)
        self.clicked = False

    def draw(self):
        pygame.draw.rect(self.surface, (50, 50, 50), (self.width - 164, self.height - 150, 326 + 5, 100+5), border_radius=24)
        pygame.draw.rect(self.surface, "darkgrey", (self.width - 164, self.height - 150, 326, 100), border_radius=24)
    
    def event(self):
        action = False
        #Gets the position of the cursor on the app
        pos = pygame.mouse.get_pos()
        #Checks to see if the mouse is hovering over the image
        if self.container_rect.collidepoint(pos):
            #checks to see if the mouse clicked on the image
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
            #checks to see if the mouse is no longer clicked on the image
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        return action