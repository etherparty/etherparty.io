#etherparty.io v1
#GPLv3
<<<<<<< HEAD
import apsw, re, random, binascii, logging, subprocess, os, time, json, hashlib, mandrill, tweepy
from flask import Flask, request, Response, redirect
app = Flask(__name__)

auth = tweepy.OAuthHandler('YrFLtZEo6aWlQv1g8yYOONF40', 'wDjEJ5tRaR3Y50I3JfhZR7LOjkWWn3trq1qdIv58qSgFD8SG4F')
auth.set_access_token('2965296846-Ny6Q4rd4SnsRic4hDsHZtJkQy3csp0GXMqsN7lU', 'SqhEg5p6VcDBnEkdyrGr4FbvnshjTt9GxUWvmGgmIQUrI')
tweepy_api = tweepy.API(auth)
mandrill_client = mandrill.Mandrill('GWxgR8BRZEGbo6r2aRhN_w')
log_file = './access.log'
db_file = '/home/ubuntu/.etherparty/users.db'
logger = logging.getLogger('werkzeug')
logger.setLevel(666)
logger.addHandler(logging.FileHandler(log_file))
tweets = [] #store tweets
timelastchecked = 0 #store timelastchecked for tweets
=======

import apsw, re, random, binascii, logging, subprocess, os
from epconfig import *
from opcodes import *
from time import gmtime, strftime
from flask import Flask, request, Response
app = Flask(__name__)

logger = logging.getLogger('werkzeug')
logger.setLevel(666)
logger.addHandler(logging.FileHandler(log_file))
>>>>>>> 27238ec29c4619656a09d8a921aa09f552392c5b

def log__():
   _env = request.environ
   keys = ['HTTP_CF_CONNECTING_IP','QUERY_STRING', 'REQUEST_METHOD', 'REMOTE_ADDR', 
           'HTTP_USER_AGENT','HTTP_ACCEPT_LANGUAGE', 'HTTP_COOKIE', 'PATH_INFO' ]
   result = []

   for key in keys:
      result.append('None' if key not in _env else _env[key])

   result.append(request.form if len(request.form) > 0 else 'None' )

<<<<<<< HEAD
   logger.log(666,"[ %s ] - IP %s - QS %s - METHOD %s - REMOTEIP %s - UAGENT %s - LANG %s - PATH %s - FORM %s", time.strftime("%Y-%m-%d %H:%M:%S"),  result[0], result[1], result[2], result[3], result[4], result[5], result[7], result[8])

@app.after_request
def req_hand(res):
  log__()
  return res

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
    return Response(response='', status=404)

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
    'alias': sanitize( request.form['alias'] )
   }

   blobhex = hashlib.sha256( json.dumps(blob).encode('ascii') ).hexdigest()

   blobkey = str( int( blobhex[:16], 16 ) ).zfill(64)

   #TODO need to put character limit on input field, 32byte word max 

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

        blob['txid'] = hexdata[-1]

        #TODO store in sqlite blobhex, blobkey, txid, timestamp, email, name, alias

        db = apsw.Connection(db_file)
        cursor = db.cursor()
        retval = cursor.execute('''INSERT into users(blobhex,blobkey,txid,timestamp,email,name,alias) VALUES (?,?,?,?,?,?,?);''', [blobhex, blobkey, blob['txid'], blob['timestamp'], blob['email'], blob['name'], blob['alias'] ] )
        print('successful addition to db', retval)
        cursor.close()

        message = {
            "html": "Hello and welcome on behalf of the team at Etherparty!  <br><br> We are excited to add you to the Etherparty family, and we hope you're as excited to try our services as we are to build them! <br><br> For your information: <br><br> ID#: " + str(int(blobkey)) + " <br> Alias: " + binascii.unhexlify( blob['alias'] ).decode('ascii') + " <br> Proof of Registration: " + blobhex + " <br> Registration date: " + time.ctime(int(binascii.unhexlify( blob['timestamp'] ).decode('ascii'))) + " <br><br> Please keep this email for your records, you will be able to use this information later to sign up for our beta products very soon! <br><br> Don't hestitate to send questions or comments to hello@etherparty.io. <br><br> Thank you for registering with Etherparty.io, we'll let you know when we launch!",
            "subject": "Thanks for registering! Etherparty.io",
            "from_email": "hello@etherparty.io",
            "from_name": "Etherparty",
            "to": [
                {
                    "email":  binascii.unhexlify( blob['email'] ).decode('ascii'),
                    "name":  binascii.unhexlify( blob['name'] ).decode('ascii'),
                    "type": "to"
                }
            ]
        }
        result = mandrill_client.messages.send(message=message, async=False)
        if result[0]['status'] != 'sent': print("Failure in sending: " + str(result))
        else: print("email sent successfully: " + str(result))

        return Response(response=str(int(blobkey)), status=200) 

   except Exception as e:
        print(e, e.__dict__)
        return Response(response='', status=404)

