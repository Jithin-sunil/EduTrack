from Student.models import tbl_internshipreport, tbl_project, tbl_activityregistration
from Student.credits import get_student_credit_summary

def check_progression_eligibility(student):
    """
    Checks if a student has met the criteria to progress and graduate under FYUGP:
    - Earned all required programme credits.
    - Completed an approved internship.
    - Completed an approved research project (for BCA Honours).
    """
    credit_summary = get_student_credit_summary(student)
    
    # 1. Check Internship completion
    has_internship = tbl_internshipreport.objects.filter(
        internship__student=student,
        internshipreport_status=1
    ).exists()
    
    # 2. Check Project completion (required for BCA Honours)
    has_project = tbl_project.objects.filter(
        student=student,
        project_status=4
    ).exists()
    
    # 3. Check credits requirement
    credits_met = credit_summary['earned_total'] >= credit_summary['required_total']
    
    # Graduation check
    is_eligible_graduation = credits_met and has_internship and has_project
    
    # Simple progression logic: e.g. student is in active status
    status_text = "In Progress"
    if is_eligible_graduation:
        status_text = "Eligible for Graduation"
    elif credits_met:
        status_text = "Pending Internship and Project Evaluations"
        
    return {
        'credit_summary': credit_summary,
        'has_internship': has_internship,
        'has_project': has_project,
        'credits_met': credits_met,
        'is_eligible_graduation': is_eligible_graduation,
        'status_text': status_text
    }
