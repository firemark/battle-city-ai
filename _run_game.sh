IP='127.0.0.1'
PORT='8888'
MAP='pilif'
SPEED='1'
SERVER_OPTS=''

show_help() {
    echo -e "`basename $0` [OPTIONS...]
    --help\t\t\tprint this text
    --cmd-p1 CMD_P1\t\tcommand to run client as player1. Default is \"$CMD_A\"
    --cmd-p2 CMD_P2\t\tcommand to run client as player2. Default is \"$CMD_B\"
    --map MAP\t\t\tselect map to run game. Default is $MAP
    --ip IP\t\t\tIP of server. Default is $IP
    --port PORT\t\t\tPORT of server. Default is $PORT
    --speed SPEED\t\ttick speed of game. default is $SPEED
    --hidden-window\t\tdon't show window with game, run only server
    --turn-off-after-end\tturn off server when game is end. Good option for machine learning
    "
}

while :; do
    case $1 in
        -h|--help) show_help; exit;;
        --cmd-p1) CMD_A=$2; shift;;
        --cmd-p2) CMD_B=$2; shift;;
        --ip) IP=$2; shift;;
        --port) PORT=$2; shift;;
        --map) MAP=$2; shift;;
        --speed) SPEED=$2; shift;;
        --hidden-window) SERVER_OPTS="$SERVER_OPTS --hidden-window";;
        --turn-off-after-end) SERVER_OPTS="$SERVER_OPTS --turn-off-after-end";;
        *) break
    esac
    shift
done
