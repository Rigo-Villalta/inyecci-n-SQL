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
        tabla = request.form.get('tabla_seleccionada', '')
        with DatabaseHelper() as database:
            consulta = 'SELECT * FROM {0} WHERE nombre LIKE "%{1}%";'.format(tabla, busqueda)
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
    forma se evita la inyección SQL y es segura
    """
    if request.method == 'GET':
        return render_template('consulta_segura.html')
    if request.method == 'POST':
        busqueda = '%' + request.form.get('busqueda', '') + '%'
        tabla = request.form.get('tabla_seleccionada', '')
        with DatabaseHelper() as database:
            consulta = 'SELECT * FROM {0} WHERE nombre LIKE ?;'.format(tabla)
            # Este método hace la diferencia en cuanto a una consulta
            resultados = database.select_safe(consulta, (busqueda,))
            valores_retornados = list()
            for resultado in resultados:
                valores_retornados.append(str(resultado))
            return '<br>'.join(valores_retornados)


if __name__ == '__main__':
    app.run()
