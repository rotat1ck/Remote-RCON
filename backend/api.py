import os, time, secrets, string
import logging
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.requests import Request
import sqlite3

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

script_dir = os.path.dirname(__file__)
database_file_path = os.path.join(script_dir, "main.db")


def connect_to_database():
    try:
        conn = sqlite3.connect(database_file_path)
        logging.debug("Connected to database!")
        return conn
    except sqlite3.Error as e:
        logging.error(f"Error connecting to database: {e}")
        return None


def execute_query(conn, query):
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        logging.debug(f"Query executed: {query}")
        logging.debug(f"Results: {results}")
        return results
    except sqlite3.Error as e:
        logging.error(f"Error executing query: {e}")
        return None


def close_database_connection(conn):
    try:
        conn.close()
        logging.debug("Database connection closed!")
    except sqlite3.Error as e:
        logging.error(f"Error closing database connection: {e}")


def generate_access_code():
    characters = string.ascii_letters + string.digits
    access_code = ''.join(secrets.choice(characters) for _ in range(32))
    return access_code


@app.post("/checkhash")
async def fetch_data(request: Request):
    data = await request.json()
    
    hash_value = data.get("hash")
    
    conn = connect_to_database()
    query = f"SELECT id, rights FROM credits WHERE hash='{hash_value}'"
    results = execute_query(conn, query)
    close_database_connection(conn)

    if results == []:
        return JSONResponse(content={"success": 'false'}, status_code=404)
    else:
        timestamp = time.time()
        code = generate_access_code()

        return JSONResponse(content={"success": 'true', "code": code}, status_code=200)
