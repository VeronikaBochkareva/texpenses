import json
import os
from django.conf import settings
from .models import Categories  # Добавляем этот импорт

def load_transactions():
    file_path = os.path.join(settings.BASE_DIR, 'transactions.json')
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def get_category_transactions_sum(category_id):
    transactions = load_transactions()
    total = 0

    category_mapping = {
        "0": "others",
        "1": "study", 
        "2": "sport",
        "3": "pharmacies",
        "4": "food"
    }
    
    transaction_category_id = None
    for trans_id, cat_name in category_mapping.items():
        try:
            category = Categories.objects.get(id=category_id)
            if cat_name == category.name.lower().strip():
                transaction_category_id = trans_id
                break
        except Categories.DoesNotExist:
            continue
    
    if transaction_category_id is None:
        return 0
    
    for transaction in transactions:
        trans_cat = transaction.get('categories')
        if trans_cat is not None and str(trans_cat) == transaction_category_id:
            total += transaction.get('summ', 0)
    
    return total