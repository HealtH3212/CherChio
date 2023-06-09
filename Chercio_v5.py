import pygame
import sys

# Инициализация Pygame
pygame.init()

GRID_SIZE = 3
CELL_SIZE = 200
# Размеры окна игры
WINDOW_WIDTH = CELL_SIZE*5 +50
WINDOW_HEIGHT = CELL_SIZE*3 + 60


# Размеры игрового поля и сайдбаров
BOARD_WIDTH = CELL_SIZE * GRID_SIZE
SIDEBAR_WIDTH = (WINDOW_WIDTH - BOARD_WIDTH) // 2

# Инициализация окна игры
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Черчио")

# Цвета
WHITE = (250, 250, 250)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
CIAN = (0, 200, 255)
DARK_GREEN = (25,123,12)
PURPLE = (150, 0, 255)
YELLOW = (255, 225, 0)
ORANGE = (245, 150, 0)
GREEN = (0, 220, 0)

FIRST_COLOR = BLUE
SECOND_COLOR = RED

# Инициализация игрового поля
def reset_game():
    global grid, current_player, selected_piece, selected_cell, game_over
    grid = [[None] * GRID_SIZE for _ in range(GRID_SIZE)]
    current_player = 1
    selected_piece = None
    selected_cell = None
    game_over = False

    # Reset the remaining uses for each piece
    for piece in player1_pieces + player2_pieces:
        piece.remaining_uses = 2

# Инициализация фишек игроков
class Piece:
    def __init__(self, size, player):
        self.size = size
        self.player = player
        self.remaining_uses = 2  # Set the initial number of uses for each piece


player1_pieces = [Piece(1, 1), Piece(2, 1), Piece(3, 1)]
player2_pieces = [Piece(1, 2), Piece(2, 2), Piece(3, 2)]

# Шрифт для вывода текста
font = pygame.font.SysFont(None, 44)
f_sans = pygame.font.SysFont('Comic Sans MS', 80)

# Фоновая картинка
BACKGROUND = pygame.image.load("Background.png")
BG_top = screen.get_height() - BACKGROUND.get_height()
BG_left = screen.get_width()/2 - BACKGROUND.get_width()/2

# Иконка сверху
programIcon = pygame.image.load('icon.png')
pygame.display.set_icon(programIcon)

# Музыка
pygame.mixer.music.load("Spring song 2.mp3")
pygame.mixer.music.play(-1)

