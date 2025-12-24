#!/usr/bin/python3
import subprocess
import shutil
import os
import sys

def ejecutar_comando(comando, check=True):
    """Función de ayuda para ejecutar un comando de shell y manejar errores."""
    try:
        print(f"Ejecutando: {' '.join(comando)}")
        resultado = subprocess.run(comando, check=check, capture_output=True, text=True)
        print(resultado.stdout)
        return resultado
    except subprocess.CalledProcessError as e:
        print(f"El comando falló con un error: {e}", file=sys.stderr)
        print(f"Salida de error: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: No se encontró el comando. ¿Está {' '.join(comando[:2])} instalado y en tu PATH?", file=sys.stderr)
        sys.exit(1)

def main():
    """Función principal para manejar los argumentos de línea de comandos y ejecutar las tareas."""
    eliminar_persistencia = False
    if "--remove-persistence" in sys.argv:
        eliminar_persistencia = True
        print("Argumento detectado: --remove-persistence. Se eliminarán los datos persistentes.")

    # Definir los directorios de los que se eliminarán los datos
    directorios_a_limpiar = [
        "/opt/victoriametrics/victoria-metrics-data",
        "/opt/mariadb/data",
        "/opt/grafana/grafana_data",
        "/opt/grafana/provisioning/datasources",
        "/opt/vmalert/rules"
    ]

    # Paso 1: Detener y eliminar el stack de Docker Compose y sus volúmenes
    print("\n--- Paso 1: Deteniendo el stack de Docker Compose y eliminando volúmenes ---")
    ejecutar_comando(["docker", "compose", "down", "-v"])

    # Paso 2: Eliminar condicionalmente los datos persistentes
    if eliminar_persistencia:
        print("\n--- Paso 3: Eliminando datos persistentes de los directorios ---")
        for ruta_directorio in directorios_a_limpiar:
            if os.path.exists(ruta_directorio):
                print(f"Limpiando el contenido de: {ruta_directorio}")
                for elemento in os.listdir(ruta_directorio):
                    ruta_elemento = os.path.join(ruta_directorio, elemento)
                    if os.path.isfile(ruta_elemento) or os.path.islink(ruta_elemento):
                        os.remove(ruta_elemento)
                    elif os.path.isdir(ruta_elemento):
                        shutil.rmtree(ruta_elemento)
                print(f"El contenido de {ruta_directorio} se eliminó correctamente.")
            else:
                print(f"Directorio no encontrado, se omite: {ruta_directorio}")

    print("\n--- Proceso de limpieza finalizado. ---")

if __name__ == "__main__":
    main()
