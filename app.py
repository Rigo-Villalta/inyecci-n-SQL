from flask import Flask, render_template, request, redirect

from controlador_bd import restaurar_base_de_datos
from database import DatabaseHelper


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/restaurar-base-de-datos/')
def reiniciar_base_de_datos():
    restaurar_base_de_datos()
    return redirect(request.referrer, 302)


@app.route('/consulta-insegura/', methods=['GET', 'POST'])
def consulta_insegura():
    """
    Con este método se realiza una consulta cruda a la Base de datos
    lo cual da lugar a una posible inyección SQL
    """
    if request.method == 'GET':
        return render_template('consulta_insegura.html')
    if request.method == 'POST':
        busqueda = request.form.get('busqueda', '')
        campo = request.form.get('campo', '')
        tabla = request.form.get('tabla_seleccionada', '')
        with DatabaseHelper() as database:
            consulta = 'SELECT * FROM {0} WHERE {1} LIKE "%{2}%";'.format(tabla, campo, busqueda)
            database.insertar(consulta)
            resultados = database.select(consulta)
            valores_retornados = list()
            for resultado in resultados:
                valores_retornados.append(str(resultado))
            return '<br>'.join(valores_retornados)


@app.route('/consulta-segura/', methods=['GET', 'POST'])
def consulta_safe():
    """
    Aquí por el contrario realizamos la consulta con parámetros, de esta
    forma se evita la inyección SQL y los caracteres especiales son escapados
    sin embargo se puede realizar la inyección al manipular el DOM.
    """
    if request.method == 'GET':
        return render_template('consulta_segura.html')
    if request.method == 'POST':
        busqueda = '%' + request.form.get('busqueda', '') + '%' 
        campo = request.form.get('campo', '')
        tabla = request.form.get('tabla_seleccionada', '')
        if (
            tabla == 'estudiantes' and (campo == 'nombre' or campo == 'carnet')
            ) or (
            tabla == 'materias' and (campo == 'nombre' or campo == 'codigo')
                ):
            with DatabaseHelper() as database:
                consulta = 'SELECT * FROM {0} WHERE nombre LIKE ?;'.format(tabla)
                # Este método hace la diferencia en cuanto a una consulta
                resultados = database.select_safe(consulta, (busqueda,))
                valores_retornados = list()
                for resultado in resultados:
                    valores_retornados.append(str(resultado))
                return '<br>'.join(valores_retornados)
        else:
            return 'No puede ingresar un campo o tabla inválido. <br><h5>No manipule el DOM </h5><br><p>Este incidente será reportado al administrador del sistema</p>'


if __name__ == '__main__':
    app.run()
