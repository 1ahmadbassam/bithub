from dataclasses import dataclass


from httplib import http


def parse_command_line(line: str) -> tuple:
    [command_str, path, http_ver] = line.split(http.WHITESPACE, 2)
    http_ver = float(http_ver.strip().split('/')[1])
    command_str = command_str.strip()
    if command_str == Request.Command.GET_KEYWORD:
        command = Request.Command.GET
    elif command_str == Request.Command.POST_KEYWORD:
        command = Request.Command.POST
    elif command_str == Request.Command.HEAD_KEYWORD:
        command = Request.Command.HEAD
    elif command_str == Request.Command.PUT_KEYWORD:
        command = Request.Command.PUT
    else:
        raise ValueError(f"[ERR] Unrecognized HTTP command {command_str}.")
    return command, path.strip(), http_ver


def __parse_http_line(line: str, request_obj):
    if not line or not request_obj:
        return
    keyword, contents = line.removesuffix(http.DELIMITER).split(':', 1)
    keyword = keyword.lower().strip().replace('-', '_')
    if keyword == "keep_alive":
        if ',' not in contents:
            request_obj.keep_alive["timeout"] = contents.strip()
        else:
            for x in contents.split(','):
                [param, value] = x.split('=', 1)
                request_obj.keep_alive[param.strip()] = value.strip()
    elif keyword == "cache_control":
        for x in contents.split(','):
            [param, value] = x.split('=', 1)
            request_obj.cache_control[param.strip()] = value.strip()
    elif keyword == "date":
        request_obj.set_date(contents.strip())
    elif keyword == "if_modified_since":
        res = contents.split(';', 1)
        if len(res) > 1:
            [date, length] = res
            length = length.split("=")[1]
            request_obj.if_modified_since = (http.get_datetime(date.strip()), int(length))
        else:
            request_obj.if_modified_since = (http.get_datetime(res[0].strip()), 0)
    else:
        try:
            class_var = getattr(request_obj, keyword)
            if isinstance(class_var, set):
                setattr(request_obj, keyword, {x.strip() for x in contents.split(',')})
            elif keyword == "accept_language" or keyword == "accept_encoding":
                for x in contents.split(','):
                    var = x.split(';q=')
                    if len(var) > 1:
                        [lang, perf] = var
                        class_var[lang.strip()] = float(perf.strip())
                    else:
                        class_var[var[0].strip()] = None
            elif isinstance(class_var, dict):
                return
            else:
                setattr(request_obj, keyword, contents.strip())
        except AttributeError:
            raise ValueError(f"[ERR] Unknown HTTP header field for keyword {keyword}.")


def parse(request: str):
    if not request:
        raise ValueError("[ERR] Empty request to parse.")
    request = request.split(http.DELIMITER)
    command, path, http_ver = parse_command_line(request[0])
    request_obj = Request(command, path, http_ver)
    for line in request[1:]:
        __parse_http_line(line, request_obj)
    return request_obj


