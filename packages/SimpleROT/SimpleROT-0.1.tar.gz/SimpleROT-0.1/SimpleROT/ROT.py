# SimpleROT Library v0.1
# Created by Fix-22 (https://github.com/Fix-22)

# ROT v0.3
# ROT allows you to encrypt string using ROT13 and ROTby methods.

class ROT:

    global alphabet
    global alphabetCAPS
    global symbols

    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", 
                "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", 
                "y", "z"]
    alphabetCAPS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
                    "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", 
                    "U", "V","W","X", "Y", "Z"]

    def ROT13(string):
        roted_string = ""

        for l in string:
            if l in alphabet:
                l_index = alphabet.index(l)
                l_index = l_index + 13
                
                if l_index > 25:
                    l_index = l_index - 26
                    
                new_l = alphabet[l_index]
                roted_string += new_l
            
            elif l in alphabetCAPS:
                l_index_caps = alphabetCAPS.index(l)
                l_index_caps = l_index_caps + 13
                
                if l_index_caps > 25:
                    l_index_caps = l_index_caps - 26
                    
                new_l_caps = alphabetCAPS[l_index_caps]
                roted_string += new_l_caps
            
            elif l in " ":
                roted_string += " "
            
            else:
                roted_string += l
                
        return roted_string
    
    def ROTby_encrypt(string, n):
        roted_string = ""

        if n <= 25:
            for l in string:
                if l in alphabet:
                    l_index = alphabet.index(l)
                    l_index = l_index + n
                    
                    if l_index > 25:
                        l_index = l_index - 26
                        
                    new_l = alphabet[l_index]
                    roted_string += new_l
                
                elif l in alphabetCAPS:
                    l_index_caps = alphabetCAPS.index(l)
                    l_index_caps = l_index_caps + n
                    
                    if l_index_caps > 25:
                        l_index_caps = l_index_caps - 26
                        
                    new_l_caps = alphabetCAPS[l_index_caps]
                    roted_string += new_l_caps
                
                elif l == " ":
                    roted_string += " "
                
                else:
                    roted_string += l
                    

            return roted_string
        else:
            return f"'n' ({n}) out of range"

    def ROTby_decrypt(string, n):
            roted_string = ""

            if n <= 25:
                for l in string:
                    if l in alphabet:
                        l_index = alphabet.index(l)
                        l_index = l_index - n
                        
                        if l_index > 25:
                            l_index = l_index - 26
                            
                        new_l = alphabet[l_index]
                        roted_string += new_l
                    elif l in alphabetCAPS:
                        l_index_caps = alphabetCAPS.index(l)
                        l_index_caps = l_index_caps - n
                        
                        if l_index_caps > 25:
                            l_index_caps = l_index_caps - 26
                            
                        new_l_caps = alphabetCAPS[l_index_caps]
                        roted_string += new_l_caps
                    elif l == " ":
                        roted_string += " "
                    else:
                        roted_string += l
                        

                return roted_string
            else:
                return f"'n' ({n}) out of range"