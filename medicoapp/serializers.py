from rest_framework import serializers
from .models import   tbl_register

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = tbl_register
        fields = '__all__'


    

# class DoctorRegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = tbl_doctor_register
#         fields = '__all__'


#     def to_representation(self, instance):
#         rep = super().to_representation(instance)

#         if instance.image:
#             rep['image'] = instance.image.url  # returns "/media/..."
#         if instance.medical_id:
#             rep['medical_id'] = instance.medical_id.url

#         return rep
    
# serializers.py
# from rest_framework import serializers
# from .models import tbl_doctor_register

# class DoctorProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = tbl_doctor_register
#         fields = '__all__'
#     def to_representation(self, instance):
#         rep = super().to_representation(instance)

#         if instance.image:
#             rep['image'] = instance.image.url  # returns "/media/..."
#         if instance.medical_id:
#             rep['medical_id'] = instance.medical_id.url

#         return rep
    
# Doctor register
from rest_framework import serializers
from .models import tbl_clinic_doctor_register, tbl_hospital_doctor_register
from rest_framework import serializers
from .models import tbl_clinic_doctor_register

class ClinicDoctorRegisterSerializer(serializers.ModelSerializer):
    # ✅ remove 'available' from client input; it’ll be handled internally
    class Meta:
        model = tbl_clinic_doctor_register
        exclude = ['available']  # hide from Swagger and client

    def create(self, validated_data):
        # ✅ automatically mark doctor as available when registered
        validated_data['available'] = True
        return super().create(validated_data)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.image:
            rep['image'] = instance.image.url
        if instance.medical_id:
            rep['medical_id'] = instance.medical_id.url
        # ✅ still show availability in response (optional)
        rep['available'] = instance.available
        return rep

from rest_framework import serializers
from .models import tbl_hospital_doctor_register

class HospitalDoctorRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = tbl_hospital_doctor_register
        exclude = ['available']  # 👈 hide from Swagger input

    def create(self, validated_data):
        # 👇 Always mark new hospital doctors as available by default
        validated_data['available'] = True
        return super().create(validated_data)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.image:
            rep['image'] = instance.image.url
        if instance.medical_id:
            rep['medical_id'] = instance.medical_id.url
        rep['available'] = instance.available  # 👈 show in API response
        return rep

# serializers.py
from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()



# # serializers.py
# from rest_framework import serializers
# from .models import tbl_doctor_register

# class DoctorProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = tbl_doctor_register
#         fields = '__all__'
#     def to_representation(self, instance):
#         rep = super().to_representation(instance)

#         if instance.image:
#             rep['image'] = instance.image.url  # returns "/media/..."
#         if instance.medical_id:
#             rep['medical_id'] = instance.medical_id.url

#         return rep


#chat history serializer
# userapp/serializers.py

from rest_framework import serializers
from .models import ChatSession

class ChatHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatSession
        fields = '__all__'

from rest_framework import serializers
from .models import ChatSession
class PredictionResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatSession
        fields = ['predicted_disease', 'severity_level', 'remedy_text']


from rest_framework import serializers
# from .models import ClinicDoctorTimeSlotGroup, ClinicDoctorSubSlot
from rest_framework import serializers
from .models import ClinicDoctorTimeSlotGroup

class ClinicDoctorTimeSlotGroupSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    timeslots = serializers.ListField(
        child=serializers.CharField(), required=False  # ✅ handle list of strings
    )

    class Meta:
        model = ClinicDoctorTimeSlotGroup
        fields = ['id', 'doctor', 'doctor_name', 'date', 'start_time', 'end_time', 'timeslots']

from rest_framework import serializers
from .models import HospitalDoctorTimeSlotGroup

class HospitalDoctorTimeSlotGroupSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    timeslots = serializers.ListField(
        child=serializers.CharField(), required=False
    )  # ✅ accept list of time strings like ["10:00", "10:30"]

    class Meta:
        model = HospitalDoctorTimeSlotGroup
        fields = ['id', 'doctor', 'doctor_name', 'date', 'start_time', 'end_time', 'timeslots']






# serializers.py
from rest_framework import serializers
from .models import tbl_clinic_doctor_register

class ClinicDoctorProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = tbl_clinic_doctor_register
        fields = [
            'name', 'email', 'qualification', 'specialization', 'experience',
            'clinic_address', 'clinic_phone', 'latitude', 'longitude', 'age',
            'gender', 'place', 'image', 'medical_id'
        ]
        extra_kwargs = {
            'email': {'required': False},
        }



# serializers.py
from rest_framework import serializers
from .models import tbl_hospital_doctor_register

class HospitalDoctorProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = tbl_hospital_doctor_register
        fields = [
            'name', 'email', 'qualification', 'specialization', 'experience',
            'hospital_address', 'hospital_phone', 'latitude', 'longitude', 'age',
            'gender', 'place', 'image', 'medical_id','hospital_name'
        ]
        extra_kwargs = {
            'email': {'required': False},
        }




from rest_framework import serializers
from .models import ClinicDoctorBooking


class ClinicDoctorBookingSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)

    class Meta:
        model = ClinicDoctorBooking
        fields = [
            'id', 'user', 'user_name', 'doctor', 'doctor_name',
            'timeslot_group', 'date', 'time', 'status', 'booked_at'
        ]



from rest_framework import serializers
from .models import ClinicDoctorFeedback

class ClinicDoctorFeedbackSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)

    class Meta:
        model = ClinicDoctorFeedback
        fields = ['id', 'user', 'user_name', 'doctor', 'doctor_name', 'rating', 'comments', 'created_at']



from rest_framework import serializers
from .models import HospitalDoctorFeedback

class HospitalDoctorFeedbackSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)

    class Meta:
        model = HospitalDoctorFeedback
        fields = ['id', 'user', 'user_name', 'doctor', 'doctor_name', 'rating', 'comments', 'created_at']
