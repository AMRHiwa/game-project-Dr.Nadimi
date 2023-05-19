import sys
from PyQt5.QtWidgets import QLabel,QApplication, QMainWindow, QPlainTextEdit, QVBoxLayout, QWidget, QPushButton, QLineEdit, QHBoxLayout
from PyQt5.QtCore import QProcess, pyqtSignal, QObject, Qt, QTimer
from PyQt5.QtGui import QPixmap, QColor, QFont





# class CmdProcess(QObject):
#     outputChanged = pyqtSignal(str)

#     def __init__(self, parent=None):
#         super().__init__(parent)

#         # Create the process object and connect its signals
#         self.process = QProcess(self)
#         self.process.readyReadStandardOutput.connect(self.handle_stdout)

    # def start(self):
    #     # Start the process with cmd.exe on Windows or bash on Linux/Mac
    #     if sys.platform.startswith('win'):
    #         self.process.start('cmd.exe')
    #     else:
    #         self.process.start('bash')

    # def write(self, command):
    #     # Write a command to the process
    #     self.process.write(command.encode())

    # def handle_stdout(self):
    #     # Emit the outputChanged signal with the process's output
    #     output = self.process.readAllStandardOutput().data().decode()
    #     self.outputChanged.emit(output)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setFixedSize(1024, 900)
        self.setWindowTitle("Morabaraba")
        # self.setStyleSheet("background-image: url('data\background.png'); background-repeat: no-repeat; background-position: center;") # تنظیم سبک برای ویجت


    
        # self.colors = [QColor("red"), QColor("yellow"), QColor("blue"), QColor("purple"), QColor("orange"), QColor("pink"), QColor("skyblue")]
        self.colors = [QColor("red"), QColor("orange"), QColor("yellow"), QColor("green"), QColor("blue"), QColor("indigo"), QColor("violet")]
        self.current_color = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.change_color)
        self.timer.start(500)  # هر ثانیه تابع change_color فراخوانی می‌شود
        
        
        # Create the widgets
        self.output_widget = QPlainTextEdit(self)
        self.output_widget.setStyleSheet(
        "QPlainTextEdit {"
        "   border: 2px solid #2196F3;"
        "   border-radius: 5px;"
        "   padding: 5px;"
        "   background-color: #00ced1;"
        "   color: #333333;"
        "   font-size: 16px;"
        "}"
        )


        self.input_widget = QLineEdit(self)
        self.input_widget.setPlaceholderText('Enter row and column ...')
        self.input_widget.setStyleSheet(
        "QLineEdit {"
        "   border: 2px solid #2196F3;"
        "   border-radius: 5px;"
        "   padding: 5px;"
        "   background-color: #F5F5F5;"
        "   color: #333333;"
        "   font-size: 20px;"
        "}")


        self.run_button = QPushButton('Enter', self)
        self.run_button.setStyleSheet( 
             "QPushButton {"
        "   background-color: #cae00f;"
        "   border: 2px solid #2196F3;"

        "   color: white;"
        "   padding: 10px;"
        "   border-radius: 5px;"
        "   font-size: 16px;"
        "   color: #b8860b;"
        "}"
        "QPushButton:hover {"
        "   background-color: #45a049;"
        "}"
        "QPushButton:pressed {"
        "   background-color: #39823b;"
        "}"
        )
        
        
        self.start_button = QPushButton('Start', self)
        self.start_button.setStyleSheet( 
             "QPushButton {"
        "   background-color: #42ff75;"
        "   border: 2px solid #2196F3;"

        "   color: white;"
        "   padding: 10px;"
        "   border-radius: 5px;"
        "   font-size: 16px;"
        "   color: #b8860b;"
        "}"
        "QPushButton:hover {"
        "   background-color: #45a049;"
        "}"
        "QPushButton:pressed {"
        "   background-color: #39823b;"
        "}"
        )
        # -------------- 
        self.label_M1 = QLabel(self,text='M')
        self.label_M1.setFont(QFont('Arial', 25, weight= 250))
        self.label_M1.setAlignment(Qt.AlignCenter)
    
        # -------------- 
        self.label_M2 = QLabel(self,text='O')
        self.label_M2.setFont(QFont('Arial', 25, weight= 250))
        self.label_M2.setAlignment(Qt.AlignCenter)
        # -------------------------
        self.label_M3 = QLabel(self,text='R')
        self.label_M3.setFont(QFont('Arial', 25, weight= 250))
        self.label_M3.setAlignment(Qt.AlignCenter)
        # -------------------------
        self.label_M4 = QLabel(self,text='A')
        self.label_M4.setFont(QFont('Arial', 25, weight= 250))
        self.label_M4.setAlignment(Qt.AlignCenter)
        # -----------------------
        self.label_M5 = QLabel(self,text='B')
        self.label_M5.setFont(QFont('Arial', 25, weight= 250))
        self.label_M5.setAlignment(Qt.AlignCenter)
        # ------------------------
        self.label_M6 = QLabel(self,text='A')
        self.label_M6.setFont(QFont('Arial', 25, weight= 250))
        self.label_M6.setAlignment(Qt.AlignCenter)
        # -------------------------
        self.label_M7 = QLabel(self,text='R')
        self.label_M7.setFont(QFont('Arial', 25, weight= 250))
        self.label_M7.setAlignment(Qt.AlignCenter)
        # -------------------------
        self.label_M8 = QLabel(self,text='A')
        self.label_M8.setFont(QFont('Arial', 25, weight= 250))
        self.label_M8.setAlignment(Qt.AlignCenter)
        # -------------------------
        self.label_M9 = QLabel(self,text='B')
        self.label_M9.setFont(QFont('Arial', 25, weight= 250))
        self.label_M9.setAlignment(Qt.AlignCenter)
        # -------------------------
        self.label_M10 = QLabel(self,text='A')
        self.label_M10.setFont(QFont('Arial', 25, weight= 250))
        self.label_M10.setAlignment(Qt.AlignCenter)
        # ------------------


        self.Picture = QPixmap('data/logo.png')
        self.label_pic = QLabel(self)

        self.label_pic.setPixmap(self.Picture)

        self.background = QLabel(self)
        bg = QPixmap('data/background.png')
        self.background.setPixmap(bg)

        # Connect the widgets
        self.run_button.clicked.connect(self.run_command)
        self.start_button.clicked.connect(self.start_function)
        self.input_widget.returnPressed.connect(self.run_command)

        # Create the layout
        hbox = QHBoxLayout()
        # hbox.setStyleSheet("background-image: url('data/background.png'); background-repeat: no-repeat; background-position: center;")
        self.vbox_right = QVBoxLayout()
        self.vbox_left = QVBoxLayout()
        self.vbox_left.addWidget(self.output_widget)
        self.vbox_left.addWidget(self.input_widget)
        self.vbox_left.addWidget(self.run_button)
        self.vbox_right.addWidget(self.label_pic)
        self.vbox_right.addWidget(self.label_M1)
        self.vbox_right.addWidget(self.label_M2)
        self.vbox_right.addWidget(self.label_M3)
        self.vbox_right.addWidget(self.label_M4)
        self.vbox_right.addWidget(self.label_M5)
        self.vbox_right.addWidget(self.label_M6)
        self.vbox_right.addWidget(self.label_M7)
        self.vbox_right.addWidget(self.label_M8)
        self.vbox_right.addWidget(self.label_M9)
        self.vbox_right.addWidget(self.label_M10)
        # self.vbox_right.addWidget(spacer)

        self.vbox_right.addWidget(self.start_button)

        hbox.addLayout(self.vbox_left)
        hbox.addLayout(self.vbox_right)

        # Create the central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(hbox)
        self.setCentralWidget(central_widget)

        # Create the command process and connect its outputChanged signal
        self.cmd_process = CmdProcess(self)
        self.cmd_process.outputChanged.connect(self.handle_output)

        # Start the command process
        self.cmd_process.start()

    def change_color(self):
        self.label_M1.setStyleSheet("color: {}".format(self.colors[self.current_color].name()))
        self.current_color = (self.current_color + 1) % len(self.colors)
        
        self.label_M2.setStyleSheet("color: {}".format(self.colors[self.current_color].name()))
        self.current_color = (self.current_color + 1) % len(self.colors)
        
        self.label_M3.setStyleSheet("color: {}".format(self.colors[self.current_color].name()))
        self.current_color = (self.current_color + 1) % len(self.colors)
        
        self.label_M4.setStyleSheet("color: {}".format(self.colors[self.current_color].name()))
        self.current_color = (self.current_color + 1) % len(self.colors)
        
        self.label_M5.setStyleSheet("color: {}".format(self.colors[self.current_color].name()))
        self.current_color = (self.current_color + 1) % len(self.colors)
        
        self.label_M6.setStyleSheet("color: {}".format(self.colors[self.current_color].name()))
        self.current_color = (self.current_color + 1) % len(self.colors)
        
        self.label_M7.setStyleSheet("color: {}".format(self.colors[self.current_color].name()))
        self.current_color = (self.current_color + 1) % len(self.colors)
        
        self.label_M8.setStyleSheet("color: {}".format(self.colors[self.current_color].name()))
        self.current_color = (self.current_color + 1) % len(self.colors)
        
        self.label_M9.setStyleSheet("color: {}".format(self.colors[self.current_color].name()))
        self.current_color = (self.current_color + 1) % len(self.colors)
        
        self.label_M10.setStyleSheet("color: {}".format(self.colors[self.current_color].name()))
        self.current_color = (self.current_color + 1) % len(self.colors)
        
    def start_function(self):
        command = 'python client.py' + '\n'
        self.cmd_process.write(command)

    def run_command(self):
        # Get the command from the input widget and write it to the command process
        command = self.input_widget.text() + '\n'
        self.cmd_process.write(command)

        # Clear the input widget
        self.input_widget.clear()

    def handle_output(self, output):
        # Append the output to the output widget
        self.output_widget.insertPlainText(output)
        self.output_widget.ensureCursorVisible()

app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())
