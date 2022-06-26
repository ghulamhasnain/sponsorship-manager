from .models import *

## New students, sponsors, agents helpers

def process_agents_csv(file_data):
    to_create = []
    check = []
    for n in range(0, len(file_data)):
        row = file_data[n].split(',')
        agent = Agent.objects.get(email = row[1]) if Agent.objects.filter(email = row[1]) else False
        if not agent and row[1] not in check:
            entry = Agent(name = row[0], email = row[1], phone = row[2])
            to_create.append(entry)
            check.append(row[1])
        # to_create.append(agent)
    
    Agent.objects.bulk_create(to_create)
    return(to_create)

def process_sponsors_csv(file_data):
    to_create = []
    check = []
    for n in range(0, len(file_data)):
        row = file_data[n].split(',')
        sponsor = Sponsor.objects.get(email = row[1]) if Sponsor.objects.filter(email = row[1]) else False
        if not sponsor and row[1] not in check:
            agent = Agent.objects.get(email = row[3].strip()) if Agent.objects.filter(email = row[3].strip()) else None
            entry = Sponsor(name = row[0], email = row[1], phone = row[2], agent = agent)
            to_create.append(entry)
            check.append(row[1])
            # to_create.append(row[3].strip())
    
    Sponsor.objects.bulk_create(to_create)
    return(to_create)

def process_students_csv(file_data):
    to_create = []
    check = []
    for n in range(0, len(file_data)):
        row = file_data[n].split(',')
        student = Student.objects.get(admitnumber = row[0]) if Student.objects.filter(admitnumber = row[0]) else False
        if not student and row[0] not in check:
            sponsor = Sponsor.objects.get(email = row[21].strip()) if Sponsor.objects.filter(email = row[21].strip()) else None
            entry = Student(
                admitnumber = row[0],
                active = row[1],
                name = row[2],
                admitdate = row[3],
                batch = row[4],
                birthdate = row[5],
                birth_place = row[6],
                gender = row[7],
                religion = row[8],
                nationality = row[9],
                category = row[10],
                descent = row[11],
                address = row[12],
                city = row[13],
                country = row[14],
                mother_tongue = row[15],
                mother_name = row[16],
                mother_occupation = row[17],
                father_name = row[18],
                father_occupation = row[19],
                medical_condition = row[20],
                sponsor = sponsor
            )
            to_create.append(entry)
            check.append(row[0])
        # to_create.append(len(row))
    
    Student.objects.bulk_create(to_create)
    return(to_create)

def update_students_csv(file_data):
    to_update = []
    check = []
    for n in range(0, len(file_data)):
        row = file_data[n].split(',')
        student = Student.objects.get(admitnumber = row[0]) if Student.objects.filter(admitnumber = row[0]) else False
        active = True if row[2] == 'TRUE' else False

        if student and row[0] not in check:
            # sponsor = Sponsor.objects.get(email = row[21].strip()) if Sponsor.objects.filter(email = row[21].strip()) else None
            
            student.active = active
            student.name = row[2]
            # student.admitdate = row[3]
            student.batch = row[4]
            # student.birthdate = row[5]
            student.birth_place = row[6]
            student.gender = row[7]
            student.religion = row[8]
            student.nationality = row[9]
            student.category = row[10]
            student.descent = row[11]
            student.address = row[12]
            student.city = row[13]
            student.country = row[14]
            student.mother_tongue = row[15]
            student.mother_name = row[16]
            student.mother_occupation = row[17]
            student.father_name = row[18]
            student.father_occupation = row[19]
            student.medical_condition = row[20]
            # student.sponsor = sponsor

            to_update.append(student)
            check.append(row[0])

            student.save()
    
    # Student.objects.bulk_update(to_update, ['active', 'name', 'admitdate', 'batch', 'birthdate', 'birth_place', 'gender', 'religion', 'nationality', 'category', 'descent', 'address', 'city', 'country', 'mother_tongue', 'mother_name', 'mother_occupation', 'father_name', 'father_occupation', 'medical_condition'])
    return(to_update)