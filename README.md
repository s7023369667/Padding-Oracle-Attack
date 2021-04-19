# Padding-Oracle-Attack
How to actually code Python to do  the Padding-Oracle-Attack ?

•NTNU Oracle Sever: http://140.122.185.210:8080/oracle/xxx 

•Reference : https://samsclass.info/141/proj/p14pad.htm 

作法: 

將 ciphertext 分成 9 組，其中第一組為加密後回傳的 IV，後面 8 組是我們真正想要解出來的 ciphertext，因為 block cipher 的加密方式會把上一個 block 加密後的結果和下一個 block 的 plaintext 經過 AES(DES或任意加密法) 加密後所得到的值做 XOR 依序下去，所以我們每次都將c1和c2 送進去。
並對c1的每個位置先都設成0甚至是任何數，因為我們並不需要他，甚至不希望他干擾我們的猜測，只是由c1最後一個 byte 開始依序做猜測，目的是希望透過 Oracle 解密時查看送回來的ciphertext 經過解密後最後所產生的 padding 結果是否符合padding規則且padding 值為正確(由0x01至0x16)的資訊，我們就可以猜出 c1 在該位置應該填入的值，並將此值和padding byte做XOR來找出 D_k (C2)，所以透過此公式  我們就能依序解出整個Intermediate，在將此Intermediate和c2做XOR就能解出此block的plaintext 。
公式：(P_i=D_k (C_i)⨁C_(i-1)@D_k (C_i )=C_(i-1)⨁ Pbyte)
![image](https://user-images.githubusercontent.com/50870684/115169780-95757f00-a0f1-11eb-91ca-c3d2ea24f389.png)

以此圖舉例：
![image](https://user-images.githubusercontent.com/50870684/115169917-ec7b5400-a0f1-11eb-92d5-edcacc8a938a.png)

我們想破解C2: ciphertext[32:48]找出P2: plaintext[32:48]，此時將先對C1:ciphertext[16:32]設成全零並從最後一個byte將0到255依序填入ciphertext[31]猜測，並對ciphertext[16:32]+ ciphertext[32:48]進行Oracle，如果回傳的是valid代表我們找到ciphertext[31]應該填入的猜測值使得解密後padding結果為valid，此時我們透過將ciphertext[31]和padding byte做XOR即可得到Intermediate[47]，當我們得到Intermediate[47]，這時候要進行下一輪之前，我們必須將C1的最後一個byte設為我們已知的Intermediate[47]和下一個padding byte的XOR值，才接著把C1的ciphertext[30]做填值和C2送入Oracle，解出下一個Intermediate[46]，如此一來當我們解出整個Intermediate[32:48]後，將Intermediate[32:48]和ciphertext[32:48]做XOR即可得到plaintext[32:48]。

在解密過程中，因為 sever 是老師提供的並且在學校的網域，所以發現如果使用非學校的網路會解到一半就被擋下來，所以非常困擾，因為會沒辦法 Debug， 如果有一樣的問題必須使用 VPN 連學校網域，雖然網速慢了點，但至少可以 好好的 Debug 把程式刻出來之後，再找時間來學校一次跑完。
