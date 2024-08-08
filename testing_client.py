import sys
import threading
import socket
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QWidget, QLabel, QLineEdit
from PyQt6.QtCore import QTimer
from datetime import datetime


class Client(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize the GUI
        self.init_ui()

        # Initialize socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(("127.0.0.1", 5000))
        self.ip = socket.gethostbyname(socket.gethostname())

        # Start receiving thread
        self.receiving_thread = threading.Thread(target=self.receive_messages)
        self.receiving_thread.start()

        # Timer for periodic update
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(1000)

    def init_ui(self):
        # Setup UI components
        self.setWindowTitle("Client GUI")
        self.setGeometry(100, 100, 600, 400)

        self.label = QLabel("Connection Successful! Please enter the message:", self)
        self.text_field = QLineEdit(self)
        self.text_area = QTextEdit(self)
        self.text_area.setReadOnly(True)

        self.send_button = QPushButton("Send", self)
        self.quit_button = QPushButton("Quit", self)

        self.send_button.clicked.connect(self.send_message)
        self.quit_button.clicked.connect(self.quit_application)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.text_field)
        layout.addWidget(self.send_button)
        layout.addWidget(self.text_area)
        layout.addWidget(self.quit_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def send_message(self):
        message = self.text_field.text()
        self.text_field.clear()

        if message:
            self.socket.sendall(message.encode('utf-8'))
            time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.text_area.append(f"{time_now} [{self.ip}] Me: {message}")

    def receive_messages(self):
        while True:
            try:
                data = self.socket.recv(1024)
                if data:
                    message = data.decode('utf-8')
                    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.text_area.append(f"{time_now} [{self.ip}] Server: {message}")
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    def update_ui(self):
        # Optional: update UI periodically if needed
        pass

    def quit_application(self):
        self.socket.close()
        self.save_log()
        self.close()

    def save_log(self):
        with open("client_log.txt", "a") as log_file:
            log_file.write(self.text_area.toPlainText())
        print("Log saved successfully.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    client = Client()
    client.show()
    sys.exit(app.exec())
