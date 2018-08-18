Every object has `id` field and `x, y` coordinations.

# Solid types
Solid objects have only type (`tinywall/water/metal`) and coordinations

## Tiny Wall
* type: `tinywall`
* size: `32x32`

can be destroyed with bullets.

## Water
* type: `water`
* size: `32x32`

This tile is invisible for bullets but tanks cannot cross this tile

## Metal
* type: `metal`
* size: `32x32`

Unbreakable wall.

# Tanks
## Player
* type: `player`
* size: `32x32`

To identify your tank you need `id` field from `greetings` response.
This object sends information about speed/coordinations/direction and shots.

## NPC
* type: `npc`
* size: `32x32`

Enemy tank - like player, sends information and shots.


# Bullet
* type: `bullet`
* size: `4x4`

Crash walls, destroy tanks etc. - similar to tanks, bullet sends informations about himself.

When bullet is from player and hit another player, 'touched' player will be freezed.
