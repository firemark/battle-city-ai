# battle-city-ai

## What is this?

Is a simple clone of battle city from NES

## How to install?

```
# remember about virtualenv/pipenv!
python setup.py develop
# done.
```

## What is a goal?

Goals are two:

1. **SURVIVE** in 2 minutes
2. Get points more than the second player

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

## How to write first bot?

Copy a [example code](battle_city/client.py) and run:

```sh
# remember about virtualenv/pipenv!
# scripts have argument -a for player A and -b for player B
# ./test_it.sh [-a CMD_A] [-b CMD_B]

# linux/mingw/osx/wsl
./test_it.sh -a "python file.py"
# tmux version - more hackerable!
./test_it_tmux.sh -a "python file.py"
```

Your bot will be as yellow tank.

## Server script

```
python -m battle_city.server [--ip IP] [--port PORT] [--hide-window]
```

## Run tests

```sh
pip install -e .[test]
pytest tests/
```

## How does this work?

Server on startup create a simple server and window with game and listens for the two connections.

When connections are established and will send greetings messages then game will be started.

## Technology

* Python >=3.5
* Pygame
* Asyncio
* JSON
* Love
