from classes import Player, Enemy, Gem, Location, Game, FileHandler
from classes import (
    NegativePowerError,
    NameError,
    ColorError,
    NegativeHealthError,
    NegativeDamageError
)
import pytest


def test_create_player():
    player = FileHandler().read_from_json('json_files/test_init.json')
    assert player.name() == 'Jurek Ogórek'
    assert player.power() == 5
    assert player.health() == 100


def test_create_player_with_negative_power():
    with pytest.raises(NegativePowerError):
        Player('Jurek Ogórek', power = -1)


def test_create_player_with_negative_health():
    with pytest.raises(NegativeHealthError):
        Player('Jurek Ogórek', power = 5, health = -10)


def test_set_power():
    player = Player('Jurek Ogórek', health=100, power=5)
    assert player.power() == 5
    player.set_power(10)
    assert player.power() == 10


def test_set_power_zero():
    player = Player('Jurek', health=100, power=5)
    assert player.power() == 5
    player.set_power(0)
    assert player.power() == 0


def test_set_power_negative():
    player = Player('Jurek Ogórek', health=100, power=5)
    assert player.power() == 5
    with pytest.raises(NegativePowerError):
        player.set_power(-10)


def test_set_health():
    player = Player('Jurek Ogórek', health=100, power=5)
    assert player.health() == 100
    player.set_health(150)
    assert player.health() == 150


def test_set_health_zero():
    player = Player('Jurek', health=100, power=5)
    assert player.health() == 100
    player.set_health(0)
    assert player.health() == 0


def test_set_health_negative():
    player = Player('Jurek Ogórek', health=100, power=5)
    assert player.health() == 100
    with pytest.raises(NegativeHealthError):
        player.set_health(-10)


def test_move():
    player = FileHandler().read_from_json('json_files/test_init.json')
    assert player.current_location() == (1,1)
    assert player.move('north') == '\n\t\tYou moved north\n'
    assert player.current_location() == (0,1)


def test_move_with_barrier():
    player = FileHandler().read_from_json('json_files/test_init.json')
    assert player.current_location() == (1,1)
    assert player.move('east') == '\n\t\tThere is a barrier. You cannot go there\n'
    assert player.current_location() == (1,1)


def test_move_out_of_range():
    player = FileHandler().read_from_json('json_files/test_init.json')
    assert player.current_location() == (1,1)
    player.move('north')
    assert player.current_location() == (0,1)
    assert player.move('north') == '\n\t\tCannot go north\n'
    assert player.current_location() == (0,1)


def test_move_invalid_direction():
    player = FileHandler().read_from_json('json_files/test_init.json')
    assert player.move('nort') == '\n\t\tInvalid direction\n'


def test_pickup_gems():
    player = FileHandler().read_from_json('json_files/test_init.json')
    player.move('north')
    assert len(player.equipment()) == 1
    assert player.pickup_gems() == "\n\t\tGems were added to your equipment\n"
    assert len(player.equipment()) == 3


def test_pickup_gems_no_gems():
    player = FileHandler().read_from_json('json_files/test_init.json')
    assert len(player.equipment()) == 1
    assert player.pickup_gems() == "\n\t\tThere are no gems here\n"
    assert len(player.equipment()) == 1


def test_use_gem():
    player = FileHandler().read_from_json('json_files/test_init.json')
    assert player.move('east') == '\n\t\tThere is a barrier. You cannot go there\n'
    assert len(player.equipment()) == 1
    assert player.use_gem('east') == '\n\t\tYou used gem and removed barrier.\n'
    assert len(player.equipment()) == 0
    assert player.move('east') == '\n\t\tYou moved east\n'


def test_use_gem_other_color_than_barrier():
    player = FileHandler().read_from_json('json_files/test_init.json')
    assert player.equipment()[0].color() == 'green'
    assert len(player.equipment()) == 1
    assert player.move('west') == '\n\t\tThere is a barrier. You cannot go there\n'
    assert player.use_gem('west') == '\n\t\tYou do not have proper gem to remove this barrier.\n'
    assert len(player.equipment()) == 1


