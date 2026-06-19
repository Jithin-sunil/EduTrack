from django.db import models
from Guest.models import tbl_student, tbl_faculty, tbl_company
from Faculty.models import tbl_activity

class tbl_activityregistration(models.Model):
    activityregistration_id = models.AutoField(primary_key=True)
    activity = models.ForeignKey(tbl_activity, on_delete=models.CASCADE)
    student = models.ForeignKey(tbl_student, on_delete=models.CASCADE)
    activityregistration_date = models.DateField(auto_now_add=True)
    activityregistration_status = models.IntegerField(default=0) # 0 = Pending, 1 = Approved, 2 = Rejected
    activityregistration_completionstatus = models.IntegerField(default=0) # 0 = Ongoing, 1 = Completed, 2 = Failed

class tbl_certificate(models.Model):
    certificate_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(tbl_student, on_delete=models.CASCADE)
    activity = models.ForeignKey(tbl_activity, on_delete=models.CASCADE, null=True, blank=True)
    certificate_title = models.CharField(max_length=100)
    certificate_file = models.FileField(upload_to='Assets/StudentCertificates/')
    certificate_credit = models.IntegerField(default=0)
    certificate_remark = models.TextField(null=True, blank=True)
    certificate_status = models.IntegerField(default=0) # 0 = Pending, 1 = Approved, 2 = Rejected
    certificate_date = models.DateField(auto_now_add=True)

class tbl_internship(models.Model):
    internship_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(tbl_student, on_delete=models.CASCADE, null=True, blank=True)
    company = models.ForeignKey(tbl_company, on_delete=models.CASCADE)
    faculty = models.ForeignKey(tbl_faculty, on_delete=models.SET_NULL, null=True, blank=True)
    internship_title = models.CharField(max_length=100)
    internship_description = models.TextField()
    internship_startdate = models.DateField(null=True, blank=True)
    internship_enddate = models.DateField(null=True, blank=True)
    internship_status = models.IntegerField(default=0) # 0 = Opportunity/Vacancy, 1 = Applied, 2 = Ongoing, 3 = Completed, 4 = Rejected
    internship_date = models.DateField(auto_now_add=True)

class tbl_internshiplog(models.Model):
    internshiplog_id = models.AutoField(primary_key=True)
    internship = models.ForeignKey(tbl_internship, on_delete=models.CASCADE)
    internshiplog_workdate = models.DateField()
    internshiplog_workdone = models.TextField()
    internshiplog_hours = models.IntegerField()
    internshiplog_remark = models.TextField(null=True, blank=True)
    internshiplog_date = models.DateField(auto_now_add=True)

class tbl_internshipreport(models.Model):
    internshipreport_id = models.AutoField(primary_key=True)
    internship = models.ForeignKey(tbl_internship, on_delete=models.CASCADE)
    internshipreport_file = models.FileField(upload_to='Assets/InternshipReports/')
    internshipreport_certificate = models.FileField(upload_to='Assets/InternshipCertificates/')
    internshipreport_remark = models.TextField(null=True, blank=True)
    internshipreport_status = models.IntegerField(default=0) # 0 = Submitted, 1 = Approved, 2 = Rejected
    internshipreport_date = models.DateField(auto_now_add=True)

class tbl_project(models.Model):
    project_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(tbl_student, on_delete=models.CASCADE)
    faculty = models.ForeignKey(tbl_faculty, on_delete=models.CASCADE)
    project_title = models.CharField(max_length=100)
    project_description = models.TextField()
    project_proposal = models.FileField(upload_to='Assets/ProjectProposals/', null=True, blank=True)
    project_report = models.FileField(upload_to='Assets/ProjectReports/', null=True, blank=True)
    project_status = models.IntegerField(default=0) # 0 = Proposed, 1 = Proposal Approved, 2 = Proposal Rejected, 3 = Report Submitted, 4 = Completed/Approved, 5 = Modification Requested
    project_date = models.DateField(auto_now_add=True)

class tbl_studentcredit(models.Model):
    studentcredit_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(tbl_student, on_delete=models.CASCADE)
    studentcredit_type = models.CharField(max_length=50) # SEC, VAC, MDC, Minor, Internship, Project, Add-on, Certificate, etc.
    studentcredit_sourceid = models.IntegerField() # Source record PK id
    studentcredit_credit = models.IntegerField()
    studentcredit_remark = models.CharField(max_length=255, null=True, blank=True)
    studentcredit_date = models.DateField(auto_now_add=True)

class tbl_evaluation(models.Model):
    evaluation_id = models.AutoField(primary_key=True)
    internship = models.ForeignKey(tbl_internship, on_delete=models.CASCADE)
    evaluation_marks = models.IntegerField()
    evaluation_remark = models.TextField()
    evaluation_status = models.IntegerField(default=1) # 1 = Evaluated
    evaluation_date = models.DateField(auto_now_add=True)

class tbl_feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(tbl_student, on_delete=models.CASCADE)
    feedback_content = models.TextField()
    feedback_reply = models.TextField(null=True, blank=True)
    feedback_date = models.DateField(auto_now_add=True)
    feedback_status = models.IntegerField(default=0) # 0 = Pending, 1 = Replied

class tbl_complaint(models.Model):
    complaint_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(tbl_student, on_delete=models.CASCADE)
    complaint_title = models.CharField(max_length=100)
    complaint_content = models.TextField()
    complaint_reply = models.TextField(null=True, blank=True)
    complaint_status = models.IntegerField(default=0) # 0 = Pending, 1 = Resolved
    complaint_date = models.DateField(auto_now_add=True)
