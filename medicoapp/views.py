# views.py
from medico.settings import BASE_DIR
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
# from .models import  ClinicBooking, HospitalBooking, TblClinicDoctorBooking, TblHospitalDoctorBooking, tbl_register
from .serializers import  RegisterSerializer
from rest_framework.views import APIView
from .models import *

class RegisterUserViewSet(viewsets.ModelViewSet):
    queryset = tbl_register.objects.all()
    serializer_class = RegisterSerializer

# class DoctorRegisterViewSet(viewsets.ModelViewSet):
#     queryset = tbl_doctor_register.objects.filter(role='doctor')
#     serializer_class = DoctorRegisterSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        

#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)
#         return Response(serializer.data)
    



from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import tbl_clinic_doctor_register, tbl_hospital_doctor_register
from .serializers import ClinicDoctorRegisterSerializer, HospitalDoctorRegisterSerializer,LoginSerializer


#  Clinic Doctor ViewSet
class ClinicDoctorRegisterViewSet(viewsets.ModelViewSet):
    queryset = tbl_clinic_doctor_register.objects.all()
    serializer_class = ClinicDoctorRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


#  Hospital Doctor ViewSet
class HospitalDoctorRegisterViewSet(viewsets.ModelViewSet):
    queryset = tbl_hospital_doctor_register.objects.all()
    serializer_class = HospitalDoctorRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer
