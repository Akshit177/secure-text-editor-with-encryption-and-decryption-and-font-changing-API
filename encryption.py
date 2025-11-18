HEADER = ":::ENCRYPTED:::"
TAG_PREFIX = "::TAG::"

def _shift_from_password(password):
    return sum(ord(c) for c in password) % 26

def _tag_from_password(password):
    return str(sum(ord(c) * (i + 1) for i, c in enumerate(password)) % 99999)

def _caesar_cipher(text, shift):
    result = []
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            result.append(chr((ord(ch) - base + shift) % 26 + base))
        else:
            result.append(ch)
    return ''.join(result)

def is_encrypted(data):
    return data.startswith(HEADER)

def encrypt_text(text, password):
    shift = _shift_from_password(password)
    tag = _tag_from_password(password)
    encrypted = _caesar_cipher(text, shift)
    return f"{HEADER}\n{TAG_PREFIX}{tag}\n{encrypted}"

def decrypt_text(data, password):
    if not is_encrypted(data):
        return data

    try:
        _, tag_line, encrypted = data.split("\n", 2)
    except ValueError:
        raise ValueError("Corrupted encrypted file format.")

    stored_tag = tag_line.replace(TAG_PREFIX, "").strip()
    if stored_tag != _tag_from_password(password):
        raise ValueError("Incorrect password — decryption failed.")

    shift = _shift_from_password(password)
    return _caesar_cipher(encrypted, -shift)

