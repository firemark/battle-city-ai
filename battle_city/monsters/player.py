from battle_city.monsters.tank import Tank


class Player(Tank):
    player_id: int
    score: int = 0
    ready: bool = False
    connection = None
    is_game_over: bool = False
    nick: str = None

    had_action: bool = False
    
    def __init__(self, player_id, x, y):
        super().__init__(x, y)
        if player_id not in range(4):
            raise ValueError('player_id')
        self.player_id = player_id

    def set_connection(self, connection):
        self.connection = connection

    def set_had_action(self):
        self.had_action = True

    def set_game_over(self):
        self.is_game_over = True

    def set_nick(self, nick: str):
        self.nick = nick
        self.ready = True

