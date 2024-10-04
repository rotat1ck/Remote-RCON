import requests

def checkhash():
    data = {"hash": "3b981e15105be428cbec298e0c619f234819750c38d7e7aea124480cf4d0b9d5"}
    response = requests.post("http://localhost:8000/checkhash", json=data)

    data = response.json()
    status = data.get("success")
    userid = data.get("id")
    oplevel = data.get("level")
    accesscode = data.get("code")
    expiredate = data.get("expiredate")
    print(status, userid, oplevel, accesscode, expiredate)

checkhash()