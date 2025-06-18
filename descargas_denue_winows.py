import os
import requests
import xml.etree.ElementTree as ET

# === RUTAS QUE DEBES MODIFICAR SEGÚN TU NECESIDAD ===
ruta_xml = r"C:\Users\Z574387\OneDrive - Santander Office 365\repo_codigo\denue\DescargaMasivaOD.xml"
directorio_descarga = r"C:\Users\Z574387\Downloads"

# === NO ES NECESARIO CAMBIAR NADA MÁS ABAJO ===

def descargar_archivos_desde_xml():
    """
    Analiza un archivo XML de DescargaMasiva del INEGI y descarga todos los archivos listados.
    Usa rutas definidas dentro del script.
    """

    if not os.path.exists(directorio_descarga):
        os.makedirs(directorio_descarga)
        print(f"Directorio '{directorio_descarga}' creado.")

    try:
        # Analizar el archivo XML
        tree = ET.parse(ruta_xml)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Error al analizar el archivo XML: {e}")
        return
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo XML en la ruta: {ruta_xml}")
        return

    # Encontrar todas las URLs de los archivos
    urls_archivos = [archivo.text for archivo in root.findall('.//Archivo')]

    if not urls_archivos:
        print("No se encontraron URLs de archivos para descargar en el XML.")
        return

    total_archivos = len(urls_archivos)
    print(f"\nSe encontraron {total_archivos} archivos para descargar.\n")

    # Descargar cada archivo
    for i, url in enumerate(urls_archivos, start=1):
        try:
            nombre_archivo = url.split('/')[-1]
            ruta_guardado = os.path.join(directorio_descarga, nombre_archivo)

            print(f"[{i}/{total_archivos}] Descargando: {nombre_archivo}...")

            respuesta = requests.get(url, stream=True)
            respuesta.raise_for_status()

            with open(ruta_guardado, 'wb') as f:
                for chunk in respuesta.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"[{i}/{total_archivos}] ✅ Descarga completa: {nombre_archivo}")

        except requests.exceptions.RequestException as e:
            print(f"[{i}/{total_archivos}] ❌ Error al descargar {nombre_archivo}: {e}")
        except Exception as e:
            print(f"[{i}/{total_archivos}] ⚠️ Ocurrió un error inesperado con {nombre_archivo}: {e}")

if __name__ == "__main__":
    descargar_archivos_desde_xml()
    print("\n✅ Proceso de descarga finalizado.")
