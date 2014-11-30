#etherparty.io v1
#GPLv3

import apsw, re, random, binascii, logging, subprocess
from epconfig import *
from time import gmtime, strftime
from flask import Flask, request
app = Flask(__name__)

logger = logging.getLogger('werkzeug')
logger.setLevel(666)
logger.addHandler(logging.FileHandler(log_file))

def log__():
   logger.log(666,"[ %s ] - IP %s - QS %s - METHOD %s - REMOTEIP %s - UAGENT %s - LANG %s - COOKIE %s - PATH %s", strftime("%Y-%m-%d %H:%M:%S"),  request.environ['HTTP_CF_CONNECTING_IP'], request.environ['QUERY_STRING'], request.environ['REQUEST_METHOD'], request.environ['REMOTE_ADDR'], request.environ['HTTP_USER_AGENT'], request.environ['HTTP_ACCEPT_LANGUAGE'], "None" if 'HTTP_COOKIE' not in request.environ else request.environ['HTTP_COOKIE'], request.environ['PATH_INFO'])

@app.route("/")
def main_():
   return ''.join(open('index.html').readlines())

@app.after_request
def req_hand(res):
  log__()
  return res

@app.route("/publish", methods=['POST'])
def publish():
    print(['test', request.form])
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
