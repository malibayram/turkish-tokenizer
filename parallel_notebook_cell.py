# Copy this into a new notebook cell for parallel processing

import multiprocessing as mp
import time
from concurrent.futures import ThreadPoolExecutor

from tqdm import tqdm


def match_word_parallel(word_id_tuple):
    """Match a single word with the Qwen tokenizer"""
    word, id = word_id_tuple
    word_with_space = f"Ġ{word}"
    word_capitalized = f"Ġ{word.capitalize()}"
    
    if word in qwen_tokenizer.vocab:
        return (word, qwen_tokenizer.vocab[word])
    elif word_with_space in qwen_tokenizer.vocab:
        return (word_with_space, qwen_tokenizer.vocab[word_with_space])
    elif word_capitalized in qwen_tokenizer.vocab:
        return (word_capitalized, qwen_tokenizer.vocab[word_capitalized])
    else:
        return None

# Parallel processing with threads (simplest approach)
def run_parallel_matching():
    # Determine number of workers (adjust based on your system)
    max_workers = min(16, (mp.cpu_count() or 1) + 4)
    
    print(f"🚀 Starting parallel processing with {max_workers} threads...")
    print(f"📊 Processing {len(vocab_dict):,} words...")
    
    start_time = time.time()
    
    qwen_tokenizer_matches = {}
    not_matched = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_word = {executor.submit(match_word_parallel, item): item[0] 
                         for item in vocab_dict.items()}
        
        # Process results with progress bar
        for future in tqdm(future_to_word, desc="Matching vocabulary", unit="words"):
            result = future.result()
            if result is not None:
                qwen_tokenizer_matches[result[0]] = result[1]
            else:
                not_matched.append(future_to_word[future])
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print(f"\n✅ Parallel processing completed in {elapsed_time:.2f} seconds")
    print(f"📊 Results: {len(qwen_tokenizer_matches):,} matched, {len(not_matched):,} not matched")
    print(f"📈 Match rate: {len(qwen_tokenizer_matches)/len(vocab_dict)*100:.1f}%")
    
    return qwen_tokenizer_matches, not_matched

# Run the parallel processing
qwen_tokenizer_matches, not_matched = run_parallel_matching()

# Return results
len(qwen_tokenizer_matches), len(not_matched) 