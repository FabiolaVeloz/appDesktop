import tkinter as tk
from tkinter import messagebox, ttk
import requests
import datetime
import socket

# URL base de la API local
local_api_url = "http://127.0.0.1:5000/cars"


# Función para obtener la IP del cliente automáticamente
def get_ip():
    try:
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)
    except socket.error:
        return "No se pudo obtener la IP"


# Función para inyectar registros a la API local
def add_car():
    name = name_combobox.get()
    status = selected_status.get()
    date = date_entry.get()
    ip_client = ip_client_entry.get()

    if not name or not status or not date or not ip_client:
        messagebox.showerror("Error", "Por favor, completa todos los campos.")
        return

    # Verificar el formato de fecha DD-MM-YYYY
    try:
        datetime.datetime.strptime(date, "%d-%m-%Y")  # Validar el formato
    except ValueError:
        messagebox.showerror("Error", "Formato de fecha incorrecto. Usa DD-MM-YYYY.")
        return

    new_car = {
        "status": status,
        "date": date,  # Usar DD-MM-YYYY para almacenar
        "ipClient": ip_client,
        "name": name
    }

    try:
        response = requests.post(local_api_url, json=new_car)
        response.raise_for_status()
        added_car = response.json()
        messagebox.showinfo("Éxito", "Registro añadido exitosamente.")
        show_single_car(added_car)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"No se pudo añadir el registro: {e}")


# Función para mostrar solo el registro recién inyectado en la tabla de la ventana de insertar
def show_single_car(car):
    for row in insert_car_list.get_children():
        insert_car_list.delete(row)
    insert_car_list.insert("", "end", values=(car['id'], car['status'], car['date'], car['ipClient'], car['name']))


# Función para obtener y mostrar los últimos 10 registros de la API local
def get_last_10_cars():
    try:
        response = requests.get(local_api_url)
        response.raise_for_status()
        cars = response.json()
        last_10_cars = cars[-10:]

        for row in verify_car_list.get_children():
            verify_car_list.delete(row)

        for car in last_10_cars:
            verify_car_list.insert("", "end",
                                   values=(car['id'], car['status'], car['date'], car['ipClient'], car['name']))

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"No se pudieron obtener los registros: {e}")


# Función para cambiar entre ventanas
def show_insert_frame():
    insert_frame.pack(fill="both", expand=True)
    verify_frame.pack_forget()


def show_verify_frame():
    verify_frame.pack(fill="both", expand=True)
    insert_frame.pack_forget()
    get_last_10_cars()  # Cargar los últimos 10 registros al abrir la ventana de verificación


# Inicializamos la ventana principal
root = tk.Tk()
root.title("Gestión de Registros de IoTCar")
root.geometry("800x600")

# Colores pastel
bg_color = "#f0f8ff"
btn_color = "#add8e6"
entry_color = "#e6e6fa"

# Estilo
style = ttk.Style()
style.configure("TLabel", font=("Arial", 12), background=bg_color)
style.configure("TButton", font=("Arial", 12), background=btn_color)
style.configure("TCombobox", font=("Arial", 12))
style.configure("Treeview", font=("Arial", 10), background=bg_color, fieldbackground=entry_color)
style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background=bg_color)

root.configure(bg=bg_color)

# Crear menú superior
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

menu_bar.add_command(label="Insertar", command=show_insert_frame)
menu_bar.add_command(label="Verificar", command=show_verify_frame)

# Frame para la inserción de registros
insert_frame = tk.Frame(root, bg=bg_color)

# Lista desplegable para nombre
tk.Label(insert_frame, text="Nombre", bg=bg_color).grid(row=0, column=0, padx=10, pady=10, sticky="w")
name_combobox = ttk.Combobox(insert_frame, values=["Fabiola", "Mariana"], state="readonly", font=("Arial", 12))
name_combobox.grid(row=0, column=1, padx=10, pady=10, sticky="w")

# Mosaico de botones para seleccionar status
tk.Label(insert_frame, text="Status", bg=bg_color).grid(row=1, column=0, padx=10, pady=10, sticky="w")

statuses = [
    "adelante", "atrás", "vuelta a la derecha",
    "vuelta a la izquierda", "giro 90° a la derecha",
    "giro 90° a la izquierda", "detenerse",
    "giro 360° a la derecha", "giro 360° a la izquierda"
]

selected_status = tk.StringVar()
selected_status.set(statuses[0])

status_frame = tk.Frame(insert_frame, bg=bg_color)
status_frame.grid(row=2, column=0, columnspan=2, pady=10)

for i, status in enumerate(statuses):
    tk.Radiobutton(status_frame, text=status, variable=selected_status, value=status, font=("Arial", 12),
                   bg=bg_color).grid(row=i // 3, column=i % 3, padx=10, pady=5)

# Campo de fecha (DD-MM-YYYY)
tk.Label(insert_frame, text="Date (DD-MM-YYYY)", bg=bg_color).grid(row=3, column=0, padx=10, pady=10, sticky="w")
date_entry = tk.Entry(insert_frame, font=("Arial", 12), bg=entry_color)
date_entry.insert(0, datetime.datetime.now().strftime("%d-%m-%Y"))
date_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

# Campo de IP (automática)
tk.Label(insert_frame, text="IP Client", bg=bg_color).grid(row=4, column=0, padx=10, pady=10, sticky="w")
ip_client_entry = tk.Entry(insert_frame, font=("Arial", 12), bg=entry_color)
ip_client_entry.insert(0, get_ip())
ip_client_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w")

# Botón para inyectar el registro
add_button = tk.Button(insert_frame, text="Inyectar registro", command=add_car, font=("Arial", 12), bg=btn_color)
add_button.grid(row=5, column=0, columnspan=2, pady=10)

# Tabla para mostrar el registro recién añadido
insert_car_list = ttk.Treeview(insert_frame, columns=("ID", "Status", "Date", "IP Client", "Name"), show="headings",
                               height=5)
insert_car_list.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

for col in ("ID", "Status", "Date", "IP Client", "Name"):
    insert_car_list.heading(col, text=col, anchor="center")
    insert_car_list.column(col, width=150, anchor="center")

# Frame para la verificación de registros
verify_frame = tk.Frame(root, bg=bg_color)

# Botón para obtener los últimos 10 registros
get_button = tk.Button(verify_frame, text="Obtener últimos 10 registros", command=get_last_10_cars, font=("Arial", 12),
                       bg=btn_color)
get_button.pack(pady=10)

# Tabla para mostrar los últimos 10 registros obtenidos de la API local
verify_car_list = ttk.Treeview(verify_frame, columns=("ID", "Status", "Date", "IP Client", "Name"), show="headings",
                               height=10)
verify_car_list.pack(padx=10, pady=10, fill="both", expand=True)

for col in ("ID", "Status", "Date", "IP Client", "Name"):
    verify_car_list.heading(col, text=col, anchor="center")
    verify_car_list.column(col, width=150, anchor="center")

# Mostrar la ventana de inserción al inicio
insert_frame.pack(fill="both", expand=True)

root.mainloop()





