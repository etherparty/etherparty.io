#etherparty.io v1
#GPLv3
import apsw, re, random, binascii, logging, subprocess, os
from time import gmtime, strftime
from flask import Flask, request, Response, redirect
app = Flask(__name__)

log_file = './access.log'
logger = logging.getLogger('werkzeug')
logger.setLevel(666)
logger.addHandler(logging.FileHandler(log_file))

def log__():
   _env = request.environ
   keys = ['HTTP_CF_CONNECTING_IP','QUERY_STRING', 'REQUEST_METHOD', 'REMOTE_ADDR', 
           'HTTP_USER_AGENT','HTTP_ACCEPT_LANGUAGE', 'HTTP_COOKIE', 'PATH_INFO' ]
   result = []

   for key in keys:
      result.append('None' if key not in _env else _env[key])

   result.append(request.form if len(request.form) > 0 else 'None' )

   logger.log(666,"[ %s ] - IP %s - QS %s - METHOD %s - REMOTEIP %s - UAGENT %s - LANG %s - COOKIE %s - PATH %s - FORM %s", strftime("%Y-%m-%d %H:%M:%S"),  result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7], result[8])

filetypes = { 'js': 'application/json', 'css': 'text/css', 'html': 'text/html', 'png': 'image/png', 
   'jpg': 'image/jpg', 'php': 'text/html', 'woff': 'application/font-woff', 'ttf': 'application/x-font-ttf', 'mp4': 'video/mp4', 'ogg': 'video/ogg', 'webm': 'video/webm' }
binaryprefixes = ['ttf','woff','mp4','ogg','webm', 'jpg', 'png']
@app.route("/")
@app.route("/<path:ex>")
def extra(ex='index.html'):

  if request.headers.has_key("Range"):
    sts = 206
  else:
    sts = 200

   print(ex)
   try:
    prefix = ex.split('.')[-1]
    filetype = filetypes[ prefix ] 
    if prefix in binaryprefixes:
      ret = open('' +ex, mode="rb").read()
    else:
      ret = ''.join(open('' +ex, encoding='utf8').readlines())
    resp = Response(response=ret, status=sts, mimetype=filetype)
    return resp 
   except Exception as e:
    print('err', ex, e)
    return ''

if __name__ == "__main__":
    app.run(host="127.0.0.1",port=6666, debug=False, use_reloader=True)
