from ciphers import vigenere_encrypt, affine_encrypt, playfair_encrypt, hill_encrypt, enigma_encrypt_decrypt

print(vigenere_encrypt('HELLO','KEY'))
print(affine_encrypt('HELLO',5,8))
print(playfair_encrypt('HELLO','KEYWORD'))
print(hill_encrypt('HELLO',[[3,3],[2,5]]))
print(enigma_encrypt_decrypt('HELLO',['I','II','III'],[0,0,0],[0,0,0]))
