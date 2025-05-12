import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Menambahkan path root ke sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from database.database import Database

class ProdukKategoriView(tk.Frame):
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
        title_label = tk.Label(header_frame, text="Manajemen Produk & Kategori", font=("Arial", 18, "bold"))
        title_label.pack(side="left")
        
        # Tombol kembali ke dashboard
        back_button = tk.Button(header_frame, text="Kembali ke Dashboard", 
                              command=lambda: controller.show_frame("DashboardView"))
        back_button.pack(side="right")
        
        # Notebook (Tab Control)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill="both", expand=True)
        
        # Tab Produk
        self.produk_tab = tk.Frame(self.notebook)
        self.notebook.add(self.produk_tab, text="Produk")
        
        # Tab Kategori
        self.kategori_tab = tk.Frame(self.notebook)
        self.notebook.add(self.kategori_tab, text="Kategori")
        
        # Setup Produk Tab
        self.setup_produk_tab()
        
        # Setup Kategori Tab
        self.setup_kategori_tab()
        
        # Bind event saat tab berubah
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
    
    def on_tab_changed(self, event):
        """Handler saat tab berubah"""
        current_tab = self.notebook.index("current")
        
        # Reset form pada tab sebelumnya
        if current_tab == 0:  # Produk tab
            # Reset form kategori jika ada perubahan yang belum disimpan
            if self.kategori_nama_entry.get().strip():
                if messagebox.askyesno("Konfirmasi", "Ada perubahan pada form kategori yang belum disimpan. Simpan sekarang?"):
                    self.simpan_kategori()
                else:
                    self.batal_kategori()
            # Muat data produk
            self.load_produk()
            # Fokus ke field pencarian produk
            self.search_produk_entry.focus()
        elif current_tab == 1:  # Kategori tab
            # Reset form produk jika ada perubahan yang belum disimpan
            if (self.nama_entry.get().strip() or self.harga_entry.get().strip() or self.stok_entry.get().strip()):
                if messagebox.askyesno("Konfirmasi", "Ada perubahan pada form produk yang belum disimpan. Simpan sekarang?"):
                    self.simpan_produk()
                else:
                    self.batal_produk()
            # Muat data kategori
            self.load_kategori()
            # Fokus ke field pencarian kategori
            self.search_kategori_entry.focus()
    
    def setup_produk_tab(self):
        """Setup tampilan tab produk"""
        # Frame untuk form dan tabel
        content_frame = tk.Frame(self.produk_tab)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
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
        
        self.simpan_produk_button = tk.Button(button_frame, text="Simpan", command=self.simpan_produk, width=10)
        self.simpan_produk_button.grid(row=0, column=0, padx=5)
        
        self.batal_produk_button = tk.Button(button_frame, text="Batal", command=self.batal_produk, width=10)
        self.batal_produk_button.grid(row=0, column=1, padx=5)
        
        self.hapus_produk_button = tk.Button(button_frame, text="Hapus", command=self.hapus_produk, width=10, state="disabled")
        self.hapus_produk_button.grid(row=0, column=2, padx=5)
        
        # Frame untuk tabel produk
        table_frame = tk.LabelFrame(content_frame, text="Daftar Produk", padx=10, pady=10)
        table_frame.pack(side="right", fill="both", expand=True)
        
        # Search frame
        search_frame = tk.Frame(table_frame)
        search_frame.pack(fill="x", pady=(0, 10))
        
        search_label = tk.Label(search_frame, text="Cari:")
        search_label.pack(side="left")
        
        self.search_produk_entry = tk.Entry(search_frame, width=30)
        self.search_produk_entry.pack(side="left", padx=5)
        self.search_produk_entry.bind("<KeyRelease>", self.search_produk)
        
        # Status label untuk hasil pencarian
        self.status_label = tk.Label(table_frame, text="Menampilkan semua produk", anchor="w")
        self.status_label.pack(fill="x", pady=(0, 5))
        
        # Tabel produk
        self.produk_tree = ttk.Treeview(table_frame, columns=("id", "nama", "kategori", "harga", "stok"), show="headings")
        self.produk_tree.pack(fill="both", expand=True)
        
        # Scrollbar untuk tabel
        scrollbar = ttk.Scrollbar(self.produk_tree, orient="vertical", command=self.produk_tree.yview)
        self.produk_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        
        # Definisi kolom
        self.produk_tree.heading("id", text="ID")
        self.produk_tree.heading("nama", text="Nama Produk")
        self.produk_tree.heading("kategori", text="Kategori")
        self.produk_tree.heading("harga", text="Harga")
        self.produk_tree.heading("stok", text="Stok")
        
        # Lebar kolom
        self.produk_tree.column("id", width=50)
        self.produk_tree.column("nama", width=200)
        self.produk_tree.column("kategori", width=150)
        self.produk_tree.column("harga", width=100)
        self.produk_tree.column("stok", width=80)
        
        # Bind event klik pada tabel
        self.produk_tree.bind("<Double-1>", self.on_produk_selected)
    
    def setup_kategori_tab(self):
        """Setup tampilan tab kategori"""
        # Frame untuk form dan tabel
        content_frame = tk.Frame(self.kategori_tab)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Frame untuk form input kategori
        form_frame = tk.LabelFrame(content_frame, text="Form Kategori", padx=10, pady=10)
        form_frame.pack(side="left", fill="y", padx=(0, 10))
        
        # Form fields
        # ID Kategori (hidden)
        self.kategori_id = None
        
        # Nama Kategori
        nama_label = tk.Label(form_frame, text="Nama Kategori:")
        nama_label.grid(row=0, column=0, sticky="w", pady=5)
        self.kategori_nama_entry = tk.Entry(form_frame, width=30)
        self.kategori_nama_entry.grid(row=0, column=1, pady=5, padx=5)
        
        # Tombol-tombol aksi
        button_frame = tk.Frame(form_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        self.simpan_kategori_button = tk.Button(button_frame, text="Simpan", command=self.simpan_kategori, width=10)
        self.simpan_kategori_button.grid(row=0, column=0, padx=5)
        
        self.batal_kategori_button = tk.Button(button_frame, text="Batal", command=self.batal_kategori, width=10)
        self.batal_kategori_button.grid(row=0, column=1, padx=5)
        
        self.hapus_kategori_button = tk.Button(button_frame, text="Hapus", command=self.hapus_kategori, width=10, state="disabled")
        self.hapus_kategori_button.grid(row=0, column=2, padx=5)
        
        # Frame untuk tabel kategori
        table_frame = tk.LabelFrame(content_frame, text="Daftar Kategori", padx=10, pady=10)
        table_frame.pack(side="right", fill="both", expand=True)
        
        # Search frame
        search_frame = tk.Frame(table_frame)
        search_frame.pack(fill="x", pady=(0, 10))
        
        search_label = tk.Label(search_frame, text="Cari:")
        search_label.pack(side="left")
        
        self.search_kategori_entry = tk.Entry(search_frame, width=30)
        self.search_kategori_entry.pack(side="left", padx=5)
        self.search_kategori_entry.bind("<KeyRelease>", self.search_kategori)
        
        # Status label untuk hasil pencarian
        self.kategori_status_label = tk.Label(table_frame, text="Menampilkan semua kategori", anchor="w")
        self.kategori_status_label.pack(fill="x", pady=(0, 5))
        
        # Tabel kategori
        self.kategori_tree = ttk.Treeview(table_frame, columns=("id", "nama", "jumlah_produk"), show="headings")
        self.kategori_tree.pack(fill="both", expand=True)
        
        # Scrollbar untuk tabel
        scrollbar = ttk.Scrollbar(self.kategori_tree, orient="vertical", command=self.kategori_tree.yview)
        self.kategori_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        
        # Definisi kolom
        self.kategori_tree.heading("id", text="ID")
        self.kategori_tree.heading("nama", text="Nama Kategori")
        self.kategori_tree.heading("jumlah_produk", text="Jumlah Produk")
        
        # Lebar kolom
        self.kategori_tree.column("id", width=50)
        self.kategori_tree.column("nama", width=200)
        self.kategori_tree.column("jumlah_produk", width=100)
        
        # Bind event klik pada tabel
        self.kategori_tree.bind("<Double-1>", self.on_kategori_selected)
    
    # ===== METODE UNTUK PRODUK =====
    def load_produk(self):
        """Memuat daftar produk ke tabel"""
        # Hapus data lama
        for item in self.produk_tree.get_children():
            self.produk_tree.delete(item)
        
        # Ambil data produk dari database
        produk = self.db.get_all_produk()
        
        # Masukkan ke tabel dengan warna baris bergantian
        for i, p in enumerate(produk):
            kategori_nama = p.get("kategori_nama", "Tidak ada kategori")
            item_id = self.produk_tree.insert("", "end", values=(p["id"], p["nama"], kategori_nama, 
                                              f"Rp {p['harga']:,.0f}", p["stok"]))
            
            # Beri warna baris bergantian untuk kemudahan membaca
            if i % 2 == 0:
                self.produk_tree.item(item_id, tags=("evenrow",))
            else:
                self.produk_tree.item(item_id, tags=("oddrow",))
                
        # Update status label
        if produk:
            self.status_label.config(text=f"Menampilkan {len(produk)} produk")
        else:
            self.status_label.config(text="Tidak ada produk yang tersedia")
            
        # Konfigurasi tag untuk warna baris
        self.produk_tree.tag_configure("evenrow", background="#f0f0f0")
        self.produk_tree.tag_configure("oddrow", background="white")
        
        # Refresh kategori combobox
        self.load_kategori_combobox()
    
    def load_kategori_combobox(self):
        """Memuat daftar kategori ke combobox"""
        kategori = self.db.get_all_kategori()
        self.kategori_data = {k["nama"]: k["id"] for k in kategori}
        self.kategori_combobox["values"] = list(self.kategori_data.keys())
        if self.kategori_combobox["values"]:
            self.kategori_combobox.current(0)
    
    def search_produk(self, event=None):
        """Mencari produk berdasarkan nama atau kategori"""
        search_text = self.search_produk_entry.get().lower().strip()
        
        # Hapus data lama
        for item in self.produk_tree.get_children():
            self.produk_tree.delete(item)
        
        # Ambil data produk dari database
        produk = self.db.get_all_produk()
        
        # Filter dan masukkan ke tabel dengan warna baris bergantian
        found_items = 0
        filtered_produk = []
        
        # Filter produk berdasarkan kata kunci
        for p in produk:
            # Cari berdasarkan nama produk, kategori, atau harga
            if (search_text in p["nama"].lower() or 
                (p.get("kategori_nama") and search_text in p.get("kategori_nama", "").lower()) or
                search_text in str(p["harga"])):
                filtered_produk.append(p)
        
        # Masukkan ke tabel dengan warna baris bergantian
        for i, p in enumerate(filtered_produk):
            kategori_nama = p.get("kategori_nama", "Tidak ada kategori")
            item_id = self.produk_tree.insert("", "end", values=(p["id"], p["nama"], kategori_nama, 
                                              f"Rp {p['harga']:,.0f}", p["stok"]))
            
            # Beri warna baris bergantian untuk kemudahan membaca
            if i % 2 == 0:
                self.produk_tree.item(item_id, tags=("evenrow",))
            else:
                self.produk_tree.item(item_id, tags=("oddrow",))
                
            found_items += 1
        
        # Update status pencarian
        if search_text:
            if found_items == 0:
                messagebox.showinfo("Hasil Pencarian", f"Tidak ditemukan produk dengan kata kunci '{search_text}'")
                self.status_label.config(text=f"Tidak ditemukan produk dengan kata kunci '{search_text}'")
            elif found_items == 1:
                self.status_label.config(text=f"Ditemukan 1 produk dengan kata kunci '{search_text}'")
            else:
                self.status_label.config(text=f"Ditemukan {found_items} produk dengan kata kunci '{search_text}'")
        else:
            self.status_label.config(text=f"Menampilkan {len(produk)} produk")
            
        # Jika tidak ada hasil pencarian dan search_text kosong, tampilkan semua produk
        if found_items == 0 and not search_text:
            self.load_produk()
            
        # Konfigurasi tag untuk warna baris
        self.produk_tree.tag_configure("evenrow", background="#f0f0f0")
        self.produk_tree.tag_configure("oddrow", background="white")
    
    def on_produk_selected(self, event):
        """Handler ketika item di tabel produk dipilih"""
        selected_item = self.produk_tree.focus()
        if selected_item:  # Pastikan ada item yang dipilih
            item_data = self.produk_tree.item(selected_item)
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
                self.hapus_produk_button.config(state="normal")
    
    def simpan_produk(self):
        """Menyimpan data produk (tambah/update)"""
        # Validasi input
        nama = self.nama_entry.get().strip()
        kategori = self.kategori_combobox.get()
        harga_str = self.harga_entry.get().strip()
        stok_str = self.stok_entry.get().strip()
        
        # Validasi field kosong
        if not nama:
            messagebox.showerror("Error", "Nama produk tidak boleh kosong!")
            self.nama_entry.focus()
            return
            
        if not kategori:
            messagebox.showerror("Error", "Kategori harus dipilih!")
            self.kategori_combobox.focus()
            return
            
        if not harga_str:
            messagebox.showerror("Error", "Harga produk tidak boleh kosong!")
            self.harga_entry.focus()
            return
            
        if not stok_str:
            messagebox.showerror("Error", "Stok produk tidak boleh kosong!")
            self.stok_entry.focus()
            return
        
        # Validasi format angka
        try:
            harga = int(harga_str)
            if harga < 0:
                messagebox.showerror("Error", "Harga tidak boleh negatif!")
                self.harga_entry.focus()
                return
        except ValueError:
            messagebox.showerror("Error", "Harga harus berupa angka!")
            self.harga_entry.focus()
            self.harga_entry.select_range(0, tk.END)
            return
            
        try:
            stok = int(stok_str)
            if stok < 0:
                messagebox.showerror("Error", "Stok tidak boleh negatif!")
                self.stok_entry.focus()
                return
        except ValueError:
            messagebox.showerror("Error", "Stok harus berupa angka!")
            self.stok_entry.focus()
            self.stok_entry.select_range(0, tk.END)
            return
        
        # Ambil ID kategori
        kategori_id = self.kategori_data.get(kategori)
        if not kategori_id:
            messagebox.showerror("Error", "Kategori tidak valid!")
            return
        
        # Konfirmasi sebelum menyimpan
        aksi = "memperbarui" if self.produk_id else "menambahkan"
        if not messagebox.askyesno("Konfirmasi", f"Apakah Anda yakin ingin {aksi} produk ini?\n\nNama: {nama}\nKategori: {kategori}\nHarga: Rp {harga:,}\nStok: {stok}"):
            return
        
        # Simpan ke database
        if self.produk_id:  # Update
            if self.db.update_produk(self.produk_id, nama, kategori_id, harga, stok):
                messagebox.showinfo("Sukses", "Produk berhasil diperbarui!")
                self.batal_produk()  # Reset form
                self.load_produk()  # Refresh tabel
                # Refresh kategori tab juga karena jumlah produk mungkin berubah
                self.load_kategori()
            else:
                messagebox.showerror("Error", "Gagal memperbarui produk!")
        else:  # Tambah baru
            if self.db.add_produk(nama, kategori_id, harga, stok):
                messagebox.showinfo("Sukses", "Produk berhasil ditambahkan!")
                self.batal_produk()  # Reset form
                self.load_produk()  # Refresh tabel
                # Refresh kategori tab juga karena jumlah produk berubah
                self.load_kategori()
            else:
                messagebox.showerror("Error", "Gagal menambahkan produk!")
                
        # Fokus kembali ke field nama untuk entry berikutnya
        self.nama_entry.focus()
    
    def hapus_produk(self):
        """Menghapus produk"""
        if not self.produk_id:
            messagebox.showwarning("Peringatan", "Tidak ada produk yang dipilih untuk dihapus!")
            return
        
        # Dapatkan detail produk untuk konfirmasi
        produk = self.db.get_produk(self.produk_id)
        if not produk:
            messagebox.showerror("Error", "Produk tidak ditemukan di database!")
            self.batal_produk()
            return
            
        # Konfirmasi dengan detail produk
        if messagebox.askyesno("Konfirmasi Penghapusan", 
                             f"Apakah Anda yakin ingin menghapus produk ini?\n\n" 
                             f"Nama: {produk['nama']}\n" 
                             f"Kategori: {produk['kategori_nama'] or 'Tidak ada kategori'}\n" 
                             f"Harga: Rp {produk['harga']:,}\n" 
                             f"Stok: {produk['stok']}"):
            try:
                if self.db.delete_produk(self.produk_id):
                    messagebox.showinfo("Sukses", f"Produk '{produk['nama']}' berhasil dihapus!")
                    self.batal_produk()  # Reset form
                    self.load_produk()  # Refresh tabel
                    # Refresh kategori tab juga karena jumlah produk berubah
                    self.load_kategori()
                else:
                    messagebox.showerror("Error", "Gagal menghapus produk!")
            except Exception as e:
                messagebox.showerror("Error", f"Terjadi kesalahan saat menghapus produk: {str(e)}")
        
        # Fokus kembali ke tabel produk
        self.produk_tree.focus_set()
    
    def batal_produk(self):
        """Reset form produk"""
        # Cek apakah ada perubahan yang belum disimpan
        if (self.nama_entry.get().strip() or 
            self.harga_entry.get().strip() or 
            self.stok_entry.get().strip()):
            if not messagebox.askyesno("Konfirmasi", "Ada perubahan yang belum disimpan. Yakin ingin membatalkan?"):
                return
        
        # Reset form
        self.produk_id = None
        self.nama_entry.delete(0, tk.END)
        if self.kategori_combobox["values"]:
            self.kategori_combobox.current(0)
        self.harga_entry.delete(0, tk.END)
        self.stok_entry.delete(0, tk.END)
        self.hapus_produk_button.config(state="disabled")
        
        # Fokus kembali ke field nama
        self.nama_entry.focus()
    
    # ===== METODE UNTUK KATEGORI =====
    def load_kategori(self):
        """Memuat daftar kategori ke tabel"""
        # Hapus data lama
        for item in self.kategori_tree.get_children():
            self.kategori_tree.delete(item)
        
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
        
        # Masukkan ke tabel dengan warna baris bergantian
        for i, k in enumerate(kategori):
            jumlah_produk = produk_per_kategori.get(k["id"], 0)
            item_id = self.kategori_tree.insert("", "end", values=(k["id"], k["nama"], jumlah_produk))
            
            # Beri warna baris bergantian untuk kemudahan membaca
            if i % 2 == 0:
                self.kategori_tree.item(item_id, tags=("evenrow",))
            else:
                self.kategori_tree.item(item_id, tags=("oddrow",))
                
        # Update status label
        if kategori:
            self.kategori_status_label.config(text=f"Menampilkan {len(kategori)} kategori")
        else:
            self.kategori_status_label.config(text="Tidak ada kategori yang tersedia")
            
        # Konfigurasi tag untuk warna baris
        self.kategori_tree.tag_configure("evenrow", background="#f0f0f0")
        self.kategori_tree.tag_configure("oddrow", background="white")
    
    def search_kategori(self, event=None):
        """Mencari kategori berdasarkan nama"""
        search_text = self.search_kategori_entry.get().lower().strip()
        
        # Hapus data lama
        for item in self.kategori_tree.get_children():
            self.kategori_tree.delete(item)
        
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
        
        # Filter kategori berdasarkan kata kunci
        filtered_kategori = []
        for k in kategori:
            if search_text in k["nama"].lower():
                filtered_kategori.append(k)
        
        # Masukkan ke tabel dengan warna baris bergantian
        found_items = 0
        for i, k in enumerate(filtered_kategori):
            jumlah_produk = produk_per_kategori.get(k["id"], 0)
            item_id = self.kategori_tree.insert("", "end", values=(k["id"], k["nama"], jumlah_produk))
            
            # Beri warna baris bergantian untuk kemudahan membaca
            if i % 2 == 0:
                self.kategori_tree.item(item_id, tags=("evenrow",))
            else:
                self.kategori_tree.item(item_id, tags=("oddrow",))
                
            found_items += 1
        
        # Update status pencarian
        if search_text:
            if found_items == 0:
                messagebox.showinfo("Hasil Pencarian", f"Tidak ditemukan kategori dengan kata kunci '{search_text}'")
                self.kategori_status_label.config(text=f"Tidak ditemukan kategori dengan kata kunci '{search_text}'")
            elif found_items == 1:
                self.kategori_status_label.config(text=f"Ditemukan 1 kategori dengan kata kunci '{search_text}'")
            else:
                self.kategori_status_label.config(text=f"Ditemukan {found_items} kategori dengan kata kunci '{search_text}'")
        else:
            self.kategori_status_label.config(text=f"Menampilkan {len(kategori)} kategori")
            
        # Jika tidak ada hasil pencarian dan search_text kosong, tampilkan semua kategori
        if found_items == 0 and not search_text:
            self.load_kategori()
            
        # Konfigurasi tag untuk warna baris
        self.kategori_tree.tag_configure("evenrow", background="#f0f0f0")
        self.kategori_tree.tag_configure("oddrow", background="white")
    
    def on_kategori_selected(self, event):
        """Handler ketika item di tabel kategori dipilih"""
        selected_item = self.kategori_tree.focus()
        if selected_item:  # Pastikan ada item yang dipilih
            item_data = self.kategori_tree.item(selected_item)
            values = item_data["values"]
            
            # Isi form dengan data kategori
            self.kategori_id = values[0]
            self.kategori_nama_entry.delete(0, tk.END)
            self.kategori_nama_entry.insert(0, values[1])
            
            # Aktifkan tombol hapus
            self.hapus_kategori_button.config(state="normal")
    
    def simpan_kategori(self):
        """Menyimpan data kategori (tambah/update)"""
        # Validasi input
        nama = self.kategori_nama_entry.get().strip()
        
        if not nama:
            messagebox.showerror("Error", "Nama kategori harus diisi!")
            self.kategori_nama_entry.focus()
            return
            
        # Cek apakah kategori dengan nama yang sama sudah ada
        kategori_list = self.db.get_all_kategori()
        for kategori in kategori_list:
            if kategori["nama"].lower() == nama.lower() and kategori["id"] != self.kategori_id:
                messagebox.showerror("Error", f"Kategori dengan nama '{nama}' sudah ada!")
                self.kategori_nama_entry.focus()
                self.kategori_nama_entry.select_range(0, tk.END)
                return
        
        # Konfirmasi sebelum menyimpan
        aksi = "memperbarui" if self.kategori_id else "menambahkan"
        if not messagebox.askyesno("Konfirmasi", f"Apakah Anda yakin ingin {aksi} kategori '{nama}'?"):
            return
        
        # Simpan ke database
        if self.kategori_id:  # Update
            if self.db.update_kategori(self.kategori_id, nama):
                messagebox.showinfo("Sukses", "Kategori berhasil diperbarui!")
                self.batal_kategori()  # Reset form
                self.load_kategori()  # Refresh tabel kategori
                self.load_produk()  # Refresh tabel produk juga
            else:
                messagebox.showerror("Error", "Gagal memperbarui kategori!")
        else:  # Tambah baru
            if self.db.add_kategori(nama):
                messagebox.showinfo("Sukses", "Kategori berhasil ditambahkan!")
                self.batal_kategori()  # Reset form
                self.load_kategori()  # Refresh tabel
                # Refresh produk tab juga untuk update combobox
                self.load_kategori_combobox()
            else:
                messagebox.showerror("Error", "Gagal menambahkan kategori!")
                
        # Fokus kembali ke field nama untuk entry berikutnya
        self.kategori_nama_entry.focus()
    
    def hapus_kategori(self):
        """Menghapus kategori"""
        if not self.kategori_id:
            messagebox.showwarning("Peringatan", "Tidak ada kategori yang dipilih untuk dihapus!")
            return
        
        # Dapatkan detail kategori untuk konfirmasi
        kategori_list = self.db.get_all_kategori()
        kategori = None
        for k in kategori_list:
            if k["id"] == self.kategori_id:
                kategori = k
                break
                
        if not kategori:
            messagebox.showerror("Error", "Kategori tidak ditemukan di database!")
            self.batal_kategori()
            return
        
        # Cek apakah kategori masih digunakan oleh produk
        produk = self.db.get_all_produk()
        produk_dengan_kategori = [p for p in produk if p["kategori_id"] == self.kategori_id]
        
        pesan_konfirmasi = f"Apakah Anda yakin ingin menghapus kategori '{kategori['nama']}'?"
        
        if produk_dengan_kategori:
            nama_produk = [p["nama"] for p in produk_dengan_kategori[:3]]
            pesan_tambahan = "\n\nKategori ini digunakan oleh produk berikut:\n- " + "\n- ".join(nama_produk)
            
            if len(produk_dengan_kategori) > 3:
                pesan_tambahan += f"\n- dan {len(produk_dengan_kategori) - 3} produk lainnya"
                
            pesan_tambahan += "\n\nJika dihapus, produk tersebut tidak akan memiliki kategori."
            pesan_konfirmasi += pesan_tambahan
            
            if not messagebox.askyesno("Peringatan", pesan_konfirmasi):
                return
        else:
            if not messagebox.askyesno("Konfirmasi", pesan_konfirmasi):
                return
        
        try:
            if self.db.delete_kategori(self.kategori_id):
                messagebox.showinfo("Sukses", f"Kategori '{kategori['nama']}' berhasil dihapus!")
                self.batal_kategori()  # Reset form
                self.load_kategori()  # Refresh tabel kategori
                self.load_produk()  # Refresh tabel produk juga
            else:
                messagebox.showerror("Error", "Gagal menghapus kategori!")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan saat menghapus kategori: {str(e)}")
        
        # Fokus kembali ke tabel kategori
        self.kategori_tree.focus_set()
    
    def batal_kategori(self):
        """Reset form kategori"""
        # Cek apakah ada perubahan yang belum disimpan
        if self.kategori_nama_entry.get().strip():
            if not messagebox.askyesno("Konfirmasi", "Ada perubahan yang belum disimpan. Yakin ingin membatalkan?"):
                return
        
        # Reset form
        self.kategori_id = None
        self.kategori_nama_entry.delete(0, tk.END)
        self.hapus_kategori_button.config(state="disabled")
        
        # Fokus kembali ke field nama
        self.kategori_nama_entry.focus()

# Untuk testing modul secara independen
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Test Produk & Kategori View")
    root.geometry("1000x700")
    
    class TestController:
        def __init__(self):
            self.current_user = {"username": "admin", "role": "Admin"}
        
        def show_frame(self, frame_name):
            print(f"Showing frame: {frame_name}")
    
    controller = TestController()
    produk_kategori_view = ProdukKategoriView(root, controller)
    produk_kategori_view.pack(fill="both", expand=True)
    
    root.mainloop()