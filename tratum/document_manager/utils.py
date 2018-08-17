
def get_static_path(scheme, host, static):
    """Retorna un string formateado con la URL absoluta de un estático o ruta dada.
    """

    return '{scheme}://{host}{static}'.format(scheme=scheme,host=host,static=static)