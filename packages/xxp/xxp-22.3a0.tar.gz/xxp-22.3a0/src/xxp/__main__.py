import argparse
import sys


def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--cols",
        type=int,
        help="Format <cols> octets per line. Default 16 (-i: 12, -ps: 30)",
    )
    parser.add_argument(
        "-u", "--uppercase", action="store_true", help="use upper case hex letters"
    )
    parser.add_argument(
        "-g",
        "--group",
        type=int,
        help="number of octets per group in normal output. Default 2 (-e: 4).",
    )
    parser.add_argument("input")
    args = parser.parse_args()

    cols = 16
    group = 2

    infile = args.input
    if infile == "-":
        print(sys.stdin.buffer.read(), cols=cols, uppercase=args.uppercase, group=group)
    else:
        with open(args.input, mode="rb") as f:
            print(f.read(), cols=cols, uppercase=args.uppercase, group=group)


if __name__ == "__main__":
    sys.exit(_main())
