import math    
import struct


#Initialize hash values:
#(first 32 bits of the fractional parts of the square roots of the first 8 primes 2..19):
h0 = 0x6a09e667
h1 = 0xbb67ae85
h2 = 0x3c6ef372
h3 = 0xa54ff53a
h4 = 0x510e527f
h5 = 0x9b05688c
h6 = 0x1f83d9ab
h7 = 0x5be0cd19

#Initialize array of round constants:
#(first 32 bits of the fractional parts of the cube roots of the first 64 primes 2..311):
k = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
   0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
   0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
   0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
   0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
   0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
   0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
   0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]

def Shift_right(value, unit):
    x = len(value) - unit
    tmp = "0" * unit + value[0 : x]
    return tmp

def leftrotate(s, d):
    tmp = s[d : ] + s[0 : d]
    return tmp

def rightrotate(s, d):
   return leftrotate(s, len(s) - d)

def xor(s,d):
    tmp = ""
    for x in range(0,len(s)):
        if s[x] == '0' and d[x] == '0':
            tmp = tmp + "0" 
        if s[x] == '1' and d[x] == '1':
            tmp = tmp + "0" 
        if s[x] == '1' and d[x] == '0':
            tmp = tmp + "1" 
        if s[x] == '0' and d[x] == '1':
            tmp = tmp + "1" 
    return tmp

def add_strings(x,y):
    max_len = max(len(x), len(y)) 

    x = x.zfill(max_len) 
    y = y.zfill(max_len) 
        
    # initialize the result 
    result = '' 
        
    # initialize the carry 
    carry = 0

    # Traverse the string 
    for i in range(max_len - 1, -1, -1): 
        r = carry 
        r += 1 if x[i] == '1' else 0
        r += 1 if y[i] == '1' else 0
        result = ('1' if r % 2 == 1 else '0') + result 
        carry = 0 if r < 2 else 1     # Compute the carry. 
        
    if carry !=0 : result = '1' + result 

    finalres = result.zfill(max_len)
    if len(finalres) == 32:
        return finalres
    else: 
        n = len(finalres)
        return (finalres[n-32:33])

    

def sigma_0(value):
    temp1 = rightrotate(value, 7)
    temp2 = rightrotate(value, 18)
    temp3 = Shift_right(value,3)
    res = xor(temp1,temp2)
    return xor(res,temp3)

def sigma_1(value):
    temp1 = rightrotate(value, 17)
    temp2 = rightrotate(value, 19)
    temp3 = Shift_right(value,10)
    res = xor(temp1,temp2)
    return xor(res,temp3)

def usigma_0(value):
    temp1 = rightrotate(value, 2)
    temp2 = rightrotate(value, 13)
    temp3 = rightrotate(value,22)
    res = xor(temp1,temp2)
    return xor(res,temp3)

def usigma_1(value):
    temp1 = rightrotate(value, 6)
    temp2 = rightrotate(value, 11)
    temp3 = rightrotate(value,25)
    res = xor(temp1,temp2)
    return xor(res,temp3)

def choice_Of(det, val1, val2):
    temp = ""
    for x in range(0,len(det)):
        if det[x] == '0':
            temp = temp + val2[x]
        else:
            temp = temp + val1[x] 
    return temp

def majority(val1,val2,val3):
    temp = ""
    for x in range(0,len(val1)):
        count = int(val1[x]) + int(val2[x]) + int(val3[x])
        if count >= 2:
            temp = temp + '1'
        else:
            temp = temp + '0'
    return temp

def Val_in():
    value = input("Enter Data to Encode: ")
    value = str(value)
    return value

def Convert_val(value):
    resultant = ""
    for letter in value:
        res = ''.join(format(i, 'b') for i in bytearray(letter, encoding ='utf-8')) 
        diff = 8 - len(res)
        res = '0' * diff + res
        resultant = resultant + res
    return resultant

def Pad_val(value):  #we have to pad to nearest multiple of 512 adding a 1 seperator and last 64 for size
    value = value + '1'
    size = len(value)
    padding_size = size + 64 
    nearest_mult = math.ceil(padding_size/512)
    totalbits = nearest_mult * 512
    diff = totalbits - padding_size
    val = bin(size-1)
    val = val[2:]
    len_pad = 64 - len(val)
    padded = value + ('0' * diff) + ('0' * len_pad) + val
    return padded

