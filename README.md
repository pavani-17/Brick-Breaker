A simple brickbreaker game written in Python, utilising OOPS concepts and is playable on the Terminal, not making use of any cursor libraries. The only libraries required are `numpy` and `colorama`.

### Features of the Game
* Bricks of various types such as normal (bricks which break after n number of hits, where n varies between {1, 2, 3} for each brick), unbreakable (bricks which can be broken only under special circumstances) and exploding bricks (bricks which explode and break all neighbouring bricks, irrespective of strength)

* A simple paddle which is used to control the ball. The ball velocity depends on where it lands on the paddle, with most deflection observed at the edges.

* Powerups such as: <br>
    1) Fast Ball : Increases the speed of the ball
    2) Expand Paddle: Increases the paddle size
    3) Shrink Paddle: Decreases the paddle size
    4) Ball Multiplier: Multiplies the number of balls
    5) Thru Balls: Allows the ball to pass through and break any type of brick
    6) Paddle Grab: Allows the paddle to grab the ball and relaunch at will

### Controls:

<button>s</button> - Release the ball from the paddle <br>
<button>a</button> - Move the paddle to the left <br>
<button>d</button> - Move the paddle to the right <br>

Note that all these controls are case sensitive.

### OOPS Concepts:

The game is written in a modular fashion, allowing new features to be added with minimum modification. Writing duplicate code is avoided using the principles of inheritance and polymorphism as and when needed.

### Run Instructions:

* pip3 install numpy
* pip3 install colorama
* python3 main.py