from .models import tbl_clinic_doctor_register, tbl_hospital_doctor_register, tbl_register
class LoginView(APIView):
    """
    Login endpoint for:
    - Clinic Doctor
    - Hospital Doctor
    - Normal User (tbl_register)
    """

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        # --- Clinic Doctor Login ---
        clinic_doc = tbl_clinic_doctor_register.objects.filter(email=email, password=password).first()
        if clinic_doc:
            if clinic_doc.status != 'approved':
                return Response(
                    {'message': 'Clinic doctor account not approved yet. Please wait for admin approval.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            return Response({
                'id': clinic_doc.id,
                'name': clinic_doc.name,
                'email': clinic_doc.email,
                'password': clinic_doc.password,
                'phone': clinic_doc.clinic_phone,
                'role': clinic_doc.role,
                
            }, status=status.HTTP_200_OK)

        # --- Hospital Doctor Login ---
        hospital_doc = tbl_hospital_doctor_register.objects.filter(email=email, password=password).first()
        if hospital_doc:
            if hospital_doc.status != 'approved':
                return Response(
                    {'message': 'Hospital doctor account not approved yet. Please wait for admin approval.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            return Response({
                'id': hospital_doc.id,
                'name': hospital_doc.name,
                'email': hospital_doc.email,
                'phone': hospital_doc.hospital_phone,
                'role': hospital_doc.role,
                'password': hospital_doc.password,
            }, status=status.HTTP_200_OK)

        # --- Normal User Login ---
        user = tbl_register.objects.filter(email=email, password=password).first()
        if user:
            return Response({
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'password': user.password,
                'phone':user.phone,
                'role': user.role
            }, status=status.HTTP_200_OK)

        # --- Invalid Credentials ---
        return Response({'message': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)



# # views.py
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import tbl_doctor_register
# from .serializers import DoctorProfileSerializer

# class DoctorProfileView(APIView):
#     def get(self, request, pk):
#         try:
#             doctor = tbl_doctor_register.objects.get(pk=pk)
#             serializer = DoctorProfileSerializer(doctor, context={'request': request})
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except tbl_doctor_register.DoesNotExist:
#             return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)

# # views.py
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.parsers import MultiPartParser, FormParser
# from .models import tbl_doctor_register
# from .serializers import DoctorProfileSerializer

# class DoctorProfileUpdateView(APIView):
#     parser_classes = [MultiPartParser, FormParser]

#     def put(self, request, pk):
#         try:
#             doctor = tbl_doctor_register.objects.get(pk=pk)
#         except tbl_doctor_register.DoesNotExist:
#             return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)

#         serializer = DoctorProfileSerializer(doctor, data=request.data, partial=True)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.conf import settings
# import google.generativeai as genai
# import logging

# # Configure logger
# logger = logging.getLogger(__name__)

# # Initialize Gemini with API key
# genai.configure(api_key=settings.GOOGLE_API_KEY)

# # Load Gemini model
# model = genai.GenerativeModel("gemini-1.5-flash")


# class ChatbotAPIView(APIView):
#     """
#     Gemini chatbot API: Greets and asks health-related questions on first contact,
#     and responds via AI afterward.
#     """

#     def post(self, request):
#         user_message = request.data.get("message", "").strip()

#         if not user_message:
#             logger.warning("Empty message received.")
#             return Response(
#                 {"error": "Please provide a message."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # Respond with predefined medical questions on initial greeting
#         if user_message.lower() in ["hi", "hello", "start"]:
#             bot_reply = (
#                 "👋 Hello! I'm here to assist with your medical concerns.\n\n"
#                 "Please answer the following questions to help me understand your situation better:\n"
#                 "1. What disease or condition are you experiencing?\n"
#                 "2. What symptoms do you have? (e.g., fever, nausea, pain, fatigue, etc.)\n"
#                 "3. How long have you had these symptoms?\n"
#                 "4. Are you taking any medications currently?\n"
#                 "5. Do you have any past medical history or known allergies?\n\n"
#                 "Once you respond, I can guide you better 😊"
#             )
#             logger.info("Initial greeting triggered.")
#             return Response({"reply": bot_reply}, status=status.HTTP_200_OK)

#         try:
#             # Start a new chat session
#             chat = model.start_chat(history=[])
#             response = chat.send_message(user_message)

#             # Keep line breaks as-is (no <br> conversion)
#             bot_reply = response.text.strip()

#             logger.info(f"User: {user_message} | Bot: {bot_reply}")

#             return Response({"reply": bot_reply}, status=status.HTTP_200_OK)

#         except genai.types.BlockedPromptException as e:
#             logger.warning(f"Blocked by safety filters: {e}")
#             return Response(
#                 {"error": "Your message was blocked due to safety filters."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         except genai.types.StopCandidateException as e:
#             logger.warning(f"Stopped early: {e}")
#             return Response(
#                 {"error": "The model stopped before completing the response."},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )

#         except Exception as e:
#             logger.error("Internal server error:", exc_info=True)
#             return Response(
#                 {"error": "An internal error occurred. Please try again later."},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )
# views.py

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.conf import settings
# from .models import tbl_register
# import google.generativeai as genai
# import logging

# # Configure logger
# logger = logging.getLogger(__name__)
# genai.configure(api_key=settings.GOOGLE_API_KEY)
# model = genai.GenerativeModel("gemini-1.5-flash")



# userapp/views.py
from rest_framework.generics import ListAPIView
from .models import ChatSession
from .serializers import ChatHistorySerializer

class ChatHistoryByUserAPIView(ListAPIView):
    serializer_class = ChatHistorySerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return ChatSession.objects.filter(user_id=user_id)
    


class QuestionsListAPIView(APIView):
    def get(self, request):
        questions = [
            "What symptom did you experience first?",
            "What symptom did you experience next?",
            "When did these symptoms start?",
            "How severe are the symptoms (mild/moderate/severe)?",
            "Do you have any pre-existing conditions?"
        ]
        return Response({"questions": questions})

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ChatSession
from .serializers import PredictionResultSerializer

class PredictionResultAPIView(APIView):
    def get(self, request, user_id):
        try:
            session = ChatSession.objects.filter(user_id=user_id).latest('id')
            data = {
                'severity_level': session.severity_level,
                'predicted_disease': session.predicted_disease,
                'remedy_text': session.remedy_text,
            }
            return Response(data, status=status.HTTP_200_OK)
        except ChatSession.DoesNotExist:
            return Response({'error': 'No session found for this user'}, status=status.HTTP_404_NOT_FOUND)
        
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
# Assuming 'models.py' and 'tbl_register' are correctly imported or defined
from .models import ChatSession
import google.generativeai as genai
import json # Import the json module for parsing structured data
import re   # Import re for cleaning up potential markdown wrappers

# Configure Gemini
# NOTE: Ensure GOOGLE_API_KEY is correctly set in settings.py
genai.configure(api_key=settings.GOOGLE_API_KEY)
# Using a faster, capable model for chat/text tasks
# Corrected code in views.py
model = genai.GenerativeModel("gemini-2.5-flash")

GREETINGS = ["hi", "hello", "hey", "good morning", "good evening", "good afternoon"]
# REMEDY_TRIGGERS logic has been simplified in the remedy phase below
# to auto-generate remedies for 'Low' severity
# REMEDY_TRIGGERS = ["next"] 

class MedicalChatAPIView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        message = request.data.get("message", "").strip().lower()

        if not user_id or not message:
            return Response({"error": "Missing user_id or message"}, status=status.HTTP_400_BAD_REQUEST)

        # 1. Get or Create Session
        session = ChatSession.objects.filter(user_id=user_id, completed=False).order_by('-id').first()

        if not session:
            # Assuming tbl_register can be accessed by user_id
            try:
                # You need to ensure tbl_register is accessible,
                # For safety, let's assume session creation works if user_id is valid.
                session = ChatSession.objects.create(user_id=user_id)
            except Exception as e:
                 # Better error handling for missing user
                 return Response({"error": f"Invalid user_id or issue creating session: {e}"}, status=status.HTTP_400_BAD_REQUEST)

        # --- Remedy Phase (Simplified: We'll rely on the main prediction logic to auto-generate remedies) ---
        # The original logic for 'next' trigger is removed for a cleaner flow:
        # If severity is 'Low', we will provide the remedy immediately after prediction.
        
        # 2. Question Flow
        reply = None
        
        if not session.q1_answer and message in GREETINGS:
            reply = "Please tell me what symptom did you experience first?"
        
        elif not session.q1_answer and reply is None:
            session.q1_answer = message
            reply = "What symptom did you experience next?"
        
        elif not session.q2_answer and reply is None:
            session.q2_answer = message
            reply = "When did these symptoms start?"
        
        elif not session.q3_answer and reply is None:
            session.q3_answer = message
            reply = "How severe are the symptoms (mild/moderate/severe)?"
        
        elif not session.q4_answer and reply is None:
            session.q4_answer = message
            reply = "Do you have any pre-existing conditions?"
        
        elif not session.q5_answer and reply is None:
            session.q5_answer = message
            session.completed = True
            reply = None # Signal that the next step is prediction
        
        elif session.completed and not session.predicted_disease:
            # Prediction phase logic will run next
            pass
        
        elif session.completed and session.predicted_disease:
            # Already completed and predicted, proceed to final response
            pass
        
        else:
            # Handle user messaging after completion if reply is still None
            reply = "You have already completed the symptom assessment. Please wait for the prediction, or start a new session."

        session.save()

        # 3. Prediction Phase (The critical, corrected part)
        if session.completed and not session.predicted_disease:
            
            combined_input = f"""Patient Symptom Report:
1. First Symptom: {session.q1_answer}
2. Next Symptom: {session.q2_answer}
3. Start Time: {session.q3_answer}
4. Patient Reported Severity (to confirm): {session.q4_answer}
5. Pre-existing Conditions: {session.q5_answer}

Based on this data, act as a diagnostic assistant and determine the **Most Likely Disease** and the **Recommended Severity Level** (must be one of: **High**, **Medium**, or **Low**).

**CRITICAL INSTRUCTION**: Your response MUST be a clean JSON object with two keys: "disease" and "severity". Do not include any other text, explanation, or markdown formatting (like ```json) outside of the JSON object itself.
Example format: {{"disease": "Common Cold", "severity": "Low"}}
"""
            chat = model.start_chat(history=[])
            try:
                gemini_response = chat.send_message(combined_input)
                result_text = gemini_response.text.strip()
                
                # Use regex to clean up potential markdown wrappers (e.g., ```json...```)
                json_match = re.search(r"\{.*\}", result_text, re.DOTALL)
                
                if json_match:
                    json_string = json_match.group(0)
                    prediction_data = json.loads(json_string)
                    
                    predicted_disease = prediction_data.get("disease", "Prediction Failed")
                    raw_severity = prediction_data.get("severity", "Unknown").lower()

                    # Normalize the AI's predicted severity
                    if "high" in raw_severity or "severe" in raw_severity:
                        severity = "High"
                    elif "medium" in raw_severity or "moderate" in raw_severity:
                        severity = "Medium"
                    elif "low" in raw_severity or "mild" in raw_severity:
                        severity = "Low"
                    else:
                        severity = "Unknown"

                    session.predicted_disease = predicted_disease
                    session.severity_level = severity
                else:
                    # Fallback if AI doesn't return clean JSON
                    session.predicted_disease = f"AI Prediction Failed (Bad Format): {result_text[:50]}..."
                    session.severity_level = "Unknown"
            
            except json.JSONDecodeError as e:
                # Handle cases where the model returns invalid JSON
                session.predicted_disease = f"AI Prediction Failed (JSON Error: {e})"
                session.severity_level = "Unknown"
            except Exception as e:
                 # Catch other potential errors
                 session.predicted_disease = f"An unexpected error occurred: {e}"
                 session.severity_level = "Unknown"
            
            session.save()

        # 4. Final Response (After question flow or prediction)
        if session.completed and session.predicted_disease:
            
            # --- Remedy Generation (Auto-generate for Low severity) ---
            remedy_text = session.remedy_text
            
            if session.severity_level == "Low" and not session.given_remedy:
                remedy_prompt = f"""
You are a healthcare assistant. The user has been predicted with this mild condition: **{session.predicted_disease}**.
Please suggest safe and helpful home remedies they can try for mild symptoms. Give 5 to 7 concise, practical suggestions. Avoid medications. Use natural or home-based advice. Return in bullet points.
"""
                chat = model.start_chat(history=[])
                ai_remedy_response = chat.send_message(remedy_prompt)
                remedy_text = ai_remedy_response.text.strip()

                session.asked_remedy = True
                session.given_remedy = True
                session.remedy_text = remedy_text
                session.save()
            
            # --- Construct Final Output ---
            prediction_reply = f"Based on your symptoms, the most likely condition is **{session.predicted_disease}** with a severity level of **{session.severity_level}**."

            if session.severity_level in ["Medium", "High"]:
                prediction_reply += "\n\n⚠️ **Warning**: Given the predicted severity, please consider consulting a healthcare professional immediately."

            response_data = {
                "reply": prediction_reply,
                "completed": True,
                "summary": {
                    "answers": {
                        "First Symptom": session.q1_answer,
                        "Next Symptom": session.q2_answer,
                        "Start Time": session.q3_answer,
                        "Severity Reported": session.q4_answer,
                        "Pre-existing Conditions": session.q5_answer,
                    },
                    "prediction": session.predicted_disease,
                    "severity": session.severity_level
                }
            }
            
            if session.severity_level == "Low" and session.given_remedy:
                 response_data["remedy"] = remedy_text
                 response_data["reply"] += f"\n\nHere are some home remedies for mild relief:\n\n{remedy_text}"


            return Response(response_data)

        # 5. Return to User for Next Question
        if reply is not None:
             return Response({"reply": reply, "completed": False})
        
        # Final catch-all for a completed session that didn't go into the final response block
        if session.completed and not session.predicted_disease:
             return Response({"reply": "Processing your symptoms for a diagnosis...", "completed": False})

        # Should not be reached, but as a fallback
        return Response({"reply": "Session issue or unexpected state. Please try again or refresh.", "completed": False})
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from .models import tbl_doctor_register

# class CategoryChoicesAPIView(APIView):
#     def get(self, request):
#         choices = dict(tbl_doctor_register.category_choices)
#         return Response({"category_choices": choices}, status=status.HTTP_200_OK)


        
from django.http import FileResponse, Http404
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from io import BytesIO
from .models import ChatSession

class ChatPDFDownloadView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id, chat_id):
        try:
            chat = ChatSession.objects.get(user_id=user_id, id=chat_id)  # ✅ Use id instead of chat_id
        except ChatSession.DoesNotExist:
            raise Http404("Chat not found")

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []

        elements.append(Paragraph("Medico Prediction Pdf", styles['Title']))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"<b>User Name:</b> {chat.user.name}", styles['Normal']))
        elements.append(Spacer(1, 12))

        elements.append(Paragraph(f"<b>Predicted Disease:</b> {chat.predicted_disease}", styles['Normal']))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"<b>Severity Level:</b> {chat.severity_level}", styles['Normal']))

        if chat.remedy_text:
            elements.append(Spacer(1, 12))
            elements.append(Paragraph("<b>Remedies:</b>", styles['Normal']))
            for line in chat.remedy_text.split('\n'):
                elements.append(Paragraph(line.strip(), styles['Normal']))

        doc.build(elements)
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=f"chat_{chat.id}.pdf")




