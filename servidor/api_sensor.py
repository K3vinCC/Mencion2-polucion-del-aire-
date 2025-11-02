from flask import Flask, request, jsonify
import json
import jwt # Necesitaras instalar PyJWT: pip install PyJWT
import datetime
from functools import wraps

app = Flask(__name__)

# --- CONFIGURACION DE SEGURIDAD ---

with open('/etc/miapp_secret', 'r') as f:
    app.config['SECRET_KEY'] = f.read().strip()


# Las credenciales deben coincidir EXACTAMENTE con las del ESP32.
# Cargar dispositivos desde archivo seguro
with open('/etc/miapp/devices.json', 'r') as f:
    AUTHORIZED_DEVICES = json.load(f)


# --- DECORADOR PARA PROTEGER RUTAS ---
# Este decorador actua como un "guardia de seguridad" para los endpoints.
# Revisa si hay un token valido antes de permitir el acceso.
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # El token se espera en la cabecera 'Authorization' con el formato 'Bearer <token>'
        if 'Authorization' in request.headers:
            try:
                token = request.headers['Authorization'].split(" ")[1]
            except IndexError:
                return jsonify({'message': 'Formato de token invalido'}), 401

        if not token:
            return jsonify({'message': 'Token no encontrado'}), 401

        try:
            # Decodifica el token usando la SECRET_KEY
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_device_id = data['sub']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'El token ha expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token invalido'}), 401
        
        # Pasa el ID del dispositivo decodificado a la funcion del endpoint
        return f(current_device_id, *args, **kwargs)
    return decorated


# --- ENDPOINT DE AUTENTICACION ---
# Aqui es donde el ESP32 viene a pedir su "pase de acceso" (el token)
@app.route('/login', methods=['POST'])
def login():
    auth_data = request.json
    device_id = auth_data.get('device_id')
    device_secret = auth_data.get('device_secret')

    # Verifica si el dispositivo y su clave secreta son correctos
    if device_id and device_secret and AUTHORIZED_DEVICES.get(device_id) == device_secret:
        # Si las credenciales son validas, crea un token que expira en 24 horas
        token = jwt.encode({
            'sub': device_id,
            'iat': datetime.datetime.utcnow(), # Issued At Time
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, app.config['SECRET_KEY'], algorithm="HS256")

        return jsonify({'token': token})

    # Si las credenciales son incorrectas, deniega el acceso
    return jsonify({'message': 'No se pudo verificar'}), 401, {'WWW-Authenticate': 'Basic realm="Login required!"'}


# --- ENDPOINT PROTEGIDO PARA RECIBIR DATOS ---
# Gracias a @token_required, esta funcion solo se ejecutara si el token es valido
@app.route('/datos', methods=['POST'])
@token_required
def recibir_datos(current_device_id):
    # 'current_device_id' nos lo pasa el decorador despues de validar el token
    print(f"Recibiendo datos del dispositivo autorizado: {current_device_id}")
    
    sensor_data = request.json
    print("Datos recibidos:", sensor_data)
    
    # --- AQUI VA TU LOGICA ---
    # Por ejemplo, guardar los datos en tu base de datos GraphQL.
    # Ya puedes confiar en que estos datos vienen de un dispositivo verificado.
    
    return jsonify({"status": "ok", "message": "Datos recibidos correctamente"})


# --- EJECUCION DEL SERVIDOR ---
if __name__ == "__main__":
    # Usa host='0.0.0.0' para que el servidor sea accesible desde otros dispositivos en la red
    # El puerto debe estar abierto en tu router/firewall
    app.run(host="0.0.0.0", port=8000)
