# Usa la imagen oficial de Telegraf versión 1.30.0
FROM telegraf:1.30.0

# Instala Python 3, venv y curl
RUN apt-get update && apt-get install -y python3 python3-venv curl

# Crea un entorno virtual y activa el entorno
RUN python3 -m venv /opt/venv

# Instala el paquete 'requests' en el entorno virtual
RUN /opt/venv/bin/pip install requests

# Copia los archivos de configuración
COPY telegraf.conf /etc/telegraf/telegraf.conf
COPY telegraf.d/ /etc/telegraf/telegraf.d/

# El comando por defecto ahora utiliza la versión de python del entorno virtual si es necesario
# Por ejemplo, si un plugin usa python, debe ser invocado con /opt/venv/bin/python
CMD ["--config", "/etc/telegraf/telegraf.conf", "--config-directory", "/etc/telegraf/telegraf.d/"]
