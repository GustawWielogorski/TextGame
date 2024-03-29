import json
from random import randint


class NegativePowerError(Exception):
    def __init__(self, power):
        super().__init__('Power cannot be negative')
        self.power = power


class NameError(Exception):
    pass


class ColorError(Exception):
    pass


class NegativeHealthError(Exception):
    def __init__(self, health):
        super().__init__('Health cannot be negative')
        self.health = health


class NegativeDamageError(Exception):
    pass


class InvalidDirectionError(Exception):
    pass


class FilePathNotFound(Exception):
    pass


class FileHandler():
    def read_from_json(self, path):
        with open(path, 'r') as file_handle:
            players_map = []
            map = []
            data = json.load(file_handle)
            map_size = data['map_size']
            for item in data['player']:
                gems_eq = []
                try:
                    p_name = item['name']
                    player_x, player_y = item['current_location'].split(',')
                    current_location = int(player_x), int(player_y)
                    power = item['power']
                    health = item['health']
                    equipment = item['equipment']
                    locations = item['locations']
                    for p_item in equipment:
                        try:
                            gp_name = p_item['name']
                            gp_color = p_item['color']
                        except KeyError:
                            raise KeyError('Missing key in file')
                        gems_eq.append(Gem(gp_name, gp_color))
                    for location in locations:
                        enemies_loc = []
                        gems_loc = []
                        try:
                            x = location['x']
                            y = location['y']
                            name = location['name']
                            description = location['description']
                            barrier = location['barrier']
                            barrier_color = location['barrier_color']
                            enemies = location['enemies']
                            gems = location['gems']
                            for enemy in enemies:
                                try:
                                    e_name = enemy['name']
                                    e_health = enemy['health']
                                    e_power = enemy['power']
                                    enemy_class = Enemy(e_name, e_health,
                                                        e_power)
                                except KeyError:
                                    raise KeyError('Missing key in file')
                                enemies_loc.append(enemy_class)
                            for gem in gems:
                                try:
                                    g_name = gem['name']
                                    g_color = gem['color']
                                    gem_class = Gem(g_name, g_color)
                                except KeyError:
                                    raise KeyError('Missing key in file')
                                gems_loc.append(gem_class)
                        except KeyError:
                            raise KeyError('Missing key in file')
                        loc = Location(name,
                                       description,
                                       barrier,
                                       barrier_color,
                                       enemies_loc,
                                       gems_loc,
                                       x,
                                       y)
                        map.append(loc)
                except KeyError as e:
                    raise KeyError('Missing key in file') from e
            map_tuple = map_size, map
            for i in range(map_tuple[0]):
                players_map.append(list(range(map_tuple[0])))
            for place in map_tuple[1]:
                players_map[place._x][place._y] = place
            player = Player(p_name, current_location, players_map, power,
                            health, gems_eq)
            return player

    def save_to_json(self, path, player_info):
        with open(path, 'w') as file_handle:
            data = []
            map_size = len(player_info.locations())
            player_name = player_info.name()
            player_current_location = str(player_info.current_location())[1:-1]
            player_current_location = player_current_location.replace(' ', '')
            player_power = player_info.power()
            player_health = player_info.health()
            player_equipment = []
            locations = []
            for item in player_info.equipment():
                gem_name = item.name()
                gem_color = item.color()
                gem = {
                    'name': gem_name,
                    'color': gem_color
                }
                player_equipment.append(gem)
            for list in player_info.locations():
                for item in list:
                    x = item.x()
                    y = item.y()
                    name = item.name()
                    description = item.description()
                    barrier = item.barrier()
                    barrier_color = item.barrier_color()
                    enemies = []
                    gems = []
                    for enemy in item.enemies():
                        enemy_name = enemy.name()
                        enemy_health = enemy.health()
                        enemy_power = enemy.power()
                        en = {
                            'name': enemy_name,
                            'health': enemy_health,
                            'power': enemy_power
                        }
                        enemies.append(en)
                    for g in item.items():
                        g_name = g.name()
                        g_color = g.color()
                        ge = {
                            'name': g_name,
                            'color': g_color
                        }
                        gems.append(ge)
                    location = {
                        'x': x,
                        'y': y,
                        'name': name,
                        'description': description,
                        'barrier': barrier,
                        'barrier_color': barrier_color,
                        'enemies': enemies,
                        'gems': gems
                    }
                    locations.append(location)
            player_data = [{
                'name': player_name,
                'current_location': player_current_location,
                'power': player_power,
                'health': player_health,
                'equipment': player_equipment,
                'locations': locations
            }]
            data_final = {
                'map_size': map_size,
                'player': player_data
            }
            data.append(data_final)
            json.dump(data_final, file_handle, indent=4)


