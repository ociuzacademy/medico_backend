from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.shortcuts import redirect
from .models import tbl_admin

# Create your views here.
def index(request):
    return render(request, 'adminapp/index.html')

from django.shortcuts import render, redirect
from django.contrib import messages
  # make sure tbl_admin exists

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            admin = tbl_admin.objects.get(email=email, password=password)
            request.session['admin_id'] = admin.id
            return render(request, 'adminapp/index.html')  # on successful login
        except tbl_admin.DoesNotExist:
            messages.error(request, 'Invalid email or password')
            return render(request, 'adminapp/login.html')  # on error
    return render(request, 'adminapp/login.html')  # for GET request
from django.shortcuts import redirect

def logout_view(request):
    # Clear session data (e.g., for admin, user, or engineer)
    request.session.flush()
    return redirect('login')  # Redirect to login page after logout


from django.shortcuts import render
from medicoapp.models import  tbl_register

def view_all_users(request):
    users = tbl_register.objects.filter(role='user')  # filter by role if needed
    return render(request, 'adminapp/view_users.html', {'users': users})

from django.shortcuts import redirect, get_object_or_404


def delete_user(request, user_id):
    user = get_object_or_404(tbl_register, id=user_id)
    user.delete()
    return redirect('view_users')  # your users list page

from django.shortcuts import render
from medicoapp.models import tbl_clinic_doctor_register, tbl_hospital_doctor_register
from django.shortcuts import render, redirect, get_object_or_404

# ✅ View all pending doctors
def view_pending_doctors(request):
    clinic_pending = tbl_clinic_doctor_register.objects.filter(status='pending')
    hospital_pending = tbl_hospital_doctor_register.objects.filter(status='pending')
    return render(request, 'adminapp/view_pending_doctors.html', {
        'clinic_pending': clinic_pending,
        'hospital_pending': hospital_pending
    })


# ✅ Approve clinic doctor
def approve_clinic_doctor(request, doctor_id):
    doctor = get_object_or_404(tbl_clinic_doctor_register, id=doctor_id)
    doctor.status = 'approved'
    doctor.save()
    return redirect('view_pending_doctors')


# ✅ Reject clinic doctor
def reject_clinic_doctor(request, doctor_id):
    doctor = get_object_or_404(tbl_clinic_doctor_register, id=doctor_id)
    doctor.status = 'rejected'
    doctor.save()
    return redirect('view_pending_doctors')


# ✅ Approve hospital doctor
def approve_hospital_doctor(request, doctor_id):
    doctor = get_object_or_404(tbl_hospital_doctor_register, id=doctor_id)
    doctor.status = 'approved'
    doctor.save()
    return redirect('view_pending_doctors')


# ✅ Reject hospital doctor
def reject_hospital_doctor(request, doctor_id):
    doctor = get_object_or_404(tbl_hospital_doctor_register, id=doctor_id)
    doctor.status = 'rejected'
    doctor.save()
    return redirect('view_pending_doctors')



def view_approved_doctors(request):
    clinic_approved = tbl_clinic_doctor_register.objects.filter(status='approved')
    hospital_approved = tbl_hospital_doctor_register.objects.filter(status='approved')
    return render(request, 'adminapp/view_approved_doctors.html', {
        'clinic_approved': clinic_approved,
        'hospital_approved': hospital_approved
    })


def view_rejected_doctors(request):
    clinic_rejected = tbl_clinic_doctor_register.objects.filter(status='rejected')
    hospital_rejected = tbl_hospital_doctor_register.objects.filter(status='rejected')
    return render(request, 'adminapp/view_rejected_doctors.html', {
        'clinic_rejected': clinic_rejected,
        'hospital_rejected': hospital_rejected
    })



from django.shortcuts import render
from medicoapp.models import ClinicBooking, HospitalBooking

def view_all_bookings(request):
    clinic_bookings = ClinicBooking.objects.select_related('doctor', 'user').order_by('-created_at')
    hospital_bookings = HospitalBooking.objects.select_related('doctor', 'user').order_by('-date')

    context = {
        'clinic_bookings': clinic_bookings,
        'hospital_bookings': hospital_bookings,
    }
    return render(request, 'adminapp/view_all_bookings.html', context)
