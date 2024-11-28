from django.db import models

# Create your models here.
class Users(models.Model):
    UserHealthID=models.IntegerField(primary_key=True)
    FirstName=models.CharField(max_length=50,)
    LastName=models.CharField(max_length=50,)
    Email=models.CharField(max_length=50,)
    PhoneNumber=models.CharField(max_length=50,)
    Height=models.IntegerField()
    Weight=models.IntegerField()
    Role = models.CharField(max_length=50,)
    class Meta:
         db_table = 'users'
class Hospital(models.Model):
    HospitalID=models.IntegerField(primary_key=True)
    HospitalName = models.TextField()
    Address = models.TextField()
    ContactNumber=models.CharField(max_length=50,)
    class Meta:
         db_table = 'hospital'
class Patient(models.Model):
    PatientID = models.IntegerField(primary_key=True)
    DOB = models.TextField()
    Gender = models.CharField(max_length=50,)
    PUserHealthID =models.ForeignKey(
        Users,
        on_delete=models.SET_NULL,  
        null=True,
        to_field="UserHealthID",
        db_column="PUserHealthID"
    )
    class Meta:
         db_table = 'patient'
class Appointment(models.Model):
    AppointmentID=models.IntegerField( primary_key=True )
    AppointmentDate=models.TextField()
    Patient_ID=models.ForeignKey(
        Patient,
        on_delete=models.SET_NULL,
        null=True,
        to_field="PatientID",
         db_column="Patient_ID"
    )
    Hospital_ID=models.ForeignKey(
        Hospital,
        on_delete=models.SET_NULL,  
        null=True,
        to_field="HospitalID",
        db_column="Hospital_ID"
    )
    class Meta:
         db_table = 'appointment'
class Doctor(models.Model):
    DoctorID=models.IntegerField(primary_key=True)
    Specialization=models.TextField()
    DUserHealthID=models.ForeignKey(
        Users,
        on_delete=models.SET_NULL,  
        null=True,
        to_field="UserHealthID",
         db_column="DUserHealthID"
    )
    Doctor_HospitalID=models.ForeignKey(
        Hospital,
        on_delete=models.SET_NULL,
        null=True,
        to_field="HospitalID",
         db_column="Doctor_HospitalID"
    )
    class Meta:
         db_table = 'doctor'

class PatientDiagnosis(models.Model):
    DiagnosisID = models.IntegerField(primary_key=True)
    DiagnosisDetails = models.TextField()
    Patient_ID = models.ForeignKey(
        Patient,
        on_delete=models.SET_NULL,
        null=True,
        to_field="PatientID",
         db_column="Patient_ID"
    )
    Doctor_ID = models.ForeignKey(
        Doctor,
        on_delete=models.SET_NULL,
        null=True,
        to_field="DoctorID",
         db_column="Doctor_ID"
    )
    class Meta:
         db_table = 'patient_diagnosis'
class PatientDoctor(models.Model):
    Patient_ID = models.ForeignKey(
        Patient,
        on_delete=models.SET_NULL,
        null=True,
        to_field="PatientID",
         db_column="Patient_ID"
    )
    Doctor_ID = models.ForeignKey(
        Doctor,
        on_delete=models.SET_NULL,
        null=True,
        to_field="DoctorID",
        db_column="Doctor_ID"
    )
    class Meta:
        db_table = 'patient_doctor'
        unique_together = ('Patient_ID', 'Doctor_ID')
class Reports(models.Model):
    ReportID=models.IntegerField(primary_key=True)
    TestName=models.TextField()
    SampleCollected=models.TextField()
    Observation=models.TextField()
    Patient_ReportID=models.ForeignKey(
        Patient,
        on_delete=models.SET_NULL,
        null=True,
        to_field="PatientID",
         db_column="Patient_ReportID"
    )
    SampleType=models.TextField()
    class Meta:
         db_table = 'reports'
class Prescription(models.Model):
    PresID=models.IntegerField(primary_key=True)
    Medicines=models.TextField()
    Comments=models.TextField()
    PatientPres_ID= models.ForeignKey(
        Patient,
        on_delete=models.SET_NULL,
        null=True,
        to_field="PatientID",
         db_column="PatientPres_ID"
    )
    DoctorPres_ID=models.ForeignKey(
        Doctor,
        on_delete=models.SET_NULL,
        null=True,
        to_field="DoctorID",
         db_column="DoctorPres_ID"
    )
    class Meta:
         db_table = 'prescription'
class PatientVisit(models.Model):
    VisitReason = models.TextField()
    VisitNotes = models.TextField()
    VisitID = models.IntegerField(primary_key=True)
    VisitDate = models.TextField()
    ReportID = models.ForeignKey(
        Reports,
        on_delete=models.SET_NULL,
        null=True,
        to_field="ReportID",
         db_column="ReportID"
    )
    PresID = models.ForeignKey(
        Prescription,
        on_delete=models.SET_NULL,
        null=True,
        to_field="PresID",
         db_column="PresID"
    )
    Patient_ID= models.ForeignKey(
        Patient,
        on_delete=models.SET_NULL,
        null=True,
        to_field="PatientID",
         db_column="Patient_ID"
    )
    Doctor_ID= models.ForeignKey(
        Doctor,
        on_delete=models.SET_NULL,
        null=True,
        to_field="DoctorID",
         db_column="Doctor_ID"
    )
    DiagnosisID= models.ForeignKey(
        PatientDiagnosis,
        on_delete=models.SET_NULL,
        null=True,
        to_field="DiagnosisID",
         db_column="DiagnosisID"
    )
    AppointmentID= models.ForeignKey(
        Appointment,
        on_delete=models.SET_NULL,
        null=True,
        to_field="AppointmentID",
         db_column="AppointmentID"
    )
    class Meta:
         db_table = 'patient_visit'
class Payment(models.Model):
    PaymentID = models.IntegerField(primary_key=True)
    TranStatus=models.CharField(max_length=50)
    Patient_ID= models.ForeignKey(
        Patient,
        on_delete=models.SET_NULL,
        null=True,
        to_field="PatientID",
         db_column="Patient_ID"
    )
    Hospital_ID=models.ForeignKey(
        Hospital,
        on_delete=models.SET_NULL,
        null=True,
        to_field="HospitalID",
         db_column="Hospital_ID"
    )
    class Meta:
         db_table = 'payment'



