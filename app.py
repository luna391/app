from bottle import run, request, route, TEMPLATE_PATH, jinja2_view
import pygeoip
import os

gip4 = pygeoip.GeoIP('./geo/GeoIP.dat', pygeoip.MEMORY_CACHE)
gicity = pygeoip.GeoIP('./geo/GeoLiteCity.dat', pygeoip.MEMORY_CACHE)

TEMPLATE_PATH[:] = ['templates']

@route('/', name='home', method='GET')
@route('/index.html', name='home', method='GET')
@jinja2_view('index.html')
def index():

        your_ip = request.remote_addr
        your_location = gip4.country_name_by_addr(your_ip)
        your_city = gicity.record_by_addr(your_ip)

        header_list = request.remote_route
        if len(header_list) > 1:
            proxy_list = header_list[1:]
            proxy = ', '.join(proxy_list)
        else:
            proxy = "No proxy detected"

        return {'title':'Your IP is:',
                'your_ip':your_ip,
                'your_location': your_location,
                #'your_city': your_city['city'],
                #'your_longitude': your_city['longitude'],
                #'your_latitude': your_city['latitude'],
                'proxy': proxy}

run(host='0.0.0.0', port=8089, debug=True)
run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
