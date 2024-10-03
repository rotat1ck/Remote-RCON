import dearpygui.dearpygui as dpg
import hashlib


login =''
password =''

dpg.create_context()

def handlelogin(sender):
    global login
    login = dpg.get_value(sender)


def handlepass(sender):
    global password
    password = dpg.get_value(sender)


def check():
    global login
    global password
    data = (login + password).encode('utf-8')
    data = hashlib.sha256(data).hexdigest()
    print(data)
    

with dpg.window(tag="Auth"):
    dpg.add_text("Input password")
    inputlogin = dpg.add_input_text(label="login", hint="Enter login", callback=handlelogin)
    inputpass = dpg.add_input_text(label="password", hint="Enter password", callback=handlepass)
    check_button = dpg.add_button(label="Log in", callback=check)

dpg.create_viewport(title='Auth', width=600, height=200)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Auth", True)
dpg.start_dearpygui()

dpg.destroy_context()