import subprocess
import sys
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

RAIZ_PROYECTO = Path(__file__).resolve().parent.parent
RUTA_REPORTES = RAIZ_PROYECTO / "reportes"
RUTA_BASE_DATOS = RAIZ_PROYECTO / "base_datos"

sys.path.append(str(RUTA_REPORTES))
sys.path.append(str(RUTA_BASE_DATOS))

from generar_pdf import generar_ambos_reportes
from mongodb import guardar_tabla_simbolos

COLOR_FONDO = "#F8FAFC"
COLOR_ENCABEZADO = "#0F172A"
COLOR_TEXTO_SECUNDARIO = "#CBD5E1"
COLOR_AZUL = "#2563EB"
COLOR_AZUL_OSCURO = "#1D4ED8"
COLOR_VERDE = "#16A34A"
COLOR_VERDE_OSCURO = "#15803D"
COLOR_GRIS = "#64748B"
COLOR_GRIS_OSCURO = "#475569"
COLOR_BLANCO = "#FFFFFF"

ventana = tk.Tk()
ventana.title("Analizador Léxico de Swift")
ventana.geometry("1100x700")
ventana.minsize(900, 600)
ventana.configure(bg=COLOR_FONDO)

archivo_swift = None
ultimo_resumen = ""

estilo = ttk.Style()

estilo.configure(
    "TNotebook.Tab",
    font=("Arial", 11, "bold"),
    padding=[15, 8]
)

estilo.configure(
    "Treeview",
    font=("Arial", 10),
    rowheight=28
)

estilo.configure(
    "Treeview.Heading",
    font=("Arial", 10, "bold")
)


def seleccionar_archivo():
    global archivo_swift
    global ultimo_resumen

    archivo = filedialog.askopenfilename(
        title="Seleccionar archivo Swift",
        initialdir=RAIZ_PROYECTO / "ejemplos_swift",
        filetypes=[
            ("Archivos Swift", "*.swift"),
            ("Todos los archivos", "*.*")
        ]
    )

    if archivo == "":
        return

    archivo_swift = Path(archivo)
    ultimo_resumen = ""

    entrada_ruta.config(state="normal")
    entrada_ruta.delete(0, tk.END)
    entrada_ruta.insert(0, str(archivo_swift))
    entrada_ruta.config(state="readonly")

    limpiar_resultados()

    etiqueta_estado.config(
        text="Archivo seleccionado correctamente"
    )


def analizar_archivo():
    global ultimo_resumen

    if archivo_swift is None:
        messagebox.showwarning(
            "Archivo requerido",
            "Primero seleccione un archivo Swift."
        )
        return

    ejecutable = RAIZ_PROYECTO / "analizador" / "analizador"

    if not ejecutable.exists():
        messagebox.showerror(
            "Analizador no encontrado",
            "No se encontró el ejecutable del analizador.\n\n"
            "Compile primero el archivo Flex."
        )
        return

    try:
        with archivo_swift.open("r", encoding="utf-8") as archivo:
            proceso = subprocess.run(
                [str(ejecutable)],
                stdin=archivo,
                capture_output=True,
                text=True,
                cwd=RAIZ_PROYECTO,
                check=True
            )

        ultimo_resumen = proceso.stdout

        mostrar_resumen(proceso.stdout)
        cargar_tokens()
        cargar_simbolos()

        etiqueta_estado.config(
            text="Análisis realizado correctamente"
        )

        messagebox.showinfo(
            "Análisis",
            "El archivo fue analizado correctamente."
        )

    except Exception as error:
        messagebox.showerror(
            "Error",
            str(error)
        )


def mostrar_resumen(texto):
    marcador = "===== RESUMEN ====="

    if marcador in texto:
        texto = marcador + texto.split(marcador, 1)[1]

    cuadro_resumen.delete("1.0", tk.END)
    cuadro_resumen.insert(tk.END, texto)


def cargar_tokens():
    limpiar_tabla(tabla_tokens)

    ruta = RAIZ_PROYECTO / "tokens.txt"

    if not ruta.exists():
        return

    with ruta.open("r", encoding="utf-8") as archivo:
        for fila in archivo:
            datos = fila.rstrip("\n").split("\t", 2)

            if len(datos) == 3:
                linea = datos[0]
                token = datos[1]
                lexema = datos[2]

                tabla_tokens.insert(
                    "",
                    tk.END,
                    values=(linea, token, lexema)
                )


