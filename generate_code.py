#!/usr/bin/env python3

import re
import sys
from datetime import datetime, timedelta
from typing import List, Tuple

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


# name in wxapkg: generate3MinValidData.
def generate_3min_salt() -> str:
    delta = datetime.now() - datetime(2000, 1, 1)
    num = round(delta // timedelta(seconds=1) / 180)

    a = str(num)
    a = '0' * (8 - len(a)) + a

    b = format(num, 'X')
    b = '0' * (8 - len(b)) + b

    return a + b


# name in wxapkg: getLongValidTime, generateLongValidData.
def generate_longterm_salt(due_date: datetime) -> Tuple[int, str]:
    delta = due_date - datetime(2000, 1, 1)
    num = round(delta // timedelta(seconds=1) / 43200)

    a = str(num)
    a = '0' * (8 - len(a)) + a

    b = format(num, 'X')
    b = '0' * (8 - len(b)) + b

    return num, a + b


# DES-ECB encrypt.
# TripleDES + triple key + triple message = triple ciphertext
def des(key: str, message: str) -> str:
    backend = default_backend()
    cipher = Cipher(algorithms.TripleDES(bytes.fromhex(key) * 3), modes.ECB(), backend=backend)
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(bytes.fromhex(message) * 3)

    return ciphertext.hex()[8:16]


def generate_3min_passcode(secret: str) -> str:
    secret_hex = format(int(secret), 'X')
    secret_hex = '0' * (8 - len(secret_hex)) + secret_hex

    key = secret + secret_hex
    salt = generate_3min_salt()
    ciphertext = des(key, salt)

    a = (int(ciphertext[0:4], 16) ^ int(secret[0:4], 16)) & 0x03FF
    b = (int(ciphertext[4:8], 16) ^ int(secret[4:8], 16)) & 0xFFFF
    code = format(a, 'x') + format(b, 'x')
    code = str(int(code, 16))
    code = '0' * (8 - len(code)) + code

    return code


def generate_longterm_passcode(secret: str, due_date: datetime) -> str:
    secret_hex = format(int(secret), 'X')
    secret_hex = '0' * (8 - len(secret_hex)) + secret_hex

    key = secret + secret_hex
    salt_num, salt = generate_longterm_salt(due_date)
    ciphertext = des(key, salt)

    a = (salt_num >> 1) % 3 + 7
    b = str(int(ciphertext, 16))[-2:]
    u = 100 * a + int(b)
    v = 255 - (255 & u) << 8 | 255 & u
    if salt_num > 65535:
        c = str(salt_num ^ u)[-5:]
    else:
        c = str(salt_num ^ v)[-5:]
    code = str(a) + b + c

    return code


def validate_secret(secret: str) -> str:
    if re.match(r'^[0-9]{8}$', secret):
        return secret
    else:
        sys.exit('Invalid secret format')


def validate_date(date_argv: List[str]) -> datetime:
    # valid date: '2000-01-01' to '2099-12-31'
    # valid time: '00:00' or '12:00'
    try:
        date_list = [int(i) for i in date_argv]
        if date_list[0] < 2000 or date_list[0] > 2099 or date_list[3] not in [0, 12]:
            raise ValueError('date out of range')
        return datetime(*date_list)
    except ValueError as e:
        sys.exit(f'Invalid date format: {e}')


if __name__ == '__main__':
    if len(sys.argv) == 2:
        # 3 minutes temporary passcode
        # param: secret
        # example usage: ./generate_code.py 12345678
        secret = validate_secret(sys.argv[1])
        code = generate_3min_passcode(secret)
        print(code)

    elif len(sys.argv) == 6:
        # longterm passcode
        # param: secret, year, month, day, hour
        # example usage: ./generate_code.py 12345678 2050 6 15 0
        secret = validate_secret(sys.argv[1])
        due_date = validate_date(sys.argv[2:])
        code = generate_longterm_passcode(secret, due_date)
        print(code)

    else:
        sys.exit('Need 1 or 5 arguments')

