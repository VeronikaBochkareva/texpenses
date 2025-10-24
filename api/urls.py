from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('categories/', include('api.categories.urls'), name='categories'),
    path('expenses/', include('api.expenses.urls'), name='expenses'),
    path('settings/', include('api.settings.urls'), name='settings'),
]