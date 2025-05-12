import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Menambahkan path root ke sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from database.database import Database

class ProdukView(tk.Frame):
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
        title_label = tk.Label(header_frame, text="Kelola Produk", font=("Arial", 18, "bold"))
        title_label.pack(side="left")
        
        # Tombol kembali ke dashboard
        back_button = tk.Button(header_frame, text="Kembali ke Dashboard", 
                              command=lambda: controller.show_frame("DashboardView"))
        back_button.pack(side="right")
        
        # Frame untuk form dan tabel
        content_frame = tk.Frame(main_frame)
        content_frame.pack(fill="both", expand=True)
        
        # Frame untuk form input produk
        form_frame = tk.LabelFrame(content_frame, text="Form Produk", padx=10, pady=10)
        form_frame.pack(side="left", fill="y", padx=(0, 10))
        
        # Form fields
        # ID Produk (hidden)
        self.produk_id = None
        
        # Nama Produk
        nama_label = tk.Label(form_frame, text="Nama Produk:")
        nama_label.grid(row=0, column=0, sticky="w", pady=5)
        self.nama_entry = tk.Entry(form_frame, width=30)
        self.nama_entry.grid(row=0, column=1, pady=5, padx=5)
        
        # Kategori
        kategori_label = tk.Label(form_frame, text="Kategori:")
        kategori_label.grid(row=1, column=0, sticky="w", pady=5)
        self.kategori_combobox = ttk.Combobox(form_frame, width=27, state="readonly")
        self.kategori_combobox.grid(row=1, column=1, pady=5, padx=5)
        
        # Harga
        harga_label = tk.Label(form_frame, text="Harga:")
        harga_label.grid(row=2, column=0, sticky="w", pady=5)
        self.harga_entry = tk.Entry(form_frame, width=30)
        self.harga_entry.grid(row=2, column=1, pady=5, padx=5)
        
        # Stok
        stok_label = tk.Label(form_frame, text="Stok:")
        stok_label.grid(row=3, column=0, sticky="w", pady=5)
        self.stok_entry = tk.Entry(form_frame, width=30)
        self.stok_entry.grid(row=3, column=1, pady=5, padx=5)
        
        # Tombol-tombol aksi
        button_frame = tk.Frame(form_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        self.simpan_button = tk.Button(button_frame, text="Simpan", command=self.simpan_produk, width=10)
        self.simpan_button.grid(row=0, column=0, padx=5)
        
        self.batal_button = tk.Button(button_frame, text="Batal", command=self.batal, width=10)
        self.batal_button.grid(row=0, column=1, padx=5)
        
        self.hapus_button = tk.Button(button_frame, text="Hapus", command=self.hapus_produk, width=10, state="disabled")
        self.hapus_button.grid(row=0, column=2, padx=5)
        
        # Frame untuk tabel produk
        table_frame = tk.LabelFrame(content_frame, text="Daftar Produk", padx=10, pady=10)
        table_frame.pack(side="right", fill="both", expand=True)
        
        # Search frame
        search_frame = tk.Frame(table_frame)
        search_frame.pack(fill="x", pady=(0, 10))
        
        search_label = tk.Label(search_frame, text="Cari:")
        search_label.pack(side="left")
        
        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<KeyRelease>", self.search_produk)
        
        # Tabel produk
        self.tree = ttk.Treeview(table_frame, columns=("id", "nama", "kategori", "harga", "stok"), show="headings")
        self.tree.pack(fill="both", expand=True)
        
        # Scrollbar untuk tabel
        scrollbar = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        
        # Definisi kolom
        self.tree.heading("id", text="ID")
        self.tree.heading("nama", text="Nama Produk")
        self.tree.heading("kategori", text="Kategori")
        self.tree.heading("harga", text="Harga")
        self.tree.heading("stok", text="Stok")
        
        # Lebar kolom
        self.tree.column("id", width=50)
        self.tree.column("nama", width=200)
        self.tree.column("kategori", width=150)
        self.tree.column("harga", width=100)
        self.tree.column("stok", width=80)
        
        # Bind event klik pada tabel
        self.tree.bind("<Double-1>", self.on_item_selected)
        
        # Load data awal
        self.load_kategori()
        self.load_produk()
    
    def load_kategori(self):
        """Memuat daftar kategori ke combobox"""
        kategori = self.db.get_all_kategori()
        self.kategori_data = {k["nama"]: k["id"] for k in kategori}
        self.kategori_combobox["values"] = list(self.kategori_data.keys())
        if self.kategori_combobox["values"]:
            self.kategori_combobox.current(0)
    
    def load_produk(self):
        """Memuat daftar produk ke tabel"""
        # Hapus data lama
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Ambil data produk dari database
        produk = self.db.get_all_produk()
        
        # Masukkan ke tabel
        for p in produk:
            kategori_nama = p.get("kategori_nama", "Tidak ada kategori")
            self.tree.insert("", "end", values=(p["id"], p["nama"], kategori_nama, 
                                              f"Rp {p['harga']:,.0f}", p["stok"]))
    
    def search_produk(self, event=None):
        """Mencari produk berdasarkan nama"""
        search_text = self.search_entry.get().lower()
        
        # Hapus data lama
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Ambil data produk dari database
        produk = self.db.get_all_produk()
        
        # Filter dan masukkan ke tabel
        for p in produk:
            if search_text in p["nama"].lower():
                kategori_nama = p.get("kategori_nama", "Tidak ada kategori")
                self.tree.insert("", "end", values=(p["id"], p["nama"], kategori_nama, 
                                                  f"Rp {p['harga']:,.0f}", p["stok"]))
    
    def on_item_selected(self, event):
        """Handler ketika item di tabel dipilih"""
        selected_item = self.tree.focus()
        if selected_item:  # Pastikan ada item yang dipilih
            item_data = self.tree.item(selected_item)
            values = item_data["values"]
            
            # Ambil data produk dari database
            produk = self.db.get_produk(values[0])
            if produk:
                # Isi form dengan data produk
                self.produk_id = produk["id"]
                self.nama_entry.delete(0, tk.END)
                self.nama_entry.insert(0, produk["nama"])
                
                # Set kategori
                if produk["kategori_nama"]:
                    self.kategori_combobox.set(produk["kategori_nama"])
                
                # Set harga (hapus format Rp dan koma)
                self.harga_entry.delete(0, tk.END)
                self.harga_entry.insert(0, str(produk["harga"]))
                
                # Set stok
                self.stok_entry.delete(0, tk.END)
                self.stok_entry.insert(0, str(produk["stok"]))
                
                # Aktifkan tombol hapus
                self.hapus_button.config(state="normal")
    
    def simpan_produk(self):
        """Menyimpan data produk (tambah/update)"""
        # Validasi input
        nama = self.nama_entry.get()
        kategori_nama = self.kategori_combobox.get()
        harga_str = self.harga_entry.get()
        stok_str = self.stok_entry.get()
        
        if not nama or not kategori_nama or not harga_str or not stok_str:
            messagebox.showerror("Error", "Semua field harus diisi!")
            return
        
        try:
            harga = float(harga_str)
            stok = int(stok_str)
            
            if harga <= 0 or stok < 0:
                messagebox.showerror("Error", "Harga harus lebih dari 0 dan stok tidak boleh negatif!")
                return
        except ValueError:
            messagebox.showerror("Error", "Harga dan stok harus berupa angka!")
            return
        
        # Ambil ID kategori
        kategori_id = self.kategori_data.get(kategori_nama)
        
        # Simpan ke database
        if self.produk_id:  # Update
            if self.db.update_produk(self.produk_id, nama, kategori_id, harga, stok):
                messagebox.showinfo("Sukses", "Produk berhasil diperbarui!")
                self.batal()  # Reset form
                self.load_produk()  # Refresh tabel
            else:
                messagebox.showerror("Error", "Gagal memperbarui produk!")
        else:  # Tambah baru
            if self.db.add_produk(nama, kategori_id, harga, stok):
                messagebox.showinfo("Sukses", "Produk berhasil ditambahkan!")
                self.batal()  # Reset form
                self.load_produk()  # Refresh tabel
            else:
                messagebox.showerror("Error", "Gagal menambahkan produk!")
    
    def hapus_produk(self):
        """Menghapus produk"""
        if not self.produk_id:
            return
        
        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus produk ini?"):
            if self.db.delete_produk(self.produk_id):
                messagebox.showinfo("Sukses", "Produk berhasil dihapus!")
                self.batal()  # Reset form
                self.load_produk()  # Refresh tabel
            else:
                messagebox.showerror("Error", "Gagal menghapus produk!")
    
    def batal(self):
        """Reset form"""
        self.produk_id = None
        self.nama_entry.delete(0, tk.END)
        if self.kategori_combobox["values"]:
            self.kategori_combobox.current(0)
        self.harga_entry.delete(0, tk.END)
        self.stok_entry.delete(0, tk.END)
        self.hapus_button.config(state="disabled")

# Untuk testing modul secara independen
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Test Produk View")
    root.geometry("900x600")
    
    class TestController:
        def __init__(self):
            self.current_user = {"username": "admin", "role": "Admin"}
        
        def show_frame(self, frame_name):
            print(f"Showing frame: {frame_name}")
    
    controller = TestController()
    produk_view = ProdukView(root, controller)
    produk_view.pack(fill="both", expand=True)
    
    root.mainloop()