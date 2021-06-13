"""
This module provides a few useful functions for dealing with Chinese
text.
"""

import re
from typing import Pattern, List


def extract_chinese_characters(expression: str) -> List[str]:
    """
    This functions takes in a string and returns a list 
    of the Chinese characters present inside.
    """
    character_pattern: Pattern = re.compile("[\\u4e00-\\u9fa5]")
    chinese_characters: List[str] = character_pattern.findall(expression)
    return chinese_characters
