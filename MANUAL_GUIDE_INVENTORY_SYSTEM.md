# Manual Guide Aplikasi Inventory System

## 1. Pendahuluan

Aplikasi Inventory System adalah sistem manajemen stok barang yang digunakan untuk membantu tim operasional mengelola data barang, memantau stok, mencatat mutasi stok, serta melakukan impor/ekspor data melalui Excel.

Dokumen ini bertujuan untuk memberikan panduan penggunaan aplikasi secara formal, lengkap, dan mudah dipahami oleh pengguna, baik admin maupun operator.

## 2. Tujuan Aplikasi

Aplikasi ini digunakan untuk:
- mencatat dan mengelola data barang,
- mengatur kategori dan supplier,
- memantau stok barang secara real-time,
- mencatat transaksi masuk/keluar barang,
- mengidentifikasi barang stok rendah,
- melakukan impor dan ekspor data barang melalui Excel.

## 3. Hak Akses Pengguna

Aplikasi ini mendukung mekanisme role-based access dengan dua peran utama:

### 3.1 Admin
Admin memiliki akses penuh terhadap fitur berikut:
- menambah, mengedit, dan menghapus barang,
- mengelola kategori,
- mengelola supplier,
- melakukan impor dan ekspor Excel,
- melihat dashboard dan riwayat mutasi,
- mengatur batas stok rendah per item.

### 3.2 Operator
Operator memiliki akses terbatas untuk:
- melihat data barang,
- melakukan mutasi stok (masuk/keluar),
- melihat detail barang dan riwayat mutasi,
- melihat dashboard dan informasi stok rendah.

## 4. Persyaratan Sistem

Untuk menjalankan aplikasi, pengguna memerlukan:
- browser modern (Chrome, Edge, Firefox),
- koneksi internet untuk akses web,
- akun pengguna yang telah dibuat oleh admin atau sistem.

## 5. Langkah Masuk ke Aplikasi

### 5.1 Login
1. Buka aplikasi melalui browser.
2. Masuk ke halaman login.
3. Masukkan username dan password.
4. Klik tombol Masuk.

### 5.2 Logout
1. Klik tombol Keluar yang berada di kanan atas halaman.
2. Sistem akan mengakhiri sesi pengguna.

## 6. Tampilan Utama (Dashboard)

Setelah login, pengguna akan melihat dashboard dengan informasi berikut:
- total nilai aset inventory,
- total jenis barang,
- total stok fisik,
- daftar barang yang termasuk stok rendah,
- grafik tren mutasi stok,
- daftar barang utama.

### 6.1 Fungsi Utama Dashboard
- memberikan gambaran umum kondisi stok,
- memudahkan identifikasi barang yang perlu perhatian,
- menjadi pusat navigasi ke fitur lain.

## 7. Mengelola Barang

### 7.1 Menambah Barang Baru
1. Buka halaman Dashboard.
2. Klik tombol Tambah Barang.
3. Isi formulir berikut:
   - Nama Barang
   - Kode Barang
   - Kategori
   - Supplier
   - Stok
   - Harga
   - Ambang Stok Rendah
4. Klik Simpan Perubahan.

### 7.2 Mengedit Data Barang
1. Pilih barang yang ingin diubah dari daftar barang.
2. Klik tombol edit.
3. Perbarui data sesuai kebutuhan.
4. Klik Simpan Perubahan.

### 7.3 Menghapus Barang
1. Pilih barang yang ingin dihapus.
2. Klik tombol hapus.
3. Konfirmasi penghapusan.
4. Barang akan terhapus dari sistem.

### 7.4 Melihat Detail Barang
1. Pilih barang dari daftar.
2. Klik tombol detail (ikon informasi).
3. Sistem akan menampilkan:
   - informasi barang,
   - status stok,
   - ambang stok rendah,
   - riwayat mutasi barang.

## 8. Mengelola Kategori

Kategori digunakan untuk mengelompokkan barang berdasarkan jenis atau kelompok tertentu.