def decoderow(tup):
  each = tup
  return (str(int(each[0])), each[1], binascii.unhexlify(each[2]).decode('ascii') if each[2] is not None else None, binascii.unhexlify(each[3]).decode('ascii') )

@app.route("/users")
def getusers():
    try:
      db = apsw.Connection(db_file)
      cursor = db.cursor()
      rows = list(cursor.execute('''SELECT blobkey,blobhex,alias,timestamp FROM users order by id asc;'''))
      print('raw rows', rows)
      rows = [ decoderow(each) for each in rows ]
      cursor.close()
    except Exception as e:
      print(e, e.__dict__)

    return json.dumps(rows); 

@app.route("/tweets")
def gettweets():
    global timelastchecked
    global tweets
    timenow = int(time.time())
    if (timenow - timelastchecked) > 900:
      try:
        public_tweets = tweepy_api.user_timeline(count=3)
        tweets = [ [tweet.text, tweet.created_at.ctime() ] for tweet in public_tweets ]
        timelastchecked = timenow
      except Exception as e:
        print(e, e.__dict__)

    return json.dumps(tweets); 

if __name__ == "__main__":
    app.run(host="127.0.0.1",port=6666, debug=False, use_reloader=True)
=======
   logger.log(666,"[ %s ] - IP %s - QS %s - METHOD %s - REMOTEIP %s - UAGENT %s - LANG %s - COOKIE %s - PATH %s - FORM %s", strftime("%Y-%m-%d %H:%M:%S"),  result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7], result[8])

@app.route("/")
#Root
def root():
   return ''.join(open('index.html').readlines())

@app.route("/preview")
#Preview
def preview():
   return ''.join(open('preview.html').readlines())

@app.route("/builder")
#Builder
def builder():
   return ''.join(open('builder.html').readlines())

@app.route("/<path:filepath>")
#Assets
def assets(filepath):
   return Response(response=(filepath if filepath not in validassets else ''.join(open(filepath).readlines())), mimetype='text/css')

@app.route("/compile", methods=['POST'])
def compile_contract():
   contract = request.form['contract'].encode('ascii',errors='ignore').decode('ascii')
   try:
        contract_exec = subprocess.check_output(['echo', '-en',  contract.replace('\r\n','\n').rstrip() ]).decode('utf-8').lstrip()
        hexdata = subprocess.check_output([serpent_dir + 'serpent', 'compile',  contract_exec  ],stderr=subprocess.STDOUT).decode('utf-8')
        print(hexdata)
        output = "<h3> 0099 SUCCESS <br> CONTRACT %s <br> " % hexdata
   except Exception as e:
        print(e, e.output)
        output = "<h3> 0098 ERR <br> CODE %s <br> REASON Try checking your balance, making sure your address is valid, and your input values are correctly formatted " % e.returncode

   return output;

@app.route("/gascalc", methods=['POST'])
def gascalc():
   contract = re.sub(r'\W+','', request.form['codehex'].encode('ascii',errors='ignore').decode('ascii') )
   try:
        hexdata = subprocess.check_output([serpent_dir + 'serpent', 'deserialize', contract ],stderr=subprocess.STDOUT).decode('utf-8').split(' ')[:-1]

        #for i in range(0,len(hexdata)):
        #  try:
        #    hexdata[i] = int(hexdata[i])
        #  except Exception as e:
        #    pass #is not integer

        multiplier = float( (2600001 * 100000000) / (2700000 * 100000000) ) * 100
        totalcost =  int( int( multiplier * 500 ) + (len(contract)/2) * int(5 * multiplier) )

        #for op_ in hexdata:
        #  if type(op_) == type(''):
        #    totalcost += opcodes[op_]

        output = "<h3> 0099 SUCCESS <br> CONTRACT %s <br> GASPRICE %s <br> STARTGAS %s <br> " % (hexdata, 1, totalcost)
   except Exception as e:
        print(e)
        output = "<h3> 0098 ERR <br> REASON %s " % e

   return output;

