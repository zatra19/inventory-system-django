from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Sum, F
from django.core.paginator import Paginator
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta

from django.http import HttpResponse
from django.db.models.functions import TruncDate

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
        start_date = today - timedelta(days=6)  # 7 hari terakhir termasuk hari ini

        #1. Siapkan struktur dasar (array statis 7 hari)
        labels = [(start_date + timedelta(days=i)).strftime("%d %b") for i in range(7)]
        data_in = [0] * 7
        data_out = [0] * 7

        # 2. Optimasi ORM: Tarik dan kelompokan data mutasi sekaligus untuk 7 hari terakhir
        transactions = Transaction.objects.filter(
            timestamp__date__range=[start_date, today]
            ).annotate(
                date=TruncDate('timestamp')
            ).values('date', 'transaction_type').annotate(
                total=Sum('quantity')
            ).order_by('date')

        # 3. Petakan hasil query ke array berdasarkan index hari
        for t in transactions:
            if t['date']:
                # Hitung selisih hari untuk menentukan index array (0 sampai 6)
                delta = (t['date'] - start_date).days
                if 0 <= delta < 7:
                    if t['transaction_type'] == 'IN':
                        data_in[delta] = t['total']
                    elif t['transaction_type'] == 'OUT':
                        data_out[delta] = t['total']

        return Response({
            "labels": labels,
            "datasets": [
                {
                    "type": "bar", # Mengubah area menjadi Bar Chart
                    "label": "Barang Masuk",
                    "data": data_in,
                    "backgroundColor": "#198754", # Hijau Bootstrap
                    "borderRadius": 4, # Sudut tumpul pada bar
                },
                {
                    "type": "bar",
                    "label": "Barang Keluar",
                    "data": data_out,
                    "backgroundColor": "#dc3545", # Merah Bootstrap
                    "borderRadius": 4,
                }
            ]
        })

class AssetCategoryChartData(APIView):
    """
    Endpoint untuk Doughnut Chart: Total Nilai Aset per Kategori
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        # Asumsi relasi ForeignKey di Item adalah 'category' dan ada field 'name'
        categories = Item.objects.values('category__name').annotate(
            total_asset=Sum(F('stock') * F('price'))
        ).filter(total_asset__gt=0).order_by('-total_asset')

        labels = [cat['category__name'] for cat in categories]
        data = [cat['total_asset'] for cat in categories]

        return Response({
            "labels": labels,
            "datasets": [{
                "data": data,
                "backgroundColor": [
                    '#0d6efd', '#198754', '#ffc107', '#dc3545', '#0dcaf0', '#6c757d', '#6610f2'
                ],
                "borderWidth": 0
            }]
        })