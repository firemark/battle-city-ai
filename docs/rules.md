# Rules

## Time

Game has two units of time:

1. TICK = `0.033 seconds * SPEED_OF_GAME (default 1)`
2. TURN = `10 * TICK`

On every tick monsters (tanks & bullets) can move to specific direction.

On every turn tanks can any action (like rotate or shot),
but tank can make one action per turn (so is not possible to shot on every tick)


## Possible actions of tanks
Every action can run only once per *TURN*.

Protocol of actions are described [here](./actions.md)

### change speed
Player tanks can change speed from 0 to 2 pixels per *TICK*.

NPC tanks has a constant speed 2.

Bullet has a constant speed 8.

### freeze / unfreeze
When bullet from another player touched your tank then tank will be frozen.

When tank is frozen then you can move (but you can rotate and shoot!).

Time of freeze is randomized from 0 to 300 ticks.

### rotate
To change direction of your tank, you must rotate them.
When tank is rotated then position of tank will snap to grid 16×16 pixels.

### shoot
Setup bullet in your tank and will shoot in next *TURN*.

## Monsters

### Bullets
Kill monsters / freeze players / destroy walls and relationships

### NPC
OMG KILL IT!

You will get 200 points for each killed NPC.

### Tanks
Tanks controlled by bots.

## Walls

### Tinywall
small brick (small part of red bricks) - bullet can destroy this.

### Metal
grey bricks - is not destroyable by bullets.

### Water

blue field, only bullets can across this field.

## Coins

Every gained coin gets 100 points
