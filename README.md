# battle-city-ai
[![Build Status](https://travis-ci.org/firemark/battle-city-ai.svg?branch=master)](https://travis-ci.org/firemark/battle-city-ai)

## Legend

- [What is this?](#what-is-this)
- [How does this work?](#how-does-this-work)
- [What is the goal?](#what-is-the-goal)
  - [How to achieve that?](#how-to-achieve-that)
  - [Tips](#tips)
  - [Scores](#scores)
- [Protocol Documentation](#protocol-documentation)
- [How to Install?](#how-to-install)
- [How to write first bot?](#how-to-write-first-bot)
- [Server script](#server-script)
- [Run tests](#run-tests)
- [Technology](#technology)
- [Contributors](#contributors)


## What is this?

It is a simple clone of battle city from NES.

## How does this work?
The game runs on a server with a game window and listens for two connections: player1 and player2.
Each player is a separate client (tank) connected to the game server. The clients control their tanks 
by sending actions to the server. The game starts when both connections are established and 
greetings messages are send to both clients. The client's moves are defined once, and do not 
undergo any changes during the gameplay.

## What is the goal?

There are two goals:

1. **SURVIVE** in 2 minutes
2. Get more points than the second player

### How to achieve that?
In order to survive and score the biggest amount of points, you need to program the moves 
of your client with a thorough and clever approach. 


### Tips

TODO

### Scores

* **1** for each destroyed tiny-brick
* **5** for each 'freeze' second player
* **200** for each destroyed NPC tank
* TODO: **300** for each coin

## Protocol documentation

Is [here](docs/).

* [General Protocol](docs/protocol.md)
* [Player actions](docs/actions.md)
* [Unit's messages](docs/units.md)
* [Game's messages](docs/game.md)
* [Types in game](docs/types.md)

## How to install?

```sh
# code works in Python 3.5, 3.6 and 3.7
# remember about virtualenv or pipenv!
# https://docs.python.org/3/tutorial/venv.html
# https://pipenv.readthedocs.io/en/latest/

python setup.py develop
# done.
```

## How to write first bot?

First, copy [example code](battle_city/client.py)
(more examples are [here](battle_city/examples/))

Now:

```sh
# remember about virtualenv or pipenv!
# https://docs.python.org/3/tutorial/venv.html
# https://pipenv.readthedocs.io/en/latest/

# scripts have a optional argument -a for player A and -b for player B
# command would be a runner, example "python copied_client.py" - remember about command (python, nodejs, ruby or something else) to run your script!!
# default command for -a and -b is "python -m battle_city.client"
# ./run_game.sh [-a CMD_A] [-b CMD_B]

# linux/mingw/osx/wsl
./run_game.sh -a "python copied_client.py"
# The color of your tank will be yellow.
# tmux version - more hackerable!
./run_game_tmux.sh -a "python copied_client.py"
```

The `run_game.sh` script will run the whole game with two clients. There is no need to run anything else.
The script includes a command for running server and commands for running two clients. The basic clients are dummy.
They will just move randomly.
If you want to start implementing your algorithms for moves, create your own
client, based on the example [example code](battle_city/client.py), and after finishing, 
use it in `run_game.sh` script (examples are above).

## Server script

```
python -m battle_city.server [--ip IP] [--port PORT] [--hide-window]
```

Note that `run_game.sh` script runs the server as well as both clients by default.
If you want to create your own configuration for running the game, use the command above 
in your own script.

## Run tests

```sh
pip install -e .[test]
pytest tests/
```

## Technology

* Python >=3.5
* Pygame
* Asyncio
* JSON
* Love

## Contributors

* Firemark - game logic and everything else
* Stachu - documentation, beta testing
