import pygame
import sys
import subprocess
from db_handlers import db_login, db_registration

# Инициализация pygame
pygame.init()

# Цвета
WHITE = (255, 255, 255)
LIGHT_GRAY = (236, 240, 241)
DARK_BLUE = (44, 62, 80)
MEDIUM_BLUE = (52, 73, 94)
LIGHT_BLUE = (234, 242, 248)
PRIMARY_BLUE = (41, 128, 185)
HOVER_BLUE = (52, 152, 219)
GRAY = (189, 195, 199)
LIGHT_GRAY_TEXT = (189, 195, 199)

# Размеры окна
WIDTH, HEIGHT = 500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Приключения путника")

# Шрифты
font_small = pygame.font.SysFont("Arial", 14)
font_medium = pygame.font.SysFont("Arial", 16, bold=True)
font_large = pygame.font.SysFont("Arial", 24, bold=True)

class Button:
    #Класс для создания кнопок
    def __init__(self, x, y, width, height, text, color, hover_color, text_color=WHITE, border_radius=5):
        self.rect = pygame.Rect(x, y, width, height)  # Область кнопки
        self.text = text              # Текст кнопки
        self.color = color            # Основной цвет
        self.hover_color = hover_color  # Цвет при наведении
        self.text_color = text_color  # Цвет текста
        self.border_radius = border_radius  # Закругление углов
        self.is_hovered = False       # Наведена ли мышь
        
    def draw(self, surface):
        #Отрисовка кнопки
        # Выбор цвета в зависимости от наведения
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=self.border_radius)
        
        # Отрисовка текста
        text_surface = font_medium.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
    def check_hover(self, pos):
        #оверка наведения мыши
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered
        
    def is_clicked(self, pos, event):
        #Проверка клика по кнопке
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

class InputBox:
    #ласс для полей ввода
    def __init__(self, x, y, width, height, placeholder="", is_password=False):
        self.rect = pygame.Rect(x, y, width, height)  # Область поля
        self.color = GRAY             # Цвет рамки
        self.active_color = PRIMARY_BLUE  # Цвет при активации
        self.text = ""                # Введенный текст
        self.placeholder = placeholder  # Подсказка
        self.is_active = False        # Активно ли поле
        self.is_password = is_password  # Поле для пароля?
        self.font = font_small        # Шрифт
        
    def handle_event(self, event):
        #Обработка событий
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Активация/деактивация поля
            self.is_active = self.rect.collidepoint(event.pos)
            self.color = self.active_color if self.is_active else GRAY
            
        if event.type == pygame.KEYDOWN and self.is_active:
            # Обработка ввода текста
            if event.key == pygame.K_RETURN:
                return True
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]  # Удаление символа
            else:
                self.text += event.unicode  # Добавление символа
        return False
        
    def draw(self, surface):
        #Отрисовка поля ввода
        pygame.draw.rect(surface, self.color, self.rect, 2, border_radius=5)
        
        # Отображение текста или подсказки
        if self.text or self.is_active:
            # Для пароля показываем звездочки
            display_text = "*" * len(self.text) if self.is_password else self.text
            text_surface = self.font.render(display_text, True, DARK_BLUE)
        else:
            text_surface = self.font.render(self.placeholder, True, LIGHT_GRAY_TEXT)
            
        # Позиционирование текста
        text_rect = text_surface.get_rect(
            x=self.rect.x + 10,
            centery=self.rect.centery
        )
        surface.blit(text_surface, text_rect)

