import vertx
from middleware import EventHandler
from core.event_bus import EventBus
from core.buffer import Buffer
from com.xhaus.jyson import JysonCodec as json
from utils import get

logger = vertx.logger()

def bla(reply):
    print str(dir(reply))
    #EventBus.send('someaddress', reply)

def handle_response(resp):
    # print "got response %s" % resp.status_code
    # print resp.headers
    @resp.body_handler
    def body_handler(body):
        print "JOO", body
        EventBus.send('smart.session.manager', {'action': 'start'}, bla)
        if resp.status_code == 200:
            data = json.loads(body.to_string())
            print data
        else:
            logger.error(body)
 
class LoginHandler(EventHandler):
    def register(self):
        def handler(msg):
            if not msg.body.has_key('error'):
                headers = { 'Authorization': 'token '+msg.body['access_token'] }
                get('https://api.github.com/user', handle_response, headers=headers)
                if 'email' in msg.body['scope']: pass
            else:
                logger.error(msg.body)

        EventBus.register_handler('auth.github.login', handler=handler)


