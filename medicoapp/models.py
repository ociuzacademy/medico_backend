from django.db import models
# Create your models here.
class tbl_register(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)
    address = models.TextField()
    gender = models.CharField(max_length=10)
    age = models.IntegerField()
    place = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    role= models.CharField(max_length=20, default='user')  # Default role is 'user'

    def __str__(self):
        return self.name
    

# class tbl_doctor_register(models.Model):
#     category_choices = [
#         ('hospital', 'Hospital'),
#         ('clinic', 'Clinic'),
#     ]
#     status_choices = [
#         ('pending', 'Pending'),
#         ('approved', 'Approved'),
#         ('rejected', 'Rejected'),
#     ]
#     name = models.CharField(max_length=100)
#     email = models.EmailField(max_length=100, unique=True)
#     password = models.CharField(max_length=100)
#     phone = models.CharField(max_length=15)
#     address = models.TextField(null=True, blank=True)
#     specialization = models.CharField(max_length=100,null=True, blank=True)
#     experience = models.IntegerField(null=True, blank=True)
#     clinic_address = models.TextField(null=True, blank=True)
#     hospital_address = models.TextField(null=True, blank=True)
#     latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
#     longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
#     role = models.CharField(max_length=20, default='doctor')  # Default role is 'doctor'
#     category = models.CharField(max_length=20, choices=category_choices, default='clinic')
#     age = models.IntegerField(null=True, blank=True)
#     place = models.CharField(max_length=100, null=True, blank=True)
#     gender = models.CharField(max_length=10, null=True, blank=True)
#     image = models.ImageField(upload_to='doctor_images/', null=True, blank=True)
#     medical_id = models.ImageField(upload_to='medical_ids/', null=True, blank=True)
#     status = models.CharField(max_length=20, choices=status_choices, default='pending')
#     available = models.BooleanField(default=True)
#     def __str__(self):
#         return self.name  



# class HealthChatSession(models.Model):
#     user = models.ForeignKey(tbl_register, on_delete=models.CASCADE)
#     question_number = models.IntegerField(default=1)
#     q1_answer = models.TextField(blank=True, null=True)
#     q2_answer = models.TextField(blank=True, null=True)
#     q3_answer = models.TextField(blank=True, null=True)
#     q4_answer = models.TextField(blank=True, null=True)
#     q5_answer = models.TextField(blank=True, null=True)

#     predicted_disease = models.TextField(blank=True, null=True)  # <-- changed here
#     severity_level = models.CharField(max_length=100, blank=True, null=True)
#     completed = models.BooleanField(default=False)

#     def __str__(self):
#         return f"ChatSession for {self.user.name} - Completed: {self.completed}"


class ChatSession(models.Model):
    user = models.ForeignKey(tbl_register, on_delete=models.CASCADE)
    question_number = models.IntegerField(default=1)
    q1_answer = models.TextField(blank=True, null=True)
    q2_answer = models.TextField(blank=True, null=True)
    q3_answer = models.TextField(blank=True, null=True)
    q4_answer = models.TextField(blank=True, null=True)
    q5_answer = models.TextField(blank=True, null=True)

    predicted_disease = models.TextField(blank=True, null=True)  # <-- changed here
    severity_level = models.CharField(max_length=100, blank=True, null=True)
    completed = models.BooleanField(default=False)
    asked_remedy = models.BooleanField(default=False)
    given_remedy = models.BooleanField(default=False)
    remedy_text = models.TextField(blank=True, null=True)


    def __str__(self):
        return f"ChatSession for {self.user.name} - Completed: {self.completed}"
    



#Doctor
from django.db import models

# ✅ Clinic Doctor Model
class tbl_clinic_doctor_register(models.Model):
    status_choices = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100, null=True, blank=True)
    specialization = models.CharField(max_length=100, null=True, blank=True)
    experience = models.IntegerField(null=True, blank=True)
    clinic_name = models.CharField(max_length=100, null=True, blank=True)
    clinic_address = models.TextField(null=True, blank=True)
    clinic_phone = models.CharField(max_length=15, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    role = models.CharField(max_length=30, default='clinic_doctor')
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    place = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='clinic_doctor_images/', null=True, blank=True)
    medical_id = models.ImageField(upload_to='clinic_medical_ids/', null=True, blank=True)
    available = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=status_choices, default='pending')

    def __str__(self):
        return self.name


# ✅ Hospital Doctor Model
class tbl_hospital_doctor_register(models.Model):
    status_choices = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100, null=True, blank=True)
    specialization = models.CharField(max_length=100, null=True, blank=True)
    experience = models.IntegerField(null=True, blank=True)
    hospital_name = models.CharField(max_length=100, null=True, blank=True)
    hospital_address = models.TextField(null=True, blank=True)
    hospital_phone = models.CharField(max_length=15, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    role = models.CharField(max_length=30, default='hospital_doctor')
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    place = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='hospital_doctor_images/', null=True, blank=True)
    medical_id = models.ImageField(upload_to='hospital_medical_ids/', null=True, blank=True)
    available = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=status_choices, default='pending')

    def __str__(self):
        return self.name
from django.db import models
# from django.contrib.postgres.fields import ArrayField
from .models import tbl_clinic_doctor_register

class ClinicDoctorTimeSlotGroup(models.Model):
    doctor = models.ForeignKey(tbl_clinic_doctor_register, on_delete=models.CASCADE, related_name='slot_groups')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    timeslots = models.JSONField(default=list, blank=True)  # ✅ Store list of times like ["10:00", "10:30"]

    def __str__(self):
        return f"{self.doctor.name} - {self.date} ({self.start_time} to {self.end_time})"

