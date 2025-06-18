import os
import requests
import xml.etree.ElementTree as ET

def descargar_archivos_desde_xml(ruta_xml):
    """
    Analiza un archivo XML de DescargaMasiva del INEGI y descarga todos los archivos listados.

    Args:
        ruta_xml (str): La ruta al archivo XML de DescargaMasiva.
    """
    # Directorio para guardar los archivos descargados
    directorio_descarga = "descargas_denue"
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

    print(f"Se encontraron {len(urls_archivos)} archivos para descargar.")

    # Descargar cada archivo
    for url in urls_archivos:
        try:
            # Extraer el nombre del archivo de la URL
            nombre_archivo = url.split('/')[-1]
            ruta_guardado = os.path.join(directorio_descarga, nombre_archivo)

            print(f"Descargando: {nombre_archivo}...")

            # Realizar la solicitud de descarga
            respuesta = requests.get(url, stream=True)
            respuesta.raise_for_status()  # Lanza una excepción para códigos de error HTTP

            # Guardar el archivo en el disco
            with open(ruta_guardado, 'wb') as f:
                for chunk in respuesta.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"Descarga completa: {nombre_archivo}")

        except requests.exceptions.RequestException as e:
            print(f"Error al descargar {url}: {e}")
        except Exception as e:
            print(f"Ocurrió un error inesperado con {url}: {e}")

if __name__ == "__main__":
    # Nombre del archivo XML proporcionado
    archivo_xml = "DescargaMasivaOD.xml"
    
    # Iniciar el proceso de descarga
    descargar_archivos_desde_xml(archivo_xml)
    print("\nProceso de descarga finalizado.")
