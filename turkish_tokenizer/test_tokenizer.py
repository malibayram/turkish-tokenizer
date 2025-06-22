#!/usr/bin/env python3
"""
Simple test script for the Turkish tokenizer.
"""

import json
import sys
from pathlib import Path

# Add the current directory to the path so we can import the package
sys.path.insert(0, str(Path(__file__).parent))

try:
    # Try package import (for python -m turkish_tokenizer.test_tokenizer)
    from turkish_tokenizer import TurkishTokenizer, tokenize
    print("✅ Successfully imported Turkish tokenizer (package mode)")
except ImportError:
    try:
        # Fallback to local import (for python test_tokenizer.py)
        from core import tokenize
        from tokenizer import TurkishTokenizer
        print("✅ Successfully imported Turkish tokenizer (local mode)")
    except ImportError as e:
        print(f"❌ Failed to import Turkish tokenizer: {e}")
        sys.exit(1)

def test_basic_tokenization():
    """Test basic tokenization functionality."""
    print("\n🧪 Testing basic tokenization...")
    
    # Test cases
    test_cases = [
        ("merhaba", "Basic Turkish word"),
        ("Merhaba", "Word with uppercase"),
        ("merhaba dünya", "Simple sentence"),
        ("Merhaba Dünya!", "Sentence with uppercase and punctuation"),
    ]
    
    tokenizer = TurkishTokenizer()
    
    for text, description in test_cases:
        try:
            tokens, ids = tokenizer.tokenize(text)
            print(f"✅ {description}: '{text}' -> {len(tokens)} tokens")
            print(f"   Tokens: {tokens[:5]}{'...' if len(tokens) > 5 else ''}")
        except Exception as e:
            print(f"❌ {description}: '{text}' failed - {e}")
            return False
    
    return True

def test_convenience_function():
    """Test the convenience tokenize function."""
    print("\n🧪 Testing convenience function...")
    
    try:
        tokens, ids = tokenize("test")
        print(f"✅ Convenience function works: {len(tokens)} tokens")
        return True
    except Exception as e:
        print(f"❌ Convenience function failed: {e}")
        return False

def test_decode_functionality():
    """Test decoding functionality."""
    print("\n🧪 Testing decode functionality...")
    
    tokenizer = TurkishTokenizer()
    original_text = "merhaba"
    
    try:
        tokens, ids = tokenizer.tokenize(original_text)
        decoded_text = tokenizer.decode(ids)
        print(f"✅ Decode works: '{original_text}' -> '{decoded_text}'")
        return True
    except Exception as e:
        print(f"❌ Decode failed: {e}")
        return False

def test_batch_processing():
    """Test batch processing functionality."""
    print("\n🧪 Testing batch processing...")
    
    tokenizer = TurkishTokenizer()
    texts = ["merhaba", "dünya", "test"]
    
    try:
        results = tokenizer.tokenize_batch(texts)
        print(f"✅ Batch processing works: {len(results)} results")
        return True
    except Exception as e:
        print(f"❌ Batch processing failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Starting Turkish tokenizer tests...")
    
    tests = [
        test_basic_tokenization,
        test_convenience_function,
        test_decode_functionality,
        test_batch_processing,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The tokenizer is working correctly.")
        return 0
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 