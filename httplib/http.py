from datetime import datetime
from urllib.parse import urlparse
from dataclasses import dataclass

DELIMITER = "\r\n"
WHITESPACE = ' '

DATE_FORMAT = "%a, %d %b %Y %H:%M:%S GMT"
DEFAULT_USER_AGENT = 'Mozilla/5.0 (compatible; BitHub; Python3)'


@dataclass(frozen=True, slots=True)
class Version:
    HTTP1 = 1.0
    HTTP11 = 1.1
    HTTP2 = 2.0


@dataclass(frozen=True, slots=True)
class Language:
    ENGLISH = 'en'
    ENGLISH_UNITED_STATES = 'en-us'
    ARABIC = 'ar'
    ARABIC_SAUDI_ARABIA = 'ar-sa'


@dataclass(frozen=True, slots=True)
class Encoding:
    ZIP = "zip"
    GZIP = "gzip"
    DEFLATE = "deflate"


@dataclass(frozen=True, slots=True)
class Charset:
    ISO8859 = "iso-8859-1"
    ASCII = "ascii"
    UTF8 = "utf-8"


def get_host(url: str) -> str:
    return urlparse(url).hostname


def get_datetime(date_string: str) -> datetime:
    if not date_string:
        return None
    return datetime.strptime(date_string, DATE_FORMAT)


def get_local_datetime(date_string: str) -> datetime:
    if not date_string:
        return None
    return datetime.strptime(date_string, DATE_FORMAT)


def get_date_string(date_time: datetime) -> str:
    if not date_time:
        return None
    return date_time.strftime(DATE_FORMAT)


def format_param(name: str, param: object, var: str = None) -> str:
    if not param:
        return None
    if param and isinstance(param, str):
        return f"{str(name)}:{WHITESPACE}{str(param)}{DELIMITER}"
    field = [str(name), ":", WHITESPACE]
    if param and isinstance(param, set):
        for x in param:
            field.append(x)
            field.append(',')
            field.append(WHITESPACE)
        field.pop()
        field.pop()
    elif param and isinstance(param, dict):
        if var:
            for x, sp in param.items():
                if sp:
                    field.append(f"{str(x)};{str(var)}={str(sp)}")
                    field.append(',')
                    field.append(WHITESPACE)
                else:
                    field.append(str(x))
                    field.append(',')
                    field.append(WHITESPACE)
        else:
            for x, sp in param.items():
                if sp:
                    field.append(f"{str(x)}={str(sp)}")
                    field.append(',')
                    field.append(WHITESPACE)
                else:
                    field.append(str(x))
                    field.append(',')
                    field.append(WHITESPACE)
        field.pop()
        field.pop()
    elif param and isinstance(param, tuple):
        field.append(str(param[0]))
        if isinstance(param[1], int) and param[1] > 0:
            field.append(';')
            field.append(WHITESPACE)
            field.append(f"{str(var)}={str(param[1])}")
    else:
        field.append(str(param))
    field.append(DELIMITER)
    return ''.join(field)
