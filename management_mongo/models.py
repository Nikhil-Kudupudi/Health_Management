from django.db import models

from mongoengine import Document, StringField, IntField, BooleanField, ReferenceField, ListField, CASCADE

class User(Document):
    user_health_id = IntField(primary_key=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)
    email = StringField(max_length=50)
    phone_number = StringField(max_length=50)
    height = IntField()
    weight = IntField()
    role = StringField(max_length=50)
    meta = {'collection': 'users'}

class Hospital(Document):
    hospital_id = IntField(primary_key=True)
    hospital_name = StringField()
    address = StringField()
    contact_number = StringField(max_length=50)
    meta = {'collection': 'hospital'}

class Patient(Document):
    patient_id = IntField(primary_key=True)
    dob = StringField()
    gender = StringField(max_length=50)
    user_health_id = ReferenceField(User, reverse_delete_rule=CASCADE, null=True)
    meta = {'collection': 'patient'}

class Appointment(Document):
    appointment_id = IntField(primary_key=True)
    appointment_date = StringField()
    patient = ReferenceField(Patient, reverse_delete_rule=CASCADE, null=True)
    hospital = ReferenceField(Hospital, reverse_delete_rule=CASCADE, null=True)
    meta = {'collection': 'appointment'}

class Doctor(Document):
    doctor_id = IntField(primary_key=True)
    specialization = StringField()
    user_health_id = ReferenceField(User, reverse_delete_rule=CASCADE, null=True)
    hospital = ReferenceField(Hospital, reverse_delete_rule=CASCADE, null=True)
    meta = {'collection': 'doctor'}

class PatientDiagnosis(Document):
    diagnosis_id = IntField(primary_key=True)
    diagnosis_details = StringField()
    patient = ReferenceField(Patient, reverse_delete_rule=CASCADE, null=True)
    doctor = ReferenceField(Doctor, reverse_delete_rule=CASCADE, null=True)
    meta = {'collection': 'patient_diagnosis'}

class Reports(Document):
    report_id = IntField(primary_key=True)
    test_name = StringField()
    sample_collected = StringField()
    observation = StringField()
    sample_type = StringField()
    patient = ReferenceField(Patient, reverse_delete_rule=CASCADE, null=True)
    meta = {'collection': 'reports'}

class Prescription(Document):
    pres_id = IntField(primary_key=True)
    medicines = StringField()
    comments = StringField()
    patient = ReferenceField(Patient, reverse_delete_rule=CASCADE, null=True)
    doctor = ReferenceField(Doctor, reverse_delete_rule=CASCADE, null=True)
    meta = {'collection': 'prescription'}

class PatientVisit(Document):
    visit_reason = StringField()
    visit_notes = StringField()
    visit_id = IntField(primary_key=True)
    visit_date = StringField()
    report = ReferenceField(Reports, reverse_delete_rule=CASCADE, null=True)
    prescription = ReferenceField(Prescription, reverse_delete_rule=CASCADE, null=True)
    patient = ReferenceField(Patient, reverse_delete_rule=CASCADE, null=True)
    doctor = ReferenceField(Doctor, reverse_delete_rule=CASCADE, null=True)
    diagnosis = ReferenceField(PatientDiagnosis, reverse_delete_rule=CASCADE, null=True)
    appointment = ReferenceField(Appointment, reverse_delete_rule=CASCADE, null=True)
    meta = {'collection': 'patient_visit'}

class Payment(Document):
    payment_id = IntField(primary_key=True)
    tran_status = StringField(max_length=50)
    patient = ReferenceField(Patient, reverse_delete_rule=CASCADE, null=True)
    hospital = ReferenceField(Hospital, reverse_delete_rule=CASCADE, null=True)
    meta = {'collection': 'payment'}
