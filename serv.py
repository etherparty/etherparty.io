#etherparty.io v1
#GPLv3

import apsw, re, random, binascii, logging, subprocess, os
from epconfig import *
from time import gmtime, strftime
from flask import Flask, request
app = Flask(__name__)

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

@app.route("/")
def main_():
   return ''.join(open('index.html').readlines())

@app.route("/builder") #contracts builder
def builder():
   return ''.join(open('builder.html').readlines())

@app.route("/compile", methods=['POST'])
def compile_contract():
   contract = request.form['contract'].encode('ascii',errors='ignore').decode('ascii')
   contract_exec = subprocess.check_output(['echo', '-e', '\'' + contract.replace('\r\n','\n') + '\'']).decode('utf-8')
   hexdata = subprocess.check_output([serpent_dir + 'serpent', 'compile', '\"' + contract_exec + '\"' ],stderr=subprocess.STDOUT).decode('utf-8')
   print(hexdata)
   return hexdata;

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
         hexdata = subprocess.check_output([xcp_dir + "counterpartyd.py","--testnet", "--unconfirmed", "--data-dir=" + data_dir,"publish", "--source=" + source ,"--code-hex=" + code_hex , "--gasprice=" + gasprice , "--startgas=" + startgas, "--endowment=" + endowment], stderr=subprocess.STDOUT).decode('utf-8').replace('\n', '').split(';')
         print(hexdata)
         #output = "<h3> 0099 SUCCESS <br> UNSIGNED %s <br> SIGNED %s <br> TXID %s <br> " % (hexdata[0],hexdata[1], hexdata[2])
         output = "<h3> 0099 SUCCESS <br> TXID %s <br> " % hexdata[2]
    except Exception as e:
      print(e)
      #if 'output' in e:
      output = "<h3> 0098 ERR <br> REASON %s " % e.output
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
      print(e)
      #if 'output' in e:
      output = "<h3> 0098 ERR <br> REASON %s " % e.output
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
      hexdata = subprocess.check_output([xcp_dir + "counterpartyd.py","--testnet", "--unconfirmed", "--data-dir=" + data_dir,"burn", "--source=" + address  ,"--quantity=0.25"  ], stderr=subprocess.STDOUT).decode('utf-8').replace('\n', '').split(';')
      print(hexdata)
      output = "<h3> 0102 GASADDED <br> ADDRESS %s <br> QUANTITY %s </h3>" % (address, 'plenty') 
    except Exception as e:
      print(e)
      #if 'output' in e:
      output = "<h3> 0098 ERR <br> REASON %s " % e
      #else: output = e

    return output; 

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=80, debug=False, use_reloader=True)
