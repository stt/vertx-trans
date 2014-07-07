import vertx
from core.http import RouteMatcher
from core.sock_js import SockJSServer

from core.event_bus import EventBus
from core.buffer import Buffer

import middleware as mw
from controllers import login, users
from services import github, stache

def log_event(message):
    print ">> %s" % message.body
    print message

def vertx_stop():
    print 'doing some cleanup'
    import sys
    sys.modules.clear()

def get_subclasses(c):
    subclasses = c.__subclasses__()
    for d in list(subclasses):
        subclasses.extend(get_subclasses(d))
    return subclasses

if __name__ == '__main__':
    conf = vertx.config()
    logger = vertx.logger()

    #EventBus.register_handler('auth.github.login', False, log_event)

    rm = RouteMatcher()
    for cls in get_subclasses(mw.Middleware):
        logger.debug("init " + cls.__name__)
        if issubclass(cls, mw.Controller):
            cls().register(rm)
        elif issubclass(cls, mw.EventHandler):
            cls().register()
        else:
            cls().register()

    def msg_handler(message):
        print "Got message body %s"% message.body
    EventBus.register_handler('test.address', handler=msg_handler)

    """TODO: serve static files with apache or something"""
    def request_handler(req):
        uri = 'index.html' if len(req.uri) == 1 else req.uri[1:]
        req.response.send_file('web/' + uri)
    rm.get_re('.*', request_handler)

    def deploy_handler(err, id):
        if err is None:
    #        import static_data
            print "loaded " + id
            def bla(reply,r2): print 'bla',reply,r2
            EventBus.send_with_timeout("campudus.jsonvalidator", {
  "action" : "addSchema",
  "key" : "simpleAddSchema",
  "jsonSchema" : {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "Example Schema",
    "type": "object",
    "properties": {
      "firstName": {
        "type": "string"
      },
      "lastName": {
        "type": "string"
      },
        "age": {
          "description": "Age in years",
          "type": "integer",
          "minimum": 0
        }
      },
      "required": ["firstName", "lastName"]
    }
    }, 1000, bla)
            EventBus.send("campudus.jsonvalidator", {"action":"getSchemaKeys"}, bla)
        else:
            print 'Failed to deploy %s' % err
            err.printStackTrace()

    vertx.deploy_module('com.campudus~json-schema-validator~1.0.0', handler=deploy_handler)

    vertx.deploy_module(
      "io.vertx~mod-mongo-persistor~2.1.0",
      conf['mongo-persistor'], handler=deploy_handler)

    vertx.deploy_module(
      'com.campudus~session-manager~2.0.1-final',
      conf['session-manager'], handler=deploy_handler)
    #vertx.deploy_module('io.vertx~mod-web-server~2.0.0-final', conf['web-server'])
    #  conf['thymeleaf'], handler=deploy_handler)

    #vertx.deploy_module('io.vertx~mod-auth-mgr~2.0.0-final')

    server = vertx.create_http_server()
    server.request_handler(rm)
    SockJSServer(server).bridge({"prefix": "/eventbus"}, [{}], [{}])
    server.listen(8080)
    logger.info("Listening at http://%(host)s:%(port)i" % conf['web-server'])


