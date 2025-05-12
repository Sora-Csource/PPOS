import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Menambahkan path root ke sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from database.database import Database

class KategoriView(tk.Frame):
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
        title_label = tk.Label(header_frame, text="Kelola Kategori", font=("Arial", 18, "bold"))
        title_label.pack(side="left")
        
        # Tombol kembali ke dashboard
        back_button = tk.Button(header_frame, text="Kembali ke Dashboard", 
                              command=lambda: controller.show_frame("DashboardView"))
        back_button.pack(side="right")
        
        # Frame untuk form dan tabel
        content_frame = tk.Frame(main_frame)
        content_frame.pack(fill="both", expand=True)
        
        # Frame untuk form input kategori
        form_frame = tk.LabelFrame(content_frame, text="Form Kategori", padx=10, pady=10)
        form_frame.pack(side="left", fill="y", padx=(0, 10))
        
        # Form fields
        # ID Kategori (hidden)
        self.kategori_id = None
        
        # Nama Kategori
        nama_label = tk.Label(form_frame, text="Nama Kategori:")
        nama_label.grid(row=0, column=0, sticky="w", pady=5)
        self.nama_entry = tk.Entry(form_frame, width=30)
        self.nama_entry.grid(row=0, column=1, pady=5, padx=5)
        
        # Tombol-tombol aksi
        button_frame = tk.Frame(form_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        self.simpan_button = tk.Button(button_frame, text="Simpan", command=self.simpan_kategori, width=10)
        self.simpan_button.grid(row=0, column=0, padx=5)
        
        self.batal_button = tk.Button(button_frame, text="Batal", command=self.batal, width=10)
        self.batal_button.grid(row=0, column=1, padx=5)
        
        self.hapus_button = tk.Button(button_frame, text="Hapus", command=self.hapus_kategori, width=10, state="disabled")
        self.hapus_button.grid(row=0, column=2, padx=5)
        
        # Frame untuk tabel kategori
        table_frame = tk.LabelFrame(content_frame, text="Daftar Kategori", padx=10, pady=10)
        table_frame.pack(side="right", fill="both", expand=True)
        
        # Search frame
        search_frame = tk.Frame(table_frame)
        search_frame.pack(fill="x", pady=(0, 10))
        
        search_label = tk.Label(search_frame, text="Cari:")
        search_label.pack(side="left")
        
        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<KeyRelease>", self.search_kategori)
        
        # Tabel kategori
        self.tree = ttk.Treeview(table_frame, columns=("id", "nama", "jumlah_produk"), show="headings")
        self.tree.pack(fill="both", expand=True)
        
        # Scrollbar untuk tabel
        scrollbar = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        
        # Definisi kolom
        self.tree.heading("id", text="ID")
        self.tree.heading("nama", text="Nama Kategori")
        self.tree.heading("jumlah_produk", text="Jumlah Produk")
        
        # Lebar kolom
        self.tree.column("id", width=50)
        self.tree.column("nama", width=200)
        self.tree.column("jumlah_produk", width=100)
        
        # Bind event klik pada tabel
        self.tree.bind("<Double-1>", self.on_item_selected)
        
        # Load data awal
        self.load_kategori()
    
    def load_kategori(self):
        """Memuat daftar kategori ke tabel"""
        # Hapus data lama
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Ambil data kategori dari database
        kategori = self.db.get_all_kategori()
        
        # Hitung jumlah produk per kategori
        produk = self.db.get_all_produk()
        produk_per_kategori = {}
        for p in produk:
            if p["kategori_id"] in produk_per_kategori:
                produk_per_kategori[p["kategori_id"]] += 1
            else:
                produk_per_kategori[p["kategori_id"]] = 1
        
        # Masukkan ke tabel
        for k in kategori:
            jumlah_produk = produk_per_kategori.get(k["id"], 0)
            self.tree.insert("", "end", values=(k["id"], k["nama"], jumlah_produk))
    
    def search_kategori(self, event=None):
        """Mencari kategori berdasarkan nama"""
        search_text = self.search_entry.get().lower()
        
        # Hapus data lama
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Ambil data kategori dari database
        kategori = self.db.get_all_kategori()
        
        # Hitung jumlah produk per kategori
        produk = self.db.get_all_produk()
        produk_per_kategori = {}
        for p in produk:
            if p["kategori_id"] in produk_per_kategori:
                produk_per_kategori[p["kategori_id"]] += 1
            else:
                produk_per_kategori[p["kategori_id"]] = 1
        
        # Filter dan masukkan ke tabel
        for k in kategori:
            if search_text in k["nama"].lower():
                jumlah_produk = produk_per_kategori.get(k["id"], 0)
                self.tree.insert("", "end", values=(k["id"], k["nama"], jumlah_produk))
    
    def on_item_selected(self, event):
        """Handler ketika item di tabel dipilih"""
        selected_item = self.tree.focus()
        if selected_item:  # Pastikan ada item yang dipilih
            item_data = self.tree.item(selected_item)
            values = item_data["values"]
            
            # Isi form dengan data kategori
            self.kategori_id = values[0]
            self.nama_entry.delete(0, tk.END)
            self.nama_entry.insert(0, values[1])
            
            # Aktifkan tombol hapus
            self.hapus_button.config(state="normal")
    
    def simpan_kategori(self):
        """Menyimpan data kategori (tambah/update)"""
        # Validasi input
        nama = self.nama_entry.get()
        
        if not nama:
            messagebox.showerror("Error", "Nama kategori harus diisi!")
            return
        
        # Simpan ke database
        if self.kategori_id:  # Update
            if self.db.update_kategori(self.kategori_id, nama):
                messagebox.showinfo("Sukses", "Kategori berhasil diperbarui!")
                self.batal()  # Reset form
                self.load_kategori()  # Refresh tabel
            else:
                messagebox.showerror("Error", "Gagal memperbarui kategori!")
        else:  # Tambah baru
            if self.db.add_kategori(nama):
                messagebox.showinfo("Sukses", "Kategori berhasil ditambahkan!")
                self.batal()  # Reset form
                self.load_kategori()  # Refresh tabel
            else:
                messagebox.showerror("Error", "Gagal menambahkan kategori!")
    
    def hapus_kategori(self):
        """Menghapus kategori"""
        if not self.kategori_id:
            return
        
        # Cek apakah kategori masih digunakan oleh produk
        produk = self.db.get_all_produk()
        produk_dengan_kategori = [p for p in produk if p["kategori_id"] == self.kategori_id]
        
        if produk_dengan_kategori:
            messagebox.showerror("Error", "Kategori ini masih digunakan oleh produk! Hapus atau ubah kategori produk terlebih dahulu.")
            return
        
        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus kategori ini?"):
            if self.db.delete_kategori(self.kategori_id):
                messagebox.showinfo("Sukses", "Kategori berhasil dihapus!")
                self.batal()  # Reset form
                self.load_kategori()  # Refresh tabel
            else:
                messagebox.showerror("Error", "Gagal menghapus kategori!")
    
    def batal(self):
        """Reset form"""
        self.kategori_id = None
        self.nama_entry.delete(0, tk.END)
        self.hapus_button.config(state="disabled")

# Untuk testing modul secara independen
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Test Kategori View")
    root.geometry("800x500")
    
    class TestController:
        def __init__(self):
            self.current_user = {"username": "admin", "role": "Admin"}
        
        def show_frame(self, frame_name):
            print(f"Showing frame: {frame_name}")
    
    controller = TestController()
    kategori_view = KategoriView(root, controller)
    kategori_view.pack(fill="both", expand=True)
    
    root.mainloop()