def test_use_gem_empty_equipment():
    player = FileHandler().read_from_json('json_files/test_init.json')
    assert len(player.equipment()) == 1
    player.use_gem('east')
    assert len(player.equipment()) == 0
    assert player.use_gem('south') == '\n\t\tYou do not have proper gem to remove this barrier.\n'


def test_use_gem_no_barrier():
    player = FileHandler().read_from_json('json_files/test_init.json')
    assert len(player.equipment()) == 1
    player.use_gem('east')
    assert len(player.equipment()) == 0
    assert player.use_gem('east') == '\n\t\tThere is no barrier there.\n'


def test_show_equipment():
    player = FileHandler().read_from_json('json_files/test_init.json')
    assert len(player.equipment()) == 1
    assert player.show_equipment() == '\n\t\tYou have green gem\n'


def test_show_equipment_no_items():
    player = FileHandler().read_from_json('json_files/test_init.json')
    assert len(player.equipment()) == 1
    assert player.show_equipment() == '\n\t\tYou have green gem\n'
    player.use_gem('east')
    assert len(player.equipment()) == 0
    assert player.show_equipment() == '\n\t\tYou do not have items.\n'


def test_show_equipment_more_items():
    player = FileHandler().read_from_json('json_files/test_init.json')
    assert len(player.equipment()) == 1
    assert player.show_equipment() == '\n\t\tYou have green gem\n'
    player.move('north')
    player.pickup_gems()
    assert len(player.equipment()) == 3
    assert player.show_equipment() == '\n\t\tYou have green gem, green gem, red gem\n'


def test_look_around():
    player = FileHandler().read_from_json('json_files/test_init.json')
    y = 'You are in S. It is a safe area.'
    gems = 'There are no gems here.'
    en = 'There are no enemies here.'
    e = 'To the east you see P. It has green barrier.'
    w = 'To the west you see L. It has red barrier.'
    n = 'To the north you see GG. It has no barrier.'
    s = 'To the south you see DD. It has green barrier.'
    assert player.look_around() == f'\n\t\t{y}\n\t\t{gems}\n\t\t{en}\n\t\t{e}\n\t\t{w}\n\t\t{n}\n\t\t{s}\n'


def test_look_around_with_enemies_and_gems():
    player = FileHandler().read_from_json('json_files/test_init.json')
    player.move('north')
    y = 'You are in GG. It is a dangerous area.'
    gems = 'You see green gem, red gem.'
    en = 'You see Hydra, Orc.'
    e = 'To the east you see PG. It has green barrier.'
    w = 'To the west you see LG. It has green barrier.'
    n = 'To the north you see Sea North. '
    s = 'To the south you see S. It has no barrier.'
    assert player.look_around() == f'\n\t\t{y}\n\t\t{gems}\n\t\t{en}\n\t\t{e}\n\t\t{w}\n\t\t{n}\n\t\t{s}\n'


def test_take_damage():
    player = FileHandler().read_from_json('json_files/test_init.json')
    assert player.health() == 100
    player.take_damage(50)
    assert player.health() == 50


def test_take_damage_to_zero_health():
    player = FileHandler().read_from_json('json_files/test_init.json')
    assert player.health() == 100
    player.take_damage(100)
    assert player.health() == 0


def test_take_damage_below_zero_health():
    player = FileHandler().read_from_json('json_files/test_init.json')
    assert player.health() == 100
    player.take_damage(150)
    assert player.health() == 0


def test_take_damage_negative():
    player = FileHandler().read_from_json('json_files/test_init.json')
    assert player.health() == 100
    with pytest.raises(NegativeDamageError):
        player.take_damage(-50)


def test_take_damage_zero():
    player = FileHandler().read_from_json('json_files/test_init.json')
    assert player.health() == 100
    player.take_damage(0)
    assert player.health() == 100


def test_attack_1(monkeypatch):
    player = FileHandler().read_from_json('json_files/test_init.json')
    player.move('north')
    assert player.power() == 5

    def return_4(t, d):
        return 4

    monkeypatch.setattr('classes.randint', return_4)
    assert player.attack('Orc') == 'Orc lost 4 points of health. Orc has 1 points of health left.\n'


