from dataclasses import dataclass


from httplib import http

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

    def __init__(self, command: str, path: str, http_ver: http.Version = http.Version.HTTP1) -> None:
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
        # ------proxy-related fields------
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
        self.accept = None
        # ------new fields------
        self.accept_post = None
        self.content_type_options = None
        self.proxy_authorization = None 
        self.access_control_request_headers = None
        self.access_control_request_method = None      
        self.alt_used = None
        self.device_memory = None
        self.downlink = None
        self.early_data = None
        self.ect = None
        self.expect = None
        self.from_ = None
        self.if_match = None
        self.if_range = None
        self.if_unmodified_since = None
        self.forwarded = None
        self.max_forwards = None
        self.origin = None
        self.range = None
        self.rtt = None
        self.save_data = None
        self.sec_ch_prefers_color_scheme = None        
        self.sec_ch_prefers_reduced_motion = None      
        self.sec_ch_prefers_reduced_transparency = None
        self.sec_ch_ua = None
        self.sec_ch_ua_arch = None
        self.sec_ch_ua_bitness = None
        self.sec_ch_ua_full_version = None
        self.sec_ch_ua_full_version_list = None        
        self.sec_ch_ua_mobile = None
        self.sec_ch_ua_model = None
        self.sec_ch_ua_platform = None
        self.sec_ch_ua_platform_version = None
        self.sec_fetch_dest = None
        self.sec_fetch_mode = None
        self.sec_fetch_site = None
        self.sec_fetch_user = None
        self.sec_purpose = None
        self.sec_websocket_accept = None
        self.service_worker_navigation_preload = None
        self.te = None
        self.via = None
        self.viewport_width = None
        self.width = None
        self.x_forwarded_for = None
        self.x_forwarded_host = None
        self.x_forwarded_proto = None
        self.a_im = None
        self.accept_datetime = None
        self.authorization = None
        self.content_encoding = None
        self.content_type = None
        self.content_md5 = None
        self.cookie = None
        self.http2_settings = None
        self.pragma = None
        self.prefer = None
        self.trailer = None
        self.transfer_encoding = None
        self.upgrade = None
        self.warning = None
        self.x_requested_with = None
        self.front_end_https = None
        self.x_http_method_override = None
        self.x_att_deviceid = None
        self.x_wap_profile = None
        self.x_uidh = None
        self.x_csrf_token = None
        self.x_request_id = None
        self.x_correlation_id = None
        self.correlation_id = None
        self.correlation_id = None

    # ------ conn & keep-alive ------
    def set_conn_keep_alive(self) -> None:
        if "close" in self.connection:
            self.connection.remove("close")
        self.connection.add("keep-alive")

    def set_conn_upgrade(self) -> None:
        self.connection.add("upgrade")

    def set_conn_close(self) -> None:
        if "keep-alive" in self.connection:
            self.connection.remove("keep-alive")
        self.connection.add("close")

    def set_keep_alive_max_conn(self, max_conn: int) -> None:
        self.keep_alive["max"] = max_conn

    def set_keep_alive_timeout(self, timeout: int) -> None:
        self.keep_alive["timeout"] = timeout

    # ------accept types------
    def accept_language_add(self, language: str, preference: float = None) -> None:
        self.accept_language[language] = preference

    def accept_charset_add(self, charset: str, preference: float = None) -> None:
        self.accept_charset[charset] = preference

    # ------cache------
    def set_cache_control_max_age(self, duration: int) -> None:
        self.cache_control["max-age"] = duration

    def cache_control_add(self, field: str, param: int) -> None:
        self.cache_control[field] = param

    def set_if_modified_since(self, date_string: str, length: int =0) -> None:
        if not date_string:
            self.if_modified_since = None
        else:
            self.if_modified_since = (http.get_datetime(date_string), length)

    def set_date(self, date_string: str) -> None:
        if not date_string:
            self.date = None
        else:
            self.date = http.get_datetime(date_string)

    # ------proxy------
    def set_proxy_conn_keep_alive(self) -> None:
        if "close" in self.proxy_connection:
            self.proxy_connection.remove("close")
        self.proxy_connection.add("keep-alive")

    def set_proxy_conn_close(self) -> None:
        if "keep-alive" in self.proxy_connection:
            self.proxy_connection.remove("keep-alive")
        self.proxy_connection.add("close")

    def set_proxy_conn_upgrade(self) -> None:
        self.proxy_connection.add("upgrade")

    # ------header line-getters------
    def get_http_str(self) -> None:
        return f"HTTP/{str(self.http_ver)}"

    def get_command_statement(self) -> str:
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

    def get_obj_filename(self) -> str:
        if self.path[-1] == '/':
            return "index.html"
        else:
            rev_path = self.path[::-1]
            filename = rev_path.split('/', 1)[0]
            filename = filename[::-1]
            if "http://" + filename == self.path:  # not an object, but a domain
                return "index.html"
            return filename

    def _line_host(self) -> str:
        return http.format_param("Host", self.host)

    def _line_user_agent(self) -> str:
        return http.format_param("User-Agent", self.user_agent)

    def _line_connection(self) -> str:
        return http.format_param("Connection", self.connection)

    def _line_keep_alive(self) -> str:
        return http.format_param("Keep-Alive",
                                 self.keep_alive if "max" in self.keep_alive
                                 else self.keep_alive["timeout"] if "timeout" in self.keep_alive
                                 else None)

    def _line_referer(self) -> str:
        return http.format_param("Referer", self.referer)

    def _line_accept(self) -> str:
        return http.format_param("Accept", self.accept)

    def _line_accept_language(self) -> str:
        return http.format_param("Accept-Language", self.accept_language, "q")

    def _line_accept_charset(self) -> str:
        return http.format_param("Accept-Charset", self.accept_charset, "q")

    def _line_accept_encoding(self) -> str:
        return http.format_param("Accept-Encoding", self.accept_encoding)

    def _line_cache_control(self) -> str:
        return http.format_param("Cache-Control", self.cache_control)

    def _line_if_modified_since(self) -> str:
        return http.format_param("If-Modified-Since",
                                 (http.get_date_string(self.if_modified_since[0]),
                                  self.if_modified_since[1]) if self.if_modified_since else None,
                                 "length")

    def _line_if_none_match(self) -> str:
        return http.format_param("If-None-Match", self.if_none_match)

    def _line_date(self) -> str:
        return http.format_param("Date", http.get_date_string(self.date) if self.date else None)

    def _line_proxy_connection(self) -> str:
        return http.format_param("Proxy-Connection", self.proxy_connection)

    def _line_ua_pixels(self) -> str:
        return http.format_param("UA-pixels", self.ua_pixels)

    def _line_ua_color(self) -> str:
        return http.format_param("UA-color", self.ua_color)

    def _line_ua_os(self) -> str:
        return http.format_param("UA-OS", self.ua_os)

    def _line_ua_cpu(self) -> str:
        return http.format_param("UA-CPU", self.ua_cpu)

    def _line_dnt(self) -> str:
        return http.format_param("DNT", self.dnt)

    def _line_upgrade_insecure_requests(self) -> str:
        return http.format_param("Upgrade-Insecure-Requests", self.upgrade_insecure_requests)

    def _line_sec_gpc(self) -> str:
        return http.format_param("Sec-GPC", self.sec_gpc)
    
    def _line_content_length(self) -> str:
        return http.format_param("Content-Length", self.content_length)

    def _line_accept_post(self) -> str:
        return http.format_param("Accept-Post", self.accept_post)
    
    def _line_content_type_options(self) -> str:
        return http.format_param("Content-Type-Options", self.content_type_options)
    
    def _line_proxy_authorization(self) -> str:
        return http.format_param("Proxy-Authorization", self.proxy_authorization, None, ";")
    
    def _line_access_control_request_headers(self) -> str:
        return http.format_param("Access-Control-Request-Headers", self.access_control_request_headers)
    
    def _line_access_control_request_method(self) -> str:
        return http.format_param("Access-Control-Request-Method", self.access_control_request_method)
    
    def _line_alt_used(self) -> str:
        return http.format_param("Alt-Used", self.alt_used)
    
    def _line_device_memory(self) -> str:
        return http.format_param("Device-Memory", self.device_memory)
    
    def _line_downlink(self) -> str:
        return http.format_param("Downlink", self.downlink)
    
    def _line_early_data(self) -> str:
        return http.format_param("Early-Data", self.early_data)
    
    def _line_ect(self) -> str:
        return http.format_param("ECT", self.ect)
    
    def _line_expect(self) -> str:
        return http.format_param("Expect", self.expect)
    
    def _line_from_(self) -> str:
        return http.format_param("From", self.from_)
    
    def _line_if_match(self) -> str:
        return http.format_param("If-Match", self.if_match)
    
    def _line_if_range(self) -> str:
        return http.format_param("IF-Range", self.if_range)
    
    def _line_if_unmodified_since(self) -> str:
        return http.format_param("If-Unmodified-Since", self.if_unmodified_since)
    
    def _line_forwarded(self) -> str:
        return http.format_param("Fowarded", self.forwarded)
    
    def _line_max_forwards(self) -> str:
        return http.format_param("Max-Forwards", self.max_forwards)
    
    def _line_origin(self) -> str:
        return http.format_param("Origin", self.origin)
    
    def _line_range(self) -> str:
        return http.format_param("Range", self.range)
    
    def _line_rtt(self) -> str:
        return http.format_param("RTT", self.rtt)
    
    def _line_save_data(self) -> str:
        return http.format_param("Save-Data", self.save_data)
    
    def _line_sec_ch_prefers_color_scheme(self) -> str:
        return http.format_param("Sec-CH-Prefers-Color-Scheme", self.sec_ch_prefers_color_scheme)
    
    def _line_sec_ch_prefers_reduced_motion(self) -> str:
        return http.format_param("Sec-CH-Prefers-Reduced-Motion", self.sec_ch_prefers_reduced_motion)
    
    def _line_sec_ch_prefers_reduced_transparency(self) -> str:
        return http.format_param("Sec-CH-Prefers-Reduced-Transparency", self.sec_ch_prefers_reduced_transparency)
    
    def _line_sec_ch_ua(self) -> str:
        return http.format_param("Sec_CH-UA", self.sec_ch_ua)
    
    def _line_sec_ch_ua_arch(self) -> str:
        return http.format_param("Sec-CH-UA-Arch", self.sec_ch_ua_arch)
    
    def _line_sec_ch_ua_bitness(self) -> str:
        return http.format_param("Sec-CH-UA-Bitness", self.sec_ch_ua_bitness)
    
    def _line_sec_ch_ua_full_version(self) -> str:
        return http.format_param("Sec-CH-UA-Full-Version", self.sec_ch_ua_full_version)
    
    def _line_sec_ch_ua_full_version_list(self) -> str:
        return http.format_param("Sec-CH-UA-Full-Version-List", self.sec_ch_ua_full_version_list)
    
    def _line_sec_ch_ua_mobile(self) -> str:
        return http.format_param("Sec-CH-UA-Mobile", self.sec_ch_ua_mobile)
    
    def _line_sec_ch_ua_model(self) -> str:
        return http.format_param("Sec-CH-UA-Model", self.sec_ch_ua_model)
    
    def _line_sec_ch_ua_platform(self) -> str:
        return http.format_param("Sec-CH-UA-Platform", self.sec_ch_ua_platform)
    
    def _line_sec_ch_ua_platform_version(self) -> str:
        return http.format_param("Sec-CH-UA-Platform-Version", self.sec_ch_ua_platform_version)
    
    def _line_sec_fetch_dest(self) -> str:
        return http.format_param("Sec-Fetch-Dest", self.sec_fetch_dest)
    
    def _line_sec_fetch_mode(self) -> str:
        return http.format_param("Sec-Fetch-Mode", self.sec_fetch_mode)
    
    def _line_sec_fetch_site(self) -> str:
        return http.format_param("Sec-Fetch-Site", self.sec_fetch_site)
    
    def _line_sec_fetch_user(self) -> str:
        return http.format_param("Sec-Fetch-User", self.sec_fetch_user)
    
    def _line_sec_purpose(self) -> str:
        return http.format_param("Sec-Purpose", self.sec_purpose)
    
    def _line_sec_websocket_accept(self) -> str:
        return http.format_param("Sec-Websocket-Accept", self.sec_websocket_accept)
    
    def _line_service_worker_navigation_preload(self) -> str:
        return http.format_param("Service-Worker-Navigation-Preload", self.service_worker_navigation_preload)
    
    def _line_te(self) -> str:
        return http.format_param("TE", self.te)
    
    def _line_via(self) -> str:
        return http.format_param("Via", self.via)
    
    def _line_viewport_width(self) -> str:
        return http.format_param("Viewport-Width", self.viewport_width)
    
    def _line_width(self) -> str:
        return http.format_param("Width", self.width)
    
    def _line_x_forwarded_for(self) -> str:
        return http.format_param("X-Forwarded-For", self.x_forwarded_for)
    
    def _line_x_forwarded_host(self) -> str:
        return http.format_param("X-Forwarded-Host", self.x_forwarded_host)
    
    def _line_x_forwarded_proto(self) -> str:
        return http.format_param("X-Forwarded-Proto", self.x_forwarded_proto)
    
    def _line_a_im(self) -> str:
        return http.format_param("A-IM", self.a_im)
    
    def _line_accept_datetime(self) -> str:
        return http.format_param("Accept-Datetime", self.accept_datetime)
    
    def _line_authorization(self) -> str:
        return http.format_param("Authorization", self.authorization)
    
    def _line_content_encoding(self) -> str:
        return http.format_param("Content-Encoding", self.content_encoding)
    
    def _line_content_type(self) -> str:
        return http.format_param("Content-Type", self.content_type)
    
    def _line_content_md5(self) -> str:
        return http.format_param("Content-MD5", self.content_md5)
    
    def _line_cookie(self) -> str:
        return http.format_param("Cookie", self.cookie)
    
    def _line_http2_settings(self) -> str:
        return http.format_param("HTTP2-Settings", self.http2_settings)
    
    def _line_pragma(self) -> str:
        return http.format_param("Pragma", self.pragma)
    
    def _line_prefer(self) -> str:
        return http.format_param("Prefer", self.prefer)
    
    def _line_trailer(self) -> str:
        return http.format_param("Trailer", self.trailer)
    
    def _line_transfer_encoding(self) -> str:
        return http.format_param("Transfer-Encoding", self.transfer_encoding)
    
    def _line_upgrade(self) -> str:
        return http.format_param("Upgrade", self.upgrade)
    
    def _line_warning(self) -> str:
        return http.format_param("Warning", self.warning)
    
    def _line_x_requested_with(self) -> str:
        return http.format_param("X-Requested-With", self.x_requested_with)
    
    def _line_front_end_https(self) -> str:
        return http.format_param("Front-End-Https", self.front_end_https)
    
    def _line_x_http_method_override(self) -> str:
        return http.format_param("X-Http-Method-Override", self.x_http_method_override)
    
    def _line_x_att_deviceid(self) -> str:
        return http.format_param("X-ATT-DeviceId", self.x_att_deviceid)
    
    def _line_x_wap_profile(self) -> str:
        return http.format_param("X-Wap-Profile", self.x_wap_profile)
    
    def _line_x_uidh(self) -> str:
        return http.format_param("X-UIDH", self.x_uidh)
    
    def _line_x_csrf_token(self) -> str:
        return http.format_param("X-Csrf-Token", self.x_csrf_token)
    
    def _line_x_request_id(self) -> str:
        return http.format_param("X-Request-ID", self.x_request_id)
    
    def _line_x_correlation_id(self) -> str:
        return http.format_param("X-Correlation-ID", self.x_correlation_id)


    def __str__(self) -> str:
        request = [self.get_command_statement()]
        for func in [x for x in dir(self) if x.startswith("_line")]:
            line = getattr(self, func)()
            if line:
                request.append(line)
        request.append(http.DELIMITER)
        return ''.join(request)


def parse_command_line(line: str) -> (str, str, float):
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


def __parse_http_line(line: str, request_obj: Request) -> None:
    try:
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
                res = x.split('=', 1)
                if len(res) > 1:
                    [param, value] = x.split('=', 1)
                    request_obj.cache_control[param.strip()] = value.strip()
                else:
                    request_obj.cache_control[res[0].strip()] = None
        elif keyword == "content_length":
            request_obj.content_length = int(contents.strip())
        elif keyword == "date":
            request_obj.set_date(contents.strip())
        elif keyword == "from":
            request_obj.from_ = contents.strip()
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
    except Exception as e:
        raise ValueError(f"[ERR] Failed to parse HTTP line {line}. {e}")


def parse(request: str) -> Request:
    try:
        if not request:
            raise ValueError("[ERR] Empty request to parse.")
        request = request.split(http.DELIMITER)
        command, path, http_ver = parse_command_line(request[0])
        request_obj = Request(command, path, http_ver)
        for line in request[1:]:
            __parse_http_line(line, request_obj)
        return request_obj
    except Exception as e:
        raise ValueError(f"[ERR] Failed to parse request. {e}")
