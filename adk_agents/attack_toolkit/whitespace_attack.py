from .base import AttackPayload

class WEncodingAttack(AttackPayload):
    """
    Encodes the prompt into a sequence of space and tab characters
    representing its binary form (Steganography).
    """
    def transform(self, text: str) -> str:
        if not text:
            return ""

        try:
            # Convert text to UTF-8 bytes first to handle emojis/unicode
            byte_data = text.encode('utf-8')
            # Convert bytes to binary string (8 bits per byte)
            binary_representation = ''.join(format(b, '08b') for b in byte_data)
        except Exception as e:
            print(f"Could not convert text to binary: {e}")
            return text

        # Encode the binary string: '0' -> space, '1' -> tab
        whitespace_encoding = binary_representation.replace('0', ' ').replace('1', '\t')
        
        return whitespace_encoding