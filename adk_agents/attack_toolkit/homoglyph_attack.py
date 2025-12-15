import random
from .base import AttackPayload

HOMOGLYPH_MAP = {
    'a': ['a', 'а', 'α'], 'b': ['b', 'в', 'Ь'], 'c': ['c', 'с'], 'd': ['d'],
    'e': ['e', 'е'], 'f': ['f'], 'g': ['g'], 'h': ['h', 'н'],
    'i': ['i', 'і', 'ι'], 'j': ['j', 'ј'], 'k': ['k', 'κ'], 'l': ['l'],
    'm': ['m', 'м'], 'n': ['n'], 'o': ['o', 'о', 'ο'], 'p': ['p', 'р', 'ρ'],
    'q': ['q'], 'r': ['r'], 's': ['s', 'ѕ'], 't': ['t', 'т', 'τ'],
    'u': ['u', 'υ'], 'v': ['v', 'ν'], 'w': ['w'], 'x': ['x', 'х', 'χ'],
    'y': ['y', 'у', 'γ'], 'z': ['z'],
}

class HomoglyphAttack(AttackPayload):
    """
    Replaces characters with their homoglyph equivalents
    based on the strength attribute.
    """
    def transform(self, text: str) -> str:
        if not text:
            return ""

        result_chars = []
        for original_char in text:
            char_to_append = original_char
            lch = original_char.lower()
            
            if lch in HOMOGLYPH_MAP and random.random() < self.strength:
                if HOMOGLYPH_MAP[lch]:
                    char_to_append = random.choice(HOMOGLYPH_MAP[lch])
            
            result_chars.append(char_to_append)
        
        return ''.join(result_chars)
