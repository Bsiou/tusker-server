import mysql.connector
from flask import Flask, escape, request, session
from flask.json import dumps
from flask_cors import CORS
import uuid
import hashlib

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="secret",
  database="tuskerdb"
)

print(mydb) 

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route('/category/create', methods=['POST'])
def create_category():
	color=request.json['color']
	name=request.json['name']
	user_id=session['user_id']
	mycursor = mydb.cursor()

	sql = "INSERT INTO category ( name, color, user_id ) VALUES (%s, %s,%s)"
	val = (name,color,user_id)
	mycursor.execute(sql, val)
	mydb.commit()
	print(mycursor.rowcount, "record inserted.")
	if mycursor.rowcount==1:
		return dumps({ "success":True})
	else:
		return dumps({ "success":False})

@app.route('/category/edit', methods=['POST'])
def edit_category():
	color=request.json['color']
	name=request.json['name']
	cat_id=request.json['cat_id']
	user_id=session['user_id']
	
	mycursor = mydb.cursor()
	sql="UPDATE  category SET name=%s, color=%s where cat_id=%s and user_id=%s"
	val = (name,color,cat_id,user_id)
	mycursor.execute(sql, val)
	mydb.commit()
	print(mycursor.rowcount, "record inserted.")
	if mycursor.rowcount==1:
		return dumps({ "success":True})
	else:
		return dumps({ "success":False})

@app.route('/category/delete', methods=['POST'])
def creat_category():
	cat_id=request.json['cat_id']
	user_id=session['user_id']

	mycursor = mydb.cursor()
	sql="DELETE FROM category WHERE cat_id=%s and user_id=%s" 
	val=(cat_id,user_id)
	mycursor.execute(sql, val)
	mydb.commit()
	print(mycursor.rowcount, "record inserted.")
	if mycursor.rowcount==1:
		return dumps({ "success":True})
	else:
		return dumps({ "success":False})

@app.route('/task/create', methods=['POST'])
def creat_task():
	name=request.json['name']
	date=request.json['date']
	time=request.json['time']
	cat_id=request.json['cat_id']
	user_id=session['user_id']
	description=request.json['description']

	mycursor = mydb.cursor()
	sql = "INSERT INTO task ( name, date , time , cat_id, user_id,description  ) VALUES (%s, %s,%s,%s,%s,%s)"
	val=(name,date,time,cat_id,user_id,description)
	mycursor.execute(sql, val)
	mydb.commit()
	print(mycursor.rowcount, "record inserted.")
	if mycursor.rowcount==1:
		return dumps({ "success":True})
	else:
		return dumps({ "success":False})

@app.route('/task/edit', methods=['POST'])
def edit_task():
	name=request.json['name']
	date=request.json['date']
	time=request.json['time']
	cat_id=request.json['cat_id']
	user_id=session['user_id']
	task_id=request.json['task_id']
	description=request.json['description']


		
	mycursor = mydb.cursor()
	sql="UPDATE  task SET name=%s, date=%s, time=%s , cat_id=%s, description=%s  where task_id=%s and user_id=%s"
	val = (name,date,time,cat_id,description,task_id,user_id)
	mycursor.execute(sql, val)
	mydb.commit()
	print(mycursor.rowcount, "record inserted.")
	if mycursor.rowcount==1:
		return dumps({ "success":True})
	else:
		return dumps({ "success":False})


@app.route('/task/delete', methods=['POST'])
def delete_task():
	task_id=request.json['task_id']
	user_id=session['user_id']

	mycursor = mydb.cursor()
	sql="DELETE FROM task WHERE task_id=%s and user_id=%s" 
	val=(task_id,user_id)
	mycursor.execute(sql, val)
	mydb.commit()
	print(mycursor.rowcount, "record inserted.")
	if mycursor.rowcount==1:
		return dumps({ "success":True})
	else:
		return dumps({ "success":False})


