import time, rtc
import wifi, socketpool, ssl
import adafruit_requests
from adafruit_httpserver import HTTPServer, HTTPResponse
from secrets import secrets
from formatter import CustomFormatter
from formatter import log

pool = socketpool.SocketPool(wifi.radio)
server = HTTPServer(pool)

@server.route("/")
def base(request):
    log.info("Got request: " +request.raw_request)
    return HTTPResponse("Hello!")

@server.route("set-time", "POST")
def time(request):
    log.info("Setting time...")
    req_string = request.raw_request.decode()


startup()

def startup():
    if (connectWifi()):
        log.info("Connected to WiFi!")
        setTime()
        log.info("Time is set to: "+time.localtime().tm_hour+":"+time.localtime().tm_min+"\nIf this is not correct, consult the documentation <3")
        advertiseService()
        startWebServer()

def startWebServer():
    server.serve_forever(str(wifi.radio.ipv4_address))

def advertiseService():
    import mdns
    server = mdns.server(wifi.radio)
    server.instance_name = "Feeder S2Mini"
    server.advertiseService(service_type="_feederS2Mini", protocol="_tcp", port=80)


def setTime():
    # TODO: Search for time server on local network with mdns
    request = adafruit_requests.Session(pool, ssl_create_default_context())
    time_url = "http://worldtimeapi.org/api/"+secrets["timezone"]
    log.info("Getting current time for \""+secrets["timezone"]+"\"")
    response = request.get(time_url).json()
    unixtime = int(response['unixtime']) + int(response['raw_offset'])
    rtc.RTC().datetime = time.localtime(unixtime)

def connectWifi():
    wifi.radio.connect(secrets["ssid"], secrets["password"])
    if (wifi.radio.ap_info != None):
        return true
    return false



