def gcd(a: int, b: int) -> int:
    """Euclid's algorithm. The greatest common divisor of (a, b) is the the GCD of (b, a mod b). Keep shrinking until second value reaches zero.

    I.e. (18,12) -> (12,6) -> (6,0) = answer is 6.
    Two numbers are coprime if gcd(a,b) = 1. Meaning they share no prime factors.
    """

    while b != 0:
        a, b = b, a % b
    return a


def lcm(a: int, b: int):
    return a * b // gcd(a, b)


def is_valid_public_exponent(e: int, phi_n: int) -> bool:
    """
    e is a usable public exponent if 1 < e < phi(n) and e is coprime to phi(n)
    """
    return 1 < e < phi_n and gcd(e, phi_n) == 1


def phi(p: int, q: int) -> int:
    """
    Phi function provides the number of coprimes of the product of p & q (N)
    """
    return (p - 1) * (q - 1)