### 8.1 Menambah Kategori
1. Buka menu Kategori.
2. Klik tombol Tambah Kategori.
3. Masukkan nama kategori.
4. Simpan.

### 8.2 Mengedit Kategori
1. Pilih kategori yang ingin diubah.
2. Klik tombol edit.
3. Perbarui nama kategori.
4. Simpan perubahan.

### 8.3 Menghapus Kategori
1. Pilih kategori yang ingin dihapus.
2. Klik tombol hapus.
3. Konfirmasi penghapusan.

## 9. Mengelola Supplier

Supplier digunakan untuk mencatat pemasok barang.

### 9.1 Menambah Supplier
1. Buka menu Supplier.
2. Klik tombol Tambah Supplier.
3. Isi data berikut:
   - Nama Supplier
   - Nomor Telepon
   - Email
4. Simpan data.

### 9.2 Mengedit Supplier
1. Pilih supplier yang ingin diubah.
2. Klik tombol edit.
3. Ubah data yang diperlukan.
4. Simpan perubahan.

### 9.3 Menghapus Supplier
1. Pilih supplier yang ingin dihapus.
2. Klik tombol hapus.
3. Konfirmasi penghapusan.

## 10. Melakukan Mutasi Stok

Mutasi stok adalah aktivitas perubahan jumlah barang karena masuk atau keluar stok.

### 10.1 Stok Masuk
Digunakan ketika barang diterima atau ditambahkan ke stok.
1. Pilih barang yang akan dimutasi.
2. Klik tombol Mutasi.
3. Pilih jenis transaksi: Masuk.
4. Masukkan jumlah barang.
5. Simpan transaksi.

### 10.2 Stok Keluar
Digunakan ketika barang dipakai, dijual, atau dikurangi dari stok.
1. Pilih barang yang akan dimutasi.
2. Klik tombol Mutasi.
3. Pilih jenis transaksi: Keluar.
4. Masukkan jumlah barang.
5. Simpan transaksi.

### 10.3 Catatan Penting
- stok keluar tidak boleh melebihi stok yang tersedia,
- sistem akan menolak transaksi jika stok tidak mencukupi,
- setiap transaksi akan tercatat di riwayat mutasi.

## 11. Memahami Stok Rendah dan Threshold

Setiap barang dapat memiliki ambang batas stok rendah yang ditentukan secara terpisah.

### 11.1 Fungsi Threshold
Threshold stok rendah digunakan untuk memberi peringatan saat stok mendekati batas minimum.

### 11.2 Cara Kerja
- jika stok barang lebih kecil atau sama dengan threshold, barang dianggap stok rendah,
- sistem akan menampilkan peringatan pada dashboard,
- barang akan terlihat pada daftar stok rendah.

### 11.3 Tips Penggunaan
Gunakan threshold secara realistis sesuai kebutuhan bisnis, misalnya:
- barang fast-moving: threshold lebih rendah,
- barang slow-moving: threshold dapat lebih tinggi.

## 12. Import Data Excel

Fitur import Excel digunakan untuk memasukkan atau memperbarui data barang secara massal.

### 12.1 Format File Excel
File Excel yang dapat diimpor harus memiliki kolom berikut:
- Aksi
- Kode
- Nama
- Kategori
- Supplier
- Stok
- Mode Stok
- Harga
- Ambang Stok Rendah

### 12.2 Penjelasan Kolom
- Aksi: isi dengan Baru atau Update.
- Kode: kode unik barang, digunakan sebagai identitas utama.
- Nama: nama barang.
- Kategori: nama kategori barang.
- Supplier: nama supplier.
- Stok: nilai stok yang akan diproses.
- Mode Stok: pilih Set, Tambah, atau Kurangi.
- Harga: harga barang per unit.
- Ambang Stok Rendah: batas stok rendah.

### 12.3 Langkah Import
1. Buka halaman Dashboard.
2. Pilih file Excel yang ingin diimpor.
3. Klik tombol Import Excel.
4. Sistem akan memproses data.
5. Setelah selesai, aplikasi akan menampilkan hasil import.

