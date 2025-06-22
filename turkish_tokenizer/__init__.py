"""
Turkish Tokenizer - High-performance Turkish tokenizer with Rust backend.

This package provides a fast and accurate Turkish tokenizer that combines
linguistic rules with BPE (Byte Pair Encoding) for optimal tokenization
of Turkish text.
"""

from .core import decode_text, tokenize
from .tokenizer import TurkishTokenizer
from .version import __version__
from .wrapper import tokenize_text

__all__ = [
    "TurkishTokenizer",
    "tokenize_text",
    "tokenize",
    "__version__",
]

# Convenience function for quick tokenization
def tokenize(text: str) -> tuple[list[str], list[int]]:
    """
    Quick tokenization function for simple use cases.
    
    Args:
        text: The text to tokenize
        
    Returns:
        Tuple of (tokens, token_ids)
    """
    tokenizer = TurkishTokenizer()
    return tokenizer.tokenize(text)
