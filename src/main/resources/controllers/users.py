import vertx
from core.event_bus import EventBus
from middleware import Controller

logger = vertx.logger()

def bla(reply): print str(dir(reply))

def user_request_handler(req):
    user = {
	    "action": "save",
	    "collection": "users",
	    "document": {
		"name": "tim",
		"age": 1000,
		"shoesize": 3.14159,
		"username": "tim",
		"password": "wibble"
	    }
	}
    user['document'].update({
        'username': req.params["user"]
    })
    EventBus.send("vertx.mongopersistor", user, bla)
    req.response.end("Userz: %s ID: %s"% (req.params["user"],  req.params["id"]) ) 


class UserHandler(Controller):
    def register(self, rm):
        rm.get('/details/:user/:id', user_request_handler)
        logger.info("registered user handler")
        EventBus.send("campudus.jsonvalidator", {"action":"getSchemaKeys"}, bla)


