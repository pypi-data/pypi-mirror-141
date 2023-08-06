import re


def reformat_bind_params(q, rewrite=True):
    x = re.compile(r"[^:](:[a-z0-9_]+)")

    xx = x.findall(q)

    parts = []

    remainder = 0

    for m in x.finditer(q):
        g = m.group(1)

        a, b = m.start(1), m.end(1)

        parts.append(q[remainder:a])

        if rewrite:
            varname = q[a + 1 : b]
            parts.append(f"%({varname})s")
        else:
            parts.append(q[a:b])

        remainder = b

    parts.append(q[remainder:])
    return "".join(parts)
