#! /usr/bin/env python


import hashlib

import sys

trans_5C = "".join(chr(x ^ 0x5c) for x in xrange(256))
trans_36 = "".join(chr(x ^ 0x36) for x in xrange(256))
block_size = hashlib.sha256().block_size

def dumphex(desc, buf):
    print "========== begin %s ==========" % desc
    for i,c in enumerate(buf) :
        sys.stdout.write(hex(ord(c)))
        if 0 == ((i + 1) % 15):
            sys.stdout.write("\n")
        elif (len(buf) - 1 != i) :
            sys.stdout.write(",")
    print
    sys.stdout.flush()
    print "========== end %s ==========" % desc


def usage():
    print "========================================="
    print sys.argv[0]+" msg_file key_file out_sigfile"
    print "========================================="


def hmac_sha256(strMsg, strKey):
    lenKey = len(strKey)

    dumphex("key:", strKey)
    dumphex("Msg:", strMsg)
    if lenKey > block_size:
        strKey = hashlib.sha256(strKey).digest()
    else :
        strKey += chr(0) * (block_size - lenKey)
    
    dumphex("key:", strKey)
    o_key_pad = strKey.translate(trans_5C)
    i_key_pad = strKey.translate(trans_36)

    return hashlib.sha256(o_key_pad + hashlib.sha256(i_key_pad + strMsg).digest())

def main():
    if 4 != len(sys.argv) :
        usage()
        sys.exit()

    fileMsg = open(sys.argv[1], "rb")
    fileKey = open(sys.argv[2], "rb")
    fileSig = open(sys.argv[3], "wb")

    fileMsg.seek(0, 2)
    lenMsg = fileMsg.tell()
    fileMsg.seek(0, 0)
    
    fileKey.seek(0, 2)
    lenKey = fileKey.tell()
    fileKey.seek(0, 0)
    
    strMsg = fileMsg.read(lenMsg)
    strKey = fileKey.read(lenKey)
    fileMsg.close()
    fileKey.close()

    h = hmac_sha256(strMsg, strKey)
    print h.hexdigest()
    fileSig.write(h.digest()) 
    fileSig.close()

if "__main__" == __name__:
    main()
