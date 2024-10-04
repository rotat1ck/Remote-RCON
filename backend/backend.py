import requests, socket, sys, json

def checkhash(hash_value, conn):
    data = {"hash": hash_value}
    response = requests.post("http://localhost:8000/checkhash", json=data)

    if response.status_code == 200:
        try:
            data = response.json()
            status = data.get("success")
            userid = data.get("id")
            oplevel = data.get("level")
            accesscode = data.get("code")
            expiredate = data.get("expiredate")
            print(status, userid, oplevel, accesscode, expiredate)
            conn.sendall(f"{accesscode}".encode())
        except json.JSONDecodeError:
            print("Invalid JSON response:", response.text)
    else:
        print("Error:", response.status_code)
    conn.close()

def server():
    host, port = "0.0.0.0", 7777
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(10)
    
    while True:
        try:
            print ("Waiting for incoming connections...")
            conn, addr = server.accept()
            print(addr)
            data = conn.recv(1024) 
            hash_value = data.decode()
            checkhash(hash_value, conn)
        except KeyboardInterrupt:
            server.close()
            exit()

if __name__ == "__main__":
    server()