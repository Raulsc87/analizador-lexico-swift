import os
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError

# Rutas del proyecto
RAIZ_PROYECTO = Path(__file__).resolve().parent.parent
load_dotenv(RAIZ_PROYECTO / ".env")

# Datos de MongoDB
NOMBRE_BASE_DATOS = "analizador_swift"
NOMBRE_COLECCION = "tabla_simbolos"


# Obtener conexión con MongoDB
def obtener_coleccion():
    uri = os.getenv("MONGODB_URI")

    if not uri:
        raise ValueError(
            "No se encontró MONGODB_URI dentro del archivo .env."
        )

    cliente = MongoClient(
        uri,
        serverSelectionTimeoutMS=5000
    )

    cliente.admin.command("ping")

    base_datos = cliente[NOMBRE_BASE_DATOS]
    coleccion = base_datos[NOMBRE_COLECCION]

    return cliente, coleccion


# Leer tabla de símbolos
def leer_tabla_simbolos(ruta_tabla):
    ruta_tabla = Path(ruta_tabla)

    if not ruta_tabla.exists():
        raise FileNotFoundError(
            "No se encontró tabla_simbolos.txt."
        )

    simbolos = []

    with ruta_tabla.open("r", encoding="utf-8") as archivo:
        primera_linea = True

        for fila in archivo:
            datos = fila.rstrip("\n").split("\t", 2)

            # Ignorar encabezado
            if primera_linea:
                primera_linea = False

                if (
                    datos
                    and datos[0].strip().lower().startswith("lexema")
                ):
                    continue

            if len(datos) != 3:
                continue

            lexema, token, linea = datos

            try:
                linea = int(linea.strip())

            except ValueError:
                linea = linea.strip()

            simbolos.append(
                {
                    "lexema": lexema.strip(),
                    "token": token.strip(),
                    "linea": linea
                }
            )

    return simbolos


# Guardar tabla de símbolos
def guardar_tabla_simbolos(ruta_tabla, nombre_archivo):
    simbolos = leer_tabla_simbolos(ruta_tabla)

    if not simbolos:
        raise ValueError(
            "La tabla de símbolos está vacía."
        )

    cliente = None

    try:
        cliente, coleccion = obtener_coleccion()

        # Eliminar datos anteriores del mismo archivo
        coleccion.delete_many(
            {
                "archivo": nombre_archivo
            }
        )

        fecha_actual = datetime.now(timezone.utc)

        documentos = []

        for simbolo in simbolos:
            documentos.append(
                {
                    "archivo": nombre_archivo,
                    "lexema": simbolo["lexema"],
                    "token": simbolo["token"],
                    "linea": simbolo["linea"],
                    "fecha_analisis": fecha_actual
                }
            )

        # Guardar nuevos datos
        resultado = coleccion.insert_many(documentos)

        return len(resultado.inserted_ids)

    except PyMongoError as error:
        raise RuntimeError(
            f"Error al guardar en MongoDB: {error}"
        ) from error

    finally:
        if cliente is not None:
            cliente.close()


# Probar conexión
def probar_conexion():
    cliente = None

    try:
        cliente, _ = obtener_coleccion()

        print(
            "Conexión correcta con MongoDB Atlas."
        )

    finally:
        if cliente is not None:
            cliente.close()


# Ejecutar prueba
if __name__ == "__main__":
    probar_conexion()