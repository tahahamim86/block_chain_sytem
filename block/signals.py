from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
from .models import DiseaseDiagnosis, DiagnosisBlock
from .utils import rebuild_blockchain

@receiver(pre_delete, sender=DiseaseDiagnosis)
def delete_block_before_diagnosis(sender, instance, **kwargs):
    # Delete the corresponding block before diagnosis is removed
    try:
        block = DiagnosisBlock.objects.get(diagnosis=instance)
        block.delete()
    except DiagnosisBlock.DoesNotExist:
        pass

@receiver([post_save, post_delete], sender=DiseaseDiagnosis)
def handle_diagnosis_change(sender, instance, **kwargs):
    rebuild_blockchain()
