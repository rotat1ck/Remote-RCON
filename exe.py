import dearpygui.dearpygui as dpg
from rcon.source import Client

def get_list_of_players(sender):
    with Client('77.37.246.6', 2589, passwd='zalupa1488') as client:
        response = client.run('list')
        
        prefix, player_names = response.split(':')
        player_names = player_names.strip()
        player_names = player_names.split(', ')
        words = prefix.split()
        numbers = [word for word in words if word.isdigit()]
        print(f"     {numbers[0]}/{numbers[1]}")
        
        if dpg.does_item_exist("player_list"):
            dpg.delete_item("player_list")
        
        with dpg.child_window(width=400, height=233, parent="right_column", tag="player_list"):
            dpg.add_text(f"{numbers[0]}/{numbers[1]} Players: ")
            for player in player_names:
                dpg.add_text(player)
def lighting_all():
    with Client('77.37.246.6', 2589, passwd='zalupa1488') as client:
        response = client.run('list')
        
        prefix, player_names = response.split(':')
        player_names = player_names.strip()
        player_names = player_names.split(', ')
        for i in player_names:
            client.run(f'execute at {i} run summon minecraft:lightning_bolt ~ ~ ~')
def jdi_dox():
    with Client('77.37.246.6', 2589, passwd='zalupa1488') as client:
        client.run('effect give @a minecraft:blindness 3 1 true')
        client.run('playsound minecraft:entity.ghast.scream ambient @a ~ ~ ~ 10 0.5 1')
        client.run('title @a times 0 40 0')
        client.run('title @a subtitle {"text":"\u0418 \u0441\u043f\u043e\u0440\u0442\u0438\u043a\u043e\u0432"}')
        client.run('title @a title {"text":"\u0416\u0434\u0438 \u0434\u043e\u043a\u0441. \u0441\u0432\u0430\u0442"}')
        client.run('playsound minecraft:entity.ghast.scream ambient @a ~ ~ ~ 10 0.5 1')
        client.run('playsound minecraft:entity.ghast.scream ambient @a ~ ~ ~ 10 0.5 1')
        client.run('playsound minecraft:entity.ghast.scream ambient @a ~ ~ ~ 10 0.5 1')
    
    

dpg.create_context()

with dpg.window(tag="RemoteRCON"):
    with dpg.menu_bar():
        with dpg.menu(label="Troll"):
            dpg.add_menu_item(label="Lightning all", callback=lighting_all)
            dpg.add_menu_item(label="Dox", callback=jdi_dox)

            with dpg.menu(label="Settings"):
                dpg.add_menu_item(label="Setting 1", callback=lambda sender: print(f"Menu Item: {sender}"), check=True)
                dpg.add_menu_item(label="Setting 2", callback=lambda sender: print(f"Menu Item: {sender}"))

        dpg.add_menu_item(label="Load Players", callback=get_list_of_players)

    with dpg.group(horizontal=True):
        with dpg.child_window(width=400, height=250):
            pass

        with dpg.child_window(width=200, height=250, tag="right_column"):
            pass

dpg.create_viewport(title='RemoteRCON', width=640, height=325)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("RemoteRCON", True)
dpg.start_dearpygui()

dpg.destroy_context()