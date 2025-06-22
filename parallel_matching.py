# Parallel processing approaches for vocabulary matching

import multiprocessing as mp
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from functools import partial

from tqdm import tqdm


# Approach 1: Thread-based parallelism (simplest)
def match_word_thread(word_id_tuple):
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

def parallel_matching_threads(vocab_dict, max_workers=None):
    """Thread-based parallel processing"""
    if max_workers is None:
        max_workers = min(32, (mp.cpu_count() or 1) + 4)
    
    print(f"Using {max_workers} threads...")
    start_time = time.time()
    
    qwen_tokenizer_matches = {}
    not_matched = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_word = {executor.submit(match_word_thread, item): item[0] 
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
    
    print(f"\n✅ Thread processing completed in {elapsed_time:.2f} seconds")
    print(f"📊 Results: {len(qwen_tokenizer_matches):,} matched, {len(not_matched):,} not matched")
    print(f"📈 Match rate: {len(qwen_tokenizer_matches)/len(vocab_dict)*100:.1f}%")
    
    return qwen_tokenizer_matches, not_matched

# Approach 2: Process-based parallelism (more complex but potentially faster)
def match_word_process(word_id_tuple, qwen_vocab):
    """Process-based matching function"""
    word, id = word_id_tuple
    word_with_space = f"Ġ{word}"
    word_capitalized = f"Ġ{word.capitalize()}"
    
    if word in qwen_vocab:
        return (word, qwen_vocab[word])
    elif word_with_space in qwen_vocab:
        return (word_with_space, qwen_vocab[word_with_space])
    elif word_capitalized in qwen_vocab:
        return (word_capitalized, qwen_vocab[word_capitalized])
    else:
        return None

def parallel_matching_processes(vocab_dict, max_workers=None):
    """Process-based parallel processing"""
    if max_workers is None:
        max_workers = mp.cpu_count()
    
    print(f"Using {max_workers} processes...")
    start_time = time.time()
    
    # Create partial function with qwen_vocab
    match_func = partial(match_word_process, qwen_vocab=qwen_tokenizer.vocab)
    
    qwen_tokenizer_matches = {}
    not_matched = []
    
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_word = {executor.submit(match_func, item): item[0] 
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
    
    print(f"\n✅ Process processing completed in {elapsed_time:.2f} seconds")
    print(f"📊 Results: {len(qwen_tokenizer_matches):,} matched, {len(not_matched):,} not matched")
    print(f"📈 Match rate: {len(qwen_tokenizer_matches)/len(vocab_dict)*100:.1f}%")
    
    return qwen_tokenizer_matches, not_matched

# Approach 3: Chunked processing (memory efficient)
def process_chunk(chunk, qwen_vocab):
    """Process a chunk of words"""
    matches = {}
    not_matched = []
    
    for word, id in chunk:
        word_with_space = f"Ġ{word}"
        word_capitalized = f"Ġ{word.capitalize()}"
        
        if word in qwen_vocab:
            matches[word] = qwen_vocab[word]
        elif word_with_space in qwen_vocab:
            matches[word_with_space] = qwen_vocab[word_with_space]
        elif word_capitalized in qwen_vocab:
            matches[word_capitalized] = qwen_vocab[word_capitalized]
        else:
            not_matched.append(word)
    
    return matches, not_matched

def parallel_matching_chunked(vocab_dict, chunk_size=1000, max_workers=None):
    """Chunked parallel processing"""
    if max_workers is None:
        max_workers = mp.cpu_count()
    
    print(f"Using {max_workers} processes with chunk size {chunk_size}...")
    start_time = time.time()
    
    # Split vocabulary into chunks
    vocab_items = list(vocab_dict.items())
    chunks = [vocab_items[i:i + chunk_size] for i in range(0, len(vocab_items), chunk_size)]
    
    print(f"Split into {len(chunks)} chunks...")
    
    qwen_tokenizer_matches = {}
    not_matched = []
    
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Submit chunk processing tasks
        future_to_chunk = {executor.submit(process_chunk, chunk, qwen_tokenizer.vocab): i 
                          for i, chunk in enumerate(chunks)}
        
        # Process results with progress bar
        for future in tqdm(future_to_chunk, desc="Processing chunks", unit="chunks"):
            chunk_matches, chunk_not_matched = future.result()
            qwen_tokenizer_matches.update(chunk_matches)
            not_matched.extend(chunk_not_matched)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print(f"\n✅ Chunked processing completed in {elapsed_time:.2f} seconds")
    print(f"📊 Results: {len(qwen_tokenizer_matches):,} matched, {len(not_matched):,} not matched")
    print(f"📈 Match rate: {len(qwen_tokenizer_matches)/len(vocab_dict)*100:.1f}%")
    
    return qwen_tokenizer_matches, not_matched

# Usage examples:
if __name__ == "__main__":
    # Choose your approach:
    
    # 1. Thread-based (simplest, good for I/O bound tasks)
    # qwen_tokenizer_matches, not_matched = parallel_matching_threads(vocab_dict)
    
    # 2. Process-based (good for CPU bound tasks)
    # qwen_tokenizer_matches, not_matched = parallel_matching_processes(vocab_dict)
    
    # 3. Chunked processing (memory efficient for large datasets)
    # qwen_tokenizer_matches, not_matched = parallel_matching_chunked(vocab_dict, chunk_size=500)
    
    pass 