from django.apps import AppConfig


class BlockConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'block'

    def ready(self):
        import block.signals  