from django.db import models
from django.db import models

class HospitalDoctorTimeSlotGroup(models.Model):
    doctor = models.ForeignKey('tbl_hospital_doctor_register', on_delete=models.CASCADE, related_name='slot_groups')
    date = models.DateField()
    start_time = models.TimeField()   # doctor’s working start time
    end_time = models.TimeField()     # doctor’s working end time
    timeslots = models.JSONField(default=list, blank=True)  # ✅ store list of selected times

    def __str__(self):
        return f"{self.doctor.name} - {self.date} ({self.start_time} to {self.end_time})"



from django.db import models
from .models import tbl_register, tbl_clinic_doctor_register, ClinicDoctorTimeSlotGroup

class ClinicDoctorBooking(models.Model):
    user = models.ForeignKey(tbl_register, on_delete=models.CASCADE, related_name='clinic_bookings')
    doctor = models.ForeignKey(tbl_clinic_doctor_register, on_delete=models.CASCADE, related_name='bookings')
    timeslot_group = models.ForeignKey(ClinicDoctorTimeSlotGroup, on_delete=models.CASCADE, related_name='bookings')
    date = models.DateField()
    time = models.CharField(max_length=10)  # e.g. "10:00"

    is_booked = models.BooleanField(default=True)  # always True once booked
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} booked {self.doctor.name} on {self.date} at {self.time}"




from django.db import models
from .models import tbl_register, tbl_hospital_doctor_register, HospitalDoctorTimeSlotGroup

class HospitalDoctorBooking(models.Model):
    user = models.ForeignKey(tbl_register, on_delete=models.CASCADE)
    doctor = models.ForeignKey(tbl_hospital_doctor_register, on_delete=models.CASCADE)
    timeslot_group = models.ForeignKey(HospitalDoctorTimeSlotGroup, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default='booked')  # optional

    def __str__(self):
        return f"{self.user.name} booked {self.doctor.name} at {self.time} on {self.date}"





from django.db import models
from .models import tbl_register, tbl_clinic_doctor_register, ClinicDoctorTimeSlotGroup

class TblClinicDoctorBooking(models.Model):
    user = models.ForeignKey(tbl_register, on_delete=models.CASCADE, related_name='clinic_doctor_bookings')
    doctor = models.ForeignKey(tbl_clinic_doctor_register, on_delete=models.CASCADE, related_name='clinic_bookings')
    timeslot_group = models.ForeignKey(ClinicDoctorTimeSlotGroup, on_delete=models.CASCADE, related_name='clinic_bookings')
    date = models.DateField()
    time = models.CharField(max_length=10)  # e.g. "10:00"

    is_booked = models.BooleanField(default=True)  # always True once booked
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} booked {self.doctor.name} on {self.date} at {self.time}"




from django.db import models
from .models import tbl_register, tbl_hospital_doctor_register, HospitalDoctorTimeSlotGroup

class TblHospitalDoctorBooking(models.Model):
    user = models.ForeignKey(tbl_register, on_delete=models.CASCADE)
    doctor = models.ForeignKey(tbl_hospital_doctor_register, on_delete=models.CASCADE)
    timeslot_group = models.ForeignKey(HospitalDoctorTimeSlotGroup, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default='booked')  # optional

    def __str__(self):
        return f"{self.user.name} booked {self.doctor.name} at {self.time} on {self.date}"











class ClinicBooking(models.Model):
    user = models.ForeignKey(tbl_register, on_delete=models.CASCADE, related_name='clinic_bookings1')
    doctor = models.ForeignKey(tbl_clinic_doctor_register, on_delete=models.SET_NULL, null=True, blank=True, related_name='cbookings')
    timeslot_group = models.ForeignKey(ClinicDoctorTimeSlotGroup, on_delete=models.CASCADE, related_name='cbookings')
    date = models.DateField()
    time = models.CharField(max_length=10)
    is_booked = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.doctor:
            return f"{self.user.name} booked {self.doctor.name} on {self.date} at {self.time}"
        return f"{self.user.name} booked (Doctor deleted) on {self.date} at {self.time}"



class HospitalBooking(models.Model):
    user = models.ForeignKey(tbl_register, on_delete=models.CASCADE)
    doctor = models.ForeignKey(tbl_hospital_doctor_register, on_delete=models.SET_NULL, null=True, blank=True)
    timeslot_group = models.ForeignKey(HospitalDoctorTimeSlotGroup, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default='booked')
    is_booked = models.BooleanField(default=True)

    def __str__(self):
        if self.doctor:
            return f"{self.user.name} booked {self.doctor.name} at {self.time} on {self.date}"
        return f"{self.user.name} booked (Doctor deleted) at {self.time} on {self.date}"




class ClinicDoctorFeedback(models.Model):
    user = models.ForeignKey(tbl_register, on_delete=models.CASCADE)
    doctor = models.ForeignKey(tbl_clinic_doctor_register, on_delete=models.CASCADE)
    rating = models.IntegerField()  # 1 to 5
    comments = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} → {self.doctor.name} ({self.rating}⭐)"





class HospitalDoctorFeedback(models.Model):
    user = models.ForeignKey(tbl_register, on_delete=models.CASCADE, related_name='hospital_feedbacks')
    doctor = models.ForeignKey('tbl_hospital_doctor_register', on_delete=models.CASCADE, related_name='hospital_feedbacks')
    rating = models.IntegerField()  # e.g., 1–5 stars
    comments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.user.name} for {self.doctor.name}"
