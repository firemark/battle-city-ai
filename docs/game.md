# Game Messages

## Start game
```js
{
    "status": "game",
    "action": "start"
}
```

## Info about area
```js
{
    "status": "game",
    "action": "info",
    "ticks_left": TICK, // int
    "npcs_left": COUNT // int
}
```

## Game over
```js
{
    "status": "game",
    "action": "over",
    "winner": NAME
}
```
