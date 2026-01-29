from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('view-users/', views.view_all_users, name='view_users'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('view_pending_doctors/', views.view_pending_doctors, name='view_pending_doctors'),

    # Clinic Doctor Actions
    path('approve_clinic_doctor/<int:doctor_id>/', views.approve_clinic_doctor, name='approve_clinic_doctor'),
    path('reject_clinic_doctor/<int:doctor_id>/', views.reject_clinic_doctor, name='reject_clinic_doctor'),

    # Hospital Doctor Actions
    path('approve_hospital_doctor/<int:doctor_id>/', views.approve_hospital_doctor, name='approve_hospital_doctor'),
    path('reject_hospital_doctor/<int:doctor_id>/', views.reject_hospital_doctor, name='reject_hospital_doctor'),

    path('view_approved_doctors/', views.view_approved_doctors, name='view_approved_doctors'),

    path('view_rejected_doctors/', views.view_rejected_doctors, name='view_rejected_doctors'),

    path('view-all-bookings/', views.view_all_bookings, name='view_all_bookings'),
    
]
