def remove_char(s, n):
    if n <= len(s) - 1:
        s = s[:n] + s[n + 1 :]
        return s
    else:
        return "error index char outside"


def remove_substring(s, n, i):
    if n <= len(s) and i <= len(s):
        s = s[:n] + s[i:]
        return s
    else:
        return "error index substring outside"
