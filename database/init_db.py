import sqlite3
import os

def init_db():
    db_path = os.path.join(os.path.dirname(__file__), 'pos_inventory.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Tabel User
    c.execute('''CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL,
        last_login TEXT,
        failed_attempts INTEGER DEFAULT 0,
        locked_until TEXT
    )''')
    # Tabel Kategori
    c.execute('''CREATE TABLE IF NOT EXISTS kategori (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT UNIQUE NOT NULL
    )''')
    # Tabel Produk
    c.execute('''CREATE TABLE IF NOT EXISTS produk (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT NOT NULL,
        kategori_id INTEGER,
        harga REAL NOT NULL,
        stok INTEGER NOT NULL,
        FOREIGN KEY (kategori_id) REFERENCES kategori(id)
    )''')
    # Tabel Transaksi
    c.execute('''CREATE TABLE IF NOT EXISTS transaksi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tanggal TEXT NOT NULL,
        user_id INTEGER,
        total REAL NOT NULL,
        FOREIGN KEY (user_id) REFERENCES user(id)
    )''')
    # Tabel Detail Transaksi
    c.execute('''CREATE TABLE IF NOT EXISTS detail_transaksi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        transaksi_id INTEGER,
        produk_id INTEGER,
        qty INTEGER NOT NULL,
        harga REAL NOT NULL,
        FOREIGN KEY (transaksi_id) REFERENCES transaksi(id),
        FOREIGN KEY (produk_id) REFERENCES produk(id)
    )''')
    conn.commit()
    
    # Inisialisasi data default jika belum ada
    init_default_data(conn)
    
    conn.close()

def init_default_data(conn):
    """Inisialisasi data default jika belum ada"""
    c = conn.cursor()
    
    # Cek apakah sudah ada user
    c.execute("SELECT COUNT(*) FROM user")
    user_count = c.fetchone()[0]
    
    if user_count == 0:
        # Tambahkan user default
        c.execute("INSERT INTO user (username, password, role) VALUES (?, ?, ?)", 
                 ("admin", "admin123", "Admin"))
        c.execute("INSERT INTO user (username, password, role) VALUES (?, ?, ?)", 
                 ("kasir", "kasir123", "Kasir"))
        print("User default berhasil ditambahkan.")
    
    # Cek apakah sudah ada kategori
    c.execute("SELECT COUNT(*) FROM kategori")
    kategori_count = c.fetchone()[0]
    
    if kategori_count == 0:
        # Tambahkan kategori default
        kategori_default = [
            ("Makanan",),
            ("Minuman",),
            ("Alat Tulis",),
            ("Elektronik",),
            ("Lainnya",)
        ]
        c.executemany("INSERT INTO kategori (nama) VALUES (?)", kategori_default)
        print("Kategori default berhasil ditambahkan.")
        
        # Ambil ID kategori yang baru ditambahkan
        c.execute("SELECT id, nama FROM kategori")
        kategori_ids = {nama: id for id, nama in c.fetchall()}
        
        # Tambahkan produk default
        produk_default = [
            ("Mie Instan", kategori_ids["Makanan"], 3500, 50),
            ("Roti Tawar", kategori_ids["Makanan"], 12000, 20),
            ("Air Mineral 600ml", kategori_ids["Minuman"], 4000, 100),
            ("Teh Botol", kategori_ids["Minuman"], 5000, 50),
            ("Kopi Sachet", kategori_ids["Minuman"], 2000, 100),
            ("Buku Tulis", kategori_ids["Alat Tulis"], 5000, 30),
            ("Pulpen", kategori_ids["Alat Tulis"], 3000, 50),
            ("Pensil", kategori_ids["Alat Tulis"], 2500, 40),
            ("Charger HP", kategori_ids["Elektronik"], 25000, 10),
            ("Baterai AA", kategori_ids["Elektronik"], 12000, 24)
        ]
        c.executemany("INSERT INTO produk (nama, kategori_id, harga, stok) VALUES (?, ?, ?, ?)", produk_default)
        print("Produk default berhasil ditambahkan.")
    
    # Simpan perubahan
    conn.commit()

if __name__ == "__main__":
    init_db()
    print("Database berhasil diinisialisasi.")