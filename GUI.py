import dearpygui.dearpygui as dpg
import hashlib, socket


login =''
password =''

dpg.create_context()

def handlelogin(sender):
    global login
    login = dpg.get_value(sender)


def handlepass(sender):
    global password
    password = dpg.get_value(sender)


def createHash():
    global login
    global password
    data = (login + password).encode('utf-8')
    hash_value = hashlib.sha256(data).hexdigest()
    sendHash(hash_value)
    
def sendHash(hash_value):
    HOST, PORT = "77.37.246.6", 7777

    data = hash_value

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((HOST, PORT))
        sock.sendall(bytes(data,encoding="utf-8"))

        received = sock.recv(1024)
        received = received.decode("utf-8")

    except Exception as e:
        print(e)
    finally:
        sock.close()

    print (f"Sent: {data}")
    print (f"Received: {received}")
    
    
with dpg.window(tag="Auth"):
    dpg.set_global_font_scale(2)
    dpg.add_text("Remote RCON", indent=205)

    inputlogin = dpg.add_input_text(hint="Enter login", callback=handlelogin, indent=160, width = 250)

    inputpass = dpg.add_input_text(hint="Enter password", callback=handlepass, indent=160, width = 250, password=True)

    check_button = dpg.add_button(label="Log in", callback=createHash, indent=235, height=35)

dpg.create_viewport(title='Auth', width=600, height=300)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Auth", True)
dpg.start_dearpygui()

dpg.destroy_context()