from django.shortcuts import render, redirect
from Guest.models import tbl_faculty, tbl_student
from Faculty.models import tbl_activity
from Student.models import tbl_activityregistration, tbl_certificate, tbl_internshipreport, tbl_project, tbl_evaluation, tbl_internship, tbl_projectmilestone, tbl_internshiplog
from Administrator.models import tbl_activitycategory, tbl_notification
from Student.credits import update_student_credits
from Administrator.audit import log_action

def get_faculty(request):
    if 'fid' not in request.session:
        return None
    return tbl_faculty.objects.filter(faculty_id=request.session['fid']).first()

def Dashboard(request):
    faculty = get_faculty(request)
    if not faculty:
        return redirect('Guest:Login')
        
    activities_hosted = tbl_activity.objects.filter(faculty=faculty).count()
    pending_registrations = tbl_activityregistration.objects.filter(activity__faculty=faculty, activityregistration_status=0).count()
    
    # Departmental certificates verify queue
    pending_certs = tbl_certificate.objects.filter(
        student__programme__department=faculty.department,
        certificate_status=0
    ).count()
    
    pending_internships = tbl_internshipreport.objects.filter(
        internship__faculty=faculty,
        internshipreport_status=0
    ).count()
    
    projects_guided = tbl_project.objects.filter(faculty=faculty).count()
    
    context = {
        'faculty': faculty,
        'activities_hosted': activities_hosted,
        'pending_registrations': pending_registrations,
        'pending_certs': pending_certs,
        'pending_internships': pending_internships,
        'projects_guided': projects_guided
    }
    return render(request, 'Faculty/Dashboard.html', context)

def ManageActivities(request):
    faculty = get_faculty(request)
    if not faculty:
        return redirect('Guest:Login')
        
    activities = tbl_activity.objects.filter(faculty=faculty).order_by('-activity_date')
    categories = tbl_activitycategory.objects.filter(activitycategory_status=1)
    
    if request.method == 'POST':
        name = request.POST.get('txt_name')
        desc = request.POST.get('txt_desc')
        cat_id = request.POST.get('sel_category')
        credit = request.POST.get('txt_credit')
        startdate = request.POST.get('start_date')
        enddate = request.POST.get('end_date')
        file = request.FILES.get('activity_file')
        
        category = tbl_activitycategory.objects.get(activitycategory_id=cat_id)
        tbl_activity.objects.create(
            activitycategory=category,
            faculty=faculty,
            activity_name=name,
            activity_description=desc,
            activity_credit=credit,
            activity_startdate=startdate,
            activity_enddate=enddate,
            activity_file=file
        )
        log_action('Faculty', faculty.faculty_id, 'ActivityCreate', f"Created Activity: {name}")
        return redirect('Faculty:ManageActivities')
        
    return render(request, 'Faculty/ManageActivities.html', {'activities': activities, 'categories': categories})

def ActivityRegistrations(request):
    faculty = get_faculty(request)
    if not faculty:
        return redirect('Guest:Login')
        
    regs = tbl_activityregistration.objects.filter(
        activity__faculty=faculty,
        activityregistration_status=0
    )
    return render(request, 'Faculty/ActivityRegistrations.html', {'regs': regs})

def ApproveRegistration(request, rid, status):
    faculty = get_faculty(request)
    if not faculty:
        return redirect('Guest:Login')
        
    reg = tbl_activityregistration.objects.get(activityregistration_id=rid, activity__faculty=faculty)
    reg.activityregistration_status = status
    reg.save()
    
    action_text = "Approved" if status == 1 else "Rejected"
    log_action('Faculty', faculty.faculty_id, 'ActivityRegistrationApproval', f"{action_text} Student registration for: {reg.activity.activity_name}")
    
    return redirect('Faculty:ActivityRegistrations')

def ManageCompletion(request, aid):
    faculty = get_faculty(request)
    if not faculty:
        return redirect('Guest:Login')
        
    activity = tbl_activity.objects.get(activity_id=aid, faculty=faculty)
    participants = tbl_activityregistration.objects.filter(activity=activity, activityregistration_status=1)
    
    return render(request, 'Faculty/ManageCompletion.html', {'activity': activity, 'participants': participants})

def CompleteActivityRegistration(request, rid, status):
    faculty = get_faculty(request)
    if not faculty:
        return redirect('Guest:Login')
        
    reg = tbl_activityregistration.objects.get(activityregistration_id=rid, activity__faculty=faculty)
    
    if request.method == 'POST' and status == 1:
        att = request.POST.get('txt_attendance')
        part = request.POST.get('txt_participation')
        res = request.POST.get('txt_result')
        
        reg.attendance_percentage = att if att else 0
        reg.participation_status = part if part else ''
        reg.activity_result = res if res else ''
        reg.activityregistration_completionstatus = 1
        reg.save()
        
        log_action('Faculty', faculty.faculty_id, 'ActivityCompletionStatus', f"Marked student {reg.student.student_name} as Completed in {reg.activity.activity_name} (Att: {att}%, Part: {part}, Res: {res})")
        
        # Update student credit ledger
        update_student_credits(reg.student)
        return redirect('Faculty:ManageCompletion', aid=reg.activity.activity_id)
        
    elif status == 2:
        reg.activityregistration_completionstatus = 2
        reg.save()
        log_action('Faculty', faculty.faculty_id, 'ActivityCompletionStatus', f"Marked student {reg.student.student_name} as Failed in {reg.activity.activity_name}")
        return redirect('Faculty:ManageCompletion', aid=reg.activity.activity_id)
        
    return redirect('Faculty:ManageCompletion', aid=reg.activity.activity_id)

