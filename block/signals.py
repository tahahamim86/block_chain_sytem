from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import DiseaseDiagnosis
from .utils import rebuild_blockchain


@receiver([post_save, post_delete], sender=DiseaseDiagnosis)
def handle_diagnosis_change(sender, instance, **kwargs):
    rebuild_blockchain()
