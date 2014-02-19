"""[patient]
1. Patient Name (First and Last)
2. Patient Date of Birth
3. Patient Gender (M / F)
4. Patient MRN (usually 8-digit number) -- should be unique

[exam] (A patient may have multiple exams)
1. Exam Modality (CT, MR, XR, US) - XR = x-ray, US = ultrasound
2. Exam Date /Time
3. Exam Identifier (usually a 8-digit number) -- should be unique
4. Exam Finalized Report Date / Tim

Eventually, we may add for [exam]

Exam name (eg, CT abdomen)
Exam report (free text report of findings)


In addition to an application that's constantly running, 
it would also be nice if we can set parameters for 
your script to generate exams within a certain date interval, eg,

Generate 1000 exams between 2014-01-01 and 2014-01-31

CONSTRAINTS: - DOB < Exam DateTime < Exam Finalized DateTime
- Usually Exam Finalized DateTime is within 1-6 hours of Exam DateTime."""

from faker import Factory
import random
import sqlite3

# Initialize the database
conn = sqlite3.connect('TROVE.db')
c = conn.cursor()
c.execute('''CREATE TABLE Patients
             (Name text, DOB text, Gender text, MRN int)''')
c.execute('''CREATE TABLE Exams
             (Modality text, Exam time text, ID int, Report time text)''')

"""
def createData():
	faker = Factory.create()
	patientName = faker.first_name() + ' ' + faker.last_name()
	patientDOB = faker.date()
	genderInt = random.randint(1, 10)
	patientGender = 'M' if genderInt <= 5 else 'F'
	randMRN = str(random.randint(0, 99999999))
	MRN = randMRN.zfill(8)
	print 'Name: ' + patientName
	print 'DOB: ' + patientDOB
	print 'Gender: ' + patientGender
	print 'MRN: ' + MRN
	examMod = ''
	randExam = random.randint(1, 4)
	if randExam is 1:
		examMod = 'CT'
	elif randExam is 2:
		examMod = 'MR'
	elif randExam is 3:
		examMod = 'XR'
	else:
		examMod = 'US'
	examDateTime = str(faker.date_time())
	while int(examDateTime[:examDateTime.index('-')])<int(patientDOB[:patientDOB.index('-')]):
		examDateTime = str(faker.date_time())
	examID = str(random.randint(0,99999999)).zfill(8)
	examReportDateTime = str(faker.date_time())
	while int(examReportDateTime[:examReportDateTime.index('-')])<int(examDateTime[:examDateTime.index('-')]):
		examReportDateTime = str(faker.date_time())
	print 'Exam Modality: ' + examMod
	print 'Exam Date/Time: ' + examDateTime
	print 'Exam ID: ' + examID
	print 'Exam report: ' + examReportDateTime

createData() """


# Exam class
class Exam:
	def __init__(self, Patient, Resident, Attending):
		""" The exam class contains the variables for modality, date and time, ID, and report date and time. """
		faker = Factory.create()
		self.examMod = ''
		self.randExam = random.randint(1, 4)
		if self.randExam is 1:
			self.examMod = 'CT'
		elif self.randExam is 2:
			self.examMod = 'MR'
		elif self.randExam is 3:
			self.examMod = 'XR'
		else:
			self.examMod = 'US'

		self.examDateTime = str(faker.date_time())
		# need to check the DOB of the Patient so that the DOB < examDateTime
		while int(self.examDateTime[:self.examDateTime.index('-')])<int(Patient.DOB()[:Patient.DOB().index('-')]):
			self.examDateTime = str(faker.date_time())
		self.examID = str(random.randint(0,99999999)).zfill(8)
		self.randReport = random.randint(1, 6)
		self.examReportDateTimeNum = int(self.examDateTime[self.examDateTime.find(' ')+1:self.examDateTime.find(':')])+self.randReport
		self.examReportDateTime = self.examDateTime[:self.examDateTime.find(' ')+1] + str(self.examReportDateTimeNum) + self.examDateTime[self.examDateTime.find(':'):]
		self.examResident = Resident
		self.examAttending = Attending
		Patient.addExam(self)
		Resident.addExam(self)
		Attending.addExam(self)
		c = conn.cursor()
		c.execute("INSERT INTO Exams VALUES ('self.examMod', 'self.examdDateTime', 'self.examID', 'self.examReportDateTime')")
		conn.commit()
		
	def toString(self):
		return 'Exam Modality: '+self.examMod+'\nExam Date/Time: '+self.examDateTime+'\nExam ID: '+self.examID+'\nExam report: '+self.examReportDateTime

	def Modality(self):
		return self.examMod

	def examDate(self):
		return self.examDateTime

	def examReportDate(self):
		return self.examReportDateTime

class Patient():
	def __init__(self):
		faker = Factory.create()
		self.patientName = faker.first_name() + ' ' + faker.last_name()
		self.patientDOB = faker.date()
		self.genderInt = random.randint(1, 10)
		self.patientGender = 'M' if self.genderInt <= 5 else 'F'
		self.randMRN = str(random.randint(0, 99999999))
		self.MRN = self.randMRN.zfill(8)
		self.patientExams = []
		c = conn.cursor()
		c.execute("INSERT INTO Patients (Name, DOB, Gender, MRN) VALUES ('self.patientName', 'self.patientDOB', 'self.patientGender', 'self.MRN')")
		conn.commit()
		
	def toString(self):
		return 'Name: '+self.patientName+'\nDOB: '+self.patientDOB+'\nGender: '+self.patientGender+'\nMRN: '+self.MRN

	def Name(self):
		return self.patientName

	def DOB(self):
		return self.patientDOB

	def Gender(self):
		return self.patientGender

	def MRN(self):
		return self.MRN

	def addExam(self, exam):
		self.patientExams.append(exam)

class Resident:

	def __init__(self):
		self.Exams = []

	def addExam(self, exam):
		self.Exams.append(exam)

class Attending:

	def __init__(self):
		self.Exams = []

	def addExam(self, exam):
		self.Exams.append(exam)



for x in range(1, 10000):
	p = Patient()
	r = Resident()
	a = Attending()
	e = Exam(p, r, a)
	print e.toString()
