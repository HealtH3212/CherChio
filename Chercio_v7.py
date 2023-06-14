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
BLUE = (0, 0, 235)
RED = (235, 0, 0)
CIAN = (0, 200, 235)
PURPLE = (140, 0, 245)
YELLOW = (245, 225, 0)
ORANGE = (245, 140, 0)
GREEN = (0, 210, 0)

FIRST_COLOR = BLUE
SECOND_COLOR = RED

# Инициализация игрового поля
def reset_game():
    global grid, current_player, selected_piece, selected_cell, game_over, win
    grid = [[None] * GRID_SIZE for _ in range(GRID_SIZE)]
    current_player = 1
    selected_piece = None
    selected_cell = None
    game_over = False
    win = False

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
BACKGROUND = pygame.image.load("background.png")
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
    if current_player == 1:
        winner_text = f"Игрок {3 - current_player} победил!"
        winner_surface = font.render(winner_text, True, FIRST_COLOR)
        winner_rect = winner_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30))
        screen.blit(winner_surface, winner_rect)
        pygame.display.flip()
    else:
        winner_text = f"Игрок {3 - current_player} победил!"
        winner_surface = font.render(winner_text, True, FIRST_COLOR)
        winner_rect = winner_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30))
        screen.blit(winner_surface, winner_rect)
        pygame.display.flip()


def check_full_board():
    for row in grid:
        if None in row:
            return False
    if current_player == 1:
        for piece in player2_pieces:
            if piece.remaining_uses > 0:
                # Проверяем, существует ли хотя бы одна пустая клетка, куда можно поставить фишку текущего размера
                if any(not p or p.size < piece.size for row in grid for p in row):
                    return False
    elif current_player == 2:
        for piece in player1_pieces:
            if piece.remaining_uses > 0:
                # Проверяем, существует ли хотя бы одна пустая клетка, куда можно поставить фишку текущего размера
                if any(not p or p.size < piece.size for row in grid for p in row):
                    return False
    return True


def check_remaining_pieces():
    for piece in player1_pieces + player2_pieces:
        if piece.remaining_uses > 0:
            return False
    return True



#Режим звука
SOUND_MODE = 1

# Варианты цветов фишек
COLOR_MODE = 1

