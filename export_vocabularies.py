#!/usr/bin/env python3
"""
Export vocabularies to JSON files for Rust processing
"""

import json

from transformers import AutoTokenizer


def export_vocabularies():
    """Export Turkish and Qwen vocabularies to JSON files"""
    
    print("📖 Loading tokenizers...")
    
    # Load Qwen tokenizer
    qwen_tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3-Embedding-0.6B", use_fast=True)
    
    # Load Turkish vocabulary (assuming you have it from your notebook)
    # You'll need to run this in your notebook environment where vocab_dict is available
    try:
        from turkish_tokenizer import turkish_tokenizer as tt
        vocab_dict = {**tt.bpe_tokens, **tt.suffixes, **tt.roots}
        print(f"✅ Loaded Turkish vocabulary with {len(vocab_dict)} words")
    except ImportError:
        print("❌ Could not import Turkish tokenizer. Please run this in your notebook environment.")
        return
    
    # Export Turkish vocabulary
    print("💾 Exporting Turkish vocabulary...")
    with open("turkish_vocab.json", "w", encoding="utf-8") as f:
        json.dump(vocab_dict, f, ensure_ascii=False, indent=2)
    
    # Export Qwen vocabulary
    print("💾 Exporting Qwen vocabulary...")
    with open("qwen_vocab.json", "w", encoding="utf-8") as f:
        json.dump(qwen_tokenizer.vocab, f, ensure_ascii=False, indent=2)
    
    print("✅ Export completed!")
    print(f"📁 Files created:")
    print(f"   • turkish_vocab.json ({len(vocab_dict)} words)")
    print(f"   • qwen_vocab.json ({len(qwen_tokenizer.vocab)} tokens)")
    print("\n🚀 Now you can run the Rust application:")
    print("   cargo run -- -t turkish_vocab.json -q qwen_vocab.json -o results.json")

if __name__ == "__main__":
    export_vocabularies() 