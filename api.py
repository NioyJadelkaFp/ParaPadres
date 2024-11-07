from flask import Flask, jsonify, request
import pymysql

# ... (resto del código, incluyendo la función Conexiondb)

app = Flask(__name__)

@app.route('/asistencias', methods=['GET'])
def get_asistencias():
    conn = Conexiondb()
    if not conn:
        return jsonify({'error': 'Error de conexión a la base de datos'}), 500

    try:
        nie = request.args.get('nie')
        codigo = request.args.get('codigo')
        # ... otros parámetros

        with conn.cursor() as cursor:
            # Consulta adaptada a los parámetros de la API
            cursor.execute("""
                SELECT e.nombre, e.codigo, e.nie, ent.id_entrada, ent.fecha, ent.hora 
                FROM entrada ent
                JOIN estudiantes e ON ent.nie = e.nie 
                WHERE (e.nie LIKE %s OR e.codigo LIKE %s)
                # ... agregar condiciones para otros parámetros
            """, (f'%{nie}%' if nie else '%', f'%{codigo}%' if codigo else '%'))
            asistencias = cursor.fetchall()
            return jsonify(asistencias)
    except Exception as e:
        print(f"Error en la consulta: {str(e)}")
        return jsonify({'error': 'Error al consultar la base de datos'}), 500
    finally:
        conn.close()

# Ruta para /salidas similar a /asistencias

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=500, debug=True)