#Изменение цветового режима
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
    width_sound_circle = WINDOW_WIDTH/2+90
    height_sound_circle = WINDOW_HEIGHT/2
    sound_ring = pygame.draw.circle(screen, BLACK, (width_sound_circle, height_sound_circle), 25, 5)

    def sound_now():
        if SOUND_MODE == 1:
            sound_circle = pygame.draw.circle(screen, FIRST_COLOR, (width_sound_circle, height_sound_circle), 21)
        else:
            sound_circle = pygame.draw.circle(screen, WHITE, (width_sound_circle, height_sound_circle), 21)
        pygame.display.update()


    #Кнопки для изменения цветов
    height_color_btn = WINDOW_HEIGHT/7*5
    width_btn_first_color_mode = WINDOW_WIDTH/2-118
    width_btn_second_color_mode = WINDOW_WIDTH/2-28
    width_btn_third_color_mode = WINDOW_WIDTH/2+62
    
    first_color_mode_first_color = pygame.draw.rect(screen, BLUE, (WINDOW_WIDTH/2-115, height_color_btn, 25, 25))
    first_color_mode_second_color = pygame.draw.rect(screen, RED, (WINDOW_WIDTH/2-90, height_color_btn, 25, 25))
    btn_first_color_mode = pygame.draw.rect(screen, WHITE, (width_btn_first_color_mode, height_color_btn, 56, 25), 3)
    
    second_color_mode_first_color = pygame.draw.rect(screen, GREEN, (WINDOW_WIDTH/2-25, height_color_btn, 25, 25))
    second_color_mode_second_color = pygame.draw.rect(screen, ORANGE, (WINDOW_WIDTH/2, height_color_btn, 25, 25))
    btn_second_color_mode = pygame.draw.rect(screen, WHITE, (width_btn_second_color_mode, height_color_btn, 56, 25), 3)
    
    third_color_mode_first_color = pygame.draw.rect(screen, PURPLE, (WINDOW_WIDTH/2+65, height_color_btn, 25, 25))
    third_color_mode_second_color = pygame.draw.rect(screen, YELLOW, (WINDOW_WIDTH/2+90, height_color_btn, 25, 25))
    btn_third_color_mode = pygame.draw.rect(screen, WHITE, (width_btn_third_color_mode, height_color_btn, 56, 25), 3)


    #подсветка текущих цветов
    def colors_now(btn_first_color_mode, btn_second_color_mode, btn_third_color_mode):
        if COLOR_MODE == 1:
            btn_first_color_mode = pygame.draw.rect(screen, BLACK, (width_btn_first_color_mode, height_color_btn, 56, 25), 3)
            btn_second_color_mode = pygame.draw.rect(screen, WHITE, (width_btn_second_color_mode, height_color_btn, 56, 25), 3)
            btn_third_color_mode = pygame.draw.rect(screen, WHITE, (width_btn_third_color_mode, height_color_btn, 56, 25), 3)
        elif COLOR_MODE == 2:
            btn_second_color_mode = pygame.draw.rect(screen, BLACK, (width_btn_second_color_mode, height_color_btn, 56, 25), 3)
            btn_first_color_mode = pygame.draw.rect(screen, WHITE, (width_btn_first_color_mode, height_color_btn, 56, 25), 3)
            btn_third_color_mode = pygame.draw.rect(screen, WHITE, (width_btn_third_color_mode, height_color_btn, 56, 25), 3)
        elif COLOR_MODE == 3:
            btn_third_color_mode = pygame.draw.rect(screen, BLACK, (width_btn_third_color_mode, height_color_btn, 56, 25), 3)
            btn_first_color_mode = pygame.draw.rect(screen, WHITE, (width_btn_first_color_mode, height_color_btn, 56, 25), 3)
            btn_second_color_mode = pygame.draw.rect(screen, WHITE, (width_btn_second_color_mode, height_color_btn, 56, 25), 3)
        pygame.display.update()

    sound_now()
    colors_now(btn_first_color_mode, btn_second_color_mode, btn_third_color_mode)
    pygame.display.update()
        
    #Проверка нажатия кнопки
    def check_click_sett(btn_rect):
        action = False
        pos = pygame.mouse.get_pos()
        if btn_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        return action

    #проверка нажатия кнопок звука или цвета
    check_changes = 0
    
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
                    elif backward == 3:
                        start_the_game(3)
                    elif backward == 4:
                        start_the_game(4)
            #кнопка m, чтобы вернуться в меню
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    show_menu()

            
            #Если ещё ничего не нажали для изменения
            if check_changes == 0:
                
                #проверка нажатия кружка для изменения звука
                if check_click_sett(sound_ring):
                    if SOUND_MODE == 1:
                        SOUND_MODE = 0
                        sound_now()
                        pygame.mixer.music.pause()
                        check_changes = 1   
                    else:
                        SOUND_MODE = 1
                        sound_now()
                        pygame.mixer.music.unpause()
                        check_changes = 1
                                  
                #проверка нажатия прямоугольников для изменения цветов
                if check_click_sett(btn_first_color_mode):
                    COLOR_MODE = 1
                    change_colors()
                    colors_now(btn_first_color_mode, btn_second_color_mode, btn_third_color_mode)
                    check_changes = 1
                if check_click_sett(btn_second_color_mode):
                    COLOR_MODE = 2
                    change_colors()
                    colors_now(btn_first_color_mode, btn_second_color_mode, btn_third_color_mode)
                    check_changes = 1
                if check_click_sett(btn_third_color_mode):
                    COLOR_MODE = 3
                    change_colors()
                    colors_now(btn_first_color_mode, btn_second_color_mode, btn_third_color_mode)
                    check_changes = 1
                    
            #Если что-то нажали для изменения
            if check_changes == 1 and pygame.mouse.get_pressed()[0] == 0:
                show_settings(backward)


# Основной игровой цикл, входной параметр - меню(1) или настройки(2)
def start_the_game(backward):
    
    global selected_piece
    global selected_cell

    game_over = False
    # Переменная, отвечающая за победу.
    win = False
    if backward == 1:
        reset_game()
    if backward == 3:
        game_over = True
        win = True
    if backward == 4:
        game_over = True


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
                    # Проверка на повторное нажатие на выбранную фишку
                    if selected_piece:
                        if current_player == 1:
                            if pygame.mouse.get_pos()[0] < SIDEBAR_WIDTH:
                                if selected_piece in player1_pieces:
                                    selected_piece.remaining_uses += 1
                                    selected_piece = None
                        elif current_player == 2:
                            if pygame.mouse.get_pos()[0] > WINDOW_WIDTH - SIDEBAR_WIDTH:
                                if selected_piece in player2_pieces:
                                    selected_piece.remaining_uses += 1
                                    selected_piece = None
                    selected_cell = select_cell(pygame.mouse.get_pos())

            if event.type == pygame.MOUSEBUTTONUP:            
                if selected_piece and selected_cell:
                    if grid[selected_cell[0]][selected_cell[1]] is None:
                        if game_over == False:
                            win = False
                        place_piece(selected_piece, selected_cell)
                        if check_winner():
                            game_over = True
                            win = True
                        elif check_full_board() or check_remaining_pieces() :
                            game_over = True    
                        switch_players()
                    else:
                        if game_over == False:
                            win = False
                        if selected_piece.size > grid[selected_cell[0]][selected_cell[1]].size:
                            remove_piece(selected_cell)
                            place_piece(selected_piece, selected_cell)
                            if check_winner():
                                game_over = True
                                win = True
                            elif check_full_board() or check_remaining_pieces():
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

        
        if not game_over:
            if current_player == 1:
                turn_text = font.render(f"Ход игрока {current_player}", True, FIRST_COLOR)
            else:
                turn_text = font.render(f"Ход игрока {current_player}", True, SECOND_COLOR)
            turn_rect = turn_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30))
            screen.blit(turn_text, turn_rect)

        pygame.display.flip()

        if game_over:
            if win:
                print_winner(current_player)
            else:
                draw_text = font.render("Ничья!", True, CIAN)
                draw_rect = draw_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30))
                screen.blit(draw_text, draw_rect)

            pygame.display.flip()
            while game_over:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            start_the_game(1)
                        if event.key == pygame.K_b:
                            show_menu()
                        if event.key == pygame.K_s:
                            if win:
                                show_settings(3)
                            else:
                                show_settings(4)


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
button_start = Menu("Играть", 1)
button_settings = Menu("Настройки", 2)
button_exit = Menu("Выйти", 3)

