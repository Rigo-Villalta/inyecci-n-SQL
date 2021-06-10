Proyecto para la demostración de Inyección SQL

Realizado para la Cátedra de Seguridad De Redes
Ciclo 01 - 2021, Universidad Don Bosco.

El proyecto es una aplicación muy básica en [Flask](https://flask.palletsprojects.com), por lo tanto solo
es necesario clonar el repositorio e instalar un entorno virtual de Python,  
las dependencias y correr la aplicación app.py, por ejemplo para el caso de ubuntu en un directorio vacío:

```shell
git clone https://github.com/Rigo-Villalta/inyecci-n-SQL .
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Luego el la cosulta insegura se puede manipular el DOM para poder acceder a otras tablas y/o campos, 
así como insertar sentencias SQL adicionales en el texto del input, por ejemplo:

```SQL
"; drop table estudiantes; /*
```