from rest_framework import viewsets
from .models import ClinicDoctorTimeSlotGroup
from .serializers import ClinicDoctorTimeSlotGroupSerializer

class ClinicDoctorTimeSlotGroupViewSet(viewsets.ModelViewSet):
    queryset = ClinicDoctorTimeSlotGroup.objects.all().order_by('-date')
    serializer_class = ClinicDoctorTimeSlotGroupSerializer




from rest_framework import viewsets
from .models import HospitalDoctorTimeSlotGroup
from .serializers import HospitalDoctorTimeSlotGroupSerializer

class HospitalDoctorTimeSlotGroupViewSet(viewsets.ModelViewSet):
    queryset = HospitalDoctorTimeSlotGroup.objects.all().order_by('-date')
    serializer_class = HospitalDoctorTimeSlotGroupSerializer




from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import tbl_clinic_doctor_register, tbl_register
from .serializers import ClinicDoctorRegisterSerializer

@api_view(['GET'])
def view_nearby_clinic_doctors(request, user_id):
    """
    View nearby clinic doctors based on 'place' (not location coordinates).
    Only approved and available doctors will be shown.
    """
    try:
        user = tbl_register.objects.get(id=user_id)
    except tbl_register.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    if not user.place:
        return Response({"error": "User place not available"}, status=400)

    # ✅ Filter doctors with same place, approved, and available
    doctors = tbl_clinic_doctor_register.objects.filter(
        place__iexact=user.place,  # case-insensitive match
        status='approved',
        available=True
    )

    # ✅ Build response list
    nearby_doctors = []
    for doctor in doctors:
        nearby_doctors.append({
            "id": doctor.id,
            "name": doctor.name,
            "qualification": doctor.qualification,
            "specialization": doctor.specialization,
            "experience": doctor.experience,
            "clinic_name": doctor.clinic_name,
            "clinic_address": doctor.clinic_address,
            "clinic_phone": doctor.clinic_phone,
            "place": doctor.place,
            "available": doctor.available,
            "status": doctor.status,
            "image": doctor.image.url if doctor.image else None,
        })

    if not nearby_doctors:
        return Response({"message": "No available doctors found in your place."}, status=200)

    return Response({"nearby_clinic_doctors": nearby_doctors})


