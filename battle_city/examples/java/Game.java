import java.io.*;
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
        if (timestamp - newTimestamp > 250) {
            timestamp = newTimestamp;
            tick();
        }

        System.out.println(data.toJSONString());
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
            // do sth
        }
    }

    public void send(JSONObject obj) {
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
