#etherparty.io v1
#GPLv3
import apsw, re, random, binascii, logging, subprocess, os, time, json, hashlib
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

    if sts == 206: 
      resp.headers.add('Accept-Ranges','bytes')
      resp.headers.add('Content-Transfer-Encoding','binary')
      resp.headers.add('Content-Range','bytes %s-%s/%s' % (str(0),str(len(ret) - 1),str(len(ret))) )

    return resp 
   except Exception as e:
    print('err', ex, e)
    return ''

def sanitize(s):
  print([type(s), s])
  return binascii.hexlify( s.encode('ascii',errors='ignore') ).decode('ascii') #.zfill(128)[:128] #max 64 bytes of data allowed

@app.route("/execute", methods=['POST'])
def execute():

   print(["form", request.form])

   blob = { 
    'timestamp': sanitize( str( int( time.time() ) ) ),
    'email': sanitize( request.form['email'] ),
    'name': sanitize( request.form['name'] ),
    'addr': sanitize( request.form['addr'] ),
    'alias': sanitize( request.form['alias'] )
   }

   blobhex = hashlib.sha256( json.dumps(blob).encode('ascii') ).hexdigest()
   blobkey = str( int( blobhex[:16], 16 ) ).zfill(64)

   #TODO need to put character limit on input field, 32byte word max 

   #TODO need to store this data internally

   print(["post-sanitize", blob, blobhex, blobkey])
   try:

        source = "mvMqLp7NhrPcUkMznrBA6TkJAzHoVKqvif" #hardcode for now
        contract = "d12e2000ea15ff18333d062fce82be53ef2f82e3" #hardcode for now
        gasprice = "1"
        startgas = "200000"
        value = "0"
        xcp_dir= "/home/ubuntu/counterpartyd_build/dist/counterpartyd/"
        data_dir= "/home/ubuntu/.config/counterpartyd/"
        payload_hex = blobkey + blobhex 

        print(["pre-submission", payload_hex])

        hexdata = subprocess.check_output([xcp_dir + "counterpartyd.py","--testnet", "--unconfirmed", "--data-dir=" + data_dir,"execute", "--source=" + source ,"--contract=" + contract, "--gasprice=" + gasprice , "--startgas=" + startgas, "--value=" + value, "--payload-hex=" + payload_hex], stderr=subprocess.STDOUT).decode('utf-8').replace('\n', '').split(';')

        print(hexdata)

   except Exception as e:
        print(e, e.output, e.returncode)

   return blobkey; 

if __name__ == "__main__":
    app.run(host="127.0.0.1",port=6666, debug=False, use_reloader=True)
