import string
import numpy as np

ALPHABET = string.ascii_uppercase

# Vigenere

def vigenere_encrypt(plaintext: str, key: str) -> str:
    plaintext = plaintext.upper()
    key = key.upper()
    result = []
    ki = 0
    for ch in plaintext:
        if ch in ALPHABET:
            pi = ALPHABET.index(ch)
            ki_mod = ALPHABET.index(key[ki % len(key)])
            ci = (pi + ki_mod) % 26
            result.append(ALPHABET[ci])
            ki += 1
        else:
            result.append(ch)
    return ''.join(result)


def vigenere_decrypt(ciphertext: str, key: str) -> str:
    ciphertext = ciphertext.upper()
    key = key.upper()
    result = []
    ki = 0
    for ch in ciphertext:
        if ch in ALPHABET:
            ci = ALPHABET.index(ch)
            ki_mod = ALPHABET.index(key[ki % len(key)])
            pi = (ci - ki_mod + 26) % 26
            result.append(ALPHABET[pi])
            ki += 1
        else:
            result.append(ch)
    return ''.join(result)

# Affine

def _modinv(a: int, m: int) -> int:
    # modular inverse using extended euclid
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError(f"No modular inverse for {a} mod {m}")


def affine_encrypt(plaintext: str, a: int, b: int) -> str:
    plaintext = plaintext.upper()
    if np.gcd(a, 26) != 1:
        raise ValueError("Key 'a' must be coprime with 26")
    result = []
    for ch in plaintext:
        if ch in ALPHABET:
            p = ALPHABET.index(ch)
            c = (a * p + b) % 26
            result.append(ALPHABET[c])
        else:
            result.append(ch)
    return ''.join(result)


def affine_decrypt(ciphertext: str, a: int, b: int) -> str:
    ciphertext = ciphertext.upper()
    if np.gcd(a, 26) != 1:
        raise ValueError("Key 'a' must be coprime with 26")
    a_inv = _modinv(a, 26)
    result = []
    for ch in ciphertext:
        if ch in ALPHABET:
            c = ALPHABET.index(ch)
            p = (a_inv * (c - b)) % 26
            result.append(ALPHABET[p])
        else:
            result.append(ch)
    return ''.join(result)

# Playfair

def _generate_playfair_table(key: str):
    key = key.upper().replace('J', 'I')
    seen = set()
    table = []
    for ch in key:
        if ch in ALPHABET and ch not in seen and ch != 'J':
            seen.add(ch)
            table.append(ch)
    for ch in ALPHABET:
        if ch not in seen and ch != 'J':
            seen.add(ch)
            table.append(ch)
    return [table[i * 5:(i + 1) * 5] for i in range(5)]


def _find_pos(table, ch):
    for i, row in enumerate(table):
        for j, c in enumerate(row):
            if c == ch:
                return i, j
    return None


def _prepare_playfair_text(text: str, encrypt=True):
    text = text.upper().replace('J', 'I')
    cleaned = ''
    for ch in text:
        if ch in ALPHABET:
            cleaned += ch
    result = ''
    i = 0
    while i < len(cleaned):
        a = cleaned[i]
        b = cleaned[i+1] if i+1 < len(cleaned) else 'X'
        if a == b:
            result += a + 'X'
            i += 1
        else:
            result += a + b
            i += 2
    if len(result) % 2 == 1:
        result += 'X'
    return result


def playfair_encrypt(plaintext: str, key: str) -> str:
    table = _generate_playfair_table(key)
    pairs = _prepare_playfair_text(plaintext)
    result = ''
    for i in range(0, len(pairs), 2):
        a, b = pairs[i], pairs[i+1]
        ra, ca = _find_pos(table, a)
        rb, cb = _find_pos(table, b)
        if ra == rb:
            result += table[ra][(ca + 1) % 5]
            result += table[rb][(cb + 1) % 5]
        elif ca == cb:
            result += table[(ra + 1) % 5][ca]
            result += table[(rb + 1) % 5][cb]
        else:
            result += table[ra][cb]
            result += table[rb][ca]
    return result


def playfair_decrypt(ciphertext: str, key: str) -> str:
    table = _generate_playfair_table(key)
    text = ''.join(ch for ch in ciphertext.upper() if ch in ALPHABET)
    result = ''
    for i in range(0, len(text), 2):
        a, b = text[i], text[i+1]
        ra, ca = _find_pos(table, a)
        rb, cb = _find_pos(table, b)
        if ra == rb:
            result += table[ra][(ca - 1) % 5]
            result += table[rb][(cb - 1) % 5]
        elif ca == cb:
            result += table[(ra - 1) % 5][ca]
            result += table[(rb - 1) % 5][cb]
        else:
            result += table[ra][cb]
            result += table[rb][ca]
    # Note: removing padding X's is nontrivial; we'll leave them
    return result

