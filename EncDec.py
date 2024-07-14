def encrypt(phrase, key):
    """Encrypts the input by modifying the unicode based on the key"""
    encryption = ""
    key_uni = []
    for letter in key:
        key_uni.append(ord(letter))
    phrase_index = key_index = 0
    while phrase_index < len(phrase):
        if key_index >= len(key_uni):
            key_index = 0
        phrase_uni = ord(phrase[phrase_index]) + key_uni[key_index]
        while phrase_uni > 126:     # Keeps the valid range of unicode from 32-126
            phrase_uni -= 94
        encryption += chr(phrase_uni)
        phrase_index += 1
        key_index += 1
    return encryption


def decrypt(phrase, key):
    """Decrypts the input by modifying the unicode based on the key"""
    decryption = ""
    key_uni = []
    for letter in key:
        key_uni.append(ord(letter))
    phrase_index = key_index = 0
    while phrase_index < len(phrase):
        if key_index >= len(key_uni):
            key_index = 0
        phrase_uni = ord(phrase[phrase_index]) - key_uni[key_index]
        while phrase_uni < 32:      # Keeps the valid range of unicode from 32-126
            phrase_uni += 94
        decryption += chr(phrase_uni)
        phrase_index += 1
        key_index += 1
    return decryption