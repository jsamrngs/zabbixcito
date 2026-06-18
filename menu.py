import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from fpdf import FPDF
import smtplib
from email.message import EmailMessage
import ssl
from datetime import datetime

class FormularioEnfermeria:
    def __init__(self, root):
        self.root = root
        self.root.title("Registro de Enfermería")
        self.root.geometry("400x250")
        self.root.resizable(False, False)

        titulo = ttk.Label(root, text="Formulario de Atención", font=("Arial", 16))
        titulo.pack(pady=10)

        frame = ttk.Frame(root)
        frame.pack(pady=10)

        ttk.Label(frame, text="Nombre del estudiante:").grid(row=0, column=0, sticky="w", pady=5)
        self.nombre_entry = ttk.Entry(frame, width=30)
        self.nombre_entry.grid(row=0, column=1)

        ttk.Label(frame, text="Curso:").grid(row=1, column=0, sticky="w", pady=5)
        self.curso_entry = ttk.Entry(frame, width=30)
        self.curso_entry.grid(row=1, column=1)

        botones_frame = ttk.Frame(root)
        botones_frame.pack(pady=20)

        crear_btn = ttk.Button(botones_frame, text="Crear registro", command=self.crear_registro)
        crear_btn.grid(row=0, column=0, padx=10)

        salir_btn = ttk.Button(botones_frame, text="Salir", command=self.root.quit)
        salir_btn.grid(row=0, column=1, padx=10)

    # ---------------------------------------------------------
    # GENERAR PDF
    # ---------------------------------------------------------
    def generar_pdf(self, nombre, curso):
        fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"registro_{nombre}_{fecha}.pdf".replace(" ", "_")

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="Registro de Atención - Enfermería", ln=True, align="C")
        pdf.ln(10)

        pdf.cell(100, 10, txt=f"Nombre del estudiante: {nombre}", ln=True)
        pdf.cell(100, 10, txt=f"Curso: {curso}", ln=True)
        pdf.cell(100, 10, txt=f"Fecha y hora: {datetime.now().strftime('%d-%m-%Y %H:%M')}", ln=True)

        pdf.output(filename)
        return filename

    # ---------------------------------------------------------
    # ENVIAR CORREO
    # ---------------------------------------------------------
    def enviar_correo(self, destinatario, archivo_pdf):
        remitente = "informes.enfermeria@caprat.cl"
        password = "lfwf huih nnew qcga"

        asunto = "Informe de Atención - Enfermería"
        cuerpo = (
            "Estimado apoderado,\n\n"
            "Adjunto encontrará el informe correspondiente a la atención realizada.\n\n"
            "Saludos cordiales,\n"
            "Enfermería Colegio Caprat"
        )

        mensaje = EmailMessage()
        mensaje["From"] = remitente
        mensaje["To"] = destinatario
        mensaje["Subject"] = asunto
        mensaje.set_content(cuerpo)

        with open(archivo_pdf, "rb") as f:
            mensaje.add_attachment(
                f.read(),
                maintype="application",
                subtype="pdf",
                filename=archivo_pdf
            )

        contexto = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexto) as smtp:
            smtp.login(remitente, password)
            smtp.send_message(mensaje)

    # ---------------------------------------------------------
    # BOTÓN CREAR REGISTRO
    # ---------------------------------------------------------
    def crear_registro(self):
        nombre = self.nombre_entry.get().strip()
        curso = self.curso_entry.get().strip()

        if not nombre or not curso:
            messagebox.showwarning("Campos incompletos", "Debes completar todos los campos.")
            return

        pdf_file = self.generar_pdf(nombre, curso)

        try:
            self.enviar_correo("diosmary.rodriguez@caprat.cl", pdf_file)
            messagebox.showinfo("Éxito", "Registro creado y enviado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo enviar el correo.\n{e}")

# --- EJECUCIÓN ---
if __name__ == "__main__":
    root = tk.Tk()
    app = FormularioEnfermeria(root)
    root.mainloop()
