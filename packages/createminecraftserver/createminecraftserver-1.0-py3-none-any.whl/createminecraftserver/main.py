import time
import os
import signal
import subprocess
from pathlib import Path
from shutil import which
import readline
import json
import yaml
from urllib import request
import re
from packaging import version
from nbt.nbt import *


def sigint_handler():
    print('\n\nAborted.')
    sys.exit(0)


common_gamerules = {
    'commandBlockOutput': {'type': 'bool', 'default': 'true', 'since': '1.4.2'},
    'doDaylightCycle': {'type': 'bool', 'default': 'true', 'since': '1.6.1'},
    'doMobSpawning': {'type': 'bool', 'default': 'true', 'since': '1.4.2'},
    'doWeatherCycle': {'type': 'bool', 'default': 'true', 'since': '1.11'},
    'keepInventory': {'type': 'bool', 'default': 'false', 'since': '1.4.2'},
    'naturalRegeneration': {'type': 'bool', 'default': 'true', 'since': '1.6.1'},
    'playersSleepingPercentage': {'type': 'int', 'default': '100', 'since': '1.17'},
    'sendCommandFeedback': {'type': 'bool', 'default': 'true', 'since': '1.8'},
    'spawnRadius': {'type': 'int', 'default': '10', 'since': '1.9'}
}

uncommon_gamerules = {
    'announceAdvancements': {'type': 'bool', 'default': 'true', 'since': '1.12'},
    'disableElytraMovementCheck': {'type': 'bool', 'default': 'false', 'since': '1.9'},
    'disableRaids': {'type': 'bool', 'default': 'false', 'since': '1.14.3'},
    'doEntityDrops': {'type': 'bool', 'default': 'true', 'since': '1.8.1'},
    'doFireTick': {'type': 'bool', 'defaulindentt': 'true', 'since': '1.4.2'},
    'doInsomnia': {'type': 'bool', 'default': 'true', 'since': '1.15'},
    'doImmediateRespawn': {'type': 'bool', 'default': 'false', 'since': '1.15'},
    'doLimitedCrafting': {'type': 'bool', 'default': 'false', 'since': '1.12'},
    'doMobLoot': {'type': 'bool', 'default': 'true', 'since': '1.4.2'},
    'doPatrolSpawning': {'type': 'bool', 'default': 'true', 'since': '1.15.2'},
    'doTileDrops': {'type': 'bool', 'default': 'true', 'since': '1.4.2'},
    'doTraderSpawning': {'type': 'bool', 'default': 'true', 'since': '1.15.2'},
    'drowningDamage': {'type': 'bool', 'default': 'true', 'since': '1.15'},
    'fallDamage': {'type': 'bool', 'default': 'true', 'since': '1.15'},
    'fireDamage': {'type': 'bool', 'default': 'true', 'since': '1.15'},
    'freezeDamage': {'type': 'bool', 'default': 'true', 'since': '1.17'},
    'forgiveDeadPlayers': {'type': 'bool', 'default': 'true', 'since': '1.16'},
    'logAdminCommands': {'type': 'bool', 'default': 'true', 'since': '1.8'},
    'maxCommandChainLength': {'type': 'int', 'default': '65536', 'since': '1.12'},
    'maxEntityCramming': {'type': 'int', 'default': '24', 'since': '1.11'},
    'mobGriefing': {'type': 'bool', 'default': 'true', 'since': '1.4.2'},
    'randomTickSpeed': {'type': 'int', 'default': '3', 'since': '1.8'},
    'reducedDebugInfo': {'type': 'bool', 'default': 'false', 'since': '1.8'},
    'showDeathMessages': {'type': 'bool', 'default': 'true', 'since': '1.8'},
    'spectatorsGenerateChunks': {'type': 'bool', 'default': 'true', 'since': '1.9'},
    'universalAnger': {'type': 'bool', 'default': 'false', 'since': '1.16'}
}

# https://minecraft.fandom.com/wiki/Biome/ID
biomes = [
    'ocean',
    'plains',
    'desert',
    'mountains',
    'forest',
    'taiga',
    'swamp',
    'river',
    'nether_wastes',
    'the_end',
    'frozen_ocean',
    'frozen_river',
    'snowy_tundra',
    'snowy_mountains',
    'mushroom_fields',
    'mushroom_field_shore',
    'beach',
    'desert_hills',
    'wooded_hills',
    'taiga_hills',
    'mountain_edge',
    'jungle',
    'jungle_hills',
    'jungle_edge',
    'deep_ocean',
    'stone_shore',
    'snowy_beach',
    'birch_forest',
    'birch_forest_hills',
    'dark_forest',
    'snowy_taiga',
    'snowy_taiga_hills',
    'giant_tree_taiga',
    'giant_tree_taiga_hills',
    'wooded_mountains',
    'savanna',
    'savanna_plateau',
    'badlands',
    'wooded_badlands_plateau',
    'badlands_plateau',
    'small_end_islands',
    'end_midlands',
    'end_highlands',
    'end_barrens',
    'warm_ocean',
    'lukewarm_ocean',
    'cold_ocean',
    'deep_warm_ocean',
    'deep_lukewarm_ocean',
    'deep_cold_ocean',
    'deep_frozen_ocean',
    'the_void',
    'sunflower_plains',
    'desert_lakes',
    'gravelly_mountains',
    'flower_forest',
    'taiga_mountains',
    'swamp_hills',
    'ice_spikes',
    'modified_jungle',
    'modified_jungle_edge',
    'tall_birch_forest',
    'tall_birch_hills',
    'dark_forest_hills',
    'snowy_taiga_mountains',
    'giant_spruce_taiga',
    'giant_spruce_taiga_hills',
    'modified_gravelly_mountains',
    'shattered_savanna',
    'shattered_savanna_plateau',
    'eroded_badlands',
    'modified_wooded_badlands_plateau',
    'modified_badlands_plateau',
    'bamboo_jungle',
    'bamboo_jungle_hills',
    'soul_sand_valley',
    'crimson_forest',
    'warped_forest',
    'basalt_deltas',
    'dripstone_caves',
    'lush_caves',
    'meadow',
    'grove',
    'snowy_slopes',
    'lofty_peaks',
    'frozen_peaks',
    'stony_peaks'
]

# https://minecraft.fandom.com/wiki/Custom#Structure_defaults
generator_structures = {
    'village': {'spacing': 32, 'separation': 8, 'salt': 10387312},
    'desert_pyramid': {'spacing': 32, 'separation': 8, 'salt': 14357617},
    'igloo': {'spacing': 32, 'separation': 8, 'salt': 14357617},
    'jungle_pyramid': {'spacing': 32, 'separation': 8, 'salt': 14357619},
    'swamp_hut': {'spacing': 32, 'separation': 8, 'salt': 14357620},
    'pillager_outpost': {'spacing': 32, 'separation': 8, 'salt': 165745296},
    'monument': {'spacing': 32, 'separation': 8, 'salt': 14357617},
    'endcity': {'spacing': 32, 'separation': 5, 'salt': 10387313},
    'mansion': {'spacing': 80, 'separation': 20, 'salt': 10387319},
    'buried_treasure': {'spacing': 1, 'separation': 0, 'salt': 0},
    'mineshaft': {'spacing': 1, 'separation': 0, 'salt': 0},
    'ruined_portal': {'spacing': 40, 'separation': 15, 'salt': 34222645},
    'shipwreck': {'spacing': 24, 'separation': 4, 'salt': 165745295},
    'ocean_ruin': {'spacing': 20, 'separation': 8, 'salt': 14357621},
    'bastion_remnant': {'spacing': 27, 'separation': 4, 'salt': 30084232},
    'fortress': {'spacing': 27, 'separation': 4, 'salt': 30084232},
    'nether_fossil': {'spacing': 2, 'separation': 1, 'salt': 14357921}
}

