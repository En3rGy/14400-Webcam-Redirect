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
        hsl20_4.BaseModule.__init__(self, homeserver_context, "hsl20_4_Webcam_Redicrect")
        self.FRAMEWORK = self._get_framework()
        self.LOGGER = self._get_logger(hsl20_4.LOGGING_NONE,())
        self.PIN_I_1__BASE_PATH=1
        self.PIN_I_2__PORT=2
        self.PIN_I_STARGETURL=3
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
            self.log_val("Fetch URL", url_in)
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

                with self.http_request_handler.data_lock:
                    if "Content-Type" in header:
                        self.http_request_handler.response_content_type = header["Content-Type"]
                        self.log_val("Last content type", header["Content-Type"])
                    self.http_request_handler.response_data = response_data

                self._set_output_value(self.PIN_O_SSTATUS, "Received target data")
                self.log("Fetched target URL successfully")

            except Exception as e:
                self.log(str(e) + " for '" + url_resolved + "'")
                self._set_output_value(self.PIN_O_SSTATUS, str(e))

        def log(self, msg):
            self.DEBUG.add_message(str(self._get_input_value(self.PIN_I_1__BASE_PATH)) +
                                   ":" + str(self._get_input_value(self.PIN_I_2__PORT)) +
                                   ": " + str(msg))

        def log_val(self, key, val):
            self.DEBUG.set_value(str(self._get_input_value(self.PIN_I_1__BASE_PATH)) +
                                 ":" + str(self._get_input_value(self.PIN_I_2__PORT)) +
                                 " " + str(key), val)

        def stop_server(self):
            if self.server:
                try:
                    self.log("Shutting down running server")
                    self.server.shutdown()
                    self.server.server_close()
                except Exception as e:
                    self.log(str(e))

        def run_server(self):
            self.log("Trying to start server")
            port = self._get_input_value(self.PIN_I_2__PORT)
            server_address = ('', port)

            self.stop_server()

            try:
                self.server = ThreadedTCPServer(server_address, self.http_request_handler, bind_and_activate=False)
                self.server.allow_reuse_address = True
                self.server.server_bind()
                self.server.server_activate()
            except Exception as e:
                self.log(str(e))
                return

            ip, port = self.server.server_address
            self.t = threading.Thread(target=self.server.serve_forever)
            self.t.setDaemon(True)
            self.t.start()
            self.log("Server running on " + str(ip) + ":" + str(port))

        def on_init(self):
            self.DEBUG = self.FRAMEWORK.create_debug_section()
            self.g_out_sbc = {}
            self.server = ""
            self.t = ""

            self.http_request_handler = MyHttpRequestHandler

            self.run_server()

        def on_input_value(self, index, value):
            if index == self.PIN_I_2__PORT:
                self.run_server()

            elif index == self.PIN_I_STARGETURL:
                if not self.server:
                    self.run_server()

                if value == "0" or value == "":
                    self.log("Reset image")

                    with self.http_request_handler.data_lock:
                        self.http_request_handler.response_data = "\x00"
                        self._set_output_value(self.PIN_O_SSTATUS, "Presenting empty image")

                        empty_png = "\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x04\x00\x00\x00\x04\x08\x06\x00\x00\x00\xa9\xf1\x9e~\x00\x00\x00\x06bKGD\x00\x00\x00\x00\x00\x00\xf9C\xbb\x7f\x00\x00\x00\x0cIDAT\x08\xd7c`\xa0\x1c\x00\x00\x00D\x00\x01\x06\xc0W\xa2\x00\x00\x00\x00IEND\xaeB`\x82"

                        self.http_request_handler.response_data = empty_png
                        self.http_request_handler.response_content_type = "image/png"

                else:
                    self.get_data()

    class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
        pass

    # class MyHttpRequestHandler(SocketServer.BaseRequestHandler):
    class MyHttpRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

        data_lock = threading.RLock()

        def on_init(self):
            self.response_content_type = ""
            self.response_data = ""

        def do_GET(self):
            with self.data_lock:
                self.send_response(200)
                self.send_header('Content-type', self.response_content_type)
                self.end_headers()

                self.wfile.write(self.response_data)
