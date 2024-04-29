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
            block = data.get("block")
            if phone_number and full_name and gender and email and date_of_birth and district and block:
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
                    district=district,
                    block=block
                )
                return new_patient
            else:
                raise Exception("All fields mentioned are compulsory")
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
            district = data.get("district")
            block = data.get("block")

            patient = Patient.objects.get(id=user_created)
            new_patient = Patient.objects.create(
                user=patient.user,
                full_name=full_name,
                gender=gender,
                date_of_birth=date_of_birth,
                district=district,
                block=block,
                created_by=patient
            )
            return new_patient
        except IntegrityError as e:
            raise Exception (f"IntegrityError: {e}")

    @staticmethod
    def change_profile_user(requests, data):
        try:
            user_created = requests.user.id
            full_name = data.get("full_name")
            gender = data.get("gender")
            date_of_birth = data.get("date_of_birth")
            blood_group = data.get("blood_group")
            weight = data.get("weight")
            district = data.get("district")
            block = data.get("block")
            height = data.get("height")
            patient = Patient.objects.get(id=user_created)
            new_patient = Patient.objects.get(id=user_created)
            new_patient.user=patient.user
            if full_name:
                new_patient.full_name=full_name
            if gender:
                new_patient.gender = gender
            if block:
                new_patient.block = block

            if date_of_birth:
                new_patient.date_of_birth = date_of_birth

            if blood_group:
                new_patient.blood_group = blood_group

            if weight:
                new_patient.weight = weight

            if district:
                new_patient.district = district

            if patient:
                new_patient.created_by = patient

            if height:
                new_patient.height = height
            new_patient.save()
            return new_patient
        except:
            raise Exception ("Something Went Wrong")

