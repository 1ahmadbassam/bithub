from datetime import datetime


def get_path_from_command_line(line):
    if len(line) < 4:
        return None
    path = []
    i = 0
    while i < len(line) and line[i] == Response.WHITESPACE:
        i += 1
    while i < len(line) and line[i] != '/':
        path.append(line[i])
        i += 1
    i += 1
    return ''.join(path), i


def get_http_version_from_command_line(line, last=0):
    if not line:
        return None
    i = last
    ver = []
    while i < len(line) and line[i] == Response.WHITESPACE:
        i += 1
    while i < len(line) and line[i] != Response.WHITESPACE and line[i] != Response.DELIMITER[0]:
        ver.append(line[i])
        i += 1
    try:
        return float(''.join(ver)), i
    except ValueError:
        return None


def parse_http_line(line: str, obj):
    if not line or not obj:
        return
    keyword, contents = line.removesuffix(Response.DELIMITER).split(':', 1)
    keyword = keyword.lower().strip()
    if keyword == "connection":
        obj.connection = {x.strip() for x in contents.split(',')}
    elif keyword == "proxy-connection":
        obj.proxyConnection = {x.strip() for x in contents.split(',')}
    elif keyword == "keep-alive":
        if ',' not in contents:
            obj.keepAlive["timeout"] = contents.strip()
        else:
            for x in contents.split(','):
                [param, value] = x.split('=', 1)
                obj.keepAlive[param.strip()] = value.strip()
    elif keyword == "server":
        obj.server = contents.strip()
    elif keyword == "accept":
        obj.accept = {x.strip() for x in contents.split(',')}
    elif keyword == "vary":
        obj.vary = {x.strip() for x in contents.split(',')}
    elif keyword == "content-encoding":
        obj.contentEncoding = {x.strip() for x in contents.split(',')}
    elif keyword == "cache-control":
        for x in contents.split(','):
            [param, value] = x.split('=', 1)
            obj.cacheControl[param.strip()] = value.strip()
    elif keyword == "accept-ranges":
        obj.acceptRanges = {x.strip() for x in contents.split(',')}
    elif keyword == "etag":
        obj.etag = contents.strip()
    elif keyword == "content-length":
        obj.contentLength = int(contents.strip())
    elif keyword == "content-type":
        res = contents.split(';', 1)
        if len(res) > 1:
            [content, charset] = res
            charset = charset.split("=")[1:]
            obj.contentType = content.strip()
            obj.contentCharset = {x.strip() for x in charset.split(',')}
        else:
            obj.contentType = contents.strip()
    elif keyword == "access-control-allow-origin":
        obj.accessControlAllowOrigin = {x.strip() for x in contents.split(',')}
    elif keyword == "access-control-allow-methods":
        obj.accessControlAllowMethods = {x.strip() for x in contents.split(',')}
    elif keyword == "content-language":
        obj.contentLanguage = {x.strip() for x in contents.split(',')}
    elif keyword == "pragma":
        obj.pragma = {x.strip() for x in contents.split(',')}
    elif keyword == "www-authenticate":
        res = contents.split(';', 1)
        if len(res) > 1:
            [auth, params] = res
            params = params.split("=")[1:]
            obj.authentications[auth.strip()] = {
                x.strip() for x in params.split(',')}
        else:
            obj.authentications[contents.strip()] = None
    elif keyword == "location":
        obj.location = contents.strip()
    elif keyword == "date":
        obj.date = datetime.strptime(contents.strip(), Response.DATE_FORMAT)
    elif keyword == "last-modified":
        res = contents.split(';', 1)
        if len(res) > 1:
            [date, length] = res
            length = length.split("=")[1]
            obj.lastModified = (datetime.strptime(date.strip(), Response.DATE_FORMAT), int(length))
        else:
            obj.lastModified = (datetime.strptime(contents.strip(), Response.DATE_FORMAT), 0)
    else:
        raise ValueError("Unknown HTTP header field for line " + line)