def draw_board():
    screen.blit(BACKGROUND, (BG_left, BG_top))
    # Отрисовка счетчика оставшихся фишек игрока 1
    for i, piece in enumerate(player1_pieces):
        rect = pygame.Rect(10, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        piece_size = piece.size - 1
        if piece_size == 0:
            circle_radius = CELL_SIZE / 5
        elif piece_size == 1:
            circle_radius = CELL_SIZE / 3.5
        elif piece_size == 2:
            circle_radius = CELL_SIZE / 2.6
        circle_center = (rect.centerx, rect.centery)
        pygame.draw.circle(screen, FIRST_COLOR, circle_center, circle_radius)

        # Отрисовка счетчика оставшихся фишек
        count_text = font.render(str(piece.remaining_uses), True, WHITE)
        count_rect = count_text.get_rect(center=circle_center)  # Отрисовка в центре фишки
        screen.blit(count_text, count_rect)

    # Отрисовка счетчика оставшихся фишек игрока 2
    for i, piece in enumerate(player2_pieces):
        rect = pygame.Rect(WINDOW_WIDTH - SIDEBAR_WIDTH + 10, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        piece_size = piece.size - 1
        if piece_size == 0:
            circle_radius = CELL_SIZE / 5
        elif piece_size == 1:
            circle_radius = CELL_SIZE / 3.5
        elif piece_size == 2:
            circle_radius = CELL_SIZE / 2.6
        circle_center = (rect.centerx, rect.centery)
        pygame.draw.circle(screen, SECOND_COLOR, circle_center, circle_radius)

        # Отрисовка счетчика оставшихся фишек
        count_text = font.render(str(piece.remaining_uses), True, WHITE)
        count_rect = count_text.get_rect(center=circle_center)  # Отрисовка в центре фишки
        screen.blit(count_text, count_rect)

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            rect = pygame.Rect(SIDEBAR_WIDTH + j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1)
            pygame.draw.rect(screen, BLACK, rect, 3)

            # Отрисовка фишек в ячейках
            piece = grid[i][j]
            if piece:
                piece_size = piece.size - 1
                if piece_size == 0:
                    circle_radius = CELL_SIZE / 5
                elif piece_size == 1:
                    circle_radius = CELL_SIZE / 3.5
                elif piece_size == 2:
                    circle_radius = CELL_SIZE / 2.6

                circle_center = (rect.centerx, rect.centery)
                if (i, j) == selected_cell:
                    player_color = SECOND_COLOR if piece.player == 1 else FIRST_COLOR
                else:
                    player_color = FIRST_COLOR if piece.player == 1 else SECOND_COLOR

                pygame.draw.circle(screen, player_color, circle_center, circle_radius)


def check_winner():
    # Проверка победителя по горизонтали
    for i in range(GRID_SIZE):
        if all(piece and piece.player == current_player for piece in grid[i]):
            return True

    # Проверка победителя по вертикали
    for j in range(GRID_SIZE):
        column = [grid[i][j] for i in range(GRID_SIZE)]
        if all(piece and piece.player == current_player for piece in column):
            return True

    # Проверка победителя по диагонали (слева направо)
    diagonal = [grid[i][i] for i in range(GRID_SIZE)]
    if all(piece and piece.player == current_player for piece in diagonal):
        return True

    # Проверка победителя по диагонали (справа налево)
    diagonal = [grid[i][GRID_SIZE - i - 1] for i in range(GRID_SIZE)]
    if all(piece and piece.player == current_player for piece in diagonal):
        return True

    return False

def switch_players():
    global current_player
    current_player = 3 - current_player

def select_piece(player_pieces, mouse_pos):
    piece_index = mouse_pos[1] // CELL_SIZE
    if piece_index < len(player_pieces):
        piece = player_pieces[piece_index]
        if piece.remaining_uses > 0:  # C
            piece.remaining_uses -= 1  
            return piece
    return None

def select_cell(mouse_pos):
    row = mouse_pos[1] // CELL_SIZE
    col = (mouse_pos[0] - SIDEBAR_WIDTH) // CELL_SIZE
    if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:  # Проверка валидности координат
        if grid[row][col] is None or (selected_piece and grid[row][col].size < selected_piece.size):
            return row, col
    return None

def place_piece(piece, cell):
    if grid[cell[0]][cell[1]] is None:
        grid[cell[0]][cell[1]] = piece

def remove_piece(cell):
    grid[cell[0]][cell[1]] = None

def print_winner(current_player):
  winner_text = f"Игрок {3-current_player} победил!"
  winner_surface = font.render(winner_text, True, CIAN)
  winner_rect = winner_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT-30))
  screen.blit(winner_surface, winner_rect)
  pygame.display.flip()

def check_draw():
    for piece in player1_pieces + player2_pieces:
        if piece.remaining_uses > 0:
            return False
    return True




#Режим звука
SOUND_MODE = 1

# Варианты цветов фишек
COLOR_MODE = 1

def change_colors():
    global FIRST_COLOR
    global SECOND_COLOR
    
    if COLOR_MODE == 1:
        FIRST_COLOR = BLUE
        SECOND_COLOR = RED
    elif COLOR_MODE == 2:
        FIRST_COLOR = GREEN
        SECOND_COLOR = ORANGE
    elif COLOR_MODE == 3:
        FIRST_COLOR = PURPLE
        SECOND_COLOR = YELLOW

