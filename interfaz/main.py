import subprocess
import sys
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk


# =========================================================
# RUTAS DEL PROYECTO
# =========================================================

RAIZ_PROYECTO = Path(__file__).resolve().parent.parent
RUTA_REPORTES = RAIZ_PROYECTO / "reportes"
RUTA_BASE_DATOS = RAIZ_PROYECTO / "base_datos"


# Permitimos importar los archivos de reportes y MongoDB.
if str(RUTA_REPORTES) not in sys.path:
    sys.path.insert(0, str(RUTA_REPORTES))

if str(RUTA_BASE_DATOS) not in sys.path:
    sys.path.insert(0, str(RUTA_BASE_DATOS))


from generar_pdf import generar_ambos_reportes
from mongodb import guardar_tabla_simbolos


# =========================================================
# CLASE PRINCIPAL DE LA INTERFAZ
# =========================================================

class InterfazAnalizador:
    def __init__(self, ventana):
        self.ventana = ventana

        self.ventana.title(
            "Analizador Léxico de Swift"
        )

        self.ventana.geometry(
            "1150x720"
        )

        self.ventana.minsize(
            900,
            600
        )

        self.raiz_proyecto = RAIZ_PROYECTO

        self.archivo_swift = None

        self.ultimo_resumen = ""

        self.crear_interfaz()

    # =====================================================
    # CREACIÓN DE LA INTERFAZ
    # =====================================================

    def crear_interfaz(self):
        titulo = tk.Label(
            self.ventana,
            text="Analizador Léxico de Código Swift",
            font=("Arial", 20, "bold")
        )

        titulo.pack(
            pady=15
        )

        # -------------------------------------------------
        # SELECCIÓN DE ARCHIVO
        # -------------------------------------------------

        marco_archivo = tk.Frame(
            self.ventana
        )

        marco_archivo.pack(
            fill="x",
            padx=20,
            pady=(0, 10)
        )

        self.entrada_ruta = tk.Entry(
            marco_archivo,
            font=("Arial", 11)
        )

        self.entrada_ruta.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 10)
        )

        boton_abrir = tk.Button(
            marco_archivo,
            text="Abrir archivo Swift",
            command=self.seleccionar_archivo,
            width=18
        )

        boton_abrir.pack(
            side="left"
        )

        # -------------------------------------------------
        # BOTONES PRINCIPALES
        # -------------------------------------------------

        marco_botones = tk.Frame(
            self.ventana
        )

        marco_botones.pack(
            pady=5
        )

        boton_analizar = tk.Button(
            marco_botones,
            text="Analizar archivo",
            command=self.analizar_archivo,
            font=("Arial", 11, "bold"),
            width=18
        )

        boton_analizar.pack(
            side="left",
            padx=5
        )

        boton_pdf = tk.Button(
            marco_botones,
            text="Generar reportes PDF",
            command=self.generar_reportes,
            font=("Arial", 11, "bold"),
            width=22
        )

        boton_pdf.pack(
            side="left",
            padx=5
        )

        boton_mongodb = tk.Button(
            marco_botones,
            text="Guardar en MongoDB",
            command=self.guardar_en_mongodb,
            font=("Arial", 11, "bold"),
            width=20
        )

        boton_mongodb.pack(
            side="left",
            padx=5
        )

        boton_limpiar = tk.Button(
            marco_botones,
            text="Limpiar",
            command=self.limpiar_resultados,
            font=("Arial", 11, "bold"),
            width=12
        )

        boton_limpiar.pack(
            side="left",
            padx=5
        )

        # -------------------------------------------------
        # PESTAÑAS
        # -------------------------------------------------

        self.pestanas = ttk.Notebook(
            self.ventana
        )

        self.pestanas.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=15
        )

        pestana_resumen = tk.Frame(
            self.pestanas
        )

        pestana_tokens = tk.Frame(
            self.pestanas
        )

        pestana_simbolos = tk.Frame(
            self.pestanas
        )

        self.pestanas.add(
            pestana_resumen,
            text="Resumen"
        )

        self.pestanas.add(
            pestana_tokens,
            text="Tokens"
        )

        self.pestanas.add(
            pestana_simbolos,
            text="Tabla de símbolos"
        )

        self.crear_resumen(
            pestana_resumen
        )

        self.crear_tabla_tokens(
            pestana_tokens
        )

        self.crear_tabla_simbolos(
            pestana_simbolos
        )

    # =====================================================
    # PESTAÑA RESUMEN
    # =====================================================

    def crear_resumen(self, contenedor):
        marco_texto = tk.Frame(
            contenedor
        )

        marco_texto.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        barra_vertical = tk.Scrollbar(
            marco_texto
        )

        barra_vertical.pack(
            side="right",
            fill="y"
        )

        self.texto_resumen = tk.Text(
            marco_texto,
            font=("Courier New", 11),
            wrap="word",
            yscrollcommand=barra_vertical.set
        )

        self.texto_resumen.pack(
            side="left",
            fill="both",
            expand=True
        )

        barra_vertical.config(
            command=self.texto_resumen.yview
        )

    # =====================================================
    # PESTAÑA TOKENS
    # =====================================================

    def crear_tabla_tokens(self, contenedor):
        marco_tabla = tk.Frame(
            contenedor
        )

        marco_tabla.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        barra_vertical = tk.Scrollbar(
            marco_tabla,
            orient="vertical"
        )

        barra_vertical.pack(
            side="right",
            fill="y"
        )

        barra_horizontal = tk.Scrollbar(
            marco_tabla,
            orient="horizontal"
        )

        barra_horizontal.pack(
            side="bottom",
            fill="x"
        )

        self.tabla_tokens = ttk.Treeview(
            marco_tabla,
            columns=(
                "linea",
                "token",
                "lexema"
            ),
            show="headings",
            yscrollcommand=barra_vertical.set,
            xscrollcommand=barra_horizontal.set
        )

        self.tabla_tokens.heading(
            "linea",
            text="Línea"
        )

        self.tabla_tokens.heading(
            "token",
            text="Token"
        )

        self.tabla_tokens.heading(
            "lexema",
            text="Lexema"
        )

        self.tabla_tokens.column(
            "linea",
            width=100,
            anchor="center"
        )

        self.tabla_tokens.column(
            "token",
            width=300,
            anchor="center"
        )

        self.tabla_tokens.column(
            "lexema",
            width=450
        )

        self.tabla_tokens.pack(
            side="left",
            fill="both",
            expand=True
        )

        barra_vertical.config(
            command=self.tabla_tokens.yview
        )

        barra_horizontal.config(
            command=self.tabla_tokens.xview
        )

    # =====================================================
    # PESTAÑA TABLA DE SÍMBOLOS
    # =====================================================

    def crear_tabla_simbolos(self, contenedor):
        marco_tabla = tk.Frame(
            contenedor
        )

        marco_tabla.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        barra_vertical = tk.Scrollbar(
            marco_tabla,
            orient="vertical"
        )

        barra_vertical.pack(
            side="right",
            fill="y"
        )

        barra_horizontal = tk.Scrollbar(
            marco_tabla,
            orient="horizontal"
        )

        barra_horizontal.pack(
            side="bottom",
            fill="x"
        )

        self.tabla_simbolos = ttk.Treeview(
            marco_tabla,
            columns=(
                "lexema",
                "token",
                "linea"
            ),
            show="headings",
            yscrollcommand=barra_vertical.set,
            xscrollcommand=barra_horizontal.set
        )

        self.tabla_simbolos.heading(
            "lexema",
            text="Lexema"
        )

        self.tabla_simbolos.heading(
            "token",
            text="Token"
        )

        self.tabla_simbolos.heading(
            "linea",
            text="Línea"
        )

        self.tabla_simbolos.column(
            "lexema",
            width=400
        )

        self.tabla_simbolos.column(
            "token",
            width=300,
            anchor="center"
        )

        self.tabla_simbolos.column(
            "linea",
            width=100,
            anchor="center"
        )

        self.tabla_simbolos.pack(
            side="left",
            fill="both",
            expand=True
        )

        barra_vertical.config(
            command=self.tabla_simbolos.yview
        )

        barra_horizontal.config(
            command=self.tabla_simbolos.xview
        )

    # =====================================================
    # SELECCIONAR ARCHIVO SWIFT
    # =====================================================

    def seleccionar_archivo(self):
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo Swift",
            initialdir=(
                self.raiz_proyecto
                / "ejemplos_swift"
            ),
            filetypes=[
                (
                    "Archivos Swift",
                    "*.swift"
                ),
                (
                    "Todos los archivos",
                    "*.*"
                )
            ]
        )

        if not archivo:
            return

        self.archivo_swift = Path(
            archivo
        )

        self.entrada_ruta.delete(
            0,
            tk.END
        )

        self.entrada_ruta.insert(
            0,
            str(self.archivo_swift)
        )

        self.ultimo_resumen = ""

        self.texto_resumen.delete(
            "1.0",
            tk.END
        )

        self.limpiar_tabla(
            self.tabla_tokens
        )

        self.limpiar_tabla(
            self.tabla_simbolos
        )

    # =====================================================
    # EJECUTAR ANALIZADOR FLEX
    # =====================================================

    def analizar_archivo(self):
        if self.archivo_swift is None:
            messagebox.showwarning(
                "Archivo requerido",
                "Primero seleccione un archivo Swift."
            )
            return

        if not self.archivo_swift.exists():
            messagebox.showerror(
                "Archivo no encontrado",
                "El archivo Swift seleccionado no existe."
            )
            return

        ejecutable = (
            self.raiz_proyecto
            / "analizador"
            / "analizador"
        )

        if not ejecutable.exists():
            messagebox.showerror(
                "Analizador no encontrado",
                "No se encontró el ejecutable del analizador.\n\n"
                "Compile usando:\n\n"
                "flex -o analizador/lex.yy.c "
                "analizador/analizador.l\n\n"
                "gcc analizador/lex.yy.c "
                "-o analizador/analizador -lfl"
            )
            return

        try:
            with self.archivo_swift.open(
                "r",
                encoding="utf-8"
            ) as archivo_entrada:

                proceso = subprocess.run(
                    [str(ejecutable)],
                    stdin=archivo_entrada,
                    capture_output=True,
                    text=True,
                    cwd=self.raiz_proyecto,
                    check=True
                )

            self.ultimo_resumen = (
                proceso.stdout
            )

            self.mostrar_resumen(
                proceso.stdout
            )

            ruta_tokens = (
                self.raiz_proyecto
                / "tokens.txt"
            )

            ruta_simbolos = (
                self.raiz_proyecto
                / "tabla_simbolos.txt"
            )

            self.cargar_tokens(
                ruta_tokens
            )

            self.cargar_simbolos(
                ruta_simbolos
            )

            messagebox.showinfo(
                "Análisis terminado",
                "El archivo Swift fue analizado correctamente."
            )

        except subprocess.CalledProcessError as error:
            mensaje = (
                error.stderr
                or error.stdout
                or "No se pudo ejecutar el analizador."
            )

            messagebox.showerror(
                "Error del analizador",
                mensaje
            )

        except UnicodeDecodeError:
            messagebox.showerror(
                "Error de codificación",
                "El archivo no pudo leerse como UTF-8."
            )

        except OSError as error:
            messagebox.showerror(
                "Error",
                str(error)
            )

    # =====================================================
    # MOSTRAR RESUMEN
    # =====================================================

    def mostrar_resumen(self, contenido):
        marcador = "===== RESUMEN ====="

        if marcador in contenido:
            contenido = (
                marcador
                + contenido.split(
                    marcador,
                    1
                )[1]
            )

        self.texto_resumen.delete(
            "1.0",
            tk.END
        )

        self.texto_resumen.insert(
            tk.END,
            contenido.strip()
        )

    # =====================================================
    # CARGAR TOKENS
    # =====================================================

    def cargar_tokens(self, ruta):
        self.limpiar_tabla(
            self.tabla_tokens
        )

        if not ruta.exists():
            messagebox.showwarning(
                "Tokens no encontrados",
                "No se encontró el archivo tokens.txt."
            )
            return

        with ruta.open(
            "r",
            encoding="utf-8"
        ) as archivo:

            for fila in archivo:
                datos = fila.rstrip(
                    "\n"
                ).split(
                    "\t",
                    2
                )

                if len(datos) != 3:
                    continue

                linea, token, lexema = datos

                self.tabla_tokens.insert(
                    "",
                    tk.END,
                    values=(
                        linea,
                        token,
                        lexema
                    )
                )

    # =====================================================
    # CARGAR TABLA DE SÍMBOLOS
    # =====================================================

    def cargar_simbolos(self, ruta):
        self.limpiar_tabla(
            self.tabla_simbolos
        )

        if not ruta.exists():
            messagebox.showwarning(
                "Tabla no encontrada",
                "No se encontró tabla_simbolos.txt."
            )
            return

        with ruta.open(
            "r",
            encoding="utf-8"
        ) as archivo:

            primera_linea = True

            for fila in archivo:
                datos = fila.rstrip(
                    "\n"
                ).split(
                    "\t",
                    2
                )

                if primera_linea:
                    primera_linea = False

                    if (
                        datos
                        and datos[0]
                        .strip()
                        .lower()
                        .startswith("lexema")
                    ):
                        continue

                if len(datos) != 3:
                    continue

                lexema, token, linea = datos

                self.tabla_simbolos.insert(
                    "",
                    tk.END,
                    values=(
                        lexema,
                        token,
                        linea
                    )
                )

    # =====================================================
    # GENERAR LOS DOS REPORTES PDF
    # =====================================================

    def generar_reportes(self):
        if self.archivo_swift is None:
            messagebox.showwarning(
                "Archivo requerido",
                "Primero seleccione un archivo Swift."
            )
            return

        if not self.ultimo_resumen:
            messagebox.showwarning(
                "Análisis requerido",
                "Primero pulse el botón Analizar archivo."
            )
            return

        try:
            reporte_1, reporte_2 = generar_ambos_reportes(
                self.raiz_proyecto,
                self.archivo_swift,
                self.ultimo_resumen
            )

            messagebox.showinfo(
                "Reportes generados",
                "Los dos reportes PDF fueron generados "
                "correctamente.\n\n"
                f"Reporte 1:\n{reporte_1}\n\n"
                f"Reporte 2:\n{reporte_2}"
            )

        except (
            FileNotFoundError,
            ValueError
        ) as error:
            messagebox.showerror(
                "No se pudieron generar",
                str(error)
            )

        except Exception as error:
            messagebox.showerror(
                "Error al generar PDF",
                str(error)
            )

    # =====================================================
    # GUARDAR TABLA DE SÍMBOLOS EN MONGODB
    # =====================================================

    def guardar_en_mongodb(self):
        if self.archivo_swift is None:
            messagebox.showwarning(
                "Archivo requerido",
                "Primero seleccione un archivo Swift."
            )
            return

        if not self.ultimo_resumen:
            messagebox.showwarning(
                "Análisis requerido",
                "Primero debe analizar el archivo."
            )
            return

        ruta_tabla = (
            self.raiz_proyecto
            / "tabla_simbolos.txt"
        )

        try:
            cantidad = guardar_tabla_simbolos(
                ruta_tabla,
                self.archivo_swift.name
            )

            messagebox.showinfo(
                "MongoDB",
                f"Se guardaron {cantidad} símbolos "
                "correctamente en MongoDB Atlas."
            )

        except FileNotFoundError as error:
            messagebox.showerror(
                "Archivo no encontrado",
                str(error)
            )

        except ValueError as error:
            messagebox.showerror(
                "Datos inválidos",
                str(error)
            )

        except ConnectionError as error:
            messagebox.showerror(
                "Error de conexión",
                str(error)
            )

        except RuntimeError as error:
            messagebox.showerror(
                "Error de MongoDB",
                str(error)
            )

        except Exception as error:
            messagebox.showerror(
                "Error inesperado",
                str(error)
            )

    # =====================================================
    # LIMPIAR INTERFAZ
    # =====================================================

    def limpiar_resultados(self):
        self.archivo_swift = None
        self.ultimo_resumen = ""

        self.entrada_ruta.delete(
            0,
            tk.END
        )

        self.texto_resumen.delete(
            "1.0",
            tk.END
        )

        self.limpiar_tabla(
            self.tabla_tokens
        )

        self.limpiar_tabla(
            self.tabla_simbolos
        )

    # =====================================================
    # LIMPIAR UNA TABLA
    # =====================================================

    @staticmethod
    def limpiar_tabla(tabla):
        for elemento in tabla.get_children():
            tabla.delete(elemento)


# =========================================================
# INICIAR PROGRAMA
# =========================================================

def iniciar_aplicacion():
    ventana = tk.Tk()

    InterfazAnalizador(
        ventana
    )

    ventana.mainloop()


if __name__ == "__main__":
    iniciar_aplicacion()