def cargar_simbolos():
    limpiar_tabla(tabla_simbolos)

    ruta = RAIZ_PROYECTO / "tabla_simbolos.txt"

    if not ruta.exists():
        return

    with ruta.open("r", encoding="utf-8") as archivo:
        primera_linea = True

        for fila in archivo:
            datos = fila.rstrip("\n").split("\t", 2)

            if primera_linea:
                primera_linea = False

                if datos and datos[0].lower().startswith("lexema"):
                    continue

            if len(datos) == 3:
                lexema = datos[0]
                token = datos[1]
                linea = datos[2]

                tabla_simbolos.insert(
                    "",
                    tk.END,
                    values=(lexema, token, linea)
                )


def generar_pdf():
    if archivo_swift is None:
        messagebox.showwarning(
            "Archivo requerido",
            "Primero seleccione un archivo."
        )
        return

    if ultimo_resumen == "":
        messagebox.showwarning(
            "Análisis requerido",
            "Primero debe analizar el archivo."
        )
        return

    try:
        generar_ambos_reportes(
            RAIZ_PROYECTO,
            archivo_swift,
            ultimo_resumen
        )

        etiqueta_estado.config(
            text="Reportes PDF generados correctamente"
        )

        messagebox.showinfo(
            "PDF",
            "Los dos reportes se generaron correctamente."
        )

    except Exception as error:
        messagebox.showerror(
            "Error",
            str(error)
        )


def guardar_mongodb():
    if archivo_swift is None:
        messagebox.showwarning(
            "Archivo requerido",
            "Primero seleccione un archivo."
        )
        return

    if ultimo_resumen == "":
        messagebox.showwarning(
            "Análisis requerido",
            "Primero analice el archivo."
        )
        return

    ruta_tabla = RAIZ_PROYECTO / "tabla_simbolos.txt"

    try:
        cantidad = guardar_tabla_simbolos(
            ruta_tabla,
            archivo_swift.name
        )

        etiqueta_estado.config(
            text="Datos guardados en MongoDB"
        )

        messagebox.showinfo(
            "MongoDB",
            f"Se guardaron {cantidad} símbolos."
        )

    except Exception as error:
        messagebox.showerror(
            "MongoDB",
            str(error)
        )


def limpiar_resultados():
    cuadro_resumen.delete("1.0", tk.END)
    limpiar_tabla(tabla_tokens)
    limpiar_tabla(tabla_simbolos)


def limpiar_todo():
    global archivo_swift
    global ultimo_resumen

    archivo_swift = None
    ultimo_resumen = ""

    entrada_ruta.config(state="normal")
    entrada_ruta.delete(0, tk.END)
    entrada_ruta.config(state="readonly")

    limpiar_resultados()

    etiqueta_estado.config(
        text="Esperando archivo..."
    )


def limpiar_tabla(tabla):
    for fila in tabla.get_children():
        tabla.delete(fila)


encabezado = tk.Frame(
    ventana,
    bg=COLOR_ENCABEZADO,
    height=90
)

encabezado.pack(fill="x")

titulo = tk.Label(
    encabezado,
    text="Analizador Léxico de Swift",
    font=("Arial", 24, "bold"),
    bg=COLOR_ENCABEZADO,
    fg=COLOR_BLANCO
)

titulo.pack(pady=(15, 2))

subtitulo = tk.Label(
    encabezado,
    text="Proyecto de Compiladores",
    font=("Arial", 11),
    bg=COLOR_ENCABEZADO,
    fg=COLOR_TEXTO_SECUNDARIO
)

subtitulo.pack()

marco_archivo = tk.Frame(
    ventana,
    bg=COLOR_FONDO
)

marco_archivo.pack(
    fill="x",
    padx=30,
    pady=(20, 10)
)

etiqueta_archivo = tk.Label(
    marco_archivo,
    text="Archivo Swift:",
    font=("Arial", 11, "bold"),
    bg=COLOR_FONDO,
    fg=COLOR_ENCABEZADO
)

etiqueta_archivo.pack(anchor="w")

marco_ruta = tk.Frame(
    marco_archivo,
    bg=COLOR_FONDO
)

marco_ruta.pack(
    fill="x",
    pady=5
)

entrada_ruta = tk.Entry(
    marco_ruta,
    font=("Arial", 11),
    state="readonly"
)

entrada_ruta.pack(
    side="left",
    fill="x",
    expand=True,
    ipady=6
)

boton_abrir = tk.Button(
    marco_ruta,
    text="Seleccionar archivo",
    command=seleccionar_archivo,
    font=("Arial", 10, "bold"),
    bg=COLOR_AZUL,
    fg=COLOR_BLANCO,
    activebackground=COLOR_AZUL_OSCURO,
    activeforeground=COLOR_BLANCO,
    width=18,
    cursor="hand2"
)

boton_abrir.pack(
    side="left",
    padx=(10, 0),
    ipady=4
)

marco_botones = tk.Frame(
    ventana,
    bg=COLOR_FONDO
)

