import base64
import hashlib
import json
from django.db import models
from django.utils import timezone


class ExternalAppUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=255, db_column='first_name')
    last_name = models.CharField(max_length=255, db_column='last_name')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'app_user'


class AccessToken(models.Model):
    app_user = models.ForeignKey(ExternalAppUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=64)


class MedicalRecord(models.Model):
    app_user = models.OneToOneField(
        ExternalAppUser, on_delete=models.CASCADE, db_column='app_user_id', unique=True
    )

    class Meta:
        managed = False
        db_table = 'medical_record'

    def __str__(self):
        return f"Medical Record for {self.app_user.first_name} {self.app_user.last_name}"


class DiseaseDiagnosis(models.Model):
    diagnosis_date = models.DateField(db_column='diagnosis_date')
    disease_name = models.CharField(max_length=255)
    diagnostic_details = models.TextField()
    image = models.BinaryField(null=True, blank=True)
    medical_record = models.ForeignKey(
        MedicalRecord,
        on_delete=models.CASCADE,
        db_column='medical_record_id',
        related_name='diagnoses'
    )

    class Meta:
        managed = False
        db_table = 'disease_diagnosis'

    def __str__(self):
        return self.disease_name


class DiagnosisBlock(models.Model):
    diagnosis = models.ForeignKey(DiseaseDiagnosis, on_delete=models.CASCADE)  # Set on_delete to CASCADE
    timestamp = models.DateTimeField(default=timezone.now)
    block_hash = models.CharField(max_length=64)
    previous_hash = models.CharField(max_length=64, null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'diagnosis_block'
        
    def compute_hash(self):
        data = {
            "diagnosis_id": self.diagnosis.id,
            "diagnosis_date": str(self.diagnosis.diagnosis_date),
            "disease_name": self.diagnosis.disease_name,
            "diagnostic_details": self.diagnosis.diagnostic_details,
            "image": base64.b64encode(self.diagnosis.image).decode("utf-8") if self.diagnosis.image else None,
            "timestamp": self.timestamp.isoformat(),
            "previous_hash": self.previous_hash or ""
        }
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode('utf-8')).hexdigest()

    def save(self, *args, **kwargs):
        if not self.timestamp:
            self.timestamp = timezone.now()
        if not self.block_hash:
            self.block_hash = self.compute_hash()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Block {self.id} for Diagnosis: {self.diagnosis.disease_name}"