from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import tbl_register, tbl_hospital_doctor_register


@api_view(['GET'])
def view_nearby_hospital_doctors(request, user_id):
    """
    Get all approved and available hospital doctors 
    who are in the same place as the user.
    """
    try:
        user = tbl_register.objects.get(id=user_id)
    except tbl_register.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    if not user.place:
        return Response({"error": "User place not available"}, status=400)

    # ✅ Only approved & available doctors in the same place
    doctors = tbl_hospital_doctor_register.objects.filter(
        status='approved', available=True, place__iexact=user.place
    )

    if not doctors.exists():
        return Response({"message": "No nearby hospital doctors found in your area."}, status=200)

    nearby_doctors = []
    for doctor in doctors:
        nearby_doctors.append({
            "id": doctor.id,
            "name": doctor.name,
            "qualification": doctor.qualification,
            "specialization": doctor.specialization,
            "experience": doctor.experience,
            "phone": doctor.hospital_phone,
            "hospital_name": doctor.hospital_name,
            "hospital_address": doctor.hospital_address,
            "place": doctor.place,
            "available": doctor.available,
            "image": doctor.image.url if doctor.image else None,
            "status": doctor.status,
        })

    return Response({"nearby_hospital_doctors": nearby_doctors})




from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import tbl_clinic_doctor_register,tbl_hospital_doctor_register
from .serializers import ClinicDoctorRegisterSerializer, HospitalDoctorRegisterSerializer

