
import vertx
from urlparse import urlparse
from urllib import quote

def request(method, url, response_handler, params, headers):
    tgt = urlparse(url)
    ssl = (tgt.scheme == "https")
    port = (80 if not ssl else 443)
    client = vertx.create_http_client(ssl=ssl, port=port, host=tgt.hostname)

    params_encoded = []
    for key in sorted(params.iterkeys()):
        params_encoded.append(quote(key) + "=" + quote("%s" % params[key]))

    query_str = '&'.join(params_encoded)

    if method == 'GET':
        req = client.get(tgt.path +'?'+ query_str, response_handler)
    else:
        req = client.post(tgt.path, response_handler)
        if len(query_str) > 0:
            req.put_header('Content-Length', str(len(query_str)))
            req.put_header('Content-Type', "application/x-www-form-urlencoded")
            req.write_str(query_str)
    for key, val in headers.items():
        req.put_header(key, val)
    req.put_header('User-Agent', "stt")
    req.end()
    
def get(url, response_handler, params={}, headers={}):
    request('GET', url, response_handler, params, headers)
def post(url, response_handler, params={}, headers={}):
    request('POST', url, response_handler, params, headers)



