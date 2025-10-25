from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum
from .models import Users, Categories, Settings

@api_view(['GET'])
def categories_list(request):
    categories = Categories.objects.all().values('id', 'name')
    return Response(list(categories))

@api_view(['GET'])
def expenses_list(request):
    # Получаем все категории
    categories = Categories.objects.all()
    
    result_categories = []
    
    for category in categories:
        # Сумма всех транзакций по данной категории
        total_spent = Transactions.objects.filter(
            category=category
        ).aggregate(total=Sum('sum'))['total'] or 0
        
        # Получаем настройки для данной категории (берем первую запись)
        setting = Settings.objects.filter(users=category).first()
        total_limit = setting.total if setting else 0
        
        # Разница между лимитом и потраченной суммой
        remaining = total_limit - total_spent
        
        result_categories.append({
            'name': category.name,
            'sum_spent': total_spent,
            'sum_remain': remaining
        })
    
    return Response({'categories': result_categories})

@api_view(['GET', 'POST'])
def settings_view(request):
    
    if request.method == 'GET':
        # Получаем все настройки
        settings = Settings.objects.select_related('users').all()
        
        result_categories = []
        
        for setting in settings:
            # Сумма всех транзакций по данной категории
            total_spent = Transactions.objects.filter(
                category=setting.users
            ).aggregate(total=Sum('sum'))['total'] or 0
            
            result_categories.append({
                'name': setting.users.name,
                'sum': total_spent,
                'total': setting.total
            })
        
        return Response({'categories': result_categories})
    
    elif request.method == 'POST':
        # Обновление настроек
        data = request.data
        
        if 'categories' not in data:
            return Response(
                {'error': 'Missing categories in request data'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        updated_categories = []
        
        for category_data in data['categories']:
            category_name = category_data.get('name')
            new_total = category_data.get('total')
            
            if not category_name or new_total is None:
                continue
            
            try:
                category = Categories.objects.get(name=category_name)
                setting, created = Settings.objects.get_or_create(
                    users=category,
                    defaults={'total': new_total}
                )
                
                if not created:
                    setting.total = new_total
                    setting.save()
                
                # Пересчитываем текущую сумму транзакций
                current_sum = Transactions.objects.filter(
                    category=category
                ).aggregate(total=Sum('sum'))['total'] or 0
                
                updated_categories.append({
                    'name': category_name,
                    'sum': current_sum,
                    'total': new_total
                })
                
            except Categories.DoesNotExist:
                continue
        
        return Response({'categories': updated_categories})
