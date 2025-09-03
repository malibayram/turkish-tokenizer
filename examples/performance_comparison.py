#!/usr/bin/env python3
"""
Performance comparison between Python and Rust implementations
of the Turkish tokenizer.
"""

import os
import sys
import time

# Add the parent directory to import the Python tokenizer
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def benchmark_tokenizer(tokenizer, name, texts, iterations=1000):
    """Benchmark a tokenizer implementation"""
    print(f"\n🔥 Benchmarking {name} implementation:")
    
    # Warmup
    for text in texts[:5]:
        tokenizer.encode(text)
    
    total_time = 0
    total_tokens = 0
    
    start_time = time.time()
    for _ in range(iterations):
        for text in texts:
            tokens = tokenizer.encode(text)
            total_tokens += len(tokens)
    end_time = time.time()
    
    total_time = end_time - start_time
    avg_time_per_text = (total_time / (iterations * len(texts))) * 1000  # ms
    tokens_per_second = total_tokens / total_time
    
    print(f"  Total time: {total_time:.3f}s")
    print(f"  Average per text: {avg_time_per_text:.3f}ms")
    print(f"  Tokens per second: {tokens_per_second:,.0f}")
    
    return total_time, tokens_per_second

def main():
    print("Turkish Tokenizer Performance Comparison")
    print("=" * 45)
    
    # Test texts of varying complexity
    test_texts = [
        "merhaba",
        "merhaba dünya", 
        "Türkçe tokenizer",
        "kitaplarımızdan geliyormuşsun",
        "Türkçe doğal dil işleme çok önemli bir alan",
        "merhabaDünyaTürkçeTokenizerPerformansTestiÇokUzunKelimelerle",
        "Bu bir performans testi cümlesidir ve tokenizer hızını ölçmek için kullanılır",
    ]
    
    print(f"Test corpus: {len(test_texts)} texts")
    print(f"Iterations: 1000 per implementation")
    print()
    
    # Test Python implementation
    try:
        from turkish_tokenizer import TurkishTokenizer as PythonTokenizer
        python_tokenizer = PythonTokenizer()
        python_time, python_tps = benchmark_tokenizer(
            python_tokenizer, "Python", test_texts, 1000
        )
    except Exception as e:
        print(f"❌ Failed to test Python implementation: {e}")
        python_time, python_tps = None, None
    
    # Test Rust implementation
    try:
        import turkish_tokenizer_rs
        rust_tokenizer = turkish_tokenizer_rs.TurkishTokenizer()
        rust_time, rust_tps = benchmark_tokenizer(
            rust_tokenizer, "Rust", test_texts, 1000
        )
    except Exception as e:
        print(f"❌ Failed to test Rust implementation: {e}")
        rust_time, rust_tps = None, None
    
    # Compare results
    if python_time and rust_time:
        speedup = python_time / rust_time
        tps_improvement = rust_tps / python_tps
        
        print(f"\n🏆 Performance Comparison:")
        print(f"  Speedup: {speedup:.1f}x faster")
        print(f"  Throughput improvement: {tps_improvement:.1f}x more tokens/second")
        
        if speedup > 10:
            print(f"  🚀 Rust is significantly faster!")
        elif speedup > 2:
            print(f"  ⚡ Rust shows good performance improvement")
        else:
            print(f"  📊 Rust shows modest improvement")
    
    # Test correctness
    print(f"\n🔍 Correctness Check:")
    test_text = "kitaplarımızdan"
    
    if python_time and rust_time:
        python_result = python_tokenizer.encode(test_text)
        rust_result = rust_tokenizer.encode(test_text)
        
        if python_result == rust_result:
            print(f"  ✅ Results match: {python_result}")
        else:
            print(f"  ❌ Results differ!")
            print(f"    Python: {python_result}")
            print(f"    Rust:   {rust_result}")

if __name__ == "__main__":
    main()
