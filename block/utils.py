from .models import DiseaseDiagnosis, DiagnosisBlock
from django.utils import timezone


def rebuild_blockchain():
    """
    Rebuilds the entire blockchain for all diagnoses, ensuring that all blocks are consistent.
    This method creates or updates blocks for all diagnoses in the system.
    """
    blocks = []
    previous_hash = None

    # Get all the diagnoses ordered by diagnosis date
    diagnoses = DiseaseDiagnosis.objects.order_by('diagnosis_date', 'id')

    for diagnosis in diagnoses:
        # Get or create a block for the diagnosis
        block, created = DiagnosisBlock.objects.get_or_create(diagnosis=diagnosis)

        # Update block details
        block.timestamp = timezone.now()
        block.previous_hash = previous_hash
        block.block_hash = block.compute_hash()
        block.save()

        # Update the previous hash for the next block
        previous_hash = block.block_hash
        blocks.append(block)

    # Remove orphaned blocks (blocks that are no longer linked to a valid diagnosis)
    valid_ids = {d.id for d in diagnoses}
    DiagnosisBlock.objects.exclude(diagnosis_id__in=valid_ids).delete()


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
        # Create a new block for this diagnosis
        block = DiagnosisBlock(diagnosis=diagnosis, previous_hash=previous_hash)
        block.block_hash = block.compute_hash()
        block.save()

        # Update the previous hash for the next block
        previous_hash = block.block_hash  # Set current block hash as previous hash for next block


