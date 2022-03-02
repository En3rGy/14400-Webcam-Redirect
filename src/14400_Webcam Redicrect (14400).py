# coding: UTF-8

import urllib2
import ssl
import urlparse
import http.server
import socketserver

##!!!!##################################################################################################
#### Own written code can be placed above this commentblock . Do not change or delete commentblock! ####
########################################################################################################
##** Code created by generator - DO NOT CHANGE! **##

class WebcamRedicrect_14400_14400(hsl20_4.BaseModule):

    def __init__(self, homeserver_context):
        hsl20_4.BaseModule.__init__(self, homeserver_context, "hsl20_4_WEBCAM_REDIRECT")
        self.FRAMEWORK = self._get_framework()
        self.LOGGER = self._get_logger(hsl20_4.LOGGING_NONE,())
        self.PIN_I_NPORT=1
        self.PIN_I_STARGETURL=2
        self.PIN_O_SSTATUS=1

########################################################################################################
#### Own written code can be placed after this commentblock . Do not change or delete commentblock! ####
###################################################################################################!!!##

    def get_data(self):
        url_in = self._get_input_value(self.PIN_I_STARGETURL)  # type : str
        url_parsed = urlparse.urlparse(url_in)

        # Use Framework to resolve the host ip address.
        host_ip = self.FRAMEWORK.resolve_dns(url_parsed.hostname)
        # Append port if provided.
        netloc = host_ip
        if url_parsed.port is not None:
            netloc += ':%s' % url_parsed.port
        # Build URL with the host replaced by the resolved ip address.
        url_resolved = urlparse.urlunparse((url_parsed[0], netloc) + url_parsed[2:])  # type : str
        # Build a SSL Context to disable certificate verification.
        response_data = ""
        ags = self._get_input_value(self.PIN_I_SAGS)  # type : str
        try:
            ctx = ssl._create_unverified_context()

            request = urllib2.Request(url_resolved)
            response = urllib2.urlopen(request, context=ctx)
            response_data = response.read()
            print(response.info())
            self.http_request_handler.set_reply(response_data)

        except Exception as e:
            # self.set_output_value_sbc(self.PIN_O_BERROR, True)
            self.DEBUG.add_message("14400: " + str(e) + " for '" + url_resolved + "'")
            self.set_output_value_sbc(self.PIN_O_SSTATUS, str(e))

        return response_data

    def run_server(self):
        port = self._get_input_value(self.PIN_I_NPORT)

        with socketserver.TCPServer(("", port), self.http_request_handler) as httpd:
            print("Http Server Serving at port", port)
            httpd.serve_forever()

    def on_init(self):
        self.http_request_handler = MyHttpRequestHandler

    def on_input_value(self, index, value):
        if index == self.PIN_I_NPORT:
            self.run_server()

        elif index == self.PIN_I_STARGETURL:
            self.get_data()


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):

    def __init__(self):
        self.response_data = ""

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        # serve up an infinite stream
        self.wfile.write(self.response_data)

    def set_reply(self, data):
        self.response_data = data