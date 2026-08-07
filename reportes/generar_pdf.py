from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)


def crear_estilos():
    estilos = getSampleStyleSheet()

    estilos.add(
        ParagraphStyle(
            name="TituloCentrado",
            parent=estilos["Title"],
            alignment=TA_CENTER,
            fontSize=18,
            spaceAfter=18
        )
    )

    estilos.add(
        ParagraphStyle(
            name="Subtitulo",
            parent=estilos["Heading2"],
            fontSize=13,
            spaceBefore=10,
            spaceAfter=8
        )
    )

    return estilos


def extraer_resumen(texto_resumen):
    """
    Recibe todo el texto producido por Flex y obtiene únicamente
    las líneas que aparecen después de '===== RESUMEN ====='.
    """

    marcador = "===== RESUMEN ====="

    if marcador not in texto_resumen:
        return []

    parte_resumen = texto_resumen.split(marcador, 1)[1]

    datos = []

    for linea in parte_resumen.splitlines():
        linea = linea.strip()

        if not linea or ":" not in linea:
            continue

        nombre, valor = linea.split(":", 1)

        datos.append(
            (
                nombre.strip(),
                valor.strip()
            )
        )

    return datos


def leer_tokens(ruta_tokens):
    tokens = []

    if not ruta_tokens.exists():
        return tokens

    with ruta_tokens.open("r", encoding="utf-8") as archivo:
        for fila in archivo:
            datos = fila.rstrip("\n").split("\t", 2)

            if len(datos) != 3:
                continue

            linea, token, lexema = datos

            tokens.append(
                {
                    "linea": linea,
                    "token": token,
                    "lexema": lexema
                }
            )

    return tokens


def leer_simbolos(ruta_simbolos):
    simbolos = []

    if not ruta_simbolos.exists():
        return simbolos

    with ruta_simbolos.open("r", encoding="utf-8") as archivo:
        # Se omite la primera línea porque es el encabezado.
        next(archivo, None)

        for fila in archivo:
            datos = fila.rstrip("\n").split("\t", 2)

            if len(datos) != 3:
                continue

            lexema, token, linea = datos

            simbolos.append(
                {
                    "lexema": lexema,
                    "token": token,
                    "linea": linea
                }
            )

    return simbolos


def contar_palabras_reservadas(tokens):
    """
    Cuenta tokens que corresponden a palabras reservadas conocidas.
    Esta lista puede ampliarse conforme Diego agregue más palabras
    reservadas de Swift al archivo analizador.l.
    """

    reservadas = {
        "VAR",
        "LET",
        "IF",
        "ELSE",
        "FOR",
        "WHILE",
        "FUNC",
        "RETURN",
        "CLASS",
        "STRUCT",
        "SWITCH",
        "CASE",
        "DEFAULT",
        "BREAK",
        "CONTINUE",
        "IMPORT",
        "IN",
        "DO",
        "CATCH",
        "THROW",
        "TRY",
        "ENUM",
        "PROTOCOL",
        "EXTENSION",
        "PUBLIC",
        "PRIVATE",
        "INTERNAL",
        "STATIC"
    }

    conteo = {}

    for elemento in tokens:
        token = elemento["token"]
        lexema = elemento["lexema"]

        if token in reservadas:
            conteo[lexema] = conteo.get(lexema, 0) + 1

    return sorted(
        conteo.items(),
        key=lambda elemento: elemento[1],
        reverse=True
    )


def generar_reporte_estadisticas(
    ruta_salida,
    nombre_archivo,
    texto_resumen,
    tokens
):
    estilos = crear_estilos()

    documento = SimpleDocTemplate(
        str(ruta_salida),
        pagesize=letter,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm
    )

    contenido = []

    contenido.append(
        Paragraph(
            "Reporte 1 - Estadísticas del análisis",
            estilos["TituloCentrado"]
        )
    )

    contenido.append(
        Paragraph(
            f"Archivo analizado: {nombre_archivo}",
            estilos["Normal"]
        )
    )

    contenido.append(Spacer(1, 14))

    contenido.append(
        Paragraph(
            "Resumen general",
            estilos["Subtitulo"]
        )
    )

    datos_resumen = extraer_resumen(texto_resumen)

    tabla_resumen = [
        ["Categoría", "Cantidad"]
    ]

    for nombre, valor in datos_resumen:
        tabla_resumen.append([nombre, valor])

    tabla = Table(
        tabla_resumen,
        colWidths=[10 * cm, 4 * cm],
        repeatRows=1
    )

    tabla.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ALIGN", (1, 1), (1, -1), "CENTER"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 1), (-1, -1), 6)
            ]
        )
    )

    contenido.append(tabla)
    contenido.append(Spacer(1, 18))

    contenido.append(
        Paragraph(
            "Palabras reservadas encontradas",
            estilos["Subtitulo"]
        )
    )

    palabras = contar_palabras_reservadas(tokens)

    tabla_palabras = [
        ["Palabra reservada", "Cantidad"]
    ]

    if palabras:
        for palabra, cantidad in palabras:
            tabla_palabras.append([palabra, cantidad])
    else:
        tabla_palabras.append(
            ["No se encontraron palabras reservadas", "0"]
        )

    tabla_reservadas = Table(
        tabla_palabras,
        colWidths=[10 * cm, 4 * cm],
        repeatRows=1
    )

    tabla_reservadas.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ALIGN", (1, 1), (1, -1), "CENTER"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6)
            ]
        )
    )

    contenido.append(tabla_reservadas)

    documento.build(contenido)


