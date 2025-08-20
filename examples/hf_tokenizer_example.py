#!/usr/bin/env python3
"""
Example script demonstrating the Hugging Face compatible Turkish tokenizer.

This script shows how to use the HFTurkishTokenizer with various features
including tokenization, encoding, decoding, and integration with Hugging Face
transformers library.
"""

import os
import sys

# Add the parent directory to the path to import the tokenizer
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from turkish_tokenizer import HFTurkishTokenizer


def basic_tokenization_example():
    """Demonstrate basic tokenization functionality."""
    print("=== Basic Tokenization Example ===")
    
    # Initialize the tokenizer
    tokenizer = HFTurkishTokenizer()
    
    # Sample Turkish text
    text = "Merhaba dünya! Bu bir test cümlesidir."
    
    print(f"Original text: {text}")
    
    # Tokenize the text
    tokens = tokenizer.tokenize(text)
    print(f"Tokens: {tokens}")
    
    # Convert tokens to IDs
    token_ids = tokenizer.convert_tokens_to_ids(tokens)
    print(f"Token IDs: {token_ids}")
    
    # Convert back to tokens
    tokens_back = tokenizer.convert_ids_to_tokens(token_ids)
    print(f"Tokens back: {tokens_back}")
    
    # Decode the IDs back to text
    decoded_text = tokenizer.decode(token_ids)
    print(f"Decoded text: {decoded_text}")
    
    print()


def encoding_decoding_example():
    """Demonstrate encoding and decoding with special tokens."""
    print("=== Encoding and Decoding Example ===")
    
    tokenizer = HFTurkishTokenizer()
    
    text = "Türkiye Cumhuriyeti'nin başkenti Ankara'dır."
    
    print(f"Original text: {text}")
    
    # Encode with special tokens
    encoded = tokenizer.encode(text, add_special_tokens=True)
    print(f"Encoded with special tokens: {encoded}")
    
    # Decode with special tokens
    decoded_with_special = tokenizer.decode(encoded)
    print(f"Decoded with special tokens: {decoded_with_special}")
    
    # Decode without special tokens
    decoded_without_special = tokenizer.decode(encoded, skip_special_tokens=True)
    print(f"Decoded without special tokens: {decoded_without_special}")
    
    print()


def batch_processing_example():
    """Demonstrate batch processing capabilities."""
    print("=== Batch Processing Example ===")
    
    tokenizer = HFTurkishTokenizer()
    
    texts = [
        "Merhaba dünya!",
        "Bu bir test cümlesidir.",
        "Türkçe dil işleme örneği."
    ]
    
    print("Original texts:")
    for i, text in enumerate(texts):
        print(f"  {i+1}. {text}")
    
    # Batch encode
    encoded_batch = tokenizer.encode(texts, add_special_tokens=True)
    print(f"\nEncoded batch: {encoded_batch}")
    
    # Batch decode
    decoded_batch = tokenizer.decode(encoded_batch, skip_special_tokens=True)
    print(f"Decoded batch: {decoded_batch}")
    
    print()


def call_method_example():
    """Demonstrate the __call__ method for model input preparation."""
    print("=== __call__ Method Example ===")
    
    tokenizer = HFTurkishTokenizer()
    
    text = "Bu cümle model girişi için hazırlanacak."
    
    print(f"Original text: {text}")
    
    # Use the __call__ method to get model inputs
    model_inputs = tokenizer(
        text,
        add_special_tokens=True,
        padding=True,
        truncation=True,
        max_length=50,
        return_tensors="pt"  # Return PyTorch tensors
    )
    
    print(f"Model inputs: {model_inputs}")
    print(f"Input IDs shape: {model_inputs['input_ids'].shape}")
    print(f"Attention mask shape: {model_inputs['attention_mask'].shape}")
    
    print()


