# Usa la imagen oficial de Telegraf versión 1.30.0
FROM telegraf:1.30.0

# Instala Python 3, venv, curl, vim y which
RUN apt-get update && apt-get install -y \
    python3 \
    python3-venv \
    curl \
    vim \
    which \
 && rm -rf /var/lib/apt/lists/*

# Crea un entorno virtual y activa el entorno
RUN python3 -m venv /opt/venv

# Instala el paquete 'requests' en el entorno virtual
RUN /opt/venv/bin/pip install requests

# Añadir alias ll
RUN echo "alias ll='ls -l --color=auto'" >> /root/.bashrc

# Copia los archivos de configuración
COPY telegraf.conf /etc/telegraf/telegraf.conf
COPY telegraf.d/ /etc/telegraf/telegraf.d/

# El comando por defecto ahora utiliza la versión de python del entorno virtual si es necesario
CMD ["--config", "/etc/telegraf/telegraf.conf", "--config-directory", "/etc/telegraf/telegraf.d/"]
