from hashlib import sha256


def pkcs_encode(data: bytes, sig_len: int):
    digest = sha256(data, usedforsecurity=True).digest()  # 32 bytes

    SHA256_DIGEST_INFO_PREFIX = bytes.fromhex("3031300d060960864801650304020105000420")
    T = SHA256_DIGEST_INFO_PREFIX + digest  # 19 + 32 = 51 bytes

    ps_len = sig_len - 3 - len(T)
    if ps_len < 8:
        raise ValueError("modulus too small for this digest")

    EM = b"\x00\x01" + b"\xff" * ps_len + b"\x00" + T
    assert len(EM) == sig_len

    return EM
