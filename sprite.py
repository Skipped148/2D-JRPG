import pygame
from config import *
import math
import random

class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprite
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0
        self.health = 50
        self.max_health = 50
        self.level = 1
        self.exp = 0
        self.max_stamina = 100
        self.stamina = self.max_stamina
        self.defending = False
        self.combo_counter = 0
        self.last_attack_time = 0
        self.element = "normal"  
        self.special_charges = 0
        self.facing = 'down'
        self.animation_loop = 1

        self.down_animations = [
            self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height),
            self.game.character_spritesheet.get_sprite(35, 2, self.width, self.height),
            self.game.character_spritesheet.get_sprite(68, 2, self.width, self.height)
        ]
        self.left_animations = [
            self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height),
            self.game.character_spritesheet.get_sprite(35, 34, self.width, self.height),
            self.game.character_spritesheet.get_sprite(68, 34, self.width, self.height)
        ]
        self.up_animations = [
            self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height),
            self.game.character_spritesheet.get_sprite(35, 98, self.width, self.height),
            self.game.character_spritesheet.get_sprite(68, 98, self.width, self.height)
        ]
        self.right_animations = [
            self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height),
            self.game.character_spritesheet.get_sprite(35, 66, self.width, self.height),
            self.game.character_spritesheet.get_sprite(68, 66, self.width, self.height)
        ]
        self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    # Обновление
    def update(self):
        if not self.game.battling:
            self.movement()
            self.animate()
            self.stamina = min(self.stamina + 0.2, self.max_stamina)
            current_time = pygame.time.get_ticks()
            if current_time - self.last_attack_time > 2000:  # 2 seconds
                self.combo_counter = 0
        
        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')
        self.x_change = 0
        self.y_change = 0

    #опыт персонажа
    def gain_exp(self, amount):
        self.exp += amount
        exp_needed = self.level * 100
        if self.exp >= exp_needed:
            self.level_up()

    #LVL персонажа
    def level_up(self):
        self.level += 1
        self.exp = 0
        self.max_health += 20
        self.health = self.max_health
        self.max_stamina += 10
        self.stamina = self.max_stamina
        self.special_charges += 1

    # Движение
    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            for sprite in self.game.all_sprite:
                sprite.rect.x += PLAYER_SPEED
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_d]:
            for sprite in self.game.all_sprite:
                sprite.rect.x -= PLAYER_SPEED
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_w]:
            for sprite in self.game.all_sprite:
                sprite.rect.y += PLAYER_SPEED
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_s]:
            for sprite in self.game.all_sprite:
                sprite.rect.y -= PLAYER_SPEED
            self.y_change += PLAYER_SPEED
            self.facing = 'down'


    # Столкновения с блоками
    def collide_blocks(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    for sprite in self.game.all_sprite:
                        sprite.rect.x += PLAYER_SPEED
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                    for sprite in self.game.all_sprite:
                        sprite.rect.x -= PLAYER_SPEED

        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    for sprite in self.game.all_sprite:
                        sprite.rect.y += PLAYER_SPEED
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    for sprite in self.game.all_sprite:
                        sprite.rect.y -= PLAYER_SPEED

    # Анимация игрока
    def animate(self):
        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'up':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height)
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1



# Враги
class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y, enemy_type="normal"):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprite, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.enemy_type = enemy_type
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        # Различная статистика в зависимости от типа
        if enemy_type == "tank":
            self.level = random.randint(1, 3)
            self.health = 50 + self.level * 10
            self.max_health = 50 + self.level * 10
            self.stamina = 70
            self.max_stamina = 70
            self.exp_value = 15 * self.level
            self.defense = 5
            self.attack_power = 8 + self.level
            self.speed = 0.7
        elif enemy_type == "ranged":
            self.level = random.randint(1, 3)
            self.health = 30 + self.level * 5
            self.max_health = 30 + self.level * 5
            self.stamina = 40
            self.max_stamina = 40
            self.exp_value = 12 * self.level
            self.defense = 2
            self.attack_power = 12 + self.level
            self.speed = 1.2
        else:  # normal
            self.level = random.randint(1, 3)
            self.health = 30 + self.level * 7
            self.max_health = 30 + self.level * 7
            self.stamina = 50
            self.max_stamina = 50
            self.exp_value = 10 * self.level
            self.defense = 3
            self.attack_power = 10 + self.level
            self.speed = 1.0

        self.defending = False
        self.x_change = 0
        self.y_change = 0
        self.facing = random.choice(['left', 'right'])
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = random.randint(7, 30)
        self.attack_cooldown = 0
        self.special_ability_ready = True

        self.image = self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    # Обновление
    def update(self):
        if not self.game.battling:
            self.movement()
            self.animate()
            self.stamina = min(self.stamina + 0.1, self.max_stamina)
            if self.attack_cooldown > 0:
                self.attack_cooldown -= 1
        
        self.rect.x += self.x_change
        self.rect.y += self.y_change
        self.x_change = 0
        self.y_change = 0

    # Движение врагов
    def movement(self):
        if self.facing == 'left':
            self.x_change -= ENEMY_SPEED * self.speed
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = 'right'

        if self.facing == 'right':
            self.x_change += ENEMY_SPEED * self.speed
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = 'left'
    

    # Анимация врага
    def animate(self):
        self.left_animations = [
            self.game.enemy_spritesheet.get_sprite(3, 98, self.width, self.height),
            self.game.enemy_spritesheet.get_sprite(35, 98, self.width, self.height),
            self.game.enemy_spritesheet.get_sprite(68, 98, self.width, self.height)
        ]
        self.right_animations = [
            self.game.enemy_spritesheet.get_sprite(3, 66, self.width, self.height),
            self.game.enemy_spritesheet.get_sprite(35, 66, self.width, self.height),
            self.game.enemy_spritesheet.get_sprite(68, 66, self.width, self.height)
        ]

        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 66, self.width, self.height)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 98, self.width, self.height)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1