class Player:
    """
    Class Player. Contains attributes:
    :param name: player's name
    :type name: str
    :param current_location: player's current location
    :type current_location: tuple
    :param locations: map of locations
    :type locations: list
    :param power: player's power
    :type power: int
    :param health: player's health
    :type health: int
    :param equipment: player's equipment
    :param type: list
    """
    def __init__(self,
                 name,
                 current_location=None,
                 locations=[],
                 power=5,
                 health=100,
                 equipment=[]):
        if not name:
            raise NameError('Name cannot be empty.')
        self._name = name
        power = int(power)
        if power < 0:
            raise NegativePowerError(power)
        if health < 0:
            raise NegativeHealthError(health)
        self._power = int(power)
        self._current_location = current_location
        self._locations = locations
        self._equipment = equipment
        self._health = health
        self._base_health = health

    def name(self):
        """
        Returns player's name.
        """
        return self._name

    def power(self):
        """
        Returns player's power.
        """
        return self._power

    def health(self):
        """
        Returns player's health.
        """
        return self._health

    def current_location(self):
        """
        Returns player's current_location.
        """
        return self._current_location

    def locations(self):
        """
        Returns player's locations.
        """
        return self._locations

    def equipment(self):
        """
        Returns player's equipment.
        """
        return self._equipment

    def set_power(self, new_power):
        """
        Sets player's power.
        """
        if new_power < 0:
            raise NegativePowerError(new_power)
        self._power = int(new_power)

    def set_health(self, new_health):
        """
        Sets player's health.
        """
        if new_health < 0:
            raise NegativeHealthError(new_health)
        self._health = new_health

    def move_east(self):
        x, y = self._current_location[0], self._current_location[1]
        is_barrier = '\n\t\tThere is a barrier. You cannot go there\n'
        if y+1 == len(self._locations):
            return '\n\t\tCannot go east\n'
        east = self._locations[x][y+1]
        if east._barrier:
            return is_barrier
        self._current_location = (x, y + 1)
        return '\n\t\tYou moved east\n'

    def move_west(self):
        x, y = self._current_location[0], self._current_location[1]
        is_barrier = '\n\t\tThere is a barrier. You cannot go there\n'
        if y == 0:
            return '\n\t\tCannot go west\n'
        west = self._locations[x][y-1]
        if west._barrier:
            return is_barrier
        self._current_location = (x, y - 1)
        return '\n\t\tYou moved west\n'

    def move_north(self):
        x, y = self._current_location[0], self._current_location[1]
        is_barrier = '\n\t\tThere is a barrier. You cannot go there\n'
        if x == 0:
            return '\n\t\tCannot go north\n'
        north = self._locations[x-1][y]
        if north._barrier:
            return is_barrier
        self._current_location = (x - 1, y)
        return '\n\t\tYou moved north\n'

    def move_south(self):
        x, y = self._current_location[0], self._current_location[1]
        is_barrier = '\n\t\tThere is a barrier. You cannot go there\n'
        if x+1 == len(self._locations):
            return '\n\t\tCannot go south\n'
        south = self._locations[x+1][y]
        if south._barrier:
            return is_barrier
        self._current_location = (x + 1, y)
        return '\n\t\tYou moved south\n'

    def move(self, direction):
        """
        Moves player to another location if location does not have barrier.
        Changes player's current location.
        """
        if direction not in ['east', 'west', 'north', 'south']:
            return '\n\t\tInvalid direction\n'
        x, y = self._current_location[0], self._current_location[1]
        self._locations[x][y].remove_barrier()
        if direction == 'east':
            return self.move_east()
        if direction == 'west':
            return self.move_west()
        if direction == 'north':
            return self.move_north()
        if direction == 'south':
            return self.move_south()

    def pickup_gems(self):
        """
        Adds all gems that are in the area to player's equipment.
        Removes gems from location.
        """
        x, y = self._current_location[0], self._current_location[1]
        location = self._locations[x][y]
        gems = location._items
        if not gems:
            return "\n\t\tThere are no gems here\n"
        else:
            for gem in gems:
                self._equipment.append(gem)
            location.clear_items()
            return "\n\t\tGems were added to your equipment\n"

    def use_gem(self, direction):
        """
        Uses gem from player's equipment to remove barrier
        if player has proper gem.
        """
        if direction not in ['east', 'west', 'north', 'south']:
            return '\n\t\tInvalid direction\n'
        x, y = self._current_location[0], self._current_location[1]
        east = self._locations[x][y+1]
        west = self._locations[x][y-1]
        north = self._locations[x-1][y]
        south = self._locations[x+1][y]
        length_of_eq = len(self._equipment)
        if direction == 'east':
            direction = east
        if direction == 'west':
            direction = west
        if direction == 'north':
            direction = north
        if direction == 'south':
            direction = south
        if not direction._barrier:
            return '\n\t\tThere is no barrier there.\n'
        for gem in self._equipment:
            if gem._color == direction._barrier_color:
                direction.remove_barrier()
                self._equipment.remove(gem)
        if len(self._equipment) == length_of_eq:
            return '\n\t\tYou do not have proper gem to remove this barrier.\n'
        return '\n\t\tYou used gem and removed barrier.\n'

    def show_equipment(self):
        """
        Returns players current equipment.
        """
        index = 0
        equipment_description = 'You have '
        for item in self._equipment:
            if index == 0:
                equipment_description += item._name
                index += 1
            else:
                equipment_description += f', {item._name}'
        if not self._equipment:
            return '\n\t\tYou do not have items.\n'
        return f'\n\t\t{equipment_description}\n'

    def look_east(self):
        x, y = self._current_location[0], self._current_location[1]
        if y+1 == len(self._locations):
            name_e = 'Sea East'
            barrier_description_e = ''
        else:
            east = self._locations[x][y+1]
            name_e = east._name
            if east._barrier:
                barrier_description_e = (f'It has {east._barrier_color}'
                                         + ' barrier.')
            else:
                barrier_description_e = 'It has no barrier.'
        return name_e, barrier_description_e

    def look_west(self):
        x, y = self._current_location[0], self._current_location[1]
        if y == 0:
            name_w = 'Sea West'
            barrier_description_w = ''
        else:
            west = self._locations[x][y-1]
            name_w = west._name
            if west._barrier:
                barrier_description_w = (f'It has {west._barrier_color}'
                                         + ' barrier.')
            else:
                barrier_description_w = 'It has no barrier.'
        return name_w, barrier_description_w

    def look_north(self):
        x, y = self._current_location[0], self._current_location[1]
        if x == 0:
            name_n = 'Sea North'
            barrier_description_n = ''
        else:
            north = self._locations[x-1][y]
            name_n = north._name
            if north._barrier:
                barrier_description_n = (f'It has {north._barrier_color}'
                                         + ' barrier.')
            else:
                barrier_description_n = 'It has no barrier.'
        return name_n, barrier_description_n

    def look_south(self):
        x, y = self._current_location[0], self._current_location[1]
        if x+1 == len(self._locations):
            name_s = 'Sea South'
            barrier_description_s = ''
        else:
            south = self._locations[x+1][y]
            name_s = south._name
            if south._barrier:
                barrier_description_s = (f'It has {south._barrier_color}'
                                         + ' barrier.')
            else:
                barrier_description_s = 'It has no barrier.'
        return name_s, barrier_description_s

    def look_around(self):
        """
        Returns info about current player's location and
        locations next to player.
        """
        x, y = self._current_location[0], self._current_location[1]
        location = self._locations[x][y]
        name_e, barrier_description_e = self.look_east()
        name_w, barrier_description_w = self.look_west()
        name_n, barrier_description_n = self.look_north()
        name_s, barrier_description_s = self.look_south()
        index_enemies = 0
        if location._enemies:
            enemies_description = 'You see '
            for enemy in location._enemies:
                if index_enemies == 0:
                    enemies_description += enemy._name
                    index_enemies += 1
                else:
                    enemies_description += f', {enemy._name}'
        else:
            enemies_description = 'There are no enemies here'
        index_items = 0
        if location._items:
            items_description = 'You see '
            for item in location._items:
                if index_items == 0:
                    items_description += f'{item._color} gem'
                    index_items += 1
                else:
                    items_description += f', {item._color} gem'
        else:
            items_description = 'There are no gems here'
        you = f"You are in {location._name}. {location._description}"
        items = f"{items_description}."
        en = f"{enemies_description}."
        east_d = f"To the east you see {name_e}. {barrier_description_e}"
        west_d = f"To the west you see {name_w}. {barrier_description_w}"
        north_d = f"To the north you see {name_n}. {barrier_description_n}"
        south_d = f"To the south you see {name_s}. {barrier_description_s}"
        return (f"\n\t\t{you}\n\t\t{items}\n\t\t{en}\n\t\t{east_d}"
                + f"\n\t\t{west_d}\n\t\t{north_d}\n\t\t{south_d}\n")

    def take_damage(self, damage):
        """
        Removes damage points from player's health.
        """
        damage = int(damage)
        if damage < 0:
            raise NegativeDamageError('Damage cannot be negative.')
        self._health -= min(damage, self._health)

    def attack(self, name_of_enemy):
        """
        Removes random amount of damage points from enemy's health points.
        """
        x, y = self._current_location[0], self._current_location[1]
        location = self._locations[x][y]
        if self.power() == 0:
            return 'You have no power.'
        if not location._enemies:
            return 'There are no enemies to attack.'
        for enemy in location._enemies:
            en = enemy._name
            if name_of_enemy == enemy._name:
                damage = randint(1, self.power())
                enemy.take_damage(damage)
                return (f'{enemy._name} lost {damage} points of health.' +
                        f' {en} has {enemy._health} points of health left.\n')

    def enemy_attack(self, name_of_enemy):
        """
        Enemy removes random amound of damage points
        from player's health points
        """
        x, y = self._current_location[0], self._current_location[1]
        location = self._locations[x][y]
        for enemy in location._enemies:
            if name_of_enemy == enemy._name:
                damage = randint(1, enemy.power())
                self.take_damage(damage)
                if self._health <= 0:
                    self._health = 0
                    return (f'You lost {damage} points of health.'
                            + f' You have {self._health} points of health'
                            + ' left.\n\n\t\tYou died.')
                return (f'You lost {damage} points of health.'
                        + f' You have {self._health} points of health left.\n')

    def fight(self, name_of_enemy):
        """
        Removes health points of player and enemy until one has no
        health points left.
        """
        x, y = self._current_location[0], self._current_location[1]
        location = self._locations[x][y]
        fight = '\n'
        for enemy in location._enemies:
            if name_of_enemy == enemy._name:
                while enemy.is_alive():
                    if self._health == 0:
                        break
                    fight += f'\t\t{self.attack(name_of_enemy)}\n'
                    if enemy._health == 0:
                        fight += f'\t\t{enemy._name} died.\n'
                        location._enemies.remove(enemy)
                        break
                    fight += f'\t\t{(self.enemy_attack(name_of_enemy))}\n'
                return fight

    def did_win(self):
        """
        Returns True if there are no enemies left on map.
        """
        enemies_total = []
        for row in self._locations:
            for column in row:
                for enemy in column._enemies:
                    enemies_total.append(enemy)
        if not enemies_total:
            return True

    def rest(self):
        """
        Restores player's health points to base value.
        """
        self.set_health(self._base_health)
        return '\n\t\tYour health points have been restored.\n'

    def enemy_info(self, name_of_enemy):
        x, y = self._current_location[0], self._current_location[1]
        location = self._locations[x][y]
        for enemy in location._enemies:
            if name_of_enemy == enemy._name:
                return enemy.__str__()
            else:
                continue
        return f"\n\t\tThere is no enemy named {name_of_enemy}\n"

    def action(self, action):
        """
        Returns method proper to user's input.
        """
        action = action.lower().split()
        if action[0] == 'move' and len(action) == 2:
            return self.move(action[1])
        if action[0] == 'use' and action[1] == 'gem' and len(action) == 3:
            return self.use_gem(action[2])
        if action[0] == 'pickup' and action[1] == 'gems' and len(action) == 2:
            return self.pickup_gems()
        if action[0] == 'look' and action[1] == 'around' and len(action) == 2:
            return self.look_around()
        if action[0] == 'fight':
            enemy_name = ''
            for item in action[1:-1]:
                enemy_name += f"{item} "
            enemy_name += action[-1]
            fight = self.fight(enemy_name.title())
            if fight is None:
                return 'Invalid action.'
            return fight
        if action[0] == 'rest' and len(action) == 1:
            return self.rest()
        if (action[0] == 'show' and action[1] == 'equipment'
                and len(action) == 2):
            return self.show_equipment()
        if action[0] == 'show' and action[1] == 'stats' and len(action) == 2:
            return self.__str__()
        if action[0] == 'enemy' and action[1] == 'info' and len(action) == 3:
            return self.enemy_info(action[2].title())
        if action[0] == 'help' and len(action) == 1:
            return self.help()
        if action[0] == 'save' and len(action) == 2:
            try:
                FileHandler().save_to_json(action[1], self)
                return f'\n\t\tsaved to {action[1]}\n'
            except PermissionError:
                raise PermissionError("Missing permissions to open file")
            except IsADirectoryError:
                raise IsADirectoryError('Can only work on files')
        return 'Invalid action.'

    def help(self):
        """
        Returns commands used in game.
        """
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

        comms = f"""
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
        return comms

    def info(self):
        """
        Returns basic description of the player.
        """
        name = f'\t\tMy name is {self._name}.'
        power = f'\t\tMy current power is {self._power}.'
        health = f'\t\tMy current health is {self._health}.'
        return f'\n{name}\n{power}\n{health}\n'

    def __str__(self):
        return self.info()


class Enemy:
    """
    Class Enemy. Contains attributes:
    :param name: enemy's name
    :type name: str

    :param health: enemy's health points
    :type health: int
    """
    def __init__(self, name, health, power):
        """
        Creates instance of Enemy.

        Raises ValueError if name is empty or health is negative.
        """
        if not name:
            raise NameError('Name cannot be empty')
        health = int(health)
        power = int(power)
        if health < 0:
            raise NegativeHealthError(health)
        if power < 0:
            raise NegativePowerError(power)
        self._name = name
        self._health = health
        self._power = power

    def name(self):
        """
        Returns name of the enemy enemy.
        """
        return self._name

    def health(self):
        """
        Returns health of enemy.
        """
        return self._health

    def set_health(self, new_health):
        """
        Sets health of enemy.
        """
        self._health = max(0, new_health)

    def power(self):
        """
        Returns power of enemy.
        """
        return self._power

    def __str__(self):
        """
        Returns info about enemy.
        """
        name = f'\n\t\tThis is {self._name}.'
        health = f'\n\t\tIt has {self._health} health points.'
        power = f'\n\t\tIt has {self._power} power points.\n'
        return name + health + power

    def take_damage(self, damage):
        """
        Reduces health of enemy by damage.
        """
        damage = int(damage)
        if damage <= 0:
            raise ValueError('Damage has to be positive')
        self._health -= min(damage, self._health)
        return True

    def is_alive(self):
        """
        Returns True if health is greater than 0.
        """
        return self._health > 0


class Gem:
    def __init__(self, name, color):
        if not name:
            raise NameError('Name cannot be empty')
        self._name = name
        if not color:
            raise ColorError('Color name cannot be empty')
        self._color = color

    def name(self):
        return self._name

    def color(self):
        return self._color


class Location:
    def __init__(self,
                 name,
                 description=None,
                 barrier=None,
                 barrier_color=None,
                 enemies=[],
                 items=None,
                 x=None,
                 y=None):
        self._name = name
        self._barrier = barrier
        self._barrier_color = barrier_color
        self._enemies = enemies
        self._description = description
        self._items = items
        self._x = x
        self._y = y

    def name(self):
        return self._name

    def barrier(self):
        return self._barrier

    def set_barrier(self, y_n):
        self._barrier = y_n

    def barrier_color(self):
        return self._barrier_color

    def enemies(self):
        return self._enemies

    def items(self):
        return self._items

    def x(self):
        return self._x

    def y(self):
        return self._y

    def clear_items(self):
        self._items = []

    def description(self):
        return self._description

    def remove_barrier(self):
        self._barrier = False

    def __str__(self):
        return f'{self._description}'


class Game:
    def init_player(self):
        self.player = None
        while True:
            p = '\n\t\tLoad saved game? (yes "path to game file"/no)\n\n> '
            load = input(p).split()
            if load[0] == 'no':
                init = 'json_files/init.json'
                self.player = FileHandler().read_from_json(init)
            elif load[0] == 'yes':
                try:
                    f = f'json_files/{load[1]}'
                    self.player = FileHandler().read_from_json(f)
                except FileNotFoundError:
                    print(FilePathNotFound('Could not open this file'))
                except PermissionError:
                    print(PermissionError("Missing permissions to open file"))
                except IsADirectoryError:
                    print(IsADirectoryError('Can only work on files'))
                if not self.player:
                    continue
            else:
                print('Wrong input, try again.')
                continue
            return self.player

    def play(self):
        print('\n\t\tStarting game')
        print(self.player.help())
        while True:
            user_input = input('> ')
            if user_input == ('exit'):
                break
            print(self.player.action(user_input))
            if self.player.did_win():
                print('\t\tYou won\n')
                break
            if self.player._health == 0:
                print('\t\tYou lost\n')
                break
