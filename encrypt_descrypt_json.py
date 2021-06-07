import json
import math
import base64
from Crypto.Cipher import AES
 
# AES key must be either 16, 24, or 32 bytes long
COMMON_ENCRYPTION_KEY='asdjk@15r32r1234asdsaeqwe314SEFT'
# Make sure the initialization vector is 16 bytes
COMMON_16_BYTE_IV_FOR_AES='IVIVIVIVIVIVIVIV'
 
def get_common_cipher():
	return AES.new(COMMON_ENCRYPTION_KEY,
									AES.MODE_CBC,
									COMMON_16_BYTE_IV_FOR_AES)

def encrypt_with_common_cipher(cleartext):
	common_cipher = get_common_cipher()
	cleartext_length = len(cleartext)
	next_multiple_of_16 = 16 * math.ceil(cleartext_length/16)
	padded_cleartext = cleartext.rjust(next_multiple_of_16)
	raw_ciphertext = common_cipher.encrypt(padded_cleartext)
	return base64.b64encode(raw_ciphertext).decode('utf-8')

def decrypt_with_common_cipher(ciphertext):
	common_cipher = get_common_cipher()
	raw_ciphertext = base64.b64decode(ciphertext)
	decrypted_message_with_padding = common_cipher.decrypt(raw_ciphertext)
	return decrypted_message_with_padding.decode('utf-8').strip()

def encrypt_json_with_common_cipher(json_obj):
	json_string = json.dumps(json_obj)
	return encrypt_with_common_cipher(json_string)
    
def decrypt_json_with_common_cipher(json_ciphertext):
	json_string = decrypt_with_common_cipher(json_ciphertext)
	return json.loads(json_string)
