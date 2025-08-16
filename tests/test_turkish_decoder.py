import pytest
from turkish_tokenizer import TurkishDecoder


class TestTurkishDecoder:
    """Test suite for TurkishDecoder class."""
    
    @pytest.fixture
    def reverse_dict(self):
        """Create a sample reverse dictionary for testing."""
        return {
            1: ["kitap"],
            2: ["masa"],
            3: [" "],
            4: ["<uppercase>"],
            5: ["<unknown>"],
            6: ["<pad>"],
            7: ["<eos>"],
            20000: ["a", "e"],  # Sample suffix
            20001: ["lar", "ler"],  # Plural suffix
            20002: ["da", "de", "ta", "te"],  # Locative suffix
        }
    
    @pytest.fixture
    def decoder(self, reverse_dict):
        """Create a decoder instance for testing."""
        return TurkishDecoder(reverse_dict)
    
    def test_decoder_initialization(self, decoder):
        """Test that decoder initializes correctly."""
        assert decoder is not None
        assert hasattr(decoder, 'reverse_dict')
        assert hasattr(decoder, 'ALL_VOWELS')
        assert hasattr(decoder, 'INCE_VOWELS')
        assert hasattr(decoder, 'AI_VOWELS')
        assert hasattr(decoder, 'EI_VOWELS')
        assert hasattr(decoder, 'OU_VOWELS')
        assert hasattr(decoder, 'HARD_CONSONANTS')
        assert hasattr(decoder, 'WHITESPACE')
    
    def test_starts_with_vowel(self, decoder):
        """Test vowel detection at word start."""
        assert decoder._starts_with_vowel("a")
        assert decoder._starts_with_vowel("e")
        assert decoder._starts_with_vowel("ı")
        assert decoder._starts_with_vowel("i")
        assert decoder._starts_with_vowel("o")
        assert decoder._starts_with_vowel("ö")
        assert decoder._starts_with_vowel("u")
        assert decoder._starts_with_vowel("ü")
        
        assert not decoder._starts_with_vowel("k")
        assert not decoder._starts_with_vowel("m")
        assert not decoder._starts_with_vowel("")
    
    def test_ends_with_vowel(self, decoder):
        """Test vowel detection at word end."""
        assert decoder._ends_with_vowel("a")
        assert decoder._ends_with_vowel("e")
        assert decoder._ends_with_vowel("ı")
        assert decoder._ends_with_vowel("i")
        assert decoder._ends_with_vowel("o")
        assert decoder._ends_with_vowel("ö")
        assert decoder._ends_with_vowel("u")
        assert decoder._ends_with_vowel("ü")
        
        assert not decoder._ends_with_vowel("k")
        assert not decoder._ends_with_vowel("m")
        assert not decoder._ends_with_vowel("")
    
    def test_ends_with_ince(self, decoder):
        """Test front vowel detection at word end."""
        assert decoder._ends_with_ince("e")
        assert decoder._ends_with_ince("i")
        assert decoder._ends_with_ince("ö")
        assert decoder._ends_with_ince("ü")
        assert decoder._ends_with_ince("saat")  # Special case
        assert decoder._ends_with_ince("kilovatsaat")  # Special case
        assert decoder._ends_with_ince("ziraat")  # Special case
        assert decoder._ends_with_ince("itaat")  # Special case
        
        assert not decoder._ends_with_ince("a")
        assert not decoder._ends_with_ince("ı")
        assert not decoder._ends_with_ince("o")
        assert not decoder._ends_with_ince("u")
    
    def test_ends_with_sert_unsuz(self, decoder):
        """Test hard consonant detection at word end."""
        assert decoder._ends_with_sert_unsuz("f")
        assert decoder._ends_with_sert_unsuz("s")
        assert decoder._ends_with_sert_unsuz("t")
        assert decoder._ends_with_sert_unsuz("k")
        assert decoder._ends_with_sert_unsuz("ç")
        assert decoder._ends_with_sert_unsuz("ş")
        assert decoder._ends_with_sert_unsuz("h")
        assert decoder._ends_with_sert_unsuz("p")
        
        assert not decoder._ends_with_sert_unsuz("a")
        assert not decoder._ends_with_sert_unsuz("e")
        assert not decoder._ends_with_sert_unsuz("m")
        assert not decoder._ends_with_sert_unsuz("")
    
    def test_get_vowel_suffix_index(self, decoder):
        """Test vowel harmony suffix index calculation."""
        # Back unrounded vowels
        assert decoder._get_vowel_suffix_index("a") == 0
        assert decoder._get_vowel_suffix_index("ı") == 0
        
        # Front unrounded vowels
        assert decoder._get_vowel_suffix_index("e") == 1
        assert decoder._get_vowel_suffix_index("i") == 1
        
        # Back rounded vowels
        assert decoder._get_vowel_suffix_index("o") == 2
        assert decoder._get_vowel_suffix_index("u") == 2
        
        # Front rounded vowels (should default to 3)
        assert decoder._get_vowel_suffix_index("ö") == 3
        assert decoder._get_vowel_suffix_index("ü") == 3
    
    def test_decode_simple_tokens(self, decoder):
        """Test decoding of simple tokens."""
        ids = [1, 3, 2]  # kitap, space, masa
        result = decoder.decode(ids)
        
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_decode_with_special_tokens(self, decoder):
        """Test decoding with special tokens."""
        ids = [4, 1, 3, 2]  # uppercase, kitap, space, masa
        result = decoder.decode(ids)
        
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_decode_empty_list(self, decoder):
        """Test decoding empty token list."""
        ids = []
        result = decoder.decode(ids)
        
        assert isinstance(result, str)
        # Should return empty string or handle gracefully
    
    def test_decode_unknown_tokens(self, decoder):
        """Test decoding with unknown token IDs."""
        ids = [999, 888]  # Unknown IDs
        result = decoder.decode(ids)
        
        assert isinstance(result, str)
        # Should handle gracefully without crashing
    
    def test_decode_with_suffixes(self, decoder):
        """Test decoding with suffix tokens."""
        ids = [1, 20001]  # kitap + plural suffix
        result = decoder.decode(ids)
        
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_decode_complex_sequence(self, decoder):
        """Test decoding complex token sequences."""
        ids = [4, 1, 20001, 3, 2, 20002]  # uppercase + kitap + plural + space + masa + locative
        result = decoder.decode(ids)
        
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_ends_with_any(self, decoder):
        """Test the _ends_with_any method."""
        # Test with vowels
        assert decoder._ends_with_any("kitap", "aeıioöuü")
        assert decoder._ends_with_any("masa", "aeıioöuü")
        
        # Test with consonants
        assert decoder._ends_with_any("kitap", "fstkçşhp")
        assert not decoder._ends_with_any("masa", "fstkçşhp")
        
        # Test with mixed characters
        assert decoder._ends_with_any("kitap", "ap")
        # "masa" ends with "a" which is in "ap", so this should be True
        assert decoder._ends_with_any("masa", "ap")


