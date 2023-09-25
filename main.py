from textblob import TextBlob


class SadRobot:
    def __init__(self):
        self.happiness = 0

    def analyze_sentiment(self, text):
        blob = TextBlob(text)
        return blob.sentiment.polarity

    def calculate_happiness(self, sentiment):
        if sentiment > 0:
            return 20
        elif sentiment < 0:
            return -20
        else:
            return 10

    def increase_happiness(self, sentiment):
        if sentiment > 0:
            self.happiness += 1

    def generate_response(self, sentiment):
        if sentiment > 0:
            return "Thank you for the positivity. It really helps my day!"
        elif sentiment < 0:
            return "I guess you are also in a bad situation. I am sorry If I am disturbing you ..."
        else:
            return "I feel that way as well."

    def interact(self, user_input):
        sentiment = self.analyze_sentiment(user_input)
        self.happiness += self.calculate_happiness(sentiment)
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
        if sad_robot.happiness >= 100:
            print("Congratulations! You have made the Sad Robot happy!")
            play_again = input("Do you want to play again? (yes/no): ")
            if play_again.lower() == 'yes':
                sad_robot.happiness = 0  # reset the points
                print("Let's play again!")
                print("Type 'exit' to end the game.")
            else:
                print("Goodbye!")
                break


if __name__ == "__main__":
    main()