def test_attack_2(monkeypatch):
    player = FileHandler().read_from_json('json_files/test_init.json')
    player.move('north')
    assert player.power() == 5

    def return_2(t, d):
        return 2

    monkeypatch.setattr('classes.randint', return_2)
    assert player.attack('Hydra') == 'Hydra lost 2 points of health. Hydra has 8 points of health left.\n'


def test_attack_no_power():
    player = FileHandler().read_from_json('json_files/test_init.json')
    player.set_power(0)
    assert player.power() == 0
    assert player.attack('Hydra') == 'You have no power.'


def test_attack_power_eq_1():
    player = FileHandler().read_from_json('json_files/test_init.json')
    player.move('north')
    player.set_power(1)
    assert player.power() == 1
    assert player.attack('Orc') == 'Orc lost 1 points of health. Orc has 4 points of health left.\n'


def test_enemy_attack_1(monkeypatch):
    player = FileHandler().read_from_json('json_files/test_init.json')
    player.move('north')
    assert player.health() == 100

    def return_3(t,d):
        return 3

    monkeypatch.setattr('classes.randint', return_3)
    assert player.enemy_attack('Hydra') == 'You lost 3 points of health. You have 97 points of health left.\n'


def test_enemy_attack_2(monkeypatch):
    player = FileHandler().read_from_json('json_files/test_init.json')
    player.move('north')
    assert player.health() == 100

    def return_10(t,d):
        return 10

    monkeypatch.setattr('classes.randint', return_10)
    assert player.enemy_attack('Orc') == 'You lost 10 points of health. You have 90 points of health left.\n'


def test_enemy_attack_all_players_health(monkeypatch):
    player = FileHandler().read_from_json('json_files/test_init.json')
    player.move('north')
    assert player.health() == 100

    def return_100(t,d):
        return 100

    monkeypatch.setattr('classes.randint', return_100)
    assert player.enemy_attack('Orc') == 'You lost 100 points of health. You have 0 points of health left.\n\n\t\tYou died.'


def test_enemy_attack_above_players_health(monkeypatch):
    player = FileHandler().read_from_json('json_files/test_init.json')
    player.move('north')
    assert player.health() == 100

    def return_150(t,d):
        return 150

    monkeypatch.setattr('classes.randint', return_150)
    assert player.enemy_attack('Orc') == 'You lost 150 points of health. You have 0 points of health left.\n\n\t\tYou died.'


def test_fight_1(monkeypatch):
    player = FileHandler().read_from_json('json_files/test_init.json')
    player.move('north')

    def return_10(t,d):
        return 10

    monkeypatch.setattr('classes.randint', return_10)
    assert player.fight('Hydra') == '\n\t\tHydra lost 10 points of health. Hydra has 0 points of health left.\n\n\t\tHydra died.\n'


def test_fight_2(monkeypatch):
    player = FileHandler().read_from_json('json_files/test_init.json')
    player.move('north')

    def return_5(t,d):
        return 5

    monkeypatch.setattr('classes.randint', return_5)
    h1 = '\n\t\tHydra lost 5 points of health. Hydra has 5 points of health left.\n'
    h2 = '\n\t\tYou lost 5 points of health. You have 95 points of health left.\n'
    h3 = '\n\t\tHydra lost 5 points of health. Hydra has 0 points of health left.\n'
    assert player.fight('Hydra') == f'{h1}{h2}{h3}\n\t\tHydra died.\n'


def test_fight_player_dies(monkeypatch):
    player = FileHandler().read_from_json('json_files/test_init.json')
    player.move('north')
    player.set_health(5)

    def return_5(t,d):
        return 5

    monkeypatch.setattr('classes.randint', return_5)
    h1 = '\n\t\tHydra lost 5 points of health. Hydra has 5 points of health left.\n'
    h2 = '\n\t\tYou lost 5 points of health. You have 0 points of health left.\n'
    assert player.fight('Hydra') == f'{h1}{h2}\n\t\tYou died.\n'


def test_did_win():
    player = FileHandler().read_from_json('json_files/test_init.json')
    assert player.did_win() is not True


def test_did_win_no_enemies():
    player = Player('Jurek')
    assert player.did_win() is True


def test_did_win_killed_enemies():
    player = FileHandler().read_from_json('json_files/test_init.json')
    assert player.did_win() is not True
    player.move('north')
    player.fight('Hydra')
    player.fight('Orc')
    assert player.did_win() is True


