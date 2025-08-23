"""
Turkish Tokenizer

A comprehensive Turkish language tokenizer.
Provides state-of-the-art tokenization and text generation capabilities for Turkish.
"""

__version__ = "0.2.24"
__author__ = "M. Ali Bayram"
__email__ = "malibayram20@gmail.com"

from .turkish_decoder import TurkishDecoder
from .turkish_tokenizer import TokenType, TurkishTokenizer

# Conditionally import HFTurkishTokenizer if transformers is available
try:
    from .hf_turkish_tokenizer import HFTurkishTokenizer
    HF_TOKENIZER_AVAILABLE = True
except (ImportError, TypeError):
    HF_TOKENIZER_AVAILABLE = False
    HFTurkishTokenizer = None

__all__ = [
    # Tokenizer
    "TurkishTokenizer",
    "TokenType",
    "TurkishDecoder",
]

# Add HFTurkishTokenizer to __all__ only if available
if HF_TOKENIZER_AVAILABLE:
    __all__.append("HFTurkishTokenizer")

# Package metadata
__title__ = "turkish-tokenizer"
__description__ = "Turkish tokenizer for Turkish language processing"
__url__ = "https://github.com/malibayram/turkish-tokenizer"
__license__ = "MIT"
