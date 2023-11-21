from datetime import datetime

from httplib import http


def parse_response_line(line: str) -> tuple:
    [http_ver, status_code, status_phrase] = line.split(http.WHITESPACE, 2)
    http_ver = float(http_ver.split('/')[1])
    return status_code, status_phrase, http_ver


def __parse_http_line(line: str, obj):
    if not line or not obj:
        return
    keyword, contents = line.removesuffix(http.DELIMITER).split(':', 1)
    keyword = keyword.lower().strip()
    if keyword == "connection":
        obj.connection = {x.strip() for x in contents.split(',')}
    elif keyword == "proxy-connection":
        obj.proxyConnection = {x.strip() for x in contents.split(',')}
    elif keyword == "keep-alive":
        if ',' not in contents:
            obj.keep_alive["timeout"] = contents.strip()
        else:
            for x in contents.split(','):
                [param, value] = x.split('=', 1)
                obj.keep_alive[param.strip()] = value.strip()
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
            charset = charset.split("=")[1:][0]
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
    elif keyword == "x-frame-options":
        obj.xFrameOptions = contents.strip()
    elif keyword == "x-xss-protection":
        obj.xXSSProtection = contents.strip()
    elif keyword == "www-authenticate":
        res = contents.split(';', 1)
        if len(res) > 1:
            [auth, params] = res
            params = params.split("=")[1:]
            obj.authentications[auth.strip()] = {
                x.strip() for x in params.split(',')}
        else:
            obj.authentications[contents.strip()] = None
    elif keyword == "upgrade":
        obj.upgrade = {x.strip() for x in contents.split(',')}
    elif keyword == "location":
        obj.location = contents.strip()
    elif keyword == "date":
        obj.date = datetime.strptime(contents.strip(), http.DATE_FORMAT)
    elif keyword == "last-modified":
        res = contents.split(';', 1)
        if len(res) > 1:
            [date, length] = res
            length = length.split("=")[1]
            obj.lastModified = (datetime.strptime(date.strip(), http.DATE_FORMAT), int(length))
        else:
            obj.lastModified = (datetime.strptime(contents.strip(), http.DATE_FORMAT), 0)
    else:
        raise ValueError("Unknown HTTP header field for line " + line)


def parse(res: str):
    if not res:
        return None
    if isinstance(res, bytes):
        res = res.decode(http.Charset.ASCII)
    res = res.split(http.DELIMITER)
    res_status, res_message, http_ver = parse_response_line(res[0])
    if not res_status or not res_message:
        return None
    obj = Response(res_status, res_message, http_ver)

    for line in res[1:]:
        __parse_http_line(line, obj)
    return obj



