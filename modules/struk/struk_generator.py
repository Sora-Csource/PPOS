import os
import json
import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime
import pandas as pd
import sys

# Menambahkan path root ke sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from database.database import Database

class StrukGenerator:
    def __init__(self):
        self.db = Database()
        self.settings = self.load_settings()
    
    def load_settings(self):
        """Memuat pengaturan dari file settings.json"""
        settings_path = os.path.join(os.path.dirname(__file__), '..', '..', 'settings.json')
        default_settings = {
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
            }
        }
        
        if os.path.exists(settings_path):
            try:
                with open(settings_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading settings: {e}")
                return default_settings
        else:
            return default_settings
    
    def generate_struk_text(self, transaksi_id):
        """Menghasilkan teks struk untuk transaksi tertentu"""
        try:
            # Ambil data transaksi
            transaksi = self.db.get_transaksi(transaksi_id)
            if not transaksi:
                return "Error: Transaksi tidak ditemukan"
            
            # Ambil detail transaksi
            detail_transaksi = self.db.get_detail_transaksi(transaksi_id)
            if not detail_transaksi:
                return "Error: Detail transaksi tidak ditemukan"
            
            # Ambil data kasir
            kasir = self.db.get_user_by_id(transaksi["user_id"])
            kasir_name = kasir["username"] if kasir else "Unknown"
            
            # Format tanggal
            tanggal_obj = datetime.strptime(transaksi["tanggal"], "%Y-%m-%d %H:%M:%S")
            tanggal_str = tanggal_obj.strftime("%d-%m-%Y %H:%M:%S")
            
            # Buat teks struk
            struk_text = []
            
            # Header struk
            if self.settings["struk"]["tampilkan_logo"]:
                struk_text.append("="*40)
                struk_text.append(f"{self.settings['toko']['nama']:^40}")
                struk_text.append(f"{self.settings['toko']['alamat']:^40}")
                struk_text.append(f"Telp: {self.settings['toko']['telepon']:^30}")
                struk_text.append("="*40)
            
            # Info transaksi
            struk_text.append(f"No. Transaksi: {transaksi_id}")
            struk_text.append(f"Tanggal: {tanggal_str}")
            struk_text.append(f"Kasir: {kasir_name}")
            struk_text.append("-"*40)
            
            # Detail item
            struk_text.append(f"{'Produk':<20}{'Qty':^5}{'Harga':^10}{'Subtotal':>10}")
            struk_text.append("-"*40)
            
            for item in detail_transaksi:
                produk = self.db.get_produk(item["produk_id"])
                if produk:
                    nama_produk = produk["nama"]
                    if len(nama_produk) > 18:
                        nama_produk = nama_produk[:15] + "..."
                    
                    struk_text.append(
                        f"{nama_produk:<20}{item['qty']:^5}Rp {item['harga']:,.0f}{' ':>1}Rp {item['qty'] * item['harga']:,.0f}"
                    )
            
            # Total
            struk_text.append("-"*40)
            struk_text.append(f"{'TOTAL':<30}Rp {transaksi['total']:,.0f}")
            
            # Footer
            if self.settings["struk"]["tampilkan_footer"]:
                struk_text.append("="*40)
                struk_text.append(f"{self.settings['struk']['pesan_footer']:^40}")
                if self.settings["struk"]["pesan_tambahan"]:
                    struk_text.append(f"{self.settings['struk']['pesan_tambahan']:^40}")
            
            return "\n".join(struk_text)
        
        except Exception as e:
            print(f"Error generating struk: {e}")
            return f"Error: {str(e)}"
    
    def print_struk(self, transaksi_id):
        """Mencetak struk ke printer atau file"""
        struk_text = self.generate_struk_text(transaksi_id)
        
        # Buat window untuk preview struk
        preview_window = tk.Toplevel()
        preview_window.title("Preview Struk")
        preview_window.geometry("400x500")
        
        # Text widget untuk menampilkan struk
        text_widget = tk.Text(preview_window, font=("Courier New", 10))
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        text_widget.insert("1.0", struk_text)
        text_widget.config(state="disabled")
        
        # Frame untuk tombol
        button_frame = tk.Frame(preview_window)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        # Tombol cetak
        def print_to_file():
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt")],
                title="Simpan Struk Sebagai"
            )
            if file_path:
                try:
                    with open(file_path, "w") as f:
                        f.write(struk_text)
                    messagebox.showinfo("Sukses", "Struk berhasil disimpan!")
                except Exception as e:
                    messagebox.showerror("Error", f"Gagal menyimpan struk: {str(e)}")
        
        print_button = tk.Button(button_frame, text="Simpan ke File", command=print_to_file)
        print_button.pack(side="left", padx=5)
        
        # Tombol tutup
        close_button = tk.Button(button_frame, text="Tutup", command=preview_window.destroy)
        close_button.pack(side="right", padx=5)
        
        return preview_window
    
    def export_to_excel(self, transaksi_list, filename=None):
        """Mengekspor daftar transaksi ke file Excel"""
        try:
            # Siapkan data untuk ekspor
            export_data = []
            
            for transaksi in transaksi_list:
                # Ambil detail transaksi
                detail_transaksi = self.db.get_detail_transaksi(transaksi["id"])
                
                # Ambil data kasir
                kasir = self.db.get_user_by_id(transaksi["user_id"])
                kasir_name = kasir["username"] if kasir else "Unknown"
                
                # Format tanggal
                tanggal_obj = datetime.strptime(transaksi["tanggal"], "%Y-%m-%d %H:%M:%S")
                tanggal_str = tanggal_obj.strftime("%d-%m-%Y %H:%M:%S")
                
                # Tambahkan data transaksi ke list
                for item in detail_transaksi:
                    produk = self.db.get_produk(item["produk_id"])
                    if produk:
                        export_data.append({
                            "No. Transaksi": transaksi["id"],
                            "Tanggal": tanggal_str,
                            "Kasir": kasir_name,
                            "Produk": produk["nama"],
                            "Kategori": produk.get("kategori_nama", "-"),
                            "Qty": item["qty"],
                            "Harga Satuan": item["harga"],
                            "Subtotal": item["qty"] * item["harga"],
                            "Total Transaksi": transaksi["total"]
                        })
            
            # Buat DataFrame
            df = pd.DataFrame(export_data)
            
            # Jika filename tidak disediakan, minta user untuk memilih lokasi penyimpanan
            if not filename:
                filename = filedialog.asksaveasfilename(
                    defaultextension=".xlsx",
                    filetypes=[("Excel files", "*.xlsx")],
                    title="Simpan Laporan Sebagai"
                )
            
            if filename:
                # Simpan ke Excel
                df.to_excel(filename, index=False, engine="openpyxl")
                return True, "Laporan berhasil diekspor ke Excel!"
            else:
                return False, "Ekspor dibatalkan."
        
        except Exception as e:
            print(f"Error exporting to Excel: {e}")
            return False, f"Error: {str(e)}"

# Untuk testing modul secara independen
if __name__ == "__main__":
    struk_gen = StrukGenerator()
    # Test generate struk
    print(struk_gen.generate_struk_text(1))  # Ganti dengan ID transaksi yang valid