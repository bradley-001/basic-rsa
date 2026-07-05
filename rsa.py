from encodings import undefined
import hmac

from core import is_valid_public_exponent, lcm, phi
from prime_number_gen import gen_prime
from pkcs_encoding import pkcs_encode


class Public_key:
    def __init__(self, n: int, e: int) -> None:
        self.n = n
        self.e = e

    def verify(self, data: bytes, signature: bytes) -> bool:
        sig_len = (self.n.bit_length() + 7) // 8
        c = pkcs_encode(data, sig_len)

        s = int.from_bytes(signature, "big")
        o = pow(s, self.e, self.n)

        em = o.to_bytes(sig_len, "big")

        return hmac.compare_digest(em, c)


class Private_key:
    def __init__(
        self, n: int, d: int, p: int, q: int, dp=None, dq=None, qinv=None
    ) -> None:
        self.n = n
        self.d = d
        self.p = p
        self.q = q

        if dp is None or dq is None or qinv is None:
            self.dp = d % (p - 1)
            self.dq = d % (q - 1)
            self.qinv = pow(q, -1, p)
        else:
            self.dp = int(dp)
            self.dq = int(dq)
            self.qinv = int(qinv)

    def sign(self, data: bytes):
        """
        Uses CRT (Chineese Remainder Theorem) via dp, dq & qinv to accelerate the expensive private enrcryption operation
        """
        sig_len = (self.n.bit_length() + 7) // 8
        c = int.from_bytes(pkcs_encode(data, sig_len), "big")

        m1 = pow(c, self.dp, self.p)
        m2 = pow(c, self.dq, self.q)

        h = (self.qinv * (m1 - m2)) % self.p

        return (m2 + h * self.q).to_bytes(sig_len, "big")


def gen_rsa(keySize: int) -> tuple[Public_key, Private_key]:
    e = 65537
    p = gen_prime(keySize)
    q = gen_prime(keySize)
    while p == q and not is_valid_public_exponent(e, phi(p, q)):
        q = gen_prime(keySize)

    n = p * q
    lcm_n = lcm(p - 1, q - 1)

    d = pow(e, -1, lcm_n)

    public_key = Public_key(n, e)
    private_key = Private_key(n, d, p, q)

    return public_key, private_key
