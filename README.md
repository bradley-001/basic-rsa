# rsa-testing

A small RSA implementation from scratch, wrapped in a CLI called `brsa`. Part of a broader learning/research undertaken to understand the principle mathematics behind modern cryptography. The library generates it's own primes using a custom written Miller-Rabin primality test that defaults to 30 rounds. This produces a prime number with over 24 9s of confidence. (i.e. 99.99999...% prime).

The implementation uses SHA256 and currently I have not written support for SHA512.

Signing uses CRT (Chineese Remainder Theorem) to split the signing operation into two half sized exponentiaions. About a 3x/4x speed improvement over textbook RSA and mirrors what most RSA implemenations use.

> [!CAUTION] CAUTION
This code is **not** suitable for production use or use for genuine security purposes. This is a educational exercise into RSA. Real world implementations have additional protections and mitigations for advanced cryptographic attacks that this does not. I.e. Constant-time execution and blinding processes.

## Install

Needs [uv](https://docs.astral.sh/uv/) and Python 3.11+.
PyPy@3.11 is recommended for preformance improvements.

```
uv sync
```

This installs `brsa` into `.venv/bin`. Run it with `uv run brsa ...`, or put it on your `PATH` with:

```
uv tool install .
```

## Usage

Generate a key pair:

```
brsa gen -s 256 -n mykey
```

Writes `mykey.key` (private) and `mykey.pub` (public) to the current directory. `-s` sets the key size in bytes (default 256), `-n` sets the file base name (default: random hex string), `-o` sets an output directory.

Sign a file:

```
brsa sign message.txt mykey.key
```

Writes `message.txt.sig` next to it.

Verify a signature:

```
brsa verify message.txt.sig mykey.pub
```

The signature filename must end in `.sig` — the original file is looked up by stripping that suffix, so `message.txt.sig` is checked against `message.txt`.

Exits non-zero if verification fails or something goes wrong.
