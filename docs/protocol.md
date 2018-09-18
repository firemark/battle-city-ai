# Protocol Format

Protocol is very easy - asynchronous, persistent connection on TCP/IP similar to JSON-RPC

## Example

### Request
```javascript
{"action": "set_speed", "speed": 2}\n
```

### Response
```javascript
{"status": "OK", "speed": 2}\n
```

Because this game is real time, server sends data about moving of tanks/bullets etc

TODO: write about frequency and usage of informations

```javascript
{"status": "data", "action": "change", "id": "HEX", …}\n
```

