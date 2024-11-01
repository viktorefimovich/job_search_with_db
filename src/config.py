from configparser import ConfigParser
from pathlib import Path

ROOTPATH = Path(__file__).resolve().parent.parent


def config(filename: str = "database.ini", section: str = "postgresql") -> dict:
    """Чтение параметров для подключения к базе данных"""

    parser = ConfigParser()
    file_path = Path(ROOTPATH, filename)
    parser.read(file_path)

    db_params = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db_params[param[0]] = param[1]
    else:
        raise Exception(f"Section {section} is not found in the {filename} file.")
    return db_params
