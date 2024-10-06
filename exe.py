import threading
import time
import socket
import dearpygui.dearpygui as dpg
import dearpygui.dearpygui as dpg
import hashlib
import socket

def auth():
    commands_history = []
    HOST, PORT = "77.37.246.6", 7777
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))  # Connect once

    def keep_alive():
        while True:
            try:
                sock.sendall(bytes('keepalive', encoding="utf-8"))
                time.sleep(60)  # Wait for 60 seconds before sending the next keep-alive
            except Exception as e:
                print(f"Keep-alive error: {e}")
                break

    # Start the keep-alive thread
    threading.Thread(target=keep_alive, daemon=True).start()

    def get_data(command, accesscode):
        response = ""
        try:
            sock.sendall(bytes(command, encoding="utf-8"))
            sock.sendall(bytes(accesscode, encoding="utf-8"))

            response = sock.recv(1024)
            response = response.decode("utf-8")
        except Exception as e:
            print(e)
        return response

    def append_to_command_input(sender, app_data, user_data):
        player_name = user_data
        current_text = dpg.get_value("command_input")
        new_text = f"{current_text} {player_name}".strip()
        dpg.set_value("command_input", new_text)

    def get_list_of_players(sender):
        response = get_data(command='/list', accesscode=accesscode)
        if ':' in response:
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
                    dpg.add_button(label=player, callback=append_to_command_input, user_data=player)
            update_menu_items()

    def execute_command(sender, data):
        command = dpg.get_value("command_input")
        commands_history.append(command)
        response = get_data(command=command, accesscode=accesscode)
        
        commands_history.append(response)

        if dpg.does_item_exist("output_box"):
            dpg.delete_item("output_box")
        with dpg.child_window(width=385, height=234, parent="left_column", tag="output_box",border=False):
            for text in commands_history:
                dpg.add_text(text)

    def get_player_names():
        response = get_data(command='/list', accesscode=accesscode)
        if ':' in response:
            prefix, player_names = response.split(':')
            player_names = player_names.strip()
            player_names = player_names.split(', ')
            return player_names
        else:
            print("Error: Invalid response from server")
            return []

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
        response = get_data(command=f'/light {player_name}', accesscode=accesscode)

    def dox_player(player_name, sender):
        response = get_data(command=f'/dox {player_name}', accesscode=accesscode)

    def cleanup():
        sock.close()
        print("Socket connection closed.")

    login = ''
    password = ''

    dpg.create_context()

    def handlelogin(sender):
        global login
        login = dpg.get_value(sender)

    def handlepass(sender):
        global password
        password = dpg.get_value(sender)

    def createHash(sender, data):
        global login
        global password
        data = (login + password).encode('utf-8')
        hash_value = hashlib.sha256(data).hexdigest()
        sendHash(hash_value)

    def sendHash(hash_value):
        data = hash_value

        try:
            sock.sendall(bytes(data, encoding="utf-8"))
            global accesscode
            received = sock.recv(1024)
            received = received.decode("utf-8")
            if received != 'Access denied':
                accesscode = received
                login_callback()
            else:
                dpg.set_value("auth_feedback", "Access denied!")
        except Exception as e:
            print("Connection error:", e)


    with dpg.window(tag="Auth", label="Authentication"):
        dpg.set_global_font_scale(2)
        dpg.add_text("Remote RCON", indent=205)

        dpg.add_input_text(hint="Enter login", callback=handlelogin, indent=160, width=250)
        dpg.add_input_text(hint="Enter password", callback=handlepass, indent=160, width=250, password=True)
        dpg.add_button(label="Log in", callback=createHash, indent=235, height=35, tag="login_button")
        dpg.add_text("", tag="auth_feedback", indent=195)
        
    with dpg.window(tag="RemoteRCONWindow", label='Remote RCON', show=False):
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
            dpg.add_text("v. 1.0")
                
    dpg.create_viewport(title='Authentication', width=600, height=300)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_viewport_resizable(False)
    dpg.set_primary_window("Auth", True)
    dpg.start_dearpygui()

def login_callback():
    # Hide the authentication window
    dpg.hide_item("Auth")
    # Show the RemoteRCON window
    dpg.show_item("RemoteRCONWindow")
    # Change the viewport title to reflect the new window
    dpg.set_viewport_title("RemoteRCON")
    # Resize the viewport if needed
    dpg.set_viewport_width(640)
    dpg.set_viewport_height(390)
    # Set the RemoteRCON window as the primary window
    dpg.set_primary_window("RemoteRCONWindow", True)
    dpg.set_global_font_scale(1)
    


auth()