def test_rest():
    player = FileHandler().read_from_json('json_files/test_init.json')
    assert player.health() == 100
    player.move('north')
    player.fight('Hydra')
    assert player.health() < 100
    assert player.rest() == '\n\t\tYour health points have been restored.\n'
    assert player.health() == 100


def test_enemy_info_1():
    player = FileHandler().read_from_json('json_files/test_init.json')
    player.move('north')
    name = '\n\t\tThis is Hydra.'
    health = '\n\t\tIt has 10 health points.'
    power = '\n\t\tIt has 5 power points.\n'
    assert player.enemy_info('Hydra') == f'{name}{health}{power}'


def test_enemy_info_2():
    player = FileHandler().read_from_json('json_files/test_init.json')
    player.move('north')
    name = '\n\t\tThis is Orc.'
    health = '\n\t\tIt has 5 health points.'
    power = '\n\t\tIt has 5 power points.\n'
    assert player.enemy_info('Orc') == f'{name}{health}{power}'


def test_action_move():
    player = FileHandler().read_from_json('json_files/test_init.json')
    assert player.action('move north') == '\n\t\tYou moved north\n'


def test_action_move_too_long():
    player = FileHandler().read_from_json('json_files/test_init.json')
    assert player.action('move north fast') == 'Invalid action.'


def test_action_use_gem():
    player = FileHandler().read_from_json('json_files/test_init.json')
    assert player.action('use gem east') == '\n\t\tYou used gem and removed barrier.\n'


def test_action_use_gem_too_long():
    player = FileHandler().read_from_json('json_files/test_init.json')
    assert player.action('use gem east fast') == 'Invalid action.'


def test_action_pickup_gems():
    player = FileHandler().read_from_json('json_files/test_init.json')
    player.move('north')
    assert player.action('pickup gems') == '\n\t\tGems were added to your equipment\n'


def test_action_look_around():
    player = FileHandler().read_from_json('json_files/test_init.json')
    y = 'You are in S. It is a safe area.'
    gems = 'There are no gems here.'
    en = 'There are no enemies here.'
    e = 'To the east you see P. It has green barrier.'
    w = 'To the west you see L. It has red barrier.'
    n = 'To the north you see GG. It has no barrier.'
    s = 'To the south you see DD. It has green barrier.'
    assert player.action('look around') == f'\n\t\t{y}\n\t\t{gems}\n\t\t{en}\n\t\t{e}\n\t\t{w}\n\t\t{n}\n\t\t{s}\n'


def test_action_fight(monkeypatch):
    player = FileHandler().read_from_json('json_files/test_init.json')
    player.move('north')

    def return_10(t,d):
        return 10

    monkeypatch.setattr('classes.randint', return_10)
    assert player.action('fight hydra') == '\n\t\tHydra lost 10 points of health. Hydra has 0 points of health left.\n\n\t\tHydra died.\n'


def test_action_rest():
    player = FileHandler().read_from_json('json_files/test_init.json')
    assert player.health() == 100
    player.move('north')
    player.fight('Hydra')
    assert player.health() < 100
    assert player.action('rest') == '\n\t\tYour health points have been restored.\n'
    assert player.health() == 100


def test_action_show_equipment():
    player = FileHandler().read_from_json('json_files/test_init.json')
    assert len(player.equipment()) == 1
    assert player.action('show equipment') == '\n\t\tYou have green gem\n'


def test_action_show_stats():
    player = FileHandler().read_from_json('json_files/test_init.json')
    name = '\t\tMy name is Jurek Ogórek.'
    power = '\t\tMy current power is 5.'
    health = '\t\tMy current health is 100.'
    assert player.action('show stats') == f'\n{name}\n{power}\n{health}\n'


def test_action_enemy_info():
    player = FileHandler().read_from_json('json_files/test_init.json')
    player.move('north')
    name = '\n\t\tThis is Hydra.'
    health = '\n\t\tIt has 10 health points.'
    power = '\n\t\tIt has 5 power points.\n'
    assert player.action('enemy info Hydra') == f'{name}{health}{power}'


