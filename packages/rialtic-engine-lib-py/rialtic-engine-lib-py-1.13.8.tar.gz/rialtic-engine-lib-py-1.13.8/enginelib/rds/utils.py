import re

_bad_chars = re.compile(r'[^0-9a-zA-z\-_]')


def sql_sanitize(text: str) -> str:
    return _bad_chars.sub("", text)
