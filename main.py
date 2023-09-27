from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QTextEdit, QLineEdit, QPushButton
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

    def generate_response(self, sentiment):
        if sentiment > 0:
            return "Thank you for the positivity. It really helps my day!"
        elif sentiment < 0:
            return "I guess you are also in a bad situation. I am sorry If I am disturbing you ..."
        else:
            return "I feel that way as well."


class SadRobotGUI(QWidget):
    def __init__(self, sad_robot):
        super().__init__()
        self.sad_robot = sad_robot
        layout = QVBoxLayout()
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)
        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("Type your text here...")
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
            self.output.append(f"Sad Robot: {response}")
            self.output.append(f"Sad Robot Happiness Level: {self.sad_robot.happiness}")
            self.sad_robot.speak(f"Sad Robot: {response}")
            self.input_line.clear()


def main():
    app = QApplication(sys.argv)
    sad_robot = SadRobot()
    gui = SadRobotGUI(sad_robot)
    gui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()


