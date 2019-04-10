import sqlite3

dBaseFile = raw_input("Create file name: ") + '.db'

conn = sqlite3.connect(dBaseFile)
dBaseQuer = conn.cursor()

class Student(object):
	def __init__(self,idNumber,lastName,firstName,course,year,gender):
		self.idNumber = idNumber
		self.lastName = lastName
		self.firstName = firstName
		self.course = course
		self.year = year
		self.gender = gender

def createdBase():
	dBaseQuer.execute('''CREATE TABLE IF NOT EXISTS records(idNumber TEXT, lastName TEXT,firstName TEXT, course TEXT, year TEXT, gender TEXT )''')
	print("File is ready.\n")

def addStudent(st_info):
	dBaseQuer.execute('''INSERT into records(idNumber,lastName,firstName,course,year,gender)VALUES(?,?,?,?,?,?)''',(st_info.idNumber,st_info.lastName,st_info.firstName,st_info.course,st_info.year,st_info.gender))
	print("\tSuccessfully Added!")
	conn.commit()

def deleteStudent():
	deleteiD = raw_input("Enter the ID Number: ")
	dBaseQuer.execute("DELETE from records WHERE idNumber = ?",(deleteiD,))
	print("Student deleted.")
	conn.commit()

def updateStudent():
	updateiD = raw_input("Enter the ID Number: ")
	print("What do want to update? (Select a number.)")
	print("[1] Last Name")
	print("[2] First Name")
	print("[3] Course")
	print("[4] Year")
	print("[5] Gender")
	updateChoice = raw_input("Choice:  ")
	if updateChoice == '1':
		newlastName = raw_input("Enter New Last Name: ")
		conn.execute("UPDATE records set lastName = ? where idNumber =?",(newlastName,updateiD))
		print("Update Successful!")
		conn.commit()
	elif updateChoice == '2':	
		newfirstName = raw_input("Enter New First Name: ")
		conn.execute("UPDATE records set firstName = ? where idNumber = ?", (newfirstName,updateiD))
		print("Update Successful!")
		conn.commit()
	elif updateChoice == '3':
		newCourse = raw_input("Enter New Course: ")
		conn.execute("UPDATE records set course = ? where idNumber = ?", (newCourse,updateiD))
		print("Update Successful!")
		conn.commit()
	elif updateChoice == '4':
		newYear = raw_input("Update Year Level: ")
		conn.execute("UPDATE records set year = ? where idNumber =?",(newYear,updateiD))
		print("Update Successful!")
		conn.commit()
	elif updateChoice == '5':
		newGender = raw_input("Update Gender: ")
		conn.execute("UPDATE records set gender = ? where idNumber = ?",(newGender,updateiD))
		conn.commit()
	else:
		print("Choice not valid.\n")


def printStudent():
	dBaseQuer.execute("SELECT * FROM records")
	for row in dBaseQuer.fetchall():
		print " ",row[0]," ",row[1]," ",row[2]," ",row[3]," ",row[4]," ",row[5]


def main():
	createdBase()

	while(True):

		print("\n SELECT OPERATION")
		print("\n[1] SHOW DATABASE")
		print("\n[2] ADD STUDENT")
		print("\n[3] DELETE STUDENT")
		print("\n[4] UPDATE STUDENT")
		print("\n[5] EXIT")

		selectOperation = raw_input("\nSelect a number:")
		if selectOperation == '1':
			printStudent()
		elif selectOperation == '2':
			idNo = raw_input("Enter ID Number: ")
			lName = raw_input("Enter Last Name: ")
			fName = raw_input("Enter First Name: ")
			course = raw_input("Enter Course: ")
			year = raw_input("Enter Year Level: ")
			gender = raw_input("Enter Gender: ")
			st_info = Student(idNo,lName,fName,course,year,gender)
			addStudent(st_info)
		elif selectOperation == '3':
			deleteStudent()
		elif selectOperation == '4':
			updateStudent()
		elif selectOperation == '5':
			print("Program Closing..")
			quit(1)
		else :
			print("Choice Invalid!")

	dBaseQuer.close()
	conn.close()

if __name__ == '__main__':
	main()