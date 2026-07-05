import base64
import random

from rsa import Private_key, Public_key


def read_bytes(filepath: str) -> bytes:
    with open(filepath, "rb") as f:
        return f.read()


def write_bytes(filepath: str, data: bytes) -> None:
    with open(filepath, "wb") as f:
        f.write(data)


def write_bytes_as_base64(filepath: str, data: bytes) -> None:
    with open(filepath, "w") as f:
        f.write(base64.b64encode(data).decode(encoding="utf-8"))


def read_bytes_from_base64(filepath: str) -> bytes:
    with open(filepath, "r") as f:
        return base64.b64decode(f.read())


def read_key(filepath: str) -> Public_key | Private_key:
    with open(filepath, "r") as f:
        lines = f.read().strip().splitlines()

    fields = dict(line.split(":", 1) for line in lines)

    if fields["type"] == "publickey":
        return Public_key(int(fields["n"]), int(fields["e"]))
    if fields["type"] == "privatekey":
        return Private_key(
            int(fields["n"]), int(fields["d"]), int(fields["p"]), int(fields["q"])
        )

    raise ValueError(f"Unknown key type: {fields['type']!r}")


def write_key(filepath: str, key: Public_key | Private_key) -> None:
    if isinstance(key, Public_key):
        lines = ["type:publickey", f"n:{key.n}", f"e:{key.e}"]
    elif isinstance(key, Private_key):
        lines = [
            "type:privatekey",
            f"n:{key.n}",
            f"d:{key.d}",
            f"p:{key.p}",
            f"q:{key.q}",
        ]
    else:
        raise TypeError(f"Unsupported key type: {type(key)!r}")

    with open(filepath, "w") as f:
        f.write("\n".join(lines) + "\n")


def gen_random_filename(noOfBytes: int = 4):
    return random.randbytes(noOfBytes).hex()