class AuthWindow:
   #Окно авторизации
    def __init__(self):
        self.inputs = []    # Список полей ввода
        self.buttons = []   # Список кнопок
        self.labels = []    # Список текстовых меток
        self.setup_ui()     # Настройка интерфейса
        
    def setup_ui(self):
        #Создание элементов интерфейса
        # Заголовок
        title_label = {
            "text": "Авторизация",
            "font": font_large,
            "color": DARK_BLUE,
            "pos": (WIDTH // 2, 100),
            "center": True
        }
        self.labels.append(title_label)
        
        # Поле логина
        login_label = {
            "text": "Логин:",
            "font": font_small,
            "color": MEDIUM_BLUE,
            "pos": (50, 170),
            "center": False
        }
        self.labels.append(login_label)
        self.login_input = InputBox(50, 190, WIDTH - 100, 40, "Введите логин")
        self.inputs.append(self.login_input)
        
        # Поле пароля
        password_label = {
            "text": "Пароль:",
            "font": font_small,
            "color": MEDIUM_BLUE,
            "pos": (50, 250),
            "center": False
        }
        self.labels.append(password_label)
        self.password_input = InputBox(50, 270, WIDTH - 100, 40, "Введите пароль", is_password=True)
        self.inputs.append(self.password_input)
        
        # Кнопка входа
        self.login_btn = Button(
            WIDTH // 2 - 120 // 2, 350, 120, 40, 
            "Войти", PRIMARY_BLUE, HOVER_BLUE
        )
        self.buttons.append(self.login_btn)
        
        # Кнопка регистрации
        self.register_btn = Button(
            WIDTH // 2 - 120 // 2, 410, 120, 40, 
            "Регистрация", WHITE, LIGHT_BLUE, PRIMARY_BLUE
        )
        self.buttons.append(self.register_btn)
        
    def draw(self, surface):
        #Отрисовка окна
        surface.fill(LIGHT_GRAY)  # Фон
        
        # Отрисовка текстовых меток
        for label in self.labels:
            text_surface = label["font"].render(label["text"], True, label["color"])
            if label["center"]:
                text_rect = text_surface.get_rect(center=label["pos"])
            else:
                text_rect = text_surface.get_rect(topleft=label["pos"])
            surface.blit(text_surface, text_rect)
        
        # Отрисовка полей ввода
        for input_box in self.inputs:
            input_box.draw(surface)
            
        # Отрисовка кнопок
        for button in self.buttons:
            button.draw(surface)
            
    def handle_events(self, events):
        #Обработка событий
        mouse_pos = pygame.mouse.get_pos()
        
        for event in events:
            # Обработка полей ввода
            for input_box in self.inputs:
                input_box.handle_event(event)
                
            # Обработка кнопок
            for button in self.buttons:
                button.check_hover(mouse_pos)
                
                if button.is_clicked(mouse_pos, event):
                    if button == self.login_btn:
                        self.handle_login()
                    elif button == self.register_btn:
                        return "register"  # Переход на регистрацию
        return None
        
    def handle_login(self):
        #Проверка логина и пароля
        login = self.login_input.text
        password = self.password_input.text
        
        if not login or not password:
            self.show_message("Ошибка", "Заполните все поля!")
            return
            
        if db_login(login, password):
            self.launch_game()  # Запуск игры
        else:
            self.show_message("Ошибка", "Неверный логин или пароль!")
    
    def launch_game(self):
        #Запуск игры
        try:
            subprocess.run(["python", "main.py"], check=True)
            pygame.quit()
            sys.exit()
        except subprocess.CalledProcessError as e:
            self.show_message("Ошибка", f"Ошибка при запуске игры: {e}")
        except FileNotFoundError:
            self.show_message("Ошибка", "Файл main.py не найден!")
    
    def show_message(self, title, message):
        #Показ сообщения
        # Создание поверхности для сообщения
        message_box = pygame.Surface((400, 200))
        message_box.fill(WHITE)
        pygame.draw.rect(message_box, GRAY, (0, 0, 400, 200), 2)
        
        # Заголовок
        title_surface = font_medium.render(title, True, DARK_BLUE)
        message_box.blit(title_surface, (20, 20))
        
        # Разбивка текста на строки
        words = message.split(' ')
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + word + " "
            if font_small.size(test_line)[0] < 360:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        
        if current_line:
            lines.append(current_line)
        
        # Отрисовка строк
        for i, line in enumerate(lines):
            line_surface = font_small.render(line, True, MEDIUM_BLUE)
            message_box.blit(line_surface, (20, 60 + i * 30))
        
        # Кнопка OK
        ok_btn = Button(150, 150, 100, 30, "OK", PRIMARY_BLUE, HOVER_BLUE)
        
        # Позиционирование сообщения по центру
        message_rect = message_box.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        
        # Цикл показа сообщения
        waiting = True
        while waiting:
            mouse_pos = pygame.mouse.get_pos()
            adjusted_mouse_pos = (mouse_pos[0] - message_rect.x, mouse_pos[1] - message_rect.y)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if ok_btn.is_clicked(adjusted_mouse_pos, event):
                    waiting = False
            
            ok_btn.check_hover(adjusted_mouse_pos)
            
            # Отрисовка
            screen.fill((0, 0, 0, 128))  # Полупрозрачный фон
            screen.blit(message_box, message_rect)
            ok_btn.draw(message_box)
            pygame.display.flip()

class RegisterWindow:
    #Окно регистрации
    def __init__(self):
        self.inputs = []
        self.buttons = []
        self.labels = []
        self.setup_ui()
        
    def setup_ui(self):
        #Настройка интерфейса
        # Заголовок
        title_label = {
            "text": "Регистрация",
            "font": font_large,
            "color": DARK_BLUE,
            "pos": (WIDTH // 2, 70),
            "center": True
        }
        self.labels.append(title_label)
        
        # Поле никнейма
        nickname_label = {
            "text": "Никнейм:",
            "font": font_small,
            "color": MEDIUM_BLUE,
            "pos": (50, 130),
            "center": False
        }
        self.labels.append(nickname_label)
        self.nickname_input = InputBox(50, 150, WIDTH - 100, 40, "Введите никнейм")
        self.inputs.append(self.nickname_input)
        
        # Поле логина
        login_label = {
            "text": "Логин:",
            "font": font_small,
            "color": MEDIUM_BLUE,
            "pos": (50, 200),
            "center": False
        }
        self.labels.append(login_label)
        self.login_input = InputBox(50, 220, WIDTH - 100, 40, "Введите логин")
        self.inputs.append(self.login_input)
        
        # Поле пароля
        password_label = {
            "text": "Пароль:",
            "font": font_small,
            "color": MEDIUM_BLUE,
            "pos": (50, 270),
            "center": False
        }
        self.labels.append(password_label)
        self.password_input = InputBox(50, 290, WIDTH - 100, 40, "Введите пароль", is_password=True)
        self.inputs.append(self.password_input)
        
        # Подтверждение пароля
        confirm_label = {
            "text": "Подтвердите пароль:",
            "font": font_small,
            "color": MEDIUM_BLUE,
            "pos": (50, 340),
            "center": False
        }
        self.labels.append(confirm_label)
        self.confirm_input = InputBox(50, 360, WIDTH - 100, 40, "Подтвердите пароль", is_password=True)
        self.inputs.append(self.confirm_input)
        
        # Кнопка регистрации
        self.register_btn = Button(
            WIDTH // 2 - 150 // 2, 430, 150, 40, 
            "Зарегистрироваться", PRIMARY_BLUE, HOVER_BLUE
        )
        self.buttons.append(self.register_btn)
        
        # Кнопка назад
        self.back_btn = Button(
            WIDTH // 2 - 100 // 2, 490, 100, 40, 
            "Назад", WHITE, LIGHT_BLUE, PRIMARY_BLUE
        )
        self.buttons.append(self.back_btn)
        
    def draw(self, surface):
        """Отрисовка окна"""
        surface.fill(LIGHT_GRAY)
        
        # Отрисовка текстовых меток
        for label in self.labels:
            text_surface = label["font"].render(label["text"], True, label["color"])
            if label["center"]:
                text_rect = text_surface.get_rect(center=label["pos"])
            else:
                text_rect = text_surface.get_rect(topleft=label["pos"])
            surface.blit(text_surface, text_rect)
        
        # Отрисовка полей ввода
        for input_box in self.inputs:
            input_box.draw(surface)
            
        # Отрисовка кнопок
        for button in self.buttons:
            button.draw(surface)
            
    def handle_events(self, events):
        """Обработка событий"""
        mouse_pos = pygame.mouse.get_pos()
        
        for event in events:
            # Обработка полей ввода
            for input_box in self.inputs:
                input_box.handle_event(event)
                
            # Обработка кнопок
            for button in self.buttons:
                button.check_hover(mouse_pos)
                
                if button.is_clicked(mouse_pos, event):
                    if button == self.register_btn:
                        self.handle_register()
                    elif button == self.back_btn:
                        return "auth"  # Возврат к авторизации
        return None
        
    def handle_register(self):
        """Обработка регистрации"""
        nickname = self.nickname_input.text
        login = self.login_input.text
        password = self.password_input.text
        confirm = self.confirm_input.text
        
        # Проверка заполнения полей
        if not nickname or not login or not password or not confirm:
            self.show_message("Ошибка", "Заполните все поля!")
            return
            
        # Проверка совпадения паролей
        if password != confirm:
            self.show_message("Ошибка", "Пароли не совпадают!")
            return
            
        # Регистрация в БД
        if db_registration(login, password, nickname):
            self.show_message("Успех", "Регистрация прошла успешно! Теперь войдите в систему.")
            # Очистка полей
            self.nickname_input.text = ""
            self.login_input.text = ""
            self.password_input.text = ""
            self.confirm_input.text = ""
            return "auth"  # Возврат к авторизации
        else:
            self.show_message("Ошибка", "Логин уже занят!")
    
    def show_message(self, title, message):
        """Показ сообщения (аналогично AuthWindow)"""
        message_box = pygame.Surface((400, 200))
        message_box.fill(WHITE)
        pygame.draw.rect(message_box, GRAY, (0, 0, 400, 200), 2)
        
        title_surface = font_medium.render(title, True, DARK_BLUE)
        message_box.blit(title_surface, (20, 20))
        
        words = message.split(' ')
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + word + " "
            if font_small.size(test_line)[0] < 360:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        
        if current_line:
            lines.append(current_line)
        
        for i, line in enumerate(lines):
            line_surface = font_small.render(line, True, MEDIUM_BLUE)
            message_box.blit(line_surface, (20, 60 + i * 30))
        
        ok_btn = Button(150, 150, 100, 30, "OK", PRIMARY_BLUE, HOVER_BLUE)
        message_rect = message_box.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        
        waiting = True
        while waiting:
            mouse_pos = pygame.mouse.get_pos()
            adjusted_mouse_pos = (mouse_pos[0] - message_rect.x, mouse_pos[1] - message_rect.y)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if ok_btn.is_clicked(adjusted_mouse_pos, event):
                    waiting = False
            
            ok_btn.check_hover(adjusted_mouse_pos)
            
            screen.fill((0, 0, 0, 128))
            screen.blit(message_box, message_rect)
            ok_btn.draw(message_box)
            pygame.display.flip()

def main():
    """Главная функция"""
    # Создание окон
    auth_window = AuthWindow()
    register_window = RegisterWindow()
    
    current_window = "auth"  # Текущее окно
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        
        # Переключение между окнами
        if current_window == "auth":
            result = auth_window.handle_events(events)
            if result == "register":
                current_window = "register"
            auth_window.draw(screen)
        elif current_window == "register":
            result = register_window.handle_events(events)
            if result == "auth":
                current_window = "auth"
            register_window.draw(screen)
        
        pygame.display.flip()
        clock.tick(30)  # 30 FPS
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()