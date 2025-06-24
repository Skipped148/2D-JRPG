import pygame
from sprite import *
from config import *
import sys
import time
import random  
from sprite import Boss
from credits import Credits

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption("My Awesome Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('PF Reminder Pro Medium.otf', 20)  
        self.running = True
        self.character_spritesheet = Spritesheet("character.png")
        self.terrain_spritesheet = Spritesheet("terrian1.png")
        self.boss_spritesheet = Spritesheet("Boss.png")
        self.Minions_spritesheet = Spritesheet ("Minions.png")
        self.enemy_spritesheet = Spritesheet("enemy.png")
        self.intro_background = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
        self.intro_background.fill((0, 0, 0))
        self.go_background = pygame.image.load("gameover.png")
        
        # Игрок Статистика
        self.player_exp = 0
        self.player_level = 1
        self.battle_options = ["Атака", "Сильная атака", "Защита", "Уклонение", "Спец.прием"]
        self.battle_cooldowns = {"Сильная атака": 0, "Спец.прием": 0}
        self.battle_message = ""
        self.title_text_surface = None
        self.description_text_surface = None
        self.battling = False
        self.current_enemy = None

    def createTilemap(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Group(self, j, i)
                if column == "B":
                    Block(self, j, i)
                if column == "W":
                    Water(self,j, i)
                if column == "M":
                    Most(self,j, i)
                if column == "T":
                    Trop(self,j, i)
                if column == "L":
                    Bush(self,j, i)
                if column == "G":
                    Tree(self,j, i)
                if column == "E":
                    Enemy(self, j, i, "normal")
                elif column == "R":
                    Enemy(self, j, i, "ranged")
                elif column == "K":
                    Enemy(self, j, i, "tank")
                if column == "X":  
                    Boss(self, j, i)
                if column == "Y":
                    Minion(self, j, i)
                if column == "P":
                    self.player = Player(self, j, i)

    def new(self):
        self.playing = True
        self.all_sprite = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.battling = False
        self.createTilemap()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            
            if self.battling:
                self.battle_events(event)
            
    def update(self):
        # 
        for key in list(self.battle_cooldowns.keys()):
            if self.battle_cooldowns[key] > 0:
                self.battle_cooldowns[key] -= 1
        
        self.all_sprite.update()
        if not self.battling:
            self.check_enemy_collisions()

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprite.draw(self.screen)
        
        #отображение ХП игрока
        health_text = self.font.render(f"HP: {self.player.health}/{self.player.max_health}", True, WHITE)
        self.screen.blit(health_text, (10, 10))
        
        if self.battling:
            self.draw_battle()
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        while self.playing and self.running:
            self.events()
            self.update()
            self.draw()

    def check_enemy_collisions(self):
        hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        if hits:
            self.start_battle(hits[0])

    def boss_intro_screen(self):
        intro = True
        title_text = """Тьма сгущается... 
    В воздухе витает запах серы и крови. 
    Из глубин подземелья поднимается Архидемон Азгхор!"""
        description_text = "Его глаза пылают ненавистью ко всему живому..."
        button_text = 'Принять бой'
        title_x = WIN_WIDTH // 2 - 300
        title_y = WIN_HEIGHT // 4
        desc_x = WIN_WIDTH // 2 - 350
        desc_y = WIN_HEIGHT // 2
        button_x = WIN_WIDTH // 2 - 60
        button_y = WIN_HEIGHT * 3 // 4

        play_button = Button(button_x, button_y, 120, 50, WHITE, BLACK, button_text, 15)
        self.screen.blit(self.intro_background, (0, 0))
        self.type_text(self.screen, title_text, (title_x, title_y), (255, 0, 0), self.font)
        self.type_text(self.screen, description_text, (desc_x, desc_y), WHITE, self.font)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    mouse_pressed = pygame.mouse.get_pressed()
                    if play_button.is_pressed(mouse_pos, mouse_pressed):
                        intro = False

            self.screen.blit(play_button.image, play_button.rect)
            pygame.display.flip()
            self.clock.tick(FPS)

    def start_battle(self, enemy): 
        self.battling = True
        self.current_enemy = enemy
        
        # Проверяем, является ли враг боссом (используйте hasattr для безопасности)
        if hasattr(enemy, 'enemy_type') and enemy.enemy_type == "boss":
            self.boss_intro_screen()
        
        self.battle_message = "Бой начался!"
        self.player_max_stamina = 100 + (self.player_level * 10)
        self.player_stamina = self.player_max_stamina
        self.enemy_max_stamina = 50
        self.current_enemy.stamina = self.enemy_max_stamina

    def game_over(self):
        restart_button = Button(WIN_WIDTH // 2 - 60, WIN_HEIGHT - 100, 120, 50, WHITE, BLACK, 'Restart', 32)

        for sprite in self.all_sprite:
            sprite.kill()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    mouse_pressed = pygame.mouse.get_pressed()
                    if restart_button.is_pressed(mouse_pos, mouse_pressed):
                        self.new()
                        self.main()
                        return

            #фулл экран ПНГ
            self.screen.blit(pygame.transform.scale(self.go_background, (WIN_WIDTH, WIN_HEIGHT)), (0, 0))
            self.screen.blit(restart_button.image, restart_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def render_text(self, text, color, font):
        return font.render(text, True, color)

    def type_text(self, surface, text, pos, color, font, delay=0.05):
        x, y = pos
        for line in text.splitlines():
            current_line = ""
            for i, char in enumerate(line):
                current_line += char
                line_surface = self.render_text(current_line, color, font)
                line_rect = line_surface.get_rect(topleft=(x, y))
                surface.blit(line_surface, line_rect)
                pygame.display.update(line_rect)
                time.sleep(delay)
            y += self.font.get_linesize()

    def intro_screen(self):
        intro = True
        title_text = """Тьма сгущается, будто в старой мельнице… 
Шепчутся ветры, предвещая кровавый пир 
Готовь свой меч, путник. Впереди – лишь склеп да кладбище..."""
        description_text = "Панк не сдох! Просто ждет, пока загрузится игра… "
        button_text = 'Начать игру'
        title_x = WIN_WIDTH // 2 - 300
        title_y = WIN_HEIGHT // 4
        desc_x = WIN_WIDTH // 2 - 350
        desc_y = WIN_HEIGHT // 2
        button_x = WIN_WIDTH // 2 - 60
        button_y = WIN_HEIGHT * 3 // 4

        play_button = Button(button_x, button_y, 120, 50, WHITE, BLACK, button_text, 15)
        self.screen.blit(self.intro_background, (0, 0))
        self.type_text(self.screen, title_text, (title_x, title_y), WHITE, self.font)
        self.type_text(self.screen, description_text, (desc_x, desc_y), WHITE, self.font)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    mouse_pressed = pygame.mouse.get_pressed()
                    if play_button.is_pressed(mouse_pos, mouse_pressed):
                        intro = False

            self.screen.blit(play_button.image, play_button.rect)
            pygame.display.flip()
            self.clock.tick(FPS)

    def draw_battle(self):
        # Bотрисовка окна
        BATTLE_WINDOW_WIDTH = WIN_WIDTH // 2
        BATTLE_WINDOW_HEIGHT = WIN_HEIGHT // 2
        battle_surface = pygame.Surface((BATTLE_WINDOW_WIDTH, BATTLE_WINDOW_HEIGHT))
        battle_surface.fill((50, 50, 50))
        self.screen.blit(battle_surface, (WIN_WIDTH // 2 - BATTLE_WINDOW_WIDTH // 2, 
                                        WIN_HEIGHT // 2 - BATTLE_WINDOW_HEIGHT // 2))

        # иконки в бою
        icon_size = 64
        text_x = WIN_WIDTH // 2 - BATTLE_WINDOW_WIDTH // 2 + 50
        text_y = WIN_HEIGHT // 2 - BATTLE_WINDOW_HEIGHT // 2 + 50

        player_icon = self.character_spritesheet.get_sprite(3, 2, icon_size, icon_size)
        self.screen.blit(player_icon, (text_x - icon_size - 20, text_y))

        enemy_icon = self.enemy_spritesheet.get_sprite(3, 2, icon_size, icon_size)
        self.screen.blit(enemy_icon, (text_x + BATTLE_WINDOW_WIDTH - icon_size - 20, text_y))

        # Отображение текущего элемента
        element_colors = {
            "normal": WHITE,
            "fire": (255, 100, 0),
            "ice": (0, 200, 255),
            "lightning": (255, 255, 0)
        }
        element_text = self.font.render(f"Элемент: {self.player.element}", True, element_colors.get(self.player.element, WHITE))
        self.screen.blit(element_text, (10, 100))

        # Сообщения в бою
        if hasattr(self, 'battle_message'):
            attack_text = self.font.render(self.battle_message, True, WHITE)
            text_rect = attack_text.get_rect(center=(WIN_WIDTH // 2, text_y + icon_size // 2))
            self.screen.blit(attack_text, text_rect)

        # Варианты боя с перезарядкой
        options = self.battle_options.copy()
        for i, option in enumerate(options):
            if self.battle_cooldowns.get(option, 0) > 0:
                options[i] = f"{option} (⏳{self.battle_cooldowns[option]})"
        
        # Кнопки в бою
        button_rects = []
        for i, (option, rect) in enumerate(zip(options, [
            pygame.Rect(WIN_WIDTH//2 - 200, WIN_HEIGHT//2 + 100, 150, 50),
            pygame.Rect(WIN_WIDTH//2 - 40, WIN_HEIGHT//2 + 100, 150, 50),
            pygame.Rect(WIN_WIDTH//2 + 120, WIN_HEIGHT//2 + 100, 150, 50),
            pygame.Rect(WIN_WIDTH//2 - 200, WIN_HEIGHT//2 + 160, 150, 50),
            pygame.Rect(WIN_WIDTH//2 - 40, WIN_HEIGHT//2 + 160, 150, 50)
        ])):
            color = (100, 100, 100) if "⏳" in option else (70, 70, 120)
            pygame.draw.rect(self.screen, color, rect)
            option_text = self.font.render(option.split(" (")[0], True, WHITE)
            self.screen.blit(option_text, (rect.centerx - option_text.get_width()//2, 
                                        rect.centery - option_text.get_height()//2))
            setattr(self, f"battle_option_{i}_rect", rect)
            button_rects.append(rect)

        # Player стата
        stamina_text = self.font.render(f"Стамина: {self.player_stamina}/{self.player_max_stamina}", True, WHITE)
        level_text = self.font.render(f"Ур. {self.player_level} (Опыт: {self.player_exp}/{self.player_level*100})", True, WHITE)
        enemy_health = self.font.render(f"Враг: HP {self.current_enemy.health}/{self.current_enemy.max_health}", True, WHITE)
        
        #  отображение типа врага
        enemy_type_text = ""
        if self.current_enemy.enemy_type == "tank":
            enemy_type_text = "Танк"
        elif self.current_enemy.enemy_type == "ranged":
            enemy_type_text = "Дальнобойный"
        else:
            enemy_type_text = "Обычный"
        enemy_type_render = self.font.render(f"Тип: {enemy_type_text}", True, WHITE)
        
        self.screen.blit(stamina_text, (10, 40))
        self.screen.blit(level_text, (10, 70))
        self.screen.blit(enemy_health, (WIN_WIDTH - 200, 40))
        self.screen.blit(enemy_type_render, (WIN_WIDTH - 200, 70))


    def battle_events(self, event):
        # Обработка выбора элементов
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            self.player.element = "normal"
            self.battle_message = "Выбран обычный элемент"
        elif keys[pygame.K_2] and self.player.level >= 2:
            self.player.element = "fire"
            self.battle_message = "Выбран огненный элемент"
        elif keys[pygame.K_3] and self.player.level >= 3:
            self.player.element = "ice"
            self.battle_message = "Выбран ледяной элемент"
        elif keys[pygame.K_4] and self.player.level >= 5:
            self.player.element = "lightning"
            self.battle_message = "Выбран элемент молнии"

        # Обработка действий в бою
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            for i in range(5):
                if hasattr(self, f"battle_option_{i}_rect") and getattr(self, f"battle_option_{i}_rect").collidepoint(pos):
                    option = self.battle_options[i]
                    if self.battle_cooldowns.get(option, 0) <= 0:
                        if option == "Атака":
                            self.battle_attack()
                        elif option == "Сильная атака":
                            self.battle_strong_attack()
                        elif option == "Защита":
                            self.battle_defend()
                        elif option == "Уклонение":
                            self.battle_dodge()
                        elif option == "Спец.прием":
                            self.battle_special()
                    break

    def battle_attack(self):
        self.player_stamina = min(self.player_stamina + 10, self.player_max_stamina)
        player_damage = random.randint(5, 10) + self.player_level
        self.execute_attack(player_damage, 0, "атакует")

    def battle_strong_attack(self):
        if self.player_stamina >= 30:
            self.player_stamina -= 30
            player_damage = random.randint(15, 25) + self.player_level * 2
            self.battle_cooldowns["Сильная атака"] = 2
            self.execute_attack(player_damage, 10, "мощно атакует")
        else:
            self.battle_message = "Недостаточно стамины для сильной атаки!"

    def battle_defend(self):
        self.player_stamina = min(self.player_stamina + 20, self.player_max_stamina)
        self.battle_message = "Вы готовитесь к защите!"
        self.player.defending = True

    def battle_dodge(self):
        if random.random() < 0.5:  # 50% chance to dodge
            self.battle_message = "Игрок уклонился!"
            self.end_battle(False)
        else:
            self.battle_message = "Уклонение не удалось!"
            enemy_damage = random.randint(5, 10) + self.current_enemy.level
            if hasattr(self.player, 'defending') and self.player.defending:
                enemy_damage = max(1, enemy_damage // 2)
            self.player.health -= enemy_damage
            self.battle_message += f"\nВраг наносит {enemy_damage} урона!"
            if self.player.health <= 0:
                self.battle_message = "Игрок повержен!"
                self.end_battle(False)
        self.player.defending = False

    def battle_special(self):
        if self.player_stamina >= 50 and self.battle_cooldowns["Спец.прием"] <= 0:
            self.player_stamina -= 50
            player_damage = random.randint(25, 40) + self.player_level * 3
            self.battle_cooldowns["Спец.прием"] = 4
            self.execute_attack(player_damage, 0, "использует спец.прием!", True)
        else:
            self.battle_message = "Недостаточно стамины или прием на перезарядке!"

    def execute_attack(self, player_damage, enemy_bonus, action, is_special=False):
        # Элементальные эффекты
        element_effect = ""
        if self.player.element == "fire" and random.random() < 0.3:
            player_damage = int(player_damage * 1.5)
            element_effect = " (Огненный удар!)"
        elif self.player.element == "ice":
            self.current_enemy.speed *= 0.8
            element_effect = " (Замедление!)"
        elif self.player.element == "lightning" and random.random() < 0.1:
            player_damage *= 3
            element_effect = " (Разряд молнии!)"

        # шанс крита
        is_critical = random.random() < 0.1
        if is_critical:
            player_damage *= 2
            crit_text = " КРИТИЧЕСКИЙ УДАР!"
        else:
            crit_text = ""
        
        # сообщение об уроне
        self.current_enemy.health -= player_damage
        self.battle_message = f"Игрок {action} и наносит {player_damage} урона!{element_effect}{crit_text}"
        
        # Check if enemy is defeated
        if self.current_enemy.health <= 0:
            exp_gain = 30 + self.current_enemy.level * 10
            self.player_exp += exp_gain
            self.check_level_up()
            self.battle_message = f"Враг повержен! Получено {exp_gain} опыта!"
            self.end_battle(True)
            return
        
        # Enemy counterattack
        if random.random() < 0.8:  # 80% chance to counterattack
            enemy_damage = random.randint(3, 8) + enemy_bonus + self.current_enemy.level
            if hasattr(self.player, 'defending') and self.player.defending:
                enemy_damage = max(1, enemy_damage // 2)
            
            self.player.health -= enemy_damage
            self.battle_message += f"\nВраг контратакует и наносит {enemy_damage} урона!"
            
            if self.player.health <= 0:
                self.battle_message = "Игрок повержен!"
                self.end_battle(False)
        else:
            self.battle_message += "\nВраг промахивается!"
        
        # Reset defense after attack
        self.player.defending = False
        
        # Special effects
        if is_special:
            self.show_special_effect()

    def show_special_effect(self):
        # Placeholder for special effects animation
        pass

    def check_level_up(self):
        exp_needed = self.player_level * 100
        if self.player_exp >= exp_needed:
            self.player_level += 1
            self.player_exp -= exp_needed
            self.player.max_health += 20
            self.player.health = self.player.max_health
            self.battle_message += f"\nУровень повышен! Теперь вы {self.player_level} уровня!"

    def battle_flee(self):
        FLEE_PENALTY = 0.3
        damage = int(self.player.max_health * FLEE_PENALTY)
        
        if random.random() < 0.5:
            self.player.health -= damage
            self.battle_message = f"Игрок успешно сбежал, но получил {damage} урона!"
            self.battling = False
        else:
            self.player.health -= damage
            self.battle_message = f"Игрок не смог сбежать и получил {damage} урона!"

        if self.player.health <= 0:
            self.battle_message = "Игрок погиб, пытаясь сбежать!"
            self.end_battle(False)

    def end_battle(self, victory):
        self.battling = False
        self.player.defending = False
        
        if victory and self.battle_message != "Игрок уклонился!":
            # Проверяем, был ли это босс
            if hasattr(self.current_enemy, 'enemy_type') and self.current_enemy.enemy_type == "boss":
                self.current_enemy.kill()
                # Показываем титры и завершаем игру
                credits = Credits(self)
                credits.show()
                self.running = False
                return
            else:
                self.current_enemy.kill()
        
        if self.player.health <= 0:
            self.game_over()

# Initialize and run the game
g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    if not g.running:
        g.game_over()

pygame.quit()
sys.exit()