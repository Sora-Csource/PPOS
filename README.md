# Aplikasi POS & Inventory Management Offline

Aplikasi Point of Sale (POS) dan Inventory Management yang dapat dijalankan secara offline untuk mengelola penjualan dan inventaris produk.

## Fitur Utama

- **Login dan Manajemen User**
  - Multi-level user (Admin dan Kasir)
  - Autentikasi username dan password
  - Pengelolaan user (tambah, edit, hapus)

- **Dashboard**
  - Tampilan statistik (total produk, stok menipis, transaksi hari ini)
  - Menu navigasi ke semua modul

- **Pengelolaan Produk**
  - CRUD (Create, Read, Update, Delete) produk
  - Pencarian produk
  - Kategorisasi produk

- **Pengelolaan Kategori**
  - CRUD kategori produk
  - Melihat jumlah produk per kategori

- **Transaksi**
  - Pembuatan transaksi penjualan
  - Keranjang belanja
  - Pencarian produk saat transaksi
  - Pencetakan struk

- **Laporan**
  - Laporan penjualan dengan filter tanggal
  - Laporan produk terlaris
  - Laporan stok menipis
  - Ekspor data ke Excel

- **Pengaturan**
  - Konfigurasi informasi toko
  - Pengaturan struk
  - Pengaturan tampilan aplikasi

## Struktur Aplikasi

```
.
├── database/                  # Modul database
│   ├── database.py           # Kelas Database untuk operasi database
│   └── init_db.py            # Inisialisasi struktur database
├── modules/                   # Modul-modul aplikasi
│   ├── dashboard/            # Modul dashboard
│   ├── kategori/             # Modul pengelolaan kategori
│   ├── laporan/              # Modul laporan dan ekspor data
│   ├── produk/               # Modul pengelolaan produk
│   ├── setting/              # Modul pengaturan aplikasi
│   ├── struk/                # Modul pencetakan struk
│   ├── transaksi/            # Modul transaksi penjualan
│   └── user/                 # Modul login dan pengelolaan user
├── main.py                    # File utama aplikasi
└── settings.json              # File konfigurasi aplikasi
```

## Cara Penggunaan

1. **Instalasi**
   - Pastikan Python 3.6+ sudah terinstal
   - Instal dependensi: `pip install pandas openpyxl`

2. **Menjalankan Aplikasi**
   - Jalankan file `main.py`: `python main.py`
   - Login dengan username dan password default:
     - Admin: username `admin`, password `admin123`
     - Kasir: username `kasir`, password `kasir123`

3. **Penggunaan Dasar**
   - Setelah login, Anda akan diarahkan ke Dashboard
   - Navigasi ke modul yang diinginkan melalui menu di Dashboard
   - Untuk transaksi baru, pilih menu "Transaksi Baru"
   - Untuk melihat laporan, pilih menu "Laporan Penjualan"

## Pencetakan Struk

Aplikasi mendukung pencetakan struk dengan dua cara:
1. **Preview di Browser**: Struk akan ditampilkan di browser dan dapat dicetak
2. **Simpan ke File**: Struk dapat disimpan sebagai file teks

## Ekspor Data

Data transaksi dan laporan dapat diekspor ke format Excel (.xlsx) untuk analisis lebih lanjut atau keperluan pelaporan.

## Pengembangan Selanjutnya

- Integrasi dengan printer termal
- Fitur barcode scanner
- Fitur diskon dan promo
- Manajemen supplier
- Fitur retur barang
- Sinkronisasi data ke cloud

---

© 2023 POS & Inventory Management System