class TestTurkishDecoderEdgeCases:
    """Test edge cases for TurkishDecoder."""
    
    @pytest.fixture
    def reverse_dict(self):
        return {
            1: ["test"],
            2: [" "],
            3: ["<unknown>"],
        }
    
    @pytest.fixture
    def decoder(self, reverse_dict):
        return TurkishDecoder(reverse_dict)
    
    def test_decode_single_token(self, decoder):
        """Test decoding single token."""
        ids = [1]
        result = decoder.decode(ids)
        
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_decode_repeated_tokens(self, decoder):
        """Test decoding repeated tokens."""
        ids = [1, 1, 1]  # Same token repeated
        result = decoder.decode(ids)
        
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_decode_with_whitespace(self, decoder):
        """Test decoding with whitespace tokens."""
        ids = [1, 2, 1]  # test, space, test
        result = decoder.decode(ids)
        
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_decode_very_long_sequence(self, decoder):
        """Test decoding very long token sequences."""
        ids = [1] * 1000  # 1000 repeated tokens
        result = decoder.decode(ids)
        
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_decode_with_numbers(self, decoder):
        """Test decoding with numeric token IDs."""
        ids = [1, 2, 3, 4, 5]
        result = decoder.decode(ids)
        
        assert isinstance(result, str)
        # Should handle gracefully even if some IDs don't exist
    
    def test_vowel_harmony_edge_cases(self, decoder):
        """Test vowel harmony with edge cases."""
        # Test with empty strings
        assert not decoder._starts_with_vowel("")
        assert not decoder._ends_with_vowel("")
        assert not decoder._ends_with_ince("")
        assert not decoder._ends_with_sert_unsuz("")
        
        # Test with single characters
        assert decoder._starts_with_vowel("a")
        assert decoder._ends_with_vowel("a")
        assert not decoder._ends_with_ince("a")
        assert not decoder._ends_with_sert_unsuz("a")
        
        # Test with special characters
        assert not decoder._starts_with_vowel("!")
        assert not decoder._ends_with_vowel("!")
        assert not decoder._ends_with_ince("!")
        assert not decoder._ends_with_sert_unsuz("!")


class TestTurkishDecoderPerformance:
    """Test performance characteristics of TurkishDecoder."""
    
    @pytest.fixture
    def reverse_dict(self):
        # Create a larger reverse dictionary for performance testing
        large_dict = {}
        for i in range(1000):
            large_dict[i] = [f"token_{i}"]
        return large_dict
    
    @pytest.fixture
    def decoder(self, reverse_dict):
        return TurkishDecoder(reverse_dict)
    
    def test_decode_speed(self, decoder):
        """Test that decoding is reasonably fast."""
        import time
        
        # Create a long sequence of tokens
        ids = list(range(100))  # 100 tokens
        
        start_time = time.time()
        result = decoder.decode(ids)
        end_time = time.time()
        
        # Should complete in reasonable time
        assert end_time - start_time < 1.0  # 1 second
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_vowel_detection_speed(self, decoder):
        """Test that vowel detection methods are fast."""
        import time
        
        test_words = ["kitap", "masa", "üzerinde", "çanta", "şemsiye"] * 100
        
        # Test _starts_with_vowel
        start_time = time.time()
        for word in test_words:
            decoder._starts_with_vowel(word)
        end_time = time.time()
        assert end_time - start_time < 1.0
        
        # Test _ends_with_vowel
        start_time = time.time()
        for word in test_words:
            decoder._ends_with_vowel(word)
        end_time = time.time()
        assert end_time - start_time < 1.0
        
        # Test _ends_with_ince
        start_time = time.time()
        for word in test_words:
            decoder._ends_with_ince(word)
        end_time = time.time()
        assert end_time - start_time < 1.0


if __name__ == "__main__":
    pytest.main([__file__])
