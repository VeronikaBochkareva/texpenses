from django.apps import AppConfig
import os
from django.db.utils import OperationalError, ProgrammingError

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    def ready(self):
        if os.environ.get('RUN_MAIN'):
            try:
                self.load_categories()
            except (OperationalError, ProgrammingError):
                print("Database not ready, skipping categories load")
            except Exception as e:
                print(f"Error loading categories: {e}")

    def load_categories(self):
        from django.core.management import call_command
        call_command('load_categories')

