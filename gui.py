import sys
from PyQt5.QtWidgets import QLabel,QApplication, QMainWindow, QPlainTextEdit, QVBoxLayout, QWidget, QPushButton, QLineEdit, QHBoxLayout
from PyQt5.QtCore import QProcess, pyqtSignal, QObject
from PyQt5.QtGui import QPixmap

class CmdProcess(QObject):
    outputChanged = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Create the process object and connect its signals
        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.handle_stdout)

    def start(self):
        # Start the process with cmd.exe on Windows or bash on Linux/Mac
        if sys.platform.startswith('win'):
            self.process.start('cmd.exe')
        else:
            self.process.start('bash')

    def write(self, command):
        # Write a command to the process
        self.process.write(command.encode())

    def handle_stdout(self):
        # Emit the outputChanged signal with the process's output
        output = self.process.readAllStandardOutput().data().decode()
        self.outputChanged.emit(output)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setFixedSize(1024, 720)
        self.setWindowTitle("Morabaraba")
        # self.setStyleSheet("background-image: url('data\background.png'); background-repeat: no-repeat; background-position: center;") # تنظیم سبک برای ویجت
        # Create the widgets
        self.output_widget = QPlainTextEdit(self)
        self.input_widget = QLineEdit(self)
        self.run_button = QPushButton('Run', self)
        self.start_button = QPushButton('Start', self)
        self.label_welcome = QLabel(self,text='Welcome to the Morabaraba')
        self.label_turn = QLabel(self,text='Trun of player : ')
        self.label_mark_player1 = QLabel(self,text='Mark of player 1 :')
        self.label_mark_player2 = QLabel(self,text='Mark of player 2 :')
        self.Picture = QPixmap('data/logo.png')
        self.label_pic = QLabel(self)

        self.label_pic.setPixmap(self.Picture)

        self.background = QLabel(self)
        bg = QPixmap('data/background.png')
        self.background.setPixmap(bg)
        # self.setCentralWidget(self.background)

        spacer = QWidget()
        spacer.setFixedSize(20, 300)

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
        self.vbox_right.addWidget(self.label_welcome)
        self.vbox_right.addWidget(spacer)

        self.vbox_right.addWidget(self.start_button)
        self.vbox_right.addWidget(self.label_turn)
        self.vbox_right.addWidget(self.label_mark_player1)
        self.vbox_right.addWidget(self.label_mark_player2)
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