# Hill cipher (2x2)

def _text_to_numbers(text: str):
    return [ALPHABET.index(ch) for ch in text]

def _numbers_to_text(nums):
    return ''.join(ALPHABET[n % 26] for n in nums)


def _matrix_mod_inv(matrix, modulus=26):
    # Only for 2x2
    det = int(round(np.linalg.det(matrix)))
    det_inv = _modinv(det, modulus)
    inv_mat = det_inv * np.round(det * np.linalg.inv(matrix)).astype(int) % modulus
    return inv_mat


def hill_encrypt(plaintext: str, key_matrix: list) -> str:
    # key_matrix should be list of lists 2x2
    matrix = np.array(key_matrix)
    if matrix.shape != (2, 2):
        raise ValueError("Key matrix must be 2x2")
    plaintext = ''.join(ch for ch in plaintext.upper() if ch in ALPHABET)
    if len(plaintext) % 2 == 1:
        plaintext += 'X'
    nums = _text_to_numbers(plaintext)
    result_nums = []
    for i in range(0, len(nums), 2):
        pair = np.array(nums[i:i+2])
        cipher_pair = matrix.dot(pair) % 26
        result_nums.extend(cipher_pair.tolist())
    return _numbers_to_text(result_nums)


def hill_decrypt(ciphertext: str, key_matrix: list) -> str:
    matrix = np.array(key_matrix)
    inv = _matrix_mod_inv(matrix)
    text = ''.join(ch for ch in ciphertext.upper() if ch in ALPHABET)
    nums = _text_to_numbers(text)
    result_nums = []
    for i in range(0, len(nums), 2):
        pair = np.array(nums[i:i+2])
        plain_pair = inv.dot(pair) % 26
        result_nums.extend(plain_pair.tolist())
    return _numbers_to_text(result_nums)

# Enigma - simplified implementation

# Using rotors I, II, III and reflector B
ROTOR_WIRINGS = {
    'I':    "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
    'II':   "AJDKSIRUXBLHWTMCQGZNPYFVOE",
    'III':  "BDFHJLCPRTXVZNYEIWGAKMUSQO",
}
ROTOR_NOTCH = {
    'I': 'Q',
    'II': 'E',
    'III': 'V',
}
REFLECTOR_B = "YRUHQSLDPXNGOKMIEBFZCWVJAT"


def _rotor_forward(ch, wiring, pos, ring):
    idx = (ALPHABET.index(ch) + pos - ring) % 26
    out = wiring[idx]
    return ALPHABET[(ALPHABET.index(out) - pos + ring) % 26]


def _rotor_backward(ch, wiring, pos, ring):
    idx = (ALPHABET.index(ch) + pos - ring) % 26
    # find in wiring
    j = wiring.index(ALPHABET[idx])
    return ALPHABET[(j - pos + ring) % 26]


def enigma_encrypt_decrypt(text: str, rotors: list, positions: list, rings: list) -> str:
    # rotors: list of names ['I','II','III'] order from right to left
    # positions: list of ints 0-25 for each rotor's starting pos
    # rings: list of ints 0-25 for ring settings
    result = ''
    for ch in text.upper():
        if ch not in ALPHABET:
            result += ch
            continue
        # step rotors (rightmost always steps)
        # double stepping simplified
        if rotors:
            # rightmost index 0
            positions[0] = (positions[0] + 1) % 26
            # middle rotor step if rightmost at notch
            if len(rotors) > 1 and ALPHABET[positions[0]] == ROTOR_NOTCH[rotors[0]]:
                positions[1] = (positions[1] + 1) % 26
            # left rotor step if middle at notch
            if len(rotors) > 2 and ALPHABET[positions[1]] == ROTOR_NOTCH[rotors[1]]:
                positions[2] = (positions[2] + 1) % 26
        # pass through rotors forward
        c = ch
        for i, rotor in enumerate(rotors):
            c = _rotor_forward(c, ROTOR_WIRINGS[rotor], positions[i], rings[i])
        # reflector
        idx = ALPHABET.index(c)
        c = REFLECTOR_B[idx]
        # backwards
        for i, rotor in enumerate(reversed(rotors)):
            idxr = len(rotors) - 1 - i
            c = _rotor_backward(c, ROTOR_WIRINGS[rotor], positions[idxr], rings[idxr])
        result += c
    return result