marco_botones.pack(pady=10)

boton_analizar = tk.Button(
    marco_botones,
    text="Analizar",
    command=analizar_archivo,
    width=16,
    font=("Arial", 10, "bold"),
    bg=COLOR_AZUL,
    fg=COLOR_BLANCO,
    activebackground=COLOR_AZUL_OSCURO,
    activeforeground=COLOR_BLANCO,
    cursor="hand2"
)

boton_analizar.grid(
    row=0,
    column=0,
    padx=6,
    ipady=5
)

boton_pdf = tk.Button(
    marco_botones,
    text="Generar PDF",
    command=generar_pdf,
    width=16,
    font=("Arial", 10, "bold"),
    bg=COLOR_AZUL,
    fg=COLOR_BLANCO,
    activebackground=COLOR_AZUL_OSCURO,
    activeforeground=COLOR_BLANCO,
    cursor="hand2"
)

boton_pdf.grid(
    row=0,
    column=1,
    padx=6,
    ipady=5
)

boton_mongo = tk.Button(
    marco_botones,
    text="Guardar MongoDB",
    command=guardar_mongodb,
    width=18,
    font=("Arial", 10, "bold"),
    bg=COLOR_VERDE,
    fg=COLOR_BLANCO,
    activebackground=COLOR_VERDE_OSCURO,
    activeforeground=COLOR_BLANCO,
    cursor="hand2"
)

boton_mongo.grid(
    row=0,
    column=2,
    padx=6,
    ipady=5
)

boton_limpiar = tk.Button(
    marco_botones,
    text="Limpiar",
    command=limpiar_todo,
    width=14,
    font=("Arial", 10, "bold"),
    bg=COLOR_GRIS,
    fg=COLOR_BLANCO,
    activebackground=COLOR_GRIS_OSCURO,
    activeforeground=COLOR_BLANCO,
    cursor="hand2"
)

boton_limpiar.grid(
    row=0,
    column=3,
    padx=6,
    ipady=5
)

pestanas = ttk.Notebook(ventana)

pestanas.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=10
)

pestana_resumen = tk.Frame(
    pestanas,
    bg=COLOR_BLANCO
)

pestanas.add(
    pestana_resumen,
    text="Resumen"
)

cuadro_resumen = tk.Text(
    pestana_resumen,
    font=("Courier New", 12),
    padx=15,
    pady=15,
    bg=COLOR_BLANCO,
    fg=COLOR_ENCABEZADO
)

cuadro_resumen.pack(
    fill="both",
    expand=True
)

pestana_tokens = tk.Frame(
    pestanas,
    bg=COLOR_BLANCO
)

pestanas.add(
    pestana_tokens,
    text="Tokens"
)

tabla_tokens = ttk.Treeview(
    pestana_tokens,
    columns=("linea", "token", "lexema"),
    show="headings"
)

tabla_tokens.heading(
    "linea",
    text="Línea"
)

tabla_tokens.heading(
    "token",
    text="Token"
)

tabla_tokens.heading(
    "lexema",
    text="Lexema"
)

tabla_tokens.column(
    "linea",
    width=100,
    anchor="center"
)

tabla_tokens.column(
    "token",
    width=300,
    anchor="center"
)

tabla_tokens.column(
    "lexema",
    width=450
)

tabla_tokens.pack(
    fill="both",
    expand=True
)

pestana_simbolos = tk.Frame(
    pestanas,
    bg=COLOR_BLANCO
)

pestanas.add(
    pestana_simbolos,
    text="Tabla de símbolos"
)

tabla_simbolos = ttk.Treeview(
    pestana_simbolos,
    columns=("lexema", "token", "linea"),
    show="headings"
)

tabla_simbolos.heading(
    "lexema",
    text="Lexema"
)

tabla_simbolos.heading(
    "token",
    text="Token"
)

tabla_simbolos.heading(
    "linea",
    text="Línea"
)

tabla_simbolos.column(
    "lexema",
    width=400
)

tabla_simbolos.column(
    "token",
    width=300,
    anchor="center"
)

tabla_simbolos.column(
    "linea",
    width=100,
    anchor="center"
)

tabla_simbolos.pack(
    fill="both",
    expand=True
)

barra_estado = tk.Frame(
    ventana,
    bg=COLOR_ENCABEZADO
)

barra_estado.pack(fill="x")

etiqueta_estado = tk.Label(
    barra_estado,
    text="Esperando archivo...",
    font=("Arial", 10),
    bg=COLOR_ENCABEZADO,
    fg=COLOR_BLANCO
)

etiqueta_estado.pack(
    anchor="w",
    padx=15,
    pady=8
)

ventana.mainloop()
