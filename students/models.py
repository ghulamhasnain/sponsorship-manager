from django.db import models

# Create your models here.
class Agent(models.Model):
	name = models.CharField(max_length=50)
	email = models.CharField(max_length=50)
	phone = models.CharField(max_length=50)

	def __str__(self):
		return self.name

class Sponsor(models.Model):
	name = models.CharField(max_length=50)
	email = models.CharField(max_length=50)
	phone = models.CharField(max_length=50)
	agent = models.ForeignKey(Agent, on_delete=models.PROTECT, related_name='sponsor_agent', null=True, blank=True)

	def __str__(self):
		return self.name

class Student(models.Model):
	admitnumber = models.CharField(max_length=10, unique=True)
	active = models.BooleanField()
	name = models.CharField(max_length=50)
	admitdate = models.DateField()
	batch = models.CharField(max_length=12)
	birthdate = models.DateField()
	birth_place = models.CharField(max_length=50, default='')
	gender = models.CharField(max_length=10, choices=[('male','Male'), ('female', 'Female')])
	religion = models.CharField(max_length=50, default='')
	nationality = models.CharField(max_length=30)
	category = models.CharField(max_length=30, choices=[('orphan','Orphan'), ('non_orphan', 'Non Orphan'), ('special_non_orphan', 'Special Non Orphan')])
	descent = models.CharField(max_length=30, choices=[('syed', 'Syed'), ('non_syed', 'Non Syed')])
	address = models.CharField(max_length=200)
	city = models.CharField(max_length=50, default='')
	country = models.CharField(max_length=50, default='')
	mother_tongue = models.CharField(max_length=50, default='')
	mother_name = models.CharField(max_length=50)
	mother_occupation = models.CharField(max_length=50)
	father_name = models.CharField(max_length=50)
	father_occupation = models.CharField(max_length=50)
	medical_condition = models.CharField(max_length=200, default='')
	sponsor = models.ForeignKey(Sponsor, on_delete=models.PROTECT, related_name='orphan_sponsor', null=True, blank=True)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.admitnumber

class Medical(models.Model):
	date = models.DateField()
	description = models.CharField(max_length=200)
	student = models.ForeignKey(Student, on_delete=models.PROTECT, related_name='medical_student', null=True, blank=True)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.student)