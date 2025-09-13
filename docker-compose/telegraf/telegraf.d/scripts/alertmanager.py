#!/usr/bin/env python3
import requests
import os, sys
import json
from datetime import datetime, timezone
import re

ALERTMANAGER_URL = "http://192.168.1.100:9093/api/v2/alerts"

# Guardar el estado siempre en la misma carpeta que el script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(SCRIPT_DIR, "vmalert.json")

# Tiempo que tiene que pasar para dejar de guardar una alerta restaurada
# Segundos = 10 minutos
RESTORED_TTL = 600

# Funcion para remplazar el valor host de generatorUrl por la IP del servidor para acceder a la alerta por navegador webº
def replace_host_regex(url, new_host):
    pattern = r'^(https?://)[^/:]+(:8880)'
    return re.sub(pattern, lambda m: f'{m.group(1)}{new_host}{m.group(2)}', url)

# Listamos las alertas actuales
def fetch_alerts():
    response = requests.get(ALERTMANAGER_URL, timeout=30)
    data = response.json()
    alertas = []

    for alerta in data:
        # State code para severity
        severity = alerta.get("labels", {}).get("severity", "")
        if severity == "warning":
            severity_code = 1
        elif severity == "critical":
            severity_code = 2
        else:
            severity_code = 0

        # State code para state
        state = alerta.get("status", {}).get("state", "")
        if state == "active":
            state_code = 1
        elif state == "suppressed":
            state_code = 2
        elif state == "resolved":
            state_code = 3
        else:
            state_code = 0

        # Calcular diferencia entre startsAt y updatedAt
        starts_at = datetime.fromisoformat(
            alerta["startsAt"].replace("Z", "+00:00")
        )
        updated_at = datetime.fromisoformat(
            alerta["updatedAt"].replace("Z", "+00:00")
        )
        duration = updated_at - starts_at


        alertas.append({
            "alertid": alerta.get("labels", {}).get("alertid", ""),
            "alertname": alerta.get("labels", {}).get("alertname", ""),
            "alertgroup": alerta.get("labels", {}).get("alertgroup", ""),
            "environment": alerta.get("labels", {}).get("environment", ""),
            "host": alerta.get("labels", {}).get("host", ""),
            "team": alerta.get("labels", {}).get("team", ""),
            "severity": severity,
            "severity_code": severity_code,
            "state": state,
            "state_code": state_code,
            "durationActive": int(duration.total_seconds()),
            "startsAt": alerta.get("startsAt", ""),
            "updatedAt": alerta.get("updatedAt", ""),
            "generatorURL": replace_host_regex(str(alerta.get("generatorURL", "")), "192.168.1.100")
        })
    return alertas


sys.stdout.write(json.dumps(fetch_alerts(), indent=2))
