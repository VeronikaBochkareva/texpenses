from django.core.management.base import BaseCommand
from django.db import transaction
import requests
from api.models import Categories

class Command(BaseCommand):
    help = 'Load categories from bank API'

    def handle(self, *args, **options):
        try:
            bank_api_url = "http://192.168.50.167:5000/bank_api/categories"
            
            self.stdout.write(f'Fetching categories from {bank_api_url}...')
            
            response = requests.get(bank_api_url)
            response.raise_for_status()
            categories_data = response.json()
            
            
            with transaction.atomic():
                Categories.objects.all().delete()
                
                for key, name in categories_data.items():
                    clean_name = name.strip()
                    category = Categories.objects.create(name=clean_name)
                    self.stdout.write(f'Created category: {clean_name}')
                
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully loaded {len(categories_data)} categories')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error: {e}')
            )
