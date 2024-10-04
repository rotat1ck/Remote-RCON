import requests, socket, sys, json

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
        print("Error:", response.status_code)
    conn.close()

def handleCommand(command, accesscode):
    data = {"code": accesscode}
    response = requests.post("http://localhost:8000/main", json=data)
    if response.status_code == 200:
        try:
            data = response.json()
            userid = data.get("id")
            oplvl = data.get("oplevel")
            code = data.get("accesscode")
        except json.JSONDecodeError:
            print("Invalid JSON response:", response.text)
    else:
        print("Error:", response.status_code)
def server():
    host, port = "0.0.0.0", 7777
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(10)
    
    while True:
        try:
            conn, addr = server.accept()
            data = conn.recv(1024) 
            hash_value = data.decode()
            if hash_value[0] != '/':
                checkhash(hash_value, conn, addr)
            else:
                command = hash_value
                data = conn.recv(1024) 
                accesscode = data.decode()
                handleCommand(command, accesscode)
        except KeyboardInterrupt:
            server.close()
            exit()

if __name__ == "__main__":
    server()