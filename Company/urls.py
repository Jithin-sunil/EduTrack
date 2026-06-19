from django.urls import path
from . import views

app_name = 'Company'

urlpatterns = [
    path('Dashboard/', views.Dashboard, name='Dashboard'),
    path('PostInternship/', views.PostInternship, name='PostInternship'),
    path('InternshipApplications/', views.InternshipApplications, name='InternshipApplications'),
    path('ApproveApplication/<int:iid>/', views.ApproveApplication, name='ApproveApplication'),
    path('RejectApplication/<int:iid>/', views.RejectApplication, name='RejectApplication'),
    path('MonitorInterns/', views.MonitorInterns, name='MonitorInterns'),
    path('ViewLogs/<int:iid>/', views.ViewLogs, name='ViewLogs'),
    path('AddLogRemark/<int:lid>/', views.AddLogRemark, name='AddLogRemark'),
]
