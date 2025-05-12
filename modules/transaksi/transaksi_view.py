import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
from datetime import datetime
import pandas as pd
from tkinter import filedialog

# Menambahkan path root ke sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from database.database import Database

class TransaksiView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.db = Database()
        
        # Inisialisasi keranjang belanja
        self.keranjang = []
        
        # Frame utama dengan padding
        main_frame = tk.Frame(self, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Header
        header_frame = tk.Frame(main_frame)
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Judul
        title_label = tk.Label(header_frame, text="Transaksi Baru", font=("Arial", 18, "bold"))
        title_label.pack(side="left")
        
        # Tombol kembali ke dashboard
        back_button = tk.Button(header_frame, text="Kembali ke Dashboard", 
                              command=lambda: controller.show_frame("DashboardView"))
        back_button.pack(side="right")
        
        # Frame untuk konten transaksi
        content_frame = tk.Frame(main_frame)
        content_frame.pack(fill="both", expand=True)
        
        # Frame kiri: Daftar produk
        produk_frame = tk.LabelFrame(content_frame, text="Daftar Produk", padx=10, pady=10)
        produk_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Search produk
        search_frame = tk.Frame(produk_frame)
        search_frame.pack(fill="x", pady=(0, 10))
        
        search_label = tk.Label(search_frame, text="Cari Produk:")
        search_label.pack(side="left")
        
        self.search_entry = tk.Entry(search_frame, width=25)
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<KeyRelease>", self.search_produk)
        
        # Tabel produk
        produk_table_frame = tk.Frame(produk_frame)
        produk_table_frame.pack(fill="both", expand=True)
        
        self.produk_tree = ttk.Treeview(produk_table_frame, 
                                      columns=("id", "nama", "kategori", "harga", "stok"), 
                                      show="headings")
        self.produk_tree.pack(side="left", fill="both", expand=True)
        
        # Scrollbar untuk tabel produk
        produk_scrollbar = ttk.Scrollbar(produk_table_frame, orient="vertical", command=self.produk_tree.yview)
        self.produk_tree.configure(yscrollcommand=produk_scrollbar.set)
        produk_scrollbar.pack(side="right", fill="y")
        
        # Definisi kolom produk
        self.produk_tree.heading("id", text="ID")
        self.produk_tree.heading("nama", text="Nama Produk")
        self.produk_tree.heading("kategori", text="Kategori")
        self.produk_tree.heading("harga", text="Harga")
        self.produk_tree.heading("stok", text="Stok")
        
        # Lebar kolom produk
        self.produk_tree.column("id", width=40)
        self.produk_tree.column("nama", width=150)
        self.produk_tree.column("kategori", width=100)
        self.produk_tree.column("harga", width=80)
        self.produk_tree.column("stok", width=50)
        
        # Bind event klik pada tabel produk
        self.produk_tree.bind("<Double-1>", self.tambah_ke_keranjang)
        
        # Frame untuk input jumlah
        qty_frame = tk.Frame(produk_frame)
        qty_frame.pack(fill="x", pady=10)
        
        qty_label = tk.Label(qty_frame, text="Jumlah:")
        qty_label.pack(side="left")
        
        self.qty_entry = tk.Entry(qty_frame, width=5)
        self.qty_entry.pack(side="left", padx=5)
        self.qty_entry.insert(0, "1")
        
        tambah_button = tk.Button(qty_frame, text="Tambah ke Keranjang", command=self.tambah_ke_keranjang)
        tambah_button.pack(side="left", padx=5)
        
        # Frame kanan: Keranjang dan total
        keranjang_frame = tk.LabelFrame(content_frame, text="Keranjang Belanja", padx=10, pady=10)
        keranjang_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        # Tabel keranjang
        keranjang_table_frame = tk.Frame(keranjang_frame)
        keranjang_table_frame.pack(fill="both", expand=True)
        
        self.keranjang_tree = ttk.Treeview(keranjang_table_frame, 
                                         columns=("id", "nama", "harga", "qty", "subtotal"), 
                                         show="headings")
        self.keranjang_tree.pack(side="left", fill="both", expand=True)
        
        # Scrollbar untuk tabel keranjang
        keranjang_scrollbar = ttk.Scrollbar(keranjang_table_frame, orient="vertical", command=self.keranjang_tree.yview)
        self.keranjang_tree.configure(yscrollcommand=keranjang_scrollbar.set)
        keranjang_scrollbar.pack(side="right", fill="y")
        
        # Definisi kolom keranjang
        self.keranjang_tree.heading("id", text="ID")
        self.keranjang_tree.heading("nama", text="Nama Produk")
        self.keranjang_tree.heading("harga", text="Harga")
        self.keranjang_tree.heading("qty", text="Qty")
        self.keranjang_tree.heading("subtotal", text="Subtotal")
        
        # Lebar kolom keranjang
        self.keranjang_tree.column("id", width=40)
        self.keranjang_tree.column("nama", width=150)
        self.keranjang_tree.column("harga", width=80)
        self.keranjang_tree.column("qty", width=50)
        self.keranjang_tree.column("subtotal", width=100)
        
        # Bind event klik pada tabel keranjang untuk hapus item
        self.keranjang_tree.bind("<Double-1>", self.hapus_dari_keranjang)
        
        # Frame untuk total dan tombol aksi
        total_frame = tk.Frame(keranjang_frame)
        total_frame.pack(fill="x", pady=10)
        
        # Label total
        total_label = tk.Label(total_frame, text="Total:")
        total_label.grid(row=0, column=0, sticky="w")
        
        self.total_value = tk.Label(total_frame, text="Rp 0", font=("Arial", 12, "bold"))
        self.total_value.grid(row=0, column=1, sticky="w")
        
        # Tombol hapus item
        hapus_button = tk.Button(total_frame, text="Hapus Item", command=self.hapus_dari_keranjang)
        hapus_button.grid(row=1, column=0, pady=5, sticky="w")
        
        # Tombol bersihkan keranjang
        clear_button = tk.Button(total_frame, text="Bersihkan Keranjang", command=self.bersihkan_keranjang)
        clear_button.grid(row=1, column=1, pady=5, padx=5, sticky="w")
        
        # Tombol proses transaksi
        proses_button = tk.Button(total_frame, text="Proses Transaksi", 
                                command=self.proses_transaksi, 
                                bg="#4CAF50", fg="white", 
                                font=("Arial", 10, "bold"))
        proses_button.grid(row=2, column=0, columnspan=2, pady=10, sticky="we")
        
        # Load data produk
        self.load_produk()
    
    def load_produk(self):
        """Memuat daftar produk ke tabel"""
        # Hapus data lama
        for item in self.produk_tree.get_children():
            self.produk_tree.delete(item)
        
        # Ambil data produk dari database
        produk = self.db.get_all_produk()
        
        # Masukkan ke tabel
        for p in produk:
            kategori_nama = p.get("kategori_nama", "Tidak ada kategori")
            self.produk_tree.insert("", "end", values=(p["id"], p["nama"], kategori_nama, 
                                                    f"Rp {p['harga']:,.0f}", p["stok"]))
    
    def search_produk(self, event=None):
        """Mencari produk berdasarkan nama"""
        search_text = self.search_entry.get().lower()
        
        # Hapus data lama
        for item in self.produk_tree.get_children():
            self.produk_tree.delete(item)
        
        # Ambil data produk dari database
        produk = self.db.get_all_produk()
        
        # Filter dan masukkan ke tabel
        for p in produk:
            if search_text in p["nama"].lower():
                kategori_nama = p.get("kategori_nama", "Tidak ada kategori")
                self.produk_tree.insert("", "end", values=(p["id"], p["nama"], kategori_nama, 
                                                        f"Rp {p['harga']:,.0f}", p["stok"]))
    
    def tambah_ke_keranjang(self, event=None):
        """Menambahkan produk ke keranjang"""
        # Ambil produk yang dipilih
        selected_item = self.produk_tree.focus()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih produk terlebih dahulu!")
            return
        
        # Ambil data produk
        item_data = self.produk_tree.item(selected_item)
        values = item_data["values"]
        
        # Ambil jumlah yang diinginkan
        try:
            qty = int(self.qty_entry.get())
            if qty <= 0:
                messagebox.showwarning("Peringatan", "Jumlah harus lebih dari 0!")
                return
        except ValueError:
            messagebox.showwarning("Peringatan", "Jumlah harus berupa angka!")
            return
        
        # Ambil data produk dari database
        produk_id = values[0]
        produk = self.db.get_produk(produk_id)
        
        if not produk:
            messagebox.showerror("Error", "Produk tidak ditemukan!")
            return
        
        # Cek stok
        if qty > produk["stok"]:
            messagebox.showwarning("Peringatan", f"Stok tidak cukup! Stok tersedia: {produk['stok']}")
            return
        
        # Cek apakah produk sudah ada di keranjang
        for i, item in enumerate(self.keranjang):
            if item["id"] == produk_id:
                # Update jumlah jika sudah ada
                new_qty = item["qty"] + qty
                if new_qty > produk["stok"]:
                    messagebox.showwarning("Peringatan", f"Stok tidak cukup! Stok tersedia: {produk['stok']}")
                    return
                
                self.keranjang[i]["qty"] = new_qty
                self.keranjang[i]["subtotal"] = new_qty * produk["harga"]
                self.update_keranjang_display()
                self.update_total()
                return
        
        # Tambahkan ke keranjang jika belum ada
        item = {
            "id": produk_id,
            "nama": produk["nama"],
            "harga": produk["harga"],
            "qty": qty,
            "subtotal": qty * produk["harga"]
        }
        self.keranjang.append(item)
        
        # Update tampilan keranjang
        self.update_keranjang_display()
        self.update_total()
    
    def update_keranjang_display(self):
        """Memperbarui tampilan keranjang"""
        # Hapus data lama
        for item in self.keranjang_tree.get_children():
            self.keranjang_tree.delete(item)
        
        # Masukkan data keranjang ke tabel
        for item in self.keranjang:
            self.keranjang_tree.insert("", "end", values=(
                item["id"], 
                item["nama"], 
                f"Rp {item['harga']:,.0f}", 
                item["qty"], 
                f"Rp {item['subtotal']:,.0f}"
            ))
    
    def update_total(self):
        """Memperbarui total belanja"""
        total = sum(item["subtotal"] for item in self.keranjang)
        self.total_value.config(text=f"Rp {total:,.0f}")
    
    def hapus_dari_keranjang(self, event=None):
        """Menghapus item dari keranjang"""
        selected_item = self.keranjang_tree.focus()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih item yang akan dihapus!")
            return
        
        # Ambil data item
        item_data = self.keranjang_tree.item(selected_item)
        values = item_data["values"]
        
        # Hapus dari keranjang
        for i, item in enumerate(self.keranjang):
            if item["id"] == values[0]:
                self.keranjang.pop(i)
                break
        
        # Update tampilan
        self.update_keranjang_display()
        self.update_total()
    
    def bersihkan_keranjang(self):
        """Mengosongkan keranjang"""
        if not self.keranjang:
            return
        
        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin mengosongkan keranjang?"):
            self.keranjang = []
            self.update_keranjang_display()
            self.update_total()
    
    def proses_transaksi(self):
        """Memproses transaksi"""
        if not self.keranjang:
            messagebox.showwarning("Peringatan", "Keranjang belanja kosong!")
            return
        
        # Cek user yang login
        if not hasattr(self.controller, 'current_user') or not self.controller.current_user:
            messagebox.showerror("Error", "Anda harus login terlebih dahulu!")
            return
        
        # Konfirmasi transaksi
        total = sum(item["subtotal"] for item in self.keranjang)
        if not messagebox.askyesno("Konfirmasi Transaksi", 
                                 f"Total belanja: Rp {total:,.0f}\n\nLanjutkan transaksi?"):
            return
        
        # Format data untuk database
        items = [{
            "produk_id": item["id"],
            "qty": item["qty"],
            "harga": item["harga"]
        } for item in self.keranjang]
        
        # Simpan transaksi ke database
        transaksi_id = self.db.create_transaksi(self.controller.current_user["id"], items)
        
        if transaksi_id:
            messagebox.showinfo("Sukses", "Transaksi berhasil disimpan!")
            
            # Tanyakan apakah ingin mencetak struk
            if messagebox.askyesno("Cetak Struk", "Apakah Anda ingin mencetak struk?"):
                self.cetak_struk(transaksi_id)
            
            # Tanyakan apakah ingin mengekspor ke Excel
            if messagebox.askyesno("Ekspor Data", "Apakah Anda ingin mengekspor transaksi ke Excel?"):
                self.ekspor_ke_excel(transaksi_id)
            
            # Bersihkan keranjang
            self.keranjang = []
            self.update_keranjang_display()
            self.update_total()
            
            # Refresh data produk
            self.load_produk()
        else:
            messagebox.showerror("Error", "Gagal menyimpan transaksi!")
    
    def cetak_struk(self, transaksi_id):
        """Mencetak struk transaksi"""
        # Ambil data transaksi
        transaksi = self.db.get_transaksi(transaksi_id)
        if not transaksi:
            messagebox.showerror("Error", "Data transaksi tidak ditemukan!")
            return
        
        # Buat window baru untuk preview struk
        struk_window = tk.Toplevel(self)
        struk_window.title("Preview Struk")
        struk_window.geometry("400x500")
        
        # Frame untuk struk
        struk_frame = tk.Frame(struk_window, padx=20, pady=20)
        struk_frame.pack(fill="both", expand=True)
        
        # Header struk
        header_label = tk.Label(struk_frame, text="STRUK PEMBELIAN", font=("Arial", 12, "bold"))
        header_label.pack(pady=(0, 10))
        
        toko_label = tk.Label(struk_frame, text="POS & Inventory Management")
        toko_label.pack()
        
        alamat_label = tk.Label(struk_frame, text="Jl. Contoh No. 123, Kota")
        alamat_label.pack()
        
        # Garis pemisah
        separator = tk.Frame(struk_frame, height=2, bd=1, relief=tk.SUNKEN)
        separator.pack(fill="x", pady=10)
        
        # Info transaksi
        info_frame = tk.Frame(struk_frame)
        info_frame.pack(fill="x")
        
        # Tanggal dan No. Transaksi
        tanggal_label = tk.Label(info_frame, text=f"Tanggal: {transaksi['tanggal']}")
        tanggal_label.pack(anchor="w")
        
        no_transaksi_label = tk.Label(info_frame, text=f"No. Transaksi: {transaksi['id']}")
        no_transaksi_label.pack(anchor="w")
        
        kasir_label = tk.Label(info_frame, text=f"Kasir: {transaksi['username']}")
        kasir_label.pack(anchor="w")
        
        # Garis pemisah
        separator2 = tk.Frame(struk_frame, height=2, bd=1, relief=tk.SUNKEN)
        separator2.pack(fill="x", pady=10)
        
        # Daftar item
        item_frame = tk.Frame(struk_frame)
        item_frame.pack(fill="x")
        
        # Header item
        tk.Label(item_frame, text="Nama", width=20, anchor="w").grid(row=0, column=0, sticky="w")
        tk.Label(item_frame, text="Qty", width=5).grid(row=0, column=1)
        tk.Label(item_frame, text="Harga", width=10).grid(row=0, column=2)
        tk.Label(item_frame, text="Subtotal", width=10).grid(row=0, column=3)
        
        # Daftar item
        for i, item in enumerate(transaksi["items"]):
            tk.Label(item_frame, text=item["produk_nama"], width=20, anchor="w").grid(row=i+1, column=0, sticky="w")
            tk.Label(item_frame, text=str(item["qty"]), width=5).grid(row=i+1, column=1)
            tk.Label(item_frame, text=f"Rp {item['harga']:,.0f}", width=10).grid(row=i+1, column=2)
            subtotal = item["qty"] * item["harga"]
            tk.Label(item_frame, text=f"Rp {subtotal:,.0f}", width=10).grid(row=i+1, column=3)
        
        # Garis pemisah
        separator3 = tk.Frame(struk_frame, height=2, bd=1, relief=tk.SUNKEN)
        separator3.pack(fill="x", pady=10)
        
        # Total
        total_frame = tk.Frame(struk_frame)
        total_frame.pack(fill="x")
        
        tk.Label(total_frame, text="Total:", font=("Arial", 10, "bold")).pack(side="left")
        tk.Label(total_frame, text=f"Rp {transaksi['total']:,.0f}", font=("Arial", 10, "bold")).pack(side="right")
        
        # Footer
        footer_frame = tk.Frame(struk_frame)
        footer_frame.pack(fill="x", pady=20)
        
        tk.Label(footer_frame, text="Terima kasih telah berbelanja", font=("Arial", 10)).pack()
        tk.Label(footer_frame, text="Barang yang sudah dibeli tidak dapat dikembalikan").pack()
        
        # Tombol cetak
        print_button = tk.Button(struk_frame, text="Cetak", command=lambda: self.print_struk(struk_window))
        print_button.pack(pady=10)
    
    def print_struk(self, window):
        """Simulasi mencetak struk (dalam aplikasi nyata akan terhubung ke printer)"""
        messagebox.showinfo("Cetak Struk", "Struk berhasil dicetak!")
        window.destroy()
    
    def ekspor_ke_excel(self, transaksi_id):
        """Mengekspor data transaksi ke file Excel"""
        # Ambil data transaksi
        transaksi = self.db.get_transaksi(transaksi_id)
        if not transaksi:
            messagebox.showerror("Error", "Data transaksi tidak ditemukan!")
            return
        
        # Buat dataframe untuk header transaksi
        header_data = {
            "No. Transaksi": [transaksi["id"]],
            "Tanggal": [transaksi["tanggal"]],
            "Kasir": [transaksi["username"]],
            "Total": [transaksi["total"]]
        }
        header_df = pd.DataFrame(header_data)
        
        # Buat dataframe untuk detail transaksi
        detail_data = {
            "Nama Produk": [],
            "Qty": [],
            "Harga": [],
            "Subtotal": []
        }
        
        for item in transaksi["items"]:
            detail_data["Nama Produk"].append(item["produk_nama"])
            detail_data["Qty"].append(item["qty"])
            detail_data["Harga"].append(item["harga"])
            detail_data["Subtotal"].append(item["qty"] * item["harga"])
        
        detail_df = pd.DataFrame(detail_data)
        
        # Buka dialog untuk menyimpan file
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            initialfile=f"Transaksi_{transaksi['id']}_{datetime.now().strftime('%Y%m%d')}.xlsx"
        )
        
        if not file_path:
            return
        
        try:
            # Buat Excel writer
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                header_df.to_excel(writer, sheet_name="Transaksi", index=False)
                detail_df.to_excel(writer, sheet_name="Detail", index=False)
            
            messagebox.showinfo("Sukses", f"Data berhasil diekspor ke {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengekspor data: {str(e)}")

# Untuk testing modul secara independen
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Test Transaksi View")
    root.geometry("1000x600")
    
    class TestController:
        def __init__(self):
            self.current_user = {"id": 1, "username": "admin", "role": "Admin"}
        
        def show_frame(self, frame_name):
            print(f"Showing frame: {frame_name}")
    
    controller = TestController()
    transaksi_view = TransaksiView(root, controller)
    transaksi_view.pack(fill="both", expand=True)
    
    root.mainloop()