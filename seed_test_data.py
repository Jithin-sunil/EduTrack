import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()

from Administrator.models import tbl_department, tbl_programme, tbl_activitycategory
from Guest.models import tbl_student, tbl_faculty, tbl_company

# 1. Create Department
dept, _ = tbl_department.objects.get_or_create(
    department_name='Computer Science',
    defaults={'department_status': 1}
)
print("Department 'Computer Science' created/fetched.")

# 2. Create Programme
prog, _ = tbl_programme.objects.get_or_create(
    programme_name='BCA Honours',
    defaults={
        'department': dept,
        'programme_duration': 8,
        'programme_totalcredit': 160,
        'programme_status': 1
    }
)
print("Programme 'BCA Honours' created/fetched.")

# 3. Create Activity Categories
categories = [
    ('Workshop', 'Academic workshops and hands-on training sessions'),
    ('Add-on Course', 'Value-added certification courses'),
    ('SEC', 'Skill Enhancement Course'),
    ('VAC', 'Value Added Course'),
    ('MDC', 'Multi Disciplinary Course')
]
for cat_name, cat_desc in categories:
    tbl_activitycategory.objects.get_or_create(
        activitycategory_name=cat_name,
        defaults={'activitycategory_description': cat_desc, 'activitycategory_status': 1}
    )
print("Activity categories seeded.")

# 4. Create Faculty Coordinator
fac, _ = tbl_faculty.objects.get_or_create(
    faculty_email='faculty@college.edu',
    defaults={
        'department': dept,
        'faculty_name': 'Dr. Rachel Green',
        'faculty_contact': '9876543222',
        'faculty_address': 'CS Dept Block B, College Campus',
        'faculty_password': 'faculty123',
        'faculty_status': 1
    }
)
print("Faculty 'Dr. Rachel Green' (faculty@college.edu / faculty123) created/fetched.")

# 5. Create Student Akhil
stud, _ = tbl_student.objects.get_or_create(
    student_email='akhil@college.edu',
    defaults={
        'programme': prog,
        'student_name': 'Akhil Sunil',
        'student_gender': 'Male',
        'student_dob': '2005-05-15',
        'student_contact': '9876543211',
        'student_address': 'Sunil Villa, Cochin',
        'student_admissionno': 'BCA2026001',
        'student_semester': 1,
        'student_password': 'student123',
        'student_status': 1
    }
)
print("Student 'Akhil Sunil' (akhil@college.edu / student123) created/fetched.")

# 6. Create Internship Company
comp, _ = tbl_company.objects.get_or_create(
    company_email='hr@meta.com',
    defaults={
        'company_name': 'Meta Platforms Inc.',
        'company_contactperson': 'Mark Zuckerberg',
        'company_contact': '9876543233',
        'company_address': 'Menlo Park, California',
        'company_password': 'meta123',
        'company_status': 1
    }
)
print("Company 'Meta Platforms Inc.' (hr@meta.com / meta123) created/fetched.")
