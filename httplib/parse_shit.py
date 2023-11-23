stuff= '''self.command = command
        self.path = path
        self.http_ver = http_ver
        self.host = http.get_host(path)
        self.user_agent = http.DEFAULT_USER_AGENT
        self.connection = {"close"}
        self.keep_alive = {}
        self.referer = None
        self.accept = set()
        self.content_length = None
        self.accept_language = {}
        self.accept_charset = {}
        self.accept_encoding = set()
        self.cache_control = {}
        self.if_modified_since = None
        self.if_none_match = set()
        self.date = None
        self.proxy_connection = set()
        self.ua_pixels = None
        self.ua_color = None
        self.ua_os = None
        self.ua_cpu = None
        self.dnt = None
        self.upgrade_insecure_requests = None
        self.sec_gpc = None'''
stuff = stuff.split("\n")
for i in range(len(stuff)):
    stuff[i] = stuff[i].strip().split("=")[0].strip().removeprefix("self.")


getshit='''A-IM
Accept
Accept-Charset
Accept-Datetime
Accept-Encoding
Accept-Language
Access-Control-Request-Method
Access-Control-Request-Headers
Authorization
Cache-Control
Connection
Content-Encoding
Content-Length
Content-Type
Content-MD5
Cookie
Date
Expect
Forwarded
From
Host
HTTP2-Settings
If-Match
If-Modified-Since
If-None-Match
If-Range
If-Unmodified-Since
Max-Forwards
Origin
Pragma
Proxy-Authorization
Prefer
Range
Referer
TE
Trailer
Transfer-Encoding
User-Agent
Upgrade
Via
Warning
Upgrade-Insecure-Requests
X-Requested-With
DNT
X-Forwarded-For
X-Forwarded-Host
X-Forwarded-Proto
Front-End-Https
X-Http-Method-Override
X-ATT-DeviceId
X-Wap-Profile
Proxy-Connection
X-UIDH
X-Csrf-Token
X-Request-ID
X-Correlation-ID
Correlation-ID
Correlation-ID
Save-Data
Sec-GPC
'''

getshit = getshit.split("\n")
for i in range(len(getshit)):
    getshit[i] = getshit[i].strip().lower().replace("-","_").replace(" ","_")


parse= '''self.accept_post = set()
        self.content_type_options = None
        self.proxy_authorization = None
        self.access_control_request_headers = set()
        self.access_control_request_method = None
        self.alt_used = None
        self.device_memory = None
        self.downlink = None
        self.early_data = None
        self.ect = None
        self.expect = set()
        self.from_ = None
        self.if_match = set()
        self.if_range = None
        self.if_unmodified_since = None
        self.forwarded = set()
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
        self.sec_ch_ua_full_version_list = set()
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
        self.te = set()
        self.via = None
        self.viewport_width = None
        self.width = None
        self.x_forwarded_for = None
        self.x_forwarded_host = None
        self.x_forwarded_proto = None
        self.a_im = set()
        self.accept_datetime = None
        self.authorization = None
        self.content_encoding = set()
        self.content_type = None
        self.content_md5 = None
        self.cookie = set()
        self.http2_settings = None
        self.pragma = None
        self.prefer = set()
        self.trailer = set()
        self.transfer_encoding = set()
        self.upgrade = None
        self.warning = set()
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
        self.correlation_id = None'''

parse = parse.split("\n")
for i in range(len(parse)):
    parse[i] = parse[i].strip().split("=")[0].strip().removeprefix("self.") if parse[i].strip().split("=")[1].strip() == "set()" else None
for i in range(len(parse)):
    if parse[i]:
        print(parse[i])
for shit in parse:
    found=False
    for shit2 in stuff:
        if shit==shit2 and shit.strip()!="":
            found=True
            break
    if not found:
        pass #print(shit)

for shit in getshit:
    found=False
    for shit2 in stuff:
        if shit==shit2 and shit.strip()!="":
            found=True
            break
    for shit2 in parse:
        if shit==shit2 and shit.strip()!="":
            found=True
            break
    if not found:
        pass#print(shit)
#content length and no transfer encoding
#no content length but tranfer encoding is chucnked
#no content length nor chuncked => timeout
#handle compression and decompression in gzip and zip