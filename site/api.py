import os, time, secrets, string
import logging
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.requests import Request
import sqlite3

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

# путь до базы
script_dir = os.path.dirname(__file__)
database_file_path = os.path.join(script_dir, "main.db")

# подключение к базе
def connectToDatabase():
    try:
        conn = sqlite3.connect(database_file_path)
        return conn
    except sqlite3.Error as e:
        logging.error(f"Error connecting to database: {e}")
        
        return None


# функция выполнения sql запросов
def executeQuery(conn, query):
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            logging.debug(f"Query executed: {query}")
            logging.debug(f"Results: {results}")
            
            return results
    except sqlite3.Error as e:
        logging.error(f"Error executing query: {e}")
        
        return None


# отключение от базы
def closeDatabaseConnection(conn):
    try:
        conn.close()
        logging.debug("Database connection closed!")
    except sqlite3.Error as e:
        logging.error(f"Error closing database connection: {e}")


# функия создания кода доступа
def generateAccessCode():
    characters = string.ascii_letters + string.digits
    access_code = ''.join(secrets.choice(characters) for _ in range(32))
    
    return access_code


# создание нового кода и времени его действия
def insertAccessCode(hash_value, timenow, code):
    conn = connectToDatabase()
    query = f"UPDATE credits SET accesscode = '{code}', expires = '{timenow}' WHERE hash = '{hash_value}'"
    new_results = executeQuery(conn, query)
    closeDatabaseConnection(conn)
    
    return new_results


# получение кода и времени окончания действия
def selectAccessCreds(hash_value):
    conn = connectToDatabase()
    query = f"SELECT expires, accesscode FROM credits WHERE hash='{hash_value}'"
    results = executeQuery(conn, query)
    closeDatabaseConnection(conn)
    
    return results


@app.post("/checkhash")
async def fetch_data(request: Request):
    data = await request.json()
    
    # получение хэша от бэкэнда
    hash_value = data.get("hash")
    
    # получение id пользователя и его прав
    conn = connectToDatabase()
    query = f"SELECT id, rights FROM credits WHERE hash='{hash_value}'"
    results = executeQuery(conn, query)
    closeDatabaseConnection(conn)
    
    # если хэш не верен
    if results == []:
        return JSONResponse(content={"success": 'false'}, status_code=404)
    else:
        # id пользователя и его права
        userid = results[0][0]
        oplvl = results[0][1]
        
        # получение кода и времени окончания действия
        results = selectAccessCreds(hash_value=hash_value)
        timenow = time.time()
        
        # если кода нет в базе(первый вход)
        if results[0][0] == None:
            # создание нового кода и времени его действия
            insertAccessCode(hash_value=hash_value, timenow=timenow, code=generateAccessCode())
            
            # получение кода и времени окончания действия
            results = selectAccessCreds(hash_value=hash_value)
            
            timestamp = results[0][0]
            code = results[0][1]
        
        # если код устарел
        elif (timenow - results[0][0]) > 3600:
            # создание нового кода и времени его действия
            insertAccessCode(hash_value=hash_value, timenow=timenow, code=generateAccessCode())
            
            # получение кода и времени окончания действия
            results = selectAccessCreds(hash_value=hash_value)
            
            timestamp = results[0][0]
            code = results[0][1]
        
        else:
            # получение кода и времени окончания действия
            results = selectAccessCreds(hash_value=hash_value)
            
            timestamp = results[0][0]
            code = results[0][1]
            
        # отправка результата
        return JSONResponse(content={"success": 'true', "id": userid, "oplvl": oplvl, "code": code, "expiredate": timestamp}, status_code=200)
    
@app.post("/main")
async def handleCommands(request: Request):
    data = await request.json()
    
    # получение ключа от бэкэнда
    code_value = data.get("code")
    
    # проверка кода доступа пользователя
    conn = connectToDatabase()
    query = f"SELECT expires, rights, id FROM credits WHERE accesscode='{code_value}'"
    results = executeQuery(conn, query)
    closeDatabaseConnection(conn)
    try:
        expireDate = results[0][0]
        oplvl = results[0][1]
        userid = results[0][2]
        print(userid, oplvl, expireDate)
    


    
        # если код не верен
        if results[0][1] == None:
            return JSONResponse(content={"success": 'false'}, status_code=403)
        else:
            timenow = time.time()
                
            # если код устарел 
            if (timenow - results[0][0]) > 3600:
                # создание нового кода и времени его действия
                code = generateAccessCode()
                conn = connectToDatabase()
                query = f"UPDATE credits SET accesscode = '{code}', expires = '{timenow}' WHERE accesscode = '{code_value}'"
                newresults = executeQuery(conn, query)
                closeDatabaseConnection(conn)
                
                # получение нового ключа
                conn = connectToDatabase()
                query = f"SELECT accesscode FROM credits WHERE id='{userid}'"
                results = executeQuery(conn, query)
                code_value = results[0][0]
                closeDatabaseConnection(conn)
                
            # отправка в RCON
            return JSONResponse(content={"success": 'true', 'id': userid, 'accesscode': code_value, 'oplvl': oplvl}, status_code=200)
    except IndexError as e:
        print(e)
        return JSONResponse(content={"success": 'false'}, status_code=403)
@app.post("/ban")
async def handleBan(request: Request):
    pass