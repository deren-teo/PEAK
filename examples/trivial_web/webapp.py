from peak.api import *

class WebApp(binding.Component):

    security.allow(
        index_html = security.Anybody
    )
     
    def index_html(self, environ, input, errors):
        return "200 OK", ["Content-type: text/plain"], ["Hello world!"]