def special_tokens_example():
    """Demonstrate special tokens handling."""
    print("=== Special Tokens Example ===")
    
    # Initialize with custom special tokens
    tokenizer = HFTurkishTokenizer(
        bos_token="<s>",
        eos_token="</s>",
        sep_token="<sep>",
        cls_token="<cls>",
        mask_token="<mask>",
        pad_token="<pad>",
        unk_token="<unk>"
    )
    
    print(f"Special tokens:")
    print(f"  BOS: {tokenizer.bos_token} (ID: {tokenizer.bos_token_id})")
    print(f"  EOS: {tokenizer.eos_token} (ID: {tokenizer.eos_token_id})")
    print(f"  SEP: {tokenizer.sep_token} (ID: {tokenizer.sep_token_id})")
    print(f"  CLS: {tokenizer.cls_token} (ID: {tokenizer.cls_token_id})")
    print(f"  MASK: {tokenizer.mask_token} (ID: {tokenizer.mask_token_id})")
    print(f"  PAD: {tokenizer.pad_token} (ID: {tokenizer.pad_token_id})")
    print(f"  UNK: {tokenizer.unk_token} (ID: {tokenizer.unk_token_id})")
    
    text = "Test cümlesi"
    
    # Encode with special tokens
    encoded = tokenizer.encode(text, add_special_tokens=True)
    print(f"\nEncoded: {encoded}")
    
    # Decode with special tokens
    decoded = tokenizer.decode(encoded)
    print(f"Decoded: {decoded}")
    
    # Decode without special tokens
    decoded_clean = tokenizer.decode(encoded, skip_special_tokens=True)
    print(f"Decoded (clean): {decoded_clean}")
    
    print()


def save_load_example():
    """Demonstrate saving and loading the tokenizer."""
    print("=== Save and Load Example ===")
    
    # Create a tokenizer
    tokenizer = HFTurkishTokenizer(
        model_max_length=512,
        bos_token="<s>",
        eos_token="</s>"
    )
    
    # Save the tokenizer
    save_dir = "saved_tokenizer"
    tokenizer.save_pretrained(save_dir)
    print(f"Tokenizer saved to: {save_dir}")
    
    # Load the tokenizer
    loaded_tokenizer = HFTurkishTokenizer.from_pretrained(save_dir)
    print(f"Tokenizer loaded from: {save_dir}")
    
    # Test that they work the same
    text = "Test cümlesi"
    
    original_encoded = tokenizer.encode(text)
    loaded_encoded = loaded_tokenizer.encode(text)
    
    print(f"Original encoded: {original_encoded}")
    print(f"Loaded encoded: {loaded_encoded}")
    print(f"Same result: {original_encoded == loaded_encoded}")
    
    # Clean up
    import shutil
    shutil.rmtree(save_dir)
    print(f"Cleaned up: {save_dir}")
    
    print()


def vocabulary_example():
    """Demonstrate vocabulary access."""
    print("=== Vocabulary Example ===")
    
    tokenizer = HFTurkishTokenizer()
    
    print(f"Vocabulary size: {tokenizer.vocab_size}")
    
    # Get vocabulary
    vocab = tokenizer.get_vocab()
    print(f"Vocabulary keys: {list(vocab.keys())[:10]}...")  # Show first 10 keys
    
    # Test some specific tokens
    test_tokens = ["merhaba", "dünya", "<pad>", "<eos>", "<unknown>"]
    
    for token in test_tokens:
        if token in vocab:
            token_id = vocab[token]
            print(f"  '{token}' -> ID: {token_id}")
        else:
            print(f"  '{token}' -> Not in vocabulary")
    
    print()


def main():
    """Run all examples."""
    print("Hugging Face Turkish Tokenizer Examples")
    print("=" * 50)
    print()
    
    try:
        basic_tokenization_example()
        encoding_decoding_example()
        batch_processing_example()
        call_method_example()
        special_tokens_example()
        save_load_example()
        vocabulary_example()
        
        print("All examples completed successfully!")
        
    except Exception as e:
        print(f"Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
