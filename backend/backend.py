import requests
import socket
import json
import threading

v = 1.0 

class TimeoutException(Exception):
    pass

def checkhash(hash_value, conn, addr):
    data = {"hash": hash_value}
    response = requests.post("http://localhost:8000/checkhash", json=data)

    if response.status_code == 200:
        try:
            data = response.json()
            userid = data.get("id")
            oplvl = data.get("oplvl")
            accesscode = data.get("code")
            print(f"Подключился пользователь: {userid} | IP: {addr[0]}\nУровень доступа: {oplvl}\nКод: {accesscode}")
            conn.sendall(f"{accesscode}".encode())
        except json.JSONDecodeError:
            print("Invalid JSON response:", response.text)
    else:
        conn.sendall(f"Access denied".encode())
        print("Error:", response.status_code)


def handleCommand(conn, command, accesscode):
    data = {"code": accesscode}
    response = requests.post("http://localhost:8000/main", json=data)
    if response.status_code == 200:
        try:
            data = response.json()
            userid = data.get("id")
            oplvl = data.get("oplvl")
            code = data.get("accesscode")
            # выполнение rcon команды
            import rconexec
            try:
                dataToSend = rconexec.check(command, oplvl)
            except TimeoutError:
                dataToSend = 'Server is down. Use /start'
            print(f"Пользователь {userid} | Выполнил команду {command}")
            conn.sendall(f"{dataToSend}".encode())
        except json.JSONDecodeError:
            print("Invalid JSON response:", response.text)
    else:
        print("Error:", response.status_code)


def client_handler(conn, addr):
    print(f"Connected by {addr}")
    try:
        while True:
            data = conn.recv(10240)
            if not data:
                break
            hash_value = data.decode()
            if hash_value == 'keepalive':
                continue
            elif hash_value[0] != '/' and len(hash_value) == 64:
                checkhash(hash_value, conn, addr)
            else:
                command = hash_value[1:]
                data = conn.recv(1024)
                accesscode = data.decode()
                handleCommand(conn, command, accesscode)
    except ConnectionResetError:
        pass
    finally:
        print(f"Connection with {addr} closed.")


def server():
    host, port = "0.0.0.0", 7777
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen(10)
        print("Server is listening on port", port)

        while True:
            try:
                conn, addr = server.accept()
                client_thread = threading.Thread(target=client_handler, args=(conn, addr))
                client_thread.daemon = True
                client_thread.start()
            except KeyboardInterrupt:
                print("Server shutting down.")
                break

if __name__ == "__main__":
    server()