from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Sum, F
from django.core.paginator import Paginator
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponse

# Import untuk Django Rest Framework (Dashboard Grafik)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

# Import Model & Form
from .models import Item, Transaction
from .forms import ItemForm, TransactionForm

# --- 1. DASHBOARD & LIST ---

@login_required
def item_list(request):
    """
    Menampilkan daftar barang dengan fitur pencarian, paginasi, 
    dan ringkasan statistik aset.
    """
    query = request.GET.get('q','')
    
    # Optimasi: Gunakan select_related untuk mengambil data ForeignKey dalam 1 query
    items = Item.objects.select_related('category', 'supplier').all().order_by('-created_at')

    if query:
        items = items.filter(
            Q(name__icontains=query) |
            Q(code__icontains=query) |
            Q(category__name__icontains=query) |
            Q(supplier__name__icontains=query)
        )

    # Paginasi (5 data per halaman)
    paginator = Paginator(items, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Statistik untuk Dashboard Cards
    total_items = Item.objects.count()
    stats = Item.objects.aggregate(
        total_stock=Sum('stock'),
        total_value=Sum(F('stock') * F('price'))
    )

    return render(request, 'inventory/item_list.html', {
        'page_obj': page_obj,
        'query': query,
        'total_items': total_items,
        'total_stock': stats['total_stock'] or 0,
        'total_value': stats['total_value'] or 0,
        'transaction_form': TransactionForm(),
    })

# --- 2. CRUD OPERATIONS (ITEM) ---

@login_required
def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save()

            #TAMBAHAN: Catat Stok Awal sebagai Transaksi IN otomatis saat buat barang baru
            if item.stock > 0:
                Transaction.objects.create(
                    item=item,
                    transaction_type='IN',
                    quantity=item.stock,
                    user=request.user 
                )

            messages.success(request, f"Barang '{item.name}' berhasil ditambahkan!")
            return redirect('item_list')
    else:
        form = ItemForm()
    return render(request, 'inventory/item_form.html', {'form': form})

@login_required
def item_update(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.info(request, f"Data '{item.name}' telah diperbarui.")
            return redirect('item_list')
    else:
        form = ItemForm(instance=item)
    return render(request, 'inventory/item_form.html', {'form': form})

@login_required
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        nama_barang = item.name
        item.delete()
        messages.warning(request, f"Barang '{nama_barang}' telah dihapus dari sistem.")
        return redirect('item_list')
    return render(request, 'inventory/item_confirm_delete.html', {'item': item})

# --- 3. TRANSACTION LOGIC ---

@login_required
def add_transaction(request, item_id):
    """
    Menangani mutasi stok (IN/OUT) dengan validasi ketersediaan stok.
    """
    item = get_object_or_404(Item, id=item_id)
    
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.item = item
            transaction.user = request.user 
            
            # Logika Update Stok
            if transaction.transaction_type == 'IN':
                item.stock += transaction.quantity
                item.save()
                transaction.save()
                messages.success(request, f"Stok {item.name} berhasil ditambah!")
            elif transaction.transaction_type == 'OUT':
                if item.stock >= transaction.quantity:
                    item.stock -= transaction.quantity
                    item.save()
                    transaction.save()
                    messages.success(request, f"Stok {item.name} berhasil dikurangi!")
                else:
                    messages.error(request, f"Gagal! Stok {item.name} tidak mencukupi.")
            
            return redirect('item_list')
    
    return redirect('item_list')

@login_required
def transaction_history(request):
    """
    Menampilkan riwayat mutasi dengan filter tanggal.
    """
    transactions = Transaction.objects.select_related('item', 'user').all().order_by('-timestamp')
    
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date:
        transactions = transactions.filter(timestamp__date__gte=start_date)
    if end_date:
        transactions = transactions.filter(timestamp__date__lte=end_date)

    # Tambahkan paginasi untuk history agar tidak berat saat data banyak
    paginator = Paginator(transactions, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'inventory/transaction_history.html', {
        'page_obj': page_obj,
        'start_date': start_date,
        'end_date': end_date
    })

# --- 4. EXPORT DATA ---

@login_required
def export_transactions_csv(request):
    import csv
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="laporan_mutasi.csv"'

    writer = csv.writer(response)
    writer.writerow(['Waktu', 'Petugas', 'Barang', 'Tipe', 'Jumlah'])

    transactions = Transaction.objects.all().order_by('-timestamp')
    
    # Filter tetap berlaku di ekspor CSV
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and start_date != "":
        transactions = transactions.filter(timestamp__date__gte=start_date)
    if end_date and end_date != "":
        transactions = transactions.filter(timestamp__date__lte=end_date)

    for t in transactions:
        writer.writerow([
            t.timestamp.strftime('%Y-%m-%d %H:%M'),
            t.user.username if t.user else 'System',
            t.item.name,
            t.get_transaction_type_display(),
            t.quantity
        ])

    return response

# --- 5. API FOR CHART.JS (Django Rest Framework) ---

class InventoryChartData(APIView):
    """
    Endpoint untuk menyediakan data JSON bagi Chart.js di frontend.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        today = timezone.now().date()
        labels = []
        data_in = []
        data_out = []

        # Menghitung data 7 hari ke belakang
        for i in range(6, -1, -1):
            date = today - timedelta(days=i)
            labels.append(date.strftime("%d %b"))

            # Agregasi jumlah mutasi per tipe per hari
            in_qty = Transaction.objects.filter(
                timestamp__date=date, 
                transaction_type='IN'
            ).aggregate(total=Sum('quantity'))['total'] or 0

            out_qty = Transaction.objects.filter(
                timestamp__date=date, 
                transaction_type='OUT'
            ).aggregate(total=Sum('quantity'))['total'] or 0

            data_in.append(in_qty)
            data_out.append(out_qty)

        return Response({
            "labels": labels,
            "datasets": [
                {
                    "label": "Masuk",
                    "data": data_in,
                    "borderColor": "#198754",
                    "backgroundColor": "rgba(25, 135, 84, 0.1)",
                    "tension": 0.3,
                    "fill": True
                },
                {
                    "label": "Keluar",
                    "data": data_out,
                    "borderColor": "#dc3545",
                    "backgroundColor": "rgba(220, 53, 69, 0.1)",
                    "tension": 0.3,
                    "fill": True
                }
            ]
        })