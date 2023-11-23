from httplib import http

class Response:

    def __init__(self, status_code: int, status_phrase: str, http_ver: http.Version = http.Version.HTTP1) -> None:
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
        self.accept_charset = set()
        self.accept_encoding = set()
        self.accept_language = set()
        self.accept_patch = set()
        self.accept_post = set()
        self.content_length = None
        self.content_type = None
        self.content_language = {}
        self.content_charset = {}
        self.content_encoding = set()
        self.content_type_options = set()
        self.content_security_policy = {}
        self.x_content_type_options = None
        # ------cache-related response fields------
        self.cache_control = {}
        self.date = None
        self.last_modified = None
        # ------proxy-related fields------
        self.proxy_connection = set()
        self.proxy_authenticate = set()
        self.proxy_authorization = {}
        # ------fields used by modern browsers------
        self.access_control_allow_methods = set()
        self.access_control_allow_origin = set()
        self.upgrade = set()
        self.vary = set()
        self.pragma = set()
        self.www_authenticate = {}
        self.location = None
        self.x_xss_protection = None
        self.x_frame_options = None
        self.expect_ct = set()
        self.x_powered_by = None
        self.x_ua_compatible = None
        self.x_content_duration = None
        self.x_webkit_csp = {}
        self.x_content_type_options = None
        self.accept_ch = None
        self.accept_ch_lifetime = None
        self.non_standard_deprecated = None
        self.age = None
        self.allow = set()
        self.alt_svc = {}
        self.alt_used = None
        self.authorization = None
        self.clear_site_data = set()
        self.content_disposition = None
        self.content_dpr = None
        self.content_location = None
        self.content_range = None
        self.critical_ch = None
        self.experimental = None
        self.device_memory = None
        self.digest = None
        self.deprecated = None
        self.dnt = None
        self.downlink = None
        self.dpr = None
        self.early_data = None
        self.ect = None
        self.expect = None
        self.expires = None
        self.forwarded = set()
        self.from_ = None 
        self.host = None
        self.if_match = set()
        self.if_modified_since = None
        self.if_none_match = set()
        self.if_range = None
        self.if_unmodified_since = None
        self.large_allocation = None
        self.link = set()
        self.max_forwards = None
        self.nel = {}
        self.origin = None
        self.permissions_policy = set()
        self.range = None
        self.referer = None
        self.retry_after = None
        self.rtt = None
        self.save_data = None
        self.sec_ch_prefers_color_scheme = None
        self.sec_ch_prefers_reduced_motion = None
        self.sec_ch_prefers_reduced_transparency = None
        self.sec_ch_ua = None
        self.sec_ch_ua_arch = None
        self.sec_ch_ua_bitness = None
        self.sec_ch_ua_full_version = None
        self.sec_ch_ua_full_version_list = {}
        self.sec_ch_ua_mobile = None
        self.sec_ch_ua_model = None
        self.sec_ch_ua_platform = None
        self.sec_ch_ua_platform_version = None
        self.sec_fetch_dest = None
        self.sec_fetch_mode = None
        self.sec_fetch_site = None
        self.sec_fetch_user = None
        self.sec_gpc = None
        self.experimental_non_standard = None
        self.sec_purpose = None
        self.sec_websocket_accept = None
        self.server_timing = set()
        self.service_worker_navigation_preload = None
        self.sourcemap = None
        self.supports_loading_mode = set()
        self.te = None
        self.timing_allow_origin = None
        self.tk = None
        self.trailer = set()
        self.transfer_encoding = set()
        self.user_agent = None
        self.via = set()
        self.viewport_width = None
        self.want_digest = set()
        self.warning = {}
        self.width = None
        self.x_dns_prefetch_control = None
        self.non_standard = None
        self.x_forwarded_for = None
        self.x_forwarded_host = None
        self.x_forwarded_proto = None
        # ------policy and security related fields------
        self.referrer_policy = None
        self.feature_policy = {}
        self.cross_origin_embedder_policy = None
        self.cross_origin_opener_policy = None
        self.cross_origin_resource_policy = None
        self.strict_transport_security = set()
        self.x_content_security_policy = {}
        self.x_content_security_policy_report_only = {}
        self.access_control_allow_credentials = None
        self.access_control_allow_headers = set()
        self.access_control_expose_headers = set()
        self.access_control_max_age = None
        self.access_control_request_headers = set()
        self.access_control_request_method = None
        self.content_security_policy_report_only = {}
        self.upgrade_insecure_requests = None
        # ------cookie related fields------
        self.cookie = {}
        self.set_cookie = set()

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

    # ------cache------
    def set_cache_control_max_age(self, duration: int) -> None:
        self.cache_control["max-age"] = duration

    def set_cache_control_field(self, field: str, param: str) -> None:
        self.cache_control[field] = param

    def set_last_modified(self, date_string: str, length: int = 0) -> None:
        if not date_string:
            self.last_modified = None
        else:
            self.last_modified = (http.get_datetime(date_string), length)

    def set_date(self, date_string: str) -> None:
        if not date_string:
            self.date = None
        else:
            self.date = http.get_datetime(date_string)

    # ------content------
    def set_content_length(self, length: int) -> None:
        self.content_length = length

    def set_content_type(self, mime_type: str) -> None:
        self.content_type = mime_type

    def set_content_language(self, language: str, preference: float = None) -> None:
        self.content_language[language] = preference

    def set_content_charset(self, charset: str, preference: float = None) -> None:
        self.content_charset[charset] = preference

    def set_content_encoding(self, encoding: str) -> None:
        self.content_encoding.add(encoding)

    # ------access control------
    def add_access_control_allow_method(self, method: str) -> None:
        self.access_control_allow_methods.add(method)

    def add_access_control_allow_origin(self, origin: str) -> None:
        self.access_control_allow_origin.add(origin)

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

    # ------other fields------
    def set_x_xss_protection_mode_block(self) -> None:
        self.x_xss_protection = "1; mode=block"

    def set_x_xss_protection_report_uri(self, uri: str) -> None:
        self.x_xss_protection = f"1; report={uri}"

    def set_x_frame_options(self, option: str) -> None:
        if option.lower().strip() == "deny":
            self.x_frame_options = None
        else:
            self.x_frame_options = option

    # ------header line-getters------

    def get_http_str(self) -> str:
        return f"HTTP/{str(self.http_ver)}"

    def get_response_statement(self) -> str:
        return (f"{self.get_http_str()}{http.WHITESPACE}"
                f"{self.status_code}{http.WHITESPACE}"
                f"{self.status_phrase}{http.DELIMITER}")

    def _line_server(self) -> str:
        return http.format_param("Server", self.server)

    def _line_connection(self) -> str:
        return http.format_param("Connection", self.connection)

    def _line_proxy_connection(self) -> str:
        return http.format_param("Proxy-Connection", self.proxy_connection)

    def _line_cache_control(self) -> str:
        return http.format_param("Cache-Control", self.cache_control)

    def _line_accept(self) -> str:
        return http.format_param("Accept", self.accept)

    def _line_accept_ranges(self) -> str:
        return http.format_param("Accept-Ranges", self.accept_ranges)

    def _line_content_length(self) -> str:
        return http.format_param("Content-Length", self.content_length)

    def _line_content_type(self) -> str:
        return http.format_param("Content-Type", self.content_type)

    def _line_content_language(self) -> str:
        return http.format_param("Content-Language", self.content_language, "q")

    def _line_content_charset(self) -> str:
        return http.format_param("Content-Charset", self.content_charset, "q")

    def _line_content_encoding(self) -> str:
        return http.format_param("Content-Encoding", self.content_encoding)

    def _line_date_line(self) -> str:
        return http.format_param("Date", http.get_date_string(self.date) if self.date else None)

    def _line_last_modified(self) -> str:
        return http.format_param("Last-Modified",
                                 (http.get_date_string(self.last_modified[0]),
                                  self.last_modified[1]) if self.last_modified else None,
                                 "length")

    def _line_vary(self) -> str:
        return http.format_param("Vary", self.vary)

    def _line_access_control_allow_origin(self) -> str:
        return http.format_param("Access-Control-Allow-Origin", self.access_control_allow_origin)

    def _line_access_control_allow_methods(self) -> str:
        return http.format_param("Access-Control-Allow-Methods", self.access_control_allow_methods)

    def _line_pragma_line(self) -> str:
        return http.format_param("Pragma", self.pragma)

    def _line_etag_line(self) -> str:
        return http.format_param("ETag", self.etag)

    def _line_keep_alive_line(self) -> str:
        return http.format_param("Keep-Alive", self.keep_alive)

    def _line_www_authenticate(self) -> str:
        return http.format_param("Authentication", self.www_authenticate)

    def _line_location(self) -> str:
        return http.format_param("Location", self.location)

    def _line_xframe_options(self) -> str:
        return http.format_param("X-Frame-Options", self.x_frame_options)

    def _line_x_xss_protection(self) -> str:
        return http.format_param("X-XSS-Protection", self.x_xss_protection)

    def _line_upgrade(self) -> str:
        return http.format_param("Upgrade", self.upgrade)

    def _line_referrer_policy(self) -> str:
        return http.format_param("Referrer-Policy", self.referrer_policy)

    def _line_content_type_options(self) -> str:
        return http.format_param("Content-Type-Options", self.content_type_options)
    
    def _line_feature_policy(self) -> str:
        return http.format_param("Feature-Policy", self.feature_policy)
    
    def _line_content_security_policy(self) -> str:
        return http.format_param("Content-Security-Policy", self.content_security_policy)
    
    def _line_cross_origin_embedder_policy(self) -> str:
        return http.format_param("Cross-Origin-Embedder-Policy", self.cross_origin_embedder_policy)
    
    def _line_cross_origin_opener_policy(self) -> str:
        return http.format_param("Cross-Origin-Opener-Policy", self.cross_origin_opener_policy)

    def _line_cross_origin_resource_policy(self) -> str:
        return http.format_param("Cross-Origin-Resource-Policy", self.cross_origin_resource_policy)

    def _line_expect_ct(self) -> str:
        return http.format_param("Expect-CT", self.expect_ct)
    
    def _line_strict_transport_security(self) -> str:
        return http.format_param("Strict-Transport-Security", self.strict_transport_security)
    
    def _line_x_content_type_options(self) -> str:
        return http.format_param("X-Content-Type-Options", self.x_content_type_options)
    
    def _line_x_powered_by(self) -> str:
        return http.format_param("X-Powered-By", self.x_powered_by)
    
    def _line_x_content_security_policy(self) -> str:
        return http.format_param("X-Content-Security-Policy", self.x_content_security_policy)
    
    def _line_x_ua_compatible(self) -> str:
        return http.format_param("X-UA-Compatible", self.x_ua_compatible)
    
    def _line_x_content_duration(self) -> str:
        return http.format_param("X-Content-Duration", self.x_content_duration)
    
    def _line_x_content_security_policy_report_only(self) -> str:
        return http.format_param("X-Content-Security-Policy-Report-Only", self.x_content_security_policy_report_only)
    
    def _line_x_webkit_csp(self) -> str:
        return http.format_param("X-WebKit-CSP", self.x_webkit_csp)
    
    def _line_x_content_type_options(self) -> str:
        return http.format_param("X-Content-Type-Options", self.x_content_type_options)
    
    def _line_accept_ch(self) -> str:
        return http.format_param("Accept-CH", self.accept_ch)

    def _line_accept_ch_lifetime(self) -> str:
        return http.format_param("Accept-CH-Lifetime", self.accept_ch_lifetime)
    
    def _line_non_standard_deprecated(self) -> str:
        return http.format_param("Non-Standard-Deprecated", self.non_standard_deprecated)
    
    def _line_accept_charset(self) -> str:
        return http.format_param("Accept-Charset", self.accept_charset)
    
    def _line_accept_encoding(self) -> str:
        return http.format_param("Accept-Encoding", self.accept_encoding)
    
    def _line_accept_language(self) -> str:
        return http.format_param("Accept-Language", self.accept_language)
    
    def _line_accept_patch(self) -> str:
        return http.format_param("Accept-Patch", self.accept_patch)
    
    def _line_accept_post(self) -> str:
        return http.format_param("Accept-Post", self.accept_post)
    
    def _line_access_control_allow_credentials(self) -> str:
        return http.format_param("Access-Control-Allow-Credentials", self.access_control_allow_credentials)
    
    def _line_access_control_allow_headers(self) -> str:
        return http.format_param("Access-Control-Allow-Headers", self.access_control_allow_headers)
    
    def _line_access_control_expose_headers(self) -> str:
        return http.format_param("Access-Control-Expose-Headers", self.access_control_expose_headers)
    
    def _line_access_control_max_age(self) -> str:
        return http.format_param("Access-Control-Max-Age", self.access_control_max_age)
    
    def _line_access_control_request_headers(self) -> str:
        return http.format_param("Access-Control-Request-Headers", self.access_control_request_headers)
    
    def _line_access_control_request_method(self) -> str:
        return http.format_param("Access-Control-Request-Method", self.access_control_request_method)
    
    def _line_age(self) -> str:
        return http.format_param("Age", self.age)
    
    def _line_allow(self) -> str:
        return http.format_param("Allow", self.allow)
    
    def _line_alt_svc(self) -> str:
        return http.format_param("Alt-Svc", self.alt_svc)
    
    def _line_alt_used(self) -> str:
        return http.format_param("Alt-Used", self.alt_used)
    
    def _line_authorization(self) -> str:
        return http.format_param("Authorization", self.authorization)
    
    def _line_clear_site_data(self) -> str:
        return http.format_param("Clear-Site-Data", self.clear_site_data)
    
    def _line_content_disposition(self) -> str:
        return http.format_param("Content-Disposition", self.content_disposition)
    
    def _line_content_dpr(self) -> str:
        return http.format_param("Content-DPR", self.content_dpr)
    
    def _line_content_location(self) -> str:
        return http.format_param("Content-Location", self.content_location)
    
    def _line_content_range(self) -> str:
        return http.format_param("Content-Range", self.content_range)
    
    def _line_content_security_policy_report_only(self) -> str:
        return http.format_param("Content-Security-Policy-Report-Only", self.content_security_policy_report_only)
    
    def _line_cookie(self) -> str:
        return http.format_param("Cookie", self.cookie)
    
    def _line_critical_ch(self) -> str:
        return http.format_param("Critical-CH", self.critical_ch)
    
    def _line_device_memory(self) -> str:
        return http.format_param("Device-Memory", self.device_memory)
    
    def _line_digest(self) -> str:
        return http.format_param("Digest", self.digest)
    
    def _line_deprecated(self) -> str:
        return http.format_param("Deprecated", self.deprecated)
    
    def _line_dnt(self) -> str:
        return http.format_param("DNT", self.dnt)
    
    def _line_downlink(self) -> str:
        return http.format_param("Downlink", self.downlink)
    
    def _line_dpr(self) -> str:
        return http.format_param("DPR", self.dpr)
    
    def _line_early_data(self) -> str:
        return http.format_param("Early-Data", self.early_data)
    
    def _line_ect(self) -> str:
        return http.format_param("ECT", self.ect)
    
    def _line_expect(self) -> str:
        return http.format_param("Expect", self.expect)
    
    def _line_expires(self) -> str:
        return http.format_param("Expires", self.expires)
    
    def _line_forwarded(self) -> str:
        return http.format_param("Forwarded", self.forwarded)
    
    def _line_from(self) -> str:
        return http.format_param("From", self.from_)
    
    def _line_host(self) -> str:
        return http.format_param("Host", self.host)
    
    def _line_if_match(self) -> str:
        return http.format_param("If-Match", self.if_match)
    
    def _line_if_modified_since(self) -> str:
        return http.format_param("If-Modified-Since", self.if_modified_since)
    
    def _line_if_none_match(self) -> str:
        return http.format_param("If-None-Match", self.if_none_match)
    
    def _line_if_range(self) -> str:
        return http.format_param("If-Range", self.if_range)
    
    def _line_if_unmodified_since(self) -> str:
        return http.format_param("If-Unmodified-Since", self.if_unmodified_since)
    
    def _line_large_allocation(self) -> str:
        return http.format_param("Large-Allocation", self.large_allocation)
    
    def _line_link(self) -> str:
        return http.format_param("Link", self.link)
    
    def _line_max_forwards(self) -> str:
        return http.format_param("Max-Forwards", self.max_forwards)
    
    def _line_nel(self) -> str:
        return http.format_param("NEL", self.nel)
    
    def _line_origin(self) -> str:
        return http.format_param("Origin", self.origin)
    
    def _line_permissions_policy(self) -> str:
        return http.format_param("Permissions-Policy", self.permissions_policy)
    
    def _line_proxy_authenticate(self) -> str:
        return http.format_param("Proxy-Authenticate", self.proxy_authenticate)
    
    def _line_proxy_authorization(self) -> str:
        return http.format_param("Proxy-Authorization", self.proxy_authorization)
    
    def _line_range(self) -> str:
        return http.format_param("Range", self.range)
    
    def _line_referer(self) -> str:
        return http.format_param("Referer", self.referer)
    
    def _line_retry_after(self) -> str:
        return http.format_param("Retry-After", self.retry_after)
    
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
        return http.format_param("Sec-CH-UA", self.sec_ch_ua)
    
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
    
    def _line_sec_gpc(self) -> str:
        return http.format_param("Sec-GPC", self.sec_gpc)
    
    def _line_sec_purpose(self) -> str:
        return http.format_param("Sec-Purpose", self.sec_purpose)
    
    def _line_sec_websocket_accept(self) -> str:
        return http.format_param("Sec-WebSocket-Accept", self.sec_websocket_accept)
    
    def _line_server_timing(self) -> str:
        return http.format_param("Server-Timing", self.server_timing)
    
    def _line_service_worker_navigation_preload(self) -> str:
        return http.format_param("Service-Worker-Navigation-Preload", self.service_worker_navigation_preload)
    
    def _line_set_cookie(self) -> str:
        return http.format_param("Set-Cookie", self.set_cookie)
    
    def _line_sourcemap(self) -> str:
        return http.format_param("Sourcemap", self.sourcemap)
    
    def _line_supports_loading_mode(self) -> str:
        return http.format_param("Supports-Loading-Mode", self.supports_loading_mode)

    def _line_te(self) -> str:
        return http.format_param("TE", self.te)
    
    def _line_timing_allow_origin(self) -> str:
        return http.format_param("Timing-Allow-Origin", self.timing_allow_origin)
    
    def _line_tk(self) -> str:
        return http.format_param("Tk", self.tk)
    
    def _line_trailer(self) -> str:
        return http.format_param("Trailer", self.trailer)
    
    def _line_transfer_encoding(self) -> str:
        return http.format_param("Transfer-Encoding", self.transfer_encoding)
    
    def _line_upgrade_insecure_requests(self) -> str:
        return http.format_param("Upgrade-Insecure-Requests", self.upgrade_insecure_requests)
    
    def _line_user_agent(self) -> str:
        return http.format_param("User-Agent", self.user_agent)
    
    def _line_via(self) -> str:
        return http.format_param("Via", self.via)
    
    def _line_viewport_width(self) -> str:
        return http.format_param("Viewport-Width", self.viewport_width)
    
    def _line_want_digest(self) -> str:
        return http.format_param("Want-Digest", self.want_digest)
    
    def _line_warning(self) -> str:
        return http.format_param("Warning", self.warning)
    
    def _line_width(self) -> str:
        return http.format_param("Width", self.width)
    
    def _line_x_dns_prefetch_control(self) -> str:
        return http.format_param("X-DNS-Prefetch-Control", self.x_dns_prefetch_control)
    
    def _line_x_forwarded_for(self) -> str:
        return http.format_param("X-Forwarded-For", self.x_forwarded_for)
    
    def _line_x_forwarded_host(self) -> str:
        return http.format_param("X-Forwarded-Host", self.x_forwarded_host)
    
    def _line_x_forwarded_proto(self) -> str:
        return http.format_param("X-Forwarded-Proto", self.x_forwarded_proto)
    
    def _line_non_standard(self) -> str:
        return http.format_param("Non-Standard", self.non_standard)

    def __str__(self) -> str:
        response = [self.get_response_statement()]
        for func in [x for x in dir(self) if x.startswith("_line")]:
            line = getattr(self, func)()
            if line:
                response.append(line)
        response.append(http.DELIMITER)
        return ''.join(response)