@app.after_request
def req_hand(res):
  log__()
  return res

@app.route("/publish", methods=['POST'])
def publish():
    source = re.sub(r'\W+','', request.form['source'])
    code_hex = re.sub(r'\W+','', request.form['codehex'])
    gasprice = re.sub(r'\W+','', request.form['gasprice'])
    startgas = re.sub(r'\W+','', request.form['startgas'])
    endowment = re.sub(r'\W+','', request.form['endowment'])
    try:
         hexdata = subprocess.check_output([xcp_dir + "counterparty-cli.py","--testnet", "--unconfirmed", "--data-dir=" + data_dir,"publish", "--source=" + source ,"--code-hex=" + code_hex , "--gasprice=" + gasprice , "--startgas=" + startgas, "--endowment=" + endowment], stderr=subprocess.STDOUT).decode('utf-8').replace('\n', '').split(';')
         print(hexdata)
         #output = "<h3> 0099 SUCCESS <br> UNSIGNED %s <br> SIGNED %s <br> TXID %s <br> " % (hexdata[0],hexdata[1], hexdata[2])
         output = "<h3> 0099 SUCCESS <br> TXID %s <br> NOTE You will need to wait a few minutes for the transaction to confirm, before you attempt to retreive the contract ID" % hexdata[2]
    except Exception as e:
      print(e, e.output)
      #if 'output' in e:
      output = "<h3> 0098 ERR <br> CODE %s <br> REASON Try checking your balance, making sure your address is valid, and your input values are correctly formatted " % e.returncode
      #else: output = e

    return output; 

@app.route("/execute", methods=['POST'])
def execute():
    source = re.sub(r'\W+','', request.form['source'])
    contract = re.sub(r'\W+','', request.form['contract'])
    gasprice = re.sub(r'\W+','', request.form['gasprice'])
    startgas = re.sub(r'\W+','', request.form['startgas'])
    value = re.sub(r'\W+', '', request.form['value'])
    payload_hex = re.sub(r'\W+', '', request.form['payload'])
    try:
         hexdata = subprocess.check_output([xcp_dir + "counterpartyd.py","--testnet", "--unconfirmed", "--data-dir=" + data_dir,"execute", "--source=" + source ,"--contract=" + contract, "--gasprice=" + gasprice , "--startgas=" + startgas, "--value=" + value, "--payload-hex=" + payload_hex], stderr=subprocess.STDOUT).decode('utf-8').replace('\n', '').split(';')
         print(hexdata)
         output = "<h3> 0099 SUCCESS <br> TXID %s <br> " % hexdata[2]
    except Exception as e:
      print(e, e.output)
      #if 'output' in e:
      output = "<h3> 0098 ERR <br> CODE %s <br> REASON Try checking your balance, making sure your address is valid, and your input values are correctly formatted " % e.returncode
      #else: output = e

    return output; 

@app.route("/findcontractid", methods=['POST'])
def findcontractid():
    txid = re.sub(r'\W+', '', request.form['txid'])
    try:
      db = apsw.Connection(db_file)
      cursor = db.cursor()
      rows = list(cursor.execute('''SELECT * FROM executions WHERE tx_hash=?''', (txid,) ))
      print(rows, 'a')
      cursor.close()
      #data = subprocess.check_output(['bitcoind', '-testnet', 'importprivkey', key], stderr=subprocess.STDOUT).decode('utf-8')
      #print(data)
      output = "<h3> 0100 FETCH <br> TXID %s <br> STATUS %s <br> CONTRACTID %s </h3>" % (txid,rows[0][-1], ( "%s" % rows[0][-2] ) if rows[0][-2] != None else "yousuck")
    except Exception as e:
      print(e)
      #if 'output' in e:
      output = "<h3> 0098 ERR <br> REASON %s " % e
      #else: output = e

    return output; 

