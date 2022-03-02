# coding: UTF-8

import unittest
import json
import time
import httplib

# functional import

import urllib2
import ssl
import urlparse
import BaseHTTPServer
import SocketServer
import threading


#########################################################

class hsl20_4:
    LOGGING_NONE = 0

    def __init__(self):
        pass

    class BaseModule:
        debug_output_value = {}  # type: {}
        debug_set_remanent = {}  # type: {}
        debug_input_value = {}  # type: {}

        def __init__(self, a, b):
            pass

        def _get_framework(self):
            f = hsl20_4.Framework()
            return f

        def _get_logger(self, a, b):
            return 0

        def _get_remanent(self, key):
            return 0

        def _set_remanent(self, key, val):
            self.debug_set_remanent = val

        def _set_output_value(self, pin, value):
            """

            :type pin: int
            """
            self.debug_output_value[int(pin)] = value
            print "# Out: pin " + str(pin) + " <- " + str(value)

        def _get_input_value(self, pin):
            if pin in self.debug_input_value:
                return self.debug_input_value[pin]
            else:
                return 0

        def _get_module_id(self):
            return 123

    class Framework:
        def __init__(self):
            pass

        def _run_in_context_thread(self, a):
            pass

        def create_debug_section(self):
            d = hsl20_4.DebugHelper()
            return d

        def get_homeserver_private_ip(self):
            return "127.0.0.1"

        def get_instance_by_id(self, id):
            return ""

        def resolve_dns(self, a):
            if a == 'nina.api.proxy.bund.dev':
                return "52.59.159.124"
            else:
                print("Warning! resolve_dns: No IP for hoste reuqest " + a)
                return "127.0.0.1"

    class DebugHelper:
        def __init__(self):
            pass

        def set_value(self, cap, text):
            print("DEBUG value\t'" + str(cap) + "': " + str(text))

        def add_message(self, msg):
            print("Debug Msg\t" + str(msg))

        def add_exception(self, msg):
            print("EXCEPTION Msg\t" + str(msg))


#########################################################

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


################################################################################


class TestSequenceFunctions(unittest.TestCase):
    test = WebcamRedicrect_14400_14400(0)

    def setUp(self):
        print("\n###setUp")
        with open("credentials.txt") as f:
            self.cred = json.load(f)

        self.test = WebcamRedicrect_14400_14400(0)
        #self.test.debug_input_value[self.test.PIN_I_SAGS] = self.cred["PIN_I_SAGS"]
        self.test.on_init()

        self.target_url = "https://nina.api.proxy.bund.dev/api31/appdata/gsb/eventCodes/BBK-EVC-001.png"
        self.test.debug_input_value[self.test.PIN_I_STARGETURL] = self.target_url

        self.port = 20004
        self.test.debug_input_value[self.test.PIN_I_NPORT] = self.port

    # 1. The module shall fetch the content provided by a user configurable URL (*target URL*).
    # 3. The module shall fetch data from http and https URL.
    def test_1_3_get_data(self):
        print("\n### test_1_3_get_data")
        self.target_url = "https://nina.api.proxy.bund.dev/api31/appdata/gsb/eventCodes/BBK-EVC-001.png"
        self.test.debug_input_value[self.test.PIN_I_STARGETURL] = self.target_url
        self.test.on_input_value(self.test.PIN_I_STARGETURL, self.target_url)
        self.assertTrue(self.test.debug_output_value[self.test.PIN_O_SSTATUS] == "Received target data")

    # 2. The module shall provide a HTTP server on 127.0.0.1 and a user configurable port.
    # 4. The module shall provide the fetched data as response to a incoming GET request.
    # 5. The module shall set the content header field bases on the *target URL* content information.
    def test_2_4_5_run_server(self):
        print("\n### test_2_3_run_server")

        # set up http client
        conn = httplib.HTTPConnection("127.0.0.1", self.port)

        # test
        self.test.on_init()
        self.test.get_data()
        self.test.on_input_value(self.test.PIN_I_NPORT, self.port)
        self.test.http_request_handler.response_data = "Hello world"
        time.sleep(3)

        conn.request("GET", "/dummy.png")
        r1 = conn.getresponse()
        print r1.status, r1.reason
        data1 = r1.read()
        self.assertTrue(data1 == "Hello world")
        self.assertTrue(r1.getheader("Content-type") == "image/png")

        target_url = "https://nina.api.proxy.bund.dev/api31/appdata/gsb/eventCodes/BBK-EVC-015.png"
        self.test.debug_input_value[self.test.PIN_I_STARGETURL] = target_url
        self.test.on_input_value(self.test.PIN_I_STARGETURL, target_url)
        self.test.http_request_handler.response_data = "Hello user"
        time.sleep(3)

        conn.request("GET", "/dummy.png")
        r1 = conn.getresponse()
        print r1.status, r1.reason
        data1 = r1.read()
        self.assertTrue(data1 == "Hello user")
        self.assertTrue(r1.getheader("Content-type") == "image/png")


if __name__ == '__main__':
    unittest.main()
