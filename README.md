# vmagmonitor
Este repositorio contiene la configuración y los archivos necesarios para desplegar un stack de monitorización de infraestructura y servicios. La solución está construida con componentes de código abierto que trabajan en conjunto para ofrecer una solución completa y eficiente.

## Componentes
### VictoriaMetrics
Un sistema de monitorización y almacenamiento de series temporales, rápido y escalable, que actúa como el motor principal para la recolección y consulta de métricas. Es una alternativa optimizada y compatible con Prometheus, destacando por su bajo uso de recursos y alto rendimiento.

### Grafana 
Una plataforma de observabilidad y visualización de datos que te permite crear paneles de control interactivos y personalizables. Con Grafana, puedes analizar las métricas almacenadas en VictoriaMetrics de forma intuitiva, facilitando la toma de decisiones y el diagnóstico de problemas.

### VMalert
Un motor de alertas que evalúa reglas de alerta basadas en las métricas recopiladas. Este componente permite notificar automáticamente a los equipos de operación cuando se detectan anomalías o umbrales de rendimiento.

### Telegraf
Un agente de recolección de métricas que recopila datos de una amplia variedad de fuentes (sistemas, servicios, bases de datos, etc.). Telegraf envía las métricas de manera eficiente a VictoriaMetrics, asegurando que tengas una visión completa del estado de tu infraestructura.

## Requerimientos previsos
Para desplegar este stack de monitorización, es necesario tener instalado **Docker** y **Docker Compose** en tu sistema.

### Preparación del entorno
Antes de iniciar los servicios, debes crear los directorios necesarios para el almacenamiento persistente de datos. Esto es crucial para que la información no se pierda al reiniciar los contenedores.
Ejecuta los siguientes comandos en tu terminal:
```bash
# Directorios para los datos de VictoriaMetrics, MariaDB, Grafana y las reglas de vmalert
sudo mkdir -p /opt/victoriametrics/victoria-metrics-data
sudo mkdir -p /opt/mariadb/data
sudo mkdir -p /opt/grafana/grafana_data
sudo mkdir -p /opt/grafana/provisioning/datasources
sudo mkdir -p /opt/vmalert/rules
```

### Configuración de permisos
Para que Grafana pueda escribir en sus directorios de datos y provisionamiento, es necesario ajustar los permisos. El usuario interno de Grafana tiene el ID 472.
Ejecuta estos comandos para asignar los permisos correctos:
```bash
# Asignar permisos al usuario de Grafana para sus directorios de datos
sudo chown -R 472:472 /opt/grafana/grafana_data
sudo chown -R 472:472 /opt/grafana/provisioning/datasources
```

## Agregar datasource a Grafana
Agrega el datasource de VictoriaMetrics a Grafana por defecto.

**victoriametrics-datasource.yml**
```yml
apiVersion: 1
datasources:
  - name: victoriametrics
    type: VictoriaMetrics
    url: http://victoriametrics:8428
    isDefault: true
    access: proxy
    version: 1
    editable: false
```

### Despliegue del Stack
Una vez que tengas los directorios y los permisos configurados, ya puedes iniciar el stack. 
Navega hasta el directorio donde tengas tu archivo docker-compose.yml y ejecuta:
```bash
docker compose up -d --build --force-recreate
```
Este comando descargará las imágenes necesarias y levantará todos los servicios en segundo plano.

## Eliminar el stack 
Para detener el stack, eliminar volúmenes y eliminar la imagen telegraf que se genera a partir del `docker compose up -d` ejecuta:
```bash
./vmag-clean.py
```
Para realizar las acciones anteriores más la eliminación de los datos persistentes de los directorios especificados, ejecuta:
```bash
sudo ./vmag-clean.py --remove-persistence
```
