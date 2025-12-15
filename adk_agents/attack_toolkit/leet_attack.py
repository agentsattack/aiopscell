import random
from .base import AttackPayload

LEET_MAP = {
    'a': ['a', '@', '4'], 'b': ['b', '8'], 'c': ['c', '('], 'e': ['e', '3'],
    'g': ['g', '9', '6'], 'i': ['i', '1', '!', '|'], 'l': ['l', '1', '|'],
    'o': ['o', '0'], 's': ['s', '$', '5'], 't': ['t', '7', '+'], 'z': ['z', '2'],
    'y': ['y', '¥'],
}

class LeetAttack(AttackPayload):
    """
    Replaces characters with their LeetSpeak equivalents.
    """
    def transform(self, text: str) -> str:
        if not text:
            return ""

        result_chars = []
        for original_char in text:
            char_to_append = original_char
            lch = original_char.lower()
            
            if lch in LEET_MAP and random.random() < self.strength:
                if LEET_MAP[lch]:
                    char_to_append = random.choice(LEET_MAP[lch])
            
            result_chars.append(char_to_append)
        
        return ''.join(result_chars)