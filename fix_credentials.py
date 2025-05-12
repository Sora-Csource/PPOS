import sqlite3
import os

def fix_credentials():
    # Path database
    db_path = os.path.join(os.path.dirname(__file__), 'database', 'pos_inventory.db')
    
    # Periksa apakah file database ada
    if not os.path.exists(db_path):
        print("File database tidak ditemukan!")
        return False
    
    # Buat koneksi ke database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Periksa apakah user admin ada
        cursor.execute("SELECT * FROM user WHERE username = 'admin'")
        admin = cursor.fetchone()
        
        # Periksa apakah user kasir ada
        cursor.execute("SELECT * FROM user WHERE username = 'kasir'")
        kasir = cursor.fetchone()
        
        # Jika user admin tidak ada, tambahkan
        if not admin:
            cursor.execute("INSERT INTO user (username, password, role) VALUES (?, ?, ?)", 
                         ("admin", "admin123", "Admin"))
            print("User admin berhasil ditambahkan dengan password: admin123")
        else:
            # Update password admin
            cursor.execute("UPDATE user SET password = ? WHERE username = ?", 
                         ("admin123", "admin"))
            print("Password user admin berhasil diperbarui menjadi: admin123")
        
        # Jika user kasir tidak ada, tambahkan
        if not kasir:
            cursor.execute("INSERT INTO user (username, password, role) VALUES (?, ?, ?)", 
                         ("kasir", "kasir123", "Kasir"))
            print("User kasir berhasil ditambahkan dengan password: kasir123")
        else:
            # Update password kasir
            cursor.execute("UPDATE user SET password = ? WHERE username = ?", 
                         ("kasir123", "kasir"))
            print("Password user kasir berhasil diperbarui menjadi: kasir123")
        
        # Periksa apakah kolom failed_attempts ada dalam tabel user
        cursor.execute("PRAGMA table_info(user)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Reset status kunci dan percobaan gagal untuk semua user jika kolom ada
        if 'failed_attempts' in columns and 'locked_until' in columns:
            cursor.execute("UPDATE user SET failed_attempts = 0, locked_until = NULL")
            print("Status kunci dan percobaan gagal untuk semua user berhasil direset")
        else:
            print("Kolom keamanan tidak ditemukan, melewati reset status kunci")
        
        # Simpan perubahan
        conn.commit()
        print("\nKredensial default berhasil diperbaiki!")
        print("Silakan login dengan:\n- Username: admin, Password: admin123\n- Username: kasir, Password: kasir123")
        return True
    
    except sqlite3.Error as e:
        # Rollback jika terjadi error
        conn.rollback()
        print(f"Error saat memperbaiki kredensial: {e}")
        return False
    
    finally:
        # Tutup koneksi
        conn.close()

if __name__ == "__main__":
    fix_credentials()