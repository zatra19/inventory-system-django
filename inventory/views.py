from django.shortcuts import render, redirect, get_object_or_404
from .models import Item
from .forms import ItemForm
from django.db.models import Q
from django.db.models import Sum, F
from django.core.paginator import Paginator
from django.contrib import messages  # <-- 1. Tambahkan Import Ini

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