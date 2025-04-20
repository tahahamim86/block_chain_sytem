from .models import DiseaseDiagnosis, DiagnosisBlock
from django.utils import timezone


def rebuild_blockchain():
    blocks = []
    previous_hash = ""

    diagnoses = DiseaseDiagnosis.objects.order_by('diagnosis_date', 'id')

    for diagnosis in diagnoses:
        block, created = DiagnosisBlock.objects.get_or_create(diagnosis=diagnosis)
        block.timestamp = timezone.now()
        block.previous_hash = previous_hash
        block.block_hash = block.compute_hash()
        block.save()
        previous_hash = block.block_hash
        blocks.append(block)

    # Remove orphaned blocks
    valid_ids = [d.id for d in diagnoses]
    DiagnosisBlock.objects.exclude(diagnosis_id__in=valid_ids).delete()
