import sqlite3
import os
from datetime import datetime, timedelta

class Database:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(__file__), 'pos_inventory.db')
        self.conn = None
        self.cursor = None
    
    def connect(self):
        """Membuat koneksi ke database"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row  # Untuk akses kolom dengan nama
            self.cursor = self.conn.cursor()
            return True
        except sqlite3.Error as e:
            print(f"Error koneksi database: {e}")
            return False
    
    def disconnect(self):
        """Menutup koneksi database"""
        if self.conn:
            self.conn.close()
    
    def commit(self):
        """Commit perubahan ke database"""
        if self.conn:
            self.conn.commit()
    
    def rollback(self):
        """Rollback perubahan jika terjadi error"""
        if self.conn:
            self.conn.rollback()
    
    # ===== USER OPERATIONS =====
    def get_user(self, username, password=None):
        """Mendapatkan user berdasarkan username dan password (opsional)"""
        self.connect()
        try:
            # Periksa apakah kolom last_login ada
            self.cursor.execute("PRAGMA table_info(user)")
            columns = [column[1] for column in self.cursor.fetchall()]
            has_last_login = 'last_login' in columns
            
            if password:
                self.cursor.execute("SELECT * FROM user WHERE username = ? AND password = ?", (username, password))
                user = self.cursor.fetchone()
                if user:
                    # Update waktu login terakhir jika kolom ada
                    if has_last_login:
                        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        self.cursor.execute("UPDATE user SET last_login = ? WHERE id = ?", (current_time, user['id']))
                        self.commit()
                else:
                    # Jika password salah, catat percobaan login gagal
                    self.log_failed_login(username)
            else:
                self.cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
                user = self.cursor.fetchone()
            return dict(user) if user else None
        except sqlite3.Error as e:
            print(f"Error get_user: {e}")
            return None
        finally:
            self.disconnect()
            
    def log_failed_login(self, username):
        """Mencatat percobaan login yang gagal"""
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Catat ke log file atau database jika diperlukan
            log_file_path = os.path.join(os.path.dirname(__file__), 'login_attempts.log')
            with open(log_file_path, 'a') as log_file:
                log_file.write(f"{current_time} - Percobaan login gagal untuk username: {username}\n")
        except Exception as e:
            print(f"Error mencatat percobaan login gagal: {e}")
            pass
            
    def increment_failed_attempts(self, username):
        """Menambah jumlah percobaan login yang gagal"""
        self.connect()
        try:
            # Periksa apakah kolom failed_attempts ada
            self.cursor.execute("PRAGMA table_info(user)")
            columns = [column[1] for column in self.cursor.fetchall()]
            
            # Jika kolom tidak ada, kembalikan 0 tanpa melakukan perubahan
            if 'failed_attempts' not in columns:
                return 0
                
            # Ambil jumlah percobaan gagal saat ini
            self.cursor.execute("SELECT failed_attempts FROM user WHERE username = ?", (username,))
            result = self.cursor.fetchone()
            
            if result:
                current_attempts = result['failed_attempts'] if result['failed_attempts'] is not None else 0
                new_attempts = current_attempts + 1
                
                # Update jumlah percobaan gagal
                self.cursor.execute("UPDATE user SET failed_attempts = ? WHERE username = ?", 
                                  (new_attempts, username))
                self.commit()
                return new_attempts
            return 0
        except sqlite3.Error as e:
            print(f"Error increment_failed_attempts: {e}")
            return 0
        finally:
            self.disconnect()
    
    def reset_failed_attempts(self, username):
        """Reset jumlah percobaan login yang gagal"""
        self.connect()
        try:
            # Periksa apakah kolom failed_attempts dan locked_until ada
            self.cursor.execute("PRAGMA table_info(user)")
            columns = [column[1] for column in self.cursor.fetchall()]
            
            # Jika kolom tidak ada, kembalikan True tanpa melakukan perubahan
            if 'failed_attempts' not in columns or 'locked_until' not in columns:
                return True
                
            # Reset nilai jika kolom ada
            self.cursor.execute("UPDATE user SET failed_attempts = 0, locked_until = NULL WHERE username = ?", 
                              (username,))
            self.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error reset_failed_attempts: {e}")
            return False
        finally:
            self.disconnect()
    
    def lock_user_account(self, username, minutes=5):
        """Mengunci akun user untuk durasi tertentu"""
        self.connect()
        try:
            # Periksa apakah kolom locked_until ada
            self.cursor.execute("PRAGMA table_info(user)")
            columns = [column[1] for column in self.cursor.fetchall()]
            
            # Jika kolom tidak ada, kembalikan True tanpa melakukan perubahan
            if 'locked_until' not in columns:
                return True
                
            # Hitung waktu kunci berakhir
            current_time = datetime.now()
            lock_until = current_time.replace(microsecond=0) + timedelta(minutes=minutes)
            lock_until_str = lock_until.strftime("%Y-%m-%d %H:%M:%S")
            
            # Update status kunci di database
            self.cursor.execute("UPDATE user SET locked_until = ? WHERE username = ?", 
                              (lock_until_str, username))
            self.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error lock_user_account: {e}")
            return False
        finally:
            self.disconnect()
    
    def add_user(self, username, password, role):
        """Menambahkan user baru"""
        self.connect()
        try:
            self.cursor.execute(
                "INSERT INTO user (username, password, role) VALUES (?, ?, ?)",
                (username, password, role)
            )
            self.commit()
            return True
        except sqlite3.Error as e:
            self.rollback()
            print(f"Error add_user: {e}")
            return False
        finally:
            self.disconnect()
    
    def get_all_users(self):
        """Mendapatkan semua user"""
        self.connect()
        try:
            self.cursor.execute("SELECT * FROM user")
            users = self.cursor.fetchall()
            return [dict(user) for user in users]
        except sqlite3.Error as e:
            print(f"Error get_all_users: {e}")
            return []
        finally:
            self.disconnect()
    
    def update_user(self, user_id, username, password, role):
        """Memperbarui data user"""
        self.connect()
        try:
            self.cursor.execute(
                "UPDATE user SET username = ?, password = ?, role = ? WHERE id = ?",
                (username, password, role, user_id)
            )
            self.commit()
            return True
        except sqlite3.Error as e:
            self.rollback()
            print(f"Error update_user: {e}")
            return False
        finally:
            self.disconnect()
    
    def delete_user(self, user_id):
        """Menghapus user"""
        self.connect()
        try:
            self.cursor.execute("DELETE FROM user WHERE id = ?", (user_id,))
            self.commit()
            return True
        except sqlite3.Error as e:
            self.rollback()
            print(f"Error delete_user: {e}")
            return False
        finally:
            self.disconnect()
    
    # ===== KATEGORI OPERATIONS =====
    def get_all_kategori(self):
        """Mendapatkan semua kategori"""
        self.connect()
        try:
            self.cursor.execute("SELECT * FROM kategori")
            kategori = self.cursor.fetchall()
            return [dict(k) for k in kategori]
        except sqlite3.Error as e:
            print(f"Error get_all_kategori: {e}")
            return []
        finally:
            self.disconnect()
    
    def add_kategori(self, nama):
        """Menambahkan kategori baru"""
        self.connect()
        try:
            self.cursor.execute("INSERT INTO kategori (nama) VALUES (?)", (nama,))
            self.commit()
            return True
        except sqlite3.Error as e:
            self.rollback()
            print(f"Error add_kategori: {e}")
            return False
        finally:
            self.disconnect()
    
    def update_kategori(self, kategori_id, nama):
        """Memperbarui kategori"""
        self.connect()
        try:
            self.cursor.execute("UPDATE kategori SET nama = ? WHERE id = ?", (nama, kategori_id))
            self.commit()
            return True
        except sqlite3.Error as e:
            self.rollback()
            print(f"Error update_kategori: {e}")
            return False
        finally:
            self.disconnect()
    
    def delete_kategori(self, kategori_id):
        """Menghapus kategori"""
        self.connect()
        try:
            self.cursor.execute("DELETE FROM kategori WHERE id = ?", (kategori_id,))
            self.commit()
            return True
        except sqlite3.Error as e:
            self.rollback()
            print(f"Error delete_kategori: {e}")
            return False
        finally:
            self.disconnect()
    
    # ===== PRODUK OPERATIONS =====
    def get_all_produk(self):
        """Mendapatkan semua produk dengan nama kategori"""
        self.connect()
        try:
            self.cursor.execute("""
                SELECT p.id, p.nama, p.harga, p.stok, p.kategori_id, k.nama as kategori_nama 
                FROM produk p 
                LEFT JOIN kategori k ON p.kategori_id = k.id
            """)
            produk = self.cursor.fetchall()
            return [dict(p) for p in produk]
        except sqlite3.Error as e:
            print(f"Error get_all_produk: {e}")
            return []
        finally:
            self.disconnect()
    
    def get_produk(self, produk_id):
        """Mendapatkan detail produk berdasarkan ID"""
        self.connect()
        try:
            self.cursor.execute("""
                SELECT p.id, p.nama, p.harga, p.stok, p.kategori_id, k.nama as kategori_nama 
                FROM produk p 
                LEFT JOIN kategori k ON p.kategori_id = k.id 
                WHERE p.id = ?
            """, (produk_id,))
            produk = self.cursor.fetchone()
            return dict(produk) if produk else None
        except sqlite3.Error as e:
            print(f"Error get_produk: {e}")
            return None
        finally:
            self.disconnect()
    
    def add_produk(self, nama, kategori_id, harga, stok):
        """Menambahkan produk baru"""
        self.connect()
        try:
            self.cursor.execute(
                "INSERT INTO produk (nama, kategori_id, harga, stok) VALUES (?, ?, ?, ?)",
                (nama, kategori_id, harga, stok)
            )
            self.commit()
            return True
        except sqlite3.Error as e:
            self.rollback()
            print(f"Error add_produk: {e}")
            return False
        finally:
            self.disconnect()
    
    def update_produk(self, produk_id, nama, kategori_id, harga, stok):
        """Memperbarui produk"""
        self.connect()
        try:
            self.cursor.execute(
                "UPDATE produk SET nama = ?, kategori_id = ?, harga = ?, stok = ? WHERE id = ?",
                (nama, kategori_id, harga, stok, produk_id)
            )
            self.commit()
            return True
        except sqlite3.Error as e:
            self.rollback()
            print(f"Error update_produk: {e}")
            return False
        finally:
            self.disconnect()
    
    def delete_produk(self, produk_id):
        """Menghapus produk"""
        self.connect()
        try:
            self.cursor.execute("DELETE FROM produk WHERE id = ?", (produk_id,))
            self.commit()
            return True
        except sqlite3.Error as e:
            self.rollback()
            print(f"Error delete_produk: {e}")
            return False
        finally:
            self.disconnect()
    
    def update_stok(self, produk_id, jumlah):
        """Memperbarui stok produk (menambah/mengurangi)"""
        self.connect()
        try:
            self.cursor.execute("SELECT stok FROM produk WHERE id = ?", (produk_id,))
            current_stok = self.cursor.fetchone()
            if current_stok:
                new_stok = current_stok['stok'] + jumlah
                if new_stok < 0:
                    return False  # Stok tidak cukup
                self.cursor.execute(
                    "UPDATE produk SET stok = ? WHERE id = ?",
                    (new_stok, produk_id)
                )
                self.commit()
                return True
            return False
        except sqlite3.Error as e:
            self.rollback()
            print(f"Error update_stok: {e}")
            return False
        finally:
            self.disconnect()
    
    # ===== TRANSAKSI OPERATIONS =====
    def create_transaksi(self, user_id, items):
        """Membuat transaksi baru
        
        Args:
            user_id: ID user yang melakukan transaksi
            items: List of dict dengan format [{"produk_id": id, "qty": qty, "harga": harga}, ...]
        
        Returns:
            ID transaksi jika berhasil, None jika gagal
        """
        self.connect()
        try:
            # Hitung total transaksi
            total = sum(item["qty"] * item["harga"] for item in items)
            tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Buat transaksi baru
            self.cursor.execute(
                "INSERT INTO transaksi (tanggal, user_id, total) VALUES (?, ?, ?)",
                (tanggal, user_id, total)
            )
            transaksi_id = self.cursor.lastrowid
            
            # Tambahkan detail transaksi
            for item in items:
                self.cursor.execute(
                    "INSERT INTO detail_transaksi (transaksi_id, produk_id, qty, harga) VALUES (?, ?, ?, ?)",
                    (transaksi_id, item["produk_id"], item["qty"], item["harga"])
                )
                
                # Update stok produk
                self.cursor.execute(
                    "UPDATE produk SET stok = stok - ? WHERE id = ?",
                    (item["qty"], item["produk_id"])
                )
            
            self.commit()
            return transaksi_id
        except sqlite3.Error as e:
            self.rollback()
            print(f"Error create_transaksi: {e}")
            return None
        finally:
            self.disconnect()
    
    def get_transaksi(self, transaksi_id):
        """Mendapatkan detail transaksi berdasarkan ID"""
        self.connect()
        try:
            # Dapatkan info transaksi
            self.cursor.execute("""
                SELECT t.id, t.tanggal, t.total, t.user_id, u.username 
                FROM transaksi t 
                JOIN user u ON t.user_id = u.id 
                WHERE t.id = ?
            """, (transaksi_id,))
            transaksi = self.cursor.fetchone()
            
            if not transaksi:
                return None
            
            # Dapatkan detail item transaksi
            self.cursor.execute("""
                SELECT dt.id, dt.produk_id, dt.qty, dt.harga, p.nama as produk_nama 
                FROM detail_transaksi dt 
                JOIN produk p ON dt.produk_id = p.id 
                WHERE dt.transaksi_id = ?
            """, (transaksi_id,))
            items = self.cursor.fetchall()
            
            result = dict(transaksi)
            result["items"] = [dict(item) for item in items]
            return result
        except sqlite3.Error as e:
            print(f"Error get_transaksi: {e}")
            return None
        finally:
            self.disconnect()
    
    def get_all_transaksi(self, start_date=None, end_date=None):
        """Mendapatkan semua transaksi dengan filter tanggal opsional"""
        self.connect()
        try:
            query = """
                SELECT t.id, t.tanggal, t.total, t.user_id, u.username 
                FROM transaksi t 
                JOIN user u ON t.user_id = u.id
            """
            params = []
            
            if start_date and end_date:
                query += " WHERE t.tanggal BETWEEN ? AND ?"
                params.extend([start_date, end_date])
            elif start_date:
                query += " WHERE t.tanggal >= ?"
                params.append(start_date)
            elif end_date:
                query += " WHERE t.tanggal <= ?"
                params.append(end_date)
                
            query += " ORDER BY t.tanggal DESC"
            
            self.cursor.execute(query, params)
            transaksi = self.cursor.fetchall()
            return [dict(t) for t in transaksi]
        except sqlite3.Error as e:
            print(f"Error get_all_transaksi: {e}")
            return []
        finally:
            self.disconnect()
    
    # ===== LAPORAN OPERATIONS =====
    def get_laporan_penjualan(self, start_date, end_date):
        """Mendapatkan laporan penjualan dalam rentang tanggal"""
        self.connect()
        try:
            self.cursor.execute("""
                SELECT p.id, p.nama, SUM(dt.qty) as total_qty, SUM(dt.qty * dt.harga) as total_penjualan 
                FROM detail_transaksi dt 
                JOIN produk p ON dt.produk_id = p.id 
                JOIN transaksi t ON dt.transaksi_id = t.id 
                WHERE t.tanggal BETWEEN ? AND ? 
                GROUP BY p.id 
                ORDER BY total_penjualan DESC
            """, (start_date, end_date))
            laporan = self.cursor.fetchall()
            return [dict(item) for item in laporan]
        except sqlite3.Error as e:
            print(f"Error get_laporan_penjualan: {e}")
            return []
        finally:
            self.disconnect()
    
    def get_produk_terlaris(self, limit=10):
        """Mendapatkan produk terlaris berdasarkan jumlah terjual"""
        self.connect()
        try:
            self.cursor.execute("""
                SELECT p.id, p.nama, SUM(dt.qty) as total_terjual 
                FROM detail_transaksi dt 
                JOIN produk p ON dt.produk_id = p.id 
                GROUP BY p.id 
                ORDER BY total_terjual DESC 
                LIMIT ?
            """, (limit,))
            produk = self.cursor.fetchall()
            return [dict(p) for p in produk]
        except sqlite3.Error as e:
            print(f"Error get_produk_terlaris: {e}")
            return []
        finally:
            self.disconnect()
    
    def get_stok_menipis(self, batas=10):
        """Mendapatkan produk dengan stok menipis"""
        self.connect()
        try:
            self.cursor.execute("""
                SELECT p.id, p.nama, p.stok, k.nama as kategori_nama 
                FROM produk p 
                LEFT JOIN kategori k ON p.kategori_id = k.id 
                WHERE p.stok <= ? 
                ORDER BY p.stok ASC
            """, (batas,))
            produk = self.cursor.fetchall()
            return [dict(p) for p in produk]
        except sqlite3.Error as e:
            print(f"Error get_stok_menipis: {e}")
            return []
        finally:
            self.disconnect()
    
    def get_detail_transaksi(self, transaksi_id):
        """Mendapatkan detail item dari suatu transaksi"""
        self.connect()
        try:
            self.cursor.execute("""
                SELECT dt.id, dt.transaksi_id, dt.produk_id, dt.qty, dt.harga
                FROM detail_transaksi dt
                WHERE dt.transaksi_id = ?
            """, (transaksi_id,))
            detail = self.cursor.fetchall()
            return [dict(item) for item in detail]
        except sqlite3.Error as e:
            print(f"Error get_detail_transaksi: {e}")
            return []
        finally:
            self.disconnect()
    
    def get_user_by_id(self, user_id):
        """Mendapatkan user berdasarkan ID"""
        self.connect()
        try:
            self.cursor.execute("SELECT * FROM user WHERE id = ?", (user_id,))
            user = self.cursor.fetchone()
            return dict(user) if user else None
        except sqlite3.Error as e:
            print(f"Error get_user_by_id: {e}")
            return None
        finally:
            self.disconnect()