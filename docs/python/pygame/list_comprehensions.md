# List comprehensions

This short sub-section provides additional information on list comprehensions as they are
used commonly in Python code due to their conciseness. For a complete description of list
comprehensions, see the official Python documentation [here](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions) which describes list comprehensions as:

> List comprehensions provide a concise way to create lists. Common applications are to make new lists where each element is the result of some operations applied to each member of another sequence or iterable, or to create a subsequence of those elements that satisfy a certain condition.

In [Smash](./smash.md), [list comprehension](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions)
were introduced in the following places:

* `check_for_collisions()` in Step 6: Destroying the blocks
* `ParticleExplosion.update()` in Step 9: Add particle effects, Explosion particle effect

We will now look at each of those list comprehensions, breaking them down into more traditional
loops so you can see more clearly how they work.

## `check_for_collisions()` in Step 6: Destroying the blocks

The following excerpt shows the section of code with the list comprehension in
`check_for_collisions()`.

```python
blocks_to_destroy = [block for block in blocks if ball.collide(block.bounding_box)]
```

This type of list comprehension is very common. You will see these regularly in Python code.
What this code is doing is looping over every `block` in the `blocks` list. Each block is
checked for whether it collides with the `ball`. If it does, it is added to a new list. The
new list is is then assigned to the `blocks_to_destroy` variable.

The above single line list comprehension is equivalent to the following 4 lines of code:

```python
blocks_to_destroy = []

for block in blocks:

    if ball.collide(block.bounding_box)

        blocks_to_destroy.append(block)
```

Can you see how each of the first 3 lines of code maps to the list comprehension?

## A new example

We will now work through a new example that you can run in Replit to demonstrate the
functionality of a list comprehension and experiment with it. We will first start with
the code using a plain ld loop and then turn it into a list comprehension. The example
we will be using is to select all numbers that are negative from a list of 10 numbers.

Type in the following code and run it.

```python

numbers = [1, -1, 30, -400, -5, 13, 17, -27, 0, 1000]

negative_numbers = []

for number in numbers:

    if number < 0:

        negative_numbers.append(number)

print(negative_numbers)
```

You should see the following output:

```python
[-1, -400, -5, -27]
```

Using the same pattern as before, the list comprehension can be build from the parts of
the loop code. The entire section of code above can be condensed into:

```python
numbers = [1, -1, 30, -400, -5, 13, 17, -27, 0, 1000]

negative_numbers = [number for number in numbers if number < 0]

print(negative_numbers)
```

### Experiments

Change the code so that it only selects positive numbers.

Change the code so that it only selects numbers greater than 100.

Change the code so that is only selects numbers whose magnitude is greater than 20. To get the
magnitude you can use the built in function `abs()`. For information see the following resources:

* [Python abs() function reference](https://www.w3schools.com/python/ref_func_abs.asp)
* [How to Find an Absolute Value in Python](https://realpython.com/python-absolute-value/)

## `ParticleExplosion.update()` in Step 9: Add particle effects

The following except shows the section of code that creates the `particles` list in the
`__init__()` method as well as the list comprehension in the `update()` method of the
`ParticleExplosion` class.

```python
GRAVITY = 60

class ParticleExplosion:
    def __init__(self, pos, lifetime, colour):
        self.particles = [(pos[0], pos[1], randint(-90, 90), randint(-90, 90)) for _ in range(30)]

    def update(self, dt):
        self.particles = [(particle[0] + (particle[2] * dt),
                           particle[1] + (particle[3] * dt), particle[2],
                           particle[3] + (GRAVITY * dt))
                          for particle in self.particles]
```

This *looks* more complicated than the first example but it really isn't. We can remove
some of the code to make an more easily testable piece of code as follows (note, this
code reduces the number of particles from 30 to 5):

```python
from random import randint

GRAVITY = 60
x = 10
y = 20
pos = (x, y)
particles = [(pos[0], pos[1], randint(-90, 90), randint(-90, 90)) for _ in range(5)]
print(particles)

dt = 1
particles = [(particle[0] + (particle[2] * dt),
              particle[1] + (particle[3] * dt), particle[2],
              particle[3] + (GRAVITY * dt))
             for particle in particles]
print(particles)
```

Run the above code in Replit and you will get output similar to this below:

```python
[(10, 20, 32, -66), (10, 20, -69, -74), (10, 20, -85, 56), (10, 20, -90, -68), (10, 20, -78, -39)]
[(42, -46, 32, -6), (-59, -54, -69, -14), (-75, 76, -85, 116), (-80, -48, -90, -8), (-68, -19, -78, 21)]
```

This is the list comprehension:

```python
particles = [(particle[0] + (particle[2] * dt),
              particle[1] + (particle[3] * dt), particle[2],
              particle[3] + (GRAVITY * dt))
             for particle in particles]
```

Now lets break this down to a standard loop as we did before:

```python
new_particles = []
for particle in particles:
    x, y, vx, vy = particle
    new_x = x + vx * dt
    new_y = y + vy * dt
    new_vy = vy + GRAVITY * dt
    new_particles.append((new_x, new_y, vx, new_vy))

particles = new_particles
print(particles)
```

Because the above code uses intermediate variables, each of the items in the `particle` tuple
is given a name of `x`, `y`, `vx` or `vy` which represents the `x` and `y` co-ordinate of the
particle, the horizontal speed of the particle (`vx`) and the vertical speed of the particle
(`vy`).

What this code demonstrates that may not have been obvious in the first example above is the
limitation that you should not mutate the contents of a list when looping over them. This is
why the modified particles are first added to the `new_particles` list and then at the end of
the code the `new_particles` list is assigned to `particles`. List comprehensions do not have
this limitation.

For more information on tuples, see:

* [Python Tuples reference](https://www.w3schools.com/python/python_tuples.asp)
* [Tuples and Sequences](https://docs.python.org/3/tutorial/datastructures.html#tuples-and-sequences)

### Experiments

Replace the following line of code:

`new_particles.append((new_x, new_y, vx, new_vy))`

With:

`particles.append((new_x, new_y, vx, new_vy))`

And remove the `particles = new_particles` line of code.

Run your program. What happens?
