from django.urls import path
from . import views

app_name = 'Student'

urlpatterns = [
    path('Dashboard/', views.Dashboard, name='Dashboard'),
    path('BrowseActivities/', views.BrowseActivities, name='BrowseActivities'),
    path('RegisterActivity/<int:aid>/', views.RegisterActivity, name='RegisterActivity'),
    path('CertificateUpload/', views.CertificateUpload, name='CertificateUpload'),
    path('InternshipPortal/', views.InternshipPortal, name='InternshipPortal'),
    path('ApplyInternship/<int:iid>/', views.ApplyInternship, name='ApplyInternship'),
    path('InternshipLog/<int:iid>/', views.InternshipLog, name='InternshipLog'),
    path('InternshipReport/<int:iid>/', views.InternshipReport, name='InternshipReport'),
    
    path('ProjectSpace/', views.ProjectSpace, name='ProjectSpace'),
    
    path('Feedback/', views.Feedback, name='Feedback'),
    path('Complaint/', views.Complaint, name='Complaint'),
]
