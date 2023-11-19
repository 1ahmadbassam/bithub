from datetime import datetime
from urllib.parse import urlparse


# from requests import Request


def get_http_command_from_command_line(line):
	if not line or len(line) < 2:
		raise ValueError("Invalid command line for HTTP command retrieval")
	if line[0:3].upper() == Request.GET_COMMAND:
		return Request.GET
	elif len(line) > 3 and line[0:4].upper() == Request.POST_COMMAND:
		return Request.POST
	elif len(line) > 3 and line[0:4].upper() == Request.HEAD_COMMAND:
		return Request.HEAD
	elif line[0:3].upper() == Request.PUT_COMMAND:
		return Request.PUT
	else:
		raise ValueError("Invalid command line for HTTP command retrieval, line is " + line)


def get_path_from_command_line(line):
	if len(line) < 4:
		return None
	path = []
	i = 3
	while i < len(line) and line[i] == Request.WHITESPACE:
		i += 1
	while i < len(line) and line[i] != Request.WHITESPACE:
		path.append(line[i])
		i += 1
	return ''.join(path), i


def get_http_version_from_command_line(line, last=0):
	if not line:
		return None
	i = last
	while i < len(line) and line[i] != '/':
		i += 1
	i += 1
	ver = []
	while i < len(line) and line[i] != Request.WHITESPACE and line[i] != Request.DELIMITER[0]:
		ver.append(line[i])
		i += 1
	try:
		return float(''.join(ver))
	except ValueError:
		return None


def parse_http_line(line: str, obj):
	if not line or not obj:
		return
	keyword, contents = line.removesuffix(Request.DELIMITER).split(':', 1)
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
	elif keyword == "user-agent":
		obj.userAgent = contents.strip()
	elif keyword == "accept":
		obj.accept = {x.strip() for x in contents.split(',')}
	elif keyword == "accept-language":
		for x in contents.split(','):
			var = x.split(';q=')
			if len(var) > 1:
				[lang, perf] = var
				obj.acceptLanguage[lang.strip()] = float(perf.strip())
			else:
				obj.acceptLanguage[var[0].strip()] = None
	elif keyword == "accept-charset":
		for x in contents.split(','):
			var = x.split(';q=')
			if len(var) > 1:
				[lang, perf] = var
				obj.acceptCharset[lang.strip()] = float(perf.strip())
			else:
				obj.acceptCharset[var[0].strip()] = None
	elif keyword == "accept-encoding":
		obj.acceptEncoding = {x.strip() for x in contents.split(',')}
	elif keyword == "cache-control":
		for x in contents.split(','):
			[param, value] = x.split('=', 1)
			obj.cacheControl[param.strip()] = value.strip()
	elif keyword == "referer":
		obj.referer = contents.strip()
	elif keyword == "ua-pixels":
		obj.uaPixels = contents.strip()
	elif keyword == "ua-pixels":
		obj.uaPixels = contents.strip()
	elif keyword == "ua-color":
		obj.uaColor = contents.strip()
	elif keyword == "ua-os":
		obj.uaOS = contents.strip()
	elif keyword == "ua-cpu":
		obj.uaCPU = contents.strip()
	elif keyword == "dnt":
		if int(contents.strip()):
			obj.enable_dnt()
	elif keyword == "upgrade-insecure-requests":
		if int(contents.strip()):
			obj.enable_upgrade_insecure_requests()
	elif keyword == "sec-gpc":
		if int(contents.strip()):
			obj.enable_sec_gpc()
	elif keyword == "date":
		obj.date = datetime.strptime(contents.strip(), Request.DATE_FORMAT)
	elif keyword == "if-modified-since":
		res = contents.split(';', 1)
		if len(res) > 1:
			[date, length] = res
			length = length.split("=")[1]
			obj.ifModifiedSince = (datetime.strptime(date.strip(), Request.DATE_FORMAT), int(length))
		else:
			obj.ifModifiedSince = (datetime.strptime(contents.strip(), Request.DATE_FORMAT), 0)
	elif keyword == "if-none-match":
		obj.ifNoneMatch = {x.strip() for x in contents.split(',')}
	elif keyword == "host":
		pass
	else:
		raise ValueError("Unknown HTTP header field for line " + line)


def parse(req: str):
	if not req:
		return None
	if isinstance(req, bytes):
		req = req.decode(Request.ASCII)
	req = req.split(Request.DELIMITER)
	req_type = get_http_command_from_command_line(req[0])
	path, last = get_path_from_command_line(req[0])
	http_ver = get_http_version_from_command_line(req[0], last)
	obj = Request(req_type, path, http_ver)
	for line in req[1:]:
		parse_http_line(line, obj)
	return obj


