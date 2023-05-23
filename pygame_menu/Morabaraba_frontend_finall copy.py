import sys
import pygame
from pygame.locals import *
import subprocess


class MainMenuItem:
    def __init__(self, text, position, callback):
        self.text = text
        self.position = position
        self.callback = callback
        self.font = pygame.font.Font(None, 36)
        self.rect = pygame.Rect(self.position[0], self.position[1], 200, 50)
        self.color = (255, 255, 255)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.callback()

class MainMenu:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Define screen attributes
        self.screen_size = (680, 680)
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Main Menu")

        # Create main menu items
        self.start_item = MainMenuItem("Start", (245, 300), self.start_game)

        # Define font for the additional text
        self.text_font = pygame.font.Font(None, 50)

        # Define additional text
        self.additional_text = "Welcome to Morabaraba!"
    
    def start_game(self):
        # Create an instance of MorabaScreen and run the game
        moraba_screen = MorabaScreen(self.screen)
        moraba_screen.main()

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Handle events for main menu items
                self.start_item.handle_event(event)

            # Draw main menu items
            self.screen.fill((0, 0, 0))
            self.start_item.draw(self.screen)


            # Draw main menu items and additional text
            self.screen.fill((0, 0, 0))
            self.start_item.draw(self.screen)

            # Render and display the additional text
            text_surface = self.text_font.render(self.additional_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.screen_size[0] // 2 , 190))
            self.screen.blit(text_surface, text_rect)

            pygame.display.flip()

        pygame.quit()



class MorabaScreen():
    def __init__(self, screen):
        
        self.screen = screen

        # Initialize Pygame
        pygame.init()

        # Define board attributes
        self.board_size = (1000, 1000)  # size of the board
        # self.fill
        self.slot_size = 60  # size of each slot
        self.rows = 7  # number of rows
        self.cols = 7  # number of columns
        self.gap = 34  # gap between each slot


        # Define colors
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.dots_line = '#1D700F'
        
        # تازه اضافه شده
        self.game_over = False  # اضافه کنید
        self.player_turn = 1  # اضافه کنید
        self.board = [[0] * 8 for _ in range(3)]  # اضافه کنید

        # Define font for the labels
        self.label_font = pygame.font.Font(None, 24)

        # Initialize the current player
        self.current_player = 1

        # Initialize the player scores
        self.player1_score = 0
        self.player2_score = 0

        # Initialize the players' colors
        self.player1_color = self.BLUE
        self.player2_color = self.RED

        # Initialize the current player
        self.current_player = 1

        # Initialize the selected circles for each player
        self.player1_selected = set()
        self.player2_selected = set()

        # Initialize the screen
        self.screen = pygame.display.set_mode(self.board_size)
        pygame.display.set_caption("Morabaraba Board")

        # Set up a clock for the game loop
        self.clock = pygame.time.Clock()

        self.board_list = [(0, 0), (0, 3), (0, 6), (1, 1), (1, 3), (1, 5), (2, 2),
                    (2, 3), (2, 4), (3, 0), (3, 1), (3, 2),(3,3), (3, 4), (3, 5),
                    (3, 6), (4, 2), (4, 3), (4, 4), (5, 1), (5, 3), (5, 5),
                    (6, 0), (6, 3), (6, 6)]

        # Declare the circle_data dictionary
        self.circle_data = {}
        for (r, c) in self.board_list:
            x = c * self.slot_size + self.gap * (c + 1)
            y = r * self.slot_size + self.gap * (r + 1)
            self.circle_data[(r, c)] = {
                'position': (x + 30, y + 30),
                'color': self.dots_line
            }

    def draw_labels(self):

        self.player1_score = len(self.player1_selected)
        self.player2_score = len(self.player2_selected)


        # Render and display the current player label
        player_label = self.label_font.render("Current Player: {}".format(self.current_player), True, self.WHITE)
        player_label_rect = player_label.get_rect(topright=(self.board_size[0] - 100, 200))
        self.screen.blit(player_label, player_label_rect)

        # Render and display the player scores
        player1_score_label = self.label_font.render("Player 1 Score: {}".format(self.player1_score), True, self.WHITE)
        player1_score_label_rect = player1_score_label.get_rect(topright=(self.board_size[0] - 100, 260))
        self.screen.blit(player1_score_label, player1_score_label_rect)

        player2_score_label = self.label_font.render("Player 2 Score: {}".format(self.player2_score), True, self.WHITE)
        player2_score_label_rect = player2_score_label.get_rect(topright=(self.board_size[0] - 100, 290))
        self.screen.blit(player2_score_label, player2_score_label_rect)



    # Draw the board
    def draw_board(self):
        self.screen.fill(self.WHITE)  # fill the screen with white
        # Draw the frame around the game board
        frame_width = 1
        frame_rect = pygame.Rect(50, 50, self.board_size[0] + frame_width * 2, self.board_size[1] + frame_width * 2)
        pygame.draw.rect(self.screen, self.BLACK, frame_rect)
        # Calculate the offset for drawing the board inside the frame
        board_offset = (frame_width, frame_width)

        # Draw the game board
        pygame.draw.rect(self.screen, "black", (board_offset[0], board_offset[1], self.board_size[0], self.board_size[1]))


        pygame.draw.rect(self.screen, "black", (0, 0, 680, 680))

        # rect1
        pygame.draw.line(self.screen, self.dots_line, (64, 64), (680 - 64, 64), 4)
        pygame.draw.line(self.screen, self.dots_line, (64, 64), (64, 680 - 64), 4)
        pygame.draw.line(self.screen, self.dots_line, (680 - 55, 64), (680 - 55, 680 - 64), 4)
        pygame.draw.line(self.screen, self.dots_line, (64, 680 - 50), (680 - 55, 680 - 50), 4)
        # rect2
        pygame.draw.line(self.screen, self.dots_line, (155, 155), (680 - 155, 155), 4)
        pygame.draw.line(self.screen, self.dots_line, (155, 155), (155, 680 - 155), 4)
        pygame.draw.line(self.screen, self.dots_line, (680 - 145, 145), (680 - 145, 680 - 145), 4)
        pygame.draw.line(self.screen, self.dots_line, (155, 680 - 145), (680 - 145, 680 - 145), 4)
        # rect3
        pygame.draw.line(self.screen, self.dots_line, (250, 250), (680 - 250, 250), 4)
        pygame.draw.line(self.screen, self.dots_line, (250, 250), (250, 680 - 250), 4)
        pygame.draw.line(self.screen, self.dots_line, (680 - 240, 240), (680 - 240, 680 - 240), 4)
        pygame.draw.line(self.screen, self.dots_line, (250, 680 - 240), (680 - 240, 680 - 240), 4)
        # line
        pygame.draw.line(self.screen, self.dots_line, (64, 345), (345 - 80, 345), 4)
        pygame.draw.line(self.screen, self.dots_line, (345, 64), (345, 345 - 80), 4)
        pygame.draw.line(self.screen, self.dots_line, (450, 345), (680 - 64, 345), 4)
        pygame.draw.line(self.screen, self.dots_line, (345, 445), (345, 680 - 64), 4)
        # line
        pygame.draw.line(self.screen, self.dots_line, (64, 64), (250, 250), 6)
        pygame.draw.line(self.screen, self.dots_line, (64, 680 - 55), (260, 680 - 250), 6)
        pygame.draw.line(self.screen, self.dots_line, (680 - 250, 260), (680 - 55, 64), 6)
        pygame.draw.line(self.screen, self.dots_line, (445, 445), (680 - 50, 680 - 50), 6)

        # Draw the circles with their respective colors
        for position, data in self.circle_data.items():
            x, y = data['position']
            color = data['color']
            pygame.draw.circle(self.screen, color, (x, y), 15)
            # Draw the player's color circle
            self.is_shift(self.circle_data)


    # تابع جدید اضافه شده
    def check_win(self):
        winning_conditions = [
            # ردیف‌های برنده
            [(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],
            # ستون‌های برنده
            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],
            # قطرهای برنده
            [(0, 0), (1, 1), (2, 2)],
            [(0, 2), (1, 1), (2, 0)],
        ]

        for condition in winning_conditions:
            player1_count = 0
            player2_count = 0

            for i, j in condition:
                if self.board[i][j] == 1:
                    player1_count += 1
                elif self.board[i][j] == 2:
                    player2_count += 1

            if player1_count == 3:
                self.game_over = True
                print("Player 1 wins!")
                break
            elif player2_count == 3:
                self.game_over = True
                print("Player 2 wins!")
                break


    

    # Check if a circle was clicked and change its color
    def check_click(self, pos):
        if not self.game_over and len(self.player1_selected) + len(self.player2_selected) == 24:
            # بازی به پایان رسیده است و تمام مربع‌ها انتخاب شده‌اند
            print("The game is over. Please start a new game.")
            return

        # تبدیل موقعیت کلیک شده به شاخص ردیف و ستون
        row = pos[1] // self.square_size
        col = pos[0] // self.square_size

        # بررسی نوبت بازیکن
        if self.current_player == 1 and row in self.player2_selected:
            print("Invalid move. Please select an empty square.")
            return
        elif self.current_player == 2 and row in self.player1_selected:
            print("Invalid move. Please select an empty square.")
            return

        # ثبت مربع انتخاب شده توسط بازیکن
        self.board[row][col] = self.current_player

        if self.current_player == 1:
            self.player1_selected.append(row)
        else:
            self.player2_selected.append(row)

        # بررسی برنده شدن
        self.check_win()

        # تغییر نوبت بازیکن
        self.current_player = 2 if self.current_player == 1 else 1
        # بررسی معتبر بودن حرکت
        if not self.check_valid_move(row, col):
            print("Invalid move. Please select a valid square.")
            return
        
         # بررسی وضعیت بازی
        if not self.game_over and len(self.player1_selected) + len(self.player2_selected) == 24:
            winner = self.check_win()
            if winner is not None:
                self.game_over = True
                print("Game Over! Winner:", winner)
                print("Press 'R' to restart the game.")

        # به‌روزرسانی جدول بازی
        self.update_board(row, col)

        # تغییر نوبت بازی
        self.switch_turn()

        # به‌روزرسانی صفحه بازی
        self.draw_board()



    # تابع بررسی وقوع رویداد کلیدی
    def check_keypress(self, key):
        if key == pygame.K_r and self.game_over:
            self.reset_game()
            self.draw_board()


    # تابع جدید
    def reset_game(self):
        # تنظیمات اولیه بازی
        self.current_turn = 1
        self.player1_selected = []
        self.player2_selected = []
        self.board = [[0, 0, 0] for _ in range(8)]
        self.game_over = False





        

    # تابع جدید
    def switch_turn(self):
        if self.current_turn == 1:
            self.current_turn = 2
        else:
            self.current_turn = 1



    # تابع جدید
    def update_board(self, source_row, source_col, dest_row, dest_col):
        # خالی کردن مربع منبع
        self.board[source_row][source_col] = EMPTY

        # قرار دادن مهره بازیکن فعلی در مربع مقصد
        self.board[dest_row][dest_col] = self.current_player

        # به‌روزرسانی وضعیت انتخاب مهره‌ها
        if self.current_player == PLAYER1:
            self.player1_selected.remove((source_row, source_col))
            self.player1_selected.add((dest_row, dest_col))
        else:
            self.player2_selected.remove((source_row, source_col))
            self.player2_selected.add((dest_row, dest_col))





    # تابع جدید
    def check_valid_move(self, source_row, source_col, dest_row, dest_col):
        # بررسی معتبر بودن مربع منبع
        if self.board[source_row][source_col] != self.current_player:
            return False

        # بررسی معتبر بودن مربع مقصد
        if self.board[dest_row][dest_col] != EMPTY:
            return False

        # بررسی حرکت در یک خط عمودی یا افقی
        if source_row != dest_row and source_col != dest_col:
            return False

        # بررسی محدوده معتبر بودن حرکت
        if abs(source_row - dest_row) > 1 or abs(source_col - dest_col) > 1:
            return False

        # همه شرایط معتبر بودن حرکت برقرار است
        return True



    # Remove the color of the selected circle
    def check_click_pic(self, pos):
        for position, data in self.circle_data.items():
            x, y = data['position']
            if x - 15 <= pos[0] <= x + 15 and y - 15 <= pos[1] <= y + 15:
                # Change the color of the clicked circle
                if data['color'] == self.player1_color:
                    data['color'] = self.dots_line
                    self.player1_selected.remove(position)
                elif data['color'] == self.player2_color:
                        data['color'] = self.dots_line
                        self.player2_selected.remove(position)
                else:
                        data['color'] = self.dots_line

                break

    # Draw the player's color circle
    def is_shift(self, circle_data):
        if self.current_player == 1:
            pygame.draw.circle(self.screen, self.player1_color, (345, 345), 30)
            circle_data[(3, 3)]['color'] = self.player1_color
        else:
            pygame.draw.circle(self.screen, self.player2_color, (345, 345), 30)
            circle_data[(3, 3)]['color'] = self.player2_color

    def main(self):
        # Main game loop
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        mouse_pos = pygame.mouse.get_pos()
                        self.check_click(mouse_pos)
                    elif event.button == 3:  # Right mouse button
                        mouse_pos = pygame.mouse.get_pos()
                        self.check_click_pic(mouse_pos)

            # Draw the board and labels
            self.screen.fill(self.BLACK)
            self.draw_board()
            self.draw_labels()

            pygame.display.flip()

        pygame.quit()




if __name__ == "__main__":
    main_menu = MainMenu()
    main_menu.run()
