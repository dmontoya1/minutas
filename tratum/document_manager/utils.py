
def get_static_path(scheme, host, static):
    """Retorna un string formateado con la URL absoluta de un estático o ruta dada.
    """
    return "{0}://{1}{2}".format(scheme, host, static)
