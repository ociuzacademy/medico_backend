# urls.py
from django import views
from django.urls import path, include
from numpy import outer
from rest_framework.routers import DefaultRouter
from medicoapp.views import  *
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from . import views

schema_view = get_schema_view(
   openapi.Info(
      title="Medico App API",
      default_version='v1',
      description="API documentation for your project",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

clinic_doctor_profile_update = ClinicDoctorProfileViewSet.as_view({
    'patch': 'partial_update'
})

hospital_doctor_profile_update = HospitalDoctorProfileViewSet.as_view({
    'patch': 'partial_update'
})

# Define the router and register the viewset
router = DefaultRouter()
router.register(r'register', RegisterUserViewSet, basename='register')
router.register(r'clinic_doctors', ClinicDoctorRegisterViewSet, basename='clinic_doctors')
router.register(r'hospital_doctors', HospitalDoctorRegisterViewSet, basename='hospital_doctors')
router.register(r'clinic_doctor_timeslots', ClinicDoctorTimeSlotGroupViewSet, basename='clinic_doctor_timeslot')
router.register(r'hospital_doctor_timeslots', HospitalDoctorTimeSlotGroupViewSet, basename='hospital_doctor_timeslot')
urlpatterns = [
   path('', include(router.urls)),  # Now /api/register/ will work
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   path('login/', LoginView.as_view(), name='login'),
   path('chatbot/history/<int:user_id>/', ChatHistoryByUserAPIView.as_view(), name='chat-history-by-user'),

   path('chat/', MedicalChatAPIView.as_view(), name='medical_chat_api'),
   path('questions/', QuestionsListAPIView.as_view(), name='questions_list'),
   path('get_prediction_result/<int:user_id>/', PredictionResultAPIView.as_view(), name='get_prediction_result'),
   path('chat_download_pdf/<int:user_id>/<int:chat_id>/', ChatPDFDownloadView.as_view(), name='chat-pdf-download'),
   path('view_nearby_clinic_doctors/<int:user_id>/', views.view_nearby_clinic_doctors, name='view_nearby_clinic_doctors'),
   path('view_nearby_hospital_doctors/<int:user_id>/', views.view_nearby_hospital_doctors, name='view_nearby_hospital_doctors'),
   path('view_clinic_doctor/<int:doctor_id>/', views.view_clinic_doctor_profile, name='view_clinic_doctor_profile'),
   path('view_hospital_doctor/<int:doctor_id>/', views.view_hospital_doctor_profile, name='view_hospital_doctor_profile'),
   path('clinic-doctor/<int:doctor_id>/availability/', views.update_clinic_doctor_availability, name='update_clinic_doctor_availability'),
   path('hospital-doctor/<int:doctor_id>/availability/', views.update_hospital_doctor_availability, name='update_hospital_doctor_availability'),
   path('clinic_doctor/update/<int:pk>/', clinic_doctor_profile_update, name='clinic_doctor_profile_update'),
   path('hospital_doctor/update/<int:pk>/', hospital_doctor_profile_update, name='hospital_doctor_profile_update'),
   path('clinic/doctor/<int:doctor_id>/timeslots/', view_clinic_doctor_timeslots, name='view_clinic_doctor_timeslots'),
   path('hospital/doctor/<int:doctor_id>/timeslots/', view_hospital_doctor_timeslots, name='view_hospital_doctor_timeslots'),
   path('clinic/doctor/book-slot/', views.book_clinic_doctor_slot, name='book_clinic_doctor_slot'),
   path('hospital/doctor/book-slot/', views.book_hospital_doctor_slot, name='book_hospital_doctor_slot'),
   path('clinic/doctor/<int:doctor_id>/bookings/', views.doctor_view_booking_clinic.as_view(), name='doctor_view_booking_clinic'),
   path('hospital/doctor/<int:doctor_id>/bookings/', views.doctor_view_booking_hospital.as_view(), name='doctor_view_booking_hospital'),
   path('user/<int:user_id>/clinic/bookinKOgs/', views.user_view_booking_clinic.as_view(), name='user_view_clinic_bookings'),
   path('user/<int:user_id>/hospital/bookings/', views.user_view_booking_hospital.as_view(), name='user_view_hospital_bookings'),
   path('user-add-feedback/', views.add_clinic_doctor_feedback, name='add_clinic_doctor_feedback'),
   path('clinic/doctor/<int:doctor_id>/feedback/', views.view_clinic_doctor_feedback, name='view_clinic_doctor_feedback'),
   path('user-hospital/doctor/feedback/add/', views.add_hospital_doctor_feedback, name='add_hospital_doctor_feedback'),
   path('hospital/doctor/<int:doctor_id>/feedback/', views.view_hospital_doctor_feedback, name='view_hospital_doctor_feedback'),
   path('clinic-booking/download/<int:booking_id>/',views.download_clinic_booking_pdf,name='download_clinic_booking_pdf'),
# Hospital Booking PDF
   path('hospital-booking/download/<int:booking_id>/',views.download_hospital_booking_pdf,name='download_hospital_booking_pdf'),
]