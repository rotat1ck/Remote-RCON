import dearpygui.dearpygui as dpg
from rcon.source import Client
import functools
commands_history = []

def append_to_command_input(sender, app_data, user_data):
    player_name = user_data
    current_text = dpg.get_value("command_input")
    new_text = f"{current_text} {player_name}".strip()  # Append the player's name to the existing text
    dpg.set_value("command_input", new_text)

# Updated get_list_of_players function
def get_list_of_players(sender):
    with Client('77.37.246.6', 2589, passwd='zalupa1488') as client:
        response = client.run('list')
        
        prefix, player_names = response.split(':')
        player_names = player_names.strip()
        player_names = player_names.split(', ')
        words = prefix.split()
        numbers = [word for word in words if word.isdigit()]
        
        if dpg.does_item_exist("player_list"):
            dpg.delete_item("player_list")
        
        with dpg.child_window(width=185, height=233, parent="right_column", tag="player_list", border=False):
            dpg.add_text(f"{numbers[0]}/{numbers[1]} Players: ")
            for player in player_names:
                # Create a button for each player and append their name to the command input when clicked
                dpg.add_button(label=player, callback=append_to_command_input, user_data=player)
    update_menu_items()



def execute_command(sender, data):
    command = dpg.get_value("command_input")
    commands_history.append(command)
    with Client('77.37.246.6', 2589, passwd='zalupa1488') as client:
        response = client.run(command)
        if response != "":
            commands_history.append(response)
        else:
            commands_history.append("No answer")
        if dpg.does_item_exist("output_box"):
            dpg.delete_item("output_box")
        with dpg.child_window(width=385, height=234, parent="left_column", tag="output_box",border=False):
            for text in commands_history:
                dpg.add_text(text)

def get_player_names():
    with Client('77.37.246.6', 2589, passwd='zalupa1488') as client:
        response = client.run('list')

        prefix, player_names = response.split(':')
        player_names = player_names.strip()
        player_names = player_names.split(', ')
    return player_names

def update_menu_items():
    if dpg.does_item_exist("DoxMenu"):
        dpg.delete_item("DoxMenu", children_only=True)
    if dpg.does_item_exist("LightMenu"):
        dpg.delete_item("LightMenu", children_only=True)
    create_menu_items()
    
def dox_player_callback(player_name):
    def callback(sender, data):
        dox_player(player_name, sender)
    return callback

def light_player_callback(player_name):
    def callback(sender, data):
        light_player(player_name, sender)
    return callback

def create_menu_items():
    player_names = get_player_names()
    for player in player_names:
        dpg.add_menu_item(label=player, parent="DoxMenu", callback=dox_player_callback(player))
    for player in player_names:
        dpg.add_menu_item(label=player, parent="LightMenu", callback=light_player_callback(player))

def light_player(player_name, sender):
    with Client('77.37.246.6', 2589, passwd='zalupa1488') as client:
        response = client.run('list')
        client.run(f'execute at {player_name} run summon minecraft:lightning_bolt ~ ~ ~')

def dox_player(player_name, sender):
    with Client('77.37.246.6', 2589, passwd='zalupa1488') as client:
        client.run(f'effect give {player_name} minecraft:blindness 3 1 true')
        client.run(f'playsound minecraft:entity.ghast.scream ambient {player_name} ~ ~ ~ 10 0.5 1')
        client.run(f'title {player_name} times 0 40 0')
        client.run(f'title {player_name} subtitle {{\"text\":\"\u0418 \u0441\u043f\u043e\u0440\u0442\u0438\u043a\u043e\u0432\"}}')
        client.run(f'title {player_name} title {{\"text\":\"\u0416\u0434\u0438 \u0434\u043e\u043a\u0441. \u0441\u0432\u0430\u0442\"}}')
        client.run(f'playsound minecraft:entity.ghast.scream ambient {player_name} ~ ~ ~ 10 0.5 1')
        client.run(f'playsound minecraft:entity.ghast.scream ambient {player_name} ~ ~ ~ 10 0.5 1')
        client.run(f'playsound minecraft:entity.ghast.scream ambient {player_name} ~ ~ ~ 10 0.5 1')

dpg.create_context()

with dpg.window(tag="RemoteRCON"):
    with dpg.menu_bar():
        with dpg.menu(label="Troll"):
            with dpg.menu(label="Lightning", tag="LightMenu"):
                dpg.add_menu_item(label="LoadPlayers")

            with dpg.menu(label="Dox", tag="DoxMenu"):
                dpg.add_menu_item(label="LoadPlayers")

        dpg.add_menu_item(label="Load Players", callback=get_list_of_players)

    with dpg.group(horizontal=True):
        with dpg.child_window(width=400, height=250, tag="left_column"):
            with dpg.child_window(width=385, height=234, tag="output_box",border=False):
                pass

        with dpg.child_window(width=200, height=250, tag="right_column"):
            pass

    with dpg.group(horizontal=True):
        with dpg.child_window(width=400, height=58):
            dpg.add_input_text(tag="command_input", hint="/help")
            dpg.add_button(label="Run", callback=execute_command)

            
dpg.create_viewport(title='RemoteRCON', width=640, height=390)
dpg.setup_dearpygui()
dpg.set_viewport_resizable(False)
dpg.show_viewport()
dpg.set_primary_window("RemoteRCON", True)
dpg.start_dearpygui()

dpg.destroy_context()