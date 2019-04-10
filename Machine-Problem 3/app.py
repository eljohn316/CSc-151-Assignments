from flask import Flask, render_template, request, url_for, redirect, flash
from flaskext.mysql import MySQL 
from forms import SearchForm


app = Flask(__name__)


app.config['SECRET_KEY'] = 'secretkey'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'	
app.config['MYSQL_DATABASE_DB'] = 'dbase'
	
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
		courseid = request.form['courseid']
		year = request.form['year']
		gender = request.form['gender']
		conn = mysql.connect()
		cur = conn.cursor()		
		cur.execute("INSERT INTO student (idnumber,lastname,firstname,course,courseid,year,gender) VALUES (%s,%s,%s,%s,%s,%s,%s)",(idnumber,lastname,firstname,course,courseid,year,gender))
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
		courseid = request.form['courseid']
		year = request.form['year']
		gender = request.form['gender']
		conn = mysql.connect()
		cur = conn.cursor()
		cur.execute("""
		UPDATE student SET lastname=%s, firstname=%s, course=%s, courseid=%s, year=%s, gender=%s
		WHERE idnumber = %s
		""", (lastname,firstname,course,courseid,year,gender,id_data))
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

@app.route('/course', methods=['POST','GET'])
def course():
	if request.method == 'POST':
		courseid = request.form['courseid']
		coursename = request.form['coursename']
		conn = mysql.connect()
		cur = conn.cursor()
		cur.execute("INSERT INTO courses(courseid,coursename) VALUES (%s,%s)",(courseid,coursename))
		conn.commit()
		flash('Course added successfully!')
		return redirect(url_for('course'))
	else:
		conn = mysql.connect()
		cur = conn.cursor()
		cur.execute("SELECT * FROM courses")
		data = cur.fetchall()
		return render_template('course.html', data=data)

@app.route('/update_course', methods=['POST','GET'])
def update_course():
	if request.method == 'POST':
		course_id = request.form['courseid']
		coursename = request.form['coursename']
		conn = mysql.connect()
		cur = conn.cursor()
		cur.execute("UPDATE courses SET coursename = %s WHERE courseid = %s",(coursename, course_id))
		conn.commit()
		flash('Course updated successfully!')
		return redirect(url_for('course'))

@app.route('/delete_course/<int:course_id>', methods=['GET'])
def delete_course(course_id):
	conn = mysql.connect()
	cur = conn.cursor()
	cur.execute("DELETE FROM courses WHERE courseid=%s",(course_id))
	conn.commit()
	return redirect(url_for('course'))

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

@app.route('/all', methods=['POST','GET'])
def all():
	conn = mysql.connect()
	cur = conn.cursor()
	sql ='''SELECT student.idnumber, student.lastname, student.firstname, student.year, student.gender, courses.coursename
			FROM student, courses
			WHERE student.courseid = courses.courseid
			ORDER BY student.idnumber
		 '''
	cur.execute(sql)
	result = cur.fetchall() 
	return render_template('all.html',result=result)


if __name__ == '__main__':
	app.run(debug=True)