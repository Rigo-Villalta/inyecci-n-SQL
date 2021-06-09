import os
import sqlite3

import yaml


BASE_DE_DATOS = os.path.join('data', 'database.sqlite')
ARCHIVO_SQL = os.path.join('data', 'declaraciones_sql.yml')


class DatabaseHelper(object):
    def __init__(self):
        self._db_connection = None

    def __enter__(self):
        self._db_connection = sqlite3.connect(BASE_DE_DATOS)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._db_connection.close()

    def crear_tablas(self):
        """
        Creamos la base de datos con las instrucciones que se 
        encuentran en el archivo declaraciones.yml
        """
        with open(ARCHIVO_SQL, 'r+') as f:
            declaraciones = yaml.safe_load(f)

        declaraciones_crear = declaraciones.get('crear', list())

        for s in declaraciones_crear:
            self.insertar(s)

    def eliminar_tablas(self):
        """
        Elimina la base de datos según las instrucciones 
        destruir, dentro del archivo declaraciones.yml
        """
        with open(ARCHIVO_SQL, 'r+') as f:
            declaraciones = yaml.safe_load(f)

        declaraciones_eliminar = declaraciones.get('eliminar', list())

        for s in declaraciones_eliminar:
            self.insertar(s)

    @property
    def cursor(self):
        """
        Retorna una conexión (cursor)
        a la base de datos
        """
        if not self._db_connection:
            self._db_connection = sqlite3.connect(BASE_DE_DATOS)
        return self._db_connection.cursor()

    def reiniciar_base_de_datos(self):
        """
        Elimina y crea nuevamente las tablas dentro de
        la base de datos.
        """
        self.eliminar_tablas()
        self.crear_tablas()

        with open(ARCHIVO_SQL, 'r+') as f:
            declaraciones = yaml.safe_load(f)

        reiniciar_base_de_datos_declaraciones = declaraciones.get('reiniciar', list())

        for s in reiniciar_base_de_datos_declaraciones:
            self.insertar(s)

    def select(self, consulta):
        """
        Ejecuta la consulta en la base de datos
        y lo traslada a cadenas (con el método fetchall())
        """
        cursor = self.cursor
        cursor.execute(consulta)
        return cursor.fetchall()

    def insertar(self, consulta):
        """
        Ejecuta la consulta cruda en la bases de datos
        """
        cursor = self.cursor
        cursor.executescript(consulta)
        self._db_connection.commit()

    def select_safe(self, consulta, params):
        """
        Ejecuta la consulta de forma junto a los
        parámetros (esto lo hace resistente a la inyección SQL)
        """
        cursor = self.cursor
        if params:
            cursor.execute(consulta, params)
        else:
            cursor.execute(consulta)
        return cursor.fetchall()
