# Unit messages
On every tick in the server, server will be sent many messages about unit moving, spawning bullet/npc or destroying tank/bullet/wall.

Type of message is field `status` with value `"data"`
To determine action of object (destroy/move/change/spawn) you can use `action` field.

## Move status

Sends only basic informations about movement
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
    "position": {"x": x, "y": Y},
    "direction": "up"|"down"|"left"|"right",
    "is_freeze": true|false
}
```

## Destroy
```js
{
    "status": "data",
    "action": "destroy",
    "id": HEX
}
```
