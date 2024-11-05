from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Suponiendo que la URL de la API es la siguiente
API_URL = 'http://127.0.0.1:5000/api/asistencias'  # Cambia esto con la URL correcta de tu API externa

@app.route('/index', methods=['GET', 'POST'])
def index():
    busqueda = request.args.get('busqueda', '').strip()  # Asegúrate de eliminar espacios

    # Hacer la solicitud a la API externa
    try:
        response = requests.get(API_URL, params={'busqueda': busqueda})

        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            data = response.json()  # Recibimos los datos en formato JSON
            asistencias_hoy = data.get("asistencias", [])
            salidas_hoy = data.get("salidas", [])
        else:
            return jsonify({"error": "Error al obtener los datos de la API externa"}), 500
    except requests.exceptions.RequestException as e:
        print(f"Error al hacer la solicitud HTTP: {e}")
        return jsonify({"error": "Error de conexión con la API externa"}), 500

    # Si no hay asistencias ni salidas
    if not asistencias_hoy and not salidas_hoy:
        return jsonify({"message": "No hay registros para la búsqueda realizada."})

    # Pasamos los datos a la plantilla index.html
    return render_template('index.html', asistencias_hoy=asistencias_hoy, salidas_hoy=salidas_hoy, busqueda=busqueda)

if __name__ == '__main__':
    app.run(port=5001, debug=True)
