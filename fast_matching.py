# Ultra-fast vocabulary matching - optimized approach

import time

import numpy as np
from tqdm import tqdm


def fast_matching_approach():
    """Ultra-fast matching using optimized data structures"""
    
    print("🚀 Starting ultra-fast matching...")
    start_time = time.time()
    
    # Convert vocab to sets for O(1) lookup
    qwen_vocab_set = set(qwen_tokenizer.vocab.keys())
    
    # Pre-compute all possible variations
    print("📝 Pre-computing word variations...")
    all_variations = {}
    
    for word in tqdm(vocab_dict.keys(), desc="Pre-computing", unit="words"):
        variations = [
            word,
            f"Ġ{word}",
            f"Ġ{word.capitalize()}"
        ]
        all_variations[word] = variations
    
    # Batch process for maximum speed
    print("⚡ Batch processing matches...")
    qwen_tokenizer_matches = {}
    not_matched = []
    
    # Process in batches for better performance
    batch_size = 1000
    vocab_items = list(vocab_dict.items())
    
    for i in tqdm(range(0, len(vocab_items), batch_size), desc="Processing batches", unit="batch"):
        batch = vocab_items[i:i + batch_size]
        
        for word, id in batch:
            variations = all_variations[word]
            
            # Find first matching variation
            matched = False
            for variation in variations:
                if variation in qwen_vocab_set:
                    qwen_tokenizer_matches[variation] = qwen_tokenizer.vocab[variation]
                    matched = True
                    break
            
            if not matched:
                not_matched.append(word)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print(f"\n✅ Ultra-fast processing completed in {elapsed_time:.2f} seconds")
    print(f"📊 Results: {len(qwen_tokenizer_matches):,} matched, {len(not_matched):,} not matched")
    print(f"📈 Match rate: {len(qwen_tokenizer_matches)/len(vocab_dict)*100:.1f}%")
    print(f"⚡ Speed: {len(vocab_dict)/elapsed_time:.0f} words/second")
    
    return qwen_tokenizer_matches, not_matched

# Even faster approach using direct set operations
def ultra_fast_matching():
    """Ultra-fast matching using set operations"""
    
    print("🚀 Starting ultra-fast set-based matching...")
    start_time = time.time()
    
    # Convert to sets for O(1) lookup
    qwen_vocab_set = set(qwen_tokenizer.vocab.keys())
    turkish_words = set(vocab_dict.keys())
    
    # Direct matches
    direct_matches = turkish_words & qwen_vocab_set
    
    # Space-prefixed matches
    space_prefixed = {f"Ġ{word}" for word in turkish_words}
    space_matches = space_prefixed & qwen_vocab_set
    
    # Capitalized space-prefixed matches
    capitalized_space = {f"Ġ{word.capitalize()}" for word in turkish_words}
    capitalized_matches = capitalized_space & qwen_vocab_set
    
    # Combine all matches
    qwen_tokenizer_matches = {}
    
    # Add direct matches
    for word in direct_matches:
        qwen_tokenizer_matches[word] = qwen_tokenizer.vocab[word]
    
    # Add space-prefixed matches
    for word in space_matches:
        original_word = word[1:]  # Remove Ġ prefix
        qwen_tokenizer_matches[word] = qwen_tokenizer.vocab[word]
    
    # Add capitalized matches
    for word in capitalized_matches:
        original_word = word[1:].lower()  # Remove Ġ prefix and lowercase
        qwen_tokenizer_matches[word] = qwen_tokenizer.vocab[word]
    
    # Find not matched words
    all_matched_originals = set()
    for word in direct_matches:
        all_matched_originals.add(word)
    for word in space_matches:
        all_matched_originals.add(word[1:])
    for word in capitalized_matches:
        all_matched_originals.add(word[1:].lower())
    
    not_matched = list(turkish_words - all_matched_originals)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print(f"\n✅ Ultra-fast set processing completed in {elapsed_time:.2f} seconds")
    print(f"📊 Results: {len(qwen_tokenizer_matches):,} matched, {len(not_matched):,} not matched")
    print(f"📈 Match rate: {len(qwen_tokenizer_matches)/len(vocab_dict)*100:.1f}%")
    print(f"⚡ Speed: {len(vocab_dict)/elapsed_time:.0f} words/second")
    
    return qwen_tokenizer_matches, not_matched

# Run the fastest approach
if __name__ == "__main__":
    # Try the ultra-fast set-based approach first
    qwen_tokenizer_matches, not_matched = ultra_fast_matching() 