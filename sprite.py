import pygame
from config import *
import math
import random


class Spritrsheet:
    def __init__(self,file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self,x,y,width,height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet,(0,0), (x,y, width,height))
        sprite.set_colorkey(BLACK)
        return sprite
    
#NPC
class NPC(pygame.sprite.Sprite):
    def __init__(self, game, x, y, dialogues):
        self.game = game
        self._layer = NPC_LAYER  # Предполагается, что у вас есть определенный слой для NPC
        self.groups = self.game.all_sprite
        pygame.sprite.Sprite.__init__(self, self.groups)

        # Параметры NPC
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        # Вид NPC
        self.image = self.game.npc_sprite_sheet.get_sprite(1, 1, self.width, self.height)
        
        # Зона порожения
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        # Диалоги
        self.dialogues = dialogues
        self.current_dialogue_index = 0
        self.dialogue_active = False

    # Обновление
    def update(self):
        if self.dialogue_active:
            self.handle_dialogue()

    def handle_dialogue(self):
        # Проверка нажатия клавиши для продолжения диалога
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:  # Например, пробел для продолжения диалога
            self.current_dialogue_index += 1
            if self.current_dialogue_index >= len(self.dialogues):
                self.dialogue_active = False
                self.current_dialogue_index = 0

    def draw_dialogue(self, surface):
        if self.dialogue_active:
            font = pygame.font.Font(None, 36)  # Шрифт для текста
            dialogue_text = self.dialogues[self.current_dialogue_index]
            text_surface = font.render(dialogue_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT - 50))
            surface.blit(text_surface, text_rect)

    def interact(self):
        # Начало диалога
        self.dialogue_active = True
        self.current_dialogue_index = 0




class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprite
        pygame.sprite.Sprite.__init__(self,self.groups)
        
        # Отрисовка всего по этапам  
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.animation_loop = 1
        self.down_animations = None
        self.up_animations = None
        self.left_animations = None
        self.right_animations = None
        
        #Вид игрока
        self.image = self.game.character_spriteheet.get_sprite(3,2, self.width, self.height)
        
        
        #Зона порожения
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    #Обновление
    def update(self):
        self.movement()
        self.animete()
        self.collide_enemy()

        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')

        self.x_change = 0
        self.y_change = 0

    # Движение
    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_d]:
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_w]:
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_s]:
            self.y_change += PLAYER_SPEED
            self.facing = 'down'

    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies ,False)
        if hits:
            self.kill()
            self.game.playing = False

    # Столкновения с блоками
    def collide_blocks(self, directory):
        if directory == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right

        if directory == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
        

    #Анимация игрока
    def animete(self):
        self.down_animations = [self.game.character_spriteheet.get_sprite(3, 2, self.width, self.height),
                           self.game.character_spriteheet.get_sprite(35, 2, self.width, self.height),
                           self.game.character_spriteheet.get_sprite(68, 2, self.width, self.height)]

        self.up_animations = [self.game.character_spriteheet.get_sprite(3, 34, self.width, self.height),
                         self.game.character_spriteheet.get_sprite(35, 34, self.width, self.height),
                         self.game.character_spriteheet.get_sprite(68, 34, self.width, self.height)]

        self.left_animations = [self.game.character_spriteheet.get_sprite(3, 98, self.width, self.height),
                           self.game.character_spriteheet.get_sprite(35, 98, self.width, self.height),
                           self.game.character_spriteheet.get_sprite(68, 98, self.width, self.height)]

        self.right_animations = [self.game.character_spriteheet.get_sprite(3, 66, self.width, self.height),
                            self.game.character_spriteheet.get_sprite(35, 66, self.width, self.height),
                            self.game.character_spriteheet.get_sprite(68, 66, self.width, self.height)]
        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.game.character_spriteheet.get_sprite(3, 2, self.width, self.height)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'up':
            if self.y_change == 0:
                self.image = self.game.character_spriteheet.get_sprite(3, 34, self.width, self.height)
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.character_spriteheet.get_sprite(3, 66, self.width, self.height)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.character_spriteheet.get_sprite(3, 98, self.width, self.height)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

#Враги
class enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ENAMY_LAYER 
        self.groups = self.game.all_sprite, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.hieght = TILESIZE
        self.width = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['left','right'])
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = random.randint(7,30)

        self.image = self.game.enemy_spriteheet.get_sprite(3, 2, self.width, self.hieght)
        #self.image.set_colorkey = (BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y 

    #обновление 
    def update(self):

        self.movement()
        self.animate()
        

        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0

    #Движение врагов
    def movement(self):
        if self.facing == 'left':
            self.x_change -= ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = 'right'
        
        if self.facing == 'right':
            self.x_change += ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = 'left'
    
    #Анимация врага
    def animate(self):

        self.left_animations = [self.game.enemy_spriteheet.get_sprite(3, 98, self.width, self.hieght),
                           self.game.enemy_spriteheet.get_sprite(35, 98, self.width, self.hieght),
                           self.game.enemy_spriteheet.get_sprite(68, 98, self.width, self.hieght)]

        self.right_animations = [self.game.enemy_spriteheet.get_sprite(3, 66, self.width, self.hieght),
                            self.game.enemy_spriteheet.get_sprite(35, 66, self.width, self.hieght),
                            self.game.enemy_spriteheet.get_sprite(68, 66, self.width, self.hieght)]

        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.enemy_spriteheet.get_sprite(3, 66, self.width, self.hieght)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.enemy_spriteheet.get_sprite(3, 98, self.width, self.hieght)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1


#Стена
class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprite, self.game.blocks
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrian_spritehett.get_sprite(960, 448, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Group(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.__yaler = GROUD_LAYER
        self.groups = self.game.all_sprite
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrian_spritehett.get_sprite(64,352,self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

#Кнопки входа в игру
class Button:
    def __init__(self,x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font('HandWriting_1.otf', fontsize)
        self.content = content

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fg = fg
        self.bg = bg

        #создали прямоугольник 
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect() #хитбокс кнопки 

        self.rect.x = self.x
        self.rect.y = self.y

        #рендер шрифта
        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center = (self.width/2, self.height/2)) #центр текста
        self.image.blit(self.text, self.text_rect)

    #Нажатая клавиша :)
    def is_pressed(self,pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False
    
#Класс Атаки
class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x ,y, ):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprite, self.game.attacks
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.x = x 
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE

        self.animation_loop = 0

        self.image = self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.animate()
        self.collide()

    #Столкновение с врагами
    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, True)

    def animate(self):
        direction = self.game.player.facing

        right_animations = [self.game.attack_spritesheet.get_sprite(0, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 64, self.width, self.height)]

        down_animations = [self.game.attack_spritesheet.get_sprite(0, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 32, self.width, self.height)]

        left_animations = [self.game.attack_spritesheet.get_sprite(0, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 96, self.width, self.height)]

        up_animations = [self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(32, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(64, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(96, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(128, 0, self.width, self.height)]
        
        if direction =='up':
            self.image = up_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        if direction =='down':
            self.image = down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        if direction =='left':
            self.image = left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        if direction =='right':
            self.image = right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()


