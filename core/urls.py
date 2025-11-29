from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('patient/<str:p_id>/', views.patient_portal, name='patient_portal'),
]
