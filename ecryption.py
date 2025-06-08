def break_cipher(text):
    import string

    russian_chars = set(
        'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ' +
        'абвгдеёжзийклмнопрстуфхцчшщъыьэюя' +
        string.punctuation + string.whitespace + '0123456789'
    )

    max_score = 0
    decrypted_text = ''
    probable_key = 0

    for k in range(65536):
        attempted_text = ''.join(
            [chr((ord(c) - k) % 65536) for c in text]
        )

        
        score = sum(char in russian_chars for char in attempted_text)

        if score > max_score:
            max_score = score
            decrypted_text = attempted_text
            probable_key = k

    

        if score == len(text):
            break

    print(f"Найденный ключ: {probable_key}")
    return decrypted_text



cipher_text = input("Введите зашифрованный текст: ")
original_text = break_cipher(cipher_text)
print("Расшифрованный текст:", original_text)
