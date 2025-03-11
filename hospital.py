import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import re
import datetime

def conectar_db():
    conn = sqlite3.connect("citas_medicas.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS pacientes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT NOT NULL,
                        edad INTEGER NOT NULL,
                        telefono TEXT NOT NULL,
                        direccion TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS medicos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT NOT NULL,
                        especialidad TEXT NOT NULL,
                        telefono TEXT NOT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS citas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        paciente_id INTEGER,
                        medico_id INTEGER,
                        fecha_hora TEXT NOT NULL,
                        estado TEXT NOT NULL,
                        FOREIGN KEY (paciente_id) REFERENCES pacientes(id),
                        FOREIGN KEY (medico_id) REFERENCES medicos(id))''')
    conn.commit()
    conn.close()

def agregar_paciente(nombre, edad, telefono, direccion):
    conn = sqlite3.connect("citas_medicas.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pacientes (nombre, edad, telefono, direccion) VALUES (?, ?, ?, ?)",
                   (nombre, edad, telefono, direccion))
    conn.commit()
    conn.close()

def listar_pacientes():
    conn = sqlite3.connect("citas_medicas.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pacientes")
    pacientes = cursor.fetchall()
    conn.close()
    return pacientes

def editar_paciente(id, nombre, edad, telefono, direccion):
    conn = sqlite3.connect("citas_medicas.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE pacientes SET nombre=?, edad=?, telefono=?, direccion=? WHERE id=?",
                   (nombre, edad, telefono, direccion, id))
    conn.commit()
    conn.close()

def eliminar_paciente(id):
    conn = sqlite3.connect("citas_medicas.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pacientes WHERE id=?", (id,))
    conn.commit()
    conn.close()

def agregar_medico(nombre, especialidad, telefono):
    conn = sqlite3.connect("citas_medicas.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO medicos (nombre, especialidad, telefono) VALUES (?, ?, ?)",
                   (nombre, especialidad, telefono))
    conn.commit()
    conn.close()

def listar_medicos():
    conn = sqlite3.connect("citas_medicas.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medicos")
    medicos = cursor.fetchall()
    conn.close()
    return medicos

def editar_medico(id, nombre, especialidad, telefono):
    conn = sqlite3.connect("citas_medicas.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE medicos SET nombre=?, especialidad=?, telefono=? WHERE id=?",
                   (nombre, especialidad, telefono, id))
    conn.commit()
    conn.close()

def eliminar_medico(id):
    conn = sqlite3.connect("citas_medicas.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM medicos WHERE id=?", (id,))
    conn.commit()
    conn.close()



def ventana_pacientes():
    win = tk.Toplevel(root)
    win.title("Gestión de Pacientes")
    win.geometry("1050x500")

    title_label = tk.Label(win, text="Gestión de Pacientes", font=("Arial", 20), fg="#152281")
    title_label.pack(pady=10)

    tk.Label(win, text="Nombre:").pack()
    entry_nombre = tk.Entry(win)
    entry_nombre.pack()

    tk.Label(win, text="Edad:").pack()
    entry_edad = tk.Entry(win)
    entry_edad.pack()

    tk.Label(win, text="Teléfono:").pack()
    entry_telefono = tk.Entry(win)
    entry_telefono.pack()

    tk.Label(win, text="Dirección:").pack()
    entry_direccion = tk.Entry(win)
    entry_direccion.pack()

    def validar_campos(nombre, edad, telefono, direccion):
        if not (nombre and edad and telefono and direccion):
            messagebox.showwarning("Advertencia", "Debe completar todos los campos.")
            return False
        if not edad.isdigit() or not telefono.isdigit():
            messagebox.showwarning("Advertencia", "La edad y el teléfono deben ser numéricos.")
            return False
        return True

    def agregar():
        nombre = entry_nombre.get()
        edad = entry_edad.get()
        telefono = entry_telefono.get()
        direccion = entry_direccion.get()
        if validar_campos(nombre, edad, telefono, direccion):
            agregar_paciente(nombre, edad, telefono, direccion)
            messagebox.showinfo("Éxito", "Paciente agregado correctamente")
            listar()

    def abrir_editar_formulario(id, nombre, edad, telefono, direccion):
        editar_win = tk.Toplevel()
        editar_win.title("Editar Paciente")
        editar_win.geometry("300x300")

        tk.Label(editar_win, text="Nombre:").pack()
        entry_nombre_edit = tk.Entry(editar_win)
        entry_nombre_edit.insert(0, nombre)
        entry_nombre_edit.pack()

        tk.Label(editar_win, text="Edad:").pack()
        entry_edad_edit = tk.Entry(editar_win)
        entry_edad_edit.insert(0, edad)
        entry_edad_edit.pack()

        tk.Label(editar_win, text="Teléfono:").pack()
        entry_telefono_edit = tk.Entry(editar_win)
        entry_telefono_edit.insert(0, telefono)
        entry_telefono_edit.pack()

        tk.Label(editar_win, text="Dirección:").pack()
        entry_direccion_edit = tk.Entry(editar_win)
        entry_direccion_edit.insert(0, direccion)
        entry_direccion_edit.pack()

        def confirmar_editar():
            nombre = entry_nombre_edit.get()
            edad = entry_edad_edit.get()
            telefono = entry_telefono_edit.get()
            direccion = entry_direccion_edit.get()
            if validar_campos(nombre, edad, telefono, direccion):
                editar_paciente(id, nombre, edad, telefono, direccion)
                messagebox.showinfo("Éxito", "Paciente editado correctamente")
                editar_win.destroy()
                listar()

        tk.Button(editar_win, text="Editar", command=confirmar_editar).pack(pady=5)
        tk.Button(editar_win, text="Cancelar", command=editar_win.destroy).pack(pady=5)

    def editar():
        selected_item = tree.selection()
        if selected_item:
            item_values = tree.item(selected_item, 'values')
            abrir_editar_formulario(item_values[0], item_values[1], item_values[2], item_values[3], item_values[4])
        else:
            messagebox.showwarning("Advertencia", "Debe seleccionar un paciente para editar.")

    def eliminar():
        selected_item = tree.selection()
        if selected_item:
            item_values = tree.item(selected_item, 'values')
            if messagebox.askyesno("Confirmar", f"¿Desea eliminar al paciente ID {item_values[0]}?"):
                eliminar_paciente(item_values[0])
                messagebox.showinfo("Éxito", "Paciente eliminado correctamente")
                listar()
        else:
            messagebox.showwarning("Advertencia", "Debe seleccionar un paciente para eliminar.")

    tk.Button(win, text="Agregar", command=agregar).pack(pady=5)

    button_frame = tk.Frame(win)
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Agregar", command=agregar).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="Editar", command=editar).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="Eliminar", command=eliminar).pack(side=tk.LEFT, padx=10)

    tree = ttk.Treeview(win, columns=("ID", "Paciente ID", "Médico ID", "Fecha y Hora", "Estado"), show="headings")
    for col in ("ID", "Paciente ID", "Médico ID", "Fecha y Hora", "Estado"):
        tree.heading(col, text=col)
    tree.pack()

    def listar():
        for item in tree.get_children():
            tree.delete(item)
        for row in listar_citas():
            tree.insert("", "end", values=row)
    listar()


def ventana_medicos():
    win = tk.Toplevel(root)
    win.title("Gestión de Médicos")
    win.geometry("1050x500")

    title_label = tk.Label(win, text="Gestión de Médicos", font=("Arial", 20), fg="#152281")
    title_label.pack(pady=10)

    tk.Label(win, text="Nombre:").pack()
    entry_nombre = tk.Entry(win)
    entry_nombre.pack()

    tk.Label(win, text="Especialidad:").pack()

    especialidades = [
        "Cardiología",
        "Pediatría",
        "Ginecología",
        "Medicina General",
        "Dermatología",
        "Oftalmología",
        "Neurología",
        "Psiquiatría",
        "Ortopedia",
        "Oncología"
    ]

    combo_especialidad = ttk.Combobox(win, values=especialidades)
    combo_especialidad.set("Seleccionar especialidad")  # Texto por defecto
    combo_especialidad.pack(pady=5)

    tk.Label(win, text="Teléfono:").pack()
    entry_telefono = tk.Entry(win)
    entry_telefono.pack()

    def validar_campos_medico(nombre, especialidad, telefono):
        if not (nombre and especialidad and telefono):
            messagebox.showwarning("Advertencia", "Debe completar todos los campos.")
            return False
        if not telefono.isdigit():
            messagebox.showwarning("Advertencia", "El teléfono debe ser numérico.")
            return False
        return True

    def agregar():
        nombre = entry_nombre.get()
        especialidad = combo_especialidad.get()
        telefono = entry_telefono.get()
        if validar_campos_medico(nombre, especialidad, telefono):
            agregar_medico(nombre, especialidad, telefono)
            messagebox.showinfo("Éxito", "Médico agregado correctamente")
            listar()

    def abrir_editar_formulario(id, nombre, especialidad, telefono):
        editar_win = tk.Toplevel()
        editar_win.title("Editar Médico")
        editar_win.geometry("300x300")

        tk.Label(editar_win, text="Nombre:").pack()
        entry_nombre_edit = tk.Entry(editar_win)
        entry_nombre_edit.insert(0, nombre)
        entry_nombre_edit.pack()

        tk.Label(editar_win, text="Especialidad:").pack()

        combo_especialidad_edit = ttk.Combobox(editar_win, values=especialidades)
        combo_especialidad_edit.set(especialidad)
        combo_especialidad_edit.pack(pady=5)

        tk.Label(editar_win, text="Teléfono:").pack()
        entry_telefono_edit = tk.Entry(editar_win)
        entry_telefono_edit.insert(0, telefono)
        entry_telefono_edit.pack()

        def confirmar_editar():
            nombre = entry_nombre_edit.get()
            especialidad = combo_especialidad_edit.get()
            telefono = entry_telefono_edit.get()
            if validar_campos_medico(nombre, especialidad, telefono):
                editar_medico(id, nombre, especialidad, telefono)
                messagebox.showinfo("Éxito", "Médico editado correctamente")
                editar_win.destroy()
                listar()

        tk.Button(editar_win, text="Editar", command=confirmar_editar).pack(pady=5)
        tk.Button(editar_win, text="Cancelar", command=editar_win.destroy).pack(pady=5)

    def editar():
        selected_item = tree.selection()
        if selected_item:
            item_values = tree.item(selected_item, 'values')
            abrir_editar_formulario(item_values[0], item_values[1], item_values[2], item_values[3])
        else:
            messagebox.showwarning("Advertencia", "Debe seleccionar un médico para editar.")

    def eliminar():
        selected_item = tree.selection()
        if selected_item:
            item_values = tree.item(selected_item, 'values')
            if messagebox.askyesno("Confirmar", f"¿Desea eliminar al médico ID {item_values[0]}?"):
                eliminar_medico(item_values[0])
                messagebox.showinfo("Éxito", "Médico eliminado correctamente")
                listar()
        else:
            messagebox.showwarning("Advertencia", "Debe seleccionar un médico para eliminar.")

    tk.Button(win, text="Agregar", command=agregar).pack(pady=5)

    button_frame = tk.Frame(win)
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Editar", command=editar).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Eliminar", command=eliminar).pack(side=tk.LEFT, padx=5)

    tree = ttk.Treeview(win, columns=("ID", "Nombre", "Especialidad", "Teléfono"), show="headings")
    for col in ("ID", "Nombre", "Especialidad", "Teléfono"):
        tree.heading(col, text=col)
    tree.pack()

    def listar():
        for item in tree.get_children():
            tree.delete(item)
        for row in listar_medicos():
            tree.insert("", "end", values=row)

    listar()


def agregar_cita(paciente_id, medico_id, fecha_hora, estado):
    conn = sqlite3.connect("citas_medicas.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO citas (paciente_id, medico_id, fecha_hora, estado) VALUES (?, ?, ?, ?)",
                   (paciente_id, medico_id, fecha_hora, estado))
    conn.commit()
    conn.close()

def listar_citas():
    conn = sqlite3.connect("citas_medicas.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM citas")
    citas = cursor.fetchall()
    conn.close()
    return citas

def editar_cita(id, paciente_id, medico_id, fecha_hora, estado):
    conn = sqlite3.connect("citas_medicas.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE citas SET paciente_id=?, medico_id=?, fecha_hora=?, estado=? WHERE id=?",
                   (paciente_id, medico_id, fecha_hora, estado, id))
    conn.commit()
    conn.close()

def eliminar_cita(id):
    conn = sqlite3.connect("citas_medicas.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM citas WHERE id=?", (id,))
    conn.commit()
    conn.close()

def ventana_citas():
    win = tk.Toplevel(root)
    win.title("Gestión de Citas")
    win.geometry("1050x600")

    title_label = tk.Label(win, text="Gestión de Citas", font=("Arial", 20), fg="#152281")
    title_label.pack(pady=10)

    tk.Label(win, text="ID del Paciente:").pack()
    combo_paciente = ttk.Combobox(win, values=[p[0] for p in listar_pacientes()])
    combo_paciente.pack()

    tk.Label(win, text="ID del Médico:").pack()
    combo_medico = ttk.Combobox(win, values=[m[0] for m in listar_medicos()])
    combo_medico.pack()

    tk.Label(win, text="Fecha:").pack()
    fecha_entry = DateEntry(win)
    fecha_entry.pack()

    tk.Label(win, text="Hora (HH:MM):").pack()
    entry_hora = tk.Entry(win)
    entry_hora.pack()

    tk.Label(win, text="Estado:").pack()
    estado_entry = ttk.Combobox(win, values=["Pendiente", "Confirmada", "Cancelada"])
    estado_entry.set("Seleccionar estado")
    estado_entry.pack()

    def validar_hora(hora):
        pattern = r'^(0[0-9]|1[0-9]|2[0-3]|[0-9]):([0-5][0-9])$'
        return re.match(pattern, hora)

    def agregar():
        paciente_id = combo_paciente.get()
        medico_id = combo_medico.get()
        fecha = fecha_entry.get()
        hora = entry_hora.get()
        estado = estado_entry.get()

        if validar_hora(hora):
            fecha_hora = f"{fecha} {hora}"
            if paciente_id and medico_id and estado != "Seleccionar estado":
                agregar_cita(paciente_id, medico_id, fecha_hora, estado)
                messagebox.showinfo("Éxito", "Cita agregada correctamente")
                listar()
        else:
            messagebox.showwarning("Advertencia", "La hora debe estar en formato HH:MM.")

    def editar():
        selected_item = tree.selection()
        if selected_item:
            item_values = tree.item(selected_item, 'values')

            paciente_id = item_values[1]
            medico_id = item_values[2]
            fecha_hora = item_values[3]
            estado = item_values[4]

            fecha, hora = fecha_hora.split(" ")

            combo_paciente.set(paciente_id)
            combo_medico.set(medico_id)
            fecha_entry.set_date(fecha)
            entry_hora.delete(0, tk.END)
            entry_hora.insert(0, hora)
            estado_entry.set(estado)

            def confirmar_editar():
                paciente_id = combo_paciente.get()
                medico_id = combo_medico.get()
                fecha = fecha_entry.get()
                hora = entry_hora.get()
                estado = estado_entry.get()

                if validar_hora(hora):
                    fecha_hora = f"{fecha} {hora}"
                    editar_cita(item_values[0], paciente_id, medico_id, fecha_hora, estado)
                    messagebox.showinfo("Éxito", "Cita editada correctamente")
                    listar()
                    editar_win.destroy()

            editar_win = tk.Toplevel(win)
            editar_win.title("Editar Cita")
            editar_win.geometry("300x350")

            tk.Label(editar_win, text="ID del Paciente:").pack()
            combo_paciente_edit = ttk.Combobox(editar_win, values=[p[0] for p in listar_pacientes()])
            combo_paciente_edit.set(paciente_id)
            combo_paciente_edit.pack()

            tk.Label(editar_win, text="ID del Médico:").pack()
            combo_medico_edit = ttk.Combobox(editar_win, values=[m[0] for m in listar_medicos()])
            combo_medico_edit.set(medico_id)
            combo_medico_edit.pack()

            tk.Label(editar_win, text="Fecha:").pack()
            fecha_entry_edit = DateEntry(editar_win)
            fecha_entry_edit.set_date(fecha)
            fecha_entry_edit.pack()

            tk.Label(editar_win, text="Hora (HH:MM):").pack()
            entry_hora_edit = tk.Entry(editar_win)
            entry_hora_edit.insert(0, hora)
            entry_hora_edit.pack()

            tk.Label(editar_win, text="Estado:").pack()
            estado_entry_edit = ttk.Combobox(editar_win, values=["Pendiente", "Confirmada", "Cancelada"])
            estado_entry_edit.set(estado)
            estado_entry_edit.pack()

            tk.Button(editar_win, text="Confirmar Edición", command=confirmar_editar).pack(pady=5)
            tk.Button(editar_win, text="Cancelar", command=editar_win.destroy).pack(pady=5)
        else:
            messagebox.showwarning("Advertencia", "Debe seleccionar una cita para editar.")

    def eliminar():
        selected_item = tree.selection()
        if selected_item:
            item_values = tree.item(selected_item, 'values')
            if messagebox.askyesno("Confirmar", f"¿Desea eliminar la cita ID {item_values[0]}?"):
                eliminar_cita(item_values[0])
                messagebox.showinfo("Éxito", "Cita eliminada correctamente")
                listar()
        else:
            messagebox.showwarning("Advertencia", "Debe seleccionar una cita para eliminar.")

    tk.Button(win, text="Agregar", command=agregar).pack(pady=5)
    tk.Button(win, text="Editar", command=editar).pack(pady=5)
    tk.Button(win, text="Eliminar", command=eliminar).pack(pady=5)

    tree = ttk.Treeview(win, columns=("ID", "Paciente ID", "Médico ID", "Fecha y Hora", "Estado"), show="headings")
    for col in ("ID", "Paciente ID", "Médico ID", "Fecha y Hora", "Estado"):
        tree.heading(col, text=col)
    tree.pack()

    def listar():
        for item in tree.get_children():
            tree.delete(item)
        for row in listar_citas():
            tree.insert("", "end", values=row)

    listar()


root = tk.Tk()
root.title("Sistema de Gestión de Citas Médicas")
root.geometry("700x500")

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)
menu_gestion = tk.Menu(menu_bar, tearoff=0)
menu_gestion.add_command(label="Pacientes", command=ventana_pacientes)
menu_gestion.add_command(label="Médicos", command=ventana_medicos)
menu_gestion.add_command(label="Citas", command=ventana_citas)
menu_bar.add_cascade(label="Gestión", menu=menu_gestion)

conectar_db()
root.mainloop()