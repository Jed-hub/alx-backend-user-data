#!/usr/bin/env python3
""" Filtered logger module """
from typing import List
from re import sub


def filter_datum(fields: List, redaction: str, message: str, separator: str) -> str:
    """
    Returns the log message obfuscated
    """
    for field in fields:
        message = sub(f'{field}=.+?{separator}',
                      f'{field}={redaction}{separator}', message)

    return message
