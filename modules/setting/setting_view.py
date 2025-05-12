import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sys
import os
import json

# Menambahkan path root ke sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from database.database import Database

class SettingView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.db = Database()
        
        # Default settings
        self.settings = {
            "toko": {
                "nama": "POS & Inventory Management",
                "alamat": "Jl. Contoh No. 123, Kota",
                "telepon": "08123456789",
                "email": "info@posinventory.com"
            },
            "struk": {
                "tampilkan_logo": True,
                "tampilkan_footer": True,
                "pesan_footer": "Terima kasih telah berbelanja",
                "pesan_tambahan": "Barang yang sudah dibeli tidak dapat dikembalikan"
            },
            "aplikasi": {
                "tema": "default",
                "ukuran_font": 10
            }
        }
        
        # Load settings jika ada
        self.load_settings()
        
        # Frame utama dengan padding
        main_frame = tk.Frame(self, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Header
        header_frame = tk.Frame(main_frame)
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Judul
        title_label = tk.Label(header_frame, text="Pengaturan Aplikasi", font=("Arial", 18, "bold"))
        title_label.pack(side="left")
        
        # Tombol kembali ke dashboard
        back_button = tk.Button(header_frame, text="Kembali ke Dashboard", 
                              command=lambda: controller.show_frame("DashboardView"))
        back_button.pack(side="right")
        
        # Notebook untuk tab pengaturan
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill="both", expand=True)
        
        # Tab Informasi Toko
        toko_frame = tk.Frame(self.notebook)
        self.notebook.add(toko_frame, text="Informasi Toko")
        
        # Form informasi toko
        toko_form = tk.Frame(toko_frame, padx=20, pady=20)
        toko_form.pack(fill="both", expand=True)
        
        # Nama Toko
        tk.Label(toko_form, text="Nama Toko:").grid(row=0, column=0, sticky="w", pady=5)
        self.nama_toko_entry = tk.Entry(toko_form, width=40)
        self.nama_toko_entry.grid(row=0, column=1, sticky="w", pady=5, padx=5)
        self.nama_toko_entry.insert(0, self.settings["toko"]["nama"])
        
        # Alamat
        tk.Label(toko_form, text="Alamat:").grid(row=1, column=0, sticky="w", pady=5)
        self.alamat_entry = tk.Entry(toko_form, width=40)
        self.alamat_entry.grid(row=1, column=1, sticky="w", pady=5, padx=5)
        self.alamat_entry.insert(0, self.settings["toko"]["alamat"])
        
        # Telepon
        tk.Label(toko_form, text="Telepon:").grid(row=2, column=0, sticky="w", pady=5)
        self.telepon_entry = tk.Entry(toko_form, width=40)
        self.telepon_entry.grid(row=2, column=1, sticky="w", pady=5, padx=5)
        self.telepon_entry.insert(0, self.settings["toko"]["telepon"])
        
        # Email
        tk.Label(toko_form, text="Email:").grid(row=3, column=0, sticky="w", pady=5)
        self.email_entry = tk.Entry(toko_form, width=40)
        self.email_entry.grid(row=3, column=1, sticky="w", pady=5, padx=5)
        self.email_entry.insert(0, self.settings["toko"]["email"])
        
        # Tab Pengaturan Struk
        struk_frame = tk.Frame(self.notebook)
        self.notebook.add(struk_frame, text="Pengaturan Struk")
        
        # Form pengaturan struk
        struk_form = tk.Frame(struk_frame, padx=20, pady=20)
        struk_form.pack(fill="both", expand=True)
        
        # Tampilkan Logo
        self.tampilkan_logo_var = tk.BooleanVar(value=self.settings["struk"]["tampilkan_logo"])
        tampilkan_logo_check = tk.Checkbutton(struk_form, text="Tampilkan Logo", variable=self.tampilkan_logo_var)
        tampilkan_logo_check.grid(row=0, column=0, sticky="w", pady=5, columnspan=2)
        
        # Tampilkan Footer
        self.tampilkan_footer_var = tk.BooleanVar(value=self.settings["struk"]["tampilkan_footer"])
        tampilkan_footer_check = tk.Checkbutton(struk_form, text="Tampilkan Footer", variable=self.tampilkan_footer_var)
        tampilkan_footer_check.grid(row=1, column=0, sticky="w", pady=5, columnspan=2)
        
        # Pesan Footer
        tk.Label(struk_form, text="Pesan Footer:").grid(row=2, column=0, sticky="w", pady=5)
        self.pesan_footer_entry = tk.Entry(struk_form, width=40)
        self.pesan_footer_entry.grid(row=2, column=1, sticky="w", pady=5, padx=5)
        self.pesan_footer_entry.insert(0, self.settings["struk"]["pesan_footer"])
        
        # Pesan Tambahan
        tk.Label(struk_form, text="Pesan Tambahan:").grid(row=3, column=0, sticky="w", pady=5)
        self.pesan_tambahan_entry = tk.Entry(struk_form, width=40)
        self.pesan_tambahan_entry.grid(row=3, column=1, sticky="w", pady=5, padx=5)
        self.pesan_tambahan_entry.insert(0, self.settings["struk"]["pesan_tambahan"])
        
        # Tab Pengaturan Aplikasi
        aplikasi_frame = tk.Frame(self.notebook)
        self.notebook.add(aplikasi_frame, text="Pengaturan Aplikasi")
        
        # Form pengaturan aplikasi
        aplikasi_form = tk.Frame(aplikasi_frame, padx=20, pady=20)
        aplikasi_form.pack(fill="both", expand=True)
        
        # Tema
        tk.Label(aplikasi_form, text="Tema:").grid(row=0, column=0, sticky="w", pady=5)
        self.tema_combobox = ttk.Combobox(aplikasi_form, width=20, state="readonly")
        self.tema_combobox["values"] = ["default", "light", "dark"]
        self.tema_combobox.current(0 if self.settings["aplikasi"]["tema"] == "default" else 
                                 1 if self.settings["aplikasi"]["tema"] == "light" else 2)
        self.tema_combobox.grid(row=0, column=1, sticky="w", pady=5, padx=5)
        
        # Ukuran Font
        tk.Label(aplikasi_form, text="Ukuran Font:").grid(row=1, column=0, sticky="w", pady=5)
        self.ukuran_font_var = tk.IntVar(value=self.settings["aplikasi"]["ukuran_font"])
        ukuran_font_scale = tk.Scale(aplikasi_form, from_=8, to=14, orient=tk.HORIZONTAL, 
                                    variable=self.ukuran_font_var, length=200)
        ukuran_font_scale.grid(row=1, column=1, sticky="w", pady=5, padx=5)
        
        # Tombol simpan
        save_button = tk.Button(main_frame, text="Simpan Pengaturan", 
                              command=self.simpan_pengaturan, 
                              bg="#4CAF50", fg="white")
        save_button.pack(pady=10)
    
    def load_settings(self):
        """Memuat pengaturan dari file"""
        settings_path = os.path.join(os.path.dirname(__file__), '..', '..', 'settings.json')
        if os.path.exists(settings_path):
            try:
                with open(settings_path, 'r') as f:
                    loaded_settings = json.load(f)
                    # Update settings dengan yang dimuat
                    for category in loaded_settings:
                        if category in self.settings:
                            for key in loaded_settings[category]:
                                if key in self.settings[category]:
                                    self.settings[category][key] = loaded_settings[category][key]
            except Exception as e:
                print(f"Error loading settings: {e}")
    
    def simpan_pengaturan(self):
        """Menyimpan pengaturan ke file"""
        # Update settings dari form
        # Toko
        self.settings["toko"]["nama"] = self.nama_toko_entry.get()
        self.settings["toko"]["alamat"] = self.alamat_entry.get()
        self.settings["toko"]["telepon"] = self.telepon_entry.get()
        self.settings["toko"]["email"] = self.email_entry.get()
        
        # Struk
        self.settings["struk"]["tampilkan_logo"] = self.tampilkan_logo_var.get()
        self.settings["struk"]["tampilkan_footer"] = self.tampilkan_footer_var.get()
        self.settings["struk"]["pesan_footer"] = self.pesan_footer_entry.get()
        self.settings["struk"]["pesan_tambahan"] = self.pesan_tambahan_entry.get()
        
        # Aplikasi
        self.settings["aplikasi"]["tema"] = self.tema_combobox.get()
        self.settings["aplikasi"]["ukuran_font"] = self.ukuran_font_var.get()
        
        # Simpan ke file
        settings_path = os.path.join(os.path.dirname(__file__), '..', '..', 'settings.json')
        try:
            with open(settings_path, 'w') as f:
                json.dump(self.settings, f, indent=4)
            messagebox.showinfo("Sukses", "Pengaturan berhasil disimpan!")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan pengaturan: {str(e)}")

# Untuk testing modul secara independen
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Test Setting View")
    root.geometry("800x500")
    
    class TestController:
        def __init__(self):
            self.current_user = {"id": 1, "username": "admin", "role": "Admin"}
        
        def show_frame(self, frame_name):
            print(f"Showing frame: {frame_name}")
    
    controller = TestController()
    setting_view = SettingView(root, controller)
    setting_view.pack(fill="both", expand=True)
    
    root.mainloop()