# 📦 Inventory System Django

Sistem manajemen inventaris berbasis web yang dirancang untuk membantu tim gudang atau operasional dalam mengelola stok barang, mencatat mutasi masuk/keluar, serta memantau kondisi inventaris secara real-time.

## ✨ Fitur Utama

- **Dashboard Interaktif**: Menampilkan ringkasan aset, jumlah item, total stok fisik, serta grafik tren mutasi stok.
- **Grafik Analitik**:
  - Grafik line 7 hari terakhir untuk mutasi stok masuk/keluar.
  - Grafik doughnut untuk komposisi nilai aset per kategori.
- **Sistem Mutasi Stok**: Mencatat stok masuk (IN) dan keluar (OUT) dengan validasi otomatis.
- **Riwayat Mutasi**: Menyimpan jejak aktivitas yang mencatat siapa, kapan, dan apa yang dimutasi.
- **Peringatan Stok Rendah**: Menampilkan pemberitahuan otomatis jika stok berada di bawah ambang batas.
- **Role-Based Access**:
  - **Admin**: mengelola barang, kategori, supplier, import/export Excel, dan fitur sistem.
  - **Manager**: dapat melihat data dan laporan, tetapi tidak mengubah master data.
  - **Operator**: dapat melakukan mutasi stok dan melihat riwayat.
- **Import & Export Excel**: Mendukung ekspor data barang ke file Excel serta impor data barang secara massal.
- **Search & Pagination**: Pencarian barang berdasarkan nama, kode, kategori, atau supplier.
- **Export CSV Laporan Mutasi**: Menyediakan laporan mutasi dalam format CSV berdasarkan filter tanggal.

## 🛠️ Tech Stack

- **Backend**: Python 3.x, Django 6.0.2
- **Frontend**: Bootstrap 5, Bootstrap Icons, Chart.js
- **Database**: SQLite (default)
- **API**: Django REST Framework

## 🚀 Cara Menjalankan Project

### 1. Clone Repository
```bash
git clone https://github.com/zatra19/inventory-system-django.git
cd inventory-system-django
```

### 2. Setup Virtual Environment
```bash
# Buat virtual environment
python -m venv .venv

# Aktivasi venv (Windows)
.venv\Scripts\activate

# Aktivasi venv (Mac/Linux)
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Migration & Setup
```bash
# Jalankan migrasi database
python manage.py makemigrations
python manage.py migrate

# Buat akun admin (Superuser)
python manage.py createsuperuser
```

### 5. Jalankan Server
```bash
python manage.py runserver
```

Buka browser dan akses aplikasi di: http://127.0.0.1:8000

## 👤 Pengaturan Akun & Role

Setelah login, akses fitur akan ditentukan berdasarkan role pengguna:

- **Admin**: akses penuh ke fitur manajemen dan ekspor/impor data.
- **Manager**: melihat dashboard, detail barang, riwayat, dan laporan.
- **Operator**: melakukan mutasi stok dan melihat riwayat.

Untuk mengatur role, gunakan halaman Django Admin (`/admin/`) dan tambahkan user ke group yang sesuai, misalnya `Admin`, `Manager`, atau `Operator`.

## 📘 Dokumentasi

Untuk panduan lengkap penggunaan aplikasi, silakan baca:
- [MANUAL_GUIDE_INVENTORY_SYSTEM.md](MANUAL_GUIDE_INVENTORY_SYSTEM.md)

## 📊 Roadmap

- [x] Dashboard grafik interaktif
- [x] Role-based access (Admin / Manager / Operator)
- [x] Import & export Excel
- [x] Peringatan stok rendah
- [ ] Desktop wrapper
- [ ] Barcode scanner
- [ ] Integrasi notifikasi email lanjutan

## 🤝 Kontribusi

Kontribusi sangat terbuka. Jika Anda ingin berkontribusi:

1. Fork repository ini.
2. Buat branch fitur baru.
3. Commit perubahan Anda.
4. Push ke branch Anda.
5. Buat Pull Request.

---

Dibuat dengan ❤️ oleh [zatra19](https://github.com/zatra19)
