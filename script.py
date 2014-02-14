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
Exam report (free text report of findings)"""

from faker import Factory
import random

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
	print examDateTime.index('-')
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

createData()