def VerifyCertificates(request):
    faculty = get_faculty(request)
    if not faculty:
        return redirect('Guest:Login')
        
    certs = tbl_certificate.objects.filter(
        student__programme__department=faculty.department,
        certificate_status=0
    )
    return render(request, 'Faculty/VerifyCertificates.html', {'certs': certs})

def VerifyCertificateAction(request, cid, status):
    faculty = get_faculty(request)
    if not faculty:
        return redirect('Guest:Login')
        
    cert = tbl_certificate.objects.get(certificate_id=cid, student__programme__department=faculty.department)
    
    if request.method == 'POST':
        credits_awarded = request.POST.get('txt_credit')
        remark = request.POST.get('txt_remark')
        
        cert.certificate_status = status
        cert.certificate_credit = credits_awarded if status == 1 else 0
        cert.certificate_remark = remark
        cert.save()
        
        action_text = "Approved" if status == 1 else "Rejected"
        log_action('Faculty', faculty.faculty_id, 'CertificateVerification', f"{action_text} Certificate: {cert.certificate_title} for {cert.student.student_name}")
        
        if status == 1:
            update_student_credits(cert.student)
            
        return redirect('Faculty:VerifyCertificates')
        
    return render(request, 'Faculty/VerifyAction.html', {'cert': cert, 'status': status})

def EvaluateInternships(request):
    faculty = get_faculty(request)
    if not faculty:
        return redirect('Guest:Login')
        
    reports = tbl_internshipreport.objects.filter(
        internship__faculty=faculty,
        internshipreport_status=0
    )
    ongoing = tbl_internship.objects.filter(
        faculty=faculty,
        internship_status=2 # Ongoing
    )
    return render(request, 'Faculty/EvaluateInternships.html', {'reports': reports, 'ongoing_internships': ongoing})

def SubmitEvaluation(request, report_id):
    faculty = get_faculty(request)
    if not faculty:
        return redirect('Guest:Login')
        
    report = tbl_internshipreport.objects.get(internshipreport_id=report_id, internship__faculty=faculty)
    
    if request.method == 'POST':
        marks = request.POST.get('txt_marks')
        remark = request.POST.get('txt_remark')
        
        # Create evaluation
        tbl_evaluation.objects.create(
            internship=report.internship,
            evaluation_marks=marks,
            evaluation_remark=remark,
            evaluation_status=1
        )
        
        # Approve report
        report.internshipreport_status = 1
        report.save()
        
        # Mark internship status as completed
        report.internship.internship_status = 3
        report.internship.save()
        
        log_action('Faculty', faculty.faculty_id, 'InternshipEvaluation', f"Evaluated internship report for: {report.internship.student.student_name}")
        
        # Sync student credits
        update_student_credits(report.internship.student)
        
        return redirect('Faculty:EvaluateInternships')
        
    return render(request, 'Faculty/SubmitEvaluation.html', {'report': report})

def ApproveProjects(request):
    faculty = get_faculty(request)
    if not faculty:
        return redirect('Guest:Login')
        
    projects = tbl_project.objects.filter(faculty=faculty).order_by('project_status')
    return render(request, 'Faculty/ApproveProjects.html', {'projects': projects})

def ApproveProjectAction(request, pid, status):
    faculty = get_faculty(request)
    if not faculty:
        return redirect('Guest:Login')
        
    proj = tbl_project.objects.get(project_id=pid, faculty=faculty)
    proj.project_status = status
    if status == 4:
        # Sync credits for project
        update_student_credits(proj.student)
        
    return redirect('Faculty:ApproveProjects')

def VerifyMilestone(request, mid, status):
    faculty = get_faculty(request)
    if not faculty:
        return redirect('Guest:Login')
        
    ms = tbl_projectmilestone.objects.get(milestone_id=mid, project__faculty=faculty)
    
    if request.method == 'POST':
        remark = request.POST.get('txt_remark')
        ms.milestone_status = status
        ms.milestone_remark = remark
        ms.save()
        
        action_text = "Approved Milestone" if status == 1 else "Requested Modifications for Milestone"
        log_action('Faculty', faculty.faculty_id, 'ProjectMilestoneVerify', f"{action_text}: {ms.milestone_title} of project: {ms.project.project_title}")
        return redirect('Faculty:ApproveProjects')
        
    return render(request, 'Faculty/VerifyMilestone.html', {'milestone': ms, 'status': status})

def ViewInternLogs(request, iid):
    faculty = get_faculty(request)
    if not faculty:
        return redirect('Guest:Login')
        
    internship = tbl_internship.objects.get(internship_id=iid, faculty=faculty)
    logs = tbl_internshiplog.objects.filter(internship=internship).order_by('-internshiplog_workdate')
    
    return render(request, 'Faculty/ViewInternLogs.html', {'internship': internship, 'logs': logs})
