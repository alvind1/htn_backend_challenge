from flask import Flask, request, abort

from util import DATABASE_FILE, connect
from data import Users

app = Flask(__name__)

def post_userevent():
  body = request.json
  userid = body['userid']
  event = body['event']
  conn = connect(DATABASE_FILE)
  cur = conn.cursor()
  cur.execute('''
    INSERT OR REPLACE INTO USEREVENTS VALUES (?,?)
  ''', (userid,event))
  conn.commit()
  cur.execute('''
    SELECT EVENT FROM USEREVENTS WHERE USERID==?;
  ''', (userid,))
  events = cur.fetchall()
  cur.close()
  conn.close()
  return [e[0] for e in events]

def get_userevent():
  conn = connect(DATABASE_FILE)
  cur = conn.cursor()
  body = request.args
  if 'userid' not in body:
    abort(400) 
  userid = body['userid']
  cur.execute('''
    SELECT EVENT FROM USEREVENTS WHERE USERID==?;
  ''', (userid,))
  events = cur.fetchall()
  cur.close()
  conn.close()
  return [e[0] for e in events]

@app.route('/userevents/', methods=['GET', 'POST'])
def userevent():
  if request.method=='GET':
    return get_userevent()
  elif request.method=='POST':
    return post_userevent()

def get_user(userid):
  conn = connect(DATABASE_FILE)
  cur = conn.cursor()
  cur.execute('''
    SELECT * FROM USERS LEFT JOIN USERSKILLS ON USERS.USERID==USERSKILLS.USERID WHERE USERS.USERID==?;
  ''',(userid,))
  user_info = cur.fetchall()
  cur.close()
  conn.close()
  if user_info == []:
    abort(404)

  parsed_user = Users.parse_users(user_info)
  return parsed_user[userid]

def update_user(userid):
  s = ""
  body = request.json
  #Only get queries from an allowed list of query parameters
  parsed_request = Users.parse_put_request(body)
  for k, v in parsed_request.items():
    if k == "skills":
      continue
    s += f"{k}='{v}',"

  st = "UPDATE USERS SET " + s[:-1] + " WHERE USERS.USERID==?;"

  conn = connect(DATABASE_FILE)
  cur = conn.cursor()

  if s:
    print(st, userid)
    cur.execute(st, (userid,))

  if 'skills' in body:
    for skill in body['skills']:
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
        ''', (userid, skill['skill'],))
        userskill = cur.fetchone()
        if userskill == None:
          cur.execute('''
            UPDATE SKILLS
            SET FREQUENCY=?
            WHERE SKILL=?;
          ''', (db_skill[1]+1, db_skill[0]))
      cur.execute('''
        INSERT OR REPLACE INTO USERSKILLS
        VALUES (?, ?, ?)
      ''', (userid, skill['skill'], skill['rating'],))
      
  conn.commit()

  cur.execute('''
    SELECT * FROM USERS LEFT JOIN USERSKILLS ON USERS.USERID==USERSKILLS.USERID WHERE USERS.USERID==?;
  ''',(userid,))
  user_info = cur.fetchall()
  cur.close()
  conn.close()
  if user_info == []:
    abort(404)

  parsed_user = Users.parse_users(user_info)

  return parsed_user[userid]

@app.route('/users/<userid>/', methods=['GET', 'PUT'])
def user(userid):
  if request.method == 'GET':
    return get_user(userid)
  elif request.method == 'PUT':
    return update_user(userid)

@app.route('/users/', methods=['GET'])
def get_users():
  queries = request.args
  allowed_args = ['name', 'company', 'email', 'phone']
  query = []
  for arg in allowed_args:
    if arg in queries:
      query.append(f'{arg}=="{queries[arg]}"')
  
  qs = ""
  if query:
    qs = "WHERE " + 'and'.join(query)

  conn = connect(DATABASE_FILE)
  cur = conn.cursor()
  q = "SELECT * FROM USERS LEFT JOIN USERSKILLS ON USERS.USERID==USERSKILLS.USERID " + qs + ";"
  cur.execute(q)
  users = cur.fetchall()
  cur.close()
  conn.close()
  parsed_users = Users.parse_users(users)
  return list(parsed_users.values())

@app.route('/skills/', methods=['GET'])
def get_skills():
  args = request.args
  min_freq = args.get("min_frequency")
  if min_freq and not min_freq.isnumeric():
    min_freq = ""
  max_freq = args.get("max_frequency")
  if max_freq and not max_freq.isnumeric():
    max_freq = ""

  c = ""
  if min_freq or max_freq:
    c = " WHERE "
  if min_freq:
    c += f"SKILLS.FREQUENCY>={min_freq}"
    if max_freq:
      c += " and "
  
  if max_freq:
    c += f"SKILLS.FREQUENCY<={max_freq}"
  
  s = "SELECT * FROM SKILLS" + c

  conn = connect(DATABASE_FILE)
  cursor = conn.cursor()

  cursor.execute(s)
  skills_info = cursor.fetchall()
  skills = []
  for skill in skills_info:
    skills.append({'skill': skill[0], 'rating': skill[1]})

  return skills

if __name__ == '__main__':
  app.run()