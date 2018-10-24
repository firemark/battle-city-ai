import java.io.*;
import java.util.Random;
import java.net.Socket;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

public class Game {
    private OutputStream writer;
    private boolean start;
    private boolean firstTick;
    private long timestamp;

    private Game(Socket socket) throws IOException {
        start = false;
        firstTick = false;
        timestamp = 0;

        writer = socket.getOutputStream();
    }

    public void receive(JSONObject data) {
        // java with not external libs doesnt have async code
        // so I must check timestamp and run tick
        long newTimestamp = System.currentTimeMillis();
        if (newTimestamp - timestamp > 250) {
            timestamp = newTimestamp;
            tick();
        }

        switch ((String) data.get("status")) {
            case "data":
                String action = (String) data.get("action");
                if (action.equals("move")) {
                    return; // to many data ;_;
                }
            break;
            case "game":
                switch ((String) data.get("action")) {
                    case "start": start = true; break;
                    case "over": start = false; break;
                }
            break;
        }

        System.out.print(getColor(data));
        System.out.print(data.toJSONString());
        System.out.print("\033[0m\n");
    }

    public void tick() {
        if (!firstTick) {
            JSONObject obj = new JSONObject();
            obj.put("action", "greet");
            obj.put("name", "JAVA");
            send(obj);
            firstTick = true;
        }

        if (start) {
            Random generator = new Random();
            int action = generator.nextInt(3);
            JSONObject obj = new JSONObject();
            switch (action) {
                case 0: // random speed
                    int speed = generator.nextInt(2);
                    obj.put("action", "set_speed");
                    obj.put("speed", speed);
                    send(obj);
                break;
                case 1: // random direction
                    int index = generator.nextInt(4);
                    String direction = "";
                    switch (index) {
                        case 0: direction = "up"; break;
                        case 1: direction = "down"; break;
                        case 2: direction = "left"; break;
                        case 3: direction = "right"; break;
                    }
                    obj.put("action", "rotate");
                    obj.put("direction", direction);
                    send(obj);
                break;
                case 2: // SHOT SHOT SHOT
                    obj.put("action", "shoot");
                    send(obj);
                break;
            }
        }
    }

    private String getColor(JSONObject data) {
        switch ((String) data.get("status")) {
            case "data":
                switch ((String) data.get("action")) {
                    case "spawn": return "\033[92m"; // green
                    case "destroy": return "\033[93m"; // orange 
                }
            break;
            case "ERROR": return "\033[91m"; // red
            case "OK": return "\033[35m"; // purple
            case "game": return "\033[34m"; // blue
        }
        return "\033[0m"; // white
    }

    private void send(JSONObject obj) {
        try {
            writer.write(obj.toJSONString().getBytes());
            writer.write('\n');
            writer.flush();
        } catch (IOException e) {}
    }

    public static void main(String[] args) throws IOException {
        Socket socket = new Socket("127.0.0.1", 8888);
        try {
            Game game = new Game(socket);
            BufferedReader reader = new BufferedReader(
                new InputStreamReader(socket.getInputStream())
            );
            System.out.println("\033[1mCONNECTED!\033[0m");

            game.tick();

            JSONParser parser = new JSONParser();
            String line;
            while((line = reader.readLine()) != null) {
                try {
                    JSONObject obj = (JSONObject) parser.parse(line);
                    game.receive(obj);
                } catch (ParseException e) {}
            }
        } catch (IOException e) {
            throw e;
        } finally {
            socket.close();
        }
    }
}
