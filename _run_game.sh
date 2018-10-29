IP='127.0.0.1'
PORT='8888'
MAP='pilif'
SPEED='1'
SERVER_OPTS=''
MAX_PLAYERS=2

show_help() {
    echo -e "`basename $0` [OPTIONS...]
    --help\t\t\tprint this text
    --cmd-p1 CMD_P1\t\tcommand to run client as player1. Default is \"$CMD_A\"
    --cmd-p2 CMD_P2\t\tcommand to run client as player2. Default is \"$CMD_B\"
    --cmd-p3 CMD_P3\t\tcommand to run client as player3. Default is \"$CMD_C\"
    --cmd-p4 CMD_P4\t\tcommand to run client as player4. Default is \"$CMD_D\"
    --map MAP\t\t\tselect map to run game. Default is $MAP
    --max-players NUM\t\tnumber of bots in game. Max is 4. Default is $MAX_PLAYERS
    --ip IP\t\t\tIP of server. Default is $IP
    --port PORT\t\t\tPORT of server. Default is $PORT
    --speed SPEED\t\ttick speed of game. default is $SPEED
    --hidden-window\t\tdon't show window with game, run only server
    --turn-off-after-end\tturn off server when game is end. Good option for machine learning
    --show-collision-border\tshow borders with collisions
    "
}

while :; do
    case $1 in
        -h|--help) show_help; exit;;
        --cmd-p1) CMD_A=$2; shift;;
        --cmd-p2) CMD_B=$2; shift;;
        --cmd-p3) CMD_C=$2; shift;;
        --cmd-p4) CMD_D=$2; shift;;
        --ip) IP=$2; shift;;
        --port) PORT=$2; shift;;
        --map) MAP=$2; shift;;
        --speed) SPEED=$2; shift;;
        --max-players) MAX_PLAYERS=$2; shift;;
        --hidden-window) SERVER_OPTS="$SERVER_OPTS --hidden-window";;
        --turn-off-after-end) SERVER_OPTS="$SERVER_OPTS --turn-off-after-end";;
        --show-collision-border) SERVER_OPTS="$SERVER_OPTS --show-collision-border";;
        *) break
    esac
    shift
done
CMDS=(- "$CMD_A" "$CMD_B" "$CMD_C" "$CMD_D")
SERVER_CMD="python -m battle_city.server\
    --ip $IP\
    --port $PORT\
    --map $MAP\
    --speed $SPEED\
    --max-players $MAX_PLAYERS\
    $SERVER_OPTS"
