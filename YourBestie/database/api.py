from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import mysql.connector
from typing import List

# Database connection
DB_CONFIG = {
    "host": "sql5.freesqldatabase.com",
    "user": "sql5768467",
    "password": "[REDACTED]",
    "database": "sql5768467",
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# FastAPI app
app = FastAPI()

# Pydantic models for input validation
class User(BaseModel):
    username: str
    password: str

class Group(BaseModel):
    id: int
    title: str

class Event(BaseModel):
    id: str
    beginning: str  # Format: YYYY-MM-DD HH:MM:SS
    ending: str
    title: str
    descr: str
    place: str

#Dev Routes
@app.post("/users/")
def create_user(user: User):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Usr (username, password) VALUES ( %s, %s)",
                       (user.username, user.password))
        conn.commit()
    except mysql.connector.Error as err:
        raise HTTPException(status_code=400, detail=str(err))
    finally:
        cursor.close()
        conn.close()
    return {"message": "User created successfully"}

@app.post("/groups/")
def create_group(group: Group):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Grp (id, title) VALUES (%s, %s)",
                       (group.id, group.title))
        conn.commit()
    except mysql.connector.Error as err:
        raise HTTPException(status_code=400, detail=str(err))
    finally:
        cursor.close()
        conn.close()
    return {"message": "Group created successfully"}

@app.post("/events/")
def create_event(event: Event):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Evnt (id, beginning, ending, title, descr, place)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (event.id, event.beginning, event.ending, event.title, event.descr, event.place))
        conn.commit()
    except mysql.connector.Error as err:
        raise HTTPException(status_code=400, detail=str(err))
    finally:
        cursor.close()
        conn.close()
    return {"message": "Event created successfully"}

@app.get("/users/")
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Usr")
        users = cursor.fetchall()
    except mysql.connector.Error as err:
        raise HTTPException(status_code=400, detail=str(err))
    finally:
        cursor.close()
        conn.close()
    return users

#Useful Routes
@app.get("/events/{date}/{group_id}")
def get_events_by_date_and_group(date: str, group_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
            SELECT Evnt.* FROM Evnt
            JOIN Event_Group ON Evnt.id = Event_Group.event_id
            WHERE Event_Group.group_id = %s
            AND DATE(Evnt.beginning) LIKE %s
        """
        cursor.execute(query, (group_id, date))
        events = cursor.fetchall()
    except mysql.connector.Error as err:
        raise HTTPException(status_code=400, detail=str(err))
    finally:
        cursor.close()
        conn.close()
    return events

@app.post("/register/")
def register(user: User):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Usr WHERE username = %s", (user.username,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Username already exists")
        hashed_password = get_password_hash(user.password)
        cursor.execute("INSERT INTO Usr (username, password) VALUES (%s, %s)",
                       (user.username, hashed_password))
        conn.commit()
    except mysql.connector.Error as err:
        raise HTTPException(status_code=400, detail=str(err))
    finally:
        cursor.close()
        conn.close()
    return {"message": "User registered successfully"}

@app.post("/login/")
def login(user: User):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Usr WHERE username = %s", (user.username,))
        db_user = cursor.fetchone()
        if not db_user or not verify_password(user.password, db_user['password']):
            raise HTTPException(status_code=401, detail="Invalid username or password")
    except mysql.connector.Error as err:
        raise HTTPException(status_code=400, detail=str(err))
    finally:
        cursor.close()
        conn.close()
    return {"message": "Login successful"}
