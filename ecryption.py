def encrypt(k, m):
    return ''.join(map(chr, [(ord(c) + k) % 65536 for c in m]))

def decrypt(k, m):
    return ''.join(map(chr, [(ord(c) - k) % 65536 for c in m]))


key = int(input("Введите ключ: "))
text = input("Введите текст: ")


encrypted_text = encrypt(key, text)
print("Зашифрованный текст:", encrypted_text)


decrypted_text = decrypt(key, encrypted_text)
print("Расшифрованный текст:", decrypted_text)
