import binascii 

def decoderow(tup):
  each = tup
  each = each.split(',')
  each = [ a.replace('\'','') for a in each ]
  #print(each)
  print('id,blobhex,blobkey,txid,timestamp,email,name,alias')
  print(int(each[0]), each[1], each[2], each[3], binascii.unhexlify(each[4]).decode('ascii'), binascii.unhexlify(each[5]).decode('ascii'), binascii.unhexlify(each[6]).decode('ascii'),binascii.unhexlify(each[7]).decode('ascii') if each[7] != 'NULL' else None )


a =open('./users.db').readlines()

rows = [ decoderow(each[:-1]) for each in a ]

