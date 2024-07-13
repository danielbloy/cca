# Muncher

These instructions will take you through the steps of creating a game that uses the
1980 game Pac-Man as its inspiration. In this version, the ghosts are not constrained
by walls so can float through them.

You will control Muncher, moving him around the screen to collect all the pellets whilst avoiding being caught by the ghosts.

Each a power pellet to supercharges Muncher and allows him to eat the ghosts.

When fruit appears, munch them for a big bonus.

Get a new life for each 10,000 points scored.

## Create the project in Replit

Navigate to [replit](https://replit.com/) and login.

Create a new project using the Pygame template and give it the title "Muncher" as illustrated
by the screenshot below.

![screen shot](/img/python/pygame/muncher/create-project.png)

In the `main.py` file, replace the code provided with the template with this and run the program
to make sure it can download the packages and runs. You should be presented with a black screen
with a red zero for the score at the top of the screen.

```python
import time
import pgzrun

WIDTH = 640
HEIGHT = 800

score = 0
lives = 3
paused = False

def draw():
    screen.clear()
    screen.draw.text(f"{score}", (WIDTH / 2, 15), color="red", fontsize=24)
    
pgzrun.go()
```

## Introducing Muncher

Our protagonist is called Muncher and is a yellow round ball that likes to eat little yellow
pellets. Muncher will be comtrolled by the player and can be moved around the screen using the
cursor keys. Muncher will be 32 x 32 pixels in size and will be animated. Therefore you will
need at least 2 images for Muncher. You can create your own images using a paint program that
supports transparency (all the images provided here were created using [PixilArt](https://www.pixilart.com/draw)) or you can use my images that are provided below.

The two images should be called `muncher.png` and `muncher2.png`. Create a `images` folder in
your project and place your files in there as illustrated in the screenshot below.

![screen shot](/img/python/pygame/muncher/muncher.png) ![screen shot](/img/python/pygame/muncher/muncher2.png)

![screen shot](/img/python/pygame/muncher/create-images-folder.png)

Then add the following code before the `draw()` function:

```python
MUNCHER_START_X = WIDTH / 2
MUNCHER_START_Y = (HEIGHT / 4) * 3
muncher = Actor('muncher', (MUNCHER_START_X, MUNCHER_START_Y))
muncher.images = ['muncher', 'muncher2']
muncher.vx = 150
muncher.vy = 150
```

Then change the `draw()` function to read as follows to ensure Muncher gets
drawn each frame:

```python
def draw():
    screen.clear()
    screen.draw.text(f"{score}", (WIDTH / 2, 15), color="red", fontsize=24)

    muncher.draw()
```

To add movement for Muncher, add an `update()` function after the `draw()` function. The
`update()` function will move Muncher up, down, left or right at the correct speed (using
Munchers horixontal and vertical velocity properties in pixels per second multiplied by the
proportion of seconds that have passed since the last update):

```python
def update(dt):
    if keyboard.left:
        muncher.x -= muncher.vx * dt
    if keyboard.right:
        muncher.x += muncher.vx * dt
    if keyboard.up:
        muncher.y -= muncher.vy * dt
    if keyboard.down:
        muncher.y += muncher.vy * dt
```

Try out your game. You should be able to move Muncher around the screen.

### Experiment: Changing the speed of Muncher

The speed of Muncher is controlled by the `vx` and `vy` properties that represent the horizontal
and vertical speed that Muncher can move in pixels per second. These are currently set to `150`
each in your code. Try experimenting with different values to see what effect this has. Example
values to try are:

* 300
* 50
* 0
* -150

## Keeping Actors within the screen

What happens when Muncher gets close to the edges of the screen? Does he stop or keep going so
he goes outside the bounds of the screen?

During the game, we want Muncher to stay within the play area. We are therefore going to need to
to set some boundaries that we want to keep all Actors (Ghosts and Muncher) within. This boundary
will be set to a border of 50 pixels. We will add a `keep_in_bounds()` method to the `Actor`
class which we can call in each `update()` call. Add the following code above your `draw()`
function:

```python
BOUNDS_X1 = 50
BOUNDS_Y1 = 50
BOUNDS_X2 = WIDTH - BOUNDS_X1
BOUNDS_Y2 = HEIGHT - BOUNDS_Y1

def keep_in_bounds(actor):
    if actor.x < BOUNDS_X1:
        actor.x = BOUNDS_X1
    elif actor.x > BOUNDS_X2:
        actor.x = BOUNDS_X2

    if actor.y < BOUNDS_Y1:
        actor.y = BOUNDS_Y1
    elif actor.y > BOUNDS_Y2:
        actor.y = BOUNDS_Y2


Actor.keep_in_bounds = keep_in_bounds
```

Then add `muncher.keep_in_bounds()` to the end of your `update()` function so it reads as follows:

```python
def update(dt):
    if keyboard.left:
        muncher.x -= muncher.vx * dt
    if keyboard.right:
        muncher.x += muncher.vx * dt
    if keyboard.up:
        muncher.y -= muncher.vy * dt
    if keyboard.down:
        muncher.y += muncher.vy * dt

    muncher.keep_in_bounds()
```

Try out your game. You should be able to move Muncher around the screen but cannot go outside the bounds.

### Experiment: Changing the bounds

The variables `BOUNDS_X1` and `BOUNDS_Y1` set the width of the border around the screen.
Try using diffent values and see how it changes the playing area. Example values to try are:

* 0
* 250
* -50

## Animating Actors

We want all of our Actors to be animated. At present, as Muncher runs around the screen he looks a
little boring. In the code that creates the Muncher `Actor`, we set an `images` property that
contained the two images that we are going to use to animate Muncher.

Above your `draw()` function, add the following code which adds an `animate()` method to the `Actor`
class. This method first checks for the presence of some properties on the `Actor` instance and if
not present, provides some default values.

```python
def animate(actor):
    if not hasattr(actor, "images"):
        return
    if not hasattr(actor, "fps"):
        actor.fps = 5
    if not hasattr(actor, "next_frame"):
        actor.next_frame = time.time_ns()
    if not hasattr(actor, "frame"):
        actor.frame = 0

    now = time.time_ns()

    if now > actor.next_frame:
        actor.frame = (actor.frame + 1) % len(actor.images)
        actor.image = actor.images[actor.frame]
        while actor.next_frame < now:
            actor.next_frame += (1_000_000_000 / actor.fps)


Actor.animate = animate
```

Modify your `draw()` function to call the `animate()` method of Muncher. Your new `draw()`
function will look like this:

```python
def draw():
    screen.clear()
    screen.draw.text(f"{score}", (WIDTH / 2, 15), color="red", fontsize=24)

    muncher.animate()
    muncher.draw()
```

### Extension: More complex animations

If you want to make more elaborate or complex animations, you can add more images to
the `images` property of an Actor. For example, if you have an animation that spans
4 frames, you can change the `images` property of Muncher to read as follows:

```python
muncher.images = ['muncher', 'muncher2', 'muncher3', 'muncher4']
```

### Experiment: Animation speed

You can also adjust the speed with which Muncher is animated by providing a value
for the `fps` property on Muncher. By default, this will be set to 5 fps (Frames
Per Second). Try experimenting with different values by adding the following code
immediately after you set the `vx` and `vy` properties of Muncher:

```python
muncher.fps = 15
```

Try experimenting with different values. Examples to try are:

* 1
* 2
* 15

## Drawing lives

In this game, Muncher will start with 3 lives. We should add an indicator to the top of
the screen to indicate how many lives Muncher has. Modify your `draw()` function so that
it looks as follows:

```python
def draw():
    screen.clear()
    screen.draw.text(f"{score}", (WIDTH / 2, 15), color="red", fontsize=24)

    for i in range(lives):
        screen.blit('muncher', (5 + (37 * i), 5))
        
    muncher.animate()
    muncher.draw()
```

## Introducing the Ghosts

Muncher is antagonised by four ghosts, Blue, Orange, Red and Pink. Each of the ghosts will
be animated so will require at least 2 images. Just like Muncher, all of the ghost images
should be 32 x 32 pixels in size. You can create your own images using a paint program that
supports transparency (all the images provided here were created using [PixilArt](https://www.pixilart.com/draw)) or you can use my images that are provided below.

The two images should be placed in the `images` folder you already created and be called:

* `ghost-blue.png` ![screen shot](/img/python/pygame/muncher/ghost-blue.png)
* `ghost-blue2.png` ![screen shot](/img/python/pygame/muncher/ghost-blue2.png)
* `ghost-orange.png` ![screen shot](/img/python/pygame/muncher/ghost-orange.png)
* `ghost-orange2.png` ![screen shot](/img/python/pygame/muncher/ghost-orange2.png)
* `ghost-red.png` ![screen shot](/img/python/pygame/muncher/ghost-red.png)
* `ghost-red2.png` ![screen shot](/img/python/pygame/muncher/ghost-red2.png)
* `ghost-pink.png` ![screen shot](/img/python/pygame/muncher/ghost-pink.png)
* `ghost-pink2.png` ![screen shot](/img/python/pygame/muncher/ghost-pink2.png)

Add the following code before the `draw()` function which will create the ghosts
and give each one an individual speed and direction to start with but all will have
the same starting position:

```python
GHOST_START_X = WIDTH / 2
GHOST_START_Y = (HEIGHT / 3)
GHOST_START = (GHOST_START_X, GHOST_START_Y)

blue = Actor('ghost-blue', GHOST_START)
blue.images = ['ghost-blue', 'ghost-blue2']
blue.vx = -160
blue.vy = -160

orange = Actor('ghost-orange', GHOST_START)
orange.images = ['ghost-orange', 'ghost-orange2']
orange.vx = 260
orange.vy = 60

red = Actor('ghost-red', GHOST_START)
red.images = ['ghost-red', 'ghost-red2']
red.vx = 40
red.vy = 280

pink = Actor('ghost-pink', GHOST_START)
pink.images = ['ghost-pink', 'ghost-pink2']
pink.vx = 60
pink.vy = 60

ghosts = [blue, orange, red, pink]
```

Then change the `draw()` function to read as follows to ensure the Ghosts all get
animated and drawn each frame:

```python
def draw():
    screen.clear()
    screen.draw.text(f"{score}", (WIDTH / 2, 15), color="red", fontsize=24)

    for i in range(lives):
        screen.blit('muncher', (5 + (37 * i), 5))
        
    muncher.animate()
    muncher.draw()

    for ghost in ghosts:
        ghost.animate()
        ghost.draw()
```

Run your program and see what happens? do the ghosts move? Why do you think this is?

### Extension: More complex Ghost animations

Just as you can for Muncher, you can make more elaborate or complex animations for the
ghosts through using more animation frames by changing the `images` property of an Actor.
For example, if you have an animation that spans 5 frames that you want to use for the
blue ghost, you can change the `images` property of blue to read as follows:

```python
blue.images = ['ghost-blue', 'ghost-blue2', 'ghost-blue3', 'ghost-blue4', 'ghost-blue5']
```

## Moving the Ghosts

It looks like there is only a single ghost on the screen because they are all on top
of each other and there is no code that does movement for the ghosts yet. The technique
used for moving the ghosts is exactly the same as that for Muncher. We modify the ghosts
position by its `vx` and `vy` properties based on the elaspsed time since the ghost
was last moved.

Add the following code above your `draw()` function:

```python
def ghost_move(ghost, dt):
    ghost.x += ghost.vx * dt
    ghost.y += ghost.vy * dt


Actor.move = ghost_move
```

Then modify the `update` function so that it calls the `move()` method for each of the
Ghosts in turn.

```python
def update(dt):
    if keyboard.left:
        muncher.x -= muncher.vx * dt
    if keyboard.right:
        muncher.x += muncher.vx * dt
    if keyboard.up:
        muncher.y -= muncher.vy * dt
    if keyboard.down:
        muncher.y += muncher.vy * dt

    muncher.keep_in_bounds()

    for ghost in ghosts:
        ghost.move(dt)
```

Run your program and see what happens. Do the ghosts stay in the play area like Muncher does?
Why do you think this is? Can you fix it?

### Experiment: Changing the Ghosts speed and direction

Just as it is for Muncher, the speed of the ghosts is controlled by the `vx` and `vy` properties
that represent the horizontal and vertical speed each ghost can move in pixels per second.
Each ghost has a different set of values for the `vx` and `vy` properties. Experiment with changing
the values to see what effect it has.

## Keeping the Ghosts in bounds

The reason the ghosts all fly off the screen is because we do not perform the check to keep them
within the play area bounds like we do for Muncher. The code in the `update()` function is missing
a call to `ghost.keep_in_bounds()`.

Modify your `update()` function so that is is as follows:

```python
def update(dt):
    if keyboard.left:
        muncher.x -= muncher.vx * dt
    if keyboard.right:
        muncher.x += muncher.vx * dt
    if keyboard.up:
        muncher.y -= muncher.vy * dt
    if keyboard.down:
        muncher.y += muncher.vy * dt

    muncher.keep_in_bounds()

    for ghost in ghosts:
        ghost.move(dt)
        ghost.keep_in_bounds()
```

What happens why you run your game now? Why do you think this is? How do you think you could
go about fixing it?

### Experiment: Adding more Ghosts

The game uses an Python list to store all of the ghosts in the game. This means that we do
not need to do the movement and bounds checking for each ghost individually by their
variables names `pink`, `blue`, `orange` and `red` but can instead iterate over all of the
ghosts in a list and perform those operations. This is done in the `for ghost in ghosts:`
statement in the `update()` function. The advantage of this method is that we can add more
ghosts to the `ghosts` lists and they will automatically appear and move on the screen.

Try it. Create another ghost called `blue2` (which will use the same images as `blue`) and
add it to the `ghosts` lists. Run your game and check that it gets displayed and moves:

```python
blue2 = Actor('ghost-blue', GHOST_START)
blue2.images = ['ghost-blue', 'ghost-blue2']
blue2.vx = -10
blue2.vy = -60

ghosts = [blue, orange, red, pink, blue2]
```

Create some more ghosts called `yellow`, `mango`, `barry` and `dingo`. Create some super cool
images and animations for them.

## Bouncing the Ghosts

When the game runs, the ghosts all wizz away and stay within the play area but they eventually
all end up stuck in one of the corners. This is because the ghosts never change their direction.
What we want to do is make the ghosts bounce at the edges of the play area.

Change the `ghost_move()` function so that it is as follows:

```python
def ghost_move(ghost, dt):
    ghost.x += ghost.vx * dt
    ghost.y += ghost.vy * dt

    if ghost.x >= BOUNDS_X2:
        ghost.x = BOUNDS_X2
        ghost.vx *= -1
    elif ghost.x <= BOUNDS_X1:
        ghost.x = BOUNDS_X1
        ghost.vx *= -1
    
    if ghost.y >= BOUNDS_Y2:
        ghost.y = BOUNDS_Y2
        ghost.vy *= -1
    elif ghost.y <= BOUNDS_Y1:
        ghost.y = BOUNDS_Y1
        ghost.vy *= -1
```

Run your game and you should now see your ghosts bouncing furiously around the screen.

## Muncher and Ghost collisions

At present, when a ghost collides with Muncher, nothing happens. What we want is for the
collision to result in Muncher losing a life. Once a life is lost, we want a short pause,
then all of the actors to return to their starting positions, another short pause and
then the game to start again. The pauses will be controlled by chaining some function
calls using the Pygame `clock` class. When all lives are lost, the game will `exit()`.

Add the following two functions before your `draw()` function:

```python
def unpause():
    global paused
    paused = False


def reset_actors():
    for ghost in ghosts:
        ghost.x = GHOST_START_X
        ghost.y = GHOST_START_Y

    muncher.x = MUNCHER_START_X
    muncher.y = MUNCHER_START_Y

    if lives <= 0:
        exit()

    clock.schedule(unpause, 2)
```

The `update()` function needs two modifications done to it. The first modification is to
do nothing when the game is `paused`. This is achieved with the following code at the start
of the `update()` method:

```python
def update(dt):
    global lives, paused

    if paused:
        return
```

The second change is to check to see if any of the ghosts have collided with Muncher. This
is achieved by adding the following code to the end of the `update()` function.

```python
        for ghost in ghosts:
            if ghost.colliderect(muncher):
                lives -= 1
                paused = True
                clock.schedule(reset_actors, 2)
```

You entire `update()` function should now look as follows:

```python
def update(dt):
    global lives, paused

    if paused:
        return

    if keyboard.left:
        muncher.x -= muncher.vx * dt
    if keyboard.right:
        muncher.x += muncher.vx * dt
    if keyboard.up:
        muncher.y -= muncher.vy * dt
    if keyboard.down:
        muncher.y += muncher.vy * dt

    muncher.keep_in_bounds()

    for ghost in ghosts:
        ghost.move(dt)
        ghost.keep_in_bounds()

    for ghost in ghosts:
        if ghost.colliderect(muncher):
            lives -= 1
            paused = True
            clock.schedule(reset_actors, 2)
```

## Walls to negotiate

The play area needs some walls to make it more difficult for Muncher to avoid the ghosts.
Two different images will be required for the walls. One is 128 x 32 pixels (representing
a horizontal wall) and the other is 32 x 128 pixels (representing a vertical wall). You
can create your own images using a paint program that supports transparency (all the images
provided here were created using [PixilArt](https://www.pixilart.com/draw)) or you can use my images that are provided below.

The two images should be called `wall.png` and `wall2.png` and placed in the `images` folder.

`wall.png` should be 128 x 32 pixels ![screen shot](/img/python/pygame/muncher/wall.png)

`wall2.png` should be 32 x 128 pixels ![screen shot](/img/python/pygame/muncher/wall2.png)

All wall elements will be created as `Actors`. Add the following code before your `draw()`
function:

```python
walls = [
    Actor('wall', (WIDTH / 4, HEIGHT / 2)),
    Actor('wall', ((WIDTH / 4) * 3, HEIGHT / 2)),
    Actor('wall', (WIDTH / 2, HEIGHT / 5)),
    Actor('wall', (WIDTH / 2, (HEIGHT / 5) * 4)),
    Actor('wall2', (WIDTH / 5, HEIGHT / 3)),
    Actor('wall2', ((WIDTH / 5) * 4, HEIGHT / 3)),
    Actor('wall2', (WIDTH / 5, (HEIGHT / 3) * 2)),
    Actor('wall2', ((WIDTH / 5) * 4, (HEIGHT / 3) * 2)),
]
```

The `draw()` function needs to be updated to draw the walls. Add the additional code
to the end of your `draw()` function which should now look as follows:

```python
def draw():
    screen.clear()
    screen.draw.text(f"{score}", (WIDTH / 2, 15), color="red", fontsize=24)

    for i in range(lives):
        screen.blit('muncher', (5 + (37 * i), 5))

    muncher.animate()
    muncher.draw()

    for ghost in ghosts:
        ghost.animate()
        ghost.draw()

    for wall in walls:
        wall.draw()
```

Run your game. What happens when Muncher collides with a wall? Why do you think this is?

### Extension: Adding more walls

Try extending your game to add more wall elements to the play area. Experiment with new
images of different sizes to create interesting mazes and shapes. Just make sure to add
all of your new wall elements to the `wall` list so that they will be displayed.

## Colliding with walls

We want the ghosts to be able to go through the walls, they are ghosts after all. However,
we do not want Muncher to be able to go through the walls. We therefore need to check for
collisions between Muncher and wall elements. The collision detection algorithm that we
will be using is a relatively simple one that checks for overlaps of the edges of Muncher
and the walls but is effective enough for this type of game.

Add the following new collision detection function before your `draw()` function:

```python
def check_for_wall_collisions(actor):
    for wall in walls:
        if wall.colliderect(actor):
            # Try each of the edges of the wall
            if actor.top < wall.top and actor.bottom > wall.top:
                actor.bottom = wall.top

            if actor.bottom > wall.bottom and actor.top < wall.bottom:
                actor.top = wall.bottom

            if actor.left < wall.left and actor.right > wall.left:
                actor.right = wall.left

            if actor.right > wall.right and actor.left < wall.right:
                actor.left = wall.right
```

Then modify the `update()` function to check for collisions with muncher by adding the
following statement to the end of `update()`: `check_for_wall_collisions(muncher)`. Your
`update()` function should now look as follows:

```python
def update(dt):
    global lives, paused

    if paused:
        return

    if keyboard.left:
        muncher.x -= muncher.vx * dt
    if keyboard.right:
        muncher.x += muncher.vx * dt
    if keyboard.up:
        muncher.y -= muncher.vy * dt
    if keyboard.down:
        muncher.y += muncher.vy * dt

    muncher.keep_in_bounds()

    for ghost in ghosts:
        ghost.move(dt)
        ghost.keep_in_bounds()

    for ghost in ghosts:
        if ghost.colliderect(muncher):
            lives -= 1
            paused = True
            clock.schedule(reset_actors, 2)

    check_for_wall_collisions(muncher)
```

Run your game and check that Muncher cannot now pass through walls but the ghosts can.

## Pellets to eat

The pellets that Muncher likes to eat are small 8 x 8 pixel dots that are spread across
the play area but not where there are walls. Either create your own image or use mine
below, ensuring you copy it into the `images` folder.

![screen shot](/img/python/pygame/muncher/pellet.png)

Add the following pellet creation function before your `draw()` function:

```python
def create_pellets():
    global pellets
    pellets = []
    for y in range(14):
        for x in range(12):
            pos = (50 + (50 * x), 100 + (50 * y))
            collide = False
            for wall in walls:
                if wall.collidepoint(pos):
                    collide = True

            if not collide:
                pellets.append(Actor('pellet', pos))

pellets = []
create_pellets()
```

The `draw()` function needs to be updated to draw the pellets. Add the additional code
to the end of your `draw()` function which should now look as follows:

```python
def draw():
    screen.clear()
    screen.draw.text(f"{score}", (WIDTH / 2, 15), color="red", fontsize=24)

    for i in range(lives):
        screen.blit('muncher', (5 + (37 * i), 5))

    muncher.animate()
    muncher.draw()

    for ghost in ghosts:
        ghost.animate()
        ghost.draw()

    for wall in walls:
        wall.draw()

    for pellet in pellets:
        pellet.draw()        
```

Run your game and try to eat the pellets? What happens? Why do you think this is?

## Eating the pellets

Muncher cannot eat the pellets because we have not done the collision detection code
for it yet. Add the new code to the end of the `update()` function to perform the
collision detection and allow all of the pellets to be eaten.

New code:

```python
    global score, pellets
    before = len(pellets)
    pellets = [pellet for pellet in pellets if not pellet.colliderect(muncher)]
    after = len(pellets)
    score += (before - after) * 100
```

Your `update()` function should now be as follows:

```python
def update(dt):
    global lives, paused

    if paused:
        return

    if keyboard.left:
        muncher.x -= muncher.vx * dt
    if keyboard.right:
        muncher.x += muncher.vx * dt
    if keyboard.up:
        muncher.y -= muncher.vy * dt
    if keyboard.down:
        muncher.y += muncher.vy * dt

    muncher.keep_in_bounds()

    for ghost in ghosts:
        ghost.move(dt)
        ghost.keep_in_bounds()

    for ghost in ghosts:
        if ghost.colliderect(muncher):
            lives -= 1
            paused = True
            clock.schedule(reset_actors, 2)

    check_for_wall_collisions(muncher)

    global score, pellets
    before = len(pellets)
    pellets = [pellet for pellet in pellets if not pellet.colliderect(muncher)]
    after = len(pellets)
    score += (before - after) * 100
```

What happens when you eat all of the pellets? How do you think you should fix this?

## Eating all of the pellets

When Muncher eats all of the pellets the game should start another level. Instead it
just carries on. This is because we do not check that all pellets have been eaten.
Add the new code to the end of the `update()` function to perform the check on how many
pellets are left and start a new level if all have been eaten.

New code:

```python
    if len(pellets) <= 0:
        paused = True
        create_pellets()
        reset_actors()
```

Your `update()` function should now be as follows:

```python
def update(dt):
    global lives, paused

    if paused:
        return

    if keyboard.left:
        muncher.x -= muncher.vx * dt
    if keyboard.right:
        muncher.x += muncher.vx * dt
    if keyboard.up:
        muncher.y -= muncher.vy * dt
    if keyboard.down:
        muncher.y += muncher.vy * dt

    muncher.keep_in_bounds()

    for ghost in ghosts:
        ghost.move(dt)
        ghost.keep_in_bounds()

    for ghost in ghosts:
        if ghost.colliderect(muncher):
            lives -= 1
            paused = True
            clock.schedule(reset_actors, 2)

    check_for_wall_collisions(muncher)

    global score, pellets
    before = len(pellets)
    pellets = [pellet for pellet in pellets if not pellet.colliderect(muncher)]
    after = len(pellets)
    score += (before - after) * 100

    if len(pellets) <= 0:
        paused = True
        create_pellets()
        reset_actors()
```

## Ghosts with personality

Currently, the ghosts race around the screen in a fixed way which can make the
game just a little bit predictable. We are now going to program each of the
four ghosts with some additional intelligence to make them behave in more unique
ways

TODO

## Bonus fruit

When fruit appears, munch them for a big bonus.

TODO

## Power pelltets

Each a power pellet to supercharges Muncher and allows him to eat the ghosts.

TODO

## Getting additional lives

An additional life should be awarded for each 10,000 points the player scores.

TODO
