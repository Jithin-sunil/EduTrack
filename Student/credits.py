from Student.models import tbl_studentcredit, tbl_activityregistration, tbl_certificate, tbl_internshipreport, tbl_project
from Administrator.models import tbl_creditmaster
from django.db.models import Sum, Q

def update_student_credits(student):
    """
    Scans completed academic actions and records them in the student credit ledger (tbl_studentcredit)
    if they have not already been logged.
    """
    # 1. Activities (Workshops, Add-on Courses, VAC, SEC, MDC, etc.)
    activities_done = tbl_activityregistration.objects.filter(
        student=student,
        activityregistration_status=1,       # Approved
        activityregistration_completionstatus=1 # Completed
    )
    for reg in activities_done:
        # Check if already logged in ledger
        exists = tbl_studentcredit.objects.filter(
            student=student,
            studentcredit_type='Activity',
            studentcredit_sourceid=reg.activityregistration_id
        ).exists()
        if not exists:
            # Determine type of credit category
            category_name = reg.activity.activitycategory.activitycategory_name
            tbl_studentcredit.objects.create(
                student=student,
                studentcredit_type=category_name,
                studentcredit_sourceid=reg.activityregistration_id,
                studentcredit_credit=reg.activity.activity_credit,
                studentcredit_remark=f"Completed Activity: {reg.activity.activity_name}"
            )

    # 2. Certificates (Uploaded & Verified)
    certs_done = tbl_certificate.objects.filter(
        student=student,
        certificate_status=1 # Approved
    )
    for cert in certs_done:
        exists = tbl_studentcredit.objects.filter(
            student=student,
            studentcredit_type='Certificate',
            studentcredit_sourceid=cert.certificate_id
        ).exists()
        if not exists:
            tbl_studentcredit.objects.create(
                student=student,
                studentcredit_type='Certificate',
                studentcredit_sourceid=cert.certificate_id,
                studentcredit_credit=cert.certificate_credit,
                studentcredit_remark=f"Approved Certificate: {cert.certificate_title}"
            )

    # 3. Internships (Report Evaluated and Approved)
    internships_done = tbl_internshipreport.objects.filter(
        internship__student=student,
        internshipreport_status=1 # Approved
    )
    for report in internships_done:
        exists = tbl_studentcredit.objects.filter(
            student=student,
            studentcredit_type='Internship',
            studentcredit_sourceid=report.internshipreport_id
        ).exists()
        if not exists:
            # Fetch default credit value from Credit Master for Internship
            rule = tbl_creditmaster.objects.filter(creditmaster_category='Internship', creditmaster_status=1).first()
            credit_value = rule.creditmaster_credit if rule else 4
            tbl_studentcredit.objects.create(
                student=student,
                studentcredit_type='Internship',
                studentcredit_sourceid=report.internshipreport_id,
                studentcredit_credit=credit_value,
                studentcredit_remark=f"Completed Internship: {report.internship.internship_title}"
            )

    # 4. Research Projects (Approved and Completed)
    projects_done = tbl_project.objects.filter(
        student=student,
        project_status=4 # Approved/Completed
    )
    for proj in projects_done:
        exists = tbl_studentcredit.objects.filter(
            student=student,
            studentcredit_type='Project',
            studentcredit_sourceid=proj.project_id
        ).exists()
        if not exists:
            # Fetch default credit value from Credit Master for Project
            rule = tbl_creditmaster.objects.filter(creditmaster_category='Project', creditmaster_status=1).first()
            credit_value = rule.creditmaster_credit if rule else 6
            tbl_studentcredit.objects.create(
                student=student,
                studentcredit_type='Project',
                studentcredit_sourceid=proj.project_id,
                studentcredit_credit=credit_value,
                studentcredit_remark=f"Research Project Approved: {proj.project_title}"
            )

def get_student_credit_summary(student):
    """
    Returns a dict with category-wise earned credits and the total credits earned.
    """
    # Force ledger update first
    update_student_credits(student)
    
    # Query database ledger
    credits_list = tbl_studentcredit.objects.filter(student=student)
    
    # Total Required Credits
    required_total = student.programme.programme_totalcredit
    
    # Sum total earned
    earned_total = credits_list.aggregate(total=Sum('studentcredit_credit'))['total'] or 0
    
    # Category break down
    category_summary = {}
    categories = ['SEC', 'VAC', 'MDC', 'Minor', 'Internship', 'Project', 'Certificate', 'Workshop', 'Add-on']
    for cat in categories:
        cat_sum = credits_list.filter(studentcredit_type__icontains=cat).aggregate(total=Sum('studentcredit_credit'))['total'] or 0
        category_summary[cat] = cat_sum
        
    # Catch any other category types
    other_sum = credits_list.exclude(
        Q(studentcredit_type__icontains='SEC') |
        Q(studentcredit_type__icontains='VAC') |
        Q(studentcredit_type__icontains='MDC') |
        Q(studentcredit_type__icontains='Minor') |
        Q(studentcredit_type__icontains='Internship') |
        Q(studentcredit_type__icontains='Project') |
        Q(studentcredit_type__icontains='Certificate') |
        Q(studentcredit_type__icontains='Workshop') |
        Q(studentcredit_type__icontains='Add-on')
    ).aggregate(total=Sum('studentcredit_credit'))['total'] or 0

    
    category_summary['Other'] = other_sum

    pending_total = max(0, required_total - earned_total)
    
    return {
        'required_total': required_total,
        'earned_total': earned_total,
        'pending_total': pending_total,
        'categories': category_summary,
        'progress_percentage': min(100, round((earned_total / required_total) * 100)) if required_total > 0 else 0
    }
