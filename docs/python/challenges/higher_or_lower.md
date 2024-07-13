# Higher or lower

## Challenge

Your aim is to follow the steps and use the hints to create a text-based game where the computer
generates 10 random numbers between 1 and 50. The player is shown the first number and must
then guess if the next number is higher or lower. If the player guesses correctly, they then try to
guess if the next number is higher or lower. This continues until the player guesses correctly 9 times
or guesses incorrectly. Test your game each time you make a change by running it.

Page numbers are provided for the book [Python in easy steps](https://www.amazon.co.uk/Python-easy-steps-2nd-covers/dp/1840788127) (PIES) by Mike McGrath

## Steps

1. Output a message to the player informing them of the instructions for the game.

    Use the `print()` function. PIES: Pages 16 to 17.

2. Randomly generate 10 integers between 1 and 50 and add them to a list variable. Make sure that no two consecutive numbers are the same.

    Use a variable to record the list of numbers generated. PIES: Pages 18 to 19 and 44 to 47.

    Use the `random.random()` and `int()` functions. PIES: Pages 170 to 171.

    Alternatively, use Google to find out about the `random.randint()` function.

    Use an `if` statement and the inequality operator (`!=`) to ensure consecutive numbers have different values. PIES: Pages 52 to 53 and 30.

3. Show the user the first number and ask them for higher or lower. The player should enter 'h' or 'H' for higher and 'l' or 'L' for lower. Keep prompting until the user enters the correct value.

    Get the players guess with the `input()` function and save it to a variable. PIES: Pages 18 to 21.

    Use a while loop to ask for input until a correct value is supplied. PIES: Pages 54 to 55.

4. Compare the next value against the players decision and let them know if they were correct.

    Use the `if` and `elif` statements and `>` and `<` operators. PIES: Pages 52 to 53 and 30 to 31.

    You will need to index into the list using the `[` and `]` characters. PIES: Pages 44 to 45.

5. Allow the player to keep guessing until they guess incorrectly or get to the end. Keep track of how many guesses the player makes.

    Use a variable to track the number of guesses made. PIES: Pages 18 to 19.

    Use a `while` loop to allow the player to guess until correct. PIES: Pages 54 to 55.

    Use `break` to exit the loop early. PIES: Pages 58 to 59.

6. Once the game has ended, show the player the full set of random numbers.

7. Ask the player if they want to play again? If they answer yes, then let them have another go.

8. Keep track of the largest number of successful guesses and let the player know if they exceed it.

Once you've completed your game, how many correct guesses can you get in a row?

## Solution

Download a sample solution [here](../../img/python/challenges/higher_or_lower.py).

## PDF

Download this challenge as a [PDF file](../../img/python/challenges/2%20-%20Higher%20or%20Lower.pdf).
