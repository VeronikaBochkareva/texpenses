from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def categories(request):
    Categories = []
    return Response(Categories)

@api_view(['GET'])
def expenses(request):
    Expenses = []
    return Response(Expenses)

@api_view(['GET'])
def settings(request):
    Settings = []
    return Response(Settings)

@api_view(['POST'])
def settings(request):
    Settings = []
    return Response(Settings)
