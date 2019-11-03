from Crypto.Cipher import AES
import base64


key = bytes('????????'.ljust(16,' '))
aes = AES.new(key,AES.MODE_ECB)

# encrypt
plain_text = bytes('??????????'.ljust(16,' '))
text_enc = aes.encrypt(plain_text)
text_enc_b64 = base64.b64encode(text_enc)
print(text_enc_b64)

#output：/cM8Nx+iAidmt6RiqX8Vww==
