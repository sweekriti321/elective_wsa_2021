from flask import Flask,render_template,request,session,redirect,jsonify

#Sweekriti Parajuli
#171339 BECE(DAY)

from flask_mysqldb import MySQL

#for session
from flask_session import Session

app = Flask(__name__)

#database setting for mysql
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='dbase_trekapp'

mysql=MySQL(app)

# Session setting 
app.config["SESSION_PERMANENT"]=False
app.config["SESSION_TYPE"]="filesystem"
Session(app)

@app.route('/')
def home():
	
	loged_in_user=None
	userId=None # added by not watching class video 
	if session.get('email'):
		loged_in_user=session["email"]
	if session.get('userId'):
		userId=session['userId']
		#session.get('email')
	return render_template('index.html',result={'loged_in_user':loged_in_user,'userId':userId})


@app.route('/register')
def register():
	return render_template('register.html')
@app.route('/login')
def login():
	return render_template('login.html')


@app.route('/doLogin',methods=['post'])
def doLogin():

	email=request.form['email']
	password=request.form['psw']

	cursor =mysql.connection.cursor()
	resp=cursor.execute('''SELECT * FROM user WHERE email=%s and password=%s;''',(email,password))
	#resp=cursor.execute('''SELECT id,email,full_name,password FROM user WHERE email=%s and password=%s;''',(email,password))
	
	
	user=cursor.fetchone()
	cursor.close()
	if resp==1:
		session['email']=email  
		session['userId']= user[0]
		loged_in_user=session.get('email')
		return render_template('home.html',result={'loged_in_user':loged_in_user})# using dictionary > result={"email":email}  
		# and to get data in html >result.email
	else:
		return render_template('login.html',result="Invalid user")

@app.route('/doRegister',methods=['POST'])
def doRegister():
	full_name=request.form['full_name']
	email=request.form['email']
	phone_number=request.form['phone_number']
	address=request.form['address']
	password=request.form['psw']

	cursor =mysql.connection.cursor()
	cursor.execute('''INSERT INTO user VALUES(null,%s,%s,%s,%s,%s)''',(full_name,address,email,phone_number,password))
	mysql.connection.commit()
	cursor.close()
	return render_template('login.html',resutl="registerd sucessfully, please login to continue")
@app.route('/treaks')
def allTreaks():
	#return "i am aon treak listing page"
	#return render_template('listing.html')
	cursor=mysql.connection.cursor()
	cursor.execute('''SELECT td.id as 'SNO', td.title as 'Title',td.days as 'Days', td.difficulty as 'Difficulty', td.total_cost as 'Total Cost', td.upvotes as 'Upvotes', u.full_name as 'Full Name' FROM trek_destinations as td JOIN user as u ON td.user_id=u.id;''')
	treaks=cursor.fetchall()
	cursor.close()

	loged_in_user=None
	if session.get('email'):
		loged_in_user=session['email']

	return render_template('listing.html', result={"treaks":treaks,"loged_in_user":loged_in_user})


@app.route('/trek/<int:trekId>')
def getTrekbyId(trekId):
	#print(type(trekId))
	#return "this trek id is "+ str(trekId)
	cursor=mysql.connection.cursor()
	cursor.execute('''SELECT td.id as 'SNO', td.title as 'Title',td.days as 'Days', td.difficulty as 'Difficulty', td.total_cost as 'Total Cost', td.upvotes as 'Upvotes', u.full_name as 'Full Name' FROM trek_destinations as td JOIN user as u ON td.user_id=u.id where td.id=%s;''',(trekId,))
	treaks=cursor.fetchone()
	cursor.close()

	cursor=mysql.connection.cursor()
	cursor.execute('''SELECT * FROM `itenaries` WHERE `trek_destination_id`=%s;''',(trekId,))
	iternaries=cursor.fetchall()
	cursor.close()
	#print(iternaries)

	#return render_template('trekdetail.html', result=treaks)

	return render_template('trekdetail.html', result={"trek":treaks,"iternaries":iternaries})


@app.route('/logout')
def logout():
	session["email"]=None
	session["userId"]=None

	return redirect("/")

@app.route('/addtrek')
def addTrek():
	loged_in_user=None
	if session.get('email'):
		loged_in_user=session["email"]


	return render_template('addtrek.html',result={'loged_in_user':loged_in_user})


@app.route('/doAddTrek',methods=['post'])
def doAddTrek():
	loged_in_user=None
	if session.get('email'):
		loged_in_user=session["email"]

	title= request.form['title']
	days=request.form['days']
	difficulty=request.form['difficulty']
	total_cost=request.form['total_cost']
	upvotes=0

	cursor=mysql.connection.cursor()
	cursor.execute('''SELECT id FROM `user` where `email`=%s;''',(loged_in_user,))
	user=cursor.fetchone()
	#print(user,title, difficulty,total_cost)
	cursor.close()

	userId=user[0]

	cursor =mysql.connection.cursor()
	cursor.execute('''INSERT INTO trek_destinations VALUES(null,%s,%s,%s,%s,%s,%s)''',(title,days,difficulty,total_cost,upvotes,userId))
	mysql.connection.commit()
	cursor.close()

	return redirect('/treaks')


@app.route('/addItenary')
def addItenary():
	loged_in_user=None
	if session.get('email'):
		loged_in_user=session["email"]

	cursor=mysql.connection.cursor()
	userId=None
	if session.get('userId'):
		userId=session.get('userId')
	cursor.execute('''SELECT id, title FROM `trek_destinations` where user_id=%s;''',(userId,))
	treaks=cursor.fetchall()
	cursor.close()



	return render_template('additenary.html',result={"trek":treaks,"loged_in_user":loged_in_user})

@app.route('/doAddIternary',methods=['post'])
def doAddIternary():
	loged_in_user=None
	if session.get('email'):
		loged_in_user=session["email"]

	trek_destination_id	= request.form['trek_destination_id']
	print("trek destination id",trek_destination_id)

	day=request.form['day']
	print("day ",day)

	title= request.form['title']
	print("title ",title)

	startplace=request.form['startplace']
	print("startplace ",startplace)
	endplace=request.form['endplace']
	print("endplace ",endplace)
	description=request.form['description']
	print("description ",description)
	duration=request.form['duration']
	print("duration ",duration)
	cost=request.form['cost']
	print("cost ",cost)
	cursor =mysql.connection.cursor()
	cursor.execute('''INSERT INTO `itenaries` VALUES(null,%s,%s,%s,%s,%s,%s,%s,%s)''',(title,day,startplace,endplace,description,duration,cost,trek_destination_id))
	mysql.connection.commit()
	cursor.close()

	return redirect('/treaks')



@app.route('/iternary/<int:trekId>')
def getIternarybyTrekId(trekId):
	

	cursor=mysql.connection.cursor()
	cursor.execute('''SELECT * FROM `itenaries` WHERE `trek_destination_id`=%s;''',(trekId,))
	iternaries=cursor.fetchall()
	cursor.close()
	print("here is ////////",trekId)
	
	return render_template('iternary.html', result={"trekId":trekId,"iternaries":iternaries})


@app.route('/testAjax ')
def testAjax():
	return render_template('login.html')



def __getUserIdByEmail(email):
	# __ indicates private
	pass



app.run()



#
#
# 	install pip flask_mysqldb     http://127.0.0.1:5000/login


#  basic html home page for html	http://127.0.0.1:5000/


