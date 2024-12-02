# Pairs

TODO: Game summary

## Create the project in Replit

Navigate to [Replit](https://replit.com/) and login.

Create a new project using the Pygame template and give it the title "Pairs" as
illustrated by the screenshot below.

![screen shot](../../img/python/pygame/pairs/create-project.png)

In the `main.py` file, replace the code provided with the code below and run the program
to make sure it can download the packages and runs. You should be presented with a black screen
with a red zero for the score at the top of the screen.

```python
import time
import pgzrun
import types

WIDTH = 640
HEIGHT = 700

score = 0
paused = False

def draw():
    screen.clear()
    screen.draw.text(f"{score}", (WIDTH / 2, 15), color="red", fontsize=24)
    
pgzrun.go()
```
