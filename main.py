import os
import tkinter as tk
from tkinter import messagebox
import sys

# Import modul-modul aplikasi
from modules.user.login_view import LoginView
from modules.dashboard.dashboard_view import DashboardView
from modules.produk_kategori.produk_kategori_view import ProdukKategoriView
from modules.user.user_view import UserView
from modules.transaksi.transaksi_view import TransaksiView
from modules.laporan.laporan_view import LaporanView
from modules.setting.setting_view import SettingView

# Import database
from database.database import Database
from database.init_db import init_db

# Inisialisasi aplikasi utama
class POSApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplikasi POS & Inventory Management Offline")
        self.geometry("1000x700")
        self.resizable(True, True)
        
        # Inisialisasi database
        init_db()
        
        # Variabel untuk menyimpan user yang sedang login
        self.current_user = None
        
        # Container untuk semua frame
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        # Dictionary untuk menyimpan semua frame
        self.frames = {}
        
        # Inisialisasi semua frame
        for F in (LoginView, DashboardView, ProdukKategoriView, UserView, TransaksiView, LaporanView, SettingView):
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        # Tampilkan frame login pertama kali
        self.show_frame("LoginView")
    
    def show_frame(self, frame_name):
        """Menampilkan frame berdasarkan nama"""
        frame = self.frames.get(frame_name)
        if frame:
            frame.tkraise()
            
            # Update dashboard jika yang ditampilkan adalah dashboard
            if frame_name == "DashboardView" and hasattr(frame, "update_dashboard"):
                frame.update_dashboard()
            
            # Refresh data produk jika yang ditampilkan adalah produk kategori view
            if frame_name == "ProdukKategoriView" and hasattr(frame, "load_produk"):
                frame.load_produk()

if __name__ == "__main__":
    app = POSApp()
    app.mainloop()