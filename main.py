from flask import Flask, render_template, request, flash
import pymysql

app = Flask(__name__)

# Establecer la clave secreta
app.secret_key = 'tu_clave_secreta_unica'

def get_db_connection():
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

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()
    if not conn:
        flash("No se pudo conectar a la base de datos.", "danger")
        return render_template('index.html', asistencias_hoy=[], busqueda='')

    asistencias_hoy = []
    busqueda = ''

    if request.method == 'POST':
        busqueda = request.form.get('busqueda', '').strip()
        
        # Verificar si hay un valor en la búsqueda
        if busqueda:  
            try:
                with conn.cursor() as cursor:
                    # Consulta para entradas (asistencias)
                    cursor.execute(
                        """SELECT e.nombre, e.codigo, e.nie, ent.id_entrada, ent.fecha, ent.hora 
                        FROM entrada ent
                        JOIN estudiantes e ON ent.nie = e.nie 
                        WHERE (e.nie LIKE %s OR e.codigo LIKE %s) 
                        ORDER BY ent.fecha DESC, ent.hora DESC""",
                        ('%' + busqueda + '%', '%' + busqueda + '%')
                    )
                    asistencias_hoy = cursor.fetchall()
                    
                    # Si no hay resultados, mostrar un mensaje
                    if not asistencias_hoy:
                        flash("No se encontraron resultados para la búsqueda.", "warning")

            except Exception as e:
                print(f"Error en la consulta: {str(e)}")
                flash("Error al consultar la base de datos.", "danger")
            finally:
                conn.close()
        else:
            flash("Por favor, ingresa un NIE o Código para buscar.", "warning")

    return render_template('index.html', asistencias_hoy=asistencias_hoy, busqueda=busqueda)

if __name__ == '__main__':
    app.run(debug=True)
