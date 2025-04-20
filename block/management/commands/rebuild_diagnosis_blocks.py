from django.core.management.base import BaseCommand
from block.utils import rebuild_blockchain  # Adjust if your path differs

class Command(BaseCommand):
    help = 'Rebuilds the diagnosis blockchain for all DiseaseDiagnosis entries'

    def handle(self, *args, **options):
        self.stdout.write("🔄 Rebuilding diagnosis blockchain...")
        rebuild_blockchain()
        self.stdout.write(self.style.SUCCESS("✅ Blockchain rebuilt successfully."))
