import pygame
import random
import subprocess
import json

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

class MySprite(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()

world_map = pygame.image.load("Sprites/world_map_big.png")

character = MySprite("Sprites/definitely_character.png")
character.rect.topleft = (screen_width // 2, screen_height // 2)

hero_portrait = MySprite("Sprites/male_portrait.png")
hero_portrait.rect.topleft = (25, 25)

heroine_portrait = MySprite("Sprites/female_portrait.png")
heroine_portrait.rect.topleft = (-50, 250)

cursor = MySprite("Sprites/Cursor_small.png")
cursorx = 600
cursory = 60
cursor.rect.topleft = (cursorx, cursory)

# Sprite groups
all_sprites = pygame.sprite.Group()
all_sprites.add()

#Labels
font = pygame.font.SysFont(None, 40)
font2 = pygame.font.SysFont(None, 20)

items_label = font.render("Items", True, (255, 255, 255))
hero_name = font2.render("Arion", True, (255, 255, 255))
heroine_name = font2.render("Aria", True, (255, 255, 255))

hero_level_label = font2.render("Level ", True, (255, 255, 255))
heroine_level_label = font2.render("Level ", True, (255, 255, 255))
hero_hp_label = font2.render("", True, (255, 255, 255))
heroine_hp_label = font2.render("", True, (255, 255, 255))

instructions = font2.render("", True, (255, 255, 255))
potions_label = font.render("", True, (255, 255, 255))


# Camera position
camera_x = character.rect.x - screen_width // 2
camera_y = character.rect.y - screen_height // 2

encounter = 0
battle = False
menu = False
item_menu = False


# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle player input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False
    if keys[pygame.K_UP] and not menu:
        character.rect.y -= 5
        encounter = random.randint(0, 10000)
        if encounter >= 9950:
            battle = True
    if keys[pygame.K_DOWN] and not menu:
        character.rect.y += 5
        encounter = random.randint(0, 10000)
        if encounter >= 9950:
            battle = True
    if keys[pygame.K_LEFT] and not menu:
        character.rect.x -= 5
        encounter = random.randint(0, 10000)
        if encounter >= 9950:
            battle = True
    if keys[pygame.K_RIGHT] and not menu:
        character.rect.x += 5
        encounter = random.randint(0, 10000)
        if encounter >= 9950:
            battle = True
    elif keys[pygame.K_p] and not menu:
        menu = True
        pygame.time.delay(100)
    elif keys[pygame.K_p] and menu:
        menu = False
        pygame.time.delay(100)
    if keys[pygame.K_RETURN] and menu and cursory == 60 and not item_menu:
        world_map = pygame.image.load("Sprites/items_menu.png")
        all_sprites.remove(hero_portrait)
        all_sprites.remove(heroine_portrait)
        items_label = font.render("", True, (255, 255, 255))
        heroine_name = font2.render("", True, (255, 255, 255))
        hero_name = font2.render("", True, (255, 255, 255))
        hero_level_label = font2.render("", True, (255, 255, 255))
        heroine_level_label = font2.render("", True, (255, 255, 255))
        hero_hp_label = font2.render("", True, (255, 255, 255))
        heroine_hp_label = font2.render("", True, (255, 255, 255))
        instructions = font.render("Select an item to use", True, (255, 255, 255))
        cursorx = 100
        cursory = 80
        item_menu = True
        pygame.time.delay(100)
    elif keys[pygame.K_RETURN] and item_menu and cursory == 80:
        instructions = font.render("Use on whom?", True, (255, 255, 255))
        hero_portrait.rect.topleft = (500, 100)
        heroine_portrait.rect.topleft = (450, 350)
        all_sprites.add(hero_portrait)
        all_sprites.add(heroine_portrait)

        with open("Data/hero_data.json") as file:
            hero_data = json.load(file)
            hero_level = hero_data["level"]
            hero_hp = hero_data["hp"]
            hero_max_hp = hero_data["max hp"]

        with open("Data/heroine_data.json") as file:
            heroine_data = json.load(file)
            heroine_level = heroine_data["level"]
            heroine_hp = heroine_data["hp"]
            heroine_max_hp = heroine_data["max hp"]

        hero_hp_label = font2.render("HP " + str(hero_hp) + "/" + str(hero_max_hp), True, (255, 255, 255))
        heroine_hp_label = font2.render("HP " + str(heroine_hp) + "/" + str(heroine_max_hp), True, (255, 255, 255))
        screen.blit(hero_hp_label, (450, 100))
        screen.blit(heroine_hp_label, (400, 350))


    if menu and not item_menu:
        all_sprites.remove(character)
        world_map = pygame.image.load("Sprites/menu.png")
    if item_menu:
        with open ("Data/items.json") as file:
            item_data = json.load(file)
            potions = item_data["potion"]
        potions_label = font2.render("Potions " + str(potions), True, (255, 255, 255))

    # Update camera position based on character movement
    camera_x = character.rect.x - screen_width // 2
    camera_y = character.rect.y - screen_height // 2

    # Clamp camera position to stay within the world map boundaries
    camera_x = max(0, min(camera_x, world_map.get_width() - screen_width))
    camera_y = max(0, min(camera_y, world_map.get_height() - screen_height))

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the visible portion of the world map
    screen.blit(world_map, (0, 0), (camera_x, camera_y, screen_width, screen_height))

    # Draw the character at the center of the screen
    character_screen_pos = (screen_width // 2 - character.rect.width // 2, screen_height // 2 - character.rect.height // 2)
    if not menu and not item_menu:
        world_map = pygame.image.load("Sprites/world_map_big.png")
        screen.blit(character.image, character_screen_pos)
        all_sprites.remove(hero_portrait)
        all_sprites.remove(heroine_portrait)
        all_sprites.remove(cursor)
        items_label = font.render("", True, (255, 255, 255))
        heroine_name = font2.render("", True, (255, 255, 255))
        hero_name = font2.render("", True, (255, 255, 255))
        hero_level_label = font2.render("", True, (255, 255, 255))
        heroine_level_label = font2.render("", True, (255, 255, 255))
        hero_hp_label = font2.render("", True, (255, 255, 255))
        heroine_hp_label = font2.render("", True, (255, 255, 255))
    elif menu and not item_menu:
        with open("Data/hero_data.json") as file:
            hero_data = json.load(file)
            hero_level = hero_data["level"]
            hero_hp = hero_data["hp"]
            hero_max_hp = hero_data["max hp"]

        with open("Data/heroine_data.json") as file:
            heroine_data = json.load(file)
            heroine_level = heroine_data["level"]
            heroine_hp = heroine_data["hp"]
            heroine_max_hp = heroine_data["max hp"]

        all_sprites.add(hero_portrait)
        all_sprites.add(heroine_portrait)
        all_sprites.add(cursor)
        items_label = font.render("Items", True, (255, 255, 255))
        hero_name = font.render("Arion", True, (255, 255, 255))
        heroine_name = font.render("Aria", True, (255, 255, 255))
        hero_level_label = font2.render("Level " + str(hero_level), True, (255, 255, 255))
        heroine_level_label = font2.render("Level " + str(heroine_level), True, (255, 255, 255))
        hero_hp_label = font2.render("HP " + str(hero_hp) + "/" + str(hero_max_hp), True, (255, 255, 255))
        heroine_hp_label = font2.render("HP " + str(heroine_hp) + "/" + str(heroine_max_hp), True, (255, 255, 255))
    screen.blit(items_label, (650, 75))
    screen.blit(hero_name, (300, 50))
    screen.blit(heroine_name, (300, 250))
    screen.blit(hero_level_label, (300, 100))
    screen.blit(heroine_level_label, (300, 300))
    screen.blit(instructions, (250, 25))
    screen.blit(potions_label, (150, 100))
    if not item_menu:
        screen.blit(hero_hp_label, (300, 125))
        screen.blit(heroine_hp_label, (300, 325))
    cursor.rect.topleft = (cursorx, cursory)
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)

# Quit the game
pygame.quit()