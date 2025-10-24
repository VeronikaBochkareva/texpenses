from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Categories
from django.http import JsonResponse

@api_view(['GET'])
def categories(request):
    # Получаем все категории
    categories = Categories.objects.all()
    
    # Формируем список категорий в нужном формате
    categories_list = [
        {
            "id": category.id,
            "name": category.name
        }
        for category in categories
    ]
    
    # Возвращаем JSON ответ
    return JsonResponse({
        "categories": categories_list
    })

@api_view(['GET'])
def expenses(request):
    if request.method == 'GET':
        Expenses = []
        return Response(Expenses)

@api_view(['GET', 'POST'])
def settings(request):
    if request.method == 'GET':
        Settings = []
        return Response(Settings)
    elif request.method == 'POST':
        Settings = []
        return Response(Settings)


