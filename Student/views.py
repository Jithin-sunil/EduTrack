from django.shortcuts import render, redirect
from Guest.models import tbl_student, tbl_faculty, tbl_company
from Faculty.models import tbl_activity
from Student.models import tbl_activityregistration, tbl_certificate, tbl_internship, tbl_internshiplog, tbl_internshipreport, tbl_project, tbl_feedback, tbl_complaint
from Administrator.models import tbl_notification
from Student.progression import check_progression_eligibility
from Administrator.audit import log_action

def get_student(request):
    if 'sid' not in request.session:
        return None
    return tbl_student.objects.filter(student_id=request.session['sid']).first()

def Dashboard(request):
    student = get_student(request)
    if not student:
        return redirect('Guest:Login')
        
    prog = check_progression_eligibility(student)
    notifications = tbl_notification.objects.filter(
        models.Q(notification_role='Student') | models.Q(notification_role='All')
    ).order_by('-notification_date')[:5]
    
    context = {
        'student': student,
        'prog': prog,
        'notifications': notifications
    }
    return render(request, 'Student/Dashboard.html', context)

def BrowseActivities(request):
    student = get_student(request)
    if not student:
        return redirect('Guest:Login')
        
    activities = tbl_activity.objects.filter(activity_status=0)
    
    # Enrich activities with student's registration status
    enriched_activities = []
    for act in activities:
        reg = tbl_activityregistration.objects.filter(student=student, activity=act).first()
        reg_status = -1  # Not registered
        if reg:
            reg_status = reg.activityregistration_status # 0 = Pending, 1 = Approved, 2 = Rejected
            comp_status = reg.activityregistration_completionstatus
        else:
            comp_status = 0
            
        enriched_activities.append({
            'activity': act,
            'reg_status': reg_status,
            'comp_status': comp_status
        })
        
    return render(request, 'Student/BrowseActivities.html', {'activities': enriched_activities})

def RegisterActivity(request, aid):
    student = get_student(request)
    if not student:
        return redirect('Guest:Login')
        
    act = tbl_activity.objects.get(activity_id=aid)
    # Check if already registered
    if not tbl_activityregistration.objects.filter(student=student, activity=act).exists():
        tbl_activityregistration.objects.create(
            student=student,
            activity=act,
            activityregistration_status=0, # Pending
            activityregistration_completionstatus=0 # Ongoing
        )
        log_action('Student', student.student_id, 'ActivityRegistration', f"Registered for Activity: {act.activity_name}")
        
    return redirect('Student:BrowseActivities')

def CertificateUpload(request):
    student = get_student(request)
    if not student:
        return redirect('Guest:Login')
        
    certs = tbl_certificate.objects.filter(student=student).order_by('-certificate_date')
    # Filter out approved activities where the student doesn't have an uploaded certificate yet
    activities = tbl_activityregistration.objects.filter(student=student, activityregistration_status=1)
    
    if request.method == 'POST':
        title = request.POST.get('txt_title')
        file = request.FILES.get('cert_file')
        act_id = request.POST.get('sel_activity')
        
        act = tbl_activity.objects.get(activity_id=act_id) if act_id else None
        tbl_certificate.objects.create(
            student=student,
            activity=act,
            certificate_title=title,
            certificate_file=file,
            certificate_status=0
        )
        log_action('Student', student.student_id, 'CertificateUpload', f"Uploaded Certificate: {title}")
        return redirect('Student:CertificateUpload')
        
    return render(request, 'Student/CertificateUpload.html', {'certs': certs, 'activities': activities})

def InternshipPortal(request):
    student = get_student(request)
    if not student:
        return redirect('Guest:Login')
        
    # Browse vacancies
    vacancies = tbl_internship.objects.filter(student__isnull=True, internship_status=0)
    
    # Student's applied / ongoing / completed internships
    my_internships = tbl_internship.objects.filter(student=student).order_by('-internship_date')
    
    # Active/ongoing internship reports
    active_internship = my_internships.filter(internship_status__in=[2, 3]).first()
    
    context = {
        'vacancies': vacancies,
        'my_internships': my_internships,
        'active_internship': active_internship
    }
    return render(request, 'Student/InternshipPortal.html', context)

def ApplyInternship(request, iid):
    student = get_student(request)
    if not student:
        return redirect('Guest:Login')
        
    vacancy = tbl_internship.objects.get(internship_id=iid)
    # Check if student has already applied for this company
    already_applied = tbl_internship.objects.filter(student=student, company=vacancy.company, internship_title=vacancy.internship_title).exists()
    if not already_applied:
        # Create a new record assigning student and status = 1 (Applied)
        tbl_internship.objects.create(
            student=student,
            company=vacancy.company,
            internship_title=vacancy.internship_title,
            internship_description=vacancy.internship_description,
            internship_status=1, # Applied
            internship_startdate=vacancy.internship_startdate,
            internship_enddate=vacancy.internship_enddate
        )
        log_action('Student', student.student_id, 'InternshipApply', f"Applied for internship: {vacancy.internship_title} at {vacancy.company.company_name}")
        
    return redirect('Student:InternshipPortal')

