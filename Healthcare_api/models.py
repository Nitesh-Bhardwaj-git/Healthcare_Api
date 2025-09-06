from django.db import models


class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    email = models.EmailField(unique=True)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

class Doctor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=150)
    email = models.EmailField(unique=True)

    def __str__(self) -> str:
        return f"Dr. {self.first_name} {self.last_name}"

class PatientDoctorMapping(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='doctor_mappings')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='patient_mappings')

    class Meta:
        unique_together = ('patient', 'doctor')

    def __str__(self) -> str:
        return f"{self.patient} ↔ {self.doctor}"

