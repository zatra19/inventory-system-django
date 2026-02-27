from django.urls import path
from . import views

urlpatterns = [
    path('', views.item_list, name='item_list'),
    path('add/', views.item_create, name='item_create'),
    path('edit/<int:pk>/', views.item_update, name='item_update'),
    path('delete/<int:pk>/', views.item_delete, name='item_delete'),
    path('transaction/add/<int:item_id>/', views.add_transaction, name='add_transaction'),
    path('transactions/', views.transaction_history, name='transaction_history'),
]

