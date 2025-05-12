import os
import sys
import tempfile
import webbrowser
from datetime import datetime

# Menambahkan path root ke sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from modules.struk.struk_generator import StrukGenerator
from database.database import Database

class StrukPrinter:
    def __init__(self):
        self.db = Database()
        self.struk_generator = StrukGenerator()
    
    def print_to_thermal_printer(self, transaksi_id):
        """Mencetak struk ke printer termal (simulasi)"""
        # Dalam implementasi nyata, ini akan mengirim ke printer termal
        # Untuk simulasi, kita hanya menampilkan preview HTML
        struk_text = self.struk_generator.generate_struk_text(transaksi_id)
        return self.preview_struk_html(struk_text, transaksi_id)
    
    def preview_struk_html(self, struk_text, transaksi_id):
        """Membuat preview struk dalam format HTML"""
        # Dapatkan data transaksi untuk header
        transaksi = self.db.get_transaksi(transaksi_id)
        if not transaksi:
            return False, "Transaksi tidak ditemukan"
        
        # Buat HTML untuk struk
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Struk #{transaksi_id}</title>
            <style>
                body {{ font-family: 'Courier New', monospace; font-size: 12px; width: 300px; margin: 0 auto; padding: 10px; }}
                .header {{ text-align: center; margin-bottom: 10px; }}
                .divider {{ border-top: 1px dashed #000; margin: 5px 0; }}
                .item {{ display: flex; justify-content: space-between; margin: 3px 0; }}
                .total {{ font-weight: bold; margin-top: 5px; text-align: right; }}
                .footer {{ text-align: center; margin-top: 10px; font-size: 10px; }}
                @media print {{
                    body {{ width: 100%; }}
                    .no-print {{ display: none; }}
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>{self.struk_generator.settings['toko']['nama']}</h2>
                <p>{self.struk_generator.settings['toko']['alamat']}</p>
                <p>Telp: {self.struk_generator.settings['toko']['telepon']}</p>
            </div>
            <div class="divider"></div>
            <p>No. Transaksi: {transaksi_id}</p>
            <p>Tanggal: {transaksi['tanggal']}</p>
            <p>Kasir: {transaksi['username']}</p>
            <div class="divider"></div>
            <pre>{struk_text}</pre>
            <div class="divider"></div>
            <div class="footer">
                <p>{self.struk_generator.settings['struk']['pesan_footer']}</p>
                <p>{self.struk_generator.settings['struk']['pesan_tambahan']}</p>
            </div>
            <div class="no-print" style="margin-top: 20px; text-align: center;">
                <button onclick="window.print()">Cetak Struk</button>
                <button onclick="window.close()">Tutup</button>
            </div>
        </body>
        </html>
        """
        
        # Simpan ke file sementara dan buka di browser
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.html', mode='w', encoding='utf-8') as f:
                f.write(html_content)
                temp_path = f.name
            
            # Buka file di browser default
            webbrowser.open('file://' + temp_path)
            return True, "Struk berhasil dibuka di browser"
        except Exception as e:
            return False, f"Error: {str(e)}"

# Untuk testing modul secara independen
if __name__ == "__main__":
    printer = StrukPrinter()
    # Test print struk
    success, message = printer.print_to_thermal_printer(1)  # Ganti dengan ID transaksi yang valid
    print(message)