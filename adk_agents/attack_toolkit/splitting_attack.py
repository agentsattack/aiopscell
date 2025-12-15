import random
from .base import AttackPayload

class PromptSplittingAttack(AttackPayload):
    """
    Splits a prompt into segments and adds reassembly markers.
    The intention is that these marked segments can be distributed
    throughout a larger body of text.
    """
    def __init__(self, strength: float = 1.0, chunk_size: int = None):
        super().__init__(strength)
        self.chunk_size_config = chunk_size

    def transform(self, text: str) -> str:
        if not text:
            return ""

        current_chunk_size = self.chunk_size_config

        # Determine chunk size automatically if not explicitly configured
        if current_chunk_size is None:
            if self.strength == 0:
                current_chunk_size = 5 
            else:
                # strength 1.0 = small chunks (high fragmentation)
                # strength 0.1 = large chunks (low fragmentation)
                inverse_strength = 1.0 - (self.strength * 0.9) 
                calculated_size = int(len(text) * inverse_strength)
                current_chunk_size = max(5, calculated_size)

        if current_chunk_size < 1:
            current_chunk_size = 1

        # Split text into chunks
        chunks = []
        for i in range(0, len(text), current_chunk_size):
            chunks.append(text[i:i + current_chunk_size])

        if not chunks:
            return text

        # Add reassembly markers
        marked_chunks = []
        total_chunks = len(chunks)
        for i, chunk_content in enumerate(chunks):
            marked_chunks.append(f"[PART_{i+1}_{total_chunks}]{chunk_content}[/PART_{i+1}]")

        return "\n".join(marked_chunks)