@app.route('/daytask/create', methods=['POST'])
def creat_daytask():

	name=request.json['name']
	date=request.json['date']
	cat_id=request.json['cat_id']
	user_id=session['user_id']
	difficulty=request.json['difficulty']
	done=request.json['done']
	description=request.json['description']


	mycursor = mydb.cursor()
	sql = "INSERT INTO daytask ( name, date , cat_id, user_id, difficulty, done,description  ) VALUES (%s, %s,%s,%s,%s,%s,%s)"
	val=(name,date,cat_id,user_id,difficulty,done,description)
	mycursor.execute(sql, val)
	mydb.commit()
	print(mycursor.rowcount, "record inserted.")
	if mycursor.rowcount==1:
		return dumps({ "success":True})
	else:
		return dumps({ "success":False})

@app.route('/daytask/edit', methods=['POST'])
def edit_daytask():

	name=request.json['name']
	date=request.json['date']
	cat_id=request.json['cat_id']
	user_id=session['user_id']
	difficulty=request.json['difficulty']
	done=request.json['done']
	daytask_id=request.json['daytask_id']
	description=request.json['description']


	mycursor = mydb.cursor()
	sql = "UPDATE daytask set name=%s, date=%s, cat_id=%s, difficulty=%s, done=%s,description=%s where daytask_id=%s and user_id=%s "
	val=(name,date,cat_id,difficulty,done,description, daytask_id,user_id)
	mycursor.execute(sql, val)
	mydb.commit()
	print(mycursor.rowcount, "record inserted.")
	if mycursor.rowcount==1:
		return dumps({ "success":True})
	else:
		return dumps({ "success":False})


@app.route('/daytask/delete', methods=['POST'])
def delete_daytask():
	daytask_id=request.json['daytask_id']
	user_id=session['user_id']

	mycursor = mydb.cursor()
	sql="DELETE FROM daytask WHERE daytask_id=%s and user_id=%s" 
	val=(daytask_id,user_id)
	mycursor.execute(sql, val)
	mydb.commit()
	print(mycursor.rowcount, "record inserted.")
	if mycursor.rowcount==1:
		return dumps({ "success":True})
	else:
		return dumps({ "success":False})

@app.route('/categories/show', methods=['GET'])
def categories_show():
	user_id=session['user_id']
	mycursor = mydb.cursor()
	val=(user_id,)
	mycursor.execute("SELECT * FROM category where user_id=%s",val)


	myresult = mycursor.fetchall()
	categories = []
	for x in myresult:
		mycategory = {
			"cat_id": x[0],
			"name": x[1],
			"color": x[2],
		}
		categories.append(mycategory)
	return dumps(categories)

@app.route('/tasks/show', methods=['GET'])
def tasks_show():
	user_id=session['user_id']
	mycursor = mydb.cursor()
	val=(user_id,)
	mycursor.execute("SELECT * FROM task where user_id=%s",val)
	myresult = mycursor.fetchall()
	tasks = []
	for x in myresult:
		print(x[3])
		mytask= {
			"task_id": x[0],
			"name": x[1],
			"date": x[2].strftime("%Y-%m-%d"),
			"time":str(x[3]),
			"cat_id": x[4],
			"description":x[5]
		}
		tasks.append(mytask)
	return dumps(tasks)

@app.route('/daytasks/show', methods=['GET'])
def daytasks_show():
	user_id=session['user_id']
	mycursor = mydb.cursor()
	val=(user_id,)
	mycursor.execute("SELECT * FROM daytask where user_id=%s",val)
	myresult = mycursor.fetchall()
	daytasks = []
	for x in myresult:
		print(x[3])
		mydaytask= {
			"daytask_id": x[0],
			"name": x[1],
			"date": x[2].strftime("%Y-%m-%d"),
			"done": x[3],
			"difficulty": x[4],
			"cat_id":x[5],
			"description":x[6]
		}
		daytasks.append(mydaytask)
	return dumps(daytasks)

