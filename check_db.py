import sqlite3
import os

def check_database():
    # Path database
    db_path = os.path.join(os.path.dirname(__file__), 'database', 'pos_inventory.db')
    
    # Periksa apakah file database ada
    if not os.path.exists(db_path):
        print("File database tidak ditemukan!")
        return
    
    # Buat koneksi ke database
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Untuk akses kolom dengan nama
    cursor = conn.cursor()
    
    # Periksa tabel user
    try:
        cursor.execute("SELECT * FROM user")
        users = cursor.fetchall()
        
        if not users:
            print("Tabel user kosong! Tidak ada user yang terdaftar.")
        else:
            print(f"Jumlah user dalam database: {len(users)}")
            print("\nDaftar user:")
            for user in users:
                print(f"ID: {user['id']}, Username: {user['username']}, Password: {user['password']}, Role: {user['role']}")
        
        # Periksa apakah user default ada
        cursor.execute("SELECT * FROM user WHERE username = 'admin'")
        admin = cursor.fetchone()
        
        cursor.execute("SELECT * FROM user WHERE username = 'kasir'")
        kasir = cursor.fetchone()
        
        if not admin:
            print("\nUser admin tidak ditemukan!")
        else:
            print(f"\nUser admin ditemukan dengan password: {admin['password']}")
        
        if not kasir:
            print("User kasir tidak ditemukan!")
        else:
            print(f"User kasir ditemukan dengan password: {kasir['password']}")
            
    except sqlite3.Error as e:
        print(f"Error saat memeriksa database: {e}")
    
    # Tutup koneksi
    conn.close()

if __name__ == "__main__":
    check_database()