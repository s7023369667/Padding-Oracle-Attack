import requests
##fileOpen
def fileOpen():
    f=open('ciphertext.txt','r')
    ciphertext = f.read()
    f.close()
    return ciphertext
##把讀進來的ciphertext換成list
def block_cipher(ciphertext):
    i, ciphers, tmp = 0, [], []
    while i < len(ciphertext) + 1:
        if i % 32 != 0:
            tmp.append(ciphertext[i] + ciphertext[i + 1])
        else:
            ciphers.append(tmp)
            if i < len(ciphertext):
                tmp = [ciphertext[i] + ciphertext[i + 1]]
        i += 2
    real_cipher = ciphers
    ciphers = ciphers[1:]
    # for i in ciphers:
    #     print(i)
    ##分別輸出一個包含最前面的那個IV的block ciphers，及不包含的block ciphers
    return real_cipher,ciphers
##把block cipher轉回字串
def recover_ciphertext(ciphers):
    ciphertext=''
    for i in ciphers:
        for j in i:
            ciphertext+=j
    # print(ciphertext)
    return ciphertext
##對sever發送request，使用try, except才不會因為逾時連線重跑，
##但可能會擋住所有錯誤，所以必須完成Debug後才加
def Oracle(ciphertext):
    url=f'http://140.122.185.210:8080/oracle/{ciphertext}'
    print(url)
    try:
        response = requests.get(url)
        if response.text=='valid':
            print(response.text)
            return True
        else:
            return False
    except:
        pass
##在我們塞值做Oracle之前，先更新我們的c1
def update(iv,idx):
    for u in range(1, idx):
        update = Do_XOR(iv[-(idx - u)], '{:02x}'.format(idx))
        iv[-(idx - u)] = '{:02x}'.format(update)
    return iv
##attack
def attack(blockCipher,real_cipher):
    plaintext = ''
    for i in range(1,len(blockCipher)):
        M=[]
        iv = ['00'] * 16
        for idx in range(1,17):
            ###用M來作為下一個iv
            for j in range(1, idx):
                iv[-(j)] = M[j-1]
            ###更新
            iv=update(iv,idx)
            ###猜測
            for guessByte in range(256):
                guess = '{:02x}'.format(guessByte)
                iv[-(idx)] = guess
                test = recover_ciphertext(iv+blockCipher[i])
                ###Oracle
                if Oracle(test):
                    print("guess:",guess)
                    mid = Do_XOR(guess,'{:02x}'.format(idx))
                    M.append('{:02x}'.format(mid))
                    print(f'----{i}/{len(blockCipher)}--Get--{idx}-->----{test}--------')
                    break
        ##decrypt
        print(M[::-1])
        p=decrypt(real_cipher[i],M[::-1])
        plaintext+=p
    print(plaintext)
    file = open('ANS.txt', 'w')
    file.write(plaintext)
    file.close()
##XOR function
def Do_XOR(A,B):
    return int(str(A),16)^int(str(B),16)
##解密
def decrypt(real_cipher,mid_Val):
    d=''
    for i in range(len(real_cipher)):
        d+=chr(Do_XOR(real_cipher[i],mid_Val[i]))
    print(d)
    return d



if __name__ == '__main__':
    ciphertext = fileOpen()
    real_cipher,blockCipher= block_cipher(ciphertext)
    attack(blockCipher,real_cipher)
