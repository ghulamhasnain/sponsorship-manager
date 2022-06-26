from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import Count
from django.core.mail import EmailMessage

from .models import *
from .forms import *
from .helpers import *

import csv
import os

class Sponsors(View):
	def get(self, request):
		users = User.objects.filter(is_staff = False).annotate(sponsored = Count('orphan_sponsor')).order_by('user_info__email_to')
		campaigns = Campaign.objects.all()
		form = UserForm(prefix = 'f1')
		form2 = UserInfoForm(prefix = 'f2')
		campaign_form = EmailForm()
		return render(request, 'sponsors.html', {'sponsors': users, 'form': form, 'form2': form2, 'campaigns': campaigns, 'campaign_form': campaign_form})

	def post(self, request):
		form = UserForm(request.POST, prefix = 'f1')
		form2 = UserInfoForm(request.POST, prefix = 'f2')
		if form.is_valid() and form2.is_valid():
			username = form.cleaned_data['username']
			first_name = form.cleaned_data['first_name']
			is_staff = form.cleaned_data['is_staff']
			password = username+'123'

			user = User.objects.create_user(username, password)
			user.first_name = first_name
			user.is_staff = is_staff
			user.save()

			user_info = UserInfo.objects.create(user = user)
			user_info.email_to = form2.cleaned_data['email_to']
			user_info.save()

			return redirect("sponsors")
		else:
			users = User.objects.filter(is_staff = False).annotate(sponsored = Count('orphan_sponsor'))
			return render(request, 'sponsors.html', {'sponsors': users, 'form': form, 'form2': form2, 'error': 'Incorrct info'})

class EditSponsor(View):
	def get(self, request, username):
		user = User.objects.get(username=username)
		user_info = UserInfo.objects.get(user = user) if UserInfo.objects.filter(user = user) else False
		form = EditUserForm(instance = user)
		form2 = UserInfoForm(instance = user_info) if user_info else UserInfoForm()

		return render(request, 'includes/form.html', {'form': form, 'form2': form2})

	def post(self,request, username):
		user = User.objects.get(username = username)
		user_info = UserInfo.objects.get(user = user) if UserInfo.objects.filter(user = user) else UserInfo.objects.create(user = user)

		form = EditUserForm(request.POST, instance = user)
		form2 = UserInfoForm(request.POST, instance = user_info)
		if form.is_valid() and form2.is_valid():
			user.first_name = form.cleaned_data['first_name']
			user.is_staff = form.cleaned_data['is_staff']
			user.save()

			user_info.email_to = form2.cleaned_data['email_to']
			user_info.save()
			return redirect('sponsors')
		else:
			return HttpResponse('Incorrct info')

class DeleteAllSponsors(View):
	def post(self, request):
		users = User.objects.filter(is_staff = False).all()
		for i in range(0, len(users)):
			user_info = UserInfo.objects.get(user=users[i]) if UserInfo.objects.filter(user=users[i]) else False
			if user_info:
				user_info.delete()
		users.delete()
		return HttpResponse('done')

class ContentEmailSponsor(View):
	def post(self, request):
		campaign_post = request.POST['campaign']
		sponsor_post = request.POST['sponsor']

		campaign = Campaign.objects.get(name = campaign_post) if Campaign.objects.filter(name = campaign_post) else False
		sponsor = User.objects.get(username = sponsor_post) if User.objects.filter(username = sponsor_post) else False

		attachments = 'false'

		if campaign and sponsor:
			subject = str(campaign.subject)
			body = str(campaign.body)
			user_info = UserInfo.objects.filter(user = sponsor).get()
			email_to = user_info.email_to.replace('/', ',')

			information = Information.objects.filter(orphan__sponsor = sponsor).all()

			students = []
			for i in information:
				batch = i.orphan.batch
				batch = batch.split(' - ')[0]

				if "PR" in batch:
					batchType = 'Preparatory'
					batchLevel = batch[2]
				elif "P" in batch:
					batchType = 'Primary'
					batchLevel = batch[1]
				elif 'I' in batch:
					batchType = 'Intermediate'
					batchLevel = batch[1]

				if 'B' in batch:
					batchGen = 'Boys'
				elif 'G' in batch:
					batchGen = 'Girls'

				# batchType = 'Primary'
				# batchGen = 'Boys'
				# batchLevel = '1'

				# if len(batch) == 4 :
				# 	batchType = "Preparatory"
				# 	batchLevel = batch[2]
				# 	if batch[3] == 'G':
				# 		batchGen = 'Girls'
				# else:
				# 	batchLevel = batch[1]
				# 	if batch[0] == 'I':
				# 		batchType = "Intermediate"
				# 		if batch[2] == 'G':
				# 			batchGen = 'Girls'

				batch = batchType + ' ' + batchLevel + ' ' + batchGen
				
				students.append([i.orphan.name, i.orphan.admitnumber, i.notes, i.attendance, i.school_days, i.doc_visits, i.doc_visits_detail, i.sponsorship, i.result, i.result_of, batch])

			body = body.replace('<sponsor_name>', sponsor.first_name)
			body = body.replace('<sponsor_email>', sponsor.username)

			if len(students) == 0:
				title = ''
				body = 'No students assigned to this sponsor'
				email_to = ''

			else:
				body = body.replace('<students>', str(students[0][0])) if len(students) == 1 else body.replace('<students>', str(len(students)) + ' students')
				body = body.replace('<student/s>', 'student') if len(students) == 1 else body.replace('<student/s>', 'students')

				student_info = ''

				if '<students_info>' in body:
					for s in students:
						location = body.find('<students_info>')
						heading = '{} ( {} ): \n'.format(s[0], s[1])
						batch = ' - Class: {}\n'.format(s[10])
						attendance = ' - Attendance: {}% ({} days present out of {}) \n'.format(int(s[3]*100/s[4]), s[3], s[4]) if s[4] != 0 else ' - Attendance: There were no regular school days during the month. \n'
						result = ' - Result: No exams during the month \n' if s[8] == 0 else ' - Result: {}% in {} \n'.format(s[8], s[9])
						
						doc_visits = ' - Doctor visits: 0 \n' if s[5] == 0 else ' - Doctor visits: {} ( {} ) \n'.format(s[5], s[6])
						notes = '' if s[2] == None else ' - Note: {} \n'.format(s[2])
						if s[7][0] == '$':
							sponsorship = ' - Sponsorship: <span style="color: red"> {} </span>'.format(s[7])
						else:
							sponsorship = ' - Sponsorship: <span style="color: green"> {} </span>'.format(s[7])

						student_info += heading + batch + attendance + result + doc_visits + notes + sponsorship + '\n\n'

					body = body[:location] + student_info + body[location:]
					body = body.replace('\n\n<students_info>', '')

				if len(students) < 6:
					attachments = 'true'

			return HttpResponse(subject + ';' + body + ';' + email_to + ';' + sponsor.username + ';' + attachments)
		else:
			return HttpResponse('None')

