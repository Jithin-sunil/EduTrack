from django.db import models

class tbl_adminregistration(models.Model):
    adminregistration_id = models.AutoField(primary_key=True)
    adminregistration_name = models.CharField(max_length=60)
    adminregistration_contact = models.CharField(max_length=60)
    adminregistration_email = models.CharField(max_length=60, unique=True)
    adminregistration_password = models.CharField(max_length=60)

class tbl_department(models.Model):
    department_id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=100)
    department_status = models.IntegerField(default=1) # 1 = Active, 0 = Inactive

class tbl_programme(models.Model):
    programme_id = models.AutoField(primary_key=True)
    department = models.ForeignKey(tbl_department, on_delete=models.CASCADE)
    programme_name = models.CharField(max_length=100)
    programme_duration = models.IntegerField() # Duration in Semesters (e.g. 8)
    programme_totalcredit = models.IntegerField() # Total credits required (e.g. 160)
    programme_status = models.IntegerField(default=1) # 1 = Active, 0 = Inactive

class tbl_activitycategory(models.Model):
    activitycategory_id = models.AutoField(primary_key=True)
    activitycategory_name = models.CharField(max_length=100)
    activitycategory_description = models.TextField()
    activitycategory_status = models.IntegerField(default=1) # 1 = Active, 0 = Inactive

class tbl_creditmaster(models.Model):
    creditmaster_id = models.AutoField(primary_key=True)
    creditmaster_category = models.CharField(max_length=50) # e.g. SEC, VAC, MDC, Minor, Internship, Project, Add-on, Certificate, etc.
    creditmaster_credit = models.IntegerField()
    creditmaster_status = models.IntegerField(default=1) # 1 = Active, 0 = Inactive

class tbl_notification(models.Model):
    notification_id = models.AutoField(primary_key=True)
    notification_title = models.CharField(max_length=100)
    notification_content = models.TextField()
    notification_role = models.CharField(max_length=20) # 'Admin', 'Student', 'Faculty', 'Company', or 'All'
    notification_date = models.DateField(auto_now_add=True)
    notification_status = models.IntegerField(default=0) # 0 = Unread, 1 = Read

class tbl_auditlog(models.Model):
    auditlog_id = models.AutoField(primary_key=True)
    auditlog_usertype = models.CharField(max_length=20) # Admin, Student, Faculty, Company
    auditlog_userid = models.IntegerField()
    auditlog_module = models.CharField(max_length=50)
    auditlog_action = models.CharField(max_length=255)
    auditlog_date = models.DateField(auto_now_add=True)
    auditlog_time = models.TimeField(auto_now_add=True)
