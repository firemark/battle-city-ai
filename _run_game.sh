CMD_A='python -m battle_city.client'
CMD_B='python -m battle_city.client'
IP='127.0.0.1'
PORT='8888'
MAP='a'
SERVER_OPTS=''

function show_help() {
    echo -e "`basename $0` [OPTIONS...]
    --help\t\tprint this text
    --cmd-p1 CMD_P1\tcommand to run client as player1. Default is \"$CMD_A\"
    --cmd-p2 CMD_P2\tcommand to run client as player2. Default is \"$CMD_B\"
    --map MAP\t\tselect map to run game. Default is $MAP
    --ip IP\t\tIP of server. Default is $IP
    --port PORT\t\tPORT of server. Default is $PORT
    --hidden-window\tdon't show window with game, run only server
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
        --hidden-window) SERVER_OPTS="$SERVER_OPTS --hidden-window";;
        *) break
    esac
    shift
done