def get_status(line: str, last=0):
    if not line:
        return None
    status = []
    i = last
    while i < len(line) and line[i] == Response.WHITESPACE:
        i += 1
    while i < len(line) and line[i] != Response.WHITESPACE:
        status.append(line[i])
        i += 1
    try:
        return int(''.join(status)), i
    except ValueError:
        return None


def get_message(line: str, last=0):
    if not line:
        return None
    message = []
    i = last
    while i < len(line) and line[i] == Response.WHITESPACE:
        i += 1
    while i < len(line) and line[i] != Response.DELIMITER[0]:
        message.append(line[i])
        i += 1
    try:
        return ''.join(message)
    except ValueError:
        return None


def parse(res: str):
    if not res:
        return None
    if isinstance(res, bytes):
        res = res.decode(Response.ASCII)
    res = res.split(Response.DELIMITER)
    path, last = get_path_from_command_line(res[0])
    http_ver, last = get_http_version_from_command_line(res[0], last)
    res_status, last = get_status(res[0], last)
    res_message = get_message(res[0], last)
    if not path or not http_ver or not res_status:
        return None
    obj = Response(res_status, res_message, path, http_ver)

    for line in res[1:]:
        parse_http_line(line, obj)
    return obj


def _parse_param_to_header_field(name, params, var=None):
    if not params:
        return None
    if params and isinstance(params, str):
        return f"{str(name)}:{Response.WHITESPACE}{str(params)}{Response.DELIMITER}"
    field = [str(name), ":", Response.WHITESPACE]
    if params and isinstance(params, set):
        for x in params:
            field.append(x)
            field.append(',')
            field.append(Response.WHITESPACE)
        field.pop()
        field.pop()
    elif params and isinstance(params, dict):
        if var:
            for x, sp in params.items():
                if sp:
                    field.append(f"{str(x)};{str(var)}={str(sp)}")
                    field.append(',')
                    field.append(Response.WHITESPACE)
                else:
                    field.append(str(x))
                    field.append(',')
                    field.append(Response.WHITESPACE)
        else:
            for x, sp in params.items():
                field.append(f"{str(x)}={str(sp)}")
                field.append(',')
                field.append(Response.WHITESPACE)
        field.pop()
        field.pop()
    elif params and isinstance(params, tuple):
        field.append(str(params[0]))
        if params[1]:
            field.append(';')
            field.append(Response.WHITESPACE)
            field.append(f"{str(var)}={str(params[1])}")
    else:
        field.append(str(params))
    field.append(Response.DELIMITER)
    return ''.join(field)


