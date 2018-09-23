from unittest.mock import patch, Mock, call

from battle_city.drawer import Drawer
from battle_city.game import Game
from battle_city.monsters import Player, NPC, Bullet
from battle_city.monsters.wall import TinyWall, Metal, Water
from battle_city.basic import Direction

patch_pygame = patch('battle_city.drawer.pygame')


@patch_pygame
def test_render(pygame):
    mock_drawer = Mock(spec=Drawer)
    mock_drawer.time = 0

    Drawer.render(mock_drawer)

    assert mock_drawer.time == 1
    assert mock_drawer.method_calls == [
        call._support_pygame_events(),
        call._render_background(),
        call._render_players(),
        call._render_bullets(),
        call._render_npcs(),
        call._render_walls(),
        call._render_text(),
    ]

    assert pygame.display.flip.called


@patch_pygame
def test_render_reset_time(pygame):
    mock_drawer = Mock(spec=Drawer)
    mock_drawer.time = 99

    Drawer.render(mock_drawer)

    assert mock_drawer.time == 0


@patch_pygame
def test_render_background(pygame):
    game = Game()
    drawer = Drawer(game)

    drawer._render_background()

    drawer.screen.fill.assert_called_once_with((0x5f, 0x57, 0x4f))
    pygame.draw.rect.assert_called_once_with(drawer.screen, (0, 0, 0), (
        drawer.OFFSET, drawer.OFFSET,
        drawer.game.WIDTH, drawer.game.HEIGHT,
    ))


@patch_pygame
def test_render_players(pygame):
    game = Game()
    game.alive_players = [
        Player(0, 32, 32),
        Player(1, 64, 32),
    ]
    drawer = Drawer(game)
    drawer._blit = Mock(spec=drawer._blit)

    drawer._render_players()

    assert drawer._blit.call_args_list == [
        call('IMG_PLAYER_1_1', game.alive_players[0]),
        call('IMG_PLAYER_2_1', game.alive_players[1]),
    ]


@patch_pygame
def test_render_players_with_freeze(pygame):
    game = Game()
    game.alive_players = [
        Player(0, 32, 32),
    ]
    game.alive_players[0].set_freeze()
    drawer = Drawer(game)
    drawer._blit = Mock(spec=drawer._blit)

    drawer._render_players()

    assert drawer._blit.call_args_list == [
        call('IMG_PLAYER_1_1', game.alive_players[0]),
        call('FREEZE', game.alive_players[0]),
    ]


@patch_pygame
def test_render_npcs(pygame):
    game = Game()
    game.npcs = [
        NPC(32, 32),
        NPC(64, 32),
    ]
    drawer = Drawer(game)
    drawer._blit = Mock(spec=drawer._blit)

    drawer._render_npcs()

    assert drawer._blit.call_args_list == [
        call('IMG_NPC_1', game.npcs[0]),
        call('IMG_NPC_1', game.npcs[1]),
    ]


@patch_pygame
def test_render_bullets(pygame):
    game = Game()
    game.bullets = [
        Bullet(32, 32),
        Bullet(64, 32),
    ]
    drawer = Drawer(game)
    drawer._blit = Mock(spec=drawer._blit)

    drawer._render_bullets()

    assert drawer._blit.call_args_list == [
        call('BULLET', game.bullets[0]),
        call('BULLET', game.bullets[1]),
    ]


@patch_pygame
def test_render_walls(pygame):
    game = Game()
    game.walls = [
        TinyWall(48, 32),
        Metal(64, 48),
        Water(96, 32),
    ]
    drawer = Drawer(game)
    os = Drawer.OFFSET
    drawer.WALLS = {  # pygame surface can't use eq operator ;_;
        TinyWall: 'tiny_wall',
        Metal: 'metal',
        Water: 'water',
    }

    drawer._render_walls()

    assert drawer.screen.blit.call_args_list == [
        call('tiny_wall', (os + 48, os + 32), (16, 0, 8, 8)),
        call('metal', (os + 64, os + 48), (0, 16, 32, 32)),
        call('water', (os + 96, os + 32), (0, 0, 32, 32)),
    ]


@patch_pygame
def test_render_text(pygame):
    game = Game()
    game.npcs = [NPC(0, 0), NPC(1, 1)]
    game.players = [Player(0, 32, 32), Player(1, 64, 32)]
    game.players[0].set_nick('1234')
    game.players[0].score = 100
    game.time_left = 125
    game.npcs_left = 3
    drawer = Drawer(game)
    drawer._render_label = Mock(spec=drawer._render_label)

    drawer._render_text()

    assert drawer._render_label.call_args_list == [
        call('BATTLE CITY AI', (0, 00)),
        call('NPCs left:    003', (0, 40)),
        call('NPCs in area: 002', (0, 80)),
        call('Time left:    125', (0, 120)),
        call('NOT READY', (0, 180)),
        call('1234       000100', (0, 240), drawer.PLAYER_COLORS[0]),
        call('WAIT', (0, 260), drawer.PLAYER_COLORS[0]),
        call('P1         000000', (0, 280), drawer.PLAYER_COLORS[1]),
        call('WAIT', (0, 300), drawer.PLAYER_COLORS[1]),
    ]


@patch_pygame
def test_get_info_label_from_killed_player(pygame):
    drawer = Drawer(Game())
    player = Player(0, 0, 0)
    player.set_game_over()

    assert drawer._get_info_label(player) == 'KILLED'


@patch_pygame
def test_get_info_label_from_not_connected_player(pygame):
    drawer = Drawer(Game())
    player = Player(0, 0, 0)

    assert drawer._get_info_label(player) == 'WAIT'


@patch_pygame
def test_get_info_label_from_connected_player(pygame):
    drawer = Drawer(Game())
    player = Player(0, 0, 0)
    player.set_connection(object())

    assert drawer._get_info_label(player) == ''


@patch_pygame
def test_get_info_label_from_freezed(pygame):
    drawer = Drawer(Game())
    player = Player(0, 0, 0)
    player.set_connection(object())
    player.set_freeze()

    assert drawer._get_info_label(player) == 'FREEZE'


@patch_pygame
def test_render_label(pygame):
    drawer = Drawer(Game())
    drawer.font.render = Mock(return_value='IMAGE')

    drawer._render_label(label='test', cords=(1, 2), color=(0, 1, 2))

    drawer.screen.blit.assert_called_once_with(
        'IMAGE',
        (drawer.OFFSET_LABELS_X + 1, drawer.OFFSET_LABELS_Y + 2)
    )
    drawer.font.render.assert_called_once_with('test', 1, (0, 1, 2))


@patch_pygame
def test_drawer_blit_simple(pygame):
    drawer = Drawer(Game())
    image = object()
    drawer.IMAGES = {'IMAGE': image}

    drawer._blit('IMAGE', NPC(1, 2))

    drawer.screen.blit.assert_called_once_with(
        image,
        (drawer.OFFSET + 1, drawer.OFFSET + 2)
    )


@patch_pygame
def test_drawer_blit_pack(pygame):
    drawer = Drawer(Game())
    image = object()
    drawer.IMAGES = {
        'IMAGE': {Direction.DOWN: image}
    }

    monster = NPC(1, 2)
    monster.set_direction(Direction.DOWN)
    drawer._blit('IMAGE', monster)

    drawer.screen.blit.assert_called_once_with(
        image,
        (drawer.OFFSET + 1, drawer.OFFSET + 2)
    )
