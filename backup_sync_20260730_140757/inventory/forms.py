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
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter item name'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter item code'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter stock'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price'}),
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