generator_stronghold = {
    'count': 128,
    'distance': 32,
    'spread': 3
}

generator_presets = {
    'classic': {'biome': 'minecraft:plains', 'lakes': False, 'features': False, 'structures': ['village'],
                'stronghold': False,
                'layers': [{'block': 'minecraft:bedrock', 'height': 1}, {'block': 'minecraft:dirt', 'height': 2},
                           {'block': 'minecraft:grass_block', 'height': 1}]},

    'tunnelers_dream': {'biome': 'minecraft:mountains', 'lakes': False, 'features': True, 'structures': ['mineshaft'],
                        'stronghold': True, 'layers': [{'block': 'minecraft:bedrock', 'height': 1},
                                                       {'block': 'minecraft:stone', 'height': 230},
                                                       {'block': 'minecraft:dirt', 'height': 5},
                                                       {'block': 'minecraft:grass_block', 'height': 1}]},

    'water_world': {'biome': 'minecraft:deep_ocean', 'lakes': False, 'features': False,
                    'structures': ['monument', 'ocean_ruin', 'shipwreck'], 'stronghold': False,
                    'layers': [{'block': 'minecraft:bedrock', 'height': 1}, {'block': 'minecraft:stone', 'height': 5},
                               {'block': 'minecraft:dirt', 'height': 5}, {'block': 'minecraft:sand', 'height': 5},
                               {'block': 'minecraft:water', 'height': 90}]},

    'overworld': {'biome': 'minecraft:plains', 'lakes': True, 'features': True,
                  'structures': ['mineshaft', 'pillager_outpost', 'ruined_portal', 'village'], 'stronghold': True,
                  'layers': [{'block': 'minecraft:bedrock', 'height': 1}, {'block': 'minecraft:stone', 'height': 59},
                             {'block': 'minecraft:dirt', 'height': 3},
                             {'block': 'minecraft:grass_block', 'height': 1}]},

    'snowy_kingdom': {'biome': 'minecraft:snowy_tundra', 'lakes': False, 'features': False,
                      'structures': ['igloo', 'village'], 'stronghold': False,
                      'layers': [{'block': 'minecraft:bedrock', 'height': 1},
                                 {'block': 'minecraft:stone', 'height': 59}, {'block': 'minecraft:dirt', 'height': 3},
                                 {'block': 'minecraft:grass_block', 'height': 1},
                                 {'block': 'minecraft:snow', 'height': 1}]},

    'bottomless_pit': {'biome': 'minecraft:plains', 'lakes': False, 'features': False, 'structures': ['village'],
                       'stronghold': False, 'layers': [{'block': 'minecraft:cobblestone', 'height': 2},
                                                       {'block': 'minecraft:dirt', 'height': 3},
                                                       {'block': 'minecraft:grass_block', 'height': 1}]},

    'desert': {'biome': 'minecraft:desert', 'lakes': False, 'features': True,
               'structures': ['desert_pyramid', 'mineshaft', 'village'], 'stronghold': True,
               'layers': [{'block': 'minecraft:bedrock', 'height': 1}, {'block': 'minecraft:stone', 'height': 3},
                          {'block': 'minecraft:sandstone', 'height': 52}, {'block': 'minecraft:sand', 'height': 8}]},

    'redstone_ready': {'biome': 'minecraft:desert', 'lakes': False, 'features': False, 'structures': [],
                       'stronghold': False, 'layers': [{'block': 'minecraft:bedrock', 'height': 1},
                                                       {'block': 'minecraft:stone', 'height': 3},
                                                       {'block': 'minecraft:sandstone', 'height': 52}]},

    'the_void': {'biome': 'minecraft:the_void', 'lakes': False, 'features': True, 'structures': [], 'stronghold': False,
                 'layers': [{'block': 'minecraft:air', 'height': 1}]}
}

plugin_offers = {
    'EssentialsX': {'id': 9089},
    'Fast Async WorldEdit': {'id': 13932, 'file_name': 'FastAsyncWorldEdit',
                             'additional_info': 'Normal WorldEdit may be chosen later.'},
    'LuckPerms': {'id': 28140},
    'Multiverse-Core': {'id': 390},
    'PlugManX': {'id': 88135},
    'SkinsRestorer': {'id': 2124},
    'PlaceholderAPI': {'id': 6245},
    'ViaVersion': {'id': 19254},
    'ViaBackwards': {'id': 27448, 'depends': ['ViaVersion']},
    'WorldEdit': {'url': 'https://dev.bukkit.org/projects/worldedit/files/latest',
                  'incompatible': ['Fast Async WorldEdit']},
    'WorldGuard': {'url': 'https://dev.bukkit.org/projects/worldguard/files/latest', 'depends': ['WorldEdit']}
}


class SimpleCompleter(object):  # Custom completer

    def __init__(self, options):
        self.matches = None
        self.options = sorted(options)

    def complete(self, text, state):
        if state == 0:  # on first trigger, build possible matches
            if text:  # cache matches (entries that start with entered text)
                self.matches = [s for s in self.options
                                if s and s.startswith(text)]
            else:  # no text entered, all matches possible
                self.matches = self.options[:]

        # return match indexed by state
        try:
            return self.matches[state]
        except IndexError:
            return None


class CommaCompleter(object):  # Custom completer

    def __init__(self, options):
        self.matches = None
        self.options = sorted(options)

    def complete(self, text, state):
        if state == 0:  # on first trigger, build possible matches
            if text:  # cache matches (entries that start with entered text)
                if ',' in text:
                    comma_index = text.rindex(',') + 1
                    comma_prefix = text[:comma_index]
                    last = text[comma_index:]
                    if not last.strip():
                        comma_prefix = comma_prefix + (' ' * len(last))
                        last = last.strip()

                    self.matches = [comma_prefix + s for s in self.options
                                    if s and s.startswith(last)]
                else:
                    self.matches = [s for s in self.options
                                    if s and s.startswith(text)]
            else:  # no text entered, all matches possible
                self.matches = self.options[:]

        # return match indexed by state
        try:
            return self.matches[state]
        except IndexError:
            return None


def complete(completions):
    completer = SimpleCompleter(completions)
    readline.set_completer(completer.complete)
    readline.parse_and_bind('tab: complete')


def complete_with_comma(completions):
    completer = CommaCompleter(completions)
    readline.set_completer(completer.complete)
    readline.parse_and_bind('tab: complete')


def parse_yes_no(answer, default, indent):
    if not answer:
        return default
    if answer.lower() == 'y':
        return True
    if answer.lower() == 'n':
        return False
    print((' ' * indent) + 'Please state "y" or "n"')
    return None


player_cache = {}


