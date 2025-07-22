import tkinter as tk
from tkinter import messagebox
import threading
from rpa_login import login_glovo


def handle_login():
    email = email_entry.get()
    password = password_entry.get()
    if not email or not password:
        messagebox.showerror('Error', 'Por favor ingresa email y contraseña.')
        return
    login_button.config(state=tk.DISABLED)
    status_label.config(text='Iniciando sesión...')

    def run_login():
        result = login_glovo(email, password)
        status_label.config(text=result)
        login_button.config(state=tk.NORMAL)
        if 'exitoso' in result:
            messagebox.showinfo('Éxito', result)
        else:
            messagebox.showerror('Error', result)

    threading.Thread(target=run_login, daemon=True).start()


root = tk.Tk()
root.title('RPA Login Glovo')
root.geometry('350x200')

# Email
tk.Label(root, text='Email:').pack(pady=(20, 0))
email_entry = tk.Entry(root, width=30)
email_entry.pack()
email_entry.insert(0, 'hola@solucioning.net')

# Password
tk.Label(root, text='Contraseña:').pack(pady=(10, 0))
password_entry = tk.Entry(root, width=30, show='*')
password_entry.pack()
password_entry.insert(0, 'Solucioning25+-.')

# Botón
login_button = tk.Button(root, text='Iniciar sesión', command=handle_login)
login_button.pack(pady=15)

# Estado
status_label = tk.Label(root, text='')
status_label.pack()

root.mainloop() 