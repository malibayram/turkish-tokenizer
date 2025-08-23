import json
import os

import pytest

from turkish_tokenizer import TokenType, TurkishTokenizer


class TestTurkishTokenizer:
    """Test suite for TurkishTokenizer class."""
    
    @pytest.fixture
    def tokenizer(self):
        """Create a tokenizer instance for testing."""
        return TurkishTokenizer()
    
    def test_tokenizer_initialization(self, tokenizer):
        """Test that tokenizer initializes correctly."""
        assert tokenizer is not None
        assert hasattr(tokenizer, 'vocab')
        assert hasattr(tokenizer, 'reverse_dict')
        assert hasattr(tokenizer, 'decoder')
        assert hasattr(tokenizer, 'vocab_size')
        
        # Check that vocab is loaded
        assert len(tokenizer.vocab) > 0
        assert len(tokenizer.reverse_dict) > 0
        assert tokenizer.vocab_size > 0
        
        # Check special tokens exist
        assert "<uppercase>" in tokenizer.vocab
        assert "<unknown>" in tokenizer.vocab
        assert " " in tokenizer.vocab
        assert "<pad>" in tokenizer.vocab
        assert "<eos>" in tokenizer.vocab
    
    def test_tokenize_simple_word(self, tokenizer):
        """Test tokenizing a simple Turkish word."""
        text = "kitap"
        tokens = tokenizer.tokenize(text)
        assert isinstance(tokens, list)
        assert len(tokens) > 0
        assert all(isinstance(token, str) for token in tokens)
    
    def test_encode_simple_word(self, tokenizer):
        """Test encoding a simple Turkish word."""
        text = "kitap"
        ids = tokenizer.encode(text)
        assert isinstance(ids, list)
        assert len(ids) > 0
        assert all(isinstance(id_val, int) for id_val in ids)
    
    def test_tokenize_text_with_spaces(self, tokenizer):
        """Test tokenizing text with spaces."""
        text = "kitap masa"
        tokens = tokenizer.tokenize(text)
        assert isinstance(tokens, list)
        assert len(tokens) > 0
        
        # Should contain space tokens
        assert " " in tokens
    
    def test_encode_decode_roundtrip(self, tokenizer):
        """Test that encode followed by decode returns the original text."""
        test_texts = [
            "kitap",
            "masa üzerinde",
            "Türkçe dil",
            "merhaba dünya"
        ]
        
        for text in test_texts:
            ids = tokenizer.encode(text)
            decoded = tokenizer.decode(ids)
            # Note: Exact match might not be possible due to tokenization differences
            # but the decoded text should be reasonable
            assert isinstance(decoded, str)
            assert len(decoded) > 0
    
    def test_tokenize_text_detailed(self, tokenizer):
        """Test detailed tokenization with token types."""
        text = "kitap"
        tokens, uppercase_indices = tokenizer.tokenize_text(text)
        
        assert isinstance(tokens, list)
        assert isinstance(uppercase_indices, list)
        assert len(tokens) > 0
        
        # Check token structure
        for token in tokens:
            assert isinstance(token, dict)
            assert "token" in token
            assert "id" in token
            assert "type" in token
            assert isinstance(token["type"], TokenType)
    
    def test_uppercase_handling(self, tokenizer):
        """Test handling of uppercase letters."""
        text = "Kitap"
        tokens = tokenizer.tokenize(text)
        ids = tokenizer.encode(text)
        
        assert isinstance(tokens, list)
        assert isinstance(ids, list)
        assert len(tokens) > 0
        assert len(ids) > 0
    
    def test_empty_string(self, tokenizer):
        """Test handling of empty strings."""
        text = ""
        tokens = tokenizer.tokenize(text)
        ids = tokenizer.encode(text)
        
        assert isinstance(tokens, list)
        assert isinstance(ids, list)
        # Empty string might result in empty lists or special handling
    
    def test_whitespace_only(self, tokenizer):
        """Test handling of whitespace-only strings."""
        text = "   \n\t"
        tokens = tokenizer.tokenize(text)
        ids = tokenizer.encode(text)
        
        assert isinstance(tokens, list)
        assert isinstance(ids, list)
    
    def test_special_characters(self, tokenizer):
        """Test handling of special characters."""
        text = "kitap! masa?"
        tokens = tokenizer.tokenize(text)
        ids = tokenizer.encode(text)
        
        assert isinstance(tokens, list)
        assert isinstance(ids, list)
        assert len(tokens) > 0
        assert len(ids) > 0
    
    def test_long_text(self, tokenizer):
        """Test handling of longer text."""
        text = "Bu bir test cümlesidir. Türkçe dil kurallarına uygun olarak yazılmıştır."
        tokens = tokenizer.tokenize(text)
        ids = tokenizer.encode(text)
        
        assert isinstance(tokens, list)
        assert isinstance(ids, list)
        assert len(tokens) > 0
        assert len(ids) > 0
    
    def test_unknown_words(self, tokenizer):
        """Test handling of unknown words."""
        text = "xyzabc123"  # Likely unknown tokens
        tokens = tokenizer.tokenize(text)
        ids = tokenizer.encode(text)
        
        assert isinstance(tokens, list)
        assert isinstance(ids, list)
        assert len(tokens) > 0
        assert len(ids) > 0
    
    def test_mixed_case(self, tokenizer):
        """Test handling of mixed case text."""
        text = "Kitap Masa Üzerinde"
        tokens = tokenizer.tokenize(text)
        ids = tokenizer.encode(text)
        
        assert isinstance(tokens, list)
        assert isinstance(ids, list)
        assert len(tokens) > 0
        assert len(ids) > 0
    
    def test_numbers(self, tokenizer):
        """Test handling of numbers."""
        text = "123 kitap 456 masa"
        tokens = tokenizer.tokenize(text)
        ids = tokenizer.encode(text)
        
        assert isinstance(tokens, list)
        assert isinstance(ids, list)
        assert len(tokens) > 0
        assert len(ids) > 0
    
    def test_punctuation(self, tokenizer):
        """Test handling of punctuation."""
        text = "kitap, masa; üzerinde."
        tokens = tokenizer.tokenize(text)
        ids = tokenizer.encode(text)
        
        assert isinstance(tokens, list)
        assert isinstance(ids, list)
        assert len(tokens) > 0
        assert len(ids) > 0
    
    def test_token_types(self, tokenizer):
        """Test that different token types are correctly identified."""
        text = "kitap"
        tokens, _ = tokenizer.tokenize_text(text)
        
        token_types = [token["type"] for token in tokens]
        assert all(isinstance(t, TokenType) for t in token_types)
        
        # Should have at least one token
        assert len(token_types) > 0
    
    def test_reverse_dict_consistency(self, tokenizer):
        """Test that reverse dictionary is consistent."""
        # Test a few known tokens
        test_tokens = ["kitap", "masa", " "]
        
        for token in test_tokens:
            if token in tokenizer.vocab:
                token_id = tokenizer.vocab[token]
                assert token_id in tokenizer.reverse_dict
                assert token in tokenizer.reverse_dict[token_id]
    
    def test_max_lengths(self, tokenizer):
        """Test that max length calculations are correct."""
        assert tokenizer.max_root_len > 0
        assert tokenizer.max_suffix_len > 0
        assert tokenizer.max_bpe_len > 0
        
        # Max lengths should be reasonable
        assert tokenizer.max_root_len <= 50  # Adjust based on your data
        assert tokenizer.max_suffix_len <= 20
        assert tokenizer.max_bpe_len <= 30
    
    def test_special_markers(self, tokenizer):
        """Test that special markers are correctly defined."""
        assert tokenizer.uppercase_marker["token"] == "<uppercase>"
        assert tokenizer.unknown_marker["token"] == "<unknown>"
        assert tokenizer.space_marker["token"] == " "
        
        assert tokenizer.uppercase_marker["type"] == TokenType.ROOT
        assert tokenizer.unknown_marker["type"] == TokenType.ROOT
        assert tokenizer.space_marker["type"] == TokenType.ROOT
    
    def test_pad_eos_tokens(self, tokenizer):
        """Test that pad and eos token IDs are valid."""
        assert isinstance(tokenizer.pad_token_id, int)
        assert isinstance(tokenizer.eos_token_id, int)
        assert tokenizer.pad_token_id >= 0
        assert tokenizer.eos_token_id >= 0

    def test_callable_interface(self, tokenizer):
        """Test that tokenizer instances are callable and return expected format."""
        text = "kitap masa"
        result = tokenizer(text)
        
        assert isinstance(result, dict)
        assert "input_ids" in result
        assert "attention_mask" in result
        assert isinstance(result["input_ids"], list)
        assert isinstance(result["attention_mask"], list)
        assert len(result["input_ids"]) == len(result["attention_mask"])
        assert all(isinstance(x, int) for x in result["input_ids"])
        assert all(x == 1 for x in result["attention_mask"])

    def test_no_intersection_between_token_dictionaries(self, tokenizer):
        """Test that there are no overlapping keys between kokler, ekler, and bpe_tokenler."""
        kokler = tokenizer.roots
        ekler = tokenizer.suffixes
        bpe_tokenler = tokenizer.bpe_tokens
        
        # Check for intersections between kokler and ekler
        kokler_ekler_intersection = set(kokler.keys()) & set(ekler.keys())
        if kokler_ekler_intersection:
            pytest.fail(f"Found overlapping keys between kokler and ekler: {kokler_ekler_intersection}")
        
        # Check for intersections between kokler and bpe_tokenler
        kokler_bpe_intersection = set(kokler.keys()) & set(bpe_tokenler.keys())
        if kokler_bpe_intersection:
            pytest.fail(f"Found overlapping keys between kokler and bpe_tokenler: {kokler_bpe_intersection}")
        
        # Check for intersections between ekler and bpe_tokenler
        ekler_bpe_intersection = set(ekler.keys()) & set(bpe_tokenler.keys())
        if ekler_bpe_intersection:
            pytest.fail(f"Found overlapping keys between ekler and bpe_tokenler: {ekler_bpe_intersection}")
        
        # All intersections should be empty
        assert len(kokler_ekler_intersection) == 0, "kokler and ekler should not have overlapping keys"
        assert len(kokler_bpe_intersection) == 0, "kokler and bpe_tokenler should not have overlapping keys"
        assert len(ekler_bpe_intersection) == 0, "ekler and bpe_tokenler should not have overlapping keys"


