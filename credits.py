import pygame
from config import *

class Credits:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.clock = game.clock
        self.font_large = pygame.font.Font('PF Reminder Pro Medium.otf', 32)
        self.font_small = pygame.font.Font('PF Reminder Pro Medium.otf', 20)
        self.running = True
        self.background = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
        self.background.fill((0, 0, 0))
        
        # Титры
        self.credits = [
            "Конец",
            "",
            "Игра разработана",
            "для Курсового проекта по МДК 02.01",
            "",
            "Авторы:",
            "Иванов Денис ИСП9-322Б",
            "",
            "Спасибо за игру!",
            "",
            "© 2025 ИСП9-322Б Черно-Белое"
        ]
        
        # Позиции для титров (будет анимироваться)
        self.credit_positions = []
        for i, line in enumerate(self.credits):
            self.credit_positions.append(WIN_HEIGHT + i * 50)
            
    def show(self):
        self.running = True
        scroll_speed = 1
        end_position = -len(self.credits) * 50
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.game.running = False
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    self.running = False
            
            # Прокрутка титров
            for i in range(len(self.credit_positions)):
                self.credit_positions[i] -= scroll_speed
                
            # Проверка завершения титров
            if self.credit_positions[-1] < end_position:
                self.running = False
                self.game.running = False
            
            # Отрисовка
            self.screen.blit(self.background, (0, 0))
            
            for i, (line, y_pos) in enumerate(zip(self.credits, self.credit_positions)):
                if i == 0:  # Первая строка (заголовок)
                    text = self.font_large.render(line, True, (255, 215, 0))  # Золотой цвет
                    text_rect = text.get_rect(center=(WIN_WIDTH//2, y_pos))
                else:
                    text = self.font_small.render(line, True, WHITE)
                    text_rect = text.get_rect(center=(WIN_WIDTH//2, y_pos))
                
                if 0 <= y_pos <= WIN_HEIGHT:  # Рисуем только видимые строки
                    self.screen.blit(text, text_rect)
            
            pygame.display.flip()
            self.clock.tick(FPS)
