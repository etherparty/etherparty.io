import subprocess, json

seedaddr="mvMqLp7NhrPcUkMznrBA6TkJAzHoVKqvif"
seedpubkey="76a914a2d056e9ba66f6ac8435b3024c8dfca969b63c1688ac"
otherpubkey="76a914ba58ac68e317aeadbaa1b21e26fc6e14b457ad5c88ac"

while True:
	out1=json.loads(subprocess.check_output(["bitcoin-cli","-testnet", "listunspent" , "0"], stderr=subprocess.STDOUT).decode('utf-8').replace('\n', ''))

	largest = { 'txid': str(0), 'amount': 0 , 'vout': 0}
	for each in out1:
	  if each['scriptPubKey'] == seedpubkey:
	    if largest['amount'] < each['amount']:
	      largest = each
	      print(each)

	txstr = '[{"txid":"' + largest['txid'] + '","vout":' + str(largest['vout']) + '}]'
	amount = largest['amount'] - 0.0007
	outstr = '{"' + seedaddr + '":' + str(amount) +', "mxWGCsjeyYpqkpbdm4N2ro5yQhfRjZQapz": 0.0006}'
	try:
	  out2=subprocess.check_output(["bitcoin-cli","-testnet", "createrawtransaction", txstr , outstr ], stderr=subprocess.STDOUT).decode('utf-8').replace('\n', '').replace(otherpubkey,seedpubkey)
	  print(out2)
	except Exception as e:
	  print(e);

	out3=json.loads(subprocess.check_output(["bitcoin-cli","-testnet", "signrawtransaction", out2 ], stderr=subprocess.STDOUT).decode('utf-8').replace('\n', ''))['hex']
	print(out3)

	out4=subprocess.check_output(["bitcoin-cli","-testnet", "sendrawtransaction", out3 ], stderr=subprocess.STDOUT).decode('utf-8').replace('\n', '')
	print(out4)
