import pygame
from sprite import *
from config import *
import sys 


# сама игра
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('HandWriting_1.otf', 32)
        self.running = True

        self.character_spriteheet = Spritrsheet("character.png")
        self.terrian_spritehett = Spritrsheet("terrain.png")
        self.enemy_spriteheet = Spritrsheet("enemy.png")
        self.attack_spritesheet = Spritrsheet("attack.png")
        self.intro_background = pygame.image.load("introbackground.png")
        self.go_background = pygame.image.load("gameover.png")
        self.npc_sprite_sheet = Spritrsheet("skeleton.png")

        


    #Создание карты тайлов(КлетОЧКА)
    def createTilemap(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Group(self, j, i)
                if column == "B":
                    Block(self,j,i)
                if column =="E":
                    enemy(self,j,i)
                if column == "P":
                    self.player = Player(self,j,i)
                if column == "N":
                    self.NPC = NPC(self,j,i,dialogues = ["Привет, как дела?", "Что ты здесь делаешь?", "Удачи в твоих приключениях!"])
               

    # Запуск игры 
    def new(self):
        self.playing = True

        self.all_sprite = pygame.sprite.LayeredUpdates() #Все спрайты 
        self.blocks = pygame.sprite.LayeredUpdates() #Стены
        self.enemies = pygame.sprite.LayeredUpdates() # Враги
        self.attacks = pygame.sprite.LayeredUpdates() # Атаки 

        self.createTilemap()
        

    #События 
    def events(self):
        if self.player.rect.colliderect(self.NPC.rect):  # Проверка на столкновение с игроком
            self.NPC.interact()  # Начать диалог
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing == False
                self.running == False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Проверяем, какая кнопка мыши была нажата
                if event.button == 1:  # Левый клик мыши
                    if self.player.facing == 'up':
                        Attack(self, self.player.rect.x, self.player.rect.y - TILESIZE)
                    if self.player.facing == 'down':
                        Attack(self, self.player.rect.x, self.player.rect.y + TILESIZE)
                    if self.player.facing == 'left':
                        Attack(self, self.player.rect.x - TILESIZE, self.player.rect.y)
                    if self.player.facing == 'right':
                        Attack(self, self.player.rect.x + TILESIZE, self.player.rect.y)

    #Обновление игрового цикла
    def update(self):
        self.all_sprite.update()


    #Отрисовка экрана
    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprite.draw(self.screen)
        self.clock.tick(FPS)
        self.NPC.draw_dialogue(self.screen)
        pygame.display.update()
        

    # Основной метод пока играем
    def main(self):

        #игровой цикл
        while self.playing:
            self.events()
            self.update()
            self.draw()
            # В основном игровом цикле
           


        
    

    #конец?
    def game_over(self):
        text = self.font.render("Game Over", True, WHITE)
        text_rect = text.get_rect(center = (WIN_HEIGHT/2 , WIN_WIDTH/2))

        restart_button = Button(10, WIN_HEIGHT -60, 120, 50, WHITE, BLACK,'Restart', 32)

        #убрать все спрайты
        for sprite in self.all_sprite:
            sprite.kill()

        #Цикл событий
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running == False
            
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.new()
                self.main()
            self.screen.blit(self.go_background,(0,0))
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_button.image, restart_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def intro_screen(self):
        intro = True

        title = self.font.render('WTF THIS GAME', True, BLACK)
        title_rect = title.get_rect(x=10, y=10)

        play_button = Button(10, 50, 100, 50, WHITE, BLACK, 'Play', 32)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            #Проверка нажата ли кнопка
            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False

            self.screen.blit(self.intro_background, (0,0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()





g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()
pygame.quit()
sys.exit()