#Настройки, входной параметр - меню(1) или игра(2)
def show_settings(backward):

    #Элементы настроек
    SETTINGS = f_sans.render("Настройки", True, SECOND_COLOR)
    SETT_rect = SETTINGS.get_rect()
    SETT_rect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/4)
    Sound = font.render("Звук", True,  FIRST_COLOR)
    Sound_rect = Sound.get_rect()
    Sound_rect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
    Colors = font.render("Поменять цвета", True,  FIRST_COLOR)
    Colors_rect = Colors.get_rect()
    Colors_rect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/14*9)

    screen.blit(BACKGROUND, (BG_left, BG_top))
    screen.blit(SETTINGS, SETT_rect)
    screen.blit(Sound, Sound_rect)
    screen.blit(Colors, Colors_rect)

    global SOUND_MODE
    global COLOR_MODE
    
    #Кружок звука
    sound_ring = pygame.draw.circle(screen, BLACK, (WINDOW_WIDTH/2+90, WINDOW_HEIGHT/2), 25, 5)
    if SOUND_MODE == 1:
        sound_circle = pygame.draw.circle(screen, FIRST_COLOR, (WINDOW_WIDTH/2+90, WINDOW_HEIGHT/2), 21)
    else:
        sound_circle = pygame.draw.circle(screen, WHITE, (WINDOW_WIDTH/2+90, WINDOW_HEIGHT/2), 21)

    #Кнопки для изменения цветов
    btn1_part1 = pygame.draw.rect(screen, BLUE, (WINDOW_WIDTH/2-115, WINDOW_HEIGHT/7*5, 25, 25))
    btn1_part2 = pygame.draw.rect(screen, RED, (WINDOW_WIDTH/2-90, WINDOW_HEIGHT/7*5, 25, 25))
    btn_color1 = pygame.draw.rect(screen, WHITE, (WINDOW_WIDTH/2-118, WINDOW_HEIGHT/7*5, 56, 25), 3)
    btn2_part1 = pygame.draw.rect(screen, GREEN, (WINDOW_WIDTH/2-25, WINDOW_HEIGHT/7*5, 25, 25))
    btn2_part2 = pygame.draw.rect(screen, ORANGE, (WINDOW_WIDTH/2, WINDOW_HEIGHT/7*5, 25, 25))
    btn_color2 = pygame.draw.rect(screen, WHITE, (WINDOW_WIDTH/2-28, WINDOW_HEIGHT/7*5, 56, 25), 3)
    btn3_part1 = pygame.draw.rect(screen, PURPLE, (WINDOW_WIDTH/2+65, WINDOW_HEIGHT/7*5, 25, 25))
    btn3_part2 = pygame.draw.rect(screen, YELLOW, (WINDOW_WIDTH/2+90, WINDOW_HEIGHT/7*5, 25, 25))
    btn_color3 = pygame.draw.rect(screen, WHITE, (WINDOW_WIDTH/2+62, WINDOW_HEIGHT/7*5, 56, 25), 3)

    #подсветка текущих цветов
    def colors_now(btn_color1, btn_color2, btn_color3):
        if COLOR_MODE == 1:
            btn_color1 = pygame.draw.rect(screen, BLACK, (WINDOW_WIDTH/2-118, WINDOW_HEIGHT/7*5, 56, 25), 3)
            btn_color2 = pygame.draw.rect(screen, WHITE, (WINDOW_WIDTH/2-28, WINDOW_HEIGHT/7*5, 56, 25), 3)
            btn_color3 = pygame.draw.rect(screen, WHITE, (WINDOW_WIDTH/2+62, WINDOW_HEIGHT/7*5, 56, 25), 3)
        elif COLOR_MODE == 2:
            btn_color2 = pygame.draw.rect(screen, BLACK, (WINDOW_WIDTH/2-28, WINDOW_HEIGHT/7*5, 56, 25), 3)
            btn_color1 = pygame.draw.rect(screen, WHITE, (WINDOW_WIDTH/2-118, WINDOW_HEIGHT/7*5, 56, 25), 3)
            btn_color3 = pygame.draw.rect(screen, WHITE, (WINDOW_WIDTH/2+62, WINDOW_HEIGHT/7*5, 56, 25), 3)
        elif COLOR_MODE == 3:
            btn_color3 = pygame.draw.rect(screen, BLACK, (WINDOW_WIDTH/2+62, WINDOW_HEIGHT/7*5, 56, 25), 3)
            btn_color1 = pygame.draw.rect(screen, WHITE, (WINDOW_WIDTH/2-118, WINDOW_HEIGHT/7*5, 56, 25), 3)
            btn_color2 = pygame.draw.rect(screen, WHITE, (WINDOW_WIDTH/2-28, WINDOW_HEIGHT/7*5, 56, 25), 3)

    colors_now(btn_color1, btn_color2, btn_color3)
    pygame.display.update()
        
    #Проверка нажатия кнопки
    def check_click_sett(btn_rect):
        click = False
        action = False
        pos = pygame.mouse.get_pos()
        if btn_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and click == False:
                click = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            click = False
        return action
    
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            #кнопка b, чтобы вернуться на предыдущий экран
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    if backward == 1:
                        show_menu()
                    elif backward == 2:
                        start_the_game(2)
            #кнопка m, чтобы вернуться в меню
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    show_menu()

            #проверка нажатия кружка для изменения звука
            if check_click_sett(sound_ring):
                if SOUND_MODE == 1:
                    SOUND_MODE = 0
                    pygame.mixer.music.pause()
                    show_settings(backward)
                else:
                    SOUND_MODE = 1
                    pygame.mixer.music.unpause()
                    show_settings(backward)
                    
            #проверка нажатия прямоугольников для изменения цветов
            if check_click_sett(btn_color1):
                COLOR_MODE = 1
                change_colors()
                colors_now(btn_color1, btn_color2, btn_color3)
                show_settings(backward)
            if check_click_sett(btn_color2):
                COLOR_MODE = 2
                change_colors()
                colors_now(btn_color1, btn_color2, btn_color3)
                show_settings(backward)
            if check_click_sett(btn_color3):
                COLOR_MODE = 3
                change_colors()
                colors_now(btn_color1, btn_color2, btn_color3)
                show_settings(backward)


