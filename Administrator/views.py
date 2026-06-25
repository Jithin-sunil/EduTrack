from django.shortcuts import render, redirect
from Administrator.models import tbl_adminregistration, tbl_department, tbl_programme, tbl_activitycategory, tbl_creditmaster, tbl_notification
from Guest.models import tbl_student, tbl_faculty, tbl_company
from Student.models import tbl_feedback, tbl_complaint, tbl_studentcredit
from Administrator.audit import log_action
from django.db.models import Count, Sum

def Dashboard(request):
    if 'aid' not in request.session:
        return redirect('Guest:Login')
    
    aid = request.session['aid']
    # Aggregates
    student_count = tbl_student.objects.count()
    faculty_count = tbl_faculty.objects.count()
    company_count = tbl_company.objects.count()
    pending_students = tbl_student.objects.filter(student_status=0).count()
    pending_faculties = tbl_faculty.objects.filter(faculty_status=0).count()
    pending_companies = tbl_company.objects.filter(company_status=0).count()
    total_credits_awarded = tbl_studentcredit.objects.aggregate(total=Sum('studentcredit_credit'))['total'] or 0
    
    notifications = tbl_notification.objects.all().order_by('-notification_date')[:5]
    
    if request.method == 'POST':
        title = request.POST.get('txt_title')
        content = request.POST.get('txt_content')
        role = request.POST.get('sel_role')
        tbl_notification.objects.create(
            notification_title=title,
            notification_content=content,
            notification_role=role
        )
        log_action('Admin', aid, 'Notification', f"Created global notification: {title}")
        return redirect('Administrator:Dashboard')
        
    context = {
        'student_count': student_count,
        'faculty_count': faculty_count,
        'company_count': company_count,
        'pending_count': pending_students + pending_faculties + pending_companies,
        'total_credits': total_credits_awarded,
        'notifications': notifications,
        'admin_name': request.session.get('name')
    }
    return render(request, 'Administrator/Dashboard.html', context)

# Department CRUD
def Department(request):
    if 'aid' not in request.session:
        return redirect('Guest:Login')
    
    departments = tbl_department.objects.all()
    if request.method == 'POST':
        name = request.POST.get('txt_name')
        tbl_department.objects.create(department_name=name)
        log_action('Admin', request.session['aid'], 'Department', f"Added Department: {name}")
        return redirect('Administrator:Department')
        
    return render(request, 'Administrator/Department.html', {'departments': departments})

def del_department(request, did):
    if 'aid' not in request.session:
        return redirect('Guest:Login')
    
    dept = tbl_department.objects.get(department_id=did)
    log_action('Admin', request.session['aid'], 'Department', f"Deleted Department: {dept.department_name}")
    dept.delete()
    return redirect('Administrator:Department')

def edit_department(request, eid):
    if 'aid' not in request.session:
        return redirect('Guest:Login')
        
    dept = tbl_department.objects.get(department_id=eid)
    if request.method == 'POST':
        name = request.POST.get('txt_name')
        old_name = dept.department_name
        dept.department_name = name
        dept.save()
        log_action('Admin', request.session['aid'], 'Department', f"Updated Department: {old_name} -> {name}")
        return redirect('Administrator:Department')
        
    return render(request, 'Administrator/Department.html', {'editdata': dept, 'departments': tbl_department.objects.all()})

# Programme CRUD
def Programme(request):
    if 'aid' not in request.session:
        return redirect('Guest:Login')
        
    programmes = tbl_programme.objects.all()
    departments = tbl_department.objects.filter(department_status=1)
    
    if request.method == 'POST':
        name = request.POST.get('txt_name')
        dept_id = request.POST.get('sel_dept')
        duration = request.POST.get('txt_duration')
        totalcredit = request.POST.get('txt_totalcredit')
        
        dept = tbl_department.objects.get(department_id=dept_id)
        tbl_programme.objects.create(
            department=dept,
            programme_name=name,
            programme_duration=duration,
            programme_totalcredit=totalcredit
        )
        log_action('Admin', request.session['aid'], 'Programme', f"Added Programme: {name} under {dept.department_name}")
        return redirect('Administrator:Programme')
        
    return render(request, 'Administrator/Programme.html', {'programmes': programmes, 'departments': departments})

def del_programme(request, did):
    if 'aid' not in request.session:
        return redirect('Guest:Login')
        
    prog = tbl_programme.objects.get(programme_id=did)
    log_action('Admin', request.session['aid'], 'Programme', f"Deleted Programme: {prog.programme_name}")
    prog.delete()
    return redirect('Administrator:Programme')