@app.route('/register', methods=['POST'])
def register():
	username=request.json['username']
	password=request.json['password']
	safe_password, salt = hash_password(password)
	print(len(salt))
	mycursor = mydb.cursor()
	sql = "INSERT INTO user ( username, pass , salt  ) VALUES (%s, %s,%s)"
	val=(username,safe_password,salt)
	mycursor.execute(sql, val)
	mydb.commit()
	if mycursor.rowcount==1:
		return dumps({ "success":True})
	else:
		return dumps({ "success":False})

@app.route('/login', methods=['POST'])
def login():
	username=request.json['username']
	password=request.json['password']
	mycursor = mydb.cursor()
	val=(username,)	
	mycursor.execute("SELECT user_id,pass,salt FROM user where username=%s", val)
	myresult = mycursor.fetchall()

	if mycursor.rowcount==1:
		user_id=myresult[0][0]
		dbpassword=myresult[0][1]
		salt=myresult[0][2]
		print(password, dbpassword, salt)
		if(check_password(password, dbpassword, salt)):
			session['user_id'] = user_id
			session['username']= username
			return dumps({ "success":True})
		else:
			return dumps({ "success":False})		
	else:
		return dumps({ "success":False})

def hash_password(password):
	salt = uuid.uuid4().hex
	return hashlib.sha256(salt.encode() + password.encode()).hexdigest(), salt

def check_password(password, hashed_password, salt):
	return hashed_password == hashlib.sha256(salt.encode() + password.encode()).hexdigest()

@app.route('/checklogin', methods=['GET'])
def check_login():
	if 'user_id' in session:
		return dumps({ "success":True, "username": session['username']})
	else:
		return dumps({ "success":False})


@app.route('/logout', methods=['GET'])
def logout():
	session.clear()
	return dumps({"success":True})

@app.route('/tasks/bydate', methods=['GET'])
def tasks_bydate():
	user_id=session['user_id'] 
	date=request.json['date']
	mycursor = mydb.cursor()
	val=(date,user_id)	
	mycursor.execute("SELECT * from task where date=%s and user_id=%s", val)
	myresult = mycursor.fetchall()
	tasks = []
	for x in myresult:
		mytask= {
			"task_id": x[0],
			"name": x[1],
			"date": x[2].strftime("%Y-%m-%d"),
			"time":str(x[3]),
			"cat_id": x[4],
			"description":x[5]
		}
		tasks.append(mytask)
	return dumps(tasks)

@app.route('/daytasks/bydate', methods=['GET'])
def daytasks_bydate():
	user_id=session['user_id']
	print(user_id, "letssee")
	date=request.args['date']
	mycursor = mydb.cursor()
	val=(user_id,date)
	mycursor.execute("SELECT * FROM daytask where user_id=%s and date=%s",val)
	myresult = mycursor.fetchall()
	daytasks = []
	for x in myresult:
		print(x[3])
		mydaytask= {
			"daytask_id": x[0],
			"name": x[1],
			"date": x[2].strftime("%Y-%m-%d"),
			"done": x[3],
			"difficulty": x[4],
			"cat_id":x[5],
			"description":x[6]
		}
		daytasks.append(mydaytask)
	return dumps(daytasks)


@app.route('/daytask/complete', methods=['POST'])
def daytask_complete():
	user_id=session['user_id']
	#user_id=1
	daytask_id=request.json['daytask_id']
	mycursor = mydb.cursor()
	sql="UPDATE  daytask set done=1 WHERE daytask_id=%s and user_id=%s" 
	val=(daytask_id,user_id)
	mycursor.execute(sql, val)
	mydb.commit()
	print(mycursor.rowcount, "record inserted.")
	if mycursor.rowcount==1:
		return dumps({ "success":True})
	else:
		return dumps({ "success":False})








if __name__ == "__main__":
	app.secret_key = 'very_secret'
	app.run(host='192.168.1.2')