class Response:
    def __init__(self, status_code, status_phrase, http_ver=http.Version.HTTP1):
        # ------common http response fields------
        self.status_code = status_code
        self.status_phrase = status_phrase
        self.http_ver = http_ver
        self.server = None
        self.connection = {"close"}
        self.keep_alive = {}
        self.etag = None
        # ------content-related response fields------
        self.accept = set()
        self.accept_ranges = set()
        self.content_length = None
        self.content_type = None
        self.content_language = {}
        self.content_charset = {} ####################################
        self.content_encoding = set()
        # ------cache-related response fields------
        self.cache_control = {}
        self.date = None
        self.last_modified = None
        # ------proxy-related field------
        self.proxy_connection = set()
        # ------fields used by modern browsers------
        self.access_control_allow_methods = set()
        self.access_control_allow_origin = set()
        self.upgrade = set()
        self.vary = set()
        self.pragma = set()
        self.authentications = {}
        self.location = None
        self.x_xss_protection = None
        self.x_frame_options = None

    # ------ conn & keep-alive ------
    def set_conn_keep_alive(self):
        if "close" in self.connection:
            self.connection.remove("close")
        self.connection.add("keep-alive")

    def set_conn_upgrade(self):
        self.connection.add("upgrade")

    def set_conn_close(self):
        if "keep-alive" in self.connection:
            self.connection.remove("keep-alive")
        self.connection.add("close")

    def set_keep_alive_max_conn(self, max_conn: int):
        self.keep_alive["max"] = max_conn

    def set_keep_alive_timeout(self, timeout: int):
        self.keep_alive["timeout"] = timeout

    # ------cache------
    def set_cache_control_max_age(self, duration: int):
        self.cache_control["max-age"] = duration
    
    def set_cache_control_field(self, field: str, param: str):
        self.cache_control[field] = param

    def set_last_modified(self, date_string: str, length=0):
        if not date_string:
            self.last_modified = None
        else:
            self.last_modified = (http.get_datetime(date_string), length)

    def set_date(self, date_string: str):
        if not date_string:
            self.date = None
        else:
            self.date = http.get_datetime(date_string)

    # ------content------
    def set_content_length(self, length: int):
        self.content_length = length

    def set_content_type(self, mime_type: str):
        self.content_type = mime_type

    def set_content_language(self, language: str, preference: float = None):
        self.content_language[language] = preference

    def set_content_charset(self, charset: str, preference: float = None):
        self.content_charset[charset] = preference

    def set_content_encoding(self, encoding: str):
        self.content_encoding.add(encoding)

    # ------access control------
    def add_access_control_allow_method(self, method: str):
        self.access_control_allow_methods.add(method)

    def add_access_control_allow_origin(self, origin: str):
        self.access_control_allow_origin.add(origin)

    # ------proxy------
    def set_proxy_conn_keep_alive(self):
        if "close" in self.proxy_connection:
            self.proxy_connection.remove("close")
        self.proxy_connection.add("keep-alive")

    def set_proxy_conn_close(self):
        if "keep-alive" in self.proxy_connection:
            self.proxy_connection.remove("keep-alive")
        self.proxy_connection.add("close")

    def set_proxy_conn_upgrade(self):
        self.proxy_connection.add("upgrade")

    # ------other fields------
    def set_x_xss_protection(self, value):
        self.x_xss_protection = value

    def set_x_xss_protection_mode_block(self):
        self.x_xss_protection = "1; mode=block"

    def set_x_xss_protection_report_uri(self, uri):
        self.x_xss_protection = f"1; report={uri}"

    def set_x_frame_options(self, option):
        if option.lower().strip() == "deny":
            self.x_frame_options = None
        else:
            self.x_frame_options = option

    def _line_http_version(self):
        return f"HTTP/{str(self.http_ver)}"

    def _line_http_response(self):
        return f"{self._line_http_version()} {self.status_code} {self.status_phrase}{http.DELIMITER}"

    def _line_server(self):
        return http.format_param("Server", self.server)

    def _line_connection(self):
        return http.format_param("Connection", self.connection)

    def _line_proxy_connection(self):
        if self.proxy_connection:
            return http.format_param("Proxy-Connection", self.proxy_connection)
        else:
            return None

    def _line_cache_control(self):
        return http.format_param("Cache-Control", self.cache_control)

    def _line_accept(self):
        return http.format_param("Accept", self.accept)

    def _line_accept_ranges(self):
        return http.format_param("Accept-Ranges", self.accept_ranges)

    def _line_content_length(self):
        return http.format_param("Content-Length", self.content_length)

    def _line_content_type(self):
        return http.format_param("Content-Type", self.content_type)

    def _line_content_language(self):
        return http.format_param("Content-Language", self.content_language, "q")

    def _line_content_charset(self):
        return http.format_param("Content-Charset", self.content_charset, "q")

    def _line_content_encoding(self):
        return http.format_param("Content-Encoding", self.content_encoding)

    def _line_date_line(self):
        return http.format_param("Date", self.date.strftime(http.DATE_FORMAT))

    def _line_last_modified(self):
        return http.format_param("Last-Modified",
                                            (self.last_modified[0].strftime(http.DATE_FORMAT),
                                             self.last_modified[1] if self.last_modified[1] > 0 else None),
                                            "length")

    def _line_vary(self):
        return http.format_param("Vary", self.vary)

    def _line_access_control_allow_origin(self):
        return http.format_param("Access-Control-Allow-Origin", self.access_control_allow_origin)

    def _line_access_control_allow_methods(self):
        return http.format_param("Access-Control-Allow-Methods", self.access_control_allow_methods)

    def _line_pragma_line(self):
        return http.format_param("Pragma", self.pragma)

    def _line_etag_line(self):
        return http.format_param("ETag", self.etag)

    def _line_keep_alive_line(self):
        return http.format_param("Keep-Alive", self.keep_alive)

    def _line_authentications(self):
        return http.format_param("Authentication", self.authentications)

    def _line_location(self):
        return http.format_param("Location", self.location)

    def _line_xframe_options(self):
        return http.format_param("X-Frame-Options", self.x_frame_options)

    def _line_x_xss_protection(self):
        return http.format_param("X-XSS-Protection", self.x_xss_protection)

    def _line_upgrade(self):
        return http.format_param("Upgrade", self.upgrade)

    def __str__(self):
        response = [self._line_http_response(), self._line_server(), self._line_connection()]
        for func in [x for x in dir(self) if x.startswith("_line")]:
            line = getattr(self, func)()
            if line:
                response.append(line)
        response.append(http.DELIMITER)
        return ''.join(response)
