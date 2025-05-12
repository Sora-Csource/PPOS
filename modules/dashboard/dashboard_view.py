import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Menambahkan path root ke sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from database.database import Database

class DashboardView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.db = Database()
        
        # Frame utama dengan padding
        main_frame = tk.Frame(self, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Header dengan info user
        header_frame = tk.Frame(main_frame)
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Judul Dashboard
        title_label = tk.Label(header_frame, text="Dashboard", font=("Arial", 18, "bold"))
        title_label.pack(side="left")
        
        # Info user dan tombol logout
        self.user_label = tk.Label(header_frame, text="", font=("Arial", 10))
        self.user_label.pack(side="left", padx=20)
        
        logout_button = tk.Button(header_frame, text="Logout", command=self.logout)
        logout_button.pack(side="right")
        
        # Statistik dashboard
        stats_frame = tk.LabelFrame(main_frame, text="Statistik", padx=10, pady=10)
        stats_frame.pack(fill="x", pady=10)
        
        # Grid untuk statistik
        stats_grid = tk.Frame(stats_frame)
        stats_grid.pack(fill="x")
        
        # Statistik: Total Produk
        produk_frame = tk.Frame(stats_grid, padx=10, pady=10, relief=tk.RAISED, borderwidth=1)
        produk_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        produk_label = tk.Label(produk_frame, text="Total Produk", font=("Arial", 12))
        produk_label.pack()
        
        self.produk_count = tk.Label(produk_frame, text="0", font=("Arial", 24, "bold"))
        self.produk_count.pack(pady=10)
        
        # Statistik: Stok Menipis
        stok_frame = tk.Frame(stats_grid, padx=10, pady=10, relief=tk.RAISED, borderwidth=1)
        stok_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        
        stok_label = tk.Label(stok_frame, text="Stok Menipis", font=("Arial", 12))
        stok_label.pack()
        
        self.stok_count = tk.Label(stok_frame, text="0", font=("Arial", 24, "bold"), fg="red")
        self.stok_count.pack(pady=10)
        
        # Statistik: Total Transaksi Hari Ini
        transaksi_frame = tk.Frame(stats_grid, padx=10, pady=10, relief=tk.RAISED, borderwidth=1)
        transaksi_frame.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
        
        transaksi_label = tk.Label(transaksi_frame, text="Transaksi Hari Ini", font=("Arial", 12))
        transaksi_label.pack()
        
        self.transaksi_count = tk.Label(transaksi_frame, text="0", font=("Arial", 24, "bold"))
        self.transaksi_count.pack(pady=10)
        
        # Konfigurasi grid
        stats_grid.columnconfigure(0, weight=1)
        stats_grid.columnconfigure(1, weight=1)
        stats_grid.columnconfigure(2, weight=1)
        
        # Menu utama
        menu_frame = tk.LabelFrame(main_frame, text="Menu Utama", padx=10, pady=10)
        menu_frame.pack(fill="both", expand=True, pady=10)
        
        # Grid untuk menu
        menu_grid = tk.Frame(menu_frame)
        menu_grid.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Tombol-tombol menu
        btn_width = 20
        btn_height = 4
        
        # Baris 1
        produk_kategori_btn = tk.Button(menu_grid, text="Produk & Kategori", width=btn_width, height=btn_height,
                              command=lambda: controller.show_frame("ProdukKategoriView"))
        produk_kategori_btn.grid(row=0, column=0, padx=10, pady=10)
        
        transaksi_btn = tk.Button(menu_grid, text="Transaksi Baru", width=btn_width, height=btn_height,
                                 command=lambda: controller.show_frame("TransaksiView"))
        transaksi_btn.grid(row=0, column=1, padx=10, pady=10)
        
        # Baris 1 (lanjutan)
        laporan_btn = tk.Button(menu_grid, text="Laporan Penjualan", width=btn_width, height=btn_height,
                               command=lambda: controller.show_frame("LaporanView"))
        laporan_btn.grid(row=0, column=2, padx=10, pady=10)
        
        # Baris 2
        user_btn = tk.Button(menu_grid, text="Kelola User", width=btn_width, height=btn_height,
                            command=lambda: controller.show_frame("UserView"))
        user_btn.grid(row=1, column=0, padx=10, pady=10)
        
        setting_btn = tk.Button(menu_grid, text="Pengaturan", width=btn_width, height=btn_height,
                               command=lambda: controller.show_frame("SettingView"))
        setting_btn.grid(row=1, column=1, padx=10, pady=10)
        
        # Konfigurasi grid
        for i in range(3):
            menu_grid.columnconfigure(i, weight=1)
        for i in range(2):
            menu_grid.rowconfigure(i, weight=1)
    
    def update_dashboard(self):
        """Memperbarui informasi dashboard"""
        # Update info user
        if hasattr(self.controller, 'current_user') and self.controller.current_user:
            self.user_label.config(text=f"Login sebagai: {self.controller.current_user['username']} ({self.controller.current_user['role']})")
        
        # Update statistik
        try:
            # Hitung total produk
            produk = self.db.get_all_produk()
            self.produk_count.config(text=str(len(produk)))
            
            # Hitung produk dengan stok menipis
            stok_menipis = self.db.get_stok_menipis()
            self.stok_count.config(text=str(len(stok_menipis)))
            
            # Hitung transaksi hari ini
            from datetime import datetime
            today = datetime.now().strftime("%Y-%m-%d")
            tomorrow = datetime.now().strftime("%Y-%m-%d 23:59:59")
            transaksi_hari_ini = self.db.get_all_transaksi(today, tomorrow)
            self.transaksi_count.config(text=str(len(transaksi_hari_ini)))
        except Exception as e:
            print(f"Error updating dashboard: {e}")
    
    def logout(self):
        """Proses logout user"""
        if messagebox.askyesno("Konfirmasi Logout", "Apakah Anda yakin ingin logout?"):
            self.controller.current_user = None
            self.controller.show_frame("LoginView")

# Untuk testing modul secara independen
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Test Dashboard View")
    root.geometry("800x600")
    
    class TestController:
        def __init__(self):
            self.current_user = {"username": "admin", "role": "Admin"}
        
        def show_frame(self, frame_name):
            print(f"Showing frame: {frame_name}")
    
    controller = TestController()
    dashboard_view = DashboardView(root, controller)
    dashboard_view.pack(fill="both", expand=True)
    dashboard_view.update_dashboard()
    
    root.mainloop()