import pygame
from pygame import mixer
import csv
import constants
import sys
from character import Character
import classes
from weapon import Weapon
from items import Item
from world import World
from button import Button
import keyboard_layout
from fart import FartAnimation

mixer.init()
pygame.init()

screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon Crawler")
music_volume = pygame.mixer.music.get_volume()

#create clock for maintaining frame rate
clock = pygame.time.Clock()

#define game variables
level = 1
start_game = False
pause_game = False
start_intro = False
screen_scroll = [0, 0]

#define player movement variables
moving_left = False
moving_right = False
moving_up = False
moving_down = False

#define font
font = pygame.font.Font("assets/fonts/AtariClassic.ttf", 20)

#helper function to scale image
def scale_img(image, scale):
  w = image.get_width()
  h = image.get_height()
  return pygame.transform.scale(image, (w * scale, h * scale))

#load music and sounds
pygame.mixer.music.load("assets/audio/music.wav")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1, 0.0, 5000)
shot_fx = pygame.mixer.Sound("assets/audio/arrow_shot.mp3")
shot_fx.set_volume(0.5)
hit_fx = pygame.mixer.Sound("assets/audio/arrow_hit.wav")
hit_fx.set_volume(0.5)
coin_fx = pygame.mixer.Sound("assets/audio/coin.wav")
coin_fx.set_volume(0.5)
heal_fx = pygame.mixer.Sound("assets/audio/heal.wav")
heal_fx.set_volume(0.5)
pick_up_potion_fx = pygame.mixer.Sound("assets/audio/pick_up_potion.mp3")
pick_up_potion_fx.set_volume(1)
death_fx = pygame.mixer.Sound("assets/audio/death.mp3")
death_fx.set_volume(0.5)
fart_fx = pygame.mixer.Sound("assets/audio/shart.mp3")
fart_fx.set_volume(0.5)

#load button images
start_img = scale_img(pygame.image.load("assets/images/buttons/PlayButton_Underworld_Escape.png").convert_alpha(), constants.BUTTON_SCALE)
exit_img = scale_img(pygame.image.load("assets/images/buttons/ExitButton_Underworld_Escape.png").convert_alpha(), constants.BUTTON_SCALE)
restart_img = scale_img(pygame.image.load("assets/images/buttons/button_restart.png").convert_alpha(), constants.BUTTON_SCALE)
resume_img = scale_img(pygame.image.load("assets/images/buttons/button_resume.png").convert_alpha(), constants.BUTTON_SCALE)
options_img = scale_img(pygame.image.load("assets/images/buttons/OptionsButton_Underworld_Escape.png").convert_alpha(), constants.BUTTON_SCALE)
layout_image_qwerty = pygame.image.load('assets/images/buttons/qwerty.png').convert_alpha()
layout_image_azerty = pygame.image.load('assets/images/buttons/azerty.png').convert_alpha()
background_image = pygame.image.load("assets/images/buttons/menu_background.png").convert_alpha()
background_image = pygame.transform.scale(background_image , (constants.SCREEN_WIDTH , constants.SCREEN_HEIGHT))

#load heart images
heart_empty = scale_img(pygame.image.load("assets/images/items/heart_empty.png").convert_alpha(), constants.ITEM_SCALE)
heart_half = scale_img(pygame.image.load("assets/images/items/heart_half.png").convert_alpha(), constants.ITEM_SCALE)
heart_full = scale_img(pygame.image.load("assets/images/items/heart_full.png").convert_alpha(), constants.ITEM_SCALE)

# Load fart images
fart_images = []
for i in range(6):  # Assuming 6 frames for the fart animation
    img = pygame.image.load(f"assets/images/fart/fart{i}.png").convert_alpha()
    img = scale_img(img, constants.ITEM_SCALE)
    fart_images.append(img)


#load coin images
coin_images = []
for x in range(4):
  img = scale_img(pygame.image.load(f"assets/images/items/coin_f{x}.png").convert_alpha(), constants.ITEM_SCALE)
  coin_images.append(img)

#load potion image
red_potion = scale_img(pygame.image.load("assets/images/items/Potion_4.png").convert_alpha(), 1)

