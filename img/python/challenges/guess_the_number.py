import random

# Step 1: Output a welcome message to guess a number between 1 and 10.
print("Welcome to guess. Try to guess the number chosen by the computer")
print("in as few guesses as possible.")
print()


def play():
    print("Guess a number between 1 and 10.")

    # Step 2: Randomly generate a number between 1 and 10.
    number = random.randint(1, 10)
    print(f"Random number: {number}")

    # Step 3: Get the players input and compare to the number to guess.
    # Inform the player if the number is too high or low (or correct).
    guess = 0
    guesses = 0
    while guess != number:
        print("Enter your guess: ")

        guess = int(input())
        guesses += 1

        if guess > number:
            print("Your guess was too high")
        elif guess < number:
            print("Your guess was too low")

    # Step 4: Inform the player how many guesses it took them.
    print(f"Correct, the number is {number}. It took you {guesses} guesses.")
    return guesses


fewest = 10000
playing = True
while playing:
    guesses = play()

    # Step 6: Keep track of the smallest number of guesses.
    if fewest == 10000:
        fewest = guesses

    if fewest > guesses:
        fewest = guesses
        print("Well done, you guessed correctly in the fewest number of guesses!")

    # Step 5: Ask the player if they want to play again?
    print("Would you like to play again (Y/N)?")
    again = input().upper()
    if again != "Y":
        playing = False

# Step 7: Ask the player what range should be used (rather than 1 to 10).
# Not implemented in this sample solution