class EmailSponsor(View):
	def post(self, request):
		form = EmailForm(request.POST)
		
		if form.is_valid():
			campaign = form.cleaned_data['campaign']
			sponsor = form.cleaned_data['sponsor']
			email_to = form.cleaned_data['email_to'].split(',')
			subject = form.cleaned_data['subject']
			body = form.cleaned_data['body']
			attachment = request.POST.get('attachment', '')
			newsletter = request.POST.get('newsletter', '')
			picture = request.POST.get('picture', '')

			print(attachment)
			print(newsletter)
			print(picture)
			### preparing the HTML
			body_html = body.replace('\n', '<br>') # create the breaking points

			# find the point where student information starts
			if 'update' in subject.lower():
				location = body_html.find('( STU')
				start = 0
				for i in range(0, body_html[0:location].count('<br>')):
					start = body_html.find('<br>', start+1)

				# find the point where student information ends
				end = 0
				for i in range(0, body_html.count('Sponsorship:')):
					end = body_html.find('Sponsorship:', end+1)
				end = body_html.find('<br>', end)

				# Bold the student information part
				body_html = body_html[0:start] + '<b>' + body_html[start:end] + '</b>' + body_html[end:]

			profiles = Orphan.objects.filter(sponsor = User.objects.get(username = sponsor)).all()
			to_attach = []

			# if len(profiles) < 6:
			if attachment == '1':
				for p in profiles:
					pdf = make_pdf(p.admitnumber)
					attachment = (p.admitnumber+'.pdf', pdf, 'application/pdf')
					to_attach.append(attachment)

			if newsletter == '1':
				filename = 'newsletter.pdf'

				try:
					nl_file = open(os.path.join('/tmp/', filename))
				except:
					nl_file = False

				if not nl_file:
					return HttpResponse('Newsletter not found')
			else:
				nl_file = False

			if picture == '1':
				picfilename = 'picture.jpeg'

				try:
					pic_file = open(os.path.join('/tmp/', picfilename))
				except:
					pic_file = False

				if not pic_file:
					return HttpResponse('Picture not found')
			else:
				pic_file = False

			# attach the pdf to email
			email = EmailMessage()
			if to_attach != []:
				email.attachments = to_attach
			
			if nl_file:
				email.attach_file('/tmp/'+filename)

			if pic_file:
				email.attach_file('/tmp/'+picfilename)
			
			email.from_email = 'Dar al Zahra Sponsorship <sponsor@dar-al-zahra.org>'
			email.subject = subject
			# email.to = ['ghulamhasnain@gmail.com']
			email.to = email_to
			email.bcc = ['info@dar-al-zahra.org']
			email.content_subtype = 'html'
			email.body = body_html
			email.send()
			return HttpResponse('ok')

		else:
			return HttpResponse('error')

class Upload(View):
	def get(self, request):
		return render(request, 'upload.html')

	def post(self, request):
		file = request.FILES["file"]
		data_type = request.POST.get('info_type')

		if not file.name.endswith('.csv'):
			return HttpResponse('The file you uploaded is not a CSV file')
		else:
			file_data = file.read().decode("utf-8")
			file_data = file_data.split("\n")

			if data_type == 'sponsors':
				process_sponsor_csv(file_data)

			elif data_type == 'orphans':
				process_orphan_csv(file_data)

			elif data_type == 'information':
				process_info_csv(file_data)
				
			return redirect(data_type)

class Test(View):
	def get(self, request):
		html = '''
			<form action="http://www.dar-al-zahra.org/agent_view_profiles_json" method="post">
				<input name="agent" type="text" value="mohd.nanji@gmail.com">
				<input name="key" type="text" value="nfv8df98vujmr83jco94tue587ty34wo8rihcn4e5tmi45eyrthowiljf163">
				<input type="submit">
			</form>
		'''
		return HttpResponse(html)