def edit_programme(request, eid):
    if 'aid' not in request.session:
        return redirect('Guest:Login')
        
    prog = tbl_programme.objects.get(programme_id=eid)
    departments = tbl_department.objects.filter(department_status=1)
    
    if request.method == 'POST':
        name = request.POST.get('txt_name')
        dept_id = request.POST.get('sel_dept')
        duration = request.POST.get('txt_duration')
        totalcredit = request.POST.get('txt_totalcredit')
        
        dept = tbl_department.objects.get(department_id=dept_id)
        prog.programme_name = name
        prog.department = dept
        prog.programme_duration = duration
        prog.programme_totalcredit = totalcredit
        prog.save()
        
        log_action('Admin', request.session['aid'], 'Programme', f"Updated Programme: {prog.programme_name}")
        return redirect('Administrator:Programme')
        
    return render(request, 'Administrator/Programme.html', {'editdata': prog, 'programmes': tbl_programme.objects.all(), 'departments': departments})

# ActivityCategory CRUD
def ActivityCategory(request):
    if 'aid' not in request.session:
        return redirect('Guest:Login')
        
    categories = tbl_activitycategory.objects.all()
    if request.method == 'POST':
        name = request.POST.get('txt_name')
        desc = request.POST.get('txt_desc')
        tbl_activitycategory.objects.create(
            activitycategory_name=name,
            activitycategory_description=desc
        )
        log_action('Admin', request.session['aid'], 'ActivityCategory', f"Added Activity Category: {name}")
        return redirect('Administrator:ActivityCategory')
        
    return render(request, 'Administrator/ActivityCategory.html', {'categories': categories})

def del_activitycategory(request, did):
    if 'aid' not in request.session:
        return redirect('Guest:Login')
        
    cat = tbl_activitycategory.objects.get(activitycategory_id=did)
    log_action('Admin', request.session['aid'], 'ActivityCategory', f"Deleted Activity Category: {cat.activitycategory_name}")
    cat.delete()
    return redirect('Administrator:ActivityCategory')

def edit_activitycategory(request, eid):
    if 'aid' not in request.session:
        return redirect('Guest:Login')
        
    cat = tbl_activitycategory.objects.get(activitycategory_id=eid)
    if request.method == 'POST':
        name = request.POST.get('txt_name')
        desc = request.POST.get('txt_desc')
        cat.activitycategory_name = name
        cat.activitycategory_description = desc
        cat.save()
        log_action('Admin', request.session['aid'], 'ActivityCategory', f"Updated Activity Category: {name}")
        return redirect('Administrator:ActivityCategory')
        
    return render(request, 'Administrator/ActivityCategory.html', {'editdata': cat, 'categories': tbl_activitycategory.objects.all()})

# CreditMaster CRUD
def CreditMaster(request):
    if 'aid' not in request.session:
        return redirect('Guest:Login')
        
    credits = tbl_creditmaster.objects.all()
    if request.method == 'POST':
        category = request.POST.get('txt_category')
        val = request.POST.get('txt_credit')
        tbl_creditmaster.objects.create(
            creditmaster_category=category,
            creditmaster_credit=val
        )
        log_action('Admin', request.session['aid'], 'CreditMaster', f"Added Credit Master: {category} ({val} credits)")
        return redirect('Administrator:CreditMaster')
        
    return render(request, 'Administrator/CreditMaster.html', {'credits': credits})

def del_creditmaster(request, did):
    if 'aid' not in request.session:
        return redirect('Guest:Login')
        
    rule = tbl_creditmaster.objects.get(creditmaster_id=did)
    log_action('Admin', request.session['aid'], 'CreditMaster', f"Deleted Credit rule: {rule.creditmaster_category}")
    rule.delete()
    return redirect('Administrator:CreditMaster')

def edit_creditmaster(request, eid):
    if 'aid' not in request.session:
        return redirect('Guest:Login')
        
    rule = tbl_creditmaster.objects.get(creditmaster_id=eid)
    if request.method == 'POST':
        category = request.POST.get('txt_category')
        val = request.POST.get('txt_credit')
        rule.creditmaster_category = category
        rule.creditmaster_credit = val
        rule.save()
        log_action('Admin', request.session['aid'], 'CreditMaster', f"Updated Credit rule: {category} ({val} credits)")
        return redirect('Administrator:CreditMaster')
        
    return render(request, 'Administrator/CreditMaster.html', {'editdata': rule, 'credits': tbl_creditmaster.objects.all()})

# Account Approvals
def ApproveStudents(request):
    if 'aid' not in request.session:
        return redirect('Guest:Login')
        
    students = tbl_student.objects.all().order_by('student_status')
    return render(request, 'Administrator/ApproveStudents.html', {'students': students})

def ApproveStudentAction(request, sid, status):
    if 'aid' not in request.session:
        return redirect('Guest:Login')
        
    student = tbl_student.objects.get(student_id=sid)
    student.student_status = status
    student.save()
    
    action_text = "Approved" if status == 1 else "Rejected"
    log_action('Admin', request.session['aid'], 'StudentApproval', f"{action_text} Student: {student.student_name} (Adm: {student.student_admissionno})")
    
    # Create notification
    tbl_notification.objects.create(
        notification_title="Account Status Updated",
        notification_content=f"Your student account has been {action_text.lower()} by the administration.",
        notification_role='Student'
    )
    return redirect('Administrator:ApproveStudents')

