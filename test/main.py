import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtWidgets import QPushButton, QGridLayout

class MorabarabaGame(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Morabaraba Game')
        self.setGeometry(100, 100, 400, 300)

        # برچسب نمایش نوبت
        self.turnLabel = QLabel('نوبت: بازیکن ۱', self)

        # برچسب نمایش تعداد مهره‌های باقی‌مانده و سوخته
        self.remainingLabel = QLabel('مهره‌های باقی‌مانده: ۱۲ | مهره‌های سوخته: ۰', self)

        # قالب بندی شبکه‌ای
        grid = QGridLayout()

        # ایجاد خانه‌ها به عنوان دکمه‌ها
        self.cells = []
        for i in range(3):
            row = []
            for j in range(3):
                cell = QPushButton('', self)
                cell.setFixedSize(60, 60)
                row.append(cell)
                grid.addWidget(cell, i, j)
            self.cells.append(row)

        # اضافه کردن قالب بندی شبکه‌ای و برچسب‌ها به پنجره
        vbox = QVBoxLayout()
        vbox.addWidget(self.turnLabel)
        vbox.addWidget(self.remainingLabel)
        vbox.addLayout(grid)
        self.setLayout(vbox)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = MorabarabaGame()
    sys.exit(app.exec_())
