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
- Usually Exam Finalized DateTime is within 1-6 hours of Exam DateTime.

HOW TO RUN: type 'python fake_data_generator.py [number of exams] [begin date] [end date]
All dates should be in the format of yyyy-mm-dd.
Example: python fake_data_generator.py 1000 2012-01-02 2013-11-24"""

from faker import Factory
import random
import sqlite3
import sys

# Initialize the database
conn = sqlite3.connect('TROVE.db')
c = conn.cursor()
c.execute('''CREATE TABLE Patients
             (Name text, DOB text, Gender text, MRN int)''')
c.execute('''CREATE TABLE Exams
             (Modality text, Exam time text, ID int, Report time text)''')
examID_List = []
MRN_List = []
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
	def __init__(self, patient, resident, attending, begin_date, end_date):
		""" The exam class contains the variables for modality, date and time, ID, and report date and time. 
		An exam is designated to a single Patient, along with a single Resident and a single Attending. These 
		should be provided before an Exam object is made. """
		faker = Factory.create()

		try:
			assert patient != None and resident != None and attending != None
			# assert type(patient) == Patient and type(resident) == Resident and type(attending) == Attending
			# Make a random exam modality
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
			
			# Make a random exam date and time
			# Precondition: both begin_date and end_date should be in the format of yyyy-mm-dd
			begin_Y_M_D = begin_date.split('-') # split the date so that it's [yyyy, mm, dd]
			end_Y_M_D = end_date.split('-')
			exam_year = str(random.randint(int(begin_Y_M_D[0]), int(end_Y_M_D[0])))
			# For the date, if the begin and end have the same years then make the months in between; else just random from 1~12
			exam_month = random.randint(int(begin_Y_M_D[1]), int(end_Y_M_D[1])) if int(begin_Y_M_D[0]) == int(end_Y_M_D[0]) else random.randint(1,12)
			exam_month = str(exam_month).zfill(2) # make it so that all months will be two numbers, ex.: 01, 03, 08, 10, 12
			# Same logic for the day
			exam_day = ''
			if (int(begin_Y_M_D[0]) is int(end_Y_M_D[0]) and int(begin_Y_M_D[1]) is int(end_Y_M_D[1])):
				exam_day = str(random.randint(int(begin_Y_M_D[2]), int(end_Y_M_D[2]))).zfill(2)
			else:
				# need to consider the difference in days in different months, but we'll leave it for now.
				exam_day = str(random.randint(1,31)).zfill(2)
			self.examDateTime = exam_year + "-" + exam_month + "-" + exam_day + " " + faker.time()

			"""
			# need to check the DOB of the Patient so that the DOB < examDateTime
			while int(self.examDateTime[:self.examDateTime.index('-')])<int(patient.DOB()[:patient.DOB().index('-')]):
				self.examDateTime = str(faker.date_time()) """

			# Make a random examID - should be unique.
			self.examID = str(random.randint(0,99999999)).zfill(8)
			# Check if the examID already exists.
			if self.examID in examID_List:
				self.examID = str(random.randint(0,99999999)).zfill(8)
			else:
				examID_List.append(self.examID)
			
			# Make a random exam report date and time.
			self.randReport = random.randint(1, 6)
			self.examReportDateTimeNum = int(self.examDateTime[self.examDateTime.find(' ')+1:self.examDateTime.find(':')])+self.randReport
			self.examReportDateTime = self.examDateTime[:self.examDateTime.find(' ')+1] + str(self.examReportDateTimeNum) + self.examDateTime[self.examDateTime.find(':'):]
			
			# Add the Resident and Attending and vice versa.
			self.examResident = resident
			self.examAttending = attending
			self.examPatient = patient
			patient.addExam(self)
			resident.addExam(self)
			attending.addExam(self)
			c = conn.cursor()
			c.executescript("""INSERT INTO Exams VALUES ('self.examMod', 'self.examdDateTime', 'self.examID', 'self.examReportDateTime');""")
			conn.commit()

		except:
			print "Invalid error: Please check your inputs and try again."
		
	def toString(self):
		return 'Exam Modality: '+self.examMod+\
		'\nExam Date/Time: '+self.examDateTime+\
		'\nExam ID: '+self.examID+\
		'\nExam report: '+self.examReportDateTime+\
		'\nExam Patient: '+self.examPatient.toString()+\
		'\nExam Resident: '+self.examResident.toString()+\
		'\nExam Attending: '+self.examAttending.toString()

	def Modality(self):
		return self.examMod

	def examDate(self):
		return self.examDateTime

	def examReportDate(self):
		return self.examReportDateTime

class Patient():
	""" Class for the Patient object. A Patient object has a name that is randomly made, separated by a space. The DOB is also 
	randomly generated, along with the gender. MRN is a unique number for the patient. """
	def __init__(self, begin_date):
		faker = Factory.create()
		self.patientName = faker.first_name() + ' ' + faker.last_name()
		# Make sure all DOBs are earlier than the first possible exam date.
		self.patientDOB = faker.date()
		while self.patientDOB[:self.patientDOB.find('-')] >= begin_date:
			self.patientDOB = faker.date()
		self.genderInt = random.randint(1, 2)
		self.patientGender = 'M' if self.genderInt == 1 else 'F'
		# Check if the MRN already exists
		self.MRN = str(random.randint(0, 99999999)).zfill(8)
		if self.MRN in MRN_List:
			self.MRN = str(random.randint(0, 99999999)).zfill(8)
		else:
			MRN_List.append(self.MRN)
		self.patientExams = []
		c = conn.cursor()
		c.execute("""INSERT INTO Patients (Name, DOB, Gender, MRN) VALUES ('self.patientName', 'self.patientDOB', 'self.patientGender', 'self.MRN');""")
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
		faker = Factory.create()
		self.residentName = faker.first_name() + ' ' + faker.last_name()
		self.Exams = []

	def addExam(self, exam):
		self.Exams.append(exam)

	def toString(self):
		return 'Resident name: ' + self.residentName

class Attending:

	def __init__(self):
		faker = Factory.create()
		self.attendingName = faker.first_name() + ' ' + faker.last_name()
		self.Exams = []

	def addExam(self, exam):
		self.Exams.append(exam)

	def toString(self):
		return 'Attending name: ' + self.attendingName

def checkDate(d):
	d_list = d.split('-')
	int(d_list[0])
	int(d_list[1])
	int(d_list[2])
	if len(d_list) == 3 and len(d_list[0]) == 4 and len(d_list[1]) == 2 and len(d_list[2]) == 2:
		pass
	else:
		raise ValueError

def run(examNum, begin_date, end_date):
	# must be in yyyy-mm-dd
	try:
		checkDate(begin_date)
		checkDate(end_date)
		for x in range(1, int(examNum)):
			p = Patient(begin_date)
			r = Resident()
			a = Attending()
			e = Exam(p, r, a, begin_date, end_date)
			print "===================================="
			print e.toString()
	except ValueError:
		"Invalid date input."


if __name__ == "__main__":
	ex = sys.argv[1]
	bd = sys.argv[2]
	ed = sys.argv[3]
	run(ex, bd, ed)