def ApproveFaculties(request):
    if 'aid' not in request.session:
        return redirect('Guest:Login')
        
    faculties = tbl_faculty.objects.all().order_by('faculty_status')
    return render(request, 'Administrator/ApproveFaculties.html', {'faculties': faculties})

def ApproveFacultyAction(request, fid, status):
    if 'aid' not in request.session:
        return redirect('Guest:Login')
        
    faculty = tbl_faculty.objects.get(faculty_id=fid)
    faculty.faculty_status = status
    faculty.save()
    
    action_text = "Approved" if status == 1 else "Rejected"
    log_action('Admin', request.session['aid'], 'FacultyApproval', f"{action_text} Faculty: {faculty.faculty_name}")
    
    tbl_notification.objects.create(
        notification_title="Faculty Registration Status",
        notification_content=f"Your faculty account registration has been {action_text.lower()}.",
        notification_role='Faculty'
    )
    return redirect('Administrator:ApproveFaculties')

def ApproveCompanies(request):
    if 'aid' not in request.session:
        return redirect('Guest:Login')
        
    companies = tbl_company.objects.all().order_by('company_status')
    return render(request, 'Administrator/ApproveCompanies.html', {'companies': companies})

def ApproveCompanyAction(request, cid, status):
    if 'aid' not in request.session:
        return redirect('Guest:Login')
        
    company = tbl_company.objects.get(company_id=cid)
    company.company_status = status
    company.save()
    
    action_text = "Approved" if status == 1 else "Rejected"
    log_action('Admin', request.session['aid'], 'CompanyApproval', f"{action_text} Company Provider: {company.company_name}")
    
    tbl_notification.objects.create(
        notification_title="Company Portal Activation",
        notification_content=f"Your company account has been {action_text.lower()}.",
        notification_role='Company'
    )
    return redirect('Administrator:ApproveCompanies')

# Feedback & Complaints
def ViewFeedback(request):
    if 'aid' not in request.session:
        return redirect('Guest:Login')
        
    feedbacks = tbl_feedback.objects.all().order_by('-feedback_date')
    return render(request, 'Administrator/ViewFeedback.html', {'feedbacks': feedbacks})

def ReplyFeedback(request, fid):
    if 'aid' not in request.session:
        return redirect('Guest:Login')
        
    feedback = tbl_feedback.objects.get(feedback_id=fid)
    if request.method == 'POST':
        reply = request.POST.get('txt_reply')
        feedback.feedback_reply = reply
        feedback.feedback_status = 1
        feedback.save()
        log_action('Admin', request.session['aid'], 'FeedbackReply', f"Replied to feedback from student: {feedback.student.student_name}")
        return redirect('Administrator:ViewFeedback')
        
    return render(request, 'Administrator/Reply.html', {'type': 'Feedback', 'data': feedback})

def ViewComplaints(request):
    if 'aid' not in request.session:
        return redirect('Guest:Login')
        
    complaints = tbl_complaint.objects.all().order_by('-complaint_date')
    return render(request, 'Administrator/ViewComplaints.html', {'complaints': complaints})

def ReplyComplaint(request, cid):
    if 'aid' not in request.session:
        return redirect('Guest:Login')
        
    complaint = tbl_complaint.objects.get(complaint_id=cid)
    if request.method == 'POST':
        reply = request.POST.get('txt_reply')
        complaint.complaint_reply = reply
        complaint.complaint_status = 1
        complaint.save()
        log_action('Admin', request.session['aid'], 'ComplaintReply', f"Resolved complaint: {complaint.complaint_title}")
        return redirect('Administrator:ViewComplaints')
        
    return render(request, 'Administrator/Reply.html', {'type': 'Complaint', 'data': complaint})


# Institutional Report Generator
def ReportGenerator(request):
    if 'aid' not in request.session:
        return redirect('Guest:Login')
        
    departments = tbl_department.objects.all()
    programmes = tbl_programme.objects.all()
    
    dept_filter = request.GET.get('sel_dept')
    prog_filter = request.GET.get('sel_prog')
    
    students = tbl_student.objects.filter(student_status=1)
    
    if prog_filter:
        students = students.filter(programme_id=prog_filter)
    elif dept_filter:
        students = students.filter(programme__department_id=dept_filter)
        
    # Aggregate total credits earned per student in query
    report_data = []
    for s in students:
        total_earned = tbl_studentcredit.objects.filter(student=s).aggregate(total=Sum('studentcredit_credit'))['total'] or 0
        report_data.append({
            'student': s,
            'earned_credits': total_earned,
            'required_credits': s.programme.programme_totalcredit,
            'completion_rate': min(100, round((total_earned / s.programme.programme_totalcredit) * 100)) if s.programme.programme_totalcredit > 0 else 0
        })
        
    context = {
        'departments': departments,
        'programmes': programmes,
        'report_data': report_data,
        'selected_dept': int(dept_filter) if dept_filter else None,
        'selected_prog': int(prog_filter) if prog_filter else None
    }
    return render(request, 'Administrator/ReportGenerator.html', context)
