# Unit messages
On every tick in the server, the server will send many messages about unit moves,
spawning bullet/npc or destroying tank/bullet/wall.

Type of message is field `status` with value `"data"`
To determine action of object (destroy/move/change/spawn) you can use `action` field.

## Move status

Sends only basic information about movement
```js
{
    "status": "data",
    "action": "move",
    "id": HEX,
    "position": {"x": X, "y": Y}
}
```

## Spawn/Change/Freeze
When unit is spawned or changed (direction, speed or sth) then server sends all info about object.

```js
{
    "status": "data",
    "action": "change"|"spawn"|"freeze"|"unfreeze",
    "id": HEX,
    "type": TYPE,
    "speed": SPEED, // int
    "position": {"x": X, "y": Y},
    "direction": "up"|"down"|"left"|"right",
    "is_freeze": true|false // tank can be freezed max to 15 ticks of game.
}
```

### Possible actions

* `change` - when object is changed - like another speed or direction.
* `spawn` - when object is created - shot bullet or new NPC in the area
* `freeze` - when player was shot by another player. This player can't move.
* `unfreeze` - when is player is not freezed and can move.

## Destroy
```js
{
    "status": "data",
    "action": "destroy",
    "id": HEX
}
```