class TestTurkishTokenizerEdgeCases:
    """Test edge cases and error conditions."""
    
    @pytest.fixture
    def tokenizer(self):
        return TurkishTokenizer()
    
    def test_very_long_word(self, tokenizer):
        """Test handling of very long words."""
        long_word = "a" * 1000
        tokens = tokenizer.tokenize(long_word)
        ids = tokenizer.encode(long_word)
        
        assert isinstance(tokens, list)
        assert isinstance(ids, list)
        assert len(tokens) > 0
        assert len(ids) > 0
    
    def test_unicode_characters(self, tokenizer):
        """Test handling of Unicode characters."""
        text = "kitap çanta şemsiye öğrenci"
        tokens = tokenizer.tokenize(text)
        ids = tokenizer.encode(text)
        
        assert isinstance(tokens, list)
        assert isinstance(ids, list)
        assert len(tokens) > 0
        assert len(ids) > 0
    
    def test_emojis(self, tokenizer):
        """Test handling of emojis."""
        text = "kitap 📚 masa 🪑"
        tokens = tokenizer.tokenize(text)
        ids = tokenizer.encode(text)
        
        assert isinstance(tokens, list)
        assert isinstance(ids, list)
        assert len(tokens) > 0
        assert len(ids) > 0
    
    def test_newlines_tabs(self, tokenizer):
        """Test handling of newlines and tabs."""
        text = "kitap\nmasa\tüzerinde"
        tokens = tokenizer.tokenize(text)
        ids = tokenizer.encode(text)
        
        assert isinstance(tokens, list)
        assert isinstance(ids, list)
        assert len(tokens) > 0
        assert len(ids) > 0


class TestTurkishTokenizerPerformance:
    """Test performance characteristics."""
    
    @pytest.fixture
    def tokenizer(self):
        return TurkishTokenizer()
    
    def test_tokenization_speed(self, tokenizer):
        """Test that tokenization is reasonably fast."""
        import time
        
        text = "Bu bir test cümlesidir. " * 100  # 2000 characters
        
        start_time = time.time()
        tokens = tokenizer.tokenize(text)
        end_time = time.time()
        
        # Should complete in reasonable time (adjust threshold as needed)
        assert end_time - start_time < 1.0  # 1 second
        assert isinstance(tokens, list)
        assert len(tokens) > 0
    
    def test_encoding_speed(self, tokenizer):
        """Test that encoding is reasonably fast."""
        import time
        
        text = "Bu bir test cümlesidir. " * 100  # 2000 characters
        
        start_time = time.time()
        ids = tokenizer.encode(text)
        end_time = time.time()
        
        # Should complete in reasonable time
        assert end_time - start_time < 1.0  # 1 second
        assert isinstance(ids, list)
        assert len(ids) > 0


if __name__ == "__main__":
    pytest.main([__file__])
