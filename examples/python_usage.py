#!/usr/bin/env python3
"""
Example usage of the Rust-based Turkish tokenizer from Python.

This demonstrates how to use the high-performance Rust implementation
of the Turkish tokenizer from Python code.
"""

def main():
    try:
        # Import the Rust-based tokenizer
        from turkish_tokenizer_rs import TokenType, TurkishTokenizer
        
        print("Turkish Tokenizer - Rust Implementation from Python")
        print("=" * 55)
        
        # Initialize the tokenizer
        tokenizer = TurkishTokenizer()
        
        print(f"Vocabulary size: {tokenizer.vocab_size()}")
        print(f"Pad token: '{tokenizer.pad_token}' (ID: {tokenizer.pad_token_id})")
        print(f"EOS token: '{tokenizer.eos_token}' (ID: {tokenizer.eos_token_id})")
        print()
        
        # Test examples
        examples = [
            "merhaba dünya",
            "Türkçe tokenizer", 
            "merhabaDünya",
            "kitaplarımızdan",
            "geliyormuşsun",
        ]
        
        for text in examples:
            print(f"Text: '{text}'")
            
            # Get tokens
            tokens = tokenizer.tokenize(text)
            print(f"  Tokens: {tokens}")
            
            # Get token IDs
            token_ids = tokenizer.encode(text)
            print(f"  Token IDs: {token_ids}")
            
            # Get detailed token information
            detailed_tokens = tokenizer.tokenize_text(text)
            print("  Detailed tokens:")
            for i, token in enumerate(detailed_tokens):
                print(f"    {i}: '{token.token}' (ID: {token.id}, Type: {token.token_type})")
            
            print()
        
        # Test compatibility with ML frameworks
        print("ML Framework Compatibility:")
        result = tokenizer("merhaba dünya")
        print(f"  Input IDs: {result['input_ids']}")
        print(f"  Attention mask: {result['attention_mask']}")
        
        # Performance comparison hint
        print("\nPerformance Note:")
        print("This Rust implementation is typically 10-100x faster than pure Python!")
        
    except ImportError as e:
        print(f"Error: Could not import turkish_tokenizer_rs: {e}")
        print("\nTo install the Rust-based tokenizer:")
        print("1. Install maturin: pip install maturin")
        print("2. Build and install: maturin develop")
        print("3. Or build wheel: maturin build --release")

if __name__ == "__main__":
    main()
