import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()

from Guest.models import tbl_student, tbl_faculty, tbl_company

print("--- STUDENTS ---")
for s in tbl_student.objects.all():
    print(f"Name: {s.student_name}, Email: {s.student_email}, Pwd: {s.student_password}")

print("\n--- FACULTIES ---")
for f in tbl_faculty.objects.all():
    print(f"Name: {f.faculty_name}, Email: {f.faculty_email}, Pwd: {f.faculty_password}")

print("\n--- COMPANIES ---")
for c in tbl_company.objects.all():
    print(f"Name: {c.company_name}, Email: {c.company_email}, Pwd: {c.company_password}")