def Split_pad(value):
    blocks_num = math.ceil(len(value)/512)
    block_list = []
    if blocks_num > 1:
        for x in range(0,blocks_num):
            block_list.append(value[x*512,(x+1)*512])
    else:
        block_list.append(value)
    return block_list

def Create_schedule(block):
    W_list = []
    for x in range(0,16):
        W_list.append(block[(x*32):(x+1)*32])
    return W_list

def expand_schedule(schedule):
    for x in range(16,64):
        temp1 = schedule[x-16]
        temp2 = sigma_0(schedule[x-15])
        temp3 = schedule[x-7]
        temp4 = sigma_1(schedule[x-2])            
        res1 = add_strings(temp1,temp2)
        res2 = add_strings(temp3,temp4)
        finalres = add_strings(res2,res1)
        schedule.append(finalres)
    return schedule

def conv_hex(value):
    x = bin(value)
    x = x[2:len(x)]
    padsize = 32 - len(x)
    finalval = '0' * padsize + x
    return finalval

def create_compression_block():
    comp_block = []
    comp_block.append(conv_hex(h0))
    comp_block.append(conv_hex(h1))
    comp_block.append(conv_hex(h2))
    comp_block.append(conv_hex(h3))
    comp_block.append(conv_hex(h4))
    comp_block.append(conv_hex(h5))
    comp_block.append(conv_hex(h6))
    comp_block.append(conv_hex(h7))
    return comp_block

def create_const_block():
    newConst = []
    for const in k:
        newConst.append(conv_hex(const))
    return newConst 

def compression_process(schblk, comp_block, const_block):
    count = 0
    for elem in schblk:
            temp1 = usigma_1(comp_block[4])
            temp2 = choice_Of(comp_block[4],comp_block[5],comp_block[6])
            temp3 = comp_block[7]
            temp4 = elem
            temp5 = const_block[count]
            count = count + 1
            res1 = add_strings(temp1,temp2)
            res2 = add_strings(temp3,temp4)
            T1 = add_strings(add_strings(res1,res2),temp5)
            
            temp6 = usigma_0(comp_block[0])
            temp7 = majority(comp_block[0],comp_block[1],comp_block[2])
            T2 = add_strings(temp6,temp7)
            finalres = add_strings(T1,T2)
            comp_block.insert(0,finalres)
            comp_block.remove(comp_block[8])

            lastmod = add_strings(comp_block[4], T1)
            comp_block[4] = lastmod
    return comp_block

def convertElem(value):
    intvalue = int(value, 2)
    hexvalue = hex(intvalue)
    hexvalue = str(hexvalue)
    hexvalue = hexvalue[2:len(hexvalue)]
    #print(hexvalue)

    return hexvalue


def Main():
    value = Val_in()
    bin_val = Convert_val(value)
    #print((bin_val))
    Padding = Pad_val(bin_val)
    #print(len(Padding))
    block_list = Split_pad(Padding)
    #print(block_list)

    schedule = []
    expandedschedules = []
    for block in block_list:
        schedule.append(Create_schedule(block))
    #print(len(schedule))
    for tempsched in schedule:  
        expandedschedules.append(expand_schedule(tempsched))

    #print('cheese')
    #print(expandedschedules[0][60])
    comp_block = create_compression_block()
    const_block = create_const_block()
    #print(comp_block)

    resultantcompression = []
    for schblk in expandedschedules:
        tempblock = compression_process(schblk, comp_block, const_block)
        resultantcompression.append(tempblock)
    
    #print(resultantcompression)
    comp_block2 = create_compression_block()
    
    for compressed in resultantcompression:
        count = 0
        for elem in compressed:
            compressed[count] = add_strings(comp_block2[count], elem)
            count = count + 1
        
    hashed = ''
    for compressd in resultantcompression:
        for elem in compressed:
            hashed = hashed + convertElem(elem)

    print(hashed)
Main()
