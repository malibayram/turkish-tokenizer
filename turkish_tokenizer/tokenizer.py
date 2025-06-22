"""
Main TurkishTokenizer class providing a clean interface for tokenization.
"""

import os
from pathlib import Path
from typing import Dict, List, Tuple, Union

from .core import decode_text
from .core import tokenize as _tokenize


class TurkishTokenizer:
    """
    High-performance Turkish tokenizer with Rust backend.
    
    This tokenizer combines linguistic rules with BPE (Byte Pair Encoding)
    for optimal tokenization of Turkish text. It supports:
    
    - Root and suffix matching
    - BPE tokenization for unknown words
    - Special token handling (spaces, newlines, etc.)
    - Case-sensitive tokenization
    - Decoding back to text
    
    Example:
        >>> tokenizer = TurkishTokenizer()
        >>> tokens, ids = tokenizer.tokenize("Merhaba dünya!")
        >>> print(tokens)
        ['<uppercase>', 'merhaba', '<space>', 'dünya', '!']
        >>> text = tokenizer.decode(ids)
        >>> print(text)
        "Merhaba dünya!"
    """
    
    def __init__(self):
        """Initialize the Turkish tokenizer."""
        # The tokenizer is stateless, so no initialization needed
        pass
    
    def tokenize(self, text: str) -> Tuple[List[str], List[int]]:
        """
        Tokenize the input text.
        
        Args:
            text: The text to tokenize
            
        Returns:
            Tuple containing:
                - List of token strings
                - List of token IDs (integers)
                
        Example:
            >>> tokenizer = TurkishTokenizer()
            >>> tokens, ids = tokenizer.tokenize("Merhaba dünya!")
            >>> print(tokens)
            ['<uppercase>', 'merhaba', '<space>', 'dünya', '!']
        """
        return _tokenize(text)
    
    def decode(self, token_ids: List[int]) -> str:
        """
        Decode a list of token IDs back to text.
        
        Args:
            token_ids: List of token IDs to decode
            
        Returns:
            The decoded text string
            
        Example:
            >>> tokenizer = TurkishTokenizer()
            >>> tokens, ids = tokenizer.tokenize("Merhaba dünya!")
            >>> text = tokenizer.decode(ids)
            >>> print(text)
            "Merhaba dünya!"
        """
        return decode_text(token_ids)
    
    def tokenize_batch(self, texts: List[str]) -> List[Tuple[List[str], List[int]]]:
        """
        Tokenize a batch of texts.
        
        Args:
            texts: List of texts to tokenize
            
        Returns:
            List of tuples, each containing (tokens, token_ids)
            
        Example:
            >>> tokenizer = TurkishTokenizer()
            >>> results = tokenizer.tokenize_batch(["Merhaba", "Dünya"])
            >>> for tokens, ids in results:
            ...     print(tokens)
            ['<uppercase>', 'merhaba']
            ['<uppercase>', 'dünya']
        """
        return [_tokenize(text) for text in texts]
    
    def get_vocab_size(self) -> int:
        """
        Get the vocabulary size.
        
        Returns:
            The total number of tokens in the vocabulary
        """
        # This would need to be implemented based on the actual vocab size
        # For now, return an approximate value
        return 25000  # Approximate size based on the JSON files
    
    def get_special_tokens(self) -> Dict[str, int]:
        """
        Get the special tokens and their IDs.
        
        Returns:
            Dictionary mapping special token names to their IDs
        """
        return {
            "<space>": 1,
            "<newline>": 2,
            "<tab>": 3,
            "<unknown>": 4,
            "<uppercase>": 0
        }
    
    def __call__(self, text: str) -> Tuple[List[str], List[int]]:
        """
        Convenience method to call tokenize directly on the instance.
        
        Args:
            text: The text to tokenize
            
        Returns:
            Tuple of (tokens, token_ids)
        """
        return self.tokenize(text) 