import re


class Reg:
    # Line Regex
    TIMESTAMP_RE_TEXT = r'D (?P<hour>\d{2}):(?P<min>\d{2}):(?P<sec>\d{2})\.\d{7} '
