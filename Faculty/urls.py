from django.urls import path
from . import views

app_name = 'Faculty'

urlpatterns = [
    path('Dashboard/', views.Dashboard, name='Dashboard'),
    path('ManageActivities/', views.ManageActivities, name='ManageActivities'),
    path('ActivityRegistrations/', views.ActivityRegistrations, name='ActivityRegistrations'),
    path('ApproveRegistration/<int:rid>/<int:status>/', views.ApproveRegistration, name='ApproveRegistration'),
    path('ManageCompletion/<int:aid>/', views.ManageCompletion, name='ManageCompletion'),
    path('CompleteActivityRegistration/<int:rid>/<int:status>/', views.CompleteActivityRegistration, name='CompleteActivityRegistration'),
    
    path('VerifyCertificates/', views.VerifyCertificates, name='VerifyCertificates'),
    path('VerifyCertificateAction/<int:cid>/<int:status>/', views.VerifyCertificateAction, name='VerifyCertificateAction'),
    
    path('EvaluateInternships/', views.EvaluateInternships, name='EvaluateInternships'),
    path('SubmitEvaluation/<int:report_id>/', views.SubmitEvaluation, name='SubmitEvaluation'),
    
    path('ApproveProjects/', views.ApproveProjects, name='ApproveProjects'),
    path('ApproveProjectAction/<int:pid>/<int:status>/', views.ApproveProjectAction, name='ApproveProjectAction'),
    path('VerifyMilestone/<int:mid>/<int:status>/', views.VerifyMilestone, name='VerifyMilestone'),
    path('ViewInternLogs/<int:iid>/', views.ViewInternLogs, name='ViewInternLogs'),
]