@app.route("/fetchcontractresult", methods=['POST'])
def fetchcontractresult():
    txid = re.sub(r'\W+', '', request.form['txid'])
    try:
      db = apsw.Connection(db_file)
      cursor = db.cursor()
      rows = list(cursor.execute('''SELECT * FROM executions WHERE tx_hash=?''', (txid,) ))
      print(rows, 'a')
      cursor.close()
      #get storage, contracts, gt
      #data = subprocess.check_output(['bitcoind', '-testnet', 'importprivkey', key], stderr=subprocess.STDOUT).decode('utf-8')
      #print(data)
      output = "<h3> 0100 FETCH <br> TXID %s <br> STATUS %s <br> OUTPUT %s <br> GASPRICE %s <br> GASSTART %s <br> GASCOST %s <br> </h3>" % (txid,rows[0][-1], binascii.hexlify(rows[0][-2]).decode('utf-8'), rows[0][-8], rows[0][-7], rows[0][-6] )
    except Exception as e:
      print(e)
      #if 'output' in e:
      output = "<h3> 0098 ERR <br> REASON %s " % e
      #else: output = e

    return output; 

@app.route("/contracts", methods=['GET'])
def getcontracts():
    try:
      db = apsw.Connection(db_file)
      cursor = db.cursor()
      rows = list(cursor.execute('''SELECT tx_hash,source,contract_id,gas_price,gas_start,gas_cost,gas_remained,value,data,output,status FROM executions'''))

      str_ = '<br> tx_hash | source | contract_id | gas_price | gas_start | gas_cost | gas_remained | value | data | output | status <br>'
      for row in rows:
        for item in row:
          str_ += ' | ' + str(item)
        str_ += '<br>'

      cursor.close()
      output = "<h4> CONTRACTS %s </h4>" % str_
    except Exception as e:
      print(e)
      output = "<h3> 0098 ERR <br> REASON %s " % e

    return output; 

@app.route("/getaddress", methods=['POST'])
def getaddress():
    try:
      data = subprocess.check_output(['bitcoind', '-testnet', 'getnewaddress', '%d' % (random.random() * 1e50)  ], stderr=subprocess.STDOUT).decode('utf-8')
      print(data)
      output = "<h3> 0101 CREATED <br> ADDRESS %s </h3>" % data
    except Exception as e:
      print(e)
      #if 'output' in e:
      output = "<h3> 0098 ERR <br> REASON %s " % e
      #else: output = e

    return output; 

@app.route("/getgas", methods=['POST'])
def getgas():
    address = re.sub(r'\W+', '', request.form['address'])
    try:
      hexdata = subprocess.check_output([xcp_dir + "counterpartyd.py","--testnet", "--unconfirmed", "--data-dir=" + data_dir,"burn", "--source=" + address  ,"--quantity=0.001"  ], stderr=subprocess.STDOUT).decode('utf-8').replace('\n', '').split(';')
      print(hexdata)
      output = "<h3> 0102 GASADDED <br> ADDRESS %s <br> QUANTITY %s </h3>" % (address, 'plenty') 
    except Exception as e:
      print(e)
      #if 'output' in e:
      output = "<h3> 0098 ERR <br> REASON %s " % e
      #else: output = e

    return output; 

@app.route("/checkgas", methods=['POST'])
def checkgas():
    address = re.sub(r'\W+', '', request.form['address'])
    try:
      hexdata = subprocess.check_output([xcp_dir + "counterparty-cli.py","--testnet", "--unconfirmed", "--data-dir=" + data_dir,"balances", address ], stderr=subprocess.STDOUT).decode('utf-8').replace('\n', '').split(';')[0]
      
      output = "<h3> 0102 GASCHECK <br> ADDRESS %s <br> QUANTITY %s </h3>" % (address, (hexdata[ hexdata.find('XCP'): ]).split('|')[1].replace('.','')) 
    except Exception as e:
      print(e, e.output)
      #if 'output' in e:
      output = "<h3> 0098 ERR <br> CODE %s <br> REASON Try checking your balance, making sure your address is valid, and your input values are correctly formatted " % e.returncode
      #else: output = e

    return output; 

@app.route("/payload", methods=['POST'])
def payload():
   payload = request.form['payload'].encode('ascii',errors='ignore').decode('ascii')
   try:
        print([serpent_dir + 'serpent', 'encode_datalist', '"' + payload + '"' ])
        hexdata = subprocess.check_output([serpent_dir + 'serpent', 'encode_datalist', payload ],stderr=subprocess.STDOUT).decode('utf-8')

        output = "<h3> 0099 SUCCESS <br> PAYLOAD %s" % hexdata
   except Exception as e:
        print(e)
        output = "<h3> 0098 ERR <br> REASON %s " % e

   return output;

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=80, debug=False, use_reloader=True)
>>>>>>> 27238ec29c4619656a09d8a921aa09f552392c5b
