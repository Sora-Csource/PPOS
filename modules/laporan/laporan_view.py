import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sys
import os
from datetime import datetime, timedelta
import pandas as pd

# Menambahkan path root ke sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from database.database import Database

class LaporanView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.db = Database()
        
        # Frame utama dengan padding
        main_frame = tk.Frame(self, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Header
        header_frame = tk.Frame(main_frame)
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Judul
        title_label = tk.Label(header_frame, text="Laporan Penjualan", font=("Arial", 18, "bold"))
        title_label.pack(side="left")
        
        # Tombol kembali ke dashboard
        back_button = tk.Button(header_frame, text="Kembali ke Dashboard", 
                              command=lambda: controller.show_frame("DashboardView"))
        back_button.pack(side="right")
        
        # Frame untuk filter
        filter_frame = tk.LabelFrame(main_frame, text="Filter Laporan", padx=10, pady=10)
        filter_frame.pack(fill="x", pady=(0, 10))
        
        # Filter tanggal
        date_frame = tk.Frame(filter_frame)
        date_frame.pack(fill="x", pady=5)
        
        # Tanggal mulai
        start_date_label = tk.Label(date_frame, text="Tanggal Mulai:")
        start_date_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.start_date_entry = tk.Entry(date_frame, width=15)
        self.start_date_entry.grid(row=0, column=1, padx=5, pady=5)
        self.start_date_entry.insert(0, (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"))
        
        # Tanggal akhir
        end_date_label = tk.Label(date_frame, text="Tanggal Akhir:")
        end_date_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        
        self.end_date_entry = tk.Entry(date_frame, width=15)
        self.end_date_entry.grid(row=0, column=3, padx=5, pady=5)
        self.end_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Tombol filter
        filter_button = tk.Button(date_frame, text="Filter", command=self.filter_laporan)
        filter_button.grid(row=0, column=4, padx=10, pady=5)
        
        # Tombol preset tanggal
        preset_frame = tk.Frame(filter_frame)
        preset_frame.pack(fill="x", pady=5)
        
        hari_ini_btn = tk.Button(preset_frame, text="Hari Ini", 
                               command=lambda: self.set_date_preset("today"))
        hari_ini_btn.grid(row=0, column=0, padx=5, pady=5)
        
        kemarin_btn = tk.Button(preset_frame, text="Kemarin", 
                              command=lambda: self.set_date_preset("yesterday"))
        kemarin_btn.grid(row=0, column=1, padx=5, pady=5)
        
        minggu_ini_btn = tk.Button(preset_frame, text="Minggu Ini", 
                                 command=lambda: self.set_date_preset("this_week"))
        minggu_ini_btn.grid(row=0, column=2, padx=5, pady=5)
        
        bulan_ini_btn = tk.Button(preset_frame, text="Bulan Ini", 
                                command=lambda: self.set_date_preset("this_month"))
        bulan_ini_btn.grid(row=0, column=3, padx=5, pady=5)
        
        # Notebook untuk tab laporan
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill="both", expand=True)
        
        # Tab Transaksi
        transaksi_frame = tk.Frame(self.notebook)
        self.notebook.add(transaksi_frame, text="Daftar Transaksi")
        
        # Tabel transaksi
        self.transaksi_tree = ttk.Treeview(transaksi_frame, 
                                         columns=("id", "tanggal", "kasir", "total"), 
                                         show="headings")
        self.transaksi_tree.pack(side="left", fill="both", expand=True)
        
        # Scrollbar untuk tabel transaksi
        transaksi_scrollbar = ttk.Scrollbar(transaksi_frame, orient="vertical", command=self.transaksi_tree.yview)
        self.transaksi_tree.configure(yscrollcommand=transaksi_scrollbar.set)
        transaksi_scrollbar.pack(side="right", fill="y")
        
        # Definisi kolom transaksi
        self.transaksi_tree.heading("id", text="ID")
        self.transaksi_tree.heading("tanggal", text="Tanggal")
        self.transaksi_tree.heading("kasir", text="Kasir")
        self.transaksi_tree.heading("total", text="Total")
        
        # Lebar kolom transaksi
        self.transaksi_tree.column("id", width=50)
        self.transaksi_tree.column("tanggal", width=150)
        self.transaksi_tree.column("kasir", width=100)
        self.transaksi_tree.column("total", width=100)
        
        # Bind event klik pada tabel transaksi untuk melihat detail
        self.transaksi_tree.bind("<Double-1>", self.lihat_detail_transaksi)
        
        # Tab Produk Terlaris
        produk_frame = tk.Frame(self.notebook)
        self.notebook.add(produk_frame, text="Produk Terlaris")
        
        # Tabel produk terlaris
        self.produk_tree = ttk.Treeview(produk_frame, 
                                      columns=("id", "nama", "terjual", "total"), 
                                      show="headings")
        self.produk_tree.pack(side="left", fill="both", expand=True)
        
        # Scrollbar untuk tabel produk
        produk_scrollbar = ttk.Scrollbar(produk_frame, orient="vertical", command=self.produk_tree.yview)
        self.produk_tree.configure(yscrollcommand=produk_scrollbar.set)
        produk_scrollbar.pack(side="right", fill="y")
        
        # Definisi kolom produk
        self.produk_tree.heading("id", text="ID")
        self.produk_tree.heading("nama", text="Nama Produk")
        self.produk_tree.heading("terjual", text="Jumlah Terjual")
        self.produk_tree.heading("total", text="Total Penjualan")
        
        # Lebar kolom produk
        self.produk_tree.column("id", width=50)
        self.produk_tree.column("nama", width=200)
        self.produk_tree.column("terjual", width=100)
        self.produk_tree.column("total", width=150)
        
        # Tab Stok Menipis
        stok_frame = tk.Frame(self.notebook)
        self.notebook.add(stok_frame, text="Stok Menipis")
        
        # Tabel stok menipis
        self.stok_tree = ttk.Treeview(stok_frame, 
                                    columns=("id", "nama", "kategori", "stok"), 
                                    show="headings")
        self.stok_tree.pack(side="left", fill="both", expand=True)
        
        # Scrollbar untuk tabel stok
        stok_scrollbar = ttk.Scrollbar(stok_frame, orient="vertical", command=self.stok_tree.yview)
        self.stok_tree.configure(yscrollcommand=stok_scrollbar.set)
        stok_scrollbar.pack(side="right", fill="y")
        
        # Definisi kolom stok
        self.stok_tree.heading("id", text="ID")
        self.stok_tree.heading("nama", text="Nama Produk")
        self.stok_tree.heading("kategori", text="Kategori")
        self.stok_tree.heading("stok", text="Stok")
        
        # Lebar kolom stok
        self.stok_tree.column("id", width=50)
        self.stok_tree.column("nama", width=200)
        self.stok_tree.column("kategori", width=150)
        self.stok_tree.column("stok", width=80)
        
        # Frame untuk tombol ekspor
        export_frame = tk.Frame(main_frame)
        export_frame.pack(fill="x", pady=10)
        
        export_button = tk.Button(export_frame, text="Ekspor ke Excel", 
                                command=self.ekspor_laporan, 
                                bg="#4CAF50", fg="white")
        export_button.pack(side="right", padx=10)
        
        # Load data awal
        self.filter_laporan()
    
    def set_date_preset(self, preset):
        """Set tanggal berdasarkan preset"""
        today = datetime.now()
        
        if preset == "today":
            # Hari ini
            self.start_date_entry.delete(0, tk.END)
            self.start_date_entry.insert(0, today.strftime("%Y-%m-%d"))
            self.end_date_entry.delete(0, tk.END)
            self.end_date_entry.insert(0, today.strftime("%Y-%m-%d"))
        
        elif preset == "yesterday":
            # Kemarin
            yesterday = today - timedelta(days=1)
            self.start_date_entry.delete(0, tk.END)
            self.start_date_entry.insert(0, yesterday.strftime("%Y-%m-%d"))
            self.end_date_entry.delete(0, tk.END)
            self.end_date_entry.insert(0, yesterday.strftime("%Y-%m-%d"))
        
        elif preset == "this_week":
            # Minggu ini (Senin - Minggu)
            start_of_week = today - timedelta(days=today.weekday())
            self.start_date_entry.delete(0, tk.END)
            self.start_date_entry.insert(0, start_of_week.strftime("%Y-%m-%d"))
            self.end_date_entry.delete(0, tk.END)
            self.end_date_entry.insert(0, today.strftime("%Y-%m-%d"))
        
        elif preset == "this_month":
            # Bulan ini
            start_of_month = today.replace(day=1)
            self.start_date_entry.delete(0, tk.END)
            self.start_date_entry.insert(0, start_of_month.strftime("%Y-%m-%d"))
            self.end_date_entry.delete(0, tk.END)
            self.end_date_entry.insert(0, today.strftime("%Y-%m-%d"))
        
        # Refresh laporan
        self.filter_laporan()
    
    def filter_laporan(self):
        """Filter laporan berdasarkan tanggal"""
        try:
            start_date = self.start_date_entry.get()
            end_date = self.end_date_entry.get() + " 23:59:59"  # Tambahkan waktu untuk mencakup seluruh hari
            
            # Validasi format tanggal
            datetime.strptime(start_date, "%Y-%m-%d")
            datetime.strptime(end_date.split()[0], "%Y-%m-%d")
            
            # Load data transaksi
            self.load_transaksi(start_date, end_date)
            
            # Load data produk terlaris
            self.load_produk_terlaris(start_date, end_date)
            
            # Load data stok menipis
            self.load_stok_menipis()
        except ValueError:
            messagebox.showerror("Error", "Format tanggal tidak valid! Gunakan format YYYY-MM-DD")
    
    def load_transaksi(self, start_date, end_date):
        """Memuat daftar transaksi ke tabel"""
        # Hapus data lama
        for item in self.transaksi_tree.get_children():
            self.transaksi_tree.delete(item)
        
        # Ambil data transaksi dari database
        transaksi = self.db.get_all_transaksi(start_date, end_date)
        
        # Masukkan ke tabel
        for t in transaksi:
            self.transaksi_tree.insert("", "end", values=(
                t["id"], 
                t["tanggal"], 
                t["username"], 
                f"Rp {t['total']:,.0f}"
            ))
    
    def load_produk_terlaris(self, start_date, end_date):
        """Memuat daftar produk terlaris ke tabel"""
        # Hapus data lama
        for item in self.produk_tree.get_children():
            self.produk_tree.delete(item)
        
        # Ambil data produk terlaris dari database
        produk = self.db.get_laporan_penjualan(start_date, end_date)
        
        # Masukkan ke tabel
        for p in produk:
            self.produk_tree.insert("", "end", values=(
                p["id"], 
                p["nama"], 
                p["total_qty"], 
                f"Rp {p['total_penjualan']:,.0f}"
            ))
    
    def load_stok_menipis(self):
        """Memuat daftar produk dengan stok menipis ke tabel"""
        # Hapus data lama
        for item in self.stok_tree.get_children():
            self.stok_tree.delete(item)
        
        # Ambil data stok menipis dari database
        produk = self.db.get_stok_menipis()
        
        # Masukkan ke tabel
        for p in produk:
            self.stok_tree.insert("", "end", values=(
                p["id"], 
                p["nama"], 
                p.get("kategori_nama", "Tidak ada kategori"), 
                p["stok"]
            ))
    
    def lihat_detail_transaksi(self, event):
        """Menampilkan detail transaksi"""
        selected_item = self.transaksi_tree.focus()
        if not selected_item:
            return
        
        # Ambil data transaksi
        item_data = self.transaksi_tree.item(selected_item)
        values = item_data["values"]
        
        # Ambil detail transaksi dari database
        transaksi = self.db.get_transaksi(values[0])
        if not transaksi:
            messagebox.showerror("Error", "Data transaksi tidak ditemukan!")
            return
        
        # Buat window baru untuk detail transaksi
        detail_window = tk.Toplevel(self)
        detail_window.title(f"Detail Transaksi #{transaksi['id']}")
        detail_window.geometry("600x400")
        
        # Frame untuk detail
        detail_frame = tk.Frame(detail_window, padx=20, pady=20)
        detail_frame.pack(fill="both", expand=True)
        
        # Info transaksi
        info_frame = tk.LabelFrame(detail_frame, text="Informasi Transaksi", padx=10, pady=10)
        info_frame.pack(fill="x", pady=(0, 10))
        
        # Grid untuk info
        info_grid = tk.Frame(info_frame)
        info_grid.pack(fill="x")
        
        # No. Transaksi
        tk.Label(info_grid, text="No. Transaksi:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        tk.Label(info_grid, text=str(transaksi["id"])).grid(row=0, column=1, sticky="w", padx=5, pady=2)
        
        # Tanggal
        tk.Label(info_grid, text="Tanggal:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        tk.Label(info_grid, text=transaksi["tanggal"]).grid(row=1, column=1, sticky="w", padx=5, pady=2)
        
        # Kasir
        tk.Label(info_grid, text="Kasir:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        tk.Label(info_grid, text=transaksi["username"]).grid(row=2, column=1, sticky="w", padx=5, pady=2)
        
        # Total
        tk.Label(info_grid, text="Total:").grid(row=3, column=0, sticky="w", padx=5, pady=2)
        tk.Label(info_grid, text=f"Rp {transaksi['total']:,.0f}").grid(row=3, column=1, sticky="w", padx=5, pady=2)
        
        # Frame untuk tabel item
        item_frame = tk.LabelFrame(detail_frame, text="Detail Item", padx=10, pady=10)
        item_frame.pack(fill="both", expand=True)
        
        # Tabel item
        item_tree = ttk.Treeview(item_frame, 
                               columns=("id", "nama", "qty", "harga", "subtotal"), 
                               show="headings")
        item_tree.pack(side="left", fill="both", expand=True)
        
        # Scrollbar untuk tabel item
        item_scrollbar = ttk.Scrollbar(item_frame, orient="vertical", command=item_tree.yview)
        item_tree.configure(yscrollcommand=item_scrollbar.set)
        item_scrollbar.pack(side="right", fill="y")
        
        # Definisi kolom item
        item_tree.heading("id", text="ID")
        item_tree.heading("nama", text="Nama Produk")
        item_tree.heading("qty", text="Qty")
        item_tree.heading("harga", text="Harga")
        item_tree.heading("subtotal", text="Subtotal")
        
        # Lebar kolom item
        item_tree.column("id", width=50)
        item_tree.column("nama", width=200)
        item_tree.column("qty", width=50)
        item_tree.column("harga", width=100)
        item_tree.column("subtotal", width=100)
        
        # Masukkan data item ke tabel
        for item in transaksi["items"]:
            subtotal = item["qty"] * item["harga"]
            item_tree.insert("", "end", values=(
                item["produk_id"], 
                item["produk_nama"], 
                item["qty"], 
                f"Rp {item['harga']:,.0f}", 
                f"Rp {subtotal:,.0f}"
            ))
        
        # Tombol tutup
        close_button = tk.Button(detail_frame, text="Tutup", command=detail_window.destroy)
        close_button.pack(pady=10)
    
    def ekspor_laporan(self):
        """Mengekspor laporan ke file Excel"""
        try:
            start_date = self.start_date_entry.get()
            end_date = self.end_date_entry.get() + " 23:59:59"
            
            # Validasi format tanggal
            datetime.strptime(start_date, "%Y-%m-%d")
            datetime.strptime(end_date.split()[0], "%Y-%m-%d")
            
            # Buka dialog untuk menyimpan file
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")],
                initialfile=f"Laporan_{start_date}_sampai_{end_date.split()[0]}.xlsx"
            )
            
            if not file_path:
                return
            
            # Ambil data untuk laporan
            transaksi = self.db.get_all_transaksi(start_date, end_date)
            produk_terlaris = self.db.get_laporan_penjualan(start_date, end_date)
            stok_menipis = self.db.get_stok_menipis()
            
            # Buat dataframe untuk transaksi
            transaksi_data = {
                "ID": [],
                "Tanggal": [],
                "Kasir": [],
                "Total": []
            }
            
            for t in transaksi:
                transaksi_data["ID"].append(t["id"])
                transaksi_data["Tanggal"].append(t["tanggal"])
                transaksi_data["Kasir"].append(t["username"])
                transaksi_data["Total"].append(t["total"])
            
            transaksi_df = pd.DataFrame(transaksi_data)
            
            # Buat dataframe untuk produk terlaris
            produk_data = {
                "ID": [],
                "Nama Produk": [],
                "Jumlah Terjual": [],
                "Total Penjualan": []
            }
            
            for p in produk_terlaris:
                produk_data["ID"].append(p["id"])
                produk_data["Nama Produk"].append(p["nama"])
                produk_data["Jumlah Terjual"].append(p["total_qty"])
                produk_data["Total Penjualan"].append(p["total_penjualan"])
            
            produk_df = pd.DataFrame(produk_data)
            
            # Buat dataframe untuk stok menipis
            stok_data = {
                "ID": [],
                "Nama Produk": [],
                "Kategori": [],
                "Stok": []
            }
            
            for p in stok_menipis:
                stok_data["ID"].append(p["id"])
                stok_data["Nama Produk"].append(p["nama"])
                stok_data["Kategori"].append(p.get("kategori_nama", "Tidak ada kategori"))
                stok_data["Stok"].append(p["stok"])
            
            stok_df = pd.DataFrame(stok_data)
            
            # Buat Excel writer
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                # Tambahkan info periode laporan
                info_data = {
                    "Keterangan": ["Periode Laporan", "Tanggal Mulai", "Tanggal Akhir", "Diekspor pada"],
                    "Nilai": [
                        f"Laporan {start_date} s/d {end_date.split()[0]}",
                        start_date,
                        end_date.split()[0],
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    ]
                }
                info_df = pd.DataFrame(info_data)
                info_df.to_excel(writer, sheet_name="Info", index=False)
                
                # Tambahkan dataframe ke Excel
                transaksi_df.to_excel(writer, sheet_name="Transaksi", index=False)
                produk_df.to_excel(writer, sheet_name="Produk Terlaris", index=False)
                stok_df.to_excel(writer, sheet_name="Stok Menipis", index=False)
            
            messagebox.showinfo("Sukses", f"Laporan berhasil diekspor ke {file_path}")
        except ValueError:
            messagebox.showerror("Error", "Format tanggal tidak valid! Gunakan format YYYY-MM-DD")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengekspor laporan: {str(e)}")

# Untuk testing modul secara independen
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Test Laporan View")
    root.geometry("900x600")
    
    class TestController:
        def __init__(self):
            self.current_user = {"id": 1, "username": "admin", "role": "Admin"}
        
        def show_frame(self, frame_name):
            print(f"Showing frame: {frame_name}")
    
    controller = TestController()
    laporan_view = LaporanView(root, controller)
    laporan_view.pack(fill="both", expand=True)
    
    root.mainloop()