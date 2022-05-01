# Samson Nguyen
# 1001496565
# 4381 Info Sec II Steganography
# 4/30/2022

import os

from bitstring import BitArray

if __name__ == "__main__":
    S = 0
    L = 0
    C = "1"
    while True:
        plaintext = input("Plaintext file?")
        # plaintext = "lorem_ipsum.txt"
        if not os.path.exists(plaintext):
            print("P does not exist.")
            continue
        message = input("Message file?")
        # message = "hw.txt"
        if not os.path.exists(message):
            print("M does not exist.")
            continue
        S = int(input("Starting bit number, S?"))
        L = int(input("Length(periodicity), L?"))
        C = input("Placement(1) or retrieval(2)?")[0]
        # S = 0
        # L = 4
        if C != "1" and C != "2":
            print("Invalid mode.")
            continue
        break
    P = BitArray(filename=plaintext)
    PM = P[:]
    if C == "1":
        M = BitArray(filename=message)
        # print("PM", P.bin)
        # print(" M", M.bin)
        # print("PM", end=" ")
        bits_encoded = 0
        bits_read = 0
        counter = 0
        while True:
            if counter < 8:
                # ENCODE EACH MESSAGE BIT
                if bits_encoded < M.len:
                    # print(M.bin[bits_read], S + (bits_read * L))
                    # print(M.bin[bits_encoded], end="")
                    PM.set(M[bits_encoded], S + (bits_read * L))
                else:
                    # print(0, S + (bits_read * L))
                    # print('0', end="")
                    PM.set([0], S + (bits_read * L))
                bits_encoded += 1
                bits_read += 1
                counter += 1
            elif bits_encoded == M.len:
                # END OF MESSAGE
                # print(1, S + (bits_read * L), "EOM")
                # print("E")
                PM.set([1], S + (bits_read * L))
                bits_read += 1
                counter = 0
                break
            else:
                # NOT END OF MESSAGE
                # print('N', end='')
                PM.set(False, S + (bits_read * L))
                bits_read += 1
                counter = 0
        # PM_print = list(PM.bin[:S + bits_read * L:L])
        # del PM_print[8-1::7]
        # print("PM", ''.join(PM_print))
        p = open(plaintext, 'wb')
        p.write(PM.bytes)
        p.close()
    elif C == "2":
        PM = BitArray(length=P.len)
        bits_decoded = 0
        bits_read = 0
        counter = 0
        while True:
            # print(PM.bin)
            # print(P.bin[S + (bits_read * L)], end='')
            if counter < 8:
                # DECODE EACH MESSAGE BIT
                PM.set(P[S + (bits_read * L)], bits_decoded)
                bits_decoded += 1
                bits_read += 1
                counter += 1
            elif P[S + (bits_read * L)]:
                # END OF MESSAGE
                # print(" EOM")
                bits_read += 1
                counter = 0
                while not PM.len % 8 == 0:
                    PM.append([0])
                break
            else:
                # NOT END OF MESSAGE
                # print(" NEOM")
                bits_read += 1
                counter = 0
        m = open(message, 'wb')
        m.write(PM.bytes[:bits_decoded // 8])
        m.close()
        print(PM.bytes[:bits_decoded // 8].decode('utf-8'))

# How someone could find M or P, given (only) L.
#     Given L, search file for each possible S so that one combination of S and L will reproduce M.
#     Given L, search file for possible M, then replace M bits with alternative bits to reproduce P.
