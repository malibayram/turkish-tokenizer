"""
Turkish Tokenizer

A comprehensive Turkish language tokenizer.
Provides state-of-the-art tokenization and text generation capabilities for Turkish.
"""

__version__ = "0.2.7"
__author__ = "M. Ali Bayram"
__email__ = "malibayram20@gmail.com"

from .turkish_decoder import TurkishDecoder
from .turkish_tokenizer import TokenType, TurkishTokenizer

__all__ = [
    # Tokenizer
    "TurkishTokenizer",
    "TokenType",
    "TurkishDecoder",
]

# Package metadata
__title__ = "turkish-tokenizer"
__description__ = "Turkish tokenizer for Turkish language processing"
__url__ = "https://github.com/malibayram/turkish-tokenizer"
__license__ = "MIT"
