from django.contrib.auth.models import User
from django.test import TestCase
from .models import Category, Supplier, Item, Transaction
from .forms import ItemForm, TransactionForm


class InventoryModelFormTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Elektronik')
        self.supplier = Supplier.objects.create(name='PT Contoh', phone='0812345678', email='contoh@example.com')
        self.user = User.objects.create_user(username='tester', password='secret')

    def test_item_form_rejects_negative_stock(self):
        form = ItemForm(data={
            'name': 'Barang Tes',
            'code': 'TEST001',
            'category': self.category.id,
            'supplier': self.supplier.id,
            'stock': -1,
            'price': 10000,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('stock', form.errors)

    def test_transaction_form_rejects_non_positive_quantity(self):
        form = TransactionForm(data={
            'transaction_type': 'IN',
            'quantity': 0,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('quantity', form.errors)

    def test_item_stock_status_low_threshold(self):
        item = Item.objects.create(
            name='Printer', code='PRT001', category=self.category,
            supplier=self.supplier, stock=10, price=1500000
        )
        self.assertEqual(item.stock_status, 'warning')
        self.assertTrue(item.is_low_stock)

    def test_transaction_increases_quantity_model(self):
        transaction = Transaction.objects.create(
            item=Item.objects.create(
                name='Mouse', code='MSE001', category=self.category,
                supplier=self.supplier, stock=5, price=75000
            ),
            transaction_type='IN',
            quantity=5,
            user=self.user
        )
        self.assertEqual(transaction.quantity, 5)
