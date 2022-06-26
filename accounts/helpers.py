from django.contrib.auth.models import User
from .models import *
from emailsender.models import *

from io import StringIO, BytesIO

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader

### Reportlab functions

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors

from bidi.algorithm import get_display

import re

PAGE_HEIGHT=defaultPageSize[1]
PAGE_WIDTH=defaultPageSize[0]

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
styles.add(ParagraphStyle(name='Left', alignment=TA_LEFT))
styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT))

Title = "Hello world"
pageinfo = "platypus example"

pdfmetrics.registerFont(TTFont('Dosis', 'static/fonts/Dosis-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Amiri', 'static/fonts/Amiri-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Dosis-Bold', 'static/fonts/Dosis-Bold.ttf'))

TEXT_RE = re.compile(r'^[a-zA-Z0-9 ]+$')
def valid_text(text):
    return TEXT_RE.match(text)

def get_batch(batch):
    if batch[:2] == 'PR':
        stu_class = 'Preparatory ' + batch[2]
    elif batch[0] == 'P':
        stu_class = 'Primary ' + batch[1]
    else:
        stu_class = 'Intermediate ' + batch[1]
    return stu_class

def myFirstPage(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Bold',16)
    canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-108, Title)
    canvas.setFont('Times-Roman',9)
    canvas.drawString(inch, 0.75 * inch,"First Page / %s" % pageinfo)
    canvas.restoreState()
    
def myLaterPages(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 9)
    canvas.drawString(inch, 0.75 * inch,"Page %d %s" % (doc.page, pageinfo))
    canvas.restoreState()

def make_pdf(admitnumber):
    import arabic_reshaper

    profile = Orphan.objects.get(admitnumber = admitnumber)
    profile_number = int(admitnumber[3:])
    display_pic_url = 'http://newdaralzahra.appspot.com/profiles/%s.JPG' %profile_number

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)
    # doc = SimpleDocTemplate(self.response.out)

    Story = []
    normal_style = styles["Normal"]
    normal_style.leading = 17
    normal_style.fontSize = 15
    normal_style.fontName = 'Dosis'

    heading_style = styles["Center"]
    heading_style.leading = 17
    heading_style.fontSize = 17
    heading_style.fontName = 'Dosis-Bold'

    right_style = styles["Right"]
    right_style.leading = 17
    right_style.fontSize = 15
    right_style.fontName = 'Dosis'

    arabic_style = styles["Right"]
    arabic_style.leading = 17
    arabic_style.fontSize = 15
    arabic_style.fontName = 'Amiri'


    # Prepare the PDF content
    logo = Image('http://newdaralzahra.appspot.com/images/logo.png', width=109.0875, height=100)
    Story.append(logo)
        
    logo_name = Image('http://newdaralzahra.appspot.com/images/nameengarbgreen.png', width=225, height=30)
    Story.append(logo_name)

    Story.append(Spacer(1, 30))

    display_pic = Image(display_pic_url, width=90, height=90)
    table1_data = [
        [display_pic, Paragraph(profile.name, heading_style)]
    ]
    table1 = Table(table1_data, style = [('ALIGN',(0, 0),(-1, -1),'CENTER')])
    table1.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    Story.append(table1)

    Story.append(Spacer(3, 12))
        
    if not valid_text(profile.mother_name):
        profile.mother_name = get_display(arabic_reshaper.reshape(profile.mother_name))

    if not valid_text(profile.father_name):
        profile.father_name = get_display(arabic_reshaper.reshape(profile.father_name))

    if not valid_text(profile.address):
        profile.address = get_display(arabic_reshaper.reshape(profile.address))

    profile.batch = get_batch(profile.batch)

    table2_data = [
        [Paragraph('Admission Date', right_style), Paragraph(str(profile.admitdate), normal_style)],
        [Paragraph('Class', right_style), Paragraph(profile.batch, normal_style)],
        [Paragraph('Birth Date', right_style), Paragraph(str(profile.birthdate), normal_style)],
        [Paragraph('Gender', right_style), Paragraph(profile.gender, normal_style)],
        [Paragraph('Nationality', right_style), Paragraph(profile.nationality, normal_style)],
        [Paragraph('Category', right_style), Paragraph(profile.category, normal_style)],
        [Paragraph('Descent', right_style), Paragraph(profile.descent, normal_style)],
        [Paragraph('Address', right_style), Paragraph(profile.address, arabic_style)],
        [Paragraph("Mother's Name", right_style), Paragraph(profile.mother_name, arabic_style)],
        [Paragraph("Father's Name", right_style), Paragraph(profile.father_name, arabic_style)]
    ]
    table2 = Table(table2_data)
    table2.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('BACKGROUND', (0,0), (1,0), colors.palegreen),
        ('BACKGROUND', (0,2), (1,2), colors.palegreen),
        ('BACKGROUND', (0,4), (1,4), colors.palegreen),
        ('BACKGROUND', (0,6), (1,6), colors.palegreen),
        ('BACKGROUND', (0,8), (1,8), colors.palegreen),
    ]))
    Story.append(table2)
        
    doc.build(Story)

    pdf = buffer.getvalue()
    buffer.close()

    return pdf

