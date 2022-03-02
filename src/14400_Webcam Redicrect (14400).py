# coding: UTF-8

import urllib2
import ssl
import urlparse
import BaseHTTPServer
import SocketServer
import threading

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

        def set_output_value_sbc(self, pin, val):
            if pin in self.g_out_sbc:
                if self.g_out_sbc[pin] == val:
                    print ("# SBC: pin " + str(pin) + " <- data not send / " + str(val))
                    return

            self._set_output_value(pin, val)
            self.g_out_sbc[pin] = val

        def get_data(self):
            url_in = self._get_input_value(self.PIN_I_STARGETURL)  # type : str
            print("- get_data " + url_in)
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
            try:
                ctx = ssl._create_unverified_context()

                request = urllib2.Request(url_resolved, headers={'Host': url_parsed.hostname})
                response = urllib2.urlopen(request, context=ctx)
                response_data = response.read()
                header = response.info()
                if "Content-Type" in header:
                    self.http_request_handler.response_content_type = header["Content-Type"]
                    self.DEBUG.set_value("14400 Last content type", header["Content-Type"])

                self.http_request_handler.response_data = response_data
                self._set_output_value(self.PIN_O_SSTATUS, "Received target data")
                self.DEBUG.set_value("14400 Last target URL fetched", url_resolved)

            except Exception as e:
                self.DEBUG.add_message("14400: " + str(e) + " for '" + url_resolved + "'")
                self._set_output_value(self.PIN_O_SSTATUS, str(e))

        def run_server(self):
            port = self._get_input_value(self.PIN_I_NPORT)
            server_address = ('', port)

            if self.httpd:
                self.DEBUG.add_message("14400: Shutting down server")
                self.httpd.shutdown()

            self.httpd = ThreadedTCPServer(server_address, self.http_request_handler)
            ip, port = self.httpd.server_address
            self.t = threading.Thread(target=self.httpd.serve_forever)
            self.t.setDaemon(True)
            self.t.start()
            self.DEBUG.add_message("14400: Server running on " + str(ip) + ":" + str(port))

        def on_init(self):
            self.DEBUG = self.FRAMEWORK.create_debug_section()
            self.g_out_sbc = {}
            self.httpd = ""
            self.t = ""

            self.http_request_handler = MyHttpRequestHandler
            # self.http_request_handler.on_init()

        def on_input_value(self, index, value):
            if index == self.PIN_I_NPORT:
                self.run_server()

            elif index == self.PIN_I_STARGETURL:
                self.get_data()

    class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
        pass

    # class MyHttpRequestHandler(SocketServer.BaseRequestHandler):
    class MyHttpRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

        def on_init(self):
            self.response_content_type = ""
            self.response_data = ""

        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', self.response_content_type)
            self.end_headers()

            self.wfile.write(self.response_data)
