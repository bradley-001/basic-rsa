import argparse
import os
import sys

from files import (
    gen_random_filename,
    read_bytes,
    read_bytes_from_base64,
    read_key,
    write_bytes_as_base64,
    write_key,
)
from rsa import Private_key, Public_key, gen_rsa

SIGNATURE_SUFFIX = ".sig"


def build_parser():
    parser = argparse.ArgumentParser(
        prog="brsa",
        description="Generate, sign, and verify RSA keys.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    gen = subparsers.add_parser("gen", help="Generate an RSA key pair.")
    gen.add_argument(
        "-s",
        "--size",
        type=int,
        default=256,
        help="Key size in bytes (default: 256).",
    )
    gen.add_argument(
        "-n",
        "--name",
        default=None,
        help="Base name for the key files, producing <name>.key/<name>.pub "
        "(default: random hex string).",
    )
    gen.add_argument(
        "-o",
        "--out",
        default=".",
        help="Directory to write the key files to (default: current directory).",
    )

    sign = subparsers.add_parser("sign", help="Sign a file with a private key.")
    sign.add_argument("filename", help="File to sign.")
    sign.add_argument("private_keyfile", help="Private key to sign with.")

    verify = subparsers.add_parser(
        "verify", help="Verify a signature against a public key."
    )
    verify.add_argument(
        "signature_file",
        help=f"Signature file to verify (must end in '{SIGNATURE_SUFFIX}'; "
        "the signed file's name is derived by stripping that suffix).",
    )
    verify.add_argument("public_keyfile", help="Public key to verify with.")

    return parser


def _cmd_gen(args):
    public_key, private_key = gen_rsa(args.size)
    name = args.name or gen_random_filename()

    key_path = os.path.join(args.out, f"{name}.key")
    pub_path = os.path.join(args.out, f"{name}.pub")

    write_key(key_path, private_key)
    write_key(pub_path, public_key)
    print(f"Wrote {key_path} and {pub_path}")


def _cmd_sign(args):
    private_key = read_key(args.private_keyfile)
    if not isinstance(private_key, Private_key):
        raise TypeError(f"{args.private_keyfile} is not a private key")

    data = read_bytes(args.filename)
    signature = private_key.sign(data)

    out_path = f"{args.filename}{SIGNATURE_SUFFIX}"
    write_bytes_as_base64(out_path, signature)
    print(f"Wrote {out_path}")


def _cmd_verify(args):
    if not args.signature_file.endswith(SIGNATURE_SUFFIX):
        raise ValueError(
            f"signature file must end in '{SIGNATURE_SUFFIX}' "
            "so the signed file's name can be derived from it"
        )

    public_key = read_key(args.public_keyfile)
    if not isinstance(public_key, Public_key):
        raise TypeError(f"{args.public_keyfile} is not a public key")

    data_filename = args.signature_file[: -len(SIGNATURE_SUFFIX)]
    data = read_bytes(data_filename)
    signature = read_bytes_from_base64(args.signature_file)

    if public_key.verify(data, signature):
        print("Signature is valid.")
    else:
        print("Signature is INVALID.")
        sys.exit(1)


def main():
    args = build_parser().parse_args()

    try:
        if args.command == "gen":
            _cmd_gen(args)
        elif args.command == "sign":
            _cmd_sign(args)
        elif args.command == "verify":
            _cmd_verify(args)
    except (FileNotFoundError, ValueError, TypeError) as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
