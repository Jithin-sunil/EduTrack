from django.db import models
from Administrator.models import tbl_department, tbl_programme

class tbl_student(models.Model):
    student_id = models.AutoField(primary_key=True)
    programme = models.ForeignKey(tbl_programme, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=100)
    student_gender = models.CharField(max_length=20)
    student_dob = models.DateField()
    student_email = models.EmailField(max_length=100, unique=True)
    student_contact = models.CharField(max_length=20)
    student_address = models.TextField()
    student_admissionno = models.CharField(max_length=50, unique=True)
    student_semester = models.IntegerField(default=1)
    student_photo = models.FileField(upload_to='Assets/StudentDocs/', null=True, blank=True)
    student_password = models.CharField(max_length=60)
    student_status = models.IntegerField(default=0) # 0 = Pending, 1 = Active/Approved, 2 = Rejected
    student_date = models.DateField(auto_now_add=True)

class tbl_faculty(models.Model):
    faculty_id = models.AutoField(primary_key=True)
    department = models.ForeignKey(tbl_department, on_delete=models.CASCADE)
    faculty_name = models.CharField(max_length=100)
    faculty_email = models.EmailField(max_length=100, unique=True)
    faculty_contact = models.CharField(max_length=20)
    faculty_address = models.TextField()
    faculty_photo = models.FileField(upload_to='Assets/FacultyDocs/', null=True, blank=True)
    faculty_password = models.CharField(max_length=60)
    faculty_status = models.IntegerField(default=0) # 0 = Pending, 1 = Active/Approved, 2 = Rejected
    faculty_date = models.DateField(auto_now_add=True)

class tbl_company(models.Model):
    company_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=100)
    company_contactperson = models.CharField(max_length=100)
    company_email = models.EmailField(max_length=100, unique=True)
    company_contact = models.CharField(max_length=20)
    company_address = models.TextField()
    company_password = models.CharField(max_length=60)
    company_proof = models.FileField(upload_to='Assets/CompanyDocs/', null=True, blank=True)
    company_status = models.IntegerField(default=0) # 0 = Pending, 1 = Active/Approved, 2 = Rejected
    company_date = models.DateField(auto_now_add=True)
