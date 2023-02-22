import json
import sqlite3
import random

from util import DATABASE_FILE, JSON_DATA_FILE, MAX_INT, connect

def drop_tables():
  conn = connect(DATABASE_FILE)
  cur = conn.cursor()
  cur.execute("DROP TABLE IF EXISTS USERSKILLS;")
  cur.execute("DROP TABLE IF EXISTS USERS;")
  cur.execute("DROP TABLE IF EXISTS SKILLS;")
  cur.execute("DROP TABLE IF EXISTS USEREVENTS;")
  conn.commit()
  cur.close()
  conn.close()


def create_tables():
  conn = connect(DATABASE_FILE)
  cur = conn.cursor()
  cur.execute('''
  CREATE TABLE IF NOT EXISTS USERS
  (
    USERID TEXT PRIMARY KEY,
    NAME TEXT NOT NULL,
    COMPANY TEXT NOT NULL,
    EMAIL TEXT NOT NULL,
    PHONE TEXT NOT NULL
  );
  ''')

  cur.execute('''
  CREATE TABLE IF NOT EXISTS USERSKILLS
  (
    USERID TEXT REFERENCES USERS(USERID) NOT NULL,
    SKILL TEXT REFERENCES SKILLS(SKILL) NOT NULL,
    RATING INTEGER NOT NULL,
    PRIMARY KEY (USERID, SKILL)
  );
  ''')

  cur.execute('''
  CREATE TABLE IF NOT EXISTS SKILLS
  (
    SKILL TEXT PRIMARY KEY NOT NULL,
    FREQUENCY INTEGER NOT NULL
  );
  ''')

  cur.execute('''
  CREATE TABLE IF NOT EXISTS EVENTS 
  (
    EVENT TEXT PRIMARY KEY NOT NULL,
    FREQUENCY INTEGER NOT NULL
  );
  ''')

  cur.execute('''
  CREATE TABLE IF NOT EXISTS USEREVENTS 
  (
    USERID TEXT REFERENCES USERS(USERID) NOT NULL,
    EVENT TEXT REFERENCES EVENTS(EVENT) NOT NULL,
    PRIMARY KEY (USERID, EVENT)
  );
  ''')

  conn.commit()

  cur.close()
  conn.close()

drop_tables()
create_tables()

f = open(JSON_DATA_FILE)
data = json.load(f)

conn = connect(DATABASE_FILE)
cur = conn.cursor()

for item in data:
  inserted_user = False
  attempts = 0

  #In case we randomly generate an in-use userid
  while not inserted_user and attempts < 100:
    user_id = random.randint(0, MAX_INT)
    attempts += 1
    try:
      cur.execute('''
        INSERT INTO USERS
        VALUES (?, ?, ?, ?, ?);
      ''', (user_id, item['name'], item['company'], item['email'], item['phone']))
      inserted_user = True
    except sqlite3.IntegrityError as e:
      if attempts >= 100:
        raise e
  if attempts >= 100:
    raise sqlite3.IntegrityError

  for skill in item['skills']:
    cur.execute('''
      SELECT * FROM SKILLS WHERE SKILL=?
    ''', (skill['skill'],))
    db_skill = cur.fetchone()
    if db_skill == None:
      cur.execute('''
        INSERT INTO SKILLS
        VALUES (?,?)
      ''', (skill['skill'], 0,))
    else:
      cur.execute('''
        SELECT * FROM USERSKILLS WHERE USERID=? AND SKILL=?
      ''', (user_id, skill['skill'],))
      userskill = cur.fetchone()
      #Only increase the frequency if the added skill is not a duplicate of a previous user's skill
      if userskill == None:
        cur.execute('''
          UPDATE SKILLS
          SET FREQUENCY=?
          WHERE SKILL=?;
        ''', (db_skill[1]+1, db_skill[0]))
    cur.execute('''
      INSERT OR REPLACE INTO USERSKILLS
      VALUES (?, ?, ?)
    ''', (user_id, skill['skill'], skill['rating'],))
    
conn.commit()

cur.close()
conn.close()