item_images = []
item_images.append(coin_images)
item_images.append(red_potion)

#load weapon images
bow_image = scale_img(pygame.image.load("assets/images/weapons/bow.png").convert_alpha(), constants.WEAPON_SCALE)
arrow_image = scale_img(pygame.image.load("assets/images/weapons/arrow.png").convert_alpha(), constants.WEAPON_SCALE)
fireball_image = scale_img(pygame.image.load("assets/images/weapons/fireball.png").convert_alpha(), constants.FIREBALL_SCALE)

#load tilemap images
tile_list = []
for x in range(constants.TILE_TYPES):
  tile_image = pygame.image.load(f"assets/images/tiles/{x}.png").convert_alpha()
  tile_image = pygame.transform.scale(tile_image, (constants.TILE_SIZE, constants.TILE_SIZE))
  tile_list.append(tile_image)

#load character images
mob_animations = []
mob_types = ["elf", "imp", "skeleton", "goblin", "muddy", "tiny_zombie", "big_demon"]

#load the inventory images
inventory = pygame.image.load("assets/images/items/ItemSlot_3set_Underworld_Escape.png")

animation_types = ["idle", "run"]
for mob in mob_types:
  #load images
  animation_list = []
  for animation in animation_types:
    #reset temporary list of images
    temp_list = []
    for i in range(4):
      img = pygame.image.load(f"assets/images/characters/{mob}/{animation}/{i}.png").convert_alpha()
      img = scale_img(img, constants.SCALE)
      temp_list.append(img)
    animation_list.append(temp_list)
  mob_animations.append(animation_list)


#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

def fart():
    # Create a fart animation instance
    x = player.rect.centerx + 50  # Adjust position to the right of the player
    y = player.rect.centery
    fart_animation = FartAnimation(x, y, fart_images)
    fart_group.add(fart_animation)
    fart_fx.play()  # Play fart sound effect

#function for displaying game info
def draw_info():
  pygame.draw.rect(screen, constants.PANEL, (0, 0, constants.SCREEN_WIDTH, 50))
  pygame.draw.line(screen, constants.WHITE, (0, 50), (constants.SCREEN_WIDTH, 50))
  #draw lives
  half_heart_drawn = False
  for i in range(5):
    if player.health >= ((i + 1) * 20):
      screen.blit(heart_full, (10 + i * 50, 0))
    elif (player.health % 20 > 0) and half_heart_drawn == False:
      screen.blit(heart_half, (10 + i * 50, 0))
      half_heart_drawn = True
    else:
      screen.blit(heart_empty, (10 + i * 50, 0))

  #level
  draw_text("LEVEL: " + str(level), font, constants.WHITE, constants.SCREEN_WIDTH / 2, 15)
  #show score
  draw_text(f"X{player.score}", font, constants.WHITE, constants.SCREEN_WIDTH - 100, 15)

#function to reset level
def reset_level():
  damage_text_group.empty()
  arrow_group.empty()
  item_group.empty()
  fireball_group.empty()

  #create empty tile list
  data = []
  for row in range(constants.ROWS):
    r = [-1] * constants.COLS
    data.append(r)

  return data



#damage text class
class DamageText(pygame.sprite.Sprite):
  def __init__(self, x, y, damage, color):
    pygame.sprite.Sprite.__init__(self)
    self.image = font.render(damage, True, color)
    self.rect = self.image.get_rect()
    self.rect.center = (x, y)
    self.counter = 0

  def update(self):
    #reposition based on screen scroll
    self.rect.x += screen_scroll[0]
    self.rect.y += screen_scroll[1]

    #move damage text up
    self.rect.y -= 1
    #delete the counter after a few seconds
    self.counter += 1
    if self.counter > 30:
      self.kill()