class Response:
    GET = 0
    POST = 1
    HEAD = 2
    PUT = 3

    GET_COMMAND = "GET"
    POST_COMMAND = "POST"
    HEAD_COMMAND = "HEAD"
    PUT_COMMAND = "PUT"

    HTTP1 = 1.0
    HTTP11 = 1.1
    HTTP2 = 2.0

    ENGLISH = 'en'
    ENGLISH_UNITED_STATES = 'en-us'
    ARABIC = 'ar'
    ARABIC_SAUDI_ARABIA = 'ar-sa'

    ZIP = "zip"
    GZIP = "gzip"
    DEFLATE = "deflate"

    ISO8859 = "iso-8859-1"
    ASCII = "ascii"
    UTF8 = "utf-8"

    DELIMITER = "\r\n"
    WHITESPACE = ' '

    DATE_FORMAT = "%a, %d %b %Y %H:%M:%S GMT"

    def __init__(self, res_status, res_message, path, http_ver=HTTP1):
        self.resStatus = res_status
        self.resMessage = res_message
        self.path = path
        self.httpVer = http_ver
        self.server = None
        self.connection = {"close"}
        self.keepAlive = {}
        self.acceptRanges = set()
        self.etag = None
        self.contentLength = None
        self.contentType = None
        self.contentLanguage = {}
        self.contentCharset = {}
        self.contentEncoding = set()
        self.cacheControl = {}
        self.proxyConnection = set()
        self.date = None
        self.lastModified = None
        self.accept = set()
        self.vary = set()
        self.accessControlAllowMethods = set()
        self.accessControlAllowOrigin = set()
        self.pragma = set()
        self.authentications = {}
        self.location = None

    def set_server(self, new_server):
        self.server = new_server

    def set_path(self, new_path):
        self.path = new_path

    def set_keep_alive_connection(self):
        if "close" in self.connection:
            self.connection.remove("close")
        self.connection.add("keep-alive")

    def set_keep_alive_timeout(self, timeout):
        self.keepAlive["timeout"] = timeout

    def set_keep_alive_max(self, max):
        self.keepAlive["max"] = max

    def set_close_connection(self):
        if "keep-alive" in self.connection:
            self.connection.remove("keep-alive")
        self.connection.add("close")

    def add_connection_field(self, field):
        self.connection.add(field)

    def remove_connection_field(self, field):
        if field in self.connection:
            self.connection.remove(field)

    def add_accept_mime(self, mime_type):
        self.accept.add(mime_type)

    def add_content_language(self, language: str, q: float = None):
        self.contentLanguage[language] = q

    def add_content_charset(self, charset: str, q: float = None):
        self.contentCharset[charset] = q

    def add_content_encoding(self, encoding):
        self.contentEncoding.add(encoding)

    def remove_content_mime(self, mime_type):
        if mime_type in self.accept:
            self.accept.remove(mime_type)

    def remove_content_language(self, language):
        if language in self.contentLanguage:
            self.contentLanguage.pop(language)

    def remove_accept_charset(self, charset):
        if charset in self.contentCharset:
            self.contentCharset.pop(charset)

    def add_access_control_allow_method(self, method):
        self.accessControlAllowMethods.add(method)

    def remove_access_control_allow_method(self, method):
        if method in self.accessControlAllowMethods:
            self.accessControlAllowMethods.remove(method)

    def add_access_control_allow_origin(self, origin):
        self.accessControlAllowOrigin.add(origin)

    def remove_access_control_allow_origin(self, origin):
        if origin in self.accessControlAllowOrigin:
            self.accessControlAllowOrigin.remove(origin)

    def set_keep_alive_proxy_connection(self):
        if "close" in self.proxyConnection:
            self.proxyConnection.remove("close")
        self.proxyConnection.add("keep-alive")

    def set_close_proxy_connection(self):
        if "keep-alive" in self.proxyConnection:
            self.proxyConnection.remove("keep-alive")
        self.proxyConnection.add("close")

    def add_proxy_connection_field(self, field):
        self.proxyConnection.add(field)

    def remove_proxy_connection_field(self, field):
        if field in self.proxyConnection:
            self.proxyConnection.remove(field)

    def set_cache_control_max_age(self, duration):
        self.cacheControl["max-age"] = duration

    def set_cache_control_field(self, field, param):
        self.cacheControl[field] = param

    def set_date(self, date_string):
        if not date_string:
            self.date = None
        else:
            self.date = datetime.strptime(date_string, Response.DATE_FORMAT)

    def set_last_modified(self, date_string, length=0):
        if not date_string:
            self.lastModifiedSince = None
        else:
            self.lastModifiedSince = (datetime.strptime(
                date_string, Response.DATE_FORMAT), length)

    def add_accept_range(self, range):
        self.acceptRanges.add(range)

    def remove_accept_range(self, range):
        if range in self.acceptRanges:
            self.acceptRanges.remove(range)

    def set_content_length(self, length):
        self.contentLength = length

    def set_content_type(self, mime_type):
        self.contentType = mime_type

    def add_vary(self, field):
        self.vary.add(field)

    def remove_vary(self, field):
        if field in self.vary:
            self.vary.remove(field)

    def set_etag(self, new_etag):
        self.etag = new_etag

    def add_pragma(self, new_pragma):
        self.pragma.add(new_pragma)

    def remove_pragma(self, new_pragma):
        if new_pragma in self.pragma:
            self.pragma.remove(new_pragma)

    def set_location(self, new_location):
        self.location = new_location

    def add_authentication(self, field, param):
        self.authentications[field] = param

    def remove_authentication(self, field):
        if field in self.authentications:
            self.authentications.pop(field)

    def get_http_version(self):
        return f"HTTP/{str(self.httpVer)}"

    def get_http_response_line(self):
        return f"{self.get_http_version()} {self.resStatus} {self.resMessage}{Response.DELIMITER}"

    def get_server_line(self):
        return _parse_param_to_header_field("Server", self.server)

    def get_connection_line(self):
        return _parse_param_to_header_field("Connection", self.connection)

    def get_proxy_connection_line(self):
        if self.proxyConnection:
            return _parse_param_to_header_field("Proxy-Connection", self.proxyConnection)
        else:
            return None

    def get_cache_control_line(self):
        return _parse_param_to_header_field("Cache-Control", self.cacheControl)

    def get_accept_line(self):
        return _parse_param_to_header_field("Accept", self.accept)

    def get_accept_ranges_line(self):
        return _parse_param_to_header_field("Accept-Ranges", self.acceptRanges)

    def get_content_length_line(self):
        return _parse_param_to_header_field("Content-Length", self.contentLength)

    def get_content_type_line(self):
        return _parse_param_to_header_field("Content-Type", self.contentType)

    def get_content_language_line(self):
        return _parse_param_to_header_field("Content-Language", self.contentLanguage, "q")

    def get_content_charset_line(self):
        return _parse_param_to_header_field("Content-Charset", self.contentCharset, "q")

    def get_content_encoding_line(self):
        return _parse_param_to_header_field("Content-Encoding", self.contentEncoding)

    def get_date_line(self):
        return _parse_param_to_header_field("Date", self.date.strftime(Response.DATE_FORMAT))

    def get_last_modified_line(self):
        return _parse_param_to_header_field("Last-Modified",
                                            (self.lastModified[0].strftime(Response.DATE_FORMAT),
                                             self.lastModified[1] if self.lastModified[1] > 0 else None),
                                            "length")

    def get_vary_line(self):
        return _parse_param_to_header_field("Vary", self.vary)

    def get_access_control_allow_origin_line(self):
        return _parse_param_to_header_field("Access-Control-Allow-Origin", self.accessControlAllowOrigin)

    def get_access_control_allow_methods_line(self):
        return _parse_param_to_header_field("Access-Control-Allow-Methods", self.accessControlAllowMethods)

    def get_pragma_line(self):
        return _parse_param_to_header_field("Pragma", self.pragma)

    def get_etag_line(self):
        return _parse_param_to_header_field("ETag", self.etag)

    def get_keep_alive_line(self):
        return _parse_param_to_header_field("Keep-Alive", self.keepAlive)

    def get_authentication_line(self):
        return _parse_param_to_header_field("Authentication", self.authentications)

    def get_location_line(self):
        return _parse_param_to_header_field("Location", self.location)

    def __str__(self):
        response = [self.get_http_response_line(), self.get_server_line(),
                    self.get_connection_line()]
        if self.keepAlive:
            response.append(self.get_keep_alive_line())
        if self.proxyConnection:
            response.append(self.get_proxy_connection_line())
        if self.cacheControl:
            response.append(self.get_cache_control_line())
        if self.accept:
            response.append(self.get_accept_line())
        if self.acceptRanges:
            response.append(self.get_accept_ranges_line())
        if self.contentLength:
            response.append(self.get_content_length_line())
        if self.contentType:
            response.append(self.get_content_type_line())
        if self.contentLanguage:
            response.append(self.get_content_language_line())
        if self.contentCharset:
            response.append(self.get_content_charset_line())
        if self.contentEncoding:
            response.append(self.get_content_encoding_line())
        if self.date:
            response.append(self.get_date_line())
        if self.lastModified:
            response.append(self.get_last_modified_line())
        if self.vary:
            response.append(self.get_vary_line())
        if self.accessControlAllowOrigin:
            response.append(self.get_access_control_allow_origin_line())
        if self.accessControlAllowMethods:
            response.append(self.get_access_control_allow_methods_line())
        if self.pragma:
            response.append(self.get_pragma_line())
        if self.etag:
            response.append(self.get_etag_line())
        if self.authentications:
            response.append(self.get_authentication_line())
        if self.location:
            response.append(self.get_location_line())
        response.append(Response.DELIMITER)
        return ''.join(response)
