#etherparty.io v1
#GPLv3

import apsw, re, random, binascii, logging, subprocess, os
from epconfig import *
from opcodes import *
from time import gmtime, strftime
from flask import Flask, request, Response
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
