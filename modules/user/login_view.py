import tkinter as tk
from tkinter import messagebox, ttk
import sys
import os
from datetime import datetime

# Menambahkan path root ke sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from database.database import Database

class LoginView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.db = Database()
        
        # Membuat frame untuk form login
        self.login_frame = tk.Frame(self, padx=20, pady=20)
        self.login_frame.pack(expand=True)
        
        # Judul
        title_label = tk.Label(self.login_frame, text="Login Sistem", font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Username
        username_label = tk.Label(self.login_frame, text="Username:")
        username_label.grid(row=1, column=0, sticky="w", pady=5)
        self.username_entry = tk.Entry(self.login_frame, width=30)
        self.username_entry.grid(row=1, column=1, pady=5, padx=5)
        
        # Password
        password_label = tk.Label(self.login_frame, text="Password:")
        password_label.grid(row=2, column=0, sticky="w", pady=5)
        self.password_entry = tk.Entry(self.login_frame, width=30, show="*")
        self.password_entry.grid(row=2, column=1, pady=5, padx=5)
        
        # Tombol Login
        login_button = tk.Button(self.login_frame, text="Login", command=self.login, width=15)
        login_button.grid(row=3, column=0, columnspan=2, pady=15)
        
        # Bind Enter key untuk login
        self.username_entry.bind("<Return>", lambda event: self.password_entry.focus())
        self.password_entry.bind("<Return>", lambda event: self.login())
        
        # Fokus ke username entry saat form dibuka
        self.username_entry.focus()
    
    def login(self):
        """Memvalidasi login user"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Username dan password harus diisi!")
            return
        
        # Cek user di database berdasarkan username saja
        user_check = self.db.get_user(username)
        
        if not user_check:
            messagebox.showerror("Error", "Username tidak ditemukan!")
            self.username_entry.focus()
            return
        
        # Cek apakah akun terkunci di database
        if user_check.get('locked_until'):
            try:
                lock_time = datetime.strptime(user_check['locked_until'], "%Y-%m-%d %H:%M:%S")
                current_time = datetime.now()
                
                # Kunci akun selama 5 menit (300 detik)
                if current_time < lock_time:
                    remaining_seconds = int((lock_time - current_time).total_seconds())
                    remaining_minutes = remaining_seconds // 60
                    remaining_secs = remaining_seconds % 60
                    messagebox.showerror("Akun Terkunci", 
                                        f"Terlalu banyak percobaan gagal. Silakan coba lagi dalam {remaining_minutes} menit {remaining_secs} detik.")
                    return
                else:
                    # Reset status kunci di database jika sudah lewat waktu kunci
                    self.db.reset_failed_attempts(username)
            except (ValueError, TypeError):
                # Jika format tanggal tidak valid, reset status kunci
                self.db.reset_failed_attempts(username)
        
        # Cek user dengan username dan password
        user = self.db.get_user(username, password)
        
        if user:
            # Reset percobaan gagal di database jika berhasil login
            self.db.reset_failed_attempts(username)
            
            # Simpan informasi user ke controller
            self.controller.current_user = user
            messagebox.showinfo("Sukses", f"Selamat datang, {username}!")
            # Pindah ke halaman dashboard
            self.controller.show_frame("DashboardView")
        else:
            # Tambah percobaan gagal di database
            failed_attempts = self.db.increment_failed_attempts(username)
            max_attempts = 3
            remaining_attempts = max_attempts - failed_attempts
            
            if remaining_attempts > 0:
                messagebox.showerror("Error", 
                                    f"Password salah! Sisa percobaan: {remaining_attempts}")
            else:
                # Kunci akun jika melebihi batas percobaan
                lock_duration_minutes = 5
                self.db.lock_user_account(username, lock_duration_minutes)
                messagebox.showerror("Akun Terkunci", 
                                    f"Terlalu banyak percobaan gagal. Akun terkunci selama {lock_duration_minutes} menit.")
            
            self.password_entry.delete(0, tk.END)
            self.password_entry.focus()

# Untuk testing modul secara independen
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Test Login View")
    root.geometry("400x300")
    
    class TestController:
        def __init__(self):
            self.current_user = None
        
        def show_frame(self, frame_name):
            print(f"Showing frame: {frame_name}")
    
    controller = TestController()
    login_view = LoginView(root, controller)
    login_view.pack(fill="both", expand=True)
    
    root.mainloop()