#кружочки по бокам
def print_circles():
    width_first_col = WINDOW_WIDTH/10
    width_second_col = WINDOW_WIDTH/4
    width_third_col = WINDOW_WIDTH-WINDOW_WIDTH/4
    width_fourth_col = WINDOW_WIDTH-WINDOW_WIDTH/10
    height_small_circle_first_row = WINDOW_HEIGHT/10*3
    height_small_circle_last_row = WINDOW_HEIGHT/9*7
    height_average_circle_first_and_fourth_col = WINDOW_HEIGHT/2
    height_average_circle_second_and_third_col = WINDOW_HEIGHT/7*4
    height_big_circle_first_row = WINDOW_HEIGHT/3
    height_big_circle_last_row = WINDOW_HEIGHT/4*3
    
    pygame.draw.circle(screen, FIRST_COLOR, (width_first_col, height_small_circle_first_row), 25)
    pygame.draw.circle(screen, FIRST_COLOR, (width_first_col, height_average_circle_first_and_fourth_col), 40)
    pygame.draw.circle(screen, FIRST_COLOR, (width_first_col, height_big_circle_last_row), 60)
    pygame.draw.circle(screen, FIRST_COLOR, (width_second_col, height_small_circle_last_row), 25)
    pygame.draw.circle(screen, FIRST_COLOR, (width_second_col, height_average_circle_second_and_third_col), 40)
    pygame.draw.circle(screen, FIRST_COLOR, (width_second_col, height_big_circle_first_row), 60)
    
    pygame.draw.circle(screen, SECOND_COLOR, (width_third_col, height_small_circle_last_row), 25)
    pygame.draw.circle(screen, SECOND_COLOR, (width_third_col, height_average_circle_second_and_third_col), 40)
    pygame.draw.circle(screen, SECOND_COLOR, (width_third_col, height_big_circle_first_row), 60)
    pygame.draw.circle(screen, SECOND_COLOR, (width_fourth_col, height_small_circle_first_row), 25)
    pygame.draw.circle(screen, SECOND_COLOR, (width_fourth_col, height_average_circle_first_and_fourth_col), 40)
    pygame.draw.circle(screen, SECOND_COLOR, (width_fourth_col, height_big_circle_last_row), 60)

    
def show_menu():

     #Название игры
    GAME_NAME_FIRST_PART = f_sans.render("Чер", True,  SECOND_COLOR)
    GN1_rect = GAME_NAME_FIRST_PART.get_rect()
    GN1_rect.center = (WINDOW_WIDTH/2-70, WINDOW_HEIGHT/6)
    GAME_NAME_SECOND_PART = f_sans.render("чио", True, FIRST_COLOR)
    GN2_rect = GAME_NAME_SECOND_PART.get_rect()
    GN2_rect.center = (WINDOW_WIDTH/2+70, WINDOW_HEIGHT/6)
    
    screen.blit(BACKGROUND, (BG_left, BG_top))
    screen.blit(GAME_NAME_FIRST_PART, GN1_rect)
    screen.blit(GAME_NAME_SECOND_PART, GN2_rect)
    button_start.draw()
    button_settings.draw()
    button_exit.draw()
    print_circles()
    pygame.display.update()
    
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()       

        #Проверка нажатия кнопок меню и вызов их функций                  
        if button_start.check_click():
            start_the_game(1)
        if button_settings.check_click():
            show_settings(1)
        if button_exit.check_click():
            pygame.quit()
            sys.exit()
            
show_menu()




                        