def test_action_help():
    player = FileHandler().read_from_json('json_files/test_init.json')
    se = "'show equipment' - shows player's current equipment"
    ss = "'show stats' - shows player's current stats"
    pg = "'pickup gems' - pickups all gems from current location"
    ug = ("'use gem (direction)' - uses proper gem from equipment"
            + "and removes barrier")
    la = "'look around' - shows info about current location"
    mo = "'move (direction)' - moves player to new location"
    fi = "'fight (enemy)' - player fights with chosen enemy"
    re = "'rest' - restores player's health"
    en = "'enemy info (enemy)' - shows info about enemy"
    save = "'save (path to file)' - saves game to chosen file"
    exit = "'exit' - closes the game"
    help = "'help' - shows list of commends"
    assert player.action('help') == f"""
        \tList of commands:
        \t{se}
        \t{ss}
        \t{pg}
        \t{ug}
        \t{la}
        \t{mo}
        \t{fi}
        \t{re}
        \t{en}
        \t{save}
        \t{exit}
        \t{help}
        """


def test_action_save():
    player = FileHandler().read_from_json('json_files/test_init.json')
    assert player.action('save json_files/test_save.json') == '\n\t\tsaved to json_files/test_save.json\n'


def test_action_invalid():
    player = FileHandler().read_from_json('json_files/test_init.json')
    assert player.action('move north fast') == 'Invalid action.'
    assert player.action('use gem east fast') == 'Invalid action.'
    assert player.action('pickup gems now') == 'Invalid action.'
    assert player.action('look around now') == 'Invalid action.'
    assert player.action('fight hydra now') == 'Invalid action.'
    assert player.action('rest now') == 'Invalid action.'
    assert player.action('show equipment now') == 'Invalid action.'
    assert player.action('show stats now') == 'Invalid action.'
    assert player.action('enemy info Hydra now') == 'Invalid action.'
    assert player.action('help me') == 'Invalid action.'


def test_help():
    player = FileHandler().read_from_json('json_files/test_init.json')
    se = "'show equipment' - shows player's current equipment"
    ss = "'show stats' - shows player's current stats"
    pg = "'pickup gems' - pickups all gems from current location"
    ug = ("'use gem (direction)' - uses proper gem from equipment"
            + "and removes barrier")
    la = "'look around' - shows info about current location"
    mo = "'move (direction)' - moves player to new location"
    fi = "'fight (enemy)' - player fights with chosen enemy"
    re = "'rest' - restores player's health"
    en = "'enemy info (enemy)' - shows info about enemy"
    save = "'save (path to file)' - saves game to chosen file"
    exit = "'exit' - closes the game"
    help = "'help' - shows list of commends"
    assert player.help() == f"""
        \tList of commands:
        \t{se}
        \t{ss}
        \t{pg}
        \t{ug}
        \t{la}
        \t{mo}
        \t{fi}
        \t{re}
        \t{en}
        \t{save}
        \t{exit}
        \t{help}
        """


def test_info():
    player = FileHandler().read_from_json('json_files/test_init.json')
    name = '\t\tMy name is Jurek Ogórek.'
    power = '\t\tMy current power is 5.'
    health = '\t\tMy current health is 100.'
    assert player.info() == f'\n{name}\n{power}\n{health}\n'


def test_str():
    player = FileHandler().read_from_json('json_files/test_init.json')
    name = '\t\tMy name is Jurek Ogórek.'
    power = '\t\tMy current power is 5.'
    health = '\t\tMy current health is 100.'
    assert str(player) == f'\n{name}\n{power}\n{health}\n'


def test_enemy_info_no_enemy():
    player = FileHandler().read_from_json('json_files/test_init.json')
    assert player.enemy_info('Elf') == "\n\t\tThere is no enemy named Elf\n"


def test_introduce():
    player = Player('Jurek Ogorek', (1,1), [], 3, 100, [])
    assert player.__str__() == '\n\t\tMy name is Jurek Ogorek.\n\t\tMy current power is 3.\n\t\tMy current health is 100.\n'


def test_introduce_as_str():
    player = Player('Jurek Ogórek', power = 3, health = 100)
    assert str(player) == player.info()


