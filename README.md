# 📦 Inventory System Django

Sistem manajemen inventaris berbasis web yang dirancang untuk memudahkan pelacakan stok barang, mutasi (masuk/keluar), serta pelaporan aktivitas gudang secara *real-time*.

## ✨ Fitur Utama

* **Dashboard Modern**: Ringkasan total barang, total stok, dan estimasi nilai aset.
* **Sistem Mutasi Stok**: Pencatatan stok masuk (IN) dan keluar (OUT) dengan validasi otomatis.
* **Audit Trail (Riwayat)**: Jejak aktivitas yang mencatat siapa (petugas), kapan, dan apa yang dimutasi.
* **Peringatan Stok Rendah**: Indikator visual otomatis jika stok berada di bawah ambang batas (*threshold*).
* **Laporan Multi-format**:
    * Cetak Laporan ke PDF melalui browser.
    * Ekspor data ke format Excel (CSV) berdasarkan filter tanggal.
* **Sistem Keamanan**: Autentikasi user untuk memastikan hanya petugas berwenang yang bisa melakukan mutasi.
* **Search & Pagination**: Pencarian barang berdasarkan nama, kode, kategori, atau supplier.

## 🛠️ Tech Stack

* **Backend**: Python 3.x, Django 6.0.2
* **Frontend**: Bootstrap 5, Bootstrap Icons
* **Database**: SQLite (Default) / PostgreSQL (Optional)

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
Pastikan Anda sudah menginstal semua library yang diperlukan:
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

📊 Rencana Pengembangan (Roadmap)
* [✅] Dashboard Grafik: Integrasi Chart.js untuk visualisasi tren stok.

* [ ] Notifikasi: Pengiriman email otomatis saat stok mencapai batas kritis.

* [ ] Desktop Wrapper: Mengonversi web app menjadi aplikasi desktop (Windows/macOS).

* [ ] Barcode Scanner: Integrasi kamera untuk input barang lebih cepat.

🤝 Kontribusi
Kontribusi sangat terbuka! Jika Anda ingin memperbaiki bug atau menambah fitur:

1. Fork Repository ini.

2. Buat Branch fitur baru (git checkout -b feature/FiturKeren).

3. Commit perubahan Anda (git commit -m 'Menambahkan Fitur Keren').

4. Push ke Branch (git push origin feature/FiturKeren).

5. Buat Pull Request.


Dibuat dengan ❤️ oleh [zatra19]
