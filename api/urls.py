from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.categories_list, name='categories-list'),
    path('expenses/', views.expenses_list, name='expenses-list'),
    path('settings/', views.settings_view, name='settings-view'),
]