def test_enemy_create():
    enemy = Enemy('orc', 50, 5)
    assert enemy.name() == 'orc'
    assert enemy.health() == 50
    assert enemy.power() == 5


def test_enemy_create_negative_health():
    with pytest.raises(NegativeHealthError):
        Enemy('orc', -10, 3)


def test_enemy_create_mpty_name():
    with pytest.raises(NameError):
        Enemy('', 10, 10)


def test_enemy_set_health():
    enemy = Enemy('orc', 50, 4)
    assert enemy.health() == 50
    enemy.set_health(60)
    assert enemy.health() == 60


def test_enemy_set_health_negative():
    enemy = Enemy('orc', 50, 10)
    assert enemy.health() == 50
    enemy.set_health(-10)
    assert enemy.health() == 0


def test_enemy_description():
    enemy = Enemy('Orc', 40, 5)
    assert str(enemy) == '\n\t\tThis is Orc.\n\t\tIt has 40 health points.\n\t\tIt has 5 power points.\n'


def test_enemy_take_damage():
    enemy = Enemy('orc', 40, 5)
    assert enemy.health() == 40
    assert enemy.power() == 5
    assert enemy.take_damage(10) is True
    assert enemy.health() == 30


def test_enemy_take_damage_invalid():
    enemy = Enemy('orc', 40, 5)
    with pytest.raises(ValueError):
        enemy.take_damage(-10)
    with pytest.raises(ValueError):
        enemy.take_damage(0)


def test_enemy_take_damage_drops_below_zero():
    enemy = Enemy('orc', 10, 5)
    assert enemy.health() == 10
    assert enemy.take_damage(30) is True
    assert enemy.health() == 0


def test_enemy_is_alive_true():
    enemy = Enemy('orc', 10, 5)
    assert enemy.health() == 10
    assert enemy.is_alive()


def test_enemy_is_alive():
    enemy = Enemy('orc', 10, 5)
    assert enemy.health() == 10
    assert enemy.is_alive()
    enemy.take_damage(20)
    assert enemy.health() == 0
    assert not enemy.is_alive()


def test_enemy_is_alive_false():
    enemy = Enemy('orc', 0, 5)
    assert enemy.health() == 0
    assert not enemy.is_alive()


def test_gem_create():
    gem = Gem('green gem', 'green')
    assert gem.name() == 'green gem'
    assert gem.color() == 'green'


def test_gem_create_no_name():
    with pytest.raises(NameError):
        gem = Gem('', 'green')


def test_gem_create_no_color():
    with pytest.raises(ColorError):
        gem = Gem('green gem', '')


def test_location_create():
    location = Location('Forest', 'There are trees here.')
    assert location.name() == 'Forest'
    assert location.description() == 'There are trees here.'


def test_location_set_barrier():
    location = Location('Forest', 'There are trees here.', 0)
    assert location.name() == 'Forest'
    assert location.description() == 'There are trees here.'
    assert location.barrier() == 0
    location.set_barrier(1)
    assert location.barrier() == 1


def test_location_clear_items():
    location = Location('Forest', 'There are trees here.', items=[Gem('green gem', 'green'), Gem('red gem', 'red')])
    assert location.name() == 'Forest'
    assert location.description() == 'There are trees here.'
    assert len(location.items()) == 2
    location.clear_items()
    assert len(location.items()) == 0


def test_location_remove_barrier():
    location = Location('Forest', 'There are trees here.', 1)
    assert location.name() == 'Forest'
    assert location.description() == 'There are trees here.'
    assert location.barrier() == 1
    location.remove_barrier()
    assert location.barrier() == 0


def test_game_create():
    game = Game()
    game.player = FileHandler().read_from_json('json_files/test_init.json')
    assert game.player.power() == 5
    assert game.player.health() == 100


def test_game_create_default_enemies():
    game = Game()
    game.player = FileHandler().read_from_json('json_files/test_init.json')
    hydra = game.player.locations()[0][1].enemies()[0]
    orc = game.player.locations()[0][1].enemies()[1]
    assert hydra.name() == 'Hydra'
    assert hydra.health() == 10
    assert hydra.power() == 5
    assert orc.name() == 'Orc'
    assert orc.health() == 5
    assert orc.power() == 5
