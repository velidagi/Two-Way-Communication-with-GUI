import sys
import threading
import socket
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QWidget, QLabel, QLineEdit
from PyQt6.QtCore import QTimer, pyqtSignal, QObject
from datetime import datetime

class WorkerSignals(QObject):
    # Define signal to pass messages to the main thread
    message_received = pyqtSignal(str)

class Server(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize the GUI
        self.init_ui()

        # Initialize socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("0.0.0.0", 5000))
        self.server_socket.listen(1)
        print("Server started")
        print("Waiting for a client ...")
        self.client_socket, self.client_address = self.server_socket.accept()
        print(f"Client accepted: {self.client_address}")
        self.ip = self.client_address[0]

        # Setup signals
        self.signals = WorkerSignals()
        self.signals.message_received.connect(self.display_message)

        # Start receiving thread
        self.receiving_thread = threading.Thread(target=self.receive_messages)
        self.receiving_thread.start()

    def init_ui(self):
        # Setup UI components
        self.setWindowTitle("Server GUI")
        self.setGeometry(100, 100, 600, 400)

        self.label_s = QLabel("Connection Successful to Client! Please enter the message:", self)
        self.input_text_server = QLineEdit(self)
        self.text_area = QTextEdit(self)
        self.text_area.setReadOnly(True)

        self.send_button = QPushButton("Send", self)
        self.quit_button = QPushButton("Quit", self)

        self.send_button.clicked.connect(self.send_message)
        self.quit_button.clicked.connect(self.quit_application)

        layout = QVBoxLayout()
        layout.addWidget(self.label_s)
        layout.addWidget(self.input_text_server)
        layout.addWidget(self.send_button)
        layout.addWidget(self.text_area)
        layout.addWidget(self.quit_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Timer for periodic update (if needed)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(1000)

    def send_message(self):
        message = self.input_text_server.text()
        self.input_text_server.clear()

        if message:
            self.client_socket.sendall(message.encode('utf-8'))
            time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.text_area.append(f"{time_now} [{self.ip}] Me: {message}")

    def receive_messages(self):
        while True:
            try:
                data = self.client_socket.recv(1024).decode('utf-8')
                if data:
                    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    formatted_message = f"{time_now} [{self.ip}] Client: {data}"
                    self.signals.message_received.emit(formatted_message)
            except Exception as e:
                print(f"Error receiving message: {e}")
                self.quit_application()
                break

    def display_message(self, message):
        self.text_area.append(message)

    def update_ui(self):
        # Optional: update UI periodically if needed
        pass

    def quit_application(self):
        self.server_socket.close()
        self.client_socket.close()
        self.save_log()
        self.close()

    def save_log(self):
        with open("server_log.txt", "a") as log_file:
            log_file.write(self.text_area.toPlainText())
        print("Log saved successfully.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    server = Server()
    server.show()
    sys.exit(app.exec())
