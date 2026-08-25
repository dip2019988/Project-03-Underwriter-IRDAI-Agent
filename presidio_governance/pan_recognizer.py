import re


def find_pan_numbers(text):

    pattern = r"[A-Z]{5}[0-9]{4}[A-Z]{1}"

    return re.findall(pattern, text)