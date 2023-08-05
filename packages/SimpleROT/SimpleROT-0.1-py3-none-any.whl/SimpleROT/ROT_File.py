# SimpleROT Library v0.1
# Created by Fix-22 (https://github.com/Fix-22)

# ROT_File v0.2
# ROT_File allows you to encrypt files using ROT13 and ROTby methods from ROT class.

from SimpleROT import ROT

class ROT_file:
    
    def ROT13_file(filename):
        try:
            with open(filename, "r") as file_r:
                data = file_r.read()

            roted_data = ROT.ROT13(data)

            with open(filename, "w") as file_w:
                file_w.write(roted_data)

            return f"File '{filename}' successfully encrypted"

        except:
            return f"Unable to read the file: '{filename}'. Try change the file path."
    
    def ROTby_encrypt_file(filename, n):
        try:
            with open(filename, "r") as file_r:
                data = file_r.read()

            roted_data = ROT.ROTby_encrypt(data, n)

            with open(filename, "w") as file_w:
                file_w.write(roted_data)

            return f"File '{filename}' successfully encrypted"

        except:
            return f"Unable to read the file: '{filename}'. Try change the file path."
    
    def ROTby_decrypt_file(filename, n):
        try:
            with open(filename, "r") as file_r:
                data = file_r.read()

            roted_data = ROT.ROTby_decrypt(data, n)

            with open(filename, "w") as file_w:
                file_w.write(roted_data)

            return f"File '{filename}' successfully decrypted"

        except:
            return f"Unable to read the file: '{filename}'. Try change the file path."