from django.urls import path
from . import views

app_name = 'Basics'

urlpatterns = [
    path('Sum/', views.Sum, name='Sum'),
    path('Calculator/', views.Calculator, name='Calculator'),
    path('Largest/', views.Largest, name='Largest'),
    path('Ranklist/', views.Ranklist, name='Ranklist'),
    path('Salarycalculation/', views.Salarycalculation, name='Salarycalculation'),
]
