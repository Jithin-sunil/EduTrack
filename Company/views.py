from django.shortcuts import render, redirect
from Guest.models import tbl_company, tbl_faculty
from Student.models import tbl_internship, tbl_internshiplog
from Administrator.audit import log_action

def get_company(request):
    if 'cid' not in request.session:
        return None
    return tbl_company.objects.filter(company_id=request.session['cid']).first()

def Dashboard(request):
    company = get_company(request)
    if not company:
        return redirect('Guest:Login')
        
    posted_vacancies = tbl_internship.objects.filter(company=company, student__isnull=True).count()
    pending_applications = tbl_internship.objects.filter(company=company, internship_status=1).count()
    active_interns = tbl_internship.objects.filter(company=company, internship_status=2).count()
    
    context = {
        'company': company,
        'posted_vacancies': posted_vacancies,
        'pending_applications': pending_applications,
        'active_interns': active_interns
    }
    return render(request, 'Company/Dashboard.html', context)

def PostInternship(request):
    company = get_company(request)
    if not company:
        return redirect('Guest:Login')
        
    vacancies = tbl_internship.objects.filter(company=company, student__isnull=True).order_by('-internship_date')
    
    if request.method == 'POST':
        title = request.POST.get('txt_title')
        desc = request.POST.get('txt_desc')
        start = request.POST.get('start_date') or None
        end = request.POST.get('end_date') or None
        duration = request.POST.get('txt_duration')
        skills = request.POST.get('txt_skills')
        vacs_count = request.POST.get('txt_vacancies')
        loc = request.POST.get('txt_location')
        elig = request.POST.get('txt_eligibility')
        
        tbl_internship.objects.create(
            company=company,
            internship_title=title,
            internship_description=desc,
            internship_startdate=start,
            internship_enddate=end,
            internship_status=0, # Vacancy
            internship_duration=duration,
            internship_skills=skills,
            internship_vacancies=vacs_count if vacs_count else 1,
            internship_location=loc,
            internship_eligibility=elig
        )
        log_action('Company', company.company_id, 'InternshipVacancyCreate', f"Posted internship vacancy: {title}")
        return redirect('Company:PostInternship')
        
    return render(request, 'Company/PostInternship.html', {'vacancies': vacancies})

def InternshipApplications(request):
    company = get_company(request)
    if not company:
        return redirect('Guest:Login')
        
    apps = tbl_internship.objects.filter(company=company, internship_status=1)
    faculties = tbl_faculty.objects.filter(faculty_status=1)
    
    return render(request, 'Company/InternshipApplications.html', {'apps': apps, 'faculties': faculties})

def ApproveApplication(request, iid):
    company = get_company(request)
    if not company:
        return redirect('Guest:Login')
        
    app = tbl_internship.objects.get(internship_id=iid, company=company)
    
    if request.method == 'POST':
        fac_id = request.POST.get('sel_faculty')
        start = request.POST.get('start_date')
        end = request.POST.get('end_date')
        
        guide = tbl_faculty.objects.get(faculty_id=fac_id)
        app.faculty = guide
        app.internship_status = 2 # Approved / Ongoing
        app.internship_startdate = start
        app.internship_enddate = end
        app.save()
        
        log_action('Company', company.company_id, 'InternshipApprove', f"Approved student {app.student.student_name} for internship. Coordinator: {guide.faculty_name}")
        return redirect('Company:InternshipApplications')
        
    return redirect('Company:InternshipApplications')

def RejectApplication(request, iid):
    company = get_company(request)
    if not company:
        return redirect('Guest:Login')
        
    app = tbl_internship.objects.get(internship_id=iid, company=company)
    app.internship_status = 4 # Rejected
    app.save()
    
    log_action('Company', company.company_id, 'InternshipReject', f"Rejected application from: {app.student.student_name}")
    return redirect('Company:InternshipApplications')

def MonitorInterns(request):
    company = get_company(request)
    if not company:
        return redirect('Guest:Login')
        
    interns = tbl_internship.objects.filter(company=company, internship_status=2)
    return render(request, 'Company/MonitorInterns.html', {'interns': interns})

def ViewLogs(request, iid):
    company = get_company(request)
    if not company:
        return redirect('Guest:Login')
        
    internship = tbl_internship.objects.get(internship_id=iid, company=company)
    logs = tbl_internshiplog.objects.filter(internship=internship).order_by('-internshiplog_workdate')
    
    return render(request, 'Company/ViewLogs.html', {'internship': internship, 'logs': logs})

def AddLogRemark(request, lid):
    company = get_company(request)
    if not company:
        return redirect('Guest:Login')
        
    log = tbl_internshiplog.objects.get(internshiplog_id=lid, internship__company=company)
    if request.method == 'POST':
        remark = request.POST.get('txt_remark')
        log.internshiplog_remark = remark
        log.save()
        log_action('Company', company.company_id, 'InternshipLogRemark', f"Added mentor remark to log ID: {lid}")
        
    return redirect('Company:ViewLogs', iid=log.internship.internship_id)
