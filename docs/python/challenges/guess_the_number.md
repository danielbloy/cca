# Guess the Number

## Challenge

Your aim is to follow the steps and use the hints to create a text-based game where the player must
try and guess a number between 1 and 10 that is randomly chosen by the computer, in as few
guesses as possible. Test your game each time you make a change by running it.

Page numbers are provided for the book [Python in easy steps](https://www.amazon.co.uk/Python-easy-steps-2nd-covers/dp/1840788127) (PIES) by Mike McGrath

## Steps

1. Output a welcome message to the player to guess a number between 1 and 10.

    Use the `print()` function. PIES: Pages 16 to 17.

1. Randomly generate an integer number between 1 and 10.

    Use the `random.random()` and `int()` functions. PIES: Pages 170 to 171.

    Alternatively, use Google to find out about the `random.randint()` function.

1. Let the players make a single guess.

    Get the players guess with the `input()` function and save it to a variable. PIES: Pages 18 to 21.

    Convert the players guess to a number using the `int()` function. PIES: Page 170.

    Compare to the random number to the players guess and inform them if the number is too high, 
too low, or correct using the `if` statement and `>` and `<` operators. PIES: Pages 52, 53 and 30, 31.

1. Count how many guesses the player takes to guess correctly.

    Use a variable to track the number of guesses made. PIES: Pages 18 and 19.

    Use a while loop to allow the player to guess until correct. PIES: Pages 54 to 55.

1. Ask the player if they want to play again?

    Extract out your main game look into a function using `def`. PIES: Pages 62 to 63.

    Make your new function return the number of guesses made. PIES: Pages 66 to 67.

    Ask the player if they want to play another game by entering Y or N; use the `input()` function.

    PIES: Pages 18 to 21.

1. Track the fewest guesses to guess correctly.

    Use a variable to keep track of the fewest guesses made so far.

    Congratulate the player if they play a game and require fewer guesses than the previous best.

1. Ask the player what the upper limit for the game should be rather than 10.

    Presently your game asks the player to guess a number from 1 to 10. Adjust your game so it first asks the player what the upper limit should be so that they can play a harder or easier game.

Once you've done this, how many guesses does it take you to guess a random number from 1 to 100? How about 1 to 1,000?

## Solution

Download a sample solution [here](../../img/python/challenges/guess_the_number.py).

## PDF

Download this challenge as a [PDF file](../../img/python/challenges/2%20-%20Higher%20or%20Lower.pdf).
