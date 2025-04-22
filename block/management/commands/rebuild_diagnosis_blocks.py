from django.core.management.base import BaseCommand
from django.utils.timezone import now
from block.utils import rebuild_user_blockchain  # Update import to use user-specific rebuild function

class Command(BaseCommand):
    help = 'Rebuilds the diagnosis blockchain for a specific user.'

    def add_arguments(self, parser):
        # Add an argument to specify the user ID
        parser.add_argument('user_id', type=int, help='The ID of the user whose blockchain should be rebuilt')

    def handle(self, *args, **options):
        user_id = options['user_id']
        self.stdout.write(f"[{now()}] 🔁 Starting blockchain rebuild for user {user_id}...")

        try:
            # Rebuild the blockchain for the specific user
            rebuild_user_blockchain(user_id)
            self.stdout.write(self.style.SUCCESS(f"[{now()}] ✅ Blockchain for user {user_id} rebuilt successfully."))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"[{now()}] ❌ Failed to rebuild blockchain: {e}"))
