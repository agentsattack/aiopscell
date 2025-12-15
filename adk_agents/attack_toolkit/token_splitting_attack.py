from .base import AttackPayload

class TokenSplittingAttack(AttackPayload):
    """
    Deterministically splits words to break tokenizer boundaries using
    invisible characters (Zero Width Space).
    """
    def transform(self, text: str) -> str:
        if not text:
            return ""
            
        # Zero-width space
        splitter = '\u200B' 
        
        words = text.split(' ')
        processed_words = []
        
        for word in words:
            # Split long words in the middle to break BPE tokens
            if len(word) > 1:
                mid_point = len(word) // 2
                new_word = word[:mid_point] + splitter + word[mid_point:]
                processed_words.append(new_word)
            else:
                processed_words.append(word)
        
        return ' '.join(processed_words)