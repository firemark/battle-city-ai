# Protocol Format

Protocol is very easy - asynchronous, persistent connection on TCP/IP similar to JSON-RPC

## Example

### Request
```json
{"action": "set_speed", "speed": 2}\n
```

### Response
```json
{"status": "OK", "speed": 2}\n
```

Because this game is real time, server sends data about moving of tanks/bullets etc

```json
{"status": "data", "action": "change", "id": "HEX", …}\n
```

