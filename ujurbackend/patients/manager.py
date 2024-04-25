from django.db import IntegrityError
from patients.models import Patient
from users.models import UsersDetails


class PatientManager:
    @staticmethod
    def patient_signup(requests, data):
        try:
            phone_number = data.get("phoneNumber")
            full_name = data.get("fullName")
            gender = data.get("gender")
            email = data.get("email")
            date_of_birth = data.get("dob")
            # blood_group = data.get("bloodGroup")
            # weight = data.get("weight")
            district = data.get("district")
            user = UsersDetails.objects.get(phone=phone_number)
            if email:
                user.email = email
                user.save()
            new_patient = Patient.objects.create(
                user=user,
                full_name=full_name,
                gender=gender,
                date_of_birth=date_of_birth,
                # blood_group=blood_group,
                # weight=weight,
                address=district
            )
            return new_patient
        except IntegrityError as e:
            raise Exception (f"IntegrityError: {e}")

    @staticmethod
    def get_patient_profile(request, data):
        try:
            patient_id = request.user.id
            if patient_id:
                required_patient = Patient.objects.filter(id=patient_id).select_related('user')[0]
                if required_patient.created_by:
                    extra_patients = Patient.objects.filter(created_by=required_patient.created_by).exclude(
                        id=required_patient.id)
                    extra_patients = extra_patients.union(Patient.objects.filter(id=required_patient.created_by_id))


                else:
                    extra_patients = Patient.objects.filter(created_by=patient_id)
                return required_patient, extra_patients
        except Exception as e:
            pass

    @staticmethod
    def get_latest_appointment_patient(data):
        try:
            patient_id = data.get('patient_id')
            if patient_id:
                return Patient.objects.get(id =patient_id).select_related('user')
        except:
            pass

    @staticmethod
    def add_new_patient(requests, data):
        try:
            user_created = requests.user.id
            full_name = data.get("fullName")
            gender = data.get("gender")
            date_of_birth = data.get("dob")
            blood_group = data.get("bloodGroup")
            weight = data.get("weight")
            district = data.get("district")
            patient = Patient.objects.get(id=user_created)
            new_patient = Patient.objects.create(
                user=patient.user,
                full_name=full_name,
                gender=gender,
                date_of_birth=date_of_birth,
                blood_group=blood_group,
                weight=weight,
                address=district,
                created_by=patient
            )
            return new_patient
        except IntegrityError as e:
            raise Exception (f"IntegrityError: {e}")

