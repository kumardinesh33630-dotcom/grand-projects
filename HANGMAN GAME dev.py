import random


WORDS = [
    "python",
    "programming",
    "computer",
    "developer",
    "keyboard",
    "internet",
]


def play_hangman():
    word = random.choice(WORDS)
    guessed_letters = set()
    incorrect_guesses = 0
    max_incorrect_guesses = 6

    print("Welcome to Hangman!")

    while incorrect_guesses < max_incorrect_guesses:
        display = " ".join(
            letter if letter in guessed_letters else "_" for letter in word
        )
        print(f"\nWord: {display}")
        print(f"Incorrect guesses remaining: {max_incorrect_guesses - incorrect_guesses}")

        if all(letter in guessed_letters for letter in word):
            print(f"You won! The word was '{word}'.")
            return

        guess = input("Guess a letter: ").lower().strip()

        if len(guess) != 1 or not guess.isalpha():
            print("Please enter one letter.")
        elif guess in guessed_letters:
            print("You already guessed that letter.")
        else:
            guessed_letters.add(guess)
            if guess in word:
                print("Correct!")
            else:
                incorrect_guesses += 1
                print("Incorrect!")

    print(f"\nYou lost! The word was '{word}'.")


if __name__ == "__main__":
    play_hangman()
