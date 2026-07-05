import random
import gmpy2
from small_primes import small_primes


def gen_prime(byteSize: int) -> int:
    candidate = 0
    while True:
        candidate = _genRandomNumber(byteSize)
        if _is_prime_miller_rabin(candidate):
            break
    return candidate


def _genRandomNumber(byteSize: int):
    return (
        int.from_bytes(random.randbytes(byteSize), byteorder="big")
        | 1
        | (1 << (byteSize * 8 - 1))
    )


def _is_prime_miller_rabin(candidate, rounds=30):
    if candidate < 2:
        return False
    if candidate == 2:
        return True
    if candidate % 2 == 0:
        return False
    if not _is_prime_small_primes_check(candidate):
        return False

    odd_part = candidate - 1
    twos = 0
    while odd_part % 2 == 0:
        odd_part //= 2
        twos += 1

    # random.sample can't handle ranges larger than C ssize_t (~9.2e18).
    # random.randrange works with arbitrary-precision Python ints.
    k = min(rounds, candidate - 3)
    witnesses = set()
    while len(witnesses) < k:
        witnesses.add(random.randrange(2, candidate - 1))

    for witness in witnesses:
        current = gmpy2.powmod(witness, odd_part, candidate)
        if current == 1 or current == candidate - 1:
            continue

        for _ in range(twos - 1):
            current = gmpy2.powmod(current, 2, candidate)
            if current == candidate - 1:
                break
        else:
            return False  # witness provded candidate is composite

    return True


def _is_prime_small_primes_check(val):
    for prime in small_primes:
        if val == prime:
            return True  # val is itself one of the known primes
        if val % prime == 0:
            return False
    return True
