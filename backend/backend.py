import requests

def checkhash():
    data = {"hash": "3b981e15105be428cbec298e0c619f234819750c38d7e7aea124480cf4d0b9d5"}
    response = requests.post("http://localhost:8000/checkhash", json=data)

    data = response.json()
    status = data.get("success")
    accesscode = data.get("code")
    print(status, accesscode)

checkhash()