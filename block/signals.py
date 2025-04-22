from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
from django.utils import timezone
from .models import DiseaseDiagnosis, DiagnosisBlock
from .utils import rebuild_user_blockchain


@receiver(pre_delete, sender=DiseaseDiagnosis)
def delete_block_before_diagnosis(sender, instance, **kwargs):
    """
    Deletes the corresponding blockchain block before deleting a diagnosis.
    This ensures that the blockchain remains consistent when a diagnosis is deleted.
    """
    try:
        # Attempt to delete the blockchain block related to this diagnosis
        block = DiagnosisBlock.objects.get(diagnosis=instance)
        block.delete()
        print(f"Deleted blockchain block for diagnosis {instance.id}")
    except DiagnosisBlock.DoesNotExist:
        # If no block exists for this diagnosis, no need to do anything
        print(f"No blockchain block found for diagnosis {instance.id}")


@receiver([post_save, post_delete], sender=DiseaseDiagnosis)
def handle_diagnosis_change(sender, instance, **kwargs):
    """
    Rebuild the blockchain for the specific user when a diagnosis is saved or deleted.
    """
    # Rebuild the blockchain for the user associated with this diagnosis
    rebuild_user_blockchain(instance.medical_record.app_user.id)


def rebuild_user_blockchain(user_id):
    """
    Rebuilds the blockchain for a specific user by deleting existing blocks
    and creating new ones based on the user's diagnoses.
    """
    # Delete all blocks related to this user
    DiagnosisBlock.objects.filter(diagnosis__medical_record__app_user__id=user_id).delete()

    # Get all the diagnoses for this user, ordered by diagnosis date
    diagnoses = DiseaseDiagnosis.objects.filter(
        medical_record__app_user__id=user_id
    ).order_by('diagnosis_date')

    previous_hash = None

    # Create new blocks for the diagnoses
    for diagnosis in diagnoses:
        block = DiagnosisBlock(diagnosis=diagnosis, previous_hash=previous_hash)
        block.block_hash = block.compute_hash()
        block.save()
        previous_hash = block.block_hash  # Set current block hash as previous hash for next block
