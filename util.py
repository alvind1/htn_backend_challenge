import sqlite3

JSON_DATA_FILE = "HTN_2023_BE_Challenge_Data.json" 
DATABASE_FILE = "htnDB.db"
MAX_INT = 2**32-1

def connect(db):
  conn = sqlite3.connect(db)
  return conn
