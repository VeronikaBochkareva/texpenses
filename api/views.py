from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum
from .models import Users, Categories, Settings
from django.db import transaction

from .utils import get_category_transactions_sum, load_transactions

@api_view(['GET'])
def categories_list(request):
    categories = Categories.objects.all().values('id', 'name')
    return Response(list(categories))

@api_view(['GET'])
def expenses_list(request):
    categories = Categories.objects.all()
    
    result_categories = []
    
    for category in categories:
        total_spent = get_category_transactions_sum(category.id)
        
        setting = Settings.objects.filter(users=category).first()
        total_limit = setting.total if setting else 0
        
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
        try:
            user_id = request.GET.get('user_id')
            if not user_id:
                return Response(
                    {'error': 'user_id parameter is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user = Users.objects.get(id=user_id)
            
            category_settings = Settings.objects.filter(
                categories=user
            ).select_related('users')
            
            response_data = {
                'user_id': user.id,
                'user_name': user.name,
                'limit': user.limit,
                'category_limits': [
                    {
                        'category_id': setting.users.id,
                        'category_name': setting.users.name,
                        'total': setting.total
                    }
                    for setting in category_settings
                ]
            }
            
            return Response(response_data)
            
        except Users.DoesNotExist:
            return Response(
                {'error': 'User not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    elif request.method == 'POST':
        # Обновление данных пользователя
        try:
            data = request.data
            
            user_id = data.get('user_id')
            if not user_id:
                return Response(
                    {'error': 'user_id is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            with transaction.atomic():
                user = Users.objects.get(id=user_id)
                if 'limit' in data:
                    user.limit = data['limit']
                    user.save()
                
                category_limits = data.get('category_limits', [])
                
                for category_limit in category_limits:
                    category_id = category_limit.get('category_id')
                    total = category_limit.get('total')
                    
                    if category_id is not None and total is not None:
                        setting, created = Settings.objects.update_or_create(
                            users_id=category_id,
                            categories=user,
                            defaults={'total': total}
                        )
            
            updated_category_settings = Settings.objects.filter(
                categories=user
            ).select_related('users')
            
            response_data = {
                'user_id': user.id,
                'user_name': user.name,
                'limit': user.limit,
                'category_limits': [
                    {
                        'category_id': setting.users.id,
                        'category_name': setting.users.name,
                        'total': setting.total
                    }
                    for setting in updated_category_settings
                ]
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        except Users.DoesNotExist:
            return Response(
                {'error': 'User not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@api_view(['GET'])
def transactions_view(request):
    transactions = load_transactions()
    return Response(transactions)