"""
Turkish Tokenizer - Rust Implementation

A high-performance Turkish language tokenizer built with Rust for fast
morphological text processing.
"""

from .turkish_tokenizer_rs import Token, TokenType, TurkishTokenizer

__all__ = ["TurkishTokenizer", "Token", "TokenType"]
__version__ = "0.1.0"
