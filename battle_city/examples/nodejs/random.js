class Game {
    constructor(client) {
        this.client = client;
        this.firstTick = false;
        this.start = false;
    }

    receive(data) {
        let color = '\x1B[0m'; // default color
        switch(data.status) {
            case 'data':
                switch(data.action) {
                    case 'move': return; break; // too many data ;_;
                    case 'spawn': color = '\x1B[92m'; break; // green color
                    case 'destroy': color = '\x1B[93m'; break; // orange color
                }
            break;
            case 'ERROR': color = '\x1B[91m'; break; // red color
            case 'OK': color = '\x1B[35m'; break; // purple color
            case 'game':
                color = '\x1B[34m'; // blue color
                switch(data.action) {
                    case 'start': this.start = true; break;
                    case 'over': this.start = false; break;
                }
            break; 
        }

        console.log(color, data, '\x1B[0m');
    }

    loop() {
        if (!this.firstTick) {
            this.send({action: 'greet', name: 'TEST'});
            this.firstTick = true;
        } 

        if (this.start) {
            let action = Math.floor(Math.random() * 3);
            switch(action) {
                case 0:
                    // random speed
                    let speed = Math.round(Math.random() * 2);
                    this.send({action: 'set_speed', speed: speed});
                break;
                case 1:
                    // random direction
                    let index = Math.floor(Math.random() * 4);
                    let direction = ['up', 'down', 'left', 'right'][index];
                    this.send({action: 'rotate', direction: direction});
                break;
                case 2:
                    // SHOT SHOT SHOT
                    this.send({action: 'shot'});
                break;
            }
        }

        this.callSoon(250);
    }

    callSoon(time) {
        setTimeout(this.loop.bind(this), time);
    }

    send(data) {
        let message = JSON.stringify(data);
        this.client.write(message + '\n');
    }

}

let net = require('net');
let client = new net.Socket();
client.setNoDelay();
let game = new Game(client);

client.connect({port: 8888, host: '127.0.0.1'}, function() {
    console.log('\x1B[1mCONNECTED!\x1B[0m');
    game.loop();
});

let buffer = '';
client.on('data', function(raw) {
    let prev, next;
    let message = raw.toString('utf8');
    while ((next = message.indexOf('\n', prev)) > -1) {
      buffer += message.substring(prev, next);

      let data = JSON.parse(buffer);
      game.receive(data);

      buffer = '';
      prev = next + 1;
    }
    buffer += message.substring(prev);
});

client.on('close', function() {
	console.log('Connection closed');
});
