import random

print("Welcome to a game of higher/lower. The computer will generate 10 random")
print("numbers between 1 and 50. You will be shown the first random number and")
print("asked to guess whether the next random number is higher or lower. You will")
print("then be shown the number. If you are correct, you move on to try and guess")
print("higher or lower for the next number. No two adjacent numbers will be the")
print("same. You goal is to guess correctly as many times as possible.")
print()

# Step 2: Generate 10 random integer numbers between 1 and 50.
numbers = []
lastNumber = -1
while len(numbers) < 10:
    number = random.randint(1, 50)
    if number != lastNumber:
        lastNumber = number
        numbers.append(number)


def print_board(guess):
    for i in range(guess):
        print("%d " % (numbers[i]), end="")
    print("%d " % (numbers[guess]))


# Step 3: Present the user the first number and ask them for higher or lower.
print("Your starting number is %d" % (numbers[0]))

# Step 4: Compare the actual value against the players decision.
guess = 0

# Step 5: Cycle through until the player guesses incorrectly or gets to the end.
while guess < len(numbers):
    guess += 1
    higher = False
    lower = False
    while True:
        horl = input("Guess higher or lower (H/L): ").upper()
        if horl == 'H':
            higher = True
            lower = False
            break
        elif horl == 'L':
            lower = True
            higher = False
            break

    if higher and numbers[guess] > numbers[guess - 1]:
        print("Correct, the number %d is higher than %d!" % (numbers[guess], numbers[guess - 1]))

    elif lower and numbers[guess] < numbers[guess - 1]:
        print("Correct, the number %d is lower than %d!" % (numbers[guess], numbers[guess - 1]))

    elif higher and numbers[guess] < numbers[guess - 1]:
        print("Incorrect, the number %d is lower than %d!" % (numbers[guess], numbers[guess - 1]))
        break

    else:
        print("Incorrect, the number %d is higher than %d!" % (numbers[guess], numbers[guess - 1]))
        break

    print_board(guess)
    print("The current number is %d" % (numbers[guess]))

# Step 6: Show the player the full set of random numbers.
if guess == len(numbers):
    print("You guessed all of the numbers correctly!")
else:
    print("You guessed correct %d out of %d times" % (guess - 1, len(numbers) - 1))

print_board(len(numbers) - 1)
