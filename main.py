from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QTextEdit, QLineEdit, QPushButton, QDialog, QLabel, \
    QHBoxLayout
from textblob import TextBlob
import pyttsx3
import sys


class SadRobot:
    def __init__(self):
        self.happiness = 0
        self.engine = pyttsx3.init()
        self.set_voice_and_rate()

    def set_voice_and_rate(self):
        voices = self.engine.getProperty('voices')
        voice_index = 1
        self.engine.setProperty('voice', voices[voice_index].id)
        rate = self.engine.getProperty('rate')
        self.engine.setProperty('rate', rate - 50)

    def analyze_sentiment(self, text):
        blob = TextBlob(text)
        return blob.sentiment.polarity

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def calculate_happiness(self, sentiment):
        if sentiment > 0:
            return 20
        elif sentiment < 0:
            return -20
        else:
            return 10

    def interact(self, user_input):
        sentiment = self.analyze_sentiment(user_input)
        self.happiness += self.calculate_happiness(sentiment)
        response = self.generate_response(sentiment)
        return response

    def check_game_status(self):
        if self.happiness <= -30:
            return "You Lost"
        elif self.happiness >= 100:
            return "You Won!"
        return "continue"

    def generate_response(self, sentiment):
        if sentiment > 0:
            return "Thank you for the positivity. It really helps my day!"
        elif sentiment < 0:
            return "I guess you are also in a bad situation. I am sorry If I am disturbing you ..."
        else:
            return "I feel that way as well."


class OpeningScreen(QDialog):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel(self)
        pixmap = QPixmap("sad robot one.png")  # set the path to your image file
        label.setPixmap(pixmap)
        layout.addWidget(label)

        button_layout = QHBoxLayout()
        play_button = QPushButton("Play", self)
        play_button.clicked.connect(self.accept)
        exit_button = QPushButton("Exit", self)
        exit_button.clicked.connect(self.reject)
        button_layout.addWidget(play_button)
        button_layout.addWidget(exit_button)
        layout.addLayout(button_layout)
        self.setLayout(layout)


class GameResultScreen(QDialog):  # Base class to handle common elements
    def __init__(self, title):
        super().__init__()
        layout = QVBoxLayout()

        # Displaying title (You Won / You Lost)
        self.title_label = QLabel(title, self)
        layout.addWidget(self.title_label)

        # Image for win/lose will be set in derived classes

        # Play Again and Exit buttons
        button_layout = QHBoxLayout()

        play_again_button = QPushButton("Play Again", self)
        play_again_button.clicked.connect(self.play_again)
        button_layout.addWidget(play_again_button)

        exit_button = QPushButton("Exit", self)
        exit_button.clicked.connect(self.exit_game)
        button_layout.addWidget(exit_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def play_again(self):
        self.accept()

    def exit_game(self):
        self.reject()


class WinningScreen(GameResultScreen):
    def __init__(self):
        super().__init__("Congratulations! You Won!")
        label = QLabel(self)
        pixmap = QPixmap("robot happy.png")
        label.setPixmap(pixmap)
        self.layout().insertWidget(1, label)


class LosingScreen(GameResultScreen):
    def __init__(self):
        super().__init__("Game Over: You Lost!")
        label = QLabel(self)
        pixmap = QPixmap("sad robot 3.png")
        label.setPixmap(pixmap)
        self.layout().insertWidget(1, label)


class SadRobotGUI(QWidget):
    def __init__(self, sad_robot):
        super().__init__()
        self.sad_robot = sad_robot
        layout = QVBoxLayout()

        # Score (Happiness Level) Label
        self.score_label = QLabel(f"Happiness Level: {self.sad_robot.happiness}", self)
        layout.addWidget(self.score_label)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)
        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("Type your text here...")
        self.input_line.returnPressed.connect(self.handle_send)  # Connecting to returnPressed (ENTER button)
        layout.addWidget(self.input_line)
        send_button = QPushButton("Send")
        send_button.clicked.connect(self.handle_send)
        layout.addWidget(send_button)
        self.setLayout(layout)

    def handle_send(self):
        user_input = self.input_line.text()
        if user_input:
            response = self.sad_robot.interact(user_input)
            self.output.append(f"You: {user_input}")
            self.output.append(f"Robot says: {response}")
            self.score_label.setText(f"Happiness Level: {self.sad_robot.happiness}")

            game_status = self.sad_robot.check_game_status()
            if game_status == "You Lost":
                self.lost_game()
            elif game_status == "You Won":
                self.won_game()
            self.sad_robot.speak(response)
            self.input_line.clear()

    def lost_game(self):
        self.close()  # Close main window
        lose_screen = LosingScreen()
        response = lose_screen.exec()
        if response == QDialog.DialogCode.Accepted:
            self.restart_game()

    def won_game(self):
        self.close()  # Close main window
        win_screen = WinningScreen()
        response = win_screen.exec()
        if response == QDialog.DialogCode.Accepted:
            self.restart_game()

    def restart_game(self):
        self.sad_robot = SadRobot()  # Reset the game state
        self.__init__(self.sad_robot)  # Reinitialize the GUI
        self.show()



def main():
    app = QApplication(sys.argv)
    opening_screen = OpeningScreen()
    response = opening_screen.exec()
    if response == QDialog.DialogCode.Accepted:
        sad_robot = SadRobot()
        gui = SadRobotGUI(sad_robot)
        gui.show()
        sys.exit(app.exec())
    else:
        sys.exit()


if __name__ == "__main__":
    main()


