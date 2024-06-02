import base64
import json

from django.utils import timezone

from Crypto.Cipher import AES
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

from .keys import get_public_key_object


def get_local_time():
    return timezone.now().astimezone(timezone.get_current_timezone())


def encrypt_payload(public_key, data):
    if not isinstance(data, bytes):
        if isinstance(data, dict):
            data = json.dumps(data)
        data = data.encode()
    if isinstance(public_key, str):
        public_key = get_public_key_object(public_key)
    ciphertext = public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    ciphertext = base64.b64encode(ciphertext).decode()
    return ciphertext


def decrypt_payload(private_key, ciphertext):
    if not isinstance(ciphertext, bytes):
        ciphertext = ciphertext.encode()
    ciphertext = base64.b64decode(ciphertext)
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    return plaintext.decode()


def aes_encrypt(encryption_key, payload):
    if isinstance(payload, dict):
        payload = json.dumps(payload)
    if not isinstance(payload, str):
        raise ValueError("Invalid payload")
    encryption_key = encryption_key[:16]
    length = 16 - (len(payload) % 16)
    payload += chr(length) * length
    obj = AES.new(encryption_key, AES.MODE_ECB)
    ciphertext = obj.encrypt(payload)
    ciphertext = base64.b64encode(ciphertext)
    return ciphertext.decode()


def aes_decrypt(encryption_key, ciphertext):
    encryption_key = encryption_key[:16]
    obj2 = AES.new(encryption_key, AES.MODE_ECB)
    ciphertext = base64.b64decode(ciphertext)
    plaintext = obj2.decrypt(ciphertext)
    text = plaintext[: -plaintext[-1]]
    text = text.decode()
    return text


def ip_is_allowed(ip_patterns, ip):
    if not ip_patterns:
        return False
    if isinstance(ip_patterns, str):
        ips = ip_patterns.split(",")
    elif isinstance(ip_patterns, list):
        ips = ip_patterns
    else:
        return False
    for aip in ips:
        aip = aip.strip()
        if aip == "*":
            return True
        elif "-" in aip:
            ip_base, end = aip.split("-")
            allow_base_pattern, start = ip_base.rsplit(".", 1)
            req_base_pattern, to_check = ip.rsplit(".", 1)
            if (allow_base_pattern == req_base_pattern) and (
                int(start) <= int(to_check) <= int(end)
            ):
                return True
        else:
            if aip == ip:
                return True
    return False


def get_chunks(data_list, n):
    """Yield successive n-sized chunks from data list."""
    for i in range(0, len(data_list), n):
        yield data_list[i : i + n]  # noqa


def get_key_or_default(value_dict, key, default_value):
    return value_dict.get(key) or default_value
