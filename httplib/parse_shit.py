stuff= "self.status_code = status_code,self.status_phrase = status_phrase,self.http_ver = http_ver,self.server = None, self.connection = close,self.keep_alive = w,self.etag = None,self.accept = set(),self.accept_ranges = set(),self.content_length = None,self.content_type = None,self.content_language = w,self.content_charset = w,self.content_encoding = set(),self.cache_control = w,self.date = None,self.last_modified = None,self.proxy_connection = set(), self.access_control_allow_methods = set(),self.access_control_allow_origin = set(),self.upgrade = set(),self.vary = set(),self.pragma = set(),self.www_authenticate = w,self.location = None,self.x_xss_protection = None,self.x_frame_options = None, self.referrer_policy = None, self.content_type_options = None, self.feature_policy =  w, self.content_security_policy = w, self.cross_origin_embedder_policy = None, self.cross_origin_opener_policy = None, self.cross_origin_resource_policy = None, self.expect_ct = None, self.strict_transport_security = None, self.x_content_type_options = None, self.x_powered_by = None, self.x_content_security_policy = None, self.x_ua_compatible = None, self.x_content_duration = None, self.x_content_security_policy_report_only = None, self.x_webkit_csp = None, self.x_content_type_options = None"
stuff = stuff.split(",")
for i in range(len(stuff)):
    stuff[i] = stuff[i].split("=")[0].strip().removeprefix("self.")
print(stuff)
getshit='''Accept
Accept-CH
Accept-CH-Lifetime
Non-standard Deprecated
Accept-Charset
Accept-Encoding
Accept-Language
Accept-Patch
Accept-Post
Accept-Ranges
Access-Control-Allow-Credentials
Access-Control-Allow-Headers
Access-Control-Allow-Methods
Access-Control-Allow-Origin
Access-Control-Expose-Headers
Access-Control-Max-Age
Access-Control-Request-Headers
Access-Control-Request-Method
Age
Allow
Alt-Svc
Alt-Used
Authorization
Cache-Control
Clear-Site-Data
Connection
Content-Disposition
Content-DPR
Non-standard Deprecated
Content-Encoding
Content-Language
Content-Length
Content-Location
Content-Range
Content-Security-Policy
Content-Security-Policy-Report-Only
Content-Type
Cookie
Critical-CH
Experimental
Cross-Origin-Embedder-Policy
Cross-Origin-Opener-Policy
Cross-Origin-Resource-Policy
Date
Device-Memory
Experimental
Digest
Deprecated
DNT
Non-standard Deprecated
Downlink
Experimental
DPR
Non-standard Deprecated
Early-Data
Experimental
ECT
Experimental
ETag
Expect
Expect-CT
Expires
Forwarded
From
Host
If-Match
If-Modified-Since
If-None-Match
If-Range
If-Unmodified-Since
Keep-Alive
Large-Allocation
Non-standard Deprecated
Last-Modified
Link
Location
Max-Forwards
NEL
Experimental
Origin
Permissions-Policy
Pragma
Deprecated
Proxy-Authenticate
Proxy-Authorization
Range
Referer
Referrer-Policy
Retry-After
RTT
Experimental
Save-Data
Experimental
Sec-CH-Prefers-Color-Scheme
Experimental
Sec-CH-Prefers-Reduced-Motion
Experimental
Sec-CH-Prefers-Reduced-Transparency
Experimental
Sec-CH-UA
Experimental
Sec-CH-UA-Arch
Experimental
Sec-CH-UA-Bitness
Experimental
Sec-CH-UA-Full-Version
Deprecated
Sec-CH-UA-Full-Version-List
Experimental
Sec-CH-UA-Mobile
Experimental
Sec-CH-UA-Model
Experimental
Sec-CH-UA-Platform
Experimental
Sec-CH-UA-Platform-Version
Experimental
Sec-Fetch-Dest
Sec-Fetch-Mode
Sec-Fetch-Site
Sec-Fetch-User
Sec-GPC
Experimental Non-standard
Sec-Purpose
Sec-WebSocket-Accept
Server
Server-Timing
Service-Worker-Navigation-Preload
Set-Cookie
SourceMap
Strict-Transport-Security
Supports-Loading-Mode
Experimental
TE
Timing-Allow-Origin
Tk
Non-standard Deprecated
Trailer
Transfer-Encoding
Upgrade
Upgrade-Insecure-Requests
User-Agent
Vary
Via
Viewport-Width
Non-standard Deprecated
Want-Digest
Deprecated
Warning
Deprecated
Width
Non-standard Deprecated
WWW-Authenticate
X-Content-Type-Options
X-DNS-Prefetch-Control
Non-standard
X-Forwarded-For
Non-standard
X-Forwarded-Host
Non-standard
X-Forwarded-Proto
Non-standard
X-Frame-Options
X-XSS-Protection'''

getshit = getshit.split("\n")
for i in range(len(getshit)):
    getshit[i] = getshit[i].strip().lower().replace("-","_").replace(" ","_")
print()
print(getshit)
for shit in getshit:
    found=False
    for shit2 in stuff:
        if shit==shit2:
            found=True
            break
    if not found:
        pass
        # print(shit)

parse= '''self.accept_charset = set()
        self.accept_encoding = set()
        self.accept_language = set()
        self.accept_patch = set()
        self.accept_post = set()
        self.access_control_allow_credentials = None
        self.access_control_allow_headers = set()
        self.access_control_expose_headers = set()
        self.access_control_max_age = None
        self.access_control_request_headers = set()
        self.access_control_request_method = None
        self.age = None
        self.allow = set()
        self.alt_svc = set()
        self.alt_used = None
        self.authorization = None
        self.clear_site_data = set()
        self.content_disposition = None
        self.content_dpr = None
        self.content_location = None
        self.content_range = None
        self.content_security_policy_report_only = set()
        self.cookie = set()
        self.critical_ch = None
        self.experimental = set()
        self.device_memory = None
        self.digest = None
        self.deprecated = set()
        self.dnt = None
        self.downlink = None
        self.dpr = None
        self.early_data = None
        self.ect = None
        self.expect = set()
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
        self.nel = set()
        self.origin = None
        self.permissions_policy = set() #momken yes check
        self.proxy_authenticate = set()
        self.proxy_authorization = set()
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
        self.sec_ch_ua_full_version_list = set()
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
        self.set_cookie = set()
        self.sourcemap = None
        self.supports_loading_mode = set()
        self.te = set()
        self.timing_allow_origin = None
        self.tk = None
        self.trailer = set()
        self.transfer_encoding = set()
        self.upgrade_insecure_requests = None
        self.user_agent = None
        self.via = set()
        self.viewport_width = None
        self.want_digest = set()
        self.warning = set()
        self.width = None
        self.x_dns_prefetch_control = None
        self.non_standard = None
        self.x_forwarded_for = None
        self.x_forwarded_host = None
        self.x_forwarded_proto = None'''

parse = parse.split("\n")
for i in range(len(parse)):
    parse[i] = parse[i].strip().split("=")[0].strip().removeprefix("self.") if parse[i].strip().split("=")[1].strip()=="set()" else None

for i in range(len(parse)):
    if parse[i]:
        print(parse[i])