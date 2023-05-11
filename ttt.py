import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPlainTextEdit, QVBoxLayout, QWidget, QPushButton, QLineEdit
from PyQt5.QtCore import QProcess, pyqtSignal, QObject

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

    def run_command(self, command):
        # Run a command using subprocess and write its output to the process
        result = subprocess.run(command.split(), stdout=subprocess.PIPE)
        output = result.stdout.decode()
        self.process.write(output.encode())

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setFixedSize(1024, 720)
        self.setWindowTitle("Morabaraba")
        # Create the widgets
        self.output_widget = QPlainTextEdit(self)
        self.input_widget = QLineEdit(self)
        self.run_button = QPushButton('Run', self)

        # Connect the widgets
        self.run_button.clicked.connect(self.run_command)
        self.input_widget.returnPressed.connect(self.run_command)

        # Create the layout
        vbox = QVBoxLayout()
        vbox.addWidget(self.output_widget)
        vbox.addWidget(self.input_widget)
        vbox.addWidget(self.run_button)

        # Create the central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(vbox)
        self.setCentralWidget(central_widget)

        # Create the command process and connect its outputChanged signal
        self.cmd_process = CmdProcess(self)
        self.cmd_process.outputChanged.connect(self.handle_output)

        # Start the command process
        self.cmd_process.start()

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
