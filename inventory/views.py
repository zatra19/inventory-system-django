from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, Transaction
from .forms import ItemForm, TransactionForm
from django.db.models import Q
from django.db.models import Sum, F
from django.core.paginator import Paginator
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_date

# --- LIST & SEARCH ---
def item_list(request):
    query = request.GET.get('q')
    items = Item.objects.all().order_by('-created_at') # Pakai '-' agar data terbaru di atas

    if query:
        items = items.filter(
            Q(name__icontains=query) |
            Q(code__icontains=query) |
            Q(category__name__icontains=query) |
            Q(supplier__name__icontains=query)
        )

    paginator = Paginator(items, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

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
        'transaction_form': TransactionForm(),  # Form untuk transaksi
    })

# --- CREATE ---
def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save()
            # 2. Tambahkan pesan sukses
            messages.success(request, f"Barang '{item.name}' berhasil ditambahkan!")
            return redirect('item_list')
    else:
        form = ItemForm()
    return render(request, 'inventory/item_form.html', {'form': form})

# --- UPDATE ---
def item_update(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            # 3. Tambahkan pesan info/success
            messages.info(request, f"Data '{item.name}' telah diperbarui.")
            return redirect('item_list')
    else:
        form = ItemForm(instance=item)
    return render(request, 'inventory/item_form.html', {'form': form})

# --- DELETE ---
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        nama_barang = item.name
        item.delete()
        # 4. Tambahkan pesan peringatan
        messages.warning(request, f"Barang '{nama_barang}' telah dihapus dari sistem.")
        return redirect('item_list')
    return render(request, 'inventory/item_confirm_delete.html', {'item': item})

# --- TRANSACTION ---
def add_transaction(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.item = item
            
            # Ganti 'transaction.type' menjadi 'transaction.transaction_type'
            if transaction.transaction_type == 'IN':
                item.stock += transaction.quantity
            elif transaction.transaction_type == 'OUT':
                if item.stock >= transaction.quantity:
                    item.stock -= transaction.quantity
                else:
                    messages.error(request, f"Stok tidak cukup untuk {item.name}!")
                    return redirect('item_list')
            
            item.save()
            transaction.save()
            messages.success(request, f"Stok {item.name} berhasil diperbarui!")
            return redirect('item_list')
    
    return redirect('item_list')

@login_required # Hanya yang login yang bisa akses fungsi ini
def add_transaction(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.item = item
            transaction.user = request.user # TANGKAP USER DISINI
            
            # ... logika update stok (IN/OUT) yang sudah kita buat sebelumnya ...
            
            transaction.save()
            item.save()
            messages.success(request, f"Transaksi untuk {item.name} berhasil ditambahkan!")
            return redirect('item_list')
        
def transaction_history(request):
    transactions = Transaction.objects.all().order_by('-timestamp')
    
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date:
        transactions = transactions.filter(timestamp__date__gte=start_date)
    if end_date:
        transactions = transactions.filter(timestamp__date__lte=end_date)

    return render(request, 'inventory/transaction_history.html', {
        'transactions': transactions,
        'start_date': start_date,
        'end_date': end_date
    })

def export_transactions_csv(request):
    import csv # Pastikan sudah di-import
    from django.http import HttpResponse

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="laporan_mutasi.csv"'

    writer = csv.writer(response)
    # Header kolom
    writer.writerow(['Waktu', 'Petugas', 'Barang', 'Tipe', 'Jumlah'])

    # 1. Ambil semua data awal
    transactions = Transaction.objects.all().order_by('-timestamp')
    
    # 2. Ambil parameter filter dari request.GET (Bukan dari objek transaksi!)
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and start_date != "None" and start_date != "":
        transactions = transactions.filter(timestamp__date__gte=start_date)
    
    if end_date and end_date != "None" and end_date != "":
        transactions = transactions.filter(timestamp__date__lte=end_date)

    # 3. Looping data transaksi
    for t in transactions:
        writer.writerow([
            t.timestamp.strftime('%Y-%m-%d %H:%M'),
            t.user.username if t.user else 'System', # Ambil username petugas
            t.item.name, # Nama barang
            t.get_transaction_type_display(), # 'Stock In' atau 'Stock Out'
            t.quantity # Jumlahnya
        ])

    return response