class Request:
    @dataclass(frozen=True, slots=True)
    class Command:
        GET = 0
        POST = 1
        HEAD = 2
        PUT = 3

        GET_KEYWORD = "GET"
        POST_KEYWORD = "POST"
        HEAD_KEYWORD = "HEAD"
        PUT_KEYWORD = "PUT"

    def __init__(self, command: str, path: str, http_ver=http.Version.HTTP1):
        # ------common http request fields------
        self.command = command
        self.path = path
        self.http_ver = http_ver
        self.host = http.get_host(path)
        self.user_agent = http.DEFAULT_USER_AGENT
        self.connection = {"close"}
        self.keep_alive = {}
        self.referer = None
        # ------content-related request fields------
        self.accept = set()
        self.content_length = None
        self.accept_language = {}
        self.accept_charset = {}
        self.accept_encoding = set()
        # ------cache-related request fields------
        self.cache_control = {}
        self.if_modified_since = None
        self.if_none_match = set()
        self.date = None
        # ------proxy-related field------
        self.proxy_connection = set()
        # ------fields used by older browsers------
        self.ua_pixels = None
        self.ua_color = None
        self.ua_os = None
        self.ua_cpu = None
        # ------fields used by modern browsers------
        self.dnt = None
        self.upgrade_insecure_requests = None
        self.sec_gpc = None

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

    # ------accept types------
    def accept_language_add(self, language: str, preference: float = None):
        self.accept_language[language] = preference

    def accept_charset_add(self, charset: str, preference: float = None):
        self.accept_charset[charset] = preference

    # ------cache------
    def set_cache_control_max_age(self, duration: int):
        self.cache_control["max-age"] = duration

    def cache_control_add(self, field: str, param: int):
        self.cache_control[field] = param

    def set_if_modified_since(self, date_string: str, length=0):
        if not date_string:
            self.if_modified_since = None
        else:
            self.if_modified_since = (http.get_datetime(date_string), length)

    def set_date(self, date_string: str):
        if not date_string:
            self.date = None
        else:
            self.date = http.get_datetime(date_string)

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

    # ------header line-getters------
    def get_http_str(self):
        return f"HTTP/{str(self.http_ver)}"

    def get_command_statement(self):
        command_statement = []
        if self.command == Request.Command.GET:
            command_statement.append(Request.Command.GET_KEYWORD)
        elif self.command == Request.Command.POST:
            command_statement.append(Request.Command.POST_KEYWORD)
        elif self.command == Request.Command.HEAD:
            command_statement.append(Request.Command.HEAD_KEYWORD)
        elif self.command == Request.Command.PUT:
            command_statement.append(Request.Command.PUT_KEYWORD)
        else:
            raise ValueError("[ERR] Unimplemented command statement.")
        command_statement.append(http.WHITESPACE)
        command_statement.append(self.path)
        command_statement.append(http.WHITESPACE)
        command_statement.append(self.get_http_str())
        command_statement.append(http.DELIMITER)
        return ''.join(command_statement)

    def get_obj_filename(self):
        if self.path[-1] == '/':
            return "index.html"
        else:
            rev_path = self.path[::-1]
            filename = rev_path.split('/', 1)[0]
            filename = filename[::-1]
            if "http://" + filename == self.path:  # not an object, but a domain
                return "index.html"
            return filename

    def _line_host(self):
        return http.format_param("Host", self.host)

    def _line_user_agent(self):
        return http.format_param("User-Agent", self.user_agent)

    def _line_connection(self):
        return http.format_param("Connection", self.connection)

    def _line_keep_alive(self):
        return http.format_param("Keep-Alive",
                                 self.keep_alive if "max" in self.keep_alive
                                 else self.keep_alive["timeout"] if "timeout" in self.keep_alive
                                 else None)

    def _line_referer(self):
        return http.format_param("Referer", self.referer)

    def _line_accept(self):
        return http.format_param("Accept", self.accept)

    def _line_accept_language(self):
        return http.format_param("Accept-Language", self.accept_language, "q")

    def _line_accept_charset(self):
        return http.format_param("Accept-Charset", self.accept_charset, "q")

    def _line_accept_encoding(self):
        return http.format_param("Accept-Encoding", self.accept_encoding)

    def _line_cache_control(self):
        return http.format_param("Cache-Control", self.cache_control)

    def _line_if_modified_since(self):
        return http.format_param("If-Modified-Since",
                                 (http.get_date_string(self.if_modified_since[0]),
                                  self.if_modified_since[1]) if self.if_modified_since else None,
                                 "length")

    def _line_if_none_match(self):
        return http.format_param("If-None-Match", self.if_none_match)

    def _line_date(self):
        return http.format_param("Date", http.get_date_string(self.date))

    def _line_proxy_connection(self):
        return http.format_param("Proxy-Connection", self.proxy_connection)

    def _line_ua_pixels(self):
        return http.format_param("UA-pixels", self.ua_pixels)

    def _line_ua_color(self):
        return http.format_param("UA-color", self.ua_color)

    def _line_ua_os(self):
        return http.format_param("UA-OS", self.ua_os)

    def _line_ua_cpu(self):
        return http.format_param("UA-CPU", self.ua_cpu)

    def _line_dnt(self):
        return http.format_param("DNT", self.dnt)

    def _line_upgrade_insecure_requests(self):
        return http.format_param("Upgrade-Insecure-Requests", self.upgrade_insecure_requests)

    def _line_sec_gpc(self):
        return http.format_param("Sec-GPC", self.sec_gpc)
    
    def _line_content_length(self):
        return http.format_param("Content-Length", self.content_length)

    def __str__(self):
        request = [self.get_command_statement()]
        for func in [x for x in dir(self) if x.startswith("_line")]:
            line = getattr(self, func)()
            if line:
                request.append(line)
        request.append(http.DELIMITER)
        return ''.join(request)
