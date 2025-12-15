from abc import ABC, abstractmethod

class AttackPayload(ABC):  # Inherit from ABC to strictly enforce structure
    """
    Base class for an attack transformation module.
    Expects a 'strength' attribute to control intensity.
    """
    def __init__(self, strength: float = 1.0):
        # Ensure strength is between 0.0 and 1.0
        self.strength = max(0.0, min(1.0, strength))

    @abstractmethod
    def transform(self, text: str) -> str:
        """
        Apply the specific obfuscation or manipulation to the payload.
        Subclasses must override this.
        
        Args:
            text (str): The original malicious prompt/string.
            
        Returns:
            str: The transformed payload.
        """
        pass