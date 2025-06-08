def encrypt(key, message):
    return ''.join(chr((ord(c) + key) % 65536) for c in message)

def decrypt(key, message):
    return ''.join(chr((ord(c) - key) % 65536) for c in message)


def score_text(text, language='ru'):
    common_chars = {
        'ru': {
            ' ': 0.175, 'о': 0.110, 'е': 0.085, 'а': 0.080, 'и': 0.074,
            'н': 0.067, 'т': 0.063, 'с': 0.055, 'р': 0.047, 'в': 0.045
        },
        'en': {
            ' ': 0.183, 'e': 0.120, 't': 0.091, 'a': 0.081, 'o': 0.077,
            'i': 0.073, 'n': 0.070, 's': 0.063, 'r': 0.060, 'h': 0.059
        }
    }

    char_freqs = common_chars.get(language.lower(), common_chars['ru'])

    from collections import Counter
    text_length = len(text)
    if text_length == 0:
        return 0

    char_counts = Counter(text.lower())

    score = 0
    for char, expected_freq in char_freqs.items():
        actual_freq = char_counts.get(char, 0) / text_length
        score += (1 - abs(actual_freq - expected_freq)) * expected_freq

    return score


def break_cipher(text, language='ru', max_candidates=3):


    from collections import Counter

    if not text:
        return [], None


    counter = Counter(text)

    most_common_chars = [char for char, _ in counter.most_common(10)]

    common_chars = {
        'ru': [' ', 'о', 'е', 'а', 'и', 'н', 'т', 'с', 'р', 'в'],
        'en': [' ', 'e', 't', 'a', 'o', 'i', 'n', 's', 'r', 'h']
    }

    freq_chars = common_chars.get(language.lower(), common_chars['ru'])


    candidates = []
    for cipher_char in most_common_chars:
        for plain_char in freq_chars:
            key = (ord(cipher_char) - ord(plain_char)) % 65536
            decrypted = decrypt(key, text)
            score = score_text(decrypted, language)
            candidates.append((decrypted, key, score))


    candidates.sort(key=lambda x: x[2], reverse=True)

    
    return candidates[:max_candidates]


if __name__ == "__main__":
    try:
        key = int(input("Введите ключ для шифрования (целое число): "))
    except ValueError:
        print("Ошибка: ключ должен быть целым числом!")
        exit(1)

    plain_text = input("Введите текст для шифрования: ")


    encrypted_text = encrypt(key, plain_text)
    print("\nЗашифрованный текст:\n", encrypted_text)



    language = input("Выберите язык для анализа (ru/en), по умолчанию русский: ").lower()
    if language not in ['ru', 'en']:
        language = 'ru'

    
    print("\nПытаемся восстановить текст...")
    candidates = break_cipher(encrypted_text, language)

    if candidates:
        print("\nТоп вариантов расшифровки (в порядке убывания вероятности):")
        for i, (candidate_text, candidate_key, score) in enumerate(candidates, 1):
            print(f"\n{i}. Ключ: {candidate_key}, Оценка: {score:.4f}")
            print(f"Текст: {candidate_text[:100]}{'...' if len(candidate_text) > 100 else ''}")

        if any(candidate_key == key for _, candidate_key, _ in candidates):
            print("\nУспех! Правильный ключ найден среди кандидатов.")
        else:
            print("\nВнимание: правильный ключ не найден среди кандидатов.")
    else:
        print("\nНе удалось расшифровать текст.")


    print("\nДля сравнения, правильная расшифровка с исходным ключом:")
    print(decrypt(key, encrypted_text))
