# api/management/commands/load_transactions.py
from django.core.management.base import BaseCommand
import requests
import json
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Load transactions from bank API and save to JSON file'

    def handle(self, *args, **options):
        try:
            bank_api_url = "http://192.168.50.167:5000/bank_api/transactions"
            
            self.stdout.write(f'Fetching transactions from {bank_api_url}...')
            
            response = requests.get(bank_api_url)
            response.raise_for_status()
            transactions_data = response.json()
            
            self.stdout.write(f'Found {len(transactions_data)} transactions')
            
            # Сохраняем в JSON файл
            file_path = os.path.join(settings.BASE_DIR, 'transactions.json')
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(transactions_data, f, indent=2, ensure_ascii=False)
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully saved {len(transactions_data)} transactions to {file_path}')
            )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error: {str(e)}')
            )