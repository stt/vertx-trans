
class Middleware(object):
    """
    Wannabe middleware base-class
    """
    def register(self):
        pass

class Controller(Middleware):
    """
    Wannabe middleware base-class to init vertx request handlers
    """
    def register(self, rm):
        pass

class EventHandler(Middleware):
    """
    Wannabe middleware base-class to init vertx event handlers
    """
    def register(self):
        pass

