from battle_city.monsters.tank import Tank


class Player(Tank):
    player_id: int
    score: int = 0
    ready: bool = False
    connection = None

    had_action: bool = False
    
    def __init__(self, player_id):
        if player_id == 0:
            super().__init__(128, 320)
        elif player_id == 1:
            super().__init__(512 - 128, 320)
        else:
            raise ValueError('player_id')
        self.player_id = player_id

    def set(self, connection):
        self.connection = connection
        self.ready = True

    def set_had_action(self):
        self.had_action = True

    def get_serialized_data(self):
        data = super().get_serialized_data()
        data['player_id'] = self.player_id
        return data
