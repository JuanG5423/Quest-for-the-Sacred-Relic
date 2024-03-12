import pygame
import random
import json

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()

# Character class
class Character(pygame.sprite.Sprite):
    def __init__(self, filename, data_filename, Defending, Turn, targets):
        super().__init__()
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect()
        self.data_filename = data_filename
        self.targets = targets
        self.Turn = Turn
        self.Defending = Defending
        self.stats = {}

    def add_target(self, target):
        self.Target.append(target)

    def update_stats(self, stats):
        self.stats = stats
        with open(self.data_filename, 'w') as file:
            json.dump(stats, file)

    def get_stats(self):
        with open(self.data_filename, 'r') as file:
            stats = json.load(file)
            return stats

    def update_hp(self, hp):
        stats = self.get_stats()
        stats['hp'] = hp
        self.update_stats(stats)

    def get_hp(self):
        stats = self.get_stats()
        return stats['hp']

    def update_strength(self, strength):
        stats = self.get_stats()
        stats['strength'] = strength
        self.update_stats(stats)

    def get_strength(self):
        stats = self.get_stats()
        return stats['strength']

    def update_defense(self, defense):
        stats = self.get_stats()
        stats['defense'] = defense
        self.update_stats(stats)

    def get_defense(self):
        stats = self.get_stats()
        return stats['defense']

    def get_level(self):
        stats = self.get_stats()
        return stats['level']

    def attack(self, target):
        if self.get_strength() - target.Defense <= 0:
            target.update_hp(target.get_hp() - 1)
        else:
            target.update_hp(target.get_hp() - (self.get_strength() - target.Defense))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, filename, hp_filename, Strength, Defense, Turn, targets):
        super().__init__()
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect()
        self.hp_filename = hp_filename
        self.Strength = Strength
        self.Defense = Defense
        self.targets = targets
        self.Turn = Turn

    def add_target(self, target):
        self.Target.append(target)

    def update_hp(self, hp):
        with open(self.hp_filename, 'w') as file:
            file.write(str(hp))

    def get_hp(self):
        with open(self.hp_filename, 'r') as file:
            hp = file.read()
            return int(hp)

    def attack(self, target):
        if self.Strength - target.get_defense() <= 0:
            target.update_hp(target.get_hp() - 1)
        else:
            target.update_hp(target.get_hp() - (self.Strength - target.get_defense()))

