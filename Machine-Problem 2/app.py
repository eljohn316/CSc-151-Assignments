from flask import Flask, render_template, request, url_for, redirect, flash
from flaskext.mysql import MySQL 
from forms import SearchForm


app = Flask(__name__)


app.config['SECRET_KEY'] = 'secretkey'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'	
app.config['MYSQL_DATABASE_DB'] = 'mystudent'
	
mysql = MySQL(app)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/dashboard',methods=['POST','GET'])
def dashboard():
	if request.method == 'POST':
		idnumber = request.form['idnumber']
		lastname = request.form['lastname']
		firstname = request.form['firstname']
		course = request.form['course']
		year = request.form['year']
		gender = request.form['gender']
		conn = mysql.connect()
		cur = conn.cursor()		
		cur.execute("INSERT INTO student (idnumber,lastname,firstname,course,year,gender) VALUES (%s,%s,%s,%s,%s,%s)",(idnumber,lastname,firstname,course,year,gender))
		conn.commit()
		flash('Student added successfully! ')
		return redirect(url_for('dashboard'))
	else:
		conn = mysql.connect()
		cur = conn.cursor()
		cur.execute("SELECT * FROM student")
		students = cur.fetchall()
		return render_template('dashboard.html',students=students)

@app.route('/update', methods=['POST','GET'])
def update():
	if request.method == 'POST':
		id_data = request.form['idnumber']	
		lastname = request.form['lastname']
		firstname = request.form['firstname']
		course = request.form['course']
		year = request.form['year']
		gender = request.form['gender']
		conn = mysql.connect()
		cur = conn.cursor()
		cur.execute("""
		UPDATE student SET lastname=%s, firstname=%s, course=%s, year=%s, gender=%s
		WHERE idnumber = %s
		""", (lastname,firstname,course,year,gender,id_data))
		conn.commit()
		flash('Student updated successfully.')
		return redirect(url_for('dashboard'))

@app.route('/delete/<string:id_data>',methods=['GET'])
def delete(id_data):
		conn = mysql.connect()
		cur = conn.cursor()
		cur.execute("DELETE FROM student WHERE idnumber=%s",(id_data))
		conn.commit()
		return redirect(url_for('dashboard'))

@app.route('/search', methods=['POST','GET'])
def search():
	form = SearchForm()
	if request.method == 'POST' and form.validate_on_submit():
		student = request.form['student']
		conn = mysql.connect()
		cur = conn.cursor()
		sql = ''' SELECT * FROM student WHERE firstname LIKE "%'''+student+'''%" or lastname LIKE "%''' +student+'''%"'''
		cur.execute(sql)
		result = cur.fetchall()
		return render_template('search.html',form=form, result=result)		
	return render_template('search.html',form=form)

if __name__ == '__main__':
	app.run(debug=True)