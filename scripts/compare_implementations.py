#!/usr/bin/env python3
"""
Comparison script to verify that the Rust implementation produces
the same tokenization results as the Python implementation.
"""

import json
import os
import subprocess
import sys

# Add the parent directory to the path to import the tokenizer
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from turkish_tokenizer import TurkishTokenizer


def get_rust_output(text):
    """Get tokenization output from the Rust implementation"""
    # Create a simple Rust program that outputs JSON
    rust_code = f'''
use turkish_tokenizer::TurkishTokenizer;

fn main() -> Result<(), Box<dyn std::error::Error>> {{
    let tokenizer = TurkishTokenizer::new()?;
    let text = r#"{text}"#;
    
    let token_ids = tokenizer.encode(text);
    let tokens = tokenizer.tokenize(text);
    
    let output = serde_json::json!({{
        "token_ids": token_ids,
        "tokens": tokens
    }});
    
    println!("{{}}", output);
    Ok(())
}}
'''
    
    # Write temporary Rust file
    with open('/tmp/rust_tokenizer_test.rs', 'w') as f:
        f.write(rust_code)
    
    # Create temporary Cargo.toml
    cargo_toml = '''
[package]
name = "rust_tokenizer_test"
version = "0.1.0"
edition = "2021"

[dependencies]
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
turkish-tokenizer = { path = "../.." }
'''
    
    os.makedirs('/tmp/rust_test', exist_ok=True)
    with open('/tmp/rust_test/Cargo.toml', 'w') as f:
        f.write(cargo_toml)
    
    with open('/tmp/rust_test/src/main.rs', 'w') as f:
        f.write(rust_code)
    
    # Run the Rust program
    try:
        result = subprocess.run(
            ['cargo', 'run'], 
            cwd='/tmp/rust_test',
            capture_output=True, 
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return json.loads(result.stdout.strip())
        else:
            print(f"Rust error: {result.stderr}")
            return None
    except Exception as e:
        print(f"Failed to run Rust implementation: {e}")
        return None

def main():
    print("Comparing Python and Rust Turkish Tokenizer Implementations")
    print("=" * 60)
    
    # Initialize Python tokenizer
    python_tokenizer = TurkishTokenizer()
    
    # Test cases
    test_cases = [
        "merhaba dünya",
        "Türkçe tokenizer",
        "merhabaDünya",
        "geliyorum",
        "kitaplarımı",
        "kitaplarımızdan",
        "geliyormuşsun",
        "Merhaba Dünya Türkçe",
    ]
    
    all_match = True
    
    for text in test_cases:
        print(f"\nTesting: '{text}'")
        
        # Get Python results
        python_tokens = python_tokenizer.tokenize(text)
        python_ids = python_tokenizer.encode(text)
        
        # Get Rust results
        rust_result = get_rust_output(text)
        
        if rust_result is None:
            print("  ❌ Failed to get Rust output")
            all_match = False
            continue
        
        rust_tokens = rust_result['tokens']
        rust_ids = rust_result['token_ids']
        
        # Compare results
        tokens_match = python_tokens == rust_tokens
        ids_match = python_ids == rust_ids
        
        print(f"  Python tokens: {python_tokens}")
        print(f"  Rust tokens:   {rust_tokens}")
        print(f"  Tokens match:  {'✅' if tokens_match else '❌'}")
        
        print(f"  Python IDs: {python_ids}")
        print(f"  Rust IDs:   {rust_ids}")
        print(f"  IDs match:    {'✅' if ids_match else '❌'}")
        
        if not (tokens_match and ids_match):
            all_match = False
    
    print("\n" + "=" * 60)
    if all_match:
        print("🎉 All tests passed! Rust implementation matches Python implementation.")
    else:
        print("❌ Some tests failed. There are differences between implementations.")
    
    # Clean up temporary files
    try:
        import shutil
        shutil.rmtree('/tmp/rust_test', ignore_errors=True)
        os.remove('/tmp/rust_tokenizer_test.rs')
    except:
        pass

if __name__ == "__main__":
    main()
