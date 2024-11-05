from flask import Flask, request, jsonify
import pymysql
from flask_cors import CORS

app = Flask(__name__, static_folder=None, template_folder=None)
CORS(app)  # Permite solicitudes desde otros dominios

def Conexiondb():
    """Establece la conexión a la base de datos y maneja errores de conexión."""
    try:
        conn = pymysql.connect(
            host='by8ekzvhusvvn2yqc71b-mysql.services.clever-cloud.com',
            database='by8ekzvhusvvn2yqc71b',
            user='uueyyhu8xg3oenlv',
            password='VFbwWo8TNmZQbg04Dd7i'
        )
        return conn
    except Exception as e:
        print(f"Error de conexión a la base de datos: {str(e)}")
        return None

@app.route('/api/asistencias', methods=['GET'])
def asistencias():
    busqueda = request.args.get('busqueda', '').strip()  # Asegúrate de eliminar espacios
    conn = Conexiondb()

    if not conn:
        return jsonify({"error": "Error al conectar con la base de datos"}), 500

    try:
        with conn.cursor() as cursor:
            # Consulta de asistencias (usando LIKE)
            if busqueda:
                cursor.execute(
                    """SELECT e.nombre, e.codigo, e.nie, ent.id_entrada, ent.fecha, ent.hora 
                       FROM entrada ent
                       JOIN estudiantes e ON ent.nie = e.nie 
                       WHERE e.nie LIKE %s OR e.codigo LIKE %s
                       ORDER BY ent.fecha DESC, ent.hora DESC""",
                    ('%' + busqueda + '%', '%' + busqueda + '%')
                )
            else:
                cursor.execute(
                    """SELECT e.nombre, e.codigo, e.nie, ent.id_entrada, ent.fecha, ent.hora 
                       FROM entrada ent
                       JOIN estudiantes e ON ent.nie = e.nie 
                       ORDER BY ent.fecha DESC, ent.hora DESC"""
                )
            asistencias_hoy = cursor.fetchall()

            # Consulta de salidas (usando LIKE)
            if busqueda:
                cursor.execute(
                    """SELECT e.nombre, e.codigo, e.nie, sal.id_salida, sal.fecha, sal.hora 
                       FROM salida sal
                       JOIN estudiantes e ON sal.nie = e.nie 
                       WHERE e.nie LIKE %s OR e.codigo LIKE %s
                       ORDER BY sal.fecha DESC, sal.hora DESC""",
                    ('%' + busqueda + '%', '%' + busqueda + '%')
                )
            else:
                cursor.execute(
                    """SELECT e.nombre, e.codigo, e.nie, sal.id_salida, sal.fecha, sal.hora 
                       FROM salida sal
                       JOIN estudiantes e ON sal.nie = e.nie 
                       ORDER BY sal.fecha DESC, sal.hora DESC"""
                )
            salidas_hoy = cursor.fetchall()

    except Exception as e:
        print(f"Error en la consulta: {str(e)}")
        return jsonify({"error": "Error al consultar la base de datos"}), 500
    finally:
        conn.close()

    # Si no hay asistencias ni salidas
    if not asistencias_hoy and not salidas_hoy:
        return jsonify({"message": "No hay registros para la búsqueda realizada."})

    # Retorna los resultados como JSON
    return jsonify({
        "asistencias": [
            {
                "nombre": a[0],
                "codigo": a[1],
                "nie": a[2],
                "id_entrada": a[3],
                "fecha": a[4],
                "hora": a[5]
            } for a in asistencias_hoy
        ],
        "salidas": [
            {
                "nombre": s[0],
                "codigo": s[1],
                "nie": s[2],
                "id_salida": s[3],
                "fecha": s[4],
                "hora": s[5]
            } for s in salidas_hoy
        ],
        "busqueda": busqueda
    })


if __name__ == '__main__':
    app.run(port=5000, debug=True)