def parse_response_line(line: str) -> (int, str, float):
    [http_ver, status_code, status_phrase] = line.split(http.WHITESPACE, 2)
    http_ver = float(http_ver.split('/')[1])
    status_code = int(status_code)
    return status_code, status_phrase, http_ver


def __parse_http_line(line: str, response_obj: Response) -> None:
    try:
        if not line or not response_obj:
            return
        keyword, contents = line.removesuffix(http.DELIMITER).split(':', 1)
        keyword = keyword.lower().strip().replace('-', '_')
        if keyword == "keep_alive":
            if ',' not in contents:
                response_obj.keep_alive["timeout"] = contents.strip()
            else:
                for x in contents.split(','):
                    [param, value] = x.split('=', 1)
                    response_obj.keep_alive[param.strip()] = value.strip()
        elif keyword == "cache_control":
            for x in contents.split(','):
                res = x.split('=', 1)
                if len(res) > 1:
                    [param, value] = x.split('=', 1)
                    response_obj.cache_control[param.strip()] = value.strip()
                else:
                    response_obj.cache_control[res[0].strip()] = None
        elif keyword == "content_length":
            response_obj.content_length = int(contents.strip())
        elif keyword == "date":
            response_obj.set_date(contents.strip())
        elif keyword == "content_type":
            res = contents.split(';', 1)
            if len(res) > 1:
                [content, charset] = res
                charset = charset.split("=")[1:][0]
                response_obj.content_type = content.strip()
                response_obj.content_charset = {x.strip() for x in charset.split(',')}
            else:
                response_obj.contentType = contents.strip()
        elif keyword == "last_modified":
            res = contents.split(';', 1)
            if len(res) > 1:
                [date, length] = res
                length = length.split("=")[1]
                response_obj.last_modified = (http.get_datetime(date.strip()), int(length))
            else:
                response_obj.last_modified = (http.get_datetime(res[0].strip()), 0)
        elif keyword == "www_authenticate":
            res = contents.split(';', 1)
            if len(res) > 1:
                [auth, params] = res
                params = params.split("=")[1:]
                response_obj.www_authenticate[auth.strip()] = {
                    x.strip() for x in params.split(',')}
            else:
                response_obj.www_authenticate[contents.strip()] = None
        elif keyword == "from":
            response_obj.from_ = contents.strip()
        elif keyword == "feature_policy" or keyword == "content_security_policy" or keyword == "x_content_security_policy" or keyword == "x_content_security_policy_report_only" or keyword == "x_webkit_csp" or keyword == "proxy_authorization" or keyword == "content_security_policy_report_only":
            res={}
            for x in contents.split(";"):
                [feature, policy] = x.split(" ")
                response_obj.feature_policy[feature.strip()] = policy.strip()
            setattr(response_obj, keyword, res)
        elif keyword == "warning":
            res={}
            contents = contents.split(",")
            for x in contents:
                [code, text] = x.split("-", 1)
                res[code.strip()] = text.strip()
            setattr(response_obj, keyword, res)
        else:
            try:
                class_var = getattr(response_obj, keyword)
                if isinstance(class_var, set):
                    setattr(response_obj, keyword, {x.strip() for x in contents.split(',')})
                elif isinstance(class_var, dict):
                    return
                else:
                    setattr(response_obj, keyword, contents.strip())
            except AttributeError:
                raise ValueError(f"[ERR] Unknown HTTP header field for keyword {keyword}.")
    except Exception as e:
        raise ValueError(f"[ERR] Failed to parse HTTP header line {line}. {e}")


def parse(response: str) -> Response:
    try:
        if not response:
            raise ValueError("[ERR] Empty response to parse.")
        response = response.split(http.DELIMITER)
        res_status, res_message, http_ver = parse_response_line(response[0])
        if not res_status or not res_message:
            return None
        obj = Response(res_status, res_message, http_ver)

        for line in response[1:]:
            __parse_http_line(line, obj)
        return obj
    except Exception as e:
        raise ValueError(f"[ERR] Failed to parse HTTP response. {e}")
        