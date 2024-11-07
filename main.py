from flask import Flask, render_template, request, flash, jsonify
import pymysql


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Jadelka'

def Conexiondb():
    """Establece la conexión a la base de datos y maneja errores de conexión."""
    try:
        conn = pymysql.connect(
            host='by8ekzvhusvvn2yqc71b-mysql.services.clever-cloud.com',
            database='by8ekzvhusvvn2yqc71b',
            user='uueyyhu8xg3oenlv',
            password='VFbwWo8TNmZQbg04Dd7i'
        )
        print("Conexión exitosa a la base de datos")
        return conn
    except Exception as e:
        print(f"Error de conexión a la base de datos: {str(e)}")
        return None

@app.route('/buscar', methods=['GET'])
def buscar():
    busqueda = request.args.get('busqueda', '').strip()
    print(f"Buscando por: {busqueda}")  # Debugging
    
    if not busqueda:
        return jsonify({"error": "No se ha proporcionado ningún término de búsqueda"}), 400
    
    conn = Conexiondb()
    if not conn:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

    asistencias_hoy2 = []
    salidas_hoy = []

    try:
        with conn.cursor() as cursor:
            # Consultas SQL
            cursor.execute(
                """SELECT e.nombre, e.codigo, e.nie, ent.id_entrada, ent.fecha, ent.hora 
                   FROM entrada ent
                   JOIN estudiantes e ON ent.nie = e.nie 
                   WHERE (e.nie LIKE %s OR e.codigo LIKE %s) 
                   ORDER BY ent.fecha DESC, ent.hora DESC""",
                ('%' + busqueda + '%', '%' + busqueda + '%')
            )
            asistencias_hoy2 = cursor.fetchall()
            print(f"Asistencias: {asistencias_hoy2}")  # Debugging

            cursor.execute(
                """SELECT e.nombre, e.codigo, e.nie, sal.id_salida, sal.fecha, sal.hora 
                   FROM salida sal
                   JOIN estudiantes e ON sal.nie = e.nie 
                   WHERE (e.nie LIKE %s OR e.codigo LIKE %s) 
                   ORDER BY sal.fecha DESC, sal.hora DESC""",
                ('%' + busqueda + '%', '%' + busqueda + '%')
            )
            salidas_hoy = cursor.fetchall()
            print(f"Salidas: {salidas_hoy}")  # Debugging

            if not asistencias_hoy2 and not salidas_hoy:
                flash("No se encontraron registros para la búsqueda.", "info")
            
    except Exception as e:
        print(f"Error en la consulta: {str(e)}")
        flash("Error al consultar la base de datos.", "danger")
    finally:
        conn.close()

    return render_template('index.html', asistencias_hoy=asistencias_hoy2, salidas_hoy=salidas_hoy, busqueda=busqueda)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
