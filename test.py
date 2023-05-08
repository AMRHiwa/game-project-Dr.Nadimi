from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton
import sys


SIZE = 3
WIN_COUNT = 3



class TicTacToe(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        # ماتریس بازی:
        # 0 برای جای خالی
        # 1 برای نقطه‌های "X"
        # -1 برای نقطه‌های "O"
        self.board = [[0 for _ in range(SIZE)] for _ in range(SIZE)]
        
        # برای استفاده از الگوریتم minmax، باید به خط حرکت ها دسترسی داشته باشیم
        self.player = 1  # بازیکن "X" اول بازی را شروع می کند
        self.ai = -1  # بازیکن "O" که نرمالا کامپیوتر است
        self.moves = [i for i in range(SIZE ** 2)]

        # دکمه‌های بازی
        self.buttons = [[QPushButton(self) for _ in range(SIZE)] for _ in range(SIZE)]
        for i in range(SIZE):
            for j in range(SIZE):
                self.buttons[i][j].setFixedSize(80, 80)
                self.buttons[i][j].clicked.connect(lambda _, i=i, j=j: self.mark(i, j))
                self.buttons[i][j].setFont(self.font)
                self.buttons[i][j].setStyleSheet("QPushButton { font: bold 48px; }")

        self.buttons[0][0].setFixedSize(80, 80)

    # متد برای شروع یک بازی جدید:
    def new_game(self):
        self.board = [[0 for _ in range(SIZE)] for _ in range(SIZE)]
        self.player = 1
        self.ai = -1
        self.moves = [i for i in range(SIZE ** 2)]

        for i in range(SIZE):
            for j in range(SIZE):
                self.buttons[i][j].setText('')
                self.buttons[i][j].setEnabled(True)

    # متد برای چک کردن صحت شروع بازی:
    def check_start(self):
        count_x = 0
        count_o = 0
        
        for i in range(SIZE):
            for j in range(SIZE):
                if self.buttons[i][j].text() == "X":
                    count_x += 1
                elif self.buttons[i][j].text() == "O":
                    count_o += 1

        if abs(count_x - count_o) > 1:
            return False
        elif count_x == count_o:
            self.player = 1
            self.ai = -1
        else:
            self.player = -1
            self.ai = 1

        return True

    # متد برای گرفتن ورودی از کامپیوتر:
    def ai_move(self):
        score, i, j = self.minmax(self.board, self.ai, 0)
        self.mark(i, j)

    # الگوریتم minmax:
    def minmax(self, board, player, depth):
        if self.game_over():
            return self.evaluate()

        best_score = None
        best_row = None
        best_col = None

        if player == self.ai:
            for row in range(SIZE):
                for col in range(SIZE):
                    if board[row][col] == 0:
                        board[row][col] = player
                        action_score, _, _ = self.minmax(board, self.player, depth + 1)
                        board[row][col] = 0

                        if best_score is None or action_score > best_score:
                            best_score = action_score
                            best_row = row
                            best_col = col
        else:
            for row in range(SIZE):
                for col in range(SIZE):
                    if board[row][col] == 0:
                        board[row][col] = player
                        action_score, _, _ = self.minmax(board, self.ai, depth + 1)
                        board[row][col] = 0

                        if best_score is None or action_score < best_score:
                            best_score = action_score
                            best_row = row
                            best_col = col

        return best_score, best_row, best_col

    # متد برای ارزیابی یک حالت بازی:
    def evaluate(self):
        winner = self.check_win()

        if winner == self.ai:
            return 10
        elif winner == self.player:
            return -10
        else:
            return 0

    # متدی برای چک کردن پایان بازی:
    def game_over(self):
        return self.check_win() or len(self.moves) == 0

    # متدی برای چک کردن برد یا باخت:
    def check_win(self):
        for i in range(SIZE):
            sum_row = sum(self.board[i])
            sum_col = sum([self.board[x][i] for x in range(SIZE)])
            if abs(sum_row) == SIZE:
                return self.board[i][0]
            elif abs(sum_col) == SIZE:
                return self.board[0][i]

        sum_diag1 = sum([self.board[x][x] for x in range(SIZE)])
        sum_diag2 = sum([self.board[x][SIZE - 1 - x] for x in range(SIZE)])
        if abs(sum_diag1) == SIZE:
            return self.board[0][0]
        elif abs(sum_diag2) == SIZE:
            return self.board[0][SIZE - 1]

        return None

    # متدی برای نمایش پیغام در صورت پایان بازی:
    def show_message(self, message):
        if message == "X  Won!":
            message = "You Won!"
        elif message == "O  Won!":
            message = "Computer Won!"
        elif message == "Draw!":
            message = "Draw!"

        msgBox = QLabel(message, self)
        msgBox.setStyleSheet("font: bold 25px")
        msgBox.move(170, 300)
        msgBox.resize(200, 30)
        msgBox.show()

    # متدی برای نشان دادن نقطه‌ی انتخاب شده توسط کاربر یا کامپیوتر:
    def mark(self, i, j):
        if self.buttons[i][j].isEnabled():
            self.buttons[i][j].setText("X" if self.player == 1 else "O")
            self.buttons[i][j].setEnabled(False)

            self.board[i][j] = self.player
            self.moves.remove(i * SIZE + j)

            if self.check_win():
                self.disable_buttons()
                self.show_message(self.buttons[i][j].text() + "  Won!")
            elif len(self.moves) == 0:
                self.disable_buttons()
                self.show_message("Draw!")
            else:
                self.player *= -1
                self.ai_move()

    # متدی برای غیرفعال کردن دکمه‌های بازی در صورت پایان بازی:
    def disable_buttons(self):
        for i in range(SIZE):
            for j in range(SIZE):
                self.buttons[i][j].setEnabled(False)

    # متدی برای ساخت ویدجت‌های بازی:
    def initUI(self):
        self.setWindowTitle("Tic-Tac-Toe")
        self.setGeometry(200, 200, 350, 400)
        self.font = self.font()
        self.font.setPointSize(40)

        self.title = QLabel("Tic Tac Toe", self)
        self.title.move(130, 20)
        self.title.setFont(self.font)
        self.title.setStyleSheet('color: #1E90FF;')

        self.new_game_button = QPushButton("New Game", self)
        self.new_game_button.move(130, 250)
        self.new_game_button.clicked.connect(self.new_game)

        self.grid_layout = QVBoxLayout()
        for i in range(SIZE):
            hbox = QHBoxLayout()
            for j in range(SIZE):
                hbox.addWidget(self.buttons[i][j])
            self.grid_layout.addLayout(hbox)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.addLayout(self.grid_layout)
        self.main_layout.addWidget(self.new_game_button)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = TicTacToe()
    # ex = TicTacToe()
    ex.show()
    sys.exit(app.exec_())