def InternshipLog(request, iid):
    student = get_student(request)
    if not student:
        return redirect('Guest:Login')
        
    internship = tbl_internship.objects.get(internship_id=iid, student=student)
    logs = tbl_internshiplog.objects.filter(internship=internship).order_by('-internshiplog_workdate')
    
    if request.method == 'POST':
        workdate = request.POST.get('work_date')
        workdone = request.POST.get('work_done')
        hours = request.POST.get('hours')
        
        tbl_internshiplog.objects.create(
            internship=internship,
            internshiplog_workdate=workdate,
            internshiplog_workdone=workdone,
            internshiplog_hours=hours
        )
        log_action('Student', student.student_id, 'InternshipLog', f"Added log for date: {workdate}")
        return redirect('Student:InternshipLog', iid=iid)
        
    return render(request, 'Student/InternshipLog.html', {'internship': internship, 'logs': logs})

def InternshipReport(request, iid):
    student = get_student(request)
    if not student:
        return redirect('Guest:Login')
        
    internship = tbl_internship.objects.get(internship_id=iid, student=student)
    reports = tbl_internshipreport.objects.filter(internship=internship)
    
    if request.method == 'POST':
        report_file = request.FILES.get('report_file')
        cert_file = request.FILES.get('cert_file')
        remark = request.POST.get('txt_remark')
        
        tbl_internshipreport.objects.create(
            internship=internship,
            internshipreport_file=report_file,
            internshipreport_certificate=cert_file,
            internshipreport_remark=remark,
            internshipreport_status=0
        )
        
        # Change internship status to 3 (Completed)
        internship.internship_status = 3
        internship.save()
        
        log_action('Student', student.student_id, 'InternshipReportUpload', f"Submitted report for: {internship.internship_title}")
        return redirect('Student:InternshipPortal')
        
    return render(request, 'Student/InternshipReport.html', {'internship': internship, 'reports': reports})

def ProjectSpace(request):
    student = get_student(request)
    if not student:
        return redirect('Guest:Login')
        
    projects = tbl_project.objects.filter(student=student).order_by('-project_date')
    faculties = tbl_faculty.objects.filter(faculty_status=1)
    
    if request.method == 'POST':
        action_type = request.POST.get('action_type')
        
        if action_type == 'propose':
            title = request.POST.get('txt_title')
            desc = request.POST.get('txt_desc')
            fac_id = request.POST.get('sel_faculty')
            proposal = request.FILES.get('proposal_file')
            
            guide = tbl_faculty.objects.get(faculty_id=fac_id)
            tbl_project.objects.create(
                student=student,
                faculty=guide,
                project_title=title,
                project_description=desc,
                project_proposal=proposal,
                project_status=0
            )
            log_action('Student', student.student_id, 'ProjectPropose', f"Proposed research project: {title}")
            
        elif action_type == 'upload_report':
            proj_id = request.POST.get('proj_id')
            report = request.FILES.get('report_file')
            
            proj = tbl_project.objects.get(project_id=proj_id)
            proj.project_report = report
            proj.project_status = 3 # Report Submitted
            proj.save()
            log_action('Student', student.student_id, 'ProjectReportUpload', f"Uploaded final report for project: {proj.project_title}")
            
        return redirect('Student:ProjectSpace')
        
    return render(request, 'Student/ProjectSpace.html', {'projects': projects, 'faculties': faculties})

def Feedback(request):
    student = get_student(request)
    if not student:
        return redirect('Guest:Login')
        
    feedbacks = tbl_feedback.objects.filter(student=student).order_by('-feedback_date')
    if request.method == 'POST':
        content = request.POST.get('txt_content')
        tbl_feedback.objects.create(
            student=student,
            feedback_content=content,
            feedback_status=0
        )
        log_action('Student', student.student_id, 'FeedbackSubmit', "Submitted feedback")
        return redirect('Student:Feedback')
        
    return render(request, 'Student/Feedback.html', {'feedbacks': feedbacks})

def Complaint(request):
    student = get_student(request)
    if not student:
        return redirect('Guest:Login')
        
    complaints = tbl_complaint.objects.filter(student=student).order_by('-complaint_date')
    if request.method == 'POST':
        title = request.POST.get('txt_title')
        content = request.POST.get('txt_content')
        tbl_complaint.objects.create(
            student=student,
            complaint_title=title,
            complaint_content=content,
            complaint_status=0
        )
        log_action('Student', student.student_id, 'ComplaintSubmit', f"Filed complaint: {title}")
        return redirect('Student:Complaint')
        
    return render(request, 'Student/Complaint.html', {'complaints': complaints})
