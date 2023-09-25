from textblob import TextBlob


class SadRobot:
    def __init__(self):
        self.happiness = 0

    def analyze_sentiment(self, text):
        blob = TextBlob(text)
        return blob.sentiment.polarity

    def increase_happiness(self, sentiment):
        if sentiment > 0:
            self.happiness += 1

    def generate_response(self, sentiment):
        if sentiment > 0:
            return "Thank you for being positive!"
        elif sentiment < 0:
            return "That's not very positive..."
        else:
            return "I feel neutral about that."

    def interact(self, user_input):
        sentiment = self.analyze_sentiment(user_input)
        self.increase_happiness(sentiment)
        response = self.generate_response(sentiment)
        return response


def main():
    sad_robot = SadRobot()
    print("Welcome to the Sad Robot Game!")
    print("Type 'exit' to end the game.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        response = sad_robot.interact(user_input)
        print(f"Sad Robot: {response}")
        print(f"Sad Robot Happiness Level: {sad_robot.happiness}")


if __name__ == "__main__":
    main()