def _get_host(path):
	return urlparse(path).hostname


def _parse_param_to_header_field(name, params, var=None):
	if not params:
		return None
	if params and isinstance(params, str):
		return f"{name}:{Request.WHITESPACE}{params}{Request.DELIMITER}"
	field = [name, ":", Request.WHITESPACE]
	if params and isinstance(params, set):
		for x in params:
			field.append(x)
			field.append(',')
			field.append(Request.WHITESPACE)
		field.pop()
		field.pop()
	elif params and isinstance(params, dict):
		if var:
			for x, sp in params.items():
				if sp:
					field.append(f"{x};{var}={sp}")
					field.append(',')
					field.append(Request.WHITESPACE)
				else:
					field.append(x)
					field.append(',')
					field.append(Request.WHITESPACE)
		else:
			for x, sp in params.items():
				field.append(f"{x}={sp}")
				field.append(',')
				field.append(Request.WHITESPACE)
		field.pop()
		field.pop()
	elif params and isinstance(params, tuple):
		field.append(params[0])
		if params[1]:
			field.append(';')
			field.append(Request.WHITESPACE)
			field.append(f"{var}={params[1]}")
	else:
		field.append(params)
	field.append(Request.DELIMITER)
	return ''.join(field)


class Request:
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

	DEFAULT_USER_AGENT = 'Mozilla/5.0 (compatible; BitHub; Python3)'

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

	def __init__(self, req_type, path, http_ver=HTTP1):
		self.reqType = req_type
		self.path = path
		self.httpVer = http_ver
		self.host = _get_host(path)
		self.userAgent = Request.DEFAULT_USER_AGENT
		self.connection = {"close"}
		self.keepAlive = {}
		self.accept = set()
		self.acceptLanguage = {}
		self.acceptCharset = {}
		self.acceptEncoding = set()
		self.cacheControl = {}
		self.referer = None
		self.uaPixels = None
		self.uaColor = None
		self.uaOS = None
		self.uaCPU = None
		self.proxyConnection = set()
		self.dnt = None
		self.upgradeInsecureRequests = None
		self.secGPC = None
		self.date = None
		self.ifModifiedSince = None
		self.ifNoneMatch = set()

	def set_path(self, new_path):
		self.path = new_path

	def set_user_agent(self, user_agent):
		self.userAgent = user_agent

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

	def add_accept_language(self, language: str, q: float = None):
		self.acceptLanguage[language] = q

	def add_accept_charset(self, charset: str, q: float = None):
		self.acceptCharset[charset] = q

	def set_accept_language_preference(self, language: str, q: float):
		if language in self.acceptLanguage:
			self.acceptLanguage[language] = q

	def set_accept_charset_preference(self, charset: str, q: float):
		if charset in self.acceptCharset:
			self.acceptCharset[charset] = q

	def add_accept_encoding(self, encoding):
		self.acceptEncoding.add(encoding)

	def remove_accept_mime(self, mime_type):
		if mime_type in self.accept:
			self.accept.remove(mime_type)

	def remove_accept_language(self, language):
		if language in self.acceptLanguage:
			self.acceptLanguage.pop(language)

	def remove_accept_charset(self, charset):
		if charset in self.acceptCharset:
			self.acceptCharset.pop(charset)

	def set_ua_fields(self, pixels=None, color=None, os=None, cpu=None):
		self.uaPixels = pixels
		self.uaColor = color
		self.uaOS = os
		self.uaCPU = cpu

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
			self.date = datetime.strptime(date_string, Request.DATE_FORMAT)

	def set_if_modified_since(self, date_string, length=0):
		if not date_string:
			self.ifModifiedSince = None
		else:
			self.ifModifiedSince = (datetime.strptime(date_string, Request.DATE_FORMAT), length)

	def add_if_none_match(self, etag):
		self.ifNoneMatch.add(etag)

	def remove_if_none_match(self, etag):
		if etag in self.ifNoneMatch:
			self.ifNoneMatch.remove(etag)

	def enable_dnt(self):
		self.dnt = 1

	def disable_dnt(self):
		self.dnt = None

	def enable_upgrade_insecure_requests(self):
		self.upgradeInsecureRequests = 1

	def disable_upgrade_insecure_requests(self):
		self.upgradeInsecureRequests = None

	def enable_sec_gpc(self):
		self.secGPC = 1

	def disable_sec_gpc(self):
		self.secGPC = None

	def get_http_version(self):
		return f"HTTP/{str(self.httpVer)}"

	def get_http_command_line(self):
		command = []
		if self.reqType == Request.GET:
			command.append(Request.GET_COMMAND)
		elif self.reqType == Request.POST:
			command.append(Request.POST_COMMAND)
		elif self.reqType == Request.HEAD:
			command.append(Request.HEAD_COMMAND)
		elif self.reqType == Request.PUT:
			command.append(Request.PUT_COMMAND)
		else:
			raise ValueError("Unimplemented request type")
		command.append(Request.WHITESPACE)
		command.append(self.path)
		command.append(Request.WHITESPACE)
		command.append(self.get_http_version())
		command.append(Request.DELIMITER)
		return ''.join(command)

	def get_host_line(self):
		return _parse_param_to_header_field("Host", self.host)

	def get_connection_line(self):
		return _parse_param_to_header_field("Connection", self.connection)

	def get_proxy_connection_line(self):
		if self.proxyConnection:
			return _parse_param_to_header_field("Proxy-Connection", self.proxyConnection)
		else:
			return None

	def get_user_agent_line(self):
		return _parse_param_to_header_field("User-Agent", self.userAgent)

	def get_cache_control_line(self):
		return _parse_param_to_header_field("Cache-Control", self.cacheControl)

	def get_referer_line(self):
		return _parse_param_to_header_field("Referer", self.referer)

	def get_dnt_line(self):
		return _parse_param_to_header_field("DNT", str(self.dnt))

	def get_upgrade_insecure_requests_line(self):
		return _parse_param_to_header_field("Upgrade-Insecure-Requests", str(self.upgradeInsecureRequests))

	def get_sec_gpc_line(self):
		return _parse_param_to_header_field("Sec-GPC", str(self.secGPC))

	def __str__(self):
		# 1 - build base request
		request = [self.get_http_command_line(), self.get_host_line(), self.get_user_agent_line(),
		           self.get_connection_line()]
		if self.proxyConnection:
			request.append(self.get_proxy_connection_line())
		# 2 - add additional headers often common in browsers
		if self.accept:
			request.append(_parse_param_to_header_field("Accept", self.accept))
		if self.acceptLanguage:
			request.append(_parse_param_to_header_field("Accept-Language", self.acceptLanguage, "q"))
		if self.acceptCharset:
			request.append(_parse_param_to_header_field("Accept-Charset", self.acceptCharset, "q"))
		if self.acceptEncoding:
			request.append(_parse_param_to_header_field("Accept-Encoding", self.acceptEncoding))
		if self.ifModifiedSince:
			request.append(_parse_param_to_header_field("If-Modified-Since",
			                                            (self.ifModifiedSince[0].strftime(
				                                            Request.DATE_FORMAT),
			                                             self.ifModifiedSince[1] if self.ifModifiedSince[
				                                                                        1] > 0 else None),
			                                            "length"))
		if self.keepAlive:
			if "timeout" in self.keepAlive and "max" not in self.keepAlive:
				request.append(_parse_param_to_header_field("Keep-Alive", str(self.keepAlive["timeout"])))
			else:
				request.append(_parse_param_to_header_field("Keep-Alive", self.keepAlive))
		# 3 - add weird UA fields
		if self.uaPixels:
			request.append(_parse_param_to_header_field("UA-pixels", self.uaPixels))
		if self.uaColor:
			request.append(_parse_param_to_header_field("UA-color", self.uaColor))
		if self.uaOS:
			request.append(_parse_param_to_header_field("UA-OS", self.uaOS))
		if self.uaCPU:
			request.append(_parse_param_to_header_field("UA-CPU", self.uaCPU))
		# 4 - add fields used by modern browsers
		if self.cacheControl:
			request.append(self.get_cache_control_line())
		if self.referer:
			request.append(self.get_referer_line())
		if self.dnt:
			request.append(self.get_dnt_line())
		if self.upgradeInsecureRequests:
			request.append(self.get_upgrade_insecure_requests_line())
		if self.secGPC:
			request.append(self.get_sec_gpc_line())
		if self.ifNoneMatch:
			request.append(_parse_param_to_header_field("If-None-Match", self.ifNoneMatch))
		# 5 - add rarely used fields
		if self.date:
			request.append(_parse_param_to_header_field("Date", self.date.strftime(Request.DATE_FORMAT)))
		request.append(Request.DELIMITER)
		return ''.join(request)
