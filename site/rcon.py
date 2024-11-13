from rcon.source import Client
import os

oplvl2 = ['list', 'kick', 'dox', 'pardon']
oplvl3 = ['list', 'kick', 'ban', 'dox', 'light', 'start', 'pardon']


def check(command, oplvl):
    if oplvl == 2:
        for i in oplvl2:
            if i in command:
                return main(command)
    elif oplvl == 3:
        for i in oplvl3:
            if i in command:
                return main(command)
    elif oplvl == 4:
        return main(command)
    else:
        return 'Permission denied!'
    
    
def main(command):
    if 'list' in command:
        return get_list_of_players()
    elif 'dox' in command:
        return dox_player(command)
    elif 'light' in command:
        return light_player(command)
    elif 'start' in command:
        return start_server()
    else:
        return execute_command(command)
    

def start_server():
    try:
        with Client('77.37.246.6', 2589, passwd='xxxx') as client:
            response = client.run('list')
            #client.timeout()
        if response:
            return 'Server already running'
    except TimeoutError:
        os.chdir("C:/goidaserver")
        os.startfile("run.bat")
        return 'Starting server'

def get_list_of_players():
    with Client('77.37.246.6', 2589, passwd='xxxx') as client:
        response = client.run('list')
        return response



def execute_command(command):
    with Client('77.37.246.6', 2589, passwd='xxxx') as client:
        response = client.run(command)
        if response != "":
            return response
        else:
            return "Successfuly executed"


def light_player(command):
    player_name = command[6:]
    with Client('77.37.246.6', 2589, passwd='xxxx') as client:
        client.run(f'execute at {player_name} run summon minecraft:lightning_bolt ~ ~ ~')
    return "Successfuly executed"

def dox_player(command):
    player_name = command[4:]
    with Client('77.37.246.6', 2589, passwd='xxxx') as client:
        client.run(f'effect give {player_name} minecraft:blindness 3 1 true')
        client.run(f'playsound minecraft:entity.ghast.scream ambient {player_name} ~ ~ ~ 10 0.5 1')
        client.run(f'title {player_name} times 0 40 0')
        client.run(f'title {player_name} subtitle {{\"text\":\"\u0418 \u0441\u043f\u043e\u0440\u0442\u0438\u043a\u043e\u0432\"}}')
        client.run(f'title {player_name} title {{\"text\":\"\u0416\u0434\u0438 \u0434\u043e\u043a\u0441. \u0441\u0432\u0430\u0442\"}}')
        client.run(f'playsound minecraft:entity.ghast.scream ambient {player_name} ~ ~ ~ 10 0.5 1')
        client.run(f'playsound minecraft:entity.ghast.scream ambient {player_name} ~ ~ ~ 10 0.5 1')
        client.run(f'playsound minecraft:entity.ghast.scream ambient {player_name} ~ ~ ~ 10 0.5 1')
    return "Successfuly executed"