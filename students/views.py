from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from .models import *
from .helpers import *

# Create your views here.
class ViewStudent(View):
	def get(self, request, admitnumber):
		
		student = Student.objects.get(admitnumber = admitnumber) if Student.objects.filter(admitnumber = admitnumber) else False

		if student:
			pic = str(int(admitnumber[3:])) + ".JPG"
			return render(request, 'profile.html', {'student': student, 'pic': pic})
		
		else:
			return HttpResponse('student not found')

class Upload(View):
	def get(self, request):
		return render(request, 'upload2.html')

	def post(self, request):
		file = request.FILES["file"]
		data_type = request.POST.get('info_type')

		if not file.name.endswith('.csv'):
			return HttpResponse('The file you uploaded is not a CSV file')
		else:
			file_data = file.read().decode("utf-8")
			file_data = file_data.split("\n")

			if data_type == 'sponsors':
				upload = process_sponsors_csv(file_data)

			elif data_type == 'students':
				upload = process_students_csv(file_data)

			elif data_type == 'agents':
				upload = process_agents_csv(file_data)
				
			return HttpResponse(upload)

class UpdateStudents(View):
	def post(self, request):
		file = request.FILES["file"]
		data_type = request.POST.get('info_type')

		if not file.name.endswith('.csv'):
			return HttpResponse('The file you uploaded is not a CSV file')
		else:
			file_data = file.read().decode("utf-8")
			file_data = file_data.split("\n")

			update = update_students_csv(file_data)
	
			return HttpResponse(update)

class AllStudents(View):
	def get(self, request):
		students = Student.objects.order_by('admitnumber').all()
		return render(request, 'students.html', {'students': students})

class BatchStudents(View):
	def get(self, request):
		batches = Student.objects.filter(active = True).order_by('batch').values('batch').distinct()
		# return render(request, 'batch_students.html')
		return HttpResponse(batches)

class AllMedical(View):
	def get(self, request):
		med_records = Medical.objects.order_by('-created')[:50]
		return render(request, 'med_records.html', {'med_records': med_records})