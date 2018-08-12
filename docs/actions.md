# Actions
To change state of player tank we need to send actions with specified format:

### Request

```js
{"action": ACTION_NAME, "additional_args": "sth"}
```

### Good Response
```js
{"status": "OK", "additional_args": "sth"}
```

### Failed Response
```js
{"status": "ERROR", "message": "msg"}
```

# Available actions

## Greeting
Need to set name of player and get map. Name of player must be 6 char length and have only alphanumerics chars

### Request
```js
{"action": "greet", "name": NAME}
```

### Response
```js
{
    "status": "OK",
    "id": YOUR_HEX,
    "cords": [
        {"type": "tiny_wall", "id": "HEX", "position": {"x": X, "y": Y},
        {"type": "player", "id": "HEX", "position": {"x": X, "y": Y},
        …
    ]
}
```

Types are descripted in types.md

### Possible Errors
* `name is too long` 
* `name is blank`
* `name has wrong type`
* `name is undefined`
* `your are greeted before`

## Set Speed

### Request
```js
// available SPEED is 0, 1 or 2
{"action": "set_speed", "speed": SPEED}
```

### Response
```js
{"status": "OK", "speed": SPEED}
```

## Rotate

### Request
```js
// available Direction is "left", "right", "up" or "down"
{"action": "rotate", "direction": DIRECTION}
```

### Response
```js
{"status": "OK", "direction": DIRECTION}
```

## Shot
On the next tick will be created a new bullet with direction of tank

### Request
```js
{"action": "shot"}
```

### Response
```js
{"status": "OK"}
```
