from configparser import ConfigParser


def config(filename: str = "database.ini", section: str = "postgresql") -> dict:
    """Чтение параметров для подключения к базе данных"""

    parser = ConfigParser()
    parser.read(filename)

    db_params = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db_params[param[0]] = param[1]
    else:
        raise Exception("Section {0} is not found in the {1} file.".format(section, filename))
    return db_params
