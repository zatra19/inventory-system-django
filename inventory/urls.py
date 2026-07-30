from django.urls import path
from . import views

urlpatterns = [
    # --- Item Management ---
    path('', views.item_list, name='item_list'),
    path('add/', views.item_create, name='item_create'),
    path('detail/<int:pk>/', views.item_detail, name='item_detail'),
    path('edit/<int:pk>/', views.item_update, name='item_update'),
    path('delete/<int:pk>/', views.item_delete, name='item_delete'),
    
    # --- Transaction Management ---
    path('transaction/add/<int:item_id>/', views.add_transaction, name='add_transaction'),
    path('transactions/', views.transaction_history, name='transaction_history'),
    
    # --- Category & Supplier ---
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_create, name='category_create'),
    path('categories/edit/<int:pk>/', views.category_update, name='category_update'),
    path('categories/delete/<int:pk>/', views.category_delete, name='category_delete'),

    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('suppliers/add/', views.supplier_create, name='supplier_create'),
    path('suppliers/edit/<int:pk>/', views.supplier_update, name='supplier_update'),
    path('suppliers/delete/<int:pk>/', views.supplier_delete, name='supplier_delete'),
    
    # --- Export/Import Data ---
    path('export/items/excel/', views.export_items_excel, name='export_items_excel'),
    path('import/items/excel/', views.import_items_excel, name='import_items_excel'),
    path('export/csv/', views.export_transactions_csv, name='export_transactions_csv'),
    
    # --- API Endpoints (Untuk Chart.js) ---
    # Gunakan .as_view() karena InventoryChartData adalah Class-Based View (CBV)
    path('api/chart/inventory/', views.InventoryChartData.as_view(), name='api_inventory_chart'),
]