### 12.4 Keterangan Logika Import
- Aksi Baru: membuat barang baru.
- Aksi Update: memperbarui barang yang sudah ada berdasarkan kode.
- Mode Set: mengganti stok menjadi nilai yang ada di file.
- Mode Tambah: menambah stok lama dengan nilai yang ada di file.
- Mode Kurangi: mengurangi stok lama dengan nilai yang ada di file.

### 12.5 Tips Agar Import Berhasil
- pastikan kolom header sesuai format,
- pastikan kode barang unik untuk data baru,
- hindari mengisi data yang tidak konsisten,
- cek data kategori dan supplier sebelum import,
- gunakan file yang sudah berisi contoh format agar lebih aman.

## 13. Export Data Excel

Fitur export Excel memungkinkan pengguna mengekspor data barang ke file Excel.

### 13.1 Langkah Export
1. Buka halaman Dashboard.
2. Klik tombol Export Excel.
3. File Excel akan diunduh otomatis.

### 13.2 Kegunaan Export
- backup data barang,
- berbagi data dengan tim,
- mempersiapkan data untuk import ulang.

## 14. Riwayat Mutasi dan Laporan

### 14.1 Riwayat Mutasi
User dapat melihat seluruh kegiatan mutasi stok dari menu Riwayat.

### 14.2 Fitur yang Tersedia
- filter berdasarkan tanggal,
- melihat detail transaksi,
- melihat siapa yang melakukan transaksi,
- mengekspor data mutasi ke CSV.

## 15. Best Practice Penggunaan Aplikasi

### 15.1 Sebelum Input Data
- siapkan data barang dengan lengkap,
- pastikan kode barang konsisten,
- gunakan kategori dan supplier yang sudah ada apabila memungkinkan.

### 15.2 Saat Melakukan Stok Masuk/Keluar
- cek stok sebelum melakukan transaksi keluar,
- catat alasan perubahan stok bila perlu,
- gunakan mutasi secara konsisten untuk menjaga akurasi data.

### 15.3 Saat Melakukan Import Excel
- gunakan file template yang sudah disediakan,
- hindari mengubah struktur kolom secara acak,
- lakukan uji import pada data kecil terlebih dahulu.

## 16. Troubleshooting

### 16.1 Tidak Bisa Login
- cek username dan password,
- pastikan akun aktif,
- hubungi admin jika akun belum diberikan akses.

### 16.2 Import Excel Gagal
- cek format header,
- pastikan file berekstensi .xlsx,
- periksa nilai kolom Aksi dan Mode Stok,
- cek apakah kode barang sudah ada untuk aksi Baru.

### 16.3 Stok Tidak Berubah Setelah Mutasi
- periksa apakah transaksi berhasil disimpan,
- cek apakah stok keluar melebihi stok yang tersedia,
- lihat riwayat mutasi untuk memastikan catatan transaksi ada.

## 17. Penutup

Aplikasi Inventory System dirancang untuk membantu perusahaan atau tim operasional dalam mengelola stok barang secara lebih terorganisir, akurat, dan efisien. Dengan pemahaman yang baik terhadap fitur-fitur yang tersedia, pengguna dapat memaksimalkan manfaat sistem ini dalam aktivitas harian.

## 18. Lampiran

### Contoh Format Import Excel

| Aksi | Kode | Nama | Kategori | Supplier | Stok | Mode Stok | Harga | Ambang Stok Rendah |
|---|---|---|---|---|---|---|---|---|
| Baru | BRG001 | Mouse Logitech | Elektronik | PT Contoh | 20 | Set | 150000 | 5 |
| Update | BRG001 | Mouse Logitech Pro | Elektronik | PT Contoh | 3 | Tambah | 180000 | 7 |

### Catatan
- Gunakan kode barang yang konsisten.
- Pastikan data kategori dan supplier tersedia.
- Untuk data baru, gunakan Aksi Baru.
- Untuk data yang sudah ada, gunakan Aksi Update.
