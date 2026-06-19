from django.urls import path
from . import views

app_name = 'Administrator'

urlpatterns = [
    path('Dashboard/', views.Dashboard, name='Dashboard'),
    
    # Department CRUD
    path('Department/', views.Department, name='Department'),
    path('DelDepartment/<int:did>/', views.del_department, name='del_department'),
    path('EditDepartment/<int:eid>/', views.edit_department, name='edit_department'),
    
    # Programme CRUD
    path('Programme/', views.Programme, name='Programme'),
    path('DelProgramme/<int:did>/', views.del_programme, name='del_programme'),
    path('EditProgramme/<int:eid>/', views.edit_programme, name='edit_programme'),
    
    # ActivityCategory CRUD
    path('ActivityCategory/', views.ActivityCategory, name='ActivityCategory'),
    path('DelActivityCategory/<int:did>/', views.del_activitycategory, name='del_activitycategory'),
    path('EditActivityCategory/<int:eid>/', views.edit_activitycategory, name='edit_activitycategory'),
    
    # CreditMaster CRUD
    path('CreditMaster/', views.CreditMaster, name='CreditMaster'),
    path('DelCreditMaster/<int:did>/', views.del_creditmaster, name='del_creditmaster'),
    path('EditCreditMaster/<int:eid>/', views.edit_creditmaster, name='edit_creditmaster'),
    
    # Account Approvals
    path('ApproveStudents/', views.ApproveStudents, name='ApproveStudents'),
    path('ApproveStudentAction/<int:sid>/<int:status>/', views.ApproveStudentAction, name='ApproveStudentAction'),
    
    path('ApproveFaculties/', views.ApproveFaculties, name='ApproveFaculties'),
    path('ApproveFacultyAction/<int:fid>/<int:status>/', views.ApproveFacultyAction, name='ApproveFacultyAction'),
    
    path('ApproveCompanies/', views.ApproveCompanies, name='ApproveCompanies'),
    path('ApproveCompanyAction/<int:cid>/<int:status>/', views.ApproveCompanyAction, name='ApproveCompanyAction'),
    
    # Feedback & Complaints
    path('ViewFeedback/', views.ViewFeedback, name='ViewFeedback'),
    path('ReplyFeedback/<int:fid>/', views.ReplyFeedback, name='ReplyFeedback'),
    path('ViewComplaints/', views.ViewComplaints, name='ViewComplaints'),
    path('ReplyComplaint/<int:cid>/', views.ReplyComplaint, name='ReplyComplaint'),
    
    # Audit Logs & Reports
    path('AuditLogs/', views.AuditLogs, name='AuditLogs'),
    path('ReportGenerator/', views.ReportGenerator, name='ReportGenerator'),
]