# Основной игровой цикл, входной параметр - меню(1) или настройки(2)
def start_the_game(backward):
    
    global selected_piece
    global selected_cell

    game_over = False
    if backward == 1:
        reset_game()  

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not selected_piece:
                    if current_player == 1 and pygame.mouse.get_pos()[0] < SIDEBAR_WIDTH:
                        selected_piece = select_piece(player1_pieces, pygame.mouse.get_pos())
                    elif current_player == 2 and pygame.mouse.get_pos()[0] > WINDOW_WIDTH - SIDEBAR_WIDTH:
                        selected_piece = select_piece(player2_pieces, pygame.mouse.get_pos())
                else:
                    selected_cell = select_cell(pygame.mouse.get_pos())

            if event.type == pygame.MOUSEBUTTONUP:            
                if selected_piece and selected_cell:
                    if grid[selected_cell[0]][selected_cell[1]] is None:
                        place_piece(selected_piece, selected_cell)
                        if check_winner():
                            game_over = True
                        elif check_draw():
                            game_over = True    
                        switch_players()
                    else:
                        if selected_piece.size > grid[selected_cell[0]][selected_cell[1]].size:
                            remove_piece(selected_cell)
                            place_piece(selected_piece, selected_cell)
                            if check_winner():
                                game_over = True
                            elif check_draw():
                                game_over = True    
                            switch_players()
                    
                    selected_piece = None
                    selected_cell = None

            # Проверка нажатия клавиши R для перезапуска игры
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                    
            # Проверка нажатия клавиши B для возвращения в меню 
                if event.key == pygame.K_b:
                    show_menu()
                    
            # Проверка нажатия клавиши S для экрана настройки 
                if event.key == pygame.K_s:
                    show_settings(2)
                    
        screen.blit(BACKGROUND, (BG_left, BG_top))
        draw_board()

        if selected_piece:
            piece_rect = pygame.Rect(10 if current_player == 1 else WINDOW_WIDTH - SIDEBAR_WIDTH + 10,
                                     (selected_piece.size - 1) * CELL_SIZE,
                                     CELL_SIZE,
                                     CELL_SIZE)
            pygame.draw.rect(screen, CIAN, piece_rect, 3)

        pygame.display.flip()
        if game_over:
            if check_draw():
                draw_text = font.render("Ничья!", True, CIAN)
                draw_rect = draw_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30))
                screen.blit(draw_text, draw_rect)
            else:
                print_winner(current_player)

            pygame.display.flip()
            while game_over:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            reset_game()
                            game_over = False
                        if event.key == pygame.K_b:
                            show_menu()
                      