#Босс
class Boss(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BOSS_LAYER
        self.groups = self.game.all_sprite, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        # Уникальные характеристики босса
        self.enemy_type = "boss"
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE 
        self.height = TILESIZE 
        
        self.level = 5
        self.health = 100 + self.level * 20
        self.max_health = 200 + self.level * 20
        self.stamina = 100
        self.max_stamina = 100
        self.exp_value = 50 * self.level
        self.defense = 10
        self.attack_power = 20 + self.level
        self.speed = 0  
        
        self.defending = False
        self.x_change = 0
        self.y_change = 0
        self.facing = 'left'  
        self.attack_cooldown = 0
        self.special_ability_ready = True
        
        # Используем boss_spritesheet 
        self.image = self.game.boss_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.image.set_colorkey(BLACK) 
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        # Фазы боя
        self.phase = 1
        self.special_attacks = ["Огненный шторм", "Ледяная тюрьма", "Удар молнии"]
    
    def update(self):
        self.stamina = min(self.stamina + 0.1, self.max_stamina)
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        # Смены фаз при определенном здоровье
        if self.health < self.max_health * 0.5 and self.phase == 1:
            self.phase = 2
            self.attack_power += 5
            if hasattr(self.game, 'battle_message'):
                self.game.battle_message = "Босс входит в фазу ярости!"
        
        if self.health < self.max_health * 0.2 and self.phase == 2:
            self.phase = 3
            self.defense += 5
            if hasattr(self.game, 'battle_message'):
                self.game.battle_message = "Босс в отчаянии! Его защита увеличена!"

    def use_special_ability(self):
        if self.special_ability_ready:
            self.special_ability_ready = False
            attack = random.choice(self.special_attacks)
            
            if attack == "Огненный шторм":
                return "Босс вызывает Огненный шторм! Урон увеличен!"
            elif attack == "Ледяная тюрьма":
                return "Босс создает Ледяную тюрьму! Ваша скорость снижена!"
            else:
                return "Босс вызывает Удар молнии! Критический урон!"
        return ""
    

#Приспешник босса
class Minion(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprite, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        # Характеристики приспешника
        self.enemy_type = "minion"
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        
        self.level = 3  # Сильнее обычных врагов
        self.health = 60 + self.level * 8
        self.max_health = 60 + self.level * 8
        self.stamina = 60
        self.max_stamina = 60
        self.exp_value = 20 * self.level
        self.defense = 4
        self.attack_power = 12 + self.level
        self.speed = 0.8
        
        self.defending = False
        self.x_change = 0
        self.y_change = 0
        self.facing = random.choice(['left', 'right'])
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = random.randint(10, 40)  # Дальность патрулирования
        self.attack_cooldown = 0
        self.special_ability_ready = True
        
        # Спрайты приспешника 
        self.image = self.game.Minions_spritesheet.get_sprite(3, 3, self.width, self.height)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        # Анимации для движения влево/вправо
        self.left_animations = [
            self.game.Minions_spritesheet.get_sprite(3, 98, self.width, self.height),
            self.game.Minions_spritesheet.get_sprite(35, 98, self.width, self.height),
            self.game.Minions_spritesheet.get_sprite(68, 98, self.width, self.height)
        ]
        self.right_animations = [
            self.game.Minions_spritesheet.get_sprite(3, 66, self.width, self.height),
            self.game.Minions_spritesheet.get_sprite(35, 66, self.width, self.height),
            self.game.Minions_spritesheet.get_sprite(68, 66, self.width, self.height)
        ]

    def update(self):
        if not self.game.battling:
            self.movement()
            self.animate()
            self.stamina = min(self.stamina + 0.1, self.max_stamina)
            if self.attack_cooldown > 0:
                self.attack_cooldown -= 1
        
        self.rect.x += self.x_change
        self.rect.y += self.y_change
        self.x_change = 0
        self.y_change = 0

    def movement(self):
        if self.facing == 'left':
            self.x_change -= ENEMY_SPEED * self.speed
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = 'right'

        if self.facing == 'right':
            self.x_change += ENEMY_SPEED * self.speed
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = 'left'

    def animate(self):
        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.Minions_spritesheet.get_sprite(3, 66, self.width, self.height)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.Minions_spritesheet.get_sprite(3, 98, self.width, self.height)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

    def use_special_ability(self):
        if self.special_ability_ready:
            self.special_ability_ready = False
            return "Приспешник вызывает подкрепление!"
        return ""
# Стена
class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprite, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(390, 160, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

#Тропинка
class Trop(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprite
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(266, 47, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

#Куст
class Bush(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprite, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(450, 610, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

#Дерево
class Tree(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprite, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE_Texture
        self.height = TILESIZE_Texture

        self.image = self.game.terrain_spritesheet.get_sprite(382, 634, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


#Вода
class Water(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprite, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(608, 128, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

#Мост
class Most(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprite
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(166, 656, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

# трава
class Group(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprite
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(6, 37, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


# Кнопки входа в игру
class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font('PF Reminder Pro Medium.otf', fontsize)
        self.content = content

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fg = fg
        self.bg = bg

        # Создали прямоугольник
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()  # Хитбокс кнопки

        self.rect.x = self.x
        self.rect.y = self.y

        # Рендер шрифта
        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width / 2, self.height / 2))  # Центр текста
        self.image.blit(self.text, self.text_rect)

    # Нажатая клавиша :)
    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False


# Атака
class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x, y, element="normal", is_combo=False, is_special=False):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprite, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE
        self.element = element
        self.is_combo = is_combo
        self.is_special = is_special
        self.animation_loop = 0
        self.damage_multiplier = 1.0

        # Set damage multiplier based on element
        if self.element == "fire":
            self.damage_multiplier = 1.2
        elif self.element == "ice":
            self.damage_multiplier = 0.9  # Slows enemy
        elif self.element == "lightning":
            self.damage_multiplier = 1.5  # High damage but rare

        if self.is_combo:
            self.damage_multiplier *= 1.5
        if self.is_special:
            self.damage_multiplier *= 2.0

        self.image = self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


    def update(self):
        self.animate()
        self.collide()

    # Столкновение с врагами
    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            for hit in hits:
                base_damage = 10
                if self.is_combo:
                    base_damage += 5 * self.game.player.combo_counter
                if self.is_special:
                    base_damage += 15
                
                total_damage = int(base_damage * self.damage_multiplier)
                
                # Elemental effects
                if self.element == "fire":
                    total_damage = int(total_damage * 1.2)
                elif self.element == "ice" and random.random() < 0.3:
                    hit.speed *= 0.7  # Slow enemy
                elif self.element == "lightning" and random.random() < 0.1:
                    total_damage *= 2  # Critical hit chance
                
                hit.health -= total_damage
                
                if hit.health <= 0:
                    self.game.player.gain_exp(hit.exp_value)
                    hit.kill()

    def animate(self):
        direction = self.game.player.facing
        element_offset = 0
        if self.element == "fire":
            element_offset = 160
        elif self.element == "ice":
            element_offset = 192
        elif self.element == "lightning":
            element_offset = 224

        right_animations = [
            self.game.attack_spritesheet.get_sprite(0, 64 + element_offset, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(32, 64 + element_offset, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(64, 64 + element_offset, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(96, 64 + element_offset, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(128, 64 + element_offset, self.width, self.height)
        ]

        down_animations = [
            self.game.attack_spritesheet.get_sprite(0, 32 + element_offset, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(32, 32 + element_offset, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(64, 32 + element_offset, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(96, 32 + element_offset, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(128, 32 + element_offset, self.width, self.height)
        ]

        left_animations = [
            self.game.attack_spritesheet.get_sprite(0, 96 + element_offset, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(32, 96 + element_offset, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(64, 96 + element_offset, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(96, 96 + element_offset, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(128, 96 + element_offset, self.width, self.height)
        ]

        up_animations = [
            self.game.attack_spritesheet.get_sprite(0, 0 + element_offset, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(32, 0 + element_offset, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(64, 0 + element_offset, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(96, 0 + element_offset, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(128, 0 + element_offset, self.width, self.height)
        ]

        if direction == 'up':
            self.image = up_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        if direction == 'down':
            self.image = down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        if direction == 'left':
            self.image = left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        if direction == 'right':
            self.image = right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()
