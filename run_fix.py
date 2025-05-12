import os
import sys
import tkinter as tk
from tkinter import messagebox

# Import skrip perbaikan kredensial
from fix_credentials import fix_credentials

# Import aplikasi utama
from main import POSApp

def main():
    # Tampilkan jendela informasi
    root = tk.Tk()
    root.withdraw()  # Sembunyikan jendela utama
    
    # Jalankan perbaikan kredensial
    result = fix_credentials()
    
    if result:
        messagebox.showinfo("Sukses", "Kredensial default berhasil diperbaiki!\n\nSilakan login dengan:\n- Username: admin, Password: admin123\n- Username: kasir, Password: kasir123")
    else:
        messagebox.showerror("Error", "Gagal memperbaiki kredensial default. Silakan coba lagi.")
    
    # Tutup jendela informasi
    root.destroy()
    
    # Jalankan aplikasi utama
    app = POSApp()
    app.mainloop()

if __name__ == "__main__":
    main()