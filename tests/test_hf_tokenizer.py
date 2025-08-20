#!/usr/bin/env python3
"""
Tests for the Hugging Face compatible Turkish tokenizer.
"""

import os
import shutil
import tempfile
import unittest

from turkish_tokenizer import HFTurkishTokenizer, TurkishTokenizer


class TestHFTurkishTokenizer(unittest.TestCase):
    """Test cases for HFTurkishTokenizer."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.tokenizer = HFTurkishTokenizer()
        self.original_tokenizer = TurkishTokenizer()
        
    def test_basic_tokenization(self):
        """Test basic tokenization functionality."""
        text = "Merhaba dünya!"
        
        # Test tokenize method
        tokens = self.tokenizer.tokenize(text)
        self.assertIsInstance(tokens, list)
        self.assertTrue(len(tokens) > 0)
        
        # Test that it matches the original tokenizer
        original_tokens = self.original_tokenizer.tokenize(text)
        self.assertEqual(tokens, original_tokens)
    
    def test_encoding_decoding(self):
        """Test encoding and decoding functionality."""
        text = "Bu bir test cümlesidir."
        
        # Test encoding
        encoded = self.tokenizer.encode(text)
        self.assertIsInstance(encoded, list)
        self.assertTrue(len(encoded) > 0)
        
        # Test decoding
        decoded = self.tokenizer.decode(encoded)
        self.assertIsInstance(decoded, str)
        self.assertTrue(len(decoded) > 0)
        
        # Test that it matches the original tokenizer (without special tokens)
        encoded_no_special = self.tokenizer.encode(text, add_special_tokens=False)
        original_encoded = self.original_tokenizer.encode(text)
        self.assertEqual(encoded_no_special, original_encoded)
        
        # Test that decoded text matches original (with special tokens removed)
        decoded_no_special = self.tokenizer.decode(encoded, skip_special_tokens=True)
        original_decoded = self.original_tokenizer.decode(original_encoded)
        self.assertEqual(decoded_no_special, original_decoded)
    
    def test_convert_tokens_to_ids(self):
        """Test token to ID conversion."""
        tokens = ["merhaba", "dünya"]
        
        # Test conversion
        ids = self.tokenizer.convert_tokens_to_ids(tokens)
        self.assertIsInstance(ids, list)
        self.assertEqual(len(ids), len(tokens))
        
        # Test single token
        single_id = self.tokenizer.convert_tokens_to_ids("merhaba")
        self.assertIsInstance(single_id, int)
    
    def test_convert_ids_to_tokens(self):
        """Test ID to token conversion."""
        # Get some valid IDs from the vocabulary
        vocab = self.tokenizer.get_vocab()
        test_tokens = ["merhaba", "dünya"]
        test_ids = [vocab[token] for token in test_tokens if token in vocab]
        
        if test_ids:
            # Test conversion
            tokens = self.tokenizer.convert_ids_to_tokens(test_ids)
            self.assertIsInstance(tokens, list)
            self.assertEqual(len(tokens), len(test_ids))
            
            # Test single ID
            single_token = self.tokenizer.convert_ids_to_tokens(test_ids[0])
            self.assertIsInstance(single_token, str)
    
    def test_special_tokens(self):
        """Test special tokens handling."""
        # Test that special tokens are properly set
        self.assertIsNotNone(self.tokenizer.pad_token)
        self.assertIsNotNone(self.tokenizer.eos_token)
        self.assertIsNotNone(self.tokenizer.unk_token)
        
        # Test special token IDs
        self.assertIsNotNone(self.tokenizer.pad_token_id)
        self.assertIsNotNone(self.tokenizer.eos_token_id)
        self.assertIsNotNone(self.tokenizer.unk_token_id)
    
    def test_custom_special_tokens(self):
        """Test custom special tokens."""
        custom_tokenizer = HFTurkishTokenizer(
            bos_token="<s>",
            eos_token="</s>",
            sep_token="<sep>",
            cls_token="<cls>",
            mask_token="<mask>",
            pad_token="<pad>",
            unk_token="<unk>"
        )
        
        # Test that custom tokens are set
        self.assertEqual(custom_tokenizer.bos_token, "<s>")
        self.assertEqual(custom_tokenizer.eos_token, "</s>")
        self.assertEqual(custom_tokenizer.sep_token, "<sep>")
        self.assertEqual(custom_tokenizer.cls_token, "<cls>")
        self.assertEqual(custom_tokenizer.mask_token, "<mask>")
        self.assertEqual(custom_tokenizer.pad_token, "<pad>")
        self.assertEqual(custom_tokenizer.unk_token, "<unk>")
    
    def test_encode_with_special_tokens(self):
        """Test encoding with special tokens."""
        text = "Test cümlesi"
        
        # Encode without special tokens
        encoded_no_special = self.tokenizer.encode(text, add_special_tokens=False)
        
        # Encode with special tokens
        encoded_with_special = self.tokenizer.encode(text, add_special_tokens=True)
        
        # Should be longer with special tokens
        self.assertGreaterEqual(len(encoded_with_special), len(encoded_no_special))
    
    def test_decode_with_special_tokens(self):
        """Test decoding with special tokens."""
        text = "Test cümlesi"
        encoded = self.tokenizer.encode(text, add_special_tokens=True)
        
        # Decode with special tokens
        decoded_with_special = self.tokenizer.decode(encoded, skip_special_tokens=False)
        
        # Decode without special tokens
        decoded_without_special = self.tokenizer.decode(encoded, skip_special_tokens=True)
        
        # Should be different
        self.assertNotEqual(decoded_with_special, decoded_without_special)
    
    def test_batch_processing(self):
        """Test batch processing capabilities."""
        texts = [
            "Merhaba dünya!",
            "Bu bir test cümlesidir.",
            "Türkçe dil işleme örneği."
        ]
        
        # Batch encode
        encoded_batch = self.tokenizer.encode(texts)
        self.assertIsInstance(encoded_batch, list)
        self.assertEqual(len(encoded_batch), len(texts))
        
        # Batch decode
        decoded_batch = self.tokenizer.decode(encoded_batch, skip_special_tokens=True)
        self.assertIsInstance(decoded_batch, list)
        self.assertEqual(len(decoded_batch), len(texts))
    
    def test_call_method(self):
        """Test the __call__ method for model input preparation."""
        text = "Bu cümle model girişi için hazırlanacak."
        
        # Test basic call
        result = self.tokenizer(text)
        self.assertIn('input_ids', result)
        self.assertIn('attention_mask', result)
        
        # Test with padding and truncation
        result = self.tokenizer(
            text,
            padding=True,
            truncation=True,
            max_length=50
        )
        self.assertIn('input_ids', result)
        self.assertIn('attention_mask', result)
    
    def test_vocabulary_access(self):
        """Test vocabulary access methods."""
        # Test vocab_size property
        vocab_size = self.tokenizer.vocab_size
        self.assertIsInstance(vocab_size, int)
        self.assertGreater(vocab_size, 0)
        
        # Test get_vocab method
        vocab = self.tokenizer.get_vocab()
        self.assertIsInstance(vocab, dict)
        self.assertEqual(len(vocab), vocab_size)
    
    def test_save_load(self):
        """Test save and load functionality."""
        # Create a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save the tokenizer
            self.tokenizer.save_pretrained(temp_dir)
            
            # Check that files were created
            self.assertTrue(os.path.exists(os.path.join(temp_dir, "tokenizer_config.json")))
            self.assertTrue(os.path.exists(os.path.join(temp_dir, "kokler.json")))
            self.assertTrue(os.path.exists(os.path.join(temp_dir, "ekler.json")))
            self.assertTrue(os.path.exists(os.path.join(temp_dir, "bpe_tokenler.json")))
            
            # Load the tokenizer
            loaded_tokenizer = HFTurkishTokenizer.from_pretrained(temp_dir)
            
            # Test that they work the same
            text = "Test cümlesi"
            original_encoded = self.tokenizer.encode(text)
            loaded_encoded = loaded_tokenizer.encode(text)
            self.assertEqual(original_encoded, loaded_encoded)
    
    def test_model_max_length(self):
        """Test model_max_length parameter."""
        custom_tokenizer = HFTurkishTokenizer(model_max_length=256)
        self.assertEqual(custom_tokenizer.model_max_length, 256)
    
    def test_padding_side(self):
        """Test padding_side parameter."""
        custom_tokenizer = HFTurkishTokenizer(padding_side="left")
        self.assertEqual(custom_tokenizer.padding_side, "left")
    
    def test_truncation_side(self):
        """Test truncation_side parameter."""
        custom_tokenizer = HFTurkishTokenizer(truncation_side="left")
        self.assertEqual(custom_tokenizer.truncation_side, "left")
    
    def test_unknown_token_handling(self):
        """Test handling of unknown tokens."""
        # Test with a token that should not be in vocabulary
        unknown_token = "xyz123unknown"
        token_id = self.tokenizer._convert_token_to_id(unknown_token)
        
        # Should return unknown token ID
        self.assertEqual(token_id, self.tokenizer.unk_token_id)
    
    def test_empty_text_handling(self):
        """Test handling of empty text."""
        # Test empty string
        tokens = self.tokenizer.tokenize("")
        self.assertEqual(tokens, [])
        
        # Test encoding without special tokens
        encoded = self.tokenizer.encode("", add_special_tokens=False)
        self.assertEqual(encoded, [])
        
        # Test encoding with special tokens (should add EOS token)
        encoded_with_special = self.tokenizer.encode("", add_special_tokens=True)
        self.assertEqual(encoded_with_special, [self.tokenizer.eos_token_id])
        
        decoded = self.tokenizer.decode([])
        self.assertEqual(decoded, "")
    
    def test_whitespace_handling(self):
        """Test handling of whitespace."""
        text = "  merhaba   dünya  "
        
        # Should handle whitespace properly
        tokens = self.tokenizer.tokenize(text)
        self.assertIsInstance(tokens, list)
        self.assertTrue(len(tokens) > 0)
    
    def test_turkish_specific_features(self):
        """Test Turkish-specific morphological features."""
        # Test with Turkish words that have morphological variations
        text = "evdeki kitabı okuyorum"
        
        tokens = self.tokenizer.tokenize(text)
        self.assertIsInstance(tokens, list)
        self.assertTrue(len(tokens) > 0)
        
        # Test encoding and decoding
        encoded = self.tokenizer.encode(text)
        decoded = self.tokenizer.decode(encoded)
        
        # Should be able to reconstruct the text
        self.assertIsInstance(decoded, str)
        self.assertTrue(len(decoded) > 0)


if __name__ == "__main__":
    unittest.main()
