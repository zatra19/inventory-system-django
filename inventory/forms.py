from django import forms
from .models import Item, Category, Supplier, Transaction

class ItemForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Pilih Kategori",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    supplier = forms.ModelChoiceField(
        queryset=Supplier.objects.all(),
        empty_label="Pilih Supplier",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Item
        fields = ['name', 'code', 'category', 'supplier', 'stock', 'price', 'low_stock_threshold']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter item name'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter item code'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter stock', 'min': '0'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price', 'min': '0', 'step': '0.01'}),
            'low_stock_threshold': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Threshold stok rendah', 'min': '0'}),
        }

    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock is None or stock < 0:
            raise forms.ValidationError('Stok harus bernilai nol atau positif.')
        return stock

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is None or price < 0:
            raise forms.ValidationError('Harga harus bernilai nol atau positif.')
        return price

    def clean_low_stock_threshold(self):
        threshold = self.cleaned_data.get('low_stock_threshold')
        if threshold is None or threshold < 0:
            raise forms.ValidationError('Ambang stok rendah harus bernilai nol atau positif.')
        return threshold


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama kategori'}),
        }


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'phone', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama supplier'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nomor telepon'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email supplier'}),
        }


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        # Kita hanya butuh input tipe dan jumlah dari user
        fields = ['transaction_type', 'quantity']
        widgets = {
            'transaction_type': forms.Select(attrs={
                'class': 'form-select',
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan jumlah...',
                'min': '1' # Mencegah input angka negatif atau nol
            }),
        }

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity is None or quantity <= 0:
            raise forms.ValidationError('Jumlah harus lebih besar dari nol.')
        return quantity
