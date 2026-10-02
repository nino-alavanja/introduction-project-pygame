import pygame

class Button():
  def __init__(self, x, y, image):
    self.image = image
    self.rect = self.image.get_rect()
    self.rect.topleft = (x, y)
    self.clicked = False

  def draw(self, surface):
    action = False

    #get mouse position
    pos = pygame.mouse.get_pos()

    #check mouseover and clicked conditions
    if self.rect.collidepoint(pos):
      if pygame.mouse.get_pressed()[0] and self.clicked == False:
        action = True
        self.clicked = True
      
      if pygame.mouse.get_pressed()[0] == 0:
        self.clicked = False


    surface.blit(self.image, self.rect)

    return action