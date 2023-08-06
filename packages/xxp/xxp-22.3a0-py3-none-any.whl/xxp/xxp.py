import base64
import itertools
import string


TEXTABLE = set(string.punctuation + string.ascii_letters + string.digits + " ")


def chunks(seq, n):
    for i in range(0, len(seq), n):
        yield seq[i : i + n]


def generate(bs, cols=16, uppercase=False, group=2):
    if isinstance(bs, str):
        raise TypeError("bs should be a bytestring, not string")
    index = 0
    hexlen = 2 * cols + (cols // group - 1)
    # linefmt = "{index:08x}: {hexed:<{hexlen:}s}  {text:}".replace("{hexlen:}", str(hexlen))
    linefmt = "{index:08x}: {hexed:<{hexlen:}s}  {text:}"
    ibs = iter(bs)
    while True:
        line = bytes(itertools.islice(ibs, cols))
        iline = iter(line)
        if not line:
            break
        hexed = base64.b16encode(line).decode("ascii")
        hexed = " ".join(chunks(hexed, group * 2))
        if not uppercase:
            hexed = hexed.lower()
        text = "".join(c if c in TEXTABLE else "." for c in (chr(c) for c in line))
        yield linefmt.format(index=index, hexed=hexed, hexlen=hexlen, text=text)
        index += cols


def _format(bs, **kwargs):
    return "\n".join(generate(bs)) + "\n"


def _print(bs, **kwargs):
    print(_format(bs, **kwargs))
