"""
Mostly for checking against the reference implementation, but why not offer
it anyway...
"""

import argparse
import subprocess
import sys


def xxd(data: bytes):
    proc = subprocess.Popen(
        ["xxd", "-"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, _stderr = proc.communicate(data)
    return stdout.decode("ascii")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", help="input file")
    args = parser.parse_args()

    with open(args.infile, mode="rb") as f:
        data = f.read()

    print(xxd(data))


if __name__ == "__main__":
    sys.exit(main())
