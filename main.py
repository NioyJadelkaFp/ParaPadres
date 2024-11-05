from flask import Flask, render_template, request, flash
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

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = Conexiondb()
    if not conn:
        flash("No se pudo conectar a la base de datos.", "danger")
        return render_template('index.html', asistencias_hoy=[], salidas_hoy=[], busqueda='')

    asistencias_hoy2 = []
    salidas_hoy = []
    busqueda = ''

    if request.method == 'POST':
        busqueda = request.form.get('busqueda', '').strip()
        print(f"Buscando por: {busqueda}")
        
        if busqueda:
            try:
                with conn.cursor() as cursor:
                    # Consulta para entradas
                    cursor.execute(
                        """SELECT e.nombre, e.codigo, e.nie, ent.id_entrada, ent.fecha, ent.hora 
                           FROM entrada ent
                           JOIN estudiantes e ON ent.nie = e.nie 
                           WHERE (e.nie LIKE %s OR e.codigo LIKE %s) 
                           ORDER BY ent.fecha DESC, ent.hora DESC""",
                        ('%' + busqueda + '%', '%' + busqueda + '%')
                    )
                    asistencias_hoy2 = cursor.fetchall()
                    print(f"Resultados de asistencias: {asistencias_hoy2}")

                    # Consulta para salidas
                    cursor.execute(
                        """SELECT e.nombre, e.codigo, e.nie, sal.id_salida, sal.fecha, sal.hora 
                           FROM salida sal
                           JOIN estudiantes e ON sal.nie = e.nie 
                           WHERE (e.nie LIKE %s OR e.codigo LIKE %s) 
                           ORDER BY sal.fecha DESC, sal.hora DESC""",
                        ('%' + busqueda + '%', '%' + busqueda + '%')
                    )
                    salidas_hoy = cursor.fetchall()
                    print(f"Resultados de salidas: {salidas_hoy}")

                    # Mensaje si no hay resultados
                    if not asistencias_hoy2 and not salidas_hoy:
                        flash("No se encontraron registros para la búsqueda.", "info")

            except Exception as e:
                print(f"Error en la consulta: {str(e)}")
                flash("Error al consultar la base de datos.", "danger")
            finally:
                conn.close()  # Asegúrate de cerrar la conexión después de usarla
        else:
            flash("Por favor, ingresa un NIE o Código para buscar.", "warning")

    return render_template('index.html', asistencias_hoy=asistencias_hoy2, salidas_hoy=salidas_hoy, busqueda=busqueda)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