# CSV import functions

def process_sponsor_csv(file_data):
	users_to_create = []
	usersinfo = {}
	check = []
	for n in range(0, len(file_data)-1):
		row = file_data[n].split(',')
		row[2] = True if row[2] == 'TRUE' else False
		if not User.objects.filter(username = row[0]) and row[0] not in check:
			user = User(username = row[0], first_name = row[1], is_staff = row[2])
			user.set_password(row[0]+'123')
			users_to_create.append(user)
			check.append(row[0])

			usersinfo[user.username] = row[3]
	
	User.objects.bulk_create(users_to_create)

	usersinfo_to_create = []
	for item in usersinfo:
		user = User.objects.get(username = item)
		user_info = UserInfo(user = user, email_to = usersinfo[item])
		usersinfo_to_create.append(user_info)
	UserInfo.objects.bulk_create(usersinfo_to_create)

def process_orphan_csv(file_data):
	to_create = []
	check = []
	for n in range(0, len(file_data)-1):
		row = file_data[n].split(',')
		row[1] = True if row[1] == 'TRUE' else False
		if not Orphan.objects.filter(admitnumber = row[0]) and row[0] not in check:
			sponsor = User.objects.get(username = row[13]) if User.objects.filter(username = row[13]) else None
			orphans = Orphan(admitnumber = row[0], active = row[1], name = row[2], admitdate = row[3], batch = row[4], birthdate = row[5], gender = row[6], nationality = row[7], category = row[8], descent = row[9], address = row[10], mother_name = row[11], father_name = row[12], sponsor = sponsor)
			to_create.append(orphans)
			check.append(row[0])
	
	Orphan.objects.bulk_create(to_create)

def process_info_csv(file_data):
	to_create = []
	check = []
	for n in range(0, len(file_data)-1):
		row = file_data[n].split(',')
		orphan = Orphan.objects.get(admitnumber = row[0]) if Orphan.objects.filter(admitnumber = row[0]) else False
		if orphan and row[0] not in check:
			row[1] = None if row[1] == 'none' else row[1]
			row[4] = None if row[4] == 0 else row[4]
			row[5] = None if row[5] == 'none' else row[5]
			row[7] = None if row[7] == 'none' else row[7]

			info = Information(orphan = orphan, notes = row[1], attendance = row[2], school_days = row[3], result = row[4], result_of = row[5], doc_visits = row[6], doc_visits_detail = row[7], sponsorship = row[8])
			to_create.append(info)
			check.append(row[0])
	
	Information.objects.bulk_create(to_create)

def handle_uploaded_file(f):
    with open('/tmp/newsletter.pdf', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
