from django.urls import path
from . import views

urlpatterns = [
    # --- Item Management ---
    path('', views.item_list, name='item_list'),
    path('add/', views.item_create, name='item_create'),
    path('edit/<int:pk>/', views.item_update, name='item_update'),
    path('delete/<int:pk>/', views.item_delete, name='item_delete'),
    
    # --- Transaction Management ---
    path('transaction/add/<int:item_id>/', views.add_transaction, name='add_transaction'),
    path('transactions/', views.transaction_history, name='transaction_history'),
    
    # --- Export Data ---
    path('export/csv/', views.export_transactions_csv, name='export_transactions_csv'),

    # --- API Endpoints (Untuk Chart.js) ---
    # Gunakan .as_view() karena InventoryChartData adalah Class-Based View (CBV)
    path('api/chart/inventory/', views.InventoryChartData.as_view(), name='api_inventory_chart'),
]