#меню
class Menu:   
    def __init__(self, text, i):
        self.btn = font.render(text, True, CIAN)
        self.rect = pygame.Rect(WINDOW_WIDTH/2-125, WINDOW_HEIGHT/4+i*WINDOW_HEIGHT/8, 250, 60)
        self.text_rect = self.btn.get_rect()
        self.text_rect.center = self.rect.center
        self.clicked = False

    def draw(self):
        pygame.draw.rect(screen, BLACK, self.rect, 4, 35)
        screen.blit(self.btn, self.text_rect)

    #проверка нажатия кнопки       
    def check_click(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        return action

#кнопки меню
btn1 = Menu("Играть", 1)
btn2 = Menu("Настройки", 2)
btn3 = Menu("Выйти", 3)

#кружочки по бокам
def print_circles():
    pygame.draw.circle(screen, FIRST_COLOR, (WINDOW_WIDTH/10, WINDOW_HEIGHT/10*3), 25)
    pygame.draw.circle(screen, FIRST_COLOR, (WINDOW_WIDTH/10, WINDOW_HEIGHT/2), 40)
    pygame.draw.circle(screen, FIRST_COLOR, (WINDOW_WIDTH/10, WINDOW_HEIGHT/4*3), 60)
    pygame.draw.circle(screen, FIRST_COLOR, (WINDOW_WIDTH/4, WINDOW_HEIGHT/9*7), 25)
    pygame.draw.circle(screen, FIRST_COLOR, (WINDOW_WIDTH/4, WINDOW_HEIGHT/7*4), 40)
    pygame.draw.circle(screen, FIRST_COLOR, (WINDOW_WIDTH/4, WINDOW_HEIGHT/3), 60)
    pygame.draw.circle(screen, SECOND_COLOR, (WINDOW_WIDTH-WINDOW_WIDTH/10, WINDOW_HEIGHT/10*3), 25)
    pygame.draw.circle(screen, SECOND_COLOR, (WINDOW_WIDTH-WINDOW_WIDTH/10, WINDOW_HEIGHT/2), 40)
    pygame.draw.circle(screen, SECOND_COLOR, (WINDOW_WIDTH-WINDOW_WIDTH/10, WINDOW_HEIGHT/4*3), 60)
    pygame.draw.circle(screen, SECOND_COLOR, (WINDOW_WIDTH-WINDOW_WIDTH/4, WINDOW_HEIGHT/9*7), 25)
    pygame.draw.circle(screen, SECOND_COLOR, (WINDOW_WIDTH-WINDOW_WIDTH/4, WINDOW_HEIGHT/7*4), 40)
    pygame.draw.circle(screen, SECOND_COLOR, (WINDOW_WIDTH-WINDOW_WIDTH/4, WINDOW_HEIGHT/3), 60)


 #Название игры
##GAME_NAME = f_sans.render("Черчио", True,  RED)
##GN_rect = GAME_NAME.get_rect()
##GN_rect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/4)
    
def show_menu():

     #Название игры
    GAME_NAME1 = f_sans.render("Чер", True,  SECOND_COLOR)
    GN1_rect = GAME_NAME1.get_rect()
    GN1_rect.center = (WINDOW_WIDTH/2-70, WINDOW_HEIGHT/6)
    GAME_NAME2 = f_sans.render("чио", True, FIRST_COLOR)
    GN2_rect = GAME_NAME2.get_rect()
    GN2_rect.center = (WINDOW_WIDTH/2+70, WINDOW_HEIGHT/6)
    
    screen.blit(BACKGROUND, (BG_left, BG_top))
    screen.blit(GAME_NAME1, GN1_rect)
    screen.blit(GAME_NAME2, GN2_rect)
    #screen.blit(GAME_NAME, GN_rect)
    btn1.draw()
    btn2.draw()
    btn3.draw()
    print_circles()
    pygame.display.update()
    
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()       

        #Проверка нажатия кнопок меню и вызов их функций                  
        if btn1.check_click():
            start_the_game(1)
        if btn2.check_click():
            show_settings(1)
        if btn3.check_click():
            pygame.quit()
            sys.exit()
            
show_menu()




                        