#class for handling screen fade
class ScreenFade():
  def __init__(self, direction, colour, speed):
    self.direction = direction
    self.colour = colour
    self.speed = speed
    self.fade_counter = 0

  def fade(self):
    fade_complete = False
    self.fade_counter += self.speed
    if self.direction == 1:#whole screen fade
      pygame.draw.rect(screen, self.colour, (0 - self.fade_counter, 0, constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT))
      pygame.draw.rect(screen, self.colour, (constants.SCREEN_WIDTH // 2 + self.fade_counter, 0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
      pygame.draw.rect(screen, self.colour, (0, 0 - self.fade_counter, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT // 2))
      pygame.draw.rect(screen, self.colour, (0, constants.SCREEN_HEIGHT // 2 + self.fade_counter, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    elif self.direction == 2:#vertical screen fade down
      pygame.draw.rect(screen, self.colour, (0, 0, constants.SCREEN_WIDTH, 0 + self.fade_counter))

    if self.fade_counter >= constants.SCREEN_WIDTH:
      fade_complete = True

    return fade_complete


#create empty tile list
world_data = []
for row in range(constants.ROWS):
  r = [-1] * constants.COLS
  world_data.append(r)
#load in level data and create world
with open(f"levels/level{level}_data.csv", newline="") as csvfile:
  reader = csv.reader(csvfile, delimiter = ",")
  for x, row in enumerate(reader):
    for y, tile in enumerate(row):
      world_data[x][y] = int(tile)


world = World()
world.process_data(world_data, tile_list, item_images, mob_animations)

#create player
player = world.player
#create player's weapon
bow = Weapon(bow_image, arrow_image)

#extract enemies from world data
enemy_list = world.character_list

#create sprite groups
damage_text_group = pygame.sprite.Group()
arrow_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
fireball_group = pygame.sprite.Group()
fart_group = pygame.sprite.Group()

score_coin = Item(constants.SCREEN_WIDTH - 115, 23, 0, coin_images, True)
item_group.add(score_coin)
#add the items from the level data
for item in world.item_list:
  item_group.add(item)


#create screen fades
intro_fade = ScreenFade(1, constants.BLACK, 4)
death_fade = ScreenFade(2, constants.PINK, 4)

#create button
start_button = Button(constants.SCREEN_WIDTH // 2 - 225, constants.SCREEN_HEIGHT // 2 - 150, start_img)
exit_button = Button(constants.SCREEN_WIDTH // 2 - 225, constants.SCREEN_HEIGHT // 2 + 100, exit_img)
restart_button = Button(constants.SCREEN_WIDTH // 2 - 175, constants.SCREEN_HEIGHT // 2 - 50, restart_img)
resume_button = Button(constants.SCREEN_WIDTH // 2 - 175, constants.SCREEN_HEIGHT // 2 - 150, resume_img)
options_button = Button(constants.SCREEN_WIDTH // 2 - 225, constants.SCREEN_HEIGHT // 2 - 25, options_img )

x_image = pygame.image.load('assets/images/buttons/x_button.png').convert_alpha()
scaled_x_image = pygame.transform.scale(x_image, (50, 50))

transparent_surface = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT), pygame.SRCALPHA)
KEYBOARD_LAYOUT = "QWERTY"
MUSIC_VOLUME = 0.5


def settings_screen(screen):
    global KEYBOARD_LAYOUT, MUSIC_VOLUME , background_image , layout_image_qwerty, layout_image_azerty

    x_button = Button((constants.SCREEN_WIDTH / 2) + 550, (constants.SCREEN_HEIGHT / 2) - 350,scaled_x_image)
    slider = classes.Slider((constants.SCREEN_WIDTH / 2 - 200, constants.SCREEN_HEIGHT / 2 + 100), (400, 30), MUSIC_VOLUME * 100, 0, 100)
    layout_button_image = layout_image_qwerty
    slider = classes.Slider((constants.SCREEN_WIDTH / 2 - 200, constants.SCREEN_HEIGHT / 2 + 100), (400, 30), MUSIC_VOLUME * 100, 0, 100)
    click_count = 0 
    layout = keyboard_layout.Keyboard_layout(screen, (constants.SCREEN_WIDTH / 2), (constants.SCREEN_HEIGHT / 2))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # draw background image 
        screen.blit(background_image , (0,0))
       
       # Draw transparent background
        transparent_surface.fill((250,250,250, 155))
        screen.blit(transparent_surface, (0, 0))


        # Draw and handle X button
        if x_button.draw(screen):
            running = False


        # # Draw and handle layout button
        # layout_button = Button(constants.SCREEN_WIDTH / 2 - 100, constants.SCREEN_HEIGHT / 2 - 100, layout_button_image)
        # if layout_button.draw(screen):
        #   if constants.KEYBOARD_LAYOUT == 'QWERTY':
        #     constants.KEYBOARD_LAYOUT = 'AZERTY'
        #     layout_button_image = layout_image_azerty
        #   elif constants.KEYBOARD_LAYOUT == 'AZERTY':
        #     constants.KEYBOARD_LAYOUT = 'QWERTY'
        #     layout_button_image = layout_image_qwerty

        # # layout_button = Button(constants.SCREEN_WIDTH // 2 - 100, constants.SCREEN_HEIGHT // 2 - 100, layout_button_image)

        layout.draw()
        layout_font = pygame.font.Font('assets/fonts/AtariClassic.ttf', 50)
        layout_text = layout_font.render(constants.KEYBOARD_LAYOUT, True, "black")
        layout_rect = layout_text.get_rect(center = (constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2 - 100))
        screen.blit(layout_text, layout_rect)

        if layout.event():
            if constants.KEYBOARD_LAYOUT == "AZERTY":
                constants.KEYBOARD_LAYOUT = "QWERTY"
                print(constants.KEYBOARD_LAYOUT)
            elif constants.KEYBOARD_LAYOUT == "QWERTY":
                constants.KEYBOARD_LAYOUT = "AZERTY"
                print(constants.KEYBOARD_LAYOUT)

        if constants.KEYBOARD_LAYOUT == "AZERTY":
            instruction_lines = [
                "Z = Move Forward",
                "Q = Move Left",
                "S = Move Backwards",
                "D = Move Right",
                "Left-Click = Fire",
                "",
                "Item 1 = 1",
                "Item 2 = 2"
            ]
        elif constants.KEYBOARD_LAYOUT == "QWERTY":
            instruction_lines = [
                "W = Move Forward",
                "A = Move Left",
                "S = Move Backwards",
                "D = Move Right",
                "Left-Click = Fire",
                "",
                "Item 1 = 1",
                "Item 2 = 2"
            ]
        line_spacing = 5
        line_height = font.get_linesize() + line_spacing
        total_height = len(instruction_lines) * line_height - line_spacing
        # Create a surface for the instructions
        instructions_surface = pygame.Surface((600, total_height), pygame.SRCALPHA)  # Adjust width as needed
        instructions_surface.fill((0, 0, 0, 0))  # Transparent background

        # Render each line and blit it onto the surface
        for i, line in enumerate(instruction_lines):
            instructions_text = font.render(line, True, "black")
            instructions_surface.blit(instructions_text, (0, i * line_height))
        screen.blit(instructions_surface, (35, (constants.SCREEN_HEIGHT/2)-100))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            slider.handle_event(event)
        new_volume = slider.move_slider()
        pygame.mixer.music.set_volume(new_volume/100)
        slider.render(screen) 

        value_font = pygame.font.Font(None, 36)
        value_text = value_font.render(f"Music Volume: {int(slider.value)}", True, "black")
        text_rect = value_text.get_rect(center=(constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2 + 50))  

        screen.blit(value_text, text_rect)    

        pygame.display.flip()
  

#main game loop
run = True
while run:

  #control frame rate
  clock.tick(constants.FPS)

  if start_game == False:
    screen.blit(background_image, (0,0))
    if start_button.draw(screen):
      start_game = True
      start_intro = True
    if options_button.draw(screen):
      settings_screen(screen)
    if exit_button.draw(screen):
      run = False
  else:
    if pause_game == True:
      screen.fill(constants.MENU_BG)
      if resume_button.draw(screen):
        pause_game = False
      if exit_button.draw(screen):
        run = False
    else:
      screen.fill(constants.BG)

      if player.alive:
        #calculate player movement
        dx = 0
        dy = 0
        if moving_right == True:
          dx = constants.SPEED
        if moving_left == True:
          dx = -constants.SPEED
        if moving_up == True:
          dy = -constants.SPEED
        if moving_down == True:
          dy = constants.SPEED

        #move player
        screen_scroll, level_complete = player.move(dx, dy, world.obstacle_tiles, world.exit_tile)

        #update all objects
        world.update(screen_scroll)
        for enemy in enemy_list:
          fireball = enemy.ai(player, world.obstacle_tiles, screen_scroll, fireball_image)
          if fireball:
            fireball_group.add(fireball)
          if enemy.alive:
            enemy.update()
        player.update()
        arrow = bow.update(player)
        if arrow:
          arrow_group.add(arrow)
          shot_fx.play()
        for arrow in arrow_group:
          damage, damage_pos = arrow.update(screen_scroll, world.obstacle_tiles, enemy_list)
          if damage:
            damage_text = DamageText(damage_pos.centerx, damage_pos.y, str(damage), constants.RED)
            damage_text_group.add(damage_text)
            hit_fx.play()
        damage_text_group.update()
        fireball_group.update(screen_scroll, player)
        item_group.update(screen_scroll, player, coin_fx, pick_up_potion_fx)
        fart_group.update(screen_scroll)
        potion_img = scale_img(pygame.image.load(constants.POTION_IMG).convert_alpha(), 1)


      #draw player on screen
      world.draw(screen)
      for enemy in enemy_list:
        enemy.draw(screen)
      player.draw(screen)
      bow.draw(screen)
      for arrow in arrow_group:
        arrow.draw(screen)
      for fireball in fireball_group:
        fireball.draw(screen)
      damage_text_group.draw(screen)
      item_group.draw(screen)
      draw_info()
      screen.blit(inventory, (100, 750))
      fart_img = scale_img(pygame.image.load("assets/images/fart/fart3.png").convert_alpha(), 2)
      screen.blit(fart_img, (202, 752))
      rotated_bow_image = pygame.transform.rotate(bow_image, -35)
      screen.blit(rotated_bow_image, (72, 732))
      screen.blit(potion_img, (190, 772))

      score_coin.draw(screen)
      fart_group.draw(screen)

      #check level complete
      if level_complete == True:
        start_intro = True
        level += 1
        world_data = reset_level()
        #load in level data and create world
        with open(f"levels/level{level}_data.csv", newline="") as csvfile:
          reader = csv.reader(csvfile, delimiter = ",")
          for x, row in enumerate(reader):
            for y, tile in enumerate(row):
              world_data[x][y] = int(tile)
        world = World()
        world.process_data(world_data, tile_list, item_images, mob_animations)
        temp_hp = player.health
        temp_score = player.score
        player = world.player
        player.health = temp_hp
        player.score = temp_score
        enemy_list = world.character_list
        score_coin = Item(constants.SCREEN_WIDTH - 115, 23, 0, coin_images, True)
        item_group.add(score_coin)
        #add the items from the level data
        for item in world.item_list:
          item_group.add(item)


      #show intro
      if start_intro == True:
        if intro_fade.fade():
          start_intro = False
          intro_fade.fade_counter = 0

      #show death screen
      if player.alive == False:
        if death_fade.fade():
          if restart_button.draw(screen):
            death_fade.fade_counter = 0
            start_intro = True
            world_data = reset_level()
            #load in level data and create world
            with open(f"levels/level{level}_data.csv", newline="") as csvfile:
              reader = csv.reader(csvfile, delimiter = ",")
              for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                  world_data[x][y] = int(tile)
            world = World()
            world.process_data(world_data, tile_list, item_images, mob_animations)
            temp_score = player.score
            player = world.player
            player.score = temp_score
            enemy_list = world.character_list
            score_coin = Item(constants.SCREEN_WIDTH - 115, 23, 0, coin_images, True)
            item_group.add(score_coin)
            #add the items from the level data
            for item in world.item_list:
              item_group.add(item)

  #event handler
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
    #take keyboard presses
    if constants.KEYBOARD_LAYOUT == "QWERTY":
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_a:
          moving_left = True
        if event.key == pygame.K_d:
          moving_right = True
        if event.key == pygame.K_w:
          moving_up = True
        if event.key == pygame.K_s:
          moving_down = True
        if event.key == pygame.K_ESCAPE:
          pause_game = True
        if event.key == pygame.K_2:
            fart()
        if event.key == pygame.K_1:
          if constants.POTION_COUNT == 1:
            constants.POTION_COUNT -= 1
            constants.POTION_IMG = "assets/images/items/Potion_0.png"; potion_img = pygame.image.load(constants.POTION_IMG)
            Item.used(screen, player, heal_fx, potion_img)
            print(constants.POTION_COUNT)
          elif constants.POTION_COUNT == 2:
            constants.POTION_COUNT -= 1
            constants.POTION_IMG = "assets/images/items/Potion_1.png"; potion_img = pygame.image.load(constants.POTION_IMG)
            Item.used(screen, player, heal_fx, potion_img)
            print(constants.POTION_COUNT)
          elif constants.POTION_COUNT == 3:
            constants.POTION_COUNT -= 1
            constants.POTION_IMG = "assets/images/items/Potion_2.png"; potion_img = pygame.image.load(constants.POTION_IMG)
            Item.used(screen, player, heal_fx, potion_img)
            print(constants.POTION_COUNT)
          elif constants.POTION_COUNT == 4:
            constants.POTION_COUNT -= 1
            constants.POTION_IMG = "assets/images/items/Potion_3.png"; potion_img = pygame.image.load(constants.POTION_IMG)
            Item.used(screen, player, heal_fx, potion_img)
            print(constants.POTION_COUNT) 

    if constants.KEYBOARD_LAYOUT == "AZERTY":
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_q:
          moving_left = True
        if event.key == pygame.K_d:
          moving_right = True
        if event.key == pygame.K_z:
          moving_up = True
        if event.key == pygame.K_s:
          moving_down = True
        if event.key == pygame.K_ESCAPE:
          pause_game = True 
        if event.key == pygame.K_2:
            fart()
        if event.key == pygame.K_1:
          if constants.POTION_COUNT == 1:
            constants.POTION_COUNT -= 1
            constants.POTION_IMG = "assets/images/items/Potion_0.png"; potion_img = pygame.image.load(constants.POTION_IMG)
            Item.used(screen, player, heal_fx, potion_img)
            print(constants.POTION_COUNT)
          elif constants.POTION_COUNT == 2:
            constants.POTION_COUNT -= 1
            constants.POTION_IMG = "assets/images/items/Potion_1.png"; potion_img = pygame.image.load(constants.POTION_IMG)
            Item.used(screen, player, heal_fx, potion_img)
            print(constants.POTION_COUNT)
          elif constants.POTION_COUNT == 3:
            constants.POTION_COUNT -= 1
            constants.POTION_IMG = "assets/images/items/Potion_2.png"; potion_img = pygame.image.load(constants.POTION_IMG)
            Item.used(screen, player, heal_fx, potion_img)
            print(constants.POTION_COUNT)
          elif constants.POTION_COUNT == 4:
            constants.POTION_COUNT -= 1
            constants.POTION_IMG = "assets/images/items/Potion_3.png"; potion_img = pygame.image.load(constants.POTION_IMG)
            Item.used(screen, player, heal_fx, potion_img)
            print(constants.POTION_COUNT) 

    #keyboard button released
    if constants.KEYBOARD_LAYOUT == "QWERTY":
      if event.type == pygame.KEYUP:
        if event.key == pygame.K_a:
          moving_left = False
        if event.key == pygame.K_d:
          moving_right = False
        if event.key == pygame.K_w:
          moving_up = False
        if event.key == pygame.K_s:
          moving_down = False
        

    if constants.KEYBOARD_LAYOUT == "AZERTY":
      if event.type == pygame.KEYUP:
        if event.key == pygame.K_q:
          moving_left = False
        if event.key == pygame.K_d:
          moving_right = False
        if event.key == pygame.K_z:
          moving_up = False
        if event.key == pygame.K_s:
          moving_down = False

      

  pygame.display.update()


pygame.quit()