class MySprite(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()

hero_targets = []
heroine_targets = []
enemy_targets = []
enemy2_targets = []

# Create character objects
hero = Character("Sprites/Male.png", "hero_data.json", False, True, hero_targets)
hero.rect.topleft = (400, 100)
hero_base_defense = hero.get_defense()

heroine = Character("Sprites/Female.png", "heroine_data.json", False, False, heroine_targets)
heroine.rect.topleft = (400, 300)
heroine_base_defense = heroine.get_defense()

enemy = Enemy("Sprites/Slime.png", "enemy_hp.txt", 2, 0, False, enemy_targets)
enemy.rect.topleft = (100, 100)
enemy_hp = enemy.get_hp()

enemy2 = Enemy("Sprites/Wolf.png", "enemy2_hp.txt", 4, 1, False, enemy2_targets)
enemy2.rect.topleft = (100, 300)
enemy2_hp = enemy2.get_hp()

cursor_sprite = MySprite("Sprites/Cursor.png")
cursorx = 40
cursory = 120
cursor_sprite.rect.topleft = (cursorx, cursory)

hero_targets.append(enemy)
hero_targets.append(enemy2)
heroine_targets.append(enemy)
heroine_targets.append(enemy2)
enemy_targets.append(hero)
enemy_targets.append(heroine)
enemy2_targets.append(hero)
enemy2_targets.append(heroine)

# Sprite groups
all_sprites = pygame.sprite.Group(hero, heroine, enemy, enemy2, cursor_sprite)
hero_targets = pygame.sprite.Group(enemy, enemy2)
heroine_targets = pygame.sprite.Group(enemy, enemy2)


# Game loop
command = ""
running = True
paused = False
targeting = False
transition = False
cursor = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            enemy.update_hp(enemy_hp)
            enemy2.update_hp(enemy2_hp)
            if hero.Defending:
                hero.update_defense(hero_base_defense)
            if heroine.Defending:
                heroine.update_defense(heroine_base_defense)
            running = False

    # Handle player input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        enemy.update_hp(enemy_hp)
        enemy2.update_hp(enemy2_hp)
        if hero.Defending:
            hero.update_defense(hero_base_defense)
        if heroine.Defending:
            heroine.update_defense(heroine_base_defense)
        running = False
    if (hero.Turn or heroine.Turn) and not transition:
        if hero.Turn and hero.Defending:
            hero.Defending = False
            hero.update_defense(heroine_base_defense)
        if heroine.Turn and heroine.Defending:
            heroine.Defending = False
            heroine.update_defense(heroine_base_defense)
        if hero.Turn and hero.get_hp() <= 0:
            hero.Turn = False
            enemy.Turn = True
            continue
        elif heroine.Turn and heroine.get_hp() <= 0:
            heroine.Turn = False
            enemy2.Turn = True
            continue
        if not targeting:
            command = "Command?"
        if (keys[pygame.K_DOWN] or keys[pygame.K_UP]) and cursor == 0 and not targeting:
            cursor = 1
            pygame.time.delay(100)
        elif (keys[pygame.K_DOWN] or keys[pygame.K_UP]) and cursor == 1 and not targeting:
            cursor = 0
            pygame.time.delay(100)
        elif keys[pygame.K_DOWN] and targeting and cursory == 120:
            cursory = 320
            pygame.time.delay(100)
        elif keys[pygame.K_UP] and targeting and cursory == 320:
            cursory = 120
            pygame.time.delay(100)
        if hero.Turn:
            if keys[pygame.K_RETURN] and cursor == 0 and not targeting:
                pygame.time.delay(100)
                try:
                    bababui = hero_targets.sprites()[1]
                    command = "There are multiple enemies, which one do you attack?"
                    pygame.time.delay(100)
                    targeting = True
                except IndexError:
                    hero.attack(hero_targets.sprites()[0])
                    command = "You attack the enemy"
                    hero.Turn = False
                    enemy.Turn = True
                    transition = True
                    cursor = 0
            elif keys[pygame.K_RETURN] and cursory == 120 and targeting:
                hero.attack(hero_targets.sprites()[0])
                command = "You attack the enemy"
                targeting = False
                hero.Turn = False
                enemy.Turn = True
                transition = True
                cursory = 120
                cursor = 0
                pygame.time.delay(100)
            elif keys[pygame.K_RETURN] and cursory == 320 and targeting:
                hero.attack(hero_targets.sprites()[1])
                command = "You attack the enemy"
                targeting = False
                hero.Turn = False
                enemy.Turn = True
                transition = True
                cursory = 120
                cursor = 0
                pygame.time.delay(100)
            elif keys[pygame.K_RETURN] and cursor == 1:
                command = "You defend"
                hero.Defending = True
                hero.update_defense(heroine_base_defense * 2)
                pygame.time.delay(100)
                hero.Turn = False
                enemy.Turn = True
                transition = True
                cursor = 0
        elif heroine.Turn:
            if keys[pygame.K_RETURN] and cursor == 0 and not targeting:
                pygame.time.delay(100)
                try:
                    bababui = heroine_targets.sprites()[1]
                    command = "There are multiple enemies, which one do you attack?"
                    pygame.time.delay(100)
                    targeting = True
                except IndexError:
                    heroine.attack(heroine_targets.sprites()[0])
                    command = "You attack the enemy"
                    heroine.Turn = False
                    enemy2.Turn = True
                    transition = True
                    cursor = 0
            elif keys[pygame.K_RETURN] and cursory == 120 and targeting:
                heroine.attack(heroine_targets.sprites()[0])
                command = "You attack the enemy"
                targeting = False
                heroine.Turn = False
                enemy2.Turn = True
                cursory = 120
                transition = True
                cursor = 0
                pygame.time.delay(100)
            elif keys[pygame.K_RETURN] and cursory == 320 and targeting:
                heroine.attack(heroine_targets.sprites()[1])
                command = "You attack the enemy"
                targeting = False
                heroine.Turn = False
                enemy2.Turn = True
                cursory = 120
                transition = True
                cursor = 0
                pygame.time.delay(100)
            elif keys[pygame.K_RETURN] and cursor == 1:
                command = "You defend"
                heroine.Defending = True
                heroine.update_defense(heroine_base_defense * 2)
                pygame.time.delay(100)
                heroine.Turn = False
                enemy2.Turn = True
                transition = True
                cursor = 0
    elif enemy.Turn and not transition:
        if enemy.get_hp() <= 0:
            enemy.Turn = False
            heroine.Turn = True
        else:
            enemy.attack(enemy_targets[random.randint(0, len(enemy_targets) - 1)])
            command = "The enemy attacks you"
            enemy.Turn = False
            heroine.Turn = True
            transition = True
    elif enemy2.Turn and not transition:
        if enemy2.get_hp() <= 0:
            enemy2.Turn = False
            hero.Turn = True
            transition = True
        else:
            enemy2.attack(enemy2_targets[random.randint(0, len(enemy2_targets) - 1)])
            command = "The enemy attacks you"
            enemy2.Turn = False
            hero.Turn = True
            transition = True
    elif transition and keys[pygame.K_RETURN]:
        transition = False
        pygame.time.delay(100)

    # Update character targeting
    for character in all_sprites: #all_sprites [sprite, sprite2]
        if character in hero_targets and character.get_hp() <= 0:
            hero_targets.remove(character)
            all_sprites.remove(character)
        if character in heroine_targets and character.get_hp() <= 0:
            heroine_targets.remove(character)
            all_sprites.remove(character)
        if character in enemy_targets and character.get_hp() <= 0:
            enemy_targets.remove(character)
            all_sprites.remove(character)
        if character in enemy2_targets and character.get_hp() <= 0:
            enemy2_targets.remove(character)
            all_sprites.remove(character)

    # Update labels
    attack_color = (255, 255, 255)
    defend_color = (255, 255, 255)

    if cursor == 0:
        attack_color = (0, 255, 0)
    elif cursor == 1:
        defend_color = (0, 255, 0)

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw sprites
    if not targeting:
        all_sprites.remove(cursor_sprite)
    elif targeting:
        all_sprites.add(cursor_sprite)
    all_sprites.draw(screen)
    # Draw labels
    font = pygame.font.SysFont(None, 20)
    events_label = font.render(command, True, (255, 255, 255))
    hp_label = font.render("HP: " + str(hero.get_hp()), True, (255, 255, 255))
    hp_label2 = font.render("HP: " + str(heroine.get_hp()), True, (255, 255, 255))
    if targeting or (not hero.Turn and not heroine.Turn) or transition:
        attack_label = font.render("", True, attack_color)
        defend_label = font.render("", True, defend_color)
    else:
        attack_label = font.render("Attack", True, attack_color)
        defend_label = font.render("Defend", True, defend_color)
    if hero.get_hp() <= 0 and heroine.get_hp() <= 0 and not transition:
        command = "You ded"
        hero.Turn = False
        heroine.Turn = False
        enemy.Turn = False
        enemy2.Turn = False
        hp_label = font.render("", True, (255, 255, 255))
        hp_label2 = font.render("", True, (255, 255, 255))
        attack_label = font.render("", True, attack_color)
        defend_label = font.render("", True, defend_color)
        events_label = font.render(command, True, (255, 255, 255))
        all_sprites.remove(enemy)
        all_sprites.remove(enemy2)
        all_sprites.draw(screen)
        enemy.update_hp(enemy_hp)
        enemy2.update_hp(enemy2_hp)
        if hero.Defending:
            hero.update_defense(hero_base_defense)
        if heroine.Defending:
            heroine.update_defense(heroine_base_defense)
        running = False
    elif enemy.get_hp() <= 0 and enemy2.get_hp() <= 0 and not transition:
        command = "You win!"
        hero.Turn = False
        heroine.Turn = False
        enemy.Turn = False
        enemy2.Turn = False
        hp_label = font.render("", True, (255, 255, 255))
        hp_label2 = font.render("", True, (255, 255, 255))
        attack_label = font.render("", True, attack_color)
        defend_label = font.render("", True, defend_color)
        events_label = font.render(command, True, (255, 255, 255))
        all_sprites.remove(hero)
        all_sprites.remove(heroine)
        all_sprites.draw(screen)
        enemy.update_hp(enemy_hp)
        enemy2.update_hp(enemy2_hp)
        running = False

    if hero.get_hp() <= 0:
        hp_label = font.render("", True, (255, 255, 255))
    if heroine.get_hp() <= 0:
        hp_label2 = font.render("", True, (255, 255, 255))

    screen.blit(events_label, (150, 500))
    screen.blit(attack_label, (425, 475))
    screen.blit(defend_label, (425, 510))
    screen.blit(hp_label, (500, 150))
    screen.blit(hp_label2, (500, 395))

    # Update the display
    cursor_sprite.rect.topleft = (cursorx, cursory)
    pygame.display.flip()
    clock.tick(60)

# Quit the game
pygame.quit()