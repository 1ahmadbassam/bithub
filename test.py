# from httplib.responses import Response
#
# k = Response("200", "OK", "HTTP")
# print(k)
import numpy

from httplib.requests import Request, parse

k = Request(Request.Command.GET, "http://sdfox7.com/")
k2 = parse("GET http://sdfox7.com/ HTTP/1.1\r\n\r\n")
print(k2)

