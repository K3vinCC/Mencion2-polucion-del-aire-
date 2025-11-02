#!/usr/bin/env python3
import secrets, json, sys, os, tempfile, shutil

# --- Validar argumentos ---
if len(sys.argv) < 2:
    print("Uso: sudo add_device.py <device_id>")
    sys.exit(2)

device_id = sys.argv[1]
devices_file = "/etc/miapp/devices.json"
os.makedirs(os.path.dirname(devices_file), exist_ok=True)

# --- Generar clave segura ---
device_secret = secrets.token_hex(32)  # 32 bytes -> 64 caracteres hex

# --- Cargar archivo existente ---
if os.path.exists(devices_file):
    with open(devices_file, "r") as f:
        try:
            devices = json.load(f)
        except Exception:
            devices = {}
else:
    devices = {}

# --- Verificar si ya existe ---
if device_id in devices:
    print(f"ERROR: {device_id} ya existe en {devices_file}")
    sys.exit(1)

# --- AÃ±adir nuevo dispositivo ---
devices[device_id] = device_secret

# --- Guardar archivo de forma segura ---
fd, tmp = tempfile.mkstemp(dir=os.path.dirname(devices_file))
with os.fdopen(fd, "w") as f:
    json.dump(devices, f, indent=2)
shutil.move(tmp, devices_file)

# --- Establecer permisos seguros ---
#os.chown(devices_file, 0, 0)
os.chmod(devices_file, 0o600)

# --- Mostrar clave generada ---
print(f"… Dispositivo '{device_id}' agregado con exito")
print(f"Device secret para firmware: {device_secret}")
