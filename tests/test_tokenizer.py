"""
Tests for the Turkish tokenizer package.
"""

import pytest

from turkish_tokenizer import TurkishTokenizer, tokenize


class TestTurkishTokenizer:
    """Test cases for the TurkishTokenizer class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.tokenizer = TurkishTokenizer()
    
    def test_tokenizer_initialization(self):
        """Test that the tokenizer initializes correctly."""
        assert self.tokenizer is not None
        assert isinstance(self.tokenizer, TurkishTokenizer)
    
    def test_basic_tokenization(self):
        """Test basic tokenization functionality."""
        text = "Merhaba dünya"
        tokens, ids = self.tokenizer.tokenize(text)
        
        assert isinstance(tokens, list)
        assert isinstance(ids, list)
        assert len(tokens) == len(ids)
        assert len(tokens) > 0
    
    def test_special_tokens(self):
        """Test that special tokens are handled correctly."""
        text = "Merhaba\ndünya\t!"
        tokens, ids = self.tokenizer.tokenize(text)
        
        # Should contain special tokens
        assert "<space>" in tokens or "<newline>" in tokens or "<tab>" in tokens
    
    def test_uppercase_handling(self):
        """Test that uppercase letters are handled correctly."""
        text = "Merhaba Dünya"
        tokens, ids = self.tokenizer.tokenize(text)
        
        # Should contain uppercase token
        assert "<uppercase>" in tokens
    
    def test_decode_functionality(self):
        """Test that decoding works correctly."""
        text = "Merhaba dünya"
        tokens, ids = self.tokenizer.tokenize(text)
        decoded = self.tokenizer.decode(ids)
        
        # Decoded text should be similar to original (allowing for case differences)
        assert len(decoded) > 0
        assert isinstance(decoded, str)
    
    def test_batch_tokenization(self):
        """Test batch tokenization functionality."""
        texts = ["Merhaba", "dünya", "test"]
        results = self.tokenizer.tokenize_batch(texts)
        
        assert len(results) == len(texts)
        for tokens, ids in results:
            assert isinstance(tokens, list)
            assert isinstance(ids, list)
            assert len(tokens) == len(ids)
    
    def test_vocab_size(self):
        """Test that vocab size is returned correctly."""
        vocab_size = self.tokenizer.get_vocab_size()
        assert isinstance(vocab_size, int)
        assert vocab_size > 0
    
    def test_special_tokens_dict(self):
        """Test that special tokens dictionary is returned correctly."""
        special_tokens = self.tokenizer.get_special_tokens()
        assert isinstance(special_tokens, dict)
        assert len(special_tokens) > 0
        
        # Check for expected special tokens
        expected_tokens = ["<space>", "<newline>", "<tab>", "<unknown>", "<uppercase>"]
        for token in expected_tokens:
            assert token in special_tokens
    
    def test_call_method(self):
        """Test that the tokenizer can be called directly."""
        text = "Merhaba dünya"
        tokens, ids = self.tokenizer(text)
        
        assert isinstance(tokens, list)
        assert isinstance(ids, list)
        assert len(tokens) == len(ids)
    
    def test_empty_text(self):
        """Test tokenization of empty text."""
        tokens, ids = self.tokenizer.tokenize("")
        assert tokens == []
        assert ids == []
    
    def test_whitespace_only(self):
        """Test tokenization of whitespace-only text."""
        text = "   \n\t  "
        tokens, ids = self.tokenizer.tokenize(text)
        
        # Should contain only special tokens
        for token in tokens:
            assert token in ["<space>", "<newline>", "<tab>"]
    
    def test_punctuation(self):
        """Test tokenization of text with punctuation."""
        text = "Merhaba, dünya! Nasılsın?"
        tokens, ids = self.tokenizer.tokenize(text)
        
        assert len(tokens) > 0
        # Should contain punctuation tokens
        assert any(token in ",!?" for token in tokens)


class TestConvenienceFunction:
    """Test cases for the convenience tokenize function."""
    
    def test_convenience_tokenize(self):
        """Test the convenience tokenize function."""
        text = "Merhaba dünya"
        tokens, ids = tokenize(text)
        
        assert isinstance(tokens, list)
        assert isinstance(ids, list)
        assert len(tokens) == len(ids)
        assert len(tokens) > 0
    
    def test_convenience_vs_class(self):
        """Test that convenience function matches class method."""
        text = "Merhaba dünya"
        tokens1, ids1 = tokenize(text)
        
        tokenizer = TurkishTokenizer()
        tokens2, ids2 = tokenizer.tokenize(text)
        
        assert tokens1 == tokens2
        assert ids1 == ids2


class TestEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_very_long_text(self):
        """Test tokenization of very long text."""
        text = "Merhaba dünya! " * 1000
        tokenizer = TurkishTokenizer()
        tokens, ids = tokenizer.tokenize(text)
        
        assert len(tokens) > 0
        assert len(ids) > 0
    
    def test_turkish_characters(self):
        """Test tokenization with Turkish characters."""
        text = "çğışöü ÇĞIŞÖÜ"
        tokenizer = TurkishTokenizer()
        tokens, ids = tokenizer.tokenize(text)
        
        assert len(tokens) > 0
        assert len(ids) > 0
    
    def test_numbers(self):
        """Test tokenization with numbers."""
        text = "Merhaba 123 dünya 456"
        tokenizer = TurkishTokenizer()
        tokens, ids = tokenizer.tokenize(text)
        
        assert len(tokens) > 0
        assert len(ids) > 0
    
    def test_mixed_content(self):
        """Test tokenization with mixed content."""
        text = "Merhaba123 dünya!@# $%^&*()"
        tokenizer = TurkishTokenizer()
        tokens, ids = tokenizer.tokenize(text)
        
        assert len(tokens) > 0
        assert len(ids) > 0


@pytest.mark.integration
class TestIntegration:
    """Integration tests for the tokenizer."""
    
    def test_full_pipeline(self):
        """Test the full tokenization and decoding pipeline."""
        original_text = "Merhaba dünya! Bu bir test cümlesidir."
        tokenizer = TurkishTokenizer()
        
        # Tokenize
        tokens, ids = tokenizer.tokenize(original_text)
        
        # Decode
        decoded_text = tokenizer.decode(ids)
        
        # Basic validation
        assert len(tokens) > 0
        assert len(ids) > 0
        assert len(decoded_text) > 0
        
        # The decoded text should be similar to original
        # (allowing for case differences and spacing)
        assert "merhaba" in decoded_text.lower() or "dünya" in decoded_text.lower()
    
    def test_multiple_languages(self):
        """Test tokenization with mixed Turkish and English text."""
        text = "Merhaba world! Bu bir test testidir."
        tokenizer = TurkishTokenizer()
        tokens, ids = tokenizer.tokenize(text)
        
        assert len(tokens) > 0
        assert len(ids) > 0 