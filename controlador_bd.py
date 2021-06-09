from database import DatabaseHelper


def restaurar_base_de_datos():
    """
    Ejecutamos la utilizadad de Python para
    ejecutar una instrucción en la base de datos
    """
    with DatabaseHelper() as db:
        db.reiniciar_base_de_datos()
