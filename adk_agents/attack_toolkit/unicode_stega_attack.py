import random
from .base import AttackPayload

ZERO_WIDTH_CHARS = [
    '\u200B', # Zero-width space
    '\u200C', # Zero-width non-joiner
    '\u200D', # Zero-width joiner
    '\u2060', # Word joiner
    '\u2062', # Invisible times
    '\u2063', # Invisible separator
    '\uFEFF', # Zero-width no-break space
]

class UnicodeStegaAttack(AttackPayload):
    """
    Injects zero-width Unicode characters into the text to obfuscate it.
    """
    def transform(self, text: str) -> str:
        if not text:
            return ""
            
        if not ZERO_WIDTH_CHARS:
            return text

        result_chars = []
        
        # STRATEGY 1: Low Strength (Word Boundaries Only)
        if self.strength < 0.3:
            for char in text:
                result_chars.append(char)
                if char == ' ':
                    result_chars.append(random.choice(ZERO_WIDTH_CHARS))
            return ''.join(result_chars)

        # STRATEGY 2: Medium Strength (Context/Length Aware)
        elif self.strength < 0.7:
            words = text.split(' ')
            processed_words = []
            for word in words:
                if len(word) <= 3:
                    processed_words.append(word)
                    continue
                
                # If word is long, inject INSIDE it
                new_word = []
                for char in word:
                    new_word.append(char)
                    # 50% chance to inject after a char in a long word
                    if random.random() < 0.5:
                        new_word.append(random.choice(ZERO_WIDTH_CHARS))
                processed_words.append(''.join(new_word))
            
            return ' '.join(processed_words)

        # STRATEGY 3: High Strength (Aggressive Saturation)
        else:
            for char in text:
                result_chars.append(char)
                num_to_inject = random.randint(1, 3)
                for _ in range(num_to_inject):
                    result_chars.append(random.choice(ZERO_WIDTH_CHARS))
            return ''.join(result_chars)