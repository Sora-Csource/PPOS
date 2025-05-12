import os
import sys
import pandas as pd
from tkinter import filedialog, messagebox
from datetime import datetime

# Menambahkan path root ke sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from database.database import Database

class ExcelExporter:
    def __init__(self):
        self.db = Database()
    
    def export_transaksi(self, transaksi_list, filename=None):
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
    
    def export_produk(self, filename=None):
        """Mengekspor daftar produk ke file Excel"""
        try:
            # Ambil data produk dari database
            produk_list = self.db.get_all_produk()
            
            # Siapkan data untuk ekspor
            export_data = []
            for produk in produk_list:
                export_data.append({
                    "ID": produk["id"],
                    "Nama Produk": produk["nama"],
                    "Kategori": produk.get("kategori_nama", "-"),
                    "Harga": produk["harga"],
                    "Stok": produk["stok"]
                })
            
            # Buat DataFrame
            df = pd.DataFrame(export_data)
            
            # Jika filename tidak disediakan, minta user untuk memilih lokasi penyimpanan
            if not filename:
                filename = filedialog.asksaveasfilename(
                    defaultextension=".xlsx",
                    filetypes=[("Excel files", "*.xlsx")],
                    title="Simpan Daftar Produk Sebagai"
                )
            
            if filename:
                # Simpan ke Excel
                df.to_excel(filename, index=False, engine="openpyxl")
                return True, "Daftar produk berhasil diekspor ke Excel!"
            else:
                return False, "Ekspor dibatalkan."
        
        except Exception as e:
            print(f"Error exporting to Excel: {e}")
            return False, f"Error: {str(e)}"
    
    def export_laporan_penjualan(self, start_date, end_date, filename=None):
        """Mengekspor laporan penjualan dalam rentang tanggal ke file Excel"""
        try:
            # Ambil data laporan penjualan dari database
            laporan = self.db.get_laporan_penjualan(start_date, end_date)
            
            # Siapkan data untuk ekspor
            export_data = []
            for item in laporan:
                export_data.append({
                    "ID Produk": item["id"],
                    "Nama Produk": item["nama"],
                    "Jumlah Terjual": item["total_qty"],
                    "Total Penjualan": item["total_penjualan"]
                })
            
            # Buat DataFrame
            df = pd.DataFrame(export_data)
            
            # Jika filename tidak disediakan, minta user untuk memilih lokasi penyimpanan
            if not filename:
                filename = filedialog.asksaveasfilename(
                    defaultextension=".xlsx",
                    filetypes=[("Excel files", "*.xlsx")],
                    title="Simpan Laporan Penjualan Sebagai"
                )
            
            if filename:
                # Simpan ke Excel
                df.to_excel(filename, index=False, engine="openpyxl")
                return True, "Laporan penjualan berhasil diekspor ke Excel!"
            else:
                return False, "Ekspor dibatalkan."
        
        except Exception as e:
            print(f"Error exporting to Excel: {e}")
            return False, f"Error: {str(e)}"

# Untuk testing modul secara independen
if __name__ == "__main__":
    exporter = ExcelExporter()
    # Test export produk
    success, message = exporter.export_produk()
    print(message)