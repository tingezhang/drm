#! /usr/bin/env python

import sys



i = 0
j = 0


"""
Key-scheduling algorithm
input: key octet string
output: keystream
"""
def KSA(key):
    keylength = len(key)
    S = range(256)
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % keylength]) % 256
        #j = (j + ord(S[i]) + ord(key[i % keylength])) % 256
        tmp = S[i]
        S[i] = S[j]
        S[j] = tmp

    return S

"""
"""
def PRGA(S):
    global i
    global j
    i = (i + 1) % 256
    j = (j + S[i]) % 256
    tmp = S[i]
    S[i] = S[j]
    S[j] = tmp
    K = S[(S[i] + S[j]) % 256]
    return K

def usage():
    print "=============================================="
    print sys.argv[0]+" key_file in_msg_file out_enc_file"
    print "=============================================="

def dumphex(desc, buf_list):
    print "========== begin %s ==========" % desc
    for i,c in enumerate(buf_list) :
        sys.stdout.write(hex(c))
        if 0 == ((i + 1) % 15):
            sys.stdout.write("\n")
        elif (len(buf_list) - 1 != i) :
            sys.stdout.write(",")
    print
    sys.stdout.flush()
    print "========== end %s ==========" % desc

def main():
    global i
    global j
    if (4 != len(sys.argv)):
        usage()
        sys.exit(-1)

    key_file = open(sys.argv[1], "rb")
    msg_file = open(sys.argv[2], "rb")
    out_file = open(sys.argv[3], "wb")

    key_file.seek(0, 2)
    key_len = key_file.tell()
    key_file.seek(0, 0)
    key_bytearray = bytearray(key_file.read(key_len))
    key_file.close()

    msg_file.seek(0, 2)
    msg_len = msg_file.tell()
    msg_file.seek(0, 0)
    msg_bytearray = bytearray(msg_file.read(msg_len))
    msg_file.close()

    S = KSA(key_bytearray)
    out_list = []
    i = 0
    j = 0
    for n in msg_bytearray:
        K = PRGA(S)
        out_list.append(n ^ K)

    dumphex("enc", out_list)
    out_file.write(bytearray(out_list))
    out_file.close()

if "__main__" == __name__:
    main()