@api_view(['GET'])
def view_clinic_doctor_profile(request, doctor_id):
    try:
        doctor = tbl_clinic_doctor_register.objects.get(id=doctor_id)
    except tbl_clinic_doctor_register.DoesNotExist:
        return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ClinicDoctorRegisterSerializer(doctor)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def view_hospital_doctor_profile(request, doctor_id):
    try:
        doctor = tbl_hospital_doctor_register.objects.get(id=doctor_id)
    except tbl_hospital_doctor_register.DoesNotExist:
        return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = HospitalDoctorRegisterSerializer(doctor)
    return Response(serializer.data, status=status.HTTP_200_OK)






from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import tbl_clinic_doctor_register,tbl_hospital_doctor_register

@api_view(['POST'])
def update_clinic_doctor_availability(request, doctor_id):
    try:
        doctor = tbl_clinic_doctor_register.objects.get(id=doctor_id)
    except tbl_clinic_doctor_register.DoesNotExist:
        return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)
    
    available = request.data.get('available')

    if available is None:
        return Response({"error": "Availability value required (true/false)"}, status=status.HTTP_400_BAD_REQUEST)

    # Convert to boolean
    if isinstance(available, str):
        available = available.lower() in ['true', '1', 'yes']

    doctor.available = available
    doctor.save()

    return Response({
        "message": "Availability updated successfully",
        "doctor_id": doctor.id,
        "available": doctor.available
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
def update_hospital_doctor_availability(request, doctor_id):
    try:
        doctor = tbl_hospital_doctor_register.objects.get(id=doctor_id)
    except tbl_hospital_doctor_register.DoesNotExist:
        return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)
    
    available = request.data.get('available')

    if available is None:
        return Response({"error": "Availability value required (true/false)"}, status=status.HTTP_400_BAD_REQUEST)

    # Convert to boolean
    if isinstance(available, str):
        available = available.lower() in ['true', '1', 'yes']

    doctor.available = available
    doctor.save()

    return Response({
        "message": "Availability updated successfully",
        "doctor_id": doctor.id,
        "available": doctor.available
    }, status=status.HTTP_200_OK)





# views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import tbl_clinic_doctor_register
from .serializers import ClinicDoctorProfileUpdateSerializer

class ClinicDoctorProfileViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for updating clinic doctor profiles.
    """

    def partial_update(self, request, pk=None):
        try:
            doctor = tbl_clinic_doctor_register.objects.get(pk=pk)
        except tbl_clinic_doctor_register.DoesNotExist:
            return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ClinicDoctorProfileUpdateSerializer(doctor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





# views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import tbl_hospital_doctor_register
from .serializers import HospitalDoctorProfileUpdateSerializer

class HospitalDoctorProfileViewSet(viewsets.ViewSet):
    """
    A ViewSet for updating hospital doctor profiles (partial or full updates).
    """

    def partial_update(self, request, pk=None):
        try:
            doctor = tbl_hospital_doctor_register.objects.get(pk=pk)
        except tbl_hospital_doctor_register.DoesNotExist:
            return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = HospitalDoctorProfileUpdateSerializer(doctor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import ClinicBooking, ClinicDoctorTimeSlotGroup, tbl_register, tbl_clinic_doctor_register


# ✅ View all available time slots for a doctor
@api_view(['GET'])
def view_clinic_doctor_timeslots(request, doctor_id):
    try:
        groups = ClinicDoctorTimeSlotGroup.objects.filter(doctor_id=doctor_id).order_by('date')

        if not groups.exists():
            return Response({"message": "No time slots found for this doctor."}, status=status.HTTP_404_NOT_FOUND)

        result = []
        for group in groups:
            booked_times = list(
                ClinicBooking.objects.filter(
                    doctor_id=doctor_id,
                    date=group.date
                ).values_list('time', flat=True)
            )

            # Normalize booked times (e.g. "10:00:00" → "10:00")
            booked_times = [t[:5] for t in booked_times]

            result.append({
                "id": group.id,
                "doctor": group.doctor.id,
                "doctor_name": group.doctor.name,
                "date": group.date,
                "start_time": group.start_time.strftime("%H:%M:%S"),
                "end_time": group.end_time.strftime("%H:%M:%S"),
                "timeslots": [
                    {"time": t, "is_booked": t in booked_times}
                    for t in group.timeslots
                ],
            })

        return Response(result, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import ClinicBooking, ClinicDoctorTimeSlotGroup, tbl_register, tbl_clinic_doctor_register


@api_view(['POST'])
def book_clinic_doctor_slot(request):
    """
    Book a time slot for a clinic doctor.
    """
    data = request.data
    try:
        user = tbl_register.objects.get(id=data['user'])
        doctor = tbl_clinic_doctor_register.objects.get(id=data['doctor'])
        timeslot_group = ClinicDoctorTimeSlotGroup.objects.get(id=data['timeslot_group'])
    except (tbl_register.DoesNotExist, tbl_clinic_doctor_register.DoesNotExist, ClinicDoctorTimeSlotGroup.DoesNotExist):
        return Response({"error": "Invalid doctor, user, or timeslot group."}, status=404)

    # ✅ Directly use the JSONField list
    timeslots = timeslot_group.timeslots
    if data['time'] not in timeslots:
        return Response({"error": "Invalid time slot."}, status=400)

    # ✅ Check if already booked
    if ClinicBooking.objects.filter(
        doctor=doctor,
        date=data['date'],
        time=data['time'],
        is_booked=True
    ).exists():
        return Response({"error": "This time slot is already booked."}, status=400)

    # ✅ Create booking
    booking = ClinicBooking.objects.create(
        user=user,
        doctor=doctor,
        timeslot_group=timeslot_group,
        date=data['date'],
        time=data['time'],
        is_booked=True
    )
    return Response({
        "message": "Slot booked successfully!",
        "booking_id": booking.id,
        "doctor": doctor.name,
        "date": data['date'],
        "time": data['time']
    }, status=201)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import (
    tbl_hospital_doctor_register,
    HospitalBooking,
    HospitalDoctorTimeSlotGroup,
    tbl_register
)

# ✅ View all available hospital doctor time slots
@api_view(['GET'])
def view_hospital_doctor_timeslots(request, doctor_id):
    """
    Get all time slot groups for a hospital doctor with booking info.
    """
    try:
        groups = HospitalDoctorTimeSlotGroup.objects.filter(doctor_id=doctor_id).order_by('date')

        if not groups.exists():
            return Response({"message": "No time slots found for this doctor."}, status=status.HTTP_404_NOT_FOUND)

        result = []
        for group in groups:
            # ✅ Already booked times for that date
            booked_times = list(
                HospitalBooking.objects.filter(
                    doctor_id=doctor_id,
                    date=group.date
                ).values_list('time', flat=True)
            )

            # Normalize booked times (e.g. "10:00:00" → "10:00")
            booked_times = [t[:5] for t in booked_times]

            result.append({
                "id": group.id,
                "doctor": group.doctor.id,
                "doctor_name": group.doctor.name,
                "date": group.date,
                "start_time": group.start_time.strftime("%H:%M:%S"),
                "end_time": group.end_time.strftime("%H:%M:%S"),
                "timeslots": [
                    {"time": t, "is_booked": t in booked_times}
                    for t in group.timeslots
                ],
            })

        return Response(result, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ✅ Book a hospital doctor time slot (same logic as clinic)
@api_view(['POST'])
def book_hospital_doctor_slot(request):
    """
    Book a specific time slot for a hospital doctor.

    Expected JSON:
    {
        "user": 1,
        "doctor": 3,
        "timeslot_group": 5,
        "date": "2025-11-01",
        "time": "09:30"
    }
    """
    data = request.data

    try:
        user = tbl_register.objects.get(id=data['user'])
        doctor = tbl_hospital_doctor_register.objects.get(id=data['doctor'])
        timeslot_group = HospitalDoctorTimeSlotGroup.objects.get(id=data['timeslot_group'])
    except (tbl_register.DoesNotExist, tbl_hospital_doctor_register.DoesNotExist, HospitalDoctorTimeSlotGroup.DoesNotExist):
        return Response({"error": "Invalid doctor, user, or timeslot group."}, status=404)

    # ✅ Check if time is in available slots
    timeslots = timeslot_group.timeslots
    if data['time'] not in timeslots:
        return Response({"error": "Invalid time slot."}, status=400)

    # ✅ Check if already booked
    if HospitalBooking.objects.filter(
        doctor=doctor,
        date=data['date'],
        time=data['time'],
        is_booked=True
    ).exists():
        return Response({"error": "This time slot is already booked."}, status=400)

    # ✅ Create booking
    booking = HospitalBooking.objects.create(
        user=user,
        doctor=doctor,
        timeslot_group=timeslot_group,
        date=data['date'],
        time=data['time'],
        is_booked=True
    )

    return Response({
        "message": "Slot booked successfully!",
        "booking_id": booking.id,
        "doctor": doctor.name,
        "date": data['date'],
        "time": data['time']
    }, status=201)


# from rest_framework import status
# from .models import tbl_clinic_doctor_register, ClinicBooking, ClinicDoctorTimeSlotGroup

# @api_view(['POST'])
# def book_clinic_doctor_slot(request):
#     user_id = request.data.get('user')
#     doctor_id = request.data.get('doctor')
#     timeslot_group_id = request.data.get('timeslot_group')
#     date = request.data.get('date')
#     time = request.data.get('time')

#     # ✅ Validate doctor existence
#     try:
#         doctor = tbl_clinic_doctor_register.objects.get(id=doctor_id)
#     except tbl_clinic_doctor_register.DoesNotExist:
#         return Response({"error": "Doctor not found."}, status=status.HTTP_404_NOT_FOUND)

#     # ✅ Check if already booked
#     if ClinicBooking.objects.filter(doctor_id=doctor_id, date=date, time=time).exists():
#         return Response({"error": "This time slot is already booked."}, status=status.HTTP_400_BAD_REQUEST)
#     if not user_id or int(user_id) <= 0:
#        return Response({"error": "Invalid user ID."}, status=status.HTTP_400_BAD_REQUEST)

#     if not timeslot_group_id or int(timeslot_group_id) <= 0:
#       return Response({"error": "Invalid timeslot group ID."}, status=status.HTTP_400_BAD_REQUEST)

#     # ✅ Create booking
#     booking = ClinicBooking.objects.create(
#         user_id=user_id,
#         doctor=doctor,
#         timeslot_group_id=timeslot_group_id,
#         date=date,
#         time=time,
#         is_booked=True
#     )

#     return Response({
#         "message": "Booking successful!",
#         "booking_id": booking.id,
#         "doctor": doctor.name,
#         "date": booking.date,
#         "time": booking.time
#     }, status=status.HTTP_201_CREATED)





class doctor_view_booking_clinic(APIView):
    def get(self, request, doctor_id):
        bookings = ClinicBooking.objects.filter(doctor_id=doctor_id).order_by('-created_at')
        data = []
        for booking in bookings:
            data.append({
                "id": booking.id,
                "user": booking.user.id,
                "user_name": booking.user.name,
                "date": booking.date,
                "time": booking.time,
                # "status": booking.status,
                "booked_at": booking.created_at,
            })
        return Response(data, status=status.HTTP_200_OK)
    

class doctor_view_booking_hospital(APIView):
    def get(self, request, doctor_id):
        bookings = HospitalBooking.objects.filter(doctor_id=doctor_id)
        data = []
        for booking in bookings:
            data.append({
                "id": booking.id,
                "user": booking.user.id,
                "user_name": booking.user.name,
                "date": booking.date,
                "time": booking.time,
                "status": booking.status,
                # "booked_at": booking.created_at,
            })
        return Response(data, status=status.HTTP_200_OK)
    


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ClinicBooking
class user_view_booking_clinic(APIView):
    def get(self, request, user_id):
        bookings = ClinicBooking.objects.filter(user_id=user_id)
        data = []
        for booking in bookings:
            data.append({
                "id": booking.id,
                "doctor": booking.doctor.id if booking.doctor else None,
                "doctor_name": booking.doctor.name if booking.doctor else "Doctor removed",
                "patient": booking.user.id,
                "patient_name": booking.user.name if booking.user else "User removed",
                "date": booking.date,
                "time": booking.time,
                # "booked_at": booking.created_at,
            })
        return Response(data, status=status.HTTP_200_OK)
    
class user_view_booking_hospital(APIView):
    def get(self, request, user_id):
        bookings = HospitalBooking.objects.filter(user_id=user_id)
        data = []
        for booking in bookings:
            data.append({
                "id": booking.id,
                "doctor": booking.doctor.id if booking.doctor else None,
                "doctor_name": booking.doctor.name if booking.doctor else "Doctor removed",
                "patient": booking.user.id,
                "patient_name": booking.user.name if booking.user else "User removed",
                "date": booking.date,
                "time": booking.time,
                # "booked_at": getattr(booking, 'created_at', None),
            })
        return Response(data, status=status.HTTP_200_OK)





from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import ClinicDoctorFeedback, tbl_register, tbl_clinic_doctor_register
from .serializers import ClinicDoctorFeedbackSerializer


# ✅ Add Feedback (User → Doctor)
@api_view(['POST'])
def add_clinic_doctor_feedback(request):
    """
    User adds feedback for a clinic doctor.
    Expected JSON:
    {
        "user": 1,
        "doctor": 3,
        "rating": 5,
        "comments": "Excellent service!"
    }
    """
    data = request.data

    try:
        user = tbl_register.objects.get(id=data['user'])
        doctor = tbl_clinic_doctor_register.objects.get(id=data['doctor'])
    except (tbl_register.DoesNotExist, tbl_clinic_doctor_register.DoesNotExist):
        return Response({"error": "Invalid user or doctor ID."}, status=status.HTTP_404_NOT_FOUND)

    # ✅ Prevent duplicate feedback from same user
    if ClinicDoctorFeedback.objects.filter(user=user, doctor=doctor).exists():
        return Response({"error": "You have already submitted feedback for this doctor."}, status=400)

    serializer = ClinicDoctorFeedbackSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Feedback submitted successfully!", "feedback": serializer.data}, status=201)
    return Response(serializer.errors, status=400)


# ✅ Doctor views all feedback received
@api_view(['GET'])
def view_clinic_doctor_feedback(request, doctor_id):
    """
    Doctor views all feedback given to them.
    """
    feedbacks = ClinicDoctorFeedback.objects.filter(doctor_id=doctor_id).order_by('-created_at')

    if not feedbacks.exists():
        return Response({"message": "No feedback found for this doctor."}, status=404)

    serializer = ClinicDoctorFeedbackSerializer(feedbacks, many=True)
    return Response(serializer.data, status=200)



from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import HospitalDoctorFeedback, tbl_hospital_doctor_register, tbl_register
from .serializers import HospitalDoctorFeedbackSerializer

# 🧠 User Adds Feedback
@api_view(['POST'])
def add_hospital_doctor_feedback(request):
    user_id = request.data.get('user')
    doctor_id = request.data.get('doctor')
    rating = request.data.get('rating')
    comments = request.data.get('comments', '')

    try:
        user = tbl_register.objects.get(id=user_id)
        doctor = tbl_hospital_doctor_register.objects.get(id=doctor_id)
    except (tbl_register.DoesNotExist, tbl_hospital_doctor_register.DoesNotExist):
        return Response({'error': 'Invalid user or doctor ID'}, status=status.HTTP_404_NOT_FOUND)

    feedback = HospitalDoctorFeedback.objects.create(
        user=user, doctor=doctor, rating=rating, comments=comments
    )
    serializer = HospitalDoctorFeedbackSerializer(feedback)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


# 🧠 Doctor Views Feedback
@api_view(['GET'])
def view_hospital_doctor_feedback(request, doctor_id):
    feedbacks = HospitalDoctorFeedback.objects.filter(doctor_id=doctor_id).order_by('-created_at')
    serializer = HospitalDoctorFeedbackSerializer(feedbacks, many=True)
    return Response(serializer.data)



# views.py
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Table, TableStyle

from .models import ClinicBooking, HospitalBooking

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from .models import ClinicBooking, HospitalBooking
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
# views.py

from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch

from .models import ClinicBooking, HospitalBooking


# ✅ CLINIC BOOKING PDF DOWNLOAD
@api_view(['POST'])
def download_clinic_booking_pdf(request, booking_id):
    try:
        booking = ClinicBooking.objects.get(id=booking_id)
    except ClinicBooking.DoesNotExist:
        return Response({"error": "Booking not found"}, status=404)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="clinic_booking_{booking_id}.pdf"'

    doc = SimpleDocTemplate(response)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("<b>Clinic Doctor Booking Receipt</b>", styles['Title']))
    elements.append(Spacer(1, 0.3 * inch))

    data = [
        ["Booking ID:", booking.id],
        ["Patient Name:", booking.user.name],
        ["Doctor Name:", booking.doctor.name],
        ["Clinic Name:", booking.doctor.clinic_name],
        ["Date:", str(booking.date)],
        ["Time:", booking.time],
        ["Booked On:", str(booking.created_at)],
    ]

    table = Table(data, colWidths=[150, 300])
    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ]))

    elements.append(table)
    doc.build(elements)

    return response


# ✅ HOSPITAL BOOKING PDF DOWNLOAD
@api_view(['POST'])
def download_hospital_booking_pdf(request, booking_id):
    try:
        booking = HospitalBooking.objects.get(id=booking_id)
    except HospitalBooking.DoesNotExist:
        return Response({"error": "Booking not found"}, status=404)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="hospital_booking_{booking_id}.pdf"'

    doc = SimpleDocTemplate(response)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("<b>Hospital Doctor Booking Receipt</b>", styles['Title']))
    elements.append(Spacer(1, 0.3 * inch))

    data = [
        ["Booking ID:", booking.id],
        ["Patient Name:", booking.user.name],
        ["Doctor Name:", booking.doctor.name],
        ["Hospital Name:", booking.doctor.hospital_name],
        ["Date:", str(booking.date)],
        ["Time:", booking.time],
        ["Status:", booking.status],
    ]

    table = Table(data, colWidths=[150, 300])
    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ]))

    elements.append(table)
    doc.build(elements)

    return response
