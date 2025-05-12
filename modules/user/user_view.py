import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
import re
from datetime import datetime

# Menambahkan path root ke sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from database.database import Database

class UserView(tk.Frame):
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
        title_label = tk.Label(header_frame, text="Kelola User", font=("Arial", 18, "bold"))
        title_label.pack(side="left")
        
        # Informasi peran user
        if hasattr(controller, 'current_user') and controller.current_user:
            role_info = tk.Label(header_frame, text=f"Login sebagai: {controller.current_user['username']} ({controller.current_user['role']})", 
                               font=("Arial", 10), fg="#555555")
            role_info.pack(side="left", padx=20)
        
        # Tombol kembali ke dashboard
        back_button = tk.Button(header_frame, text="Kembali ke Dashboard", 
                              command=lambda: controller.show_frame("DashboardView"))
        back_button.pack(side="right")
        
        # Frame untuk form dan tabel
        content_frame = tk.Frame(main_frame)
        content_frame.pack(fill="both", expand=True)
        
        # Frame untuk form input user
        form_frame = tk.LabelFrame(content_frame, text="Form User", padx=10, pady=10)
        form_frame.pack(side="left", fill="y", padx=(0, 10))
        
        # Form fields
        # ID User (hidden)
        self.user_id = None
        
        # Username
        username_label = tk.Label(form_frame, text="Username:")
        username_label.grid(row=0, column=0, sticky="w", pady=5)
        self.username_entry = tk.Entry(form_frame, width=30)
        self.username_entry.grid(row=0, column=1, pady=5, padx=5)
        
        # Username hint
        username_hint = tk.Label(form_frame, text="Min. 4 karakter, tanpa spasi", fg="gray", font=("Arial", 8))
        username_hint.grid(row=0, column=2, sticky="w", padx=5)
        
        # Password
        password_label = tk.Label(form_frame, text="Password:")
        password_label.grid(row=1, column=0, sticky="w", pady=5)
        self.password_entry = tk.Entry(form_frame, width=30, show="*")
        self.password_entry.grid(row=1, column=1, pady=5, padx=5)
        
        # Password hint
        password_hint = tk.Label(form_frame, text="Min. 6 karakter", fg="gray", font=("Arial", 8))
        password_hint.grid(row=1, column=2, sticky="w", padx=5)
        
        # Show/hide password
        self.show_password_var = tk.BooleanVar(value=False)
        show_password_check = tk.Checkbutton(form_frame, text="Tampilkan password", 
                                           variable=self.show_password_var, 
                                           command=self.toggle_password_visibility)
        show_password_check.grid(row=2, column=1, sticky="w")
        
        # Role
        role_label = tk.Label(form_frame, text="Role:")
        role_label.grid(row=3, column=0, sticky="w", pady=5)
        self.role_combobox = ttk.Combobox(form_frame, width=27, state="readonly")
        self.role_combobox["values"] = ["Admin", "Kasir"]
        self.role_combobox.current(1)  # Default: Kasir
        self.role_combobox.grid(row=3, column=1, pady=5, padx=5)
        
        # Role description
        self.role_desc_label = tk.Label(form_frame, text="Kasir: Hanya dapat melakukan transaksi", fg="#555555", font=("Arial", 8))
        self.role_desc_label.grid(row=3, column=2, sticky="w", padx=5)
        
        # Bind event saat role berubah
        self.role_combobox.bind("<<ComboboxSelected>>", self.on_role_changed)
        
        # Tombol-tombol aksi
        button_frame = tk.Frame(form_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=10)
        
        self.simpan_button = tk.Button(button_frame, text="Simpan", command=self.simpan_user, width=10, 
                                     bg="#4CAF50", fg="white")
        self.simpan_button.grid(row=0, column=0, padx=5)
        
        self.batal_button = tk.Button(button_frame, text="Batal", command=self.batal, width=10)
        self.batal_button.grid(row=0, column=1, padx=5)
        
        self.hapus_button = tk.Button(button_frame, text="Hapus", command=self.hapus_user, width=10, 
                                    state="disabled", bg="#f44336", fg="white")
        self.hapus_button.grid(row=0, column=2, padx=5)
        
        self.reset_password_button = tk.Button(button_frame, text="Reset Password", command=self.reset_password, 
                                            width=15, state="disabled", bg="#2196F3", fg="white")
        self.reset_password_button.grid(row=0, column=3, padx=5)
        
        # Frame untuk tabel user
        table_frame = tk.LabelFrame(content_frame, text="Daftar User", padx=10, pady=10)
        table_frame.pack(side="right", fill="both", expand=True)
        
        # Search frame
        search_frame = tk.Frame(table_frame)
        search_frame.pack(fill="x", pady=(0, 10))
        
        search_label = tk.Label(search_frame, text="Cari:")
        search_label.pack(side="left")
        
        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<KeyRelease>", self.search_user)
        
        # Status label untuk hasil pencarian
        self.status_label = tk.Label(table_frame, text="Menampilkan semua user", anchor="w")
        self.status_label.pack(fill="x", pady=(0, 5))
        
        # Tabel user
        self.tree = ttk.Treeview(table_frame, columns=("id", "username", "role", "last_login"), show="headings")
        self.tree.pack(fill="both", expand=True)
        
        # Scrollbar untuk tabel
        scrollbar = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        
        # Definisi kolom
        self.tree.heading("id", text="ID")
        self.tree.heading("username", text="Username")
        self.tree.heading("role", text="Role")
        self.tree.heading("last_login", text="Login Terakhir")
        
        # Lebar kolom
        self.tree.column("id", width=50)
        self.tree.column("username", width=150)
        self.tree.column("role", width=100)
        self.tree.column("last_login", width=150)
        
        # Konfigurasi tag untuk warna baris
        self.tree.tag_configure("admin", background="#ffedcc")
        self.tree.tag_configure("kasir", background="#e6f3ff")
        self.tree.tag_configure("evenrow", background="#f0f0f0")
        self.tree.tag_configure("oddrow", background="white")
        
        # Bind event klik pada tabel
        self.tree.bind("<Double-1>", self.on_item_selected)
        
        # Load data awal
        self.load_user()
    
    def toggle_password_visibility(self):
        """Menampilkan atau menyembunyikan password"""
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")
    
    def on_role_changed(self, event=None):
        """Handler saat role berubah"""
        selected_role = self.role_combobox.get()
        if selected_role == "Admin":
            self.role_desc_label.config(text="Admin: Akses penuh ke semua fitur")
        else:
            self.role_desc_label.config(text="Kasir: Hanya dapat melakukan transaksi")
    
    def load_user(self):
        """Memuat daftar user ke tabel"""
        # Hapus data lama
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Ambil data user dari database
        users = self.db.get_all_users()
        
        # Masukkan ke tabel dengan warna baris bergantian
        for i, user in enumerate(users):
            # Tampilkan data login terakhir dari database
            last_login = "Belum pernah login"
            if user.get("last_login"):
                last_login = user["last_login"]
            
            item_id = self.tree.insert("", "end", values=(user["id"], user["username"], user["role"], last_login))
            
            # Beri warna baris berdasarkan role dan posisi baris
            if user["role"] == "Admin":
                self.tree.item(item_id, tags=("admin",))
            elif i % 2 == 0:
                self.tree.item(item_id, tags=("evenrow",))
            else:
                self.tree.item(item_id, tags=("oddrow",))
        
        # Update status label
        if users:
            self.status_label.config(text=f"Menampilkan {len(users)} user")
        else:
            self.status_label.config(text="Tidak ada user yang tersedia")
    
    def search_user(self, event=None):
        """Mencari user berdasarkan username atau role"""
        search_text = self.search_entry.get().lower().strip()
        
        # Hapus data lama
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Ambil data user dari database
        users = self.db.get_all_users()
        
        # Filter dan masukkan ke tabel dengan warna baris bergantian
        found_items = 0
        filtered_users = []
        
        # Filter user berdasarkan kata kunci
        for user in users:
            if (search_text in user["username"].lower() or 
                search_text in user["role"].lower()):
                filtered_users.append(user)
        
        # Masukkan ke tabel dengan warna baris bergantian
        for i, user in enumerate(filtered_users):
            # Tampilkan data login terakhir dari database
            last_login = "Belum pernah login"
            if user.get("last_login"):
                last_login = user["last_login"]
            
            item_id = self.tree.insert("", "end", values=(user["id"], user["username"], user["role"], last_login))
            
            # Beri warna baris berdasarkan role
            if user["role"] == "Admin":
                self.tree.item(item_id, tags=("admin",))
            elif i % 2 == 0:
                self.tree.item(item_id, tags=("evenrow",))
            else:
                self.tree.item(item_id, tags=("oddrow",))
                
            found_items += 1
        
        # Update status pencarian
        if search_text:
            if found_items == 0:
                self.status_label.config(text=f"Tidak ditemukan user dengan kata kunci '{search_text}'")
            elif found_items == 1:
                self.status_label.config(text=f"Ditemukan 1 user dengan kata kunci '{search_text}'")
            else:
                self.status_label.config(text=f"Ditemukan {found_items} user dengan kata kunci '{search_text}'")
        else:
            self.status_label.config(text=f"Menampilkan {len(users)} user")
    
    def on_item_selected(self, event):
        """Handler ketika item di tabel dipilih"""
        selected_item = self.tree.focus()
        if selected_item:  # Pastikan ada item yang dipilih
            item_data = self.tree.item(selected_item)
            values = item_data["values"]
            
            # Isi form dengan data user
            self.user_id = values[0]
            self.username_entry.delete(0, tk.END)
            self.username_entry.insert(0, values[1])
            
            # Kosongkan password (tidak menampilkan password lama)
            self.password_entry.delete(0, tk.END)
            
            # Set role
            if values[2] == "Admin":
                self.role_combobox.current(0)
            else:
                self.role_combobox.current(1)
            
            # Aktifkan tombol hapus dan reset password
            self.hapus_button.config(state="normal")
            self.reset_password_button.config(state="normal")
            
            # Cek apakah user yang dipilih adalah user yang sedang login
            if hasattr(self.controller, 'current_user') and self.controller.current_user:
                if self.controller.current_user["id"] == self.user_id:
                    # Disable tombol hapus jika user yang dipilih adalah user yang sedang login
                    self.hapus_button.config(state="disabled")
    
    def simpan_user(self):
        """Menyimpan data user (tambah/update)"""
        # Validasi input
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        role = self.role_combobox.get()
        
        # Validasi username
        if not username:
            messagebox.showerror("Error", "Username harus diisi!")
            self.username_entry.focus()
            return
        
        if len(username) < 4:
            messagebox.showerror("Error", "Username minimal 4 karakter!")
            self.username_entry.focus()
            return
            
        if " " in username:
            messagebox.showerror("Error", "Username tidak boleh mengandung spasi!")
            self.username_entry.focus()
            return
            
        # Validasi username hanya boleh mengandung huruf, angka, dan underscore
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            messagebox.showerror("Error", "Username hanya boleh mengandung huruf, angka, dan underscore!")
            self.username_entry.focus()
            return
        
        # Jika mode update dan password kosong, gunakan password lama
        if self.user_id and not password:
            # Cek apakah user yang sedang diedit adalah user yang sedang login
            if hasattr(self.controller, 'current_user') and self.controller.current_user:
                if self.controller.current_user["id"] == self.user_id:
                    # Jika user yang diedit adalah user yang sedang login, password harus diisi
                    messagebox.showerror("Error", "Password harus diisi!")
                    self.password_entry.focus()
                    return
            
            # Ambil user dari database
            user = self.db.get_user(username)
            if user and user["id"] != self.user_id:
                messagebox.showerror("Error", "Username sudah digunakan!")
                return
            
            # Update user tanpa mengubah password
            if self.db.update_user(self.user_id, username, user["password"], role):
                messagebox.showinfo("Sukses", "User berhasil diperbarui!")
                self.batal()  # Reset form
                self.load_user()  # Refresh tabel
            else:
                messagebox.showerror("Error", "Gagal memperbarui user!")
        else:  # Mode tambah atau update dengan password baru
            if not password:
                messagebox.showerror("Error", "Password harus diisi!")
                self.password_entry.focus()
                return
                
            if len(password) < 6:
                messagebox.showerror("Error", "Password minimal 6 karakter!")
                self.password_entry.focus()
                return
                
            # Validasi password harus mengandung minimal 1 huruf dan 1 angka
            if not (re.search(r'[a-zA-Z]', password) and re.search(r'[0-9]', password)):
                messagebox.showerror("Error", "Password harus mengandung minimal 1 huruf dan 1 angka!")
                self.password_entry.focus()
                return
            
            if self.user_id:  # Update
                # Cek apakah username sudah digunakan oleh user lain
                user = self.db.get_user(username)
                if user and user["id"] != self.user_id:
                    messagebox.showerror("Error", "Username sudah digunakan!")
                    return
                
                if self.db.update_user(self.user_id, username, password, role):
                    messagebox.showinfo("Sukses", "User berhasil diperbarui!")
                    self.batal()  # Reset form
                    self.load_user()  # Refresh tabel
                else:
                    messagebox.showerror("Error", "Gagal memperbarui user!")
            else:  # Tambah baru
                # Cek apakah username sudah digunakan
                user = self.db.get_user(username)
                if user:
                    messagebox.showerror("Error", "Username sudah digunakan!")
                    return
                
                if self.db.add_user(username, password, role):
                    messagebox.showinfo("Sukses", "User berhasil ditambahkan!")
                    self.batal()  # Reset form
                    self.load_user()  # Refresh tabel
                else:
                    messagebox.showerror("Error", "Gagal menambahkan user!")
    
    def hapus_user(self):
        """Menghapus user"""
        if not self.user_id:
            return
        
        # Cek apakah user yang akan dihapus adalah user yang sedang login
        if hasattr(self.controller, 'current_user') and self.controller.current_user:
            if self.controller.current_user["id"] == self.user_id:
                messagebox.showerror("Error", "Anda tidak dapat menghapus user yang sedang login!")
                return
        
        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus user ini?"):
            if self.db.delete_user(self.user_id):
                messagebox.showinfo("Sukses", "User berhasil dihapus!")
                self.batal()  # Reset form
                self.load_user()  # Refresh tabel
            else:
                messagebox.showerror("Error", "Gagal menghapus user!")
    
    def batal(self):
        """Reset form"""
        self.user_id = None
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.role_combobox.current(1)  # Default: Kasir
        self.on_role_changed()  # Update deskripsi role
        self.hapus_button.config(state="disabled")
        self.reset_password_button.config(state="disabled")
        self.show_password_var.set(False)
        self.toggle_password_visibility()
        self.username_entry.focus()
        
    def reset_password(self):
        """Reset password user"""
        if not self.user_id:
            return
            
        # Cek apakah user yang akan direset password adalah user yang sedang login
        is_current_user = False
        if hasattr(self.controller, 'current_user') and self.controller.current_user:
            if self.controller.current_user["id"] == self.user_id:
                is_current_user = True
        
        # Konfirmasi reset password
        if not messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin mereset password user ini?"):
            return
            
        # Dialog untuk password baru
        reset_window = tk.Toplevel(self)
        reset_window.title("Reset Password")
        reset_window.geometry("400x250")
        reset_window.resizable(False, False)
        reset_window.transient(self)  # Membuat window modal
        reset_window.grab_set()  # Mengunci fokus ke window ini
        
        # Posisikan di tengah parent window
        x = self.winfo_rootx() + (self.winfo_width() // 2) - (400 // 2)
        y = self.winfo_rooty() + (self.winfo_height() // 2) - (200 // 2)
        reset_window.geometry(f"+{x}+{y}")
        
        # Frame utama dengan padding
        main_frame = tk.Frame(reset_window, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Label informasi
        info_label = tk.Label(main_frame, text=f"Reset password untuk user: {self.username_entry.get()}", 
                             font=("Arial", 10, "bold"))
        info_label.pack(pady=(0, 15))
        
        # Password baru
        password_frame = tk.Frame(main_frame)
        password_frame.pack(fill="x", pady=5)
        
        password_label = tk.Label(password_frame, text="Password Baru:")
        password_label.pack(side="left")
        
        new_password_var = tk.StringVar()
        new_password_entry = tk.Entry(password_frame, textvariable=new_password_var, show="*", width=25)
        new_password_entry.pack(side="right")
        
        # Password hint
        password_hint = tk.Label(main_frame, text="Min. 6 karakter, harus mengandung huruf dan angka", 
                               fg="gray", font=("Arial", 8))
        password_hint.pack(anchor="e", padx=5)
        
        # Konfirmasi password
        confirm_frame = tk.Frame(main_frame)
        confirm_frame.pack(fill="x", pady=5)
        
        confirm_label = tk.Label(confirm_frame, text="Konfirmasi Password:")
        confirm_label.pack(side="left")
        
        confirm_password_var = tk.StringVar()
        confirm_password_entry = tk.Entry(confirm_frame, textvariable=confirm_password_var, show="*", width=25)
        confirm_password_entry.pack(side="right")
        
        # Tampilkan password
        show_password_var = tk.BooleanVar(value=False)
        show_password_check = tk.Checkbutton(main_frame, text="Tampilkan password", 
                                           variable=show_password_var)
        show_password_check.pack(anchor="w", pady=5)
        
        # Fungsi untuk toggle password visibility
        def toggle_password_visibility():
            if show_password_var.get():
                new_password_entry.config(show="")
                confirm_password_entry.config(show="")
            else:
                new_password_entry.config(show="*")
                confirm_password_entry.config(show="*")
                
        show_password_check.config(command=toggle_password_visibility)
        
        # Tombol aksi
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        # Fungsi untuk menyimpan password baru
        def save_new_password():
            new_password = new_password_var.get()
            confirm_password = confirm_password_var.get()
            
            # Validasi password
            if not new_password:
                messagebox.showerror("Error", "Password baru harus diisi!", parent=reset_window)
                new_password_entry.focus()
                return
                
            if len(new_password) < 6:
                messagebox.showerror("Error", "Password minimal 6 karakter!", parent=reset_window)
                new_password_entry.focus()
                return
                
            # Validasi password harus mengandung minimal 1 huruf dan 1 angka
            if not (re.search(r'[a-zA-Z]', new_password) and re.search(r'[0-9]', new_password)):
                messagebox.showerror("Error", "Password harus mengandung minimal 1 huruf dan 1 angka!", parent=reset_window)
                new_password_entry.focus()
                return
                
            # Validasi konfirmasi password
            if new_password != confirm_password:
                messagebox.showerror("Error", "Konfirmasi password tidak sesuai!", parent=reset_window)
                confirm_password_entry.focus()
                return
            
            # Ambil data user dari database
            username = self.username_entry.get().strip()
            role = self.role_combobox.get()
            
            # Catat waktu reset password sebagai waktu login terakhir
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Update password dan waktu login terakhir
            try:
                self.db.connect()
                self.db.cursor.execute(
                    "UPDATE user SET password = ?, last_login = ? WHERE id = ?",
                    (new_password, current_time, self.user_id)
                )
                self.db.commit()
                
                messagebox.showinfo("Sukses", "Password berhasil direset!", parent=reset_window)
                reset_window.destroy()
                
                # Jika user yang direset adalah user yang sedang login, tampilkan pesan tambahan
                if is_current_user:
                    messagebox.showinfo("Informasi", "Anda telah mereset password Anda sendiri. Harap ingat password baru Anda.")
                    
                # Refresh tabel untuk menampilkan waktu login terakhir yang diperbarui
                self.load_user()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal mereset password: {str(e)}", parent=reset_window)
            finally:
                self.db.disconnect()
        
        # Tombol simpan dan batal
        simpan_button = tk.Button(button_frame, text="Simpan", command=save_new_password, 
                                width=10, bg="#4CAF50", fg="white")
        simpan_button.pack(side="left", padx=5)
        
        batal_button = tk.Button(button_frame, text="Batal", command=reset_window.destroy, width=10)
        batal_button.pack(side="left", padx=5)
        
        # Set fokus ke field password baru
        new_password_entry.focus()

# Untuk testing modul secara independen
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Test User View")
    root.geometry("800x500")
    
    class TestController:
        def __init__(self):
            self.current_user = {"id": 1, "username": "admin", "role": "Admin"}
        
        def show_frame(self, frame_name):
            print(f"Showing frame: {frame_name}")
    
    controller = TestController()
    user_view = UserView(root, controller)
    user_view.pack(fill="both", expand=True)
    
    root.mainloop()