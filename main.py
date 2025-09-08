# filename: main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import sqlite3

app = FastAPI(title="Sample Microservice API")

# Database setup
def init_db():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS items
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name TEXT NOT NULL,
                       description TEXT,
                       price REAL NOT NULL)''')
    conn.commit()
    conn.close()

init_db()

# Request model
class Item(BaseModel):
    name: str
    description: str
    price: float

# Routes
@app.post("/items", response_model=Item)
def create_item(item: Item):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (name, description, price) VALUES (?, ?, ?)",
                   (item.name, item.description, item.price))
    conn.commit()
    conn.close()
    return item

@app.get("/items", response_model=List[Item])
def get_items():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, description, price FROM items")
    rows = cursor.fetchall()
    conn.close()
    return [Item(name=row[0], description=row[1], price=row[2]) for row in rows]

@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, description, price FROM items WHERE id=?", (item_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Item not found")
    return Item(name=row[0], description=row[1], price=row[2])

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id=?", (item_id,))
    conn.commit()
    conn.close()
    return {"message": f"Item {item_id} deleted successfully"}
