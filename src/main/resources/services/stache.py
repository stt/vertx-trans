import vertx
from core.event_bus import EventBus
from middleware import Controller
import pystache
import os.path

logger = vertx.logger()

prefix = '/thyme'
class LoginHandler(Controller):
    def register(self, rm):
        def request_handler(req):
            path = req.path.replace(prefix,'')
            if not path.endswith('/') and os.path.isdir(path):
                path += '/'
            if path.endswith('/'): path += 'index.html'
            print "Open "+path
            fh = open('templates/' + path)
            body = pystache.render(fh.read(), {'person': 'Mom'})
            req.response.put_header('Content-Length', str(len(body)))
            req.response.write_str(body)
            fh.close()
            req.response.end()

            #EventBus.send('vertx.thymeleaf.parser', params, handle_response)

        rm.get('/thyme', request_handler)