def generar_reporte_tokens(
    ruta_salida,
    nombre_archivo,
    tokens,
    simbolos
):
    estilos = crear_estilos()

    documento = SimpleDocTemplate(
        str(ruta_salida),
        pagesize=landscape(letter),
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm
    )

    contenido = []

    contenido.append(
        Paragraph(
            "Reporte 2 - Lexemas y tabla de símbolos",
            estilos["TituloCentrado"]
        )
    )

    contenido.append(
        Paragraph(
            f"Archivo analizado: {nombre_archivo}",
            estilos["Normal"]
        )
    )

    contenido.append(Spacer(1, 14))

    contenido.append(
        Paragraph(
            "Lexemas encontrados",
            estilos["Subtitulo"]
        )
    )

    tabla_tokens = [
        ["No.", "Línea", "Token", "Lexema"]
    ]

    for numero, elemento in enumerate(tokens, start=1):
        tabla_tokens.append(
            [
                numero,
                elemento["linea"],
                elemento["token"],
                elemento["lexema"]
            ]
        )

    tabla_lexemas = Table(
        tabla_tokens,
        colWidths=[
            1.5 * cm,
            2 * cm,
            7 * cm,
            12 * cm
        ],
        repeatRows=1
    )

    tabla_lexemas.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ALIGN", (0, 1), (1, -1), "CENTER"),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4)
            ]
        )
    )

    contenido.append(tabla_lexemas)
    contenido.append(PageBreak())

    contenido.append(
        Paragraph(
            "Tabla de símbolos",
            estilos["Subtitulo"]
        )
    )

    tabla_simbolos = [
        ["No.", "Lexema", "Token", "Línea"]
    ]

    for numero, simbolo in enumerate(simbolos, start=1):
        tabla_simbolos.append(
            [
                numero,
                simbolo["lexema"],
                simbolo["token"],
                simbolo["linea"]
            ]
        )

    tabla = Table(
        tabla_simbolos,
        colWidths=[
            1.5 * cm,
            9 * cm,
            8 * cm,
            3 * cm
        ],
        repeatRows=1
    )

    tabla.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ALIGN", (0, 1), (0, -1), "CENTER"),
                ("ALIGN", (3, 1), (3, -1), "CENTER"),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5)
            ]
        )
    )

    contenido.append(tabla)

    documento.build(contenido)


def generar_ambos_reportes(
    raiz_proyecto,
    nombre_archivo,
    texto_resumen
):
    raiz_proyecto = Path(raiz_proyecto)

    ruta_tokens = raiz_proyecto / "tokens.txt"
    ruta_simbolos = raiz_proyecto / "tabla_simbolos.txt"
    carpeta_salida = raiz_proyecto / "pdf_generados"

    carpeta_salida.mkdir(exist_ok=True)

    tokens = leer_tokens(ruta_tokens)
    simbolos = leer_simbolos(ruta_simbolos)

    if not tokens:
        raise FileNotFoundError(
            "No se encontraron datos en tokens.txt. "
            "Primero debe analizar un archivo Swift."
        )

    reporte_1 = carpeta_salida / "reporte_estadisticas.pdf"
    reporte_2 = carpeta_salida / "reporte_lexemas_simbolos.pdf"

    generar_reporte_estadisticas(
        reporte_1,
        nombre_archivo,
        texto_resumen,
        tokens
    )

    generar_reporte_tokens(
        reporte_2,
        nombre_archivo,
        tokens,
        simbolos
    )

    return reporte_1, reporte_2
