import vertx
from core.event_bus import EventBus
from middleware import Controller
from com.xhaus.jyson import JysonCodec as json
from utils import post

logger = vertx.logger()


def handle_response(resp):
    # print "got response %s" % resp.status_code
    # print resp.headers
    @resp.body_handler
    def body_handler(body):
        if resp.status_code == 200:
            data = json.loads(body.to_string())
            print data
            def bla(reply): print dir(reply), reply.message
            EventBus.send("auth.github.login", data, bla)
        else:
            print resp.status_code, body.to_string()

class LoginHandler(Controller):
    def register(self, rm):
        def user_request_handler(req):
            #session_code = request.env['rack.request.query_hash']['code']
            # TODO: check req.params['state']
            params = {
                "client_id": "2377e6850d65aa161d1f",
                "client_secret": "62c8c0af80367464a542c2f4b930499363d4ec7e",
                "code": req.params['code'],
                "accept": "json"
                }
            headers = { 'Accept': "application/json" }
            post('https://github.com/login/oauth/access_token', handle_response, params, headers)

            #req.response.put_header("Location", "https://graph.facebook.com/oauth/authorize?client_id=%s&redirect_uri=%s" % ()) 
            def bla(reply): print dir(reply), reply.message, req.uri
            EventBus.send('smart.session.manager', {'action': 'start'}, bla)
            #req.response.put_header("Cookie", "sess_id=")
            req.response.status_code = 301
            req.response.put_header("Location", "/").end()
            #req.response.end("Userz: %s ID: %s") 

        rm.get('/auth_callback', user_request_handler)