def get_player(identifier):
    if identifier in player_cache:
        return player_cache[identifier]

    response = request.urlopen(f'https://www.mc-heads.net/minecraft/profile/{identifier}').read()
    if len(response) > 0:
        info = json.loads(response)
        uuid = info['id']
        uuid = f'{uuid[:20]}-{uuid[20:]}'
        uuid = f'{uuid[:16]}-{uuid[16:]}'
        uuid = f'{uuid[:12]}-{uuid[12:]}'
        uuid = f'{uuid[:8]}-{uuid[8:]}'

        player = {
            'name': info['name'],
            'uuid': uuid
        }
        player_cache[identifier] = player
        return player
    else:
        return None


def main():
    signal.signal(signal.SIGINT, lambda s, frame: sigint_handler())

    opener = request.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0')]
    request.install_opener(opener)

    index = 0

    def indent():
        return 2 + len(str(index))

    def str_indent(additional):
        return ' ' * (indent() + additional)

    def prefix():
        return f'\n{str(index)}.'

    print('Minecraft Server creator by Rapha149\nIf a default value is specified, write nothing to use it.')

    # Java executable
    index += 1
    print(f'{prefix()} State the path to your Java executable. If it\'s on the PATH variable, '
          f'you can also just state the command.')
    print(
        f'{str_indent(0)}How to choose the Java version:\n{str_indent(0)}- Below or equal to 1.16: Java 8 to Java 16, '
        f'recommended: Java 8 or Java 11\n{str_indent(0)}- 1.17: Java 16\n{str_indent(0)}- 1.18: Java 17')
    while True:
        java = input('> ')
        if which(java) is not None:
            result = subprocess.run([java, '-version'], stderr=subprocess.PIPE)
            match = re.search('version (".+")', result.stderr.decode('utf-8'))
            if match is not None:
                print(f'{str_indent(0)}Java version successfully detected: {match.group(1)}')
                break
            else:
                print(f'{str_indent(0)}Could not detect Java version. Do you want to continue? (y/N)')
                ignore = False
                while True:
                    answer = parse_yes_no(input('> '), False, indent())
                    if answer is not None:
                        if answer:
                            ignore = True
                        else:
                            print(f'{str_indent(0)}State the path to your Java executable.')
                        break
                if ignore:
                    break
        else:
            print(f'{str_indent(0)}Executable not found.')

    # Port
    index += 1
    print(f'{prefix()} Choose a port for the server. Defaults to 25565')
    while True:
        answer = input('> ')
        if not answer:
            port = 25565
            break
        try:
            port = int(answer)
            if port > 0:
                if port <= 65535:
                    break
                else:
                    print(f'{str_indent(0)}The port has to be below 65535.')
            else:
                print(f'{str_indent(0)}The port has to be above 0.')
        except ValueError:
            print(f'{str_indent(0)}Please state a number.')

    # Folder
    index += 1
    print(f'{prefix()} Select an empty folder to install the server to. It does not have to exist.')
    while True:
        target_folder = input('> ')
        if len(target_folder) > 0:
            target_folder_path = Path(target_folder)
            if target_folder_path.is_file():
                print(f'{str_indent(0)}Please provide a folder.')
            elif target_folder_path.is_dir() and len(os.listdir(target_folder)) > 0:
                print(f'{str_indent(0)}Please provide an empty folder.')
            else:
                break
        else:
            print(f'{str_indent(0)}Please provide a folder.')

    # Paper version
    index += 1
    versions = []
    for ver in json.loads(request.urlopen('https://papermc.io/api/v2/projects/paper').read())['versions']:
        if 'pre' not in ver:
            versions.append(ver)
    print(f'{prefix()} Choose a Paper version.')
    complete(versions)
    while True:
        paper_version = input('> ')
        if paper_version in versions:
            paper_version_parsed = version.parse(paper_version)
            break
        else:
            print(f'{str_indent(0)}Unknown version. Please choose from {", ".join(versions)}')
    complete([])

    # Screen
    if which('screen') is not None:
        index += 1
        print(f'{prefix()} Do you want to use screens? (Y/n)')
        while True:
            screen = parse_yes_no(input('> '), True, indent())
            if screen is not None:
                if screen:
                    # Screen name
                    print(f'{prefix()}1 Choose a screen name.')
                    while True:
                        screen_name = input('> ')
                        if ' ' in screen_name:
                            print(f'{str_indent(1)}The screen name may not contain spaces.')
                        elif not screen_name:
                            print(f'{str_indent(1)}Please provide a screen name.')
                        else:
                            break

                    # Screen log
                    print(f'{prefix()}2 Do you want to enable screen log? (Y/n)')
                    while True:
                        screen_log = parse_yes_no(input('> '), True, indent() + 1)
                        if screen_log is not None:
                            break

                    # Automatically resumed
                    print(f'{prefix()}3 Do you want to automatically resume the screen if it already exists? (Y/n)')
                    print(
                        f'{str_indent(1)}Explanation: if your server is already running and you try to start it again,'
                        f'\n{str_indent(1 + len("Explanation: "))}it won\'t start another instance of the server but '
                        f'it will '
                        f'resume the running screen.')
                    print(
                        f'{str_indent(1)}Warning: Disabling this is not recommended and will cause issues especially '
                        f'if you want to use the restart system.')
                    while True:
                        automatically_resume = parse_yes_no(input('> '), True, indent() + 1)
                        if automatically_resume is not None:
                            break

                    # Restart
                    print(
                        f'{prefix()}4 Do you want to enable the Spigot restart system? (y/N)\n{str_indent(1)}This '
                        f'does not '
                        f'automatically restart the server.\n{str_indent(1)}Warning: Unique screen names are required.')
                    while True:
                        restart = parse_yes_no(input('> '), False, indent() + 1)
                        if restart is not None:
                            break

                    # Restart on crash
                    if restart:
                        print(f'{prefix()}5 Do you want the server to restart after a crash? (Y/n)')
                        while True:
                            restart_on_crash = parse_yes_no(input('> '), True, indent() + 1)
                            if restart_on_crash is not None:
                                break
                break
    else:
        screen = False

    # Minimum ram
    index += 1
    print(
        f'{prefix()}1 Choose a minimum ram usage.\n{str_indent(1)}Please use the format as for the "java" commnad. '
        f'E.g. "1024K", "2048M" or "1G"\n{str_indent(1)}Leave empty if you don\'t want to specify a minimum ram usage.')
    while True:
        minimum_ram = input('> ')
        if not minimum_ram:
            minimum_ram = None
            break
        elif re.match('^\\d+[KkGgMm]$', minimum_ram):
            break
        else:
            print(f'{str_indent(1)}Incorrect ram specification')

    # Maximum ram
    print(
        f'{prefix()}2 Choose a maximum ram usage.\n{str_indent(1)}Same format as in {str(index)}.1\n'
        f'{str_indent(1)}Leave empty if you don\'t want to specify a maximum ram usage.')
    while True:
        maximum_ram = input('> ')
        if not maximum_ram:
            maximum_ram = None
            break
        elif re.match('^\\d+[KkGgMm]$', maximum_ram):
            break
        else:
            print(f'{str_indent(1)}Incorrect ram specification')

    # Server settings
    # MOTD
    index += 1
    print(
        f'{prefix()} Choose a MOTD. You can use color codes with "\u00A7" and you can seperate lines using "\\n".\n'
        f'{str_indent(0)}Leave empty for default MOTD.')
    answer = input('> ')
    if answer:
        motd = ''
        for c in answer:
            try:
                c.encode('ascii')
                motd += c
            except UnicodeEncodeError:
                unicode = f'{ord(c):x}'
                motd += f'\\u{unicode:0>4}'
    else:
        motd = None

    # Max players
    index += 1
    print(f'{prefix()} Choose a maximum player count. Defaults to 20.')
    while True:
        answer = input('> ')

        if not answer:
            max_players = 20
            break
        try:
            max_players = int(answer)
            if max_players >= 1:
                break
            else:
                print('The maximum player count has to be above 0')
        except ValueError:
            print(f'{str_indent(0)}Please state a number.')

    # Whitelist
    index += 1
    print(f'{prefix()} Do you want to enable the whitelist? (y/N)')
    while True:
        whitelist = parse_yes_no(input('> '), False, indent())
        if whitelist is not None:
            if whitelist:
                # Whitelist playersversion.parse(
                print(
                    f'{prefix()}1 Which players should be whitelisted? Seperate with comma or enter nothing for '
                    f'nobody.')
                while True:
                    already_added = []
                    whitelist_players = []
                    failed = False
                    answer = input('> ')

                    if len(answer) > 0:
                        players = answer.split(',')
                        for player in players:
                            response = get_player(player.strip())
                            if response is not None:
                                if response['uuid'] not in already_added:
                                    already_added.append(response['uuid'])
                                    whitelist_players.append(response)
                            else:
                                print(f'{str_indent(1)}Player "{player.strip()}" does not exist')
                                failed = True
                    if not failed:
                        break
                break
            break

    # Operators
    index += 1
    print(f'{prefix()} Which players should be operators? Seperate with comma or enter nothing for nobody.')
    while True:
        already_added = []
        operators = []
        failed = False
        answer = input('> ')

        if len(answer) > 0:
            players = answer.split(',')
            for player in players:
                response = get_player(player.strip())
                if response is not None:
                    if response['uuid'] not in already_added:
                        already_added.append(response['uuid'])
                        response['level'] = 4
                        response['bypassesPlayerLimit'] = False
                        operators.append(response)
                else:
                    print(f'{str_indent(0)}Player "{player.strip()}" does not exist')
                    failed = True
        if not failed:
            break

    # Gamerules
    index += 1
    gamerules = {}
    print(f'{prefix()} Do you want to change gamerules? (y/N)')
    while True:
        answer = parse_yes_no(input('> '), False, indent())
        if answer is not None:
            if answer:
                print(f'{prefix()}1 Leave empty if you want to use the default value.')

                def ask_gamerule(key, info, sub_index, i):
                    if paper_version_parsed >= version.parse(info['since']):
                        iindent = ' ' * (1 + indent() + len(str(sub_index)) + len(str(i)))

                        print(
                            f'{prefix()}{str(sub_index)}.{str(i)} Set gamerule "{key}" ('
                            f'{"true/false y/n" if info["type"] == "bool" else info["type"]})\n{iindent}Defaults to "'
                            f'{info["default"]}"')
                        if info['type'] == 'bool':
                            complete(['true', 'false'])

                        while True:
                            answer = input('> ').lower()
                            if not answer:
                                break
                            else:
                                if info['type'] == 'bool':
                                    if answer == 'y':
                                        answer = 'true'
                                    if answer == 'n':
                                        answer = 'false'
                                    if answer == 'true' or answer == 'false':
                                        gamerules[key] = answer
                                        break
                                    else:
                                        print(iindent + 'Please state "true" / "y" or "false" / "n".')
                                if info['type'] == 'int':
                                    try:
                                        gamerules[key] = str(int(answer))
                                        break
                                    except ValueError:
                                        print(f'{iindent}Please state a number.')

                        complete([])
                        return True
                    else:
                        return False

                # Common gamerules
                i = 1
                for key, info in common_gamerules.items():
                    if ask_gamerule(key, info, 1, i):
                        i += 1

                # Uncommon gamerules
                print(f'{prefix()}2 Do you want to change more uncommon gamerules, too? (y/N)')
                while True:
                    answer = parse_yes_no(input('> '), False, indent() + 1)
                    if answer is not None:
                        if answer:
                            i = 1
                            for key, info in uncommon_gamerules.items():
                                if ask_gamerule(key, info, 2, i):
                                    i += 1
                        break
            break

    # Further options
    index += 1
    print(f'{prefix()} Do you want to change more specific server settings? (y/N)')
    while True:
        specific_settings = parse_yes_no(input('> '), False, indent())
        if specific_settings is not None:
            if specific_settings:
                i = 0

                def iindent():
                    return indent() + len(str(i))

                def str_iindent():
                    return ' ' * iindent()

                # Level name
                i += 1
                print(f'{prefix()}{str(i)} Choose a level name. Defaults to "world"')
                while True:
                    level_name = input('> ')
                    if not level_name:
                        level_name = None
                        break
                    elif ' ' in level_name:
                        print(f'{str_iindent()}The level name may not contain spaces.')
                    else:
                        break

                # Level type
                i += 1
                types = ['default', 'flat', 'largeBiomes', 'amplified']
                print(
                    f'{prefix()}{str(i)} Choose a level type ({"/".join(types)})\n{str_iindent()}Defaults to '
                    f'"default".')
                complete(types)
                while True:
                    level_type = input('> ').lower()
                    if not level_type:
                        level_type = None
                        break
                    if level_type == 'largebiomes':
                        level_type = 'largeBiomes'
                    if level_type in types:
                        break
                    else:
                        print(f'{str_iindent()}Unknown level type.')

                # Generation settings
                generator_settings = None
                if level_type == 'flat':
                    i += 1
                    print(
                        f'{prefix()}{str(i)} Do you want to change the generator settings? (y/N)\n'
                        f'{str_iindent()}Warning: '
                        f'This feature has only been tested in 1.17+')
                    while True:
                        answer = parse_yes_no(input('> '), False, iindent())
                        if answer is not None:
                            if answer:
                                generator_settings = {}

                                # Presets
                                presets = list(generator_presets.keys())
                                presets.append('custom')
                                print(
                                    f'{prefix()}{str(i)}.1 Choose a preset or "custom" to customize values. '
                                    f"Defaults to "
                                    f'"classic".\n{str_iindent()}  Presets: {", ".join(presets)}')
                                complete(presets)
                                while True:
                                    answer = input('> ').lower()
                                    if answer in presets:
                                        complete([])
                                        if answer != 'custom':
                                            preset = generator_presets[answer]
                                            generator_settings['biome'] = preset['biome']
                                            generator_settings['lakes'] = preset['lakes']
                                            generator_settings['features'] = preset['features']
                                            generator_settings['layers'] = preset['layers']

                                            sub_structures = {}
                                            for structure in preset['structures']:
                                                sub_structures[structure] = generator_structures[structure]
                                            structures = {'structures': sub_structures}
                                            if preset['stronghold']:
                                                structures['stronghold'] = generator_stronghold
                                            generator_settings['structures'] = structures
                                            break
                                        else:
                                            # Biome
                                            print(
                                                f'{prefix()}{str(i)}.2 Choose a biome id. Defaults to "plains".\n'
                                                f'{str_iindent()}  For a list of biome ids, '
                                                f'see https://minecraft.fandom.com/wiki/Biome/ID')
                                            complete(biomes)
                                            while True:
                                                answer = input('> ').lower()
                                                if not answer:
                                                    generator_settings['biome'] = 'minecraft:plains'
                                                    break
                                                else:
                                                    if answer.startswith('minecraft:'):
                                                        answer = answer[10:]
                                                    if answer in biomes:
                                                        generator_settings['biome'] = 'minecraft:' + answer
                                                        break
                                                    else:
                                                        print(f'{str_iindent()}  Unknown biome.')

                                            # Features
                                            print(
                                                f'{prefix()}{str(i)}.3 Do you want biome-specific features to '
                                                f'generate? (y/N)')
                                            while True:
                                                answer = parse_yes_no(input('> '), False, iindent() + 2)
                                                if answer is not None:
                                                    generator_settings['features'] = answer
                                                    break

                                            # Lakes
                                            print(f'{prefix()}{str(i)}.4 Do you want lakes to generate? (y/N)')
                                            while True:
                                                answer = parse_yes_no(input('> '), False, iindent() + 2)
                                                if answer is not None:
                                                    generator_settings['lakes'] = answer
                                                    break

                                            # Structures
                                            structures = {}
                                            print(
                                                f'{prefix()}{str(i)}.5 Choose structures to generate. Seperate with '
                                                f'comma. Leave empty for no structures.\n{str_iindent()}  Please note '
                                                f'that structures may not generate in some biomes.\n{str_iindent()}  For a '
                                                f'list of structures, '
                                                f'see https://minecraft.fandom.com/wiki/Custom#Structure_defaults')
                                            complete_with_comma(generator_structures.keys())
                                            while True:
                                                answer = input('> ').lower()
                                                if not answer:
                                                    structures['structures'] = {}
                                                    break
                                                else:
                                                    sub_structures = {}
                                                    failed = False
                                                    for structure in answer.split(','):
                                                        structure = structure.strip()
                                                        if structure in generator_structures:
                                                            sub_structures[structure] = generator_structures[structure]
                                                        else:
                                                            failed = True
                                                            print(
                                                                f'{str_iindent()}  Unknown structure: "{structure}"')
                                                            break
                                                    if not failed:
                                                        structures['structures'] = sub_structures
                                                        break

                                            # Stronghold
                                            print(
                                                f'{prefix()}{str(i)}.6 Do you want strongholds to generate? (y/N)\n'
                                                f'{str_iindent()}  They may not generate. It\'s buggy.')
                                            while True:
                                                answer = parse_yes_no(input('> '), False, iindent() + 2)
                                                if answer is not None:
                                                    if answer:
                                                        structures['stronghold'] = generator_stronghold
                                                    break

                                            generator_settings['structures'] = structures

                                            # Layers
                                            print(
                                                f'{prefix()}{str(i)}.7 Specify the layers using the following format: '
                                                f'"<block> [height]". For example: "bedrock" or "stone 59".\n'
                                                f'{str_iindent()}  If no height is given, the layer will be 1 block '
                                                f'high.\n{str_iindent()}  If you are finished, write nothing to proceed.')
                                            layers = []
                                            while True:
                                                answer = input(f'{str(len(layers) + 1)}. Layer > ')
                                                if not answer:
                                                    if not layers:
                                                        print(f'{str_iindent()}  Specify at least 1 layer.')
                                                    else:
                                                        break
                                                else:
                                                    answers = answer.split(' ')
                                                    block = answers[0]
                                                    if not block.startswith('minecraft:'):
                                                        block = 'minecraft:' + block
                                                    if len(answers) > 1:
                                                        try:
                                                            height = int(answers[1])
                                                        except ValueError:
                                                            print(f'{str_iindent}  "{answers[1]}" is not a number.')
                                                            continue
                                                    else:
                                                        height = 1
                                                    layers.append({'block': block, 'height': height})

                                            generator_settings['layers'] = layers
                                            break
                                    else:
                                        print(f'{str_iindent()}  Unknown preset.')
                            break

                # Seed
                i += 1
                print(f'{prefix()}{str(i)} Choose a world seed. (int)\n{str_iindent()}Leave empty for a random seed.')
                answer = input('> ')
                seed = answer if answer else None

                # Max build height
                if paper_version_parsed < version.parse('1.17'):
                    i += 1
                    print(
                        f'{prefix()}{str(i)} Choose a max build height. (int)\n{str_iindent()}Maximum is 256. Has to '
                        f'be a multiple of 8.\n{str_iindent()}Defaults to 256.')
                    while True:
                        answer = input('> ')
                        if not answer:
                            max_build_height = None
                            break
                        try:
                            max_build_height = int(answer)
                            if max_build_height >= 1:
                                if max_build_height <= 256:
                                    if max_build_height % 8 == 0:
                                        break
                                    print(f'{str_iindent()}The max build height has to be a multiple of 8.')
                                else:
                                    print(f'{str_iindent()}The max build height has to be below or equal to 256.')
                            else:
                                print(f'{str_iindent()}The max build height has to be above 0.')
                        except ValueError:
                            print(f'{str_iindent()}Please state a number.')
                else:
                    max_build_height = None

                # View distance
                i += 1
                print(f'{prefix()}{str(i)} Choose a view distance. (3-32)\n{str_iindent()}Defaults to 10.')
                while True:
                    answer = input('> ')
                    if not answer:
                        view_distance = None
                        break
                    try:
                        view_distance = int(answer)
                        if 3 <= view_distance <= 32:
                            break
                        else:
                            print(f'{str_iindent()}Please choose a value between 3 and 32.')
                    except ValueError:
                        print(f'{str_iindent()}Please state a number.')

                # Simulation distance
                if paper_version_parsed >= version.parse('1.18'):
                    i += 1
                    print(f'{prefix()}{str(i)} Choose a simulation distance. (5-32)\n{str_iindent()}Defaults to 10.')
                    while True:
                        answer = input('> ')
                        if not answer:
                            simulation_distance = None
                            break
                        try:
                            simulation_distance = int(answer)
                            if 5 <= simulation_distance <= 32:
                                break
                            else:
                                print(f'{str_iindent()}Please choose a value between 5 and 32.')
                        except ValueError:
                            print(f'{str_iindent()}Please state a number.')
                else:
                    simulation_distance = None

                # Entity broadcast range percentage
                if paper_version_parsed >= version.parse('1.16'):
                    i += 1
                    print(
                        f'{prefix()}{str(i)} Choose an entity broadcast range percentage. (10-1000)\n'
                        f'{str_iindent()}Defaults to 100.')
                    while True:
                        answer = input('> ')
                        if not answer:
                            entity_broadcast_range_percentage = None
                            break
                        try:
                            entity_broadcast_range_percentage = int(answer)
                            if 10 <= entity_broadcast_range_percentage <= 1000:
                                break
                            else:
                                print(f'{str_iindent()}Please choose a value between 10 and 1000.')
                        except ValueError:
                            print(f'{str_iindent()}Please state a number.')
                else:
                    entity_broadcast_range_percentage = None

                # Spawn Protection
                i += 1
                print(f'{prefix()}{str(i)} Choose a spawn protection. (int)\n{str_iindent()}Defaults to 16.')
                while True:
                    answer = input('> ')
                    if not answer:
                        spawn_protection = None
                        break
                    try:
                        spawn_protection = int(answer)
                        if spawn_protection >= 0:
                            break
                        else:
                            print(f'{str_iindent()}Please state a positive number.')
                    except ValueError:
                        print(f'{str_iindent()}Please state a number.')

                # Gamemode
                i += 1
                if paper_version_parsed >= version.parse('1.14'):
                    gamemodes = ['survival', 'creative', 'adventure', 'spectator', '0', '1', '2', '3']
                    default = 'survival'
                else:
                    gamemodes = ['0', '1', '2', '3']
                    default = '0'
                print(
                    f'{prefix()}{str(i)} Choose a default gamemode. ({"/".join(gamemodes)})\n{str_iindent()}Defaults '
                    f'to "{default}".')
                complete(gamemodes)
                while True:
                    gamemode = input('> ').lower()
                    if not gamemode:
                        gamemode = None
                        break
                    if gamemode in gamemodes:
                        break
                    else:
                        print(f'{str_iindent()}Unknown gamemode')
                complete([])

                # Force gamemode
                i += 1
                print(f'{prefix()}{str(i)} Enable force gamemode? (y/N)')
                while True:
                    force_gamemode = parse_yes_no(input('> '), False, iindent())
                    if force_gamemode is not None:
                        break

                # Difficulty
                i += 1
                if paper_version_parsed >= version.parse('1.14'):
                    difficulties = ['peaceful', 'easy', 'normal', 'hard', '0', '1', '2', '3']
                    default = 'easy'
                else:
                    difficulties = ['0', '1', '2', '3']
                    default = '1'
                print(
                    f'{prefix()}{str(i)} Choose a difficulty ({"/".join(difficulties)})\n{str_iindent()}Defaults to "'
                    f'{default}".')
                complete(difficulties)
                while True:
                    difficulty = input('> ').lower()
                    if not difficulty:
                        difficulty = None
                        break
                    if difficulty in difficulties:
                        break
                    else:
                        print(f'{str_iindent()}Unknown difficulty')
                complete([])

                # Hardcore
                i += 1
                print(f'{prefix()}{str(i)} Enable hardcore? (y/N)')
                while True:
                    hardcore = parse_yes_no(input('> '), False, iindent())
                    if hardcore is not None:
                        break

                # PVP
                i += 1
                print(f'{prefix()}{str(i)} Enable pvp? (Y/n)')
                while True:
                    pvp = parse_yes_no(input('> '), True, iindent())
                    if pvp is not None:
                        break

                # Announce player achievements
                if paper_version_parsed < version.parse('1.12'):
                    i += 1
                    print(f'{prefix()}{str(i)} Announce player achievements? (Y/n)')
                    while True:
                        announce_player_achievements = parse_yes_no(input('> '), True, iindent())
                        if announce_player_achievements is not None:
                            break
                else:
                    announce_player_achievements = None

                # Command blocks
                i += 1
                print(f'{prefix()}{str(i)} Enable command blocks? (y/N)')
                while True:
                    command_blocks = parse_yes_no(input('> '), False, iindent())
                    if command_blocks is not None:
                        break

                # Online mode
                i += 1
                print(f'{prefix()}{str(i)} Enable online mode? (Y/n)')
                while True:
                    online_mode = parse_yes_no(input('> '), True, iindent())
                    if online_mode is not None:
                        break

                # Connection throttle
                i += 1
                print(
                    f'{prefix()}{str(i)} Choose a connection throttle time. (int / milliseconds)\n'
                    f'{str_iindent()}Defaults to 4000.')
                print(
                    f'{str_iindent()}The connection throttle time is the delay before a client is allowed to connect '
                    f'again after a recent connection attempt.')
                print(
                    f'{str_iindent()}A value of 0 disables the connection throttle but leaves your server susceptible '
                    f'to attacks (only recommended for test servers).')
                while True:
                    answer = input('> ')
                    if not answer:
                        connection_throttle = None
                        break
                    try:
                        connection_throttle = int(answer)
                        if connection_throttle >= 0:
                            break
                        else:
                            print(f'{str_iindent()}Please state a positive number.')
                    except ValueError:
                        print(f'{str_iindent()}Please state a number.')

                # Allow flight
                i += 1
                print(f'{prefix()}{str(i)} Allow flight? (y/N)')
                while True:
                    allow_flight = parse_yes_no(input('> '), False, iindent())
                    if allow_flight is not None:
                        break

                # Allow nether
                i += 1
                print(f'{prefix()}{str(i)} Allow nether? (Y/n)')
                while True:
                    allow_nether = parse_yes_no(input('> '), True, iindent())
                    if allow_nether is not None:
                        break

                # Allow end
                i += 1
                print(f'{prefix()}{str(i)} Allow end? (Y/n)')
                while True:
                    allow_end = parse_yes_no(input('> '), True, iindent())
                    if allow_end is not None:
                        break

                # Bungeecord
                i += 1
                print(f'{prefix()}{str(i)} Enable bungeecord? (y/N)')
                while True:
                    bungeecord = parse_yes_no(input('> '), False, iindent())
                    if bungeecord is not None:
                        break
            break

    # Undo patches
    print(f'{prefix()} Do you want to change certain paper patches? (y/N)')
    while True:
        change_patches = parse_yes_no(input('> '), False, indent())
        if change_patches is not None:
            if change_patches:
                # Discount exploit
                print(
                    f'{prefix()}1 Do you want to enable "fix-curing-zombie-villager-discount-exploit"? (Y/n)\n'
                    f'{str_indent(1)}If enabled, villagers won\'t give you extrem discounts after curing.')
                while True:
                    patch_discount_exploit = parse_yes_no(input('> '), True, indent() + 1)
                    if patch_discount_exploit is not None:
                        break

                # Permanent block break exploit
                print(
                    f'{prefix()}2 Do you want to enable "allow-permanent-block-break-exploits"? (y/N)\n'
                    f'{str_indent(1)}If enabled, you can remove bedrock using piston glitches.')
                while True:
                    patch_permanent_block_break_exploit = parse_yes_no(input('> '), False, indent() + 1)
                    if patch_permanent_block_break_exploit is not None:
                        break

                # Piston duplication
                print(
                    f'{prefix()}2 Do you want to enable "allow-piston-duplication"? (y/N)\n{str_indent(1)}If '
                    f'enabled, you can duplicate e.g. carpets using pistons.')
                while True:
                    patch_piston_duplication = parse_yes_no(input('> '), False, indent() + 1)
                    if patch_piston_duplication is not None:
                        break
            break

    # Plugins
    index += 1
    plugins = {}
    print(f'{prefix()} Do you want to install certain plugins? (y/N)')
    while True:
        certain_plugins = parse_yes_no(input('> '), False, indent())
        if certain_plugins is not None:
            if certain_plugins:
                i = 0
                for plugin, info in plugin_offers.items():
                    delimiter = '", "'
                    if 'incompatible' in info:
                        incompatible_plugins = []
                        for incompatible in info['incompatible']:
                            if incompatible in plugins:
                                incompatible_plugins.append(incompatible)
                                break
                        if incompatible_plugins:
                            i += 1
                            print(
                                f'{prefix()}{str(i)} The plugin "{plugin}" is incompatible with the plugin'
                                f'{"s" if len(incompatible_plugins) != 1 else ""} "'
                                f'{delimiter.join(incompatible_plugins)}".')
                            continue

                    if 'depends' in info:
                        needed_plugins = []
                        for depend in info['depends']:
                            if depend not in plugins:
                                needed_plugins.append(depend)
                                break
                        if needed_plugins:
                            i += 1
                            print(
                                f'{prefix()}{str(i)} The plugin "{plugin}" depends on the plugin'
                                f'{"s" if len(needed_plugins) != 1 else ""} "{delimiter.join(needed_plugins)}".')
                            continue

                    iindent = indent() + len(str(i))
                    str_iindent = ' ' * iindent

                    if 'id' not in info:
                        if 'url' not in info:
                            continue

                        i += 1
                        print(
                            f'{prefix()}{str(i)} Install the plugin "{plugin}"? (y/N)\n{str_iindent}No further '
                            f'information due to the plugin not being available on spigotmc.org')
                        if 'additional_info' in info:
                            print(str_iindent + info['additional_info'])
                        while True:
                            answer = parse_yes_no(input('> '), False, iindent)
                            if answer is not None:
                                if answer:
                                    plugins[plugin] = {'url': info['url'], 'file': (info[
                                                                                        'file_name'] if 'file_name' in
                                                                                                        info else
                                                                                    plugin)
                                                                                   + '.jar'}
                                break
                        continue

                    response = request.urlopen(f'https://api.spiget.org/v2/resources/{str(info["id"])}').read()
                    if len(response) > 0:
                        i += 1

                        spiget_info = json.loads(response)
                        tested = False
                        for testedVersion in spiget_info['testedVersions']:
                            if paper_version.startswith(testedVersion):
                                tested = True
                                break

                        print(
                            f'{prefix()}{str(i)} Install the plugin "{plugin}"?'
                            f'{"" if tested else " [Not tested in this version!]"} (y/N)\n{str_iindent}'
                            f'{spiget_info["tag"]}')
                        if 'additional_info' in info:
                            print(str_iindent + info['additional_info'])
                        while True:
                            answer = parse_yes_no(input('> '), False, iindent)
                            if answer is not None:
                                if answer:
                                    url = None
                                    if plugin == 'EssentialsX':
                                        latest_version = json.loads(request.urlopen(
                                            f'https://api.spiget.org/v2/resources/'
                                            f'{str(info["id"])}/versions/latest').read())['name']
                                        url = f'https://github.com/EssentialsX/Essentials/releases/download/' \
                                              f'{latest_version}/EssentialsX-{latest_version}.jar'
                                    elif plugin == 'Fast Async WorldEdit':
                                        console = request.urlopen(
                                            'https://ci.athion.net/job/FastAsyncWorldEdit-1.17/lastSuccessfulBuild'
                                            '/consoleText').read()
                                        match = re.search('FastAsyncWorldEdit-Bukkit-(\\d|\\.)+-\\d+\\.jar',
                                                          str(console))
                                        if match is not None:
                                            url = \
                                                f'https://ci.athion.net/job/FastAsyncWorldEdit-1.17/lastSuccessfulBuild' \
                                                f'/artifact/artifacts/{match.group()}'
                                    else:
                                        url = info[
                                            'url'] if 'url' in info else f'https://api.spiget.org/v2/reso' \
                                                                         f'urces/{str(info["id"])}/download'

                                    if url is not None:
                                        plugins[plugin] = {'url': url, 'file': (info[
                                                                                    'file_name'] if 'file_name' in info
                                                                                else plugin) + '.jar'}
                                    else:
                                        print(f'{str(index)}.{str(i)} Couldn\'t extract the plugin\'s download url.')
                                break
            break

    # Eula
    print(
        '\nType "Yes" to agree to the EULA of Minecraft.\nSee https://account.mojang.com/documents/minecraft_eula '
        'for more information.')
    while True:
        if input('> ').lower() == 'yes':
            break
        else:
            print('Please type "Yes" to agree to the EULA of Minecraft.')

    # Prepare server
    print('\nType "confirm" to proceed with installation.')
    while True:
        if input('> ').lower() == 'confirm':
            break
        else:
            print('Type "confirm" to proceed with installation.')

    print('\nInstalling...')
    start_once = len(gamerules) > 0
    bukkit_data = {'settings': {}}
    spigot_data = {'settings': {}}
    paper_data = {'world-settings': {'default': {'game-mechanics': {}}}, 'settings': {'unsupported-settings': {}}}

    # Target folder
    target_folder_path = Path(target_folder)
    if target_folder_path.is_file():
        print('Target folder is a file.')
        exit()
    if target_folder_path.is_dir() and len(os.listdir(target_folder)) > 0:
        print('Target folder is not empty anymore.')
        exit()
    os.makedirs(target_folder, exist_ok=True)
    os.chdir(target_folder)

    # server jar
    print('Downloading server jar...')
    latest_build = \
        json.loads(request.urlopen(f'https://papermc.io/api/v2/projects/paper/versions/{paper_version}').read())[
            'builds'][
            -1]
    file_name = json.loads(
        request.urlopen(
            f'https://papermc.io/api/v2/projects/paper/versions/{paper_version}/builds/{latest_build}').read())[
        'downloads']['application']['name']
    request.urlretrieve(
        f'https://papermc.io/api/v2/projects/paper/versions/{paper_version}/builds/{latest_build}/downloads/'
        f'{file_name}', 'Paper.jar')

    # eula.txt
    print('Creating eula.txt...')
    eula_file = open('eula.txt', 'w')
    eula_file.write('eula=true\n')
    eula_file.close()

    # start scripts
    print('Creating start scripts...')
    start_file = open('start.sh', 'w')
    if screen:
        if restart:
            spigot_data['settings']['restart-script'] = './restart.sh'
            spigot_data['settings']['restart-on-crash'] = False if start_once else restart_on_crash

            if automatically_resume:
                start_file.write(
                    f'#!/bin/bash\nif screen -ls | egrep -qw "{screen_name}"\nthen\n    screen -rx "'
                    f'{screen_name}"\nelse\n    ./restart.sh attached\nfi\n')
            else:
                start_file.write(f'#!/bin/bash\n./restart.sh attached\n')

            restart_file = open('restart.sh', 'w')
            restart_file.write(
                '#!/bin/bash\nif [[ "$1" == "attached" ]]\nthen\n    screen {log}-S {name} {java}{xms}{xmx} -jar '
                'Paper.jar nogui\nelse\n    nohup screen {log}-dmS {name} {java}{xms}{xmx} -jar Paper.jar nogui '
                '>/dev/null 2>&1 &\nfi\n'.format(
                    log='-L ' if screen_log else '',
                    name=screen_name,
                    java=java,
                    xms=' -Xms' + minimum_ram if minimum_ram is not None else '',
                    xmx=' -Xmx' + maximum_ram if maximum_ram is not None else ''))
            restart_file.close()
            os.chmod('restart.sh', 0o775)
        elif automatically_resume:
            start_file.write(
                '#!/bin/bash\nif screen -ls | egrep -qw "{name}"\nthen\n    screen -rx "{name}"\nelse\n    '
                'screen {log}-S {name} {java}{xms}{xmx} -jar Paper.jar nogui\nfi\n'.format(
                    screen_name=screen_name,
                    log='-L ' if screen_log else '',
                    name=screen_name,
                    java=java,
                    xms=' -Xms' + minimum_ram if minimum_ram is not None else '',
                    xmx=' -Xmx' + maximum_ram if maximum_ram is not None else ''))
        else:
            start_file.write('#!/bin/bash\nscreen {log}-S {name} {java}{xms}{xmx} -jar Paper.jar nogui\n'.format(
                log='-L ' if screen_log else '',
                name=screen_name,
                java=java,
                xms=' -Xms' + minimum_ram if minimum_ram is not None else '',
                xmx=' -Xmx' + maximum_ram if maximum_ram is not None else ''))
    else:
        start_file.write('#!/bin/bash\n{java}{xms}{xmx} -jar Paper.jar nogui\n'.format(java=java,
                                                                                       xms=' -Xms' + minimum_ram if
                                                                                       minimum_ram is not None else '',
                                                                                       xmx=' -Xmx' + maximum_ram if
                                                                                       maximum_ram is not None else ''))
    start_file.close()
    os.chmod('start.sh', 0o775)

    # Server settings files
    print('Creating server settings files...')

    server_properties = open('server.properties', 'w')
    if motd is not None:
        server_properties.write('motd=' + motd + '\n')
    server_properties.write('max-players=' + str(max_players))
    server_properties.write('\nserver-port=' + str(port))
    server_properties.write('\nquery-port=' + str(port))
    server_properties.write('\nwhite-list=' + str(whitelist).lower())
    if specific_settings:
        if level_type is not None:
            server_properties.write('\nlevel-type=' + level_type.upper())

            if generator_settings is not None:
                server_properties.write('\ngenerator-settings=' + json.dumps(generator_settings))
        if seed is not None:
            server_properties.write('\nlevel-seed=' + seed)
        if max_build_height is not None:
            server_properties.write('\nmax-build-height=' + str(max_build_height))
        if gamemode is not None:
            server_properties.write('\ngamemode=' + gamemode)
        if force_gamemode is not None:
            server_properties.write('\nforce-gamemode=' + str(force_gamemode).lower())
        if difficulty is not None:
            server_properties.write('\ndifficulty=' + difficulty)
        if hardcore is not None:
            server_properties.write('\nhardcore=' + str(hardcore).lower())
        if pvp is not None:
            server_properties.write('\npvp=' + str(pvp).lower())
        if command_blocks is not None:
            server_properties.write('\nenable-command-block=' + str(command_blocks).lower())
        if level_name is not None:
            server_properties.write('\nlevel-name=' + level_name)
        if online_mode is not None or bungeecord is not None:
            server_properties.write(
                '\nonline-mode=' + ('false' if bungeecord is not None and bungeecord else str(online_mode).lower()))
        if allow_flight is not None:
            server_properties.write('\nallow-flight=' + str(allow_flight).lower())
        if view_distance is not None:
            server_properties.write('\nview-distance=' + str(view_distance))
        if simulation_distance is not None:
            server_properties.write('\nsimulation-distance=' + str(simulation_distance))
        if entity_broadcast_range_percentage is not None:
            server_properties.write('\nentity-broadcast-range-percentage=' + str(entity_broadcast_range_percentage))
        if spawn_protection is not None:
            server_properties.write('\nspawn-protection=' + str(spawn_protection))
        if announce_player_achievements is not None:
            server_properties.write('\nannounce-player-achievements=' + str(announce_player_achievements).lower())
        if allow_nether is not None:
            server_properties.write('\nallow-nether=' + str(allow_nether).lower())

        if connection_throttle is not None:
            bukkit_data['settings']['connection-throttle'] = connection_throttle
        if allow_end is not None:
            bukkit_data['settings']['allow-end'] = allow_end

        if bungeecord is not None:
            spigot_data['settings']['bungeecord'] = bungeecord

    if change_patches:
        paper_data['world-settings']['default']['game-mechanics'][
            'fix-curing-zombie-villager-discount-exploit'] = patch_discount_exploit
        paper_data['settings']['unsupported-settings'][
            'allow-permanent-block-break-exploits'] = patch_permanent_block_break_exploit
        paper_data['settings']['unsupported-settings']['allow-piston-duplication'] = patch_piston_duplication

    server_properties.write('\n')
    server_properties.close()
    with open('bukkit.yml', 'w') as bukkit_file:
        yaml.dump(bukkit_data, bukkit_file, default_flow_style=False)
    with open('spigot.yml', 'w') as spigot_file:
        yaml.dump(spigot_data, spigot_file, default_flow_style=False)
    with open('paper.yml', 'w') as paper_file:
        yaml.dump(paper_data, paper_file, default_flow_style=False)

    # whitelist and operators
    if whitelist:
        with open('whitelist.json', 'w') as whitelist_file:
            whitelist_file.write(json.dumps(whitelist_players, indent=2) + '\n')
    with open('ops.json', 'w') as operators_file:
        operators_file.write(json.dumps(operators, indent=2) + '\n')

    # gamerules
    if len(gamerules) > 0:
        log = 'first_start.log'
        print(f'Starting server once to create files... (Output will be written to "{log}")')
        if screen:
            time.sleep(2)
            os.system('screen -L -Logfile {log} -dmS {name} {java}{xms}{xmx} -jar Paper.jar nogui'.format(log=log,
                                                                                                          name=screen_name,
                                                                                                          java=java,
                                                                                                          xms=' -Xms' +
                                                                                                              minimum_ram
                                                                                                          if minimum_ram
                                                                                                             is not None
                                                                                                          else '',
                                                                                                          xmx=' -Xmx' +
                                                                                                              maximum_ram
                                                                                                          if maximum_ram
                                                                                                             is not None
                                                                                                          else ''))
            os.system(f'screen -S {screen_name} -X stuff "stop\n"')
            os.system(f'screen -r {screen_name}; tput cuu1; tput el')
        else:
            os.system('echo "stop" | {java}{xms}{xmx} -jar Paper.jar nogui > {log} 2>&1'.format(java=java,
                                                                                                xms=' -Xms' +
                                                                                                    minimum_ram if
                                                                                                minimum_ram is not
                                                                                                None
                                                                                                else '',
                                                                                                xmx=' -Xmx' +
                                                                                                    maximum_ram if
                                                                                                maximum_ram is not
                                                                                                None
                                                                                                else '',
                                                                                                log=log))

        with open('spigot.yml', 'r+') as spigot_file:
            spigot_data = spigot_file.read().replace('restart-on-crash: false', 'restart-on-crash: ' + (
                'true' if not screen or not restart else str(restart_on_crash).lower()))
            spigot_file.seek(0)
            spigot_file.write(spigot_data)

        with open(log) as log_file:
            if re.search('\\[\\d\\d:\\d\\d:\\d\\d INFO\\]: Timings Reset', log_file.read()):
                print('Setting gamerules...')
                if not specific_settings or level_name is None:
                    level_name = 'world'

                for dimension in ['', '_nether', '_the_end']:
                    level_file = level_name + dimension + '/level.dat'
                    nbtfile = NBTFile(level_file)
                    for gamerule in nbtfile['Data']['GameRules'].tags:
                        if gamerule.name in gamerules:
                            gamerule.value = gamerules[gamerule.name]
                    nbtfile.write_file(level_file)
            else:
                print(f'Starting server failed. Gamerules will not be set. Check {log} for errors.')

    # Plugins
    if certain_plugins:
        os.makedirs('plugins', exist_ok=True)
        print('Downloading plugins...')
        for plugin in plugins.values():
            request.urlretrieve(plugin['url'], 'plugins/' + plugin['file'])

    # Start server
    print('Finished installation! Start now? (Y/n)')
    answer = input('> ').lower()
    if not answer or answer == 'y':
        os.system('./start.sh')


if __name__ == '__main__':
    main()
