# Add this cell to your notebook for progress tracking
import time

from tqdm import tqdm

qwen_tokenizer_matches = {}
not_matched = []

# Add progress bar with estimated time
total_words = len(vocab_dict)
print(f"Processing {total_words:,} words...")

start_time = time.time()

for word, id in tqdm(vocab_dict.items(), desc="Matching vocabulary", unit="words", total=total_words):
    word_with_space = f"Ġ{word}"
    word_capitalized = f"Ġ{word.capitalize()}"
    
    if word in qwen_tokenizer.vocab:
        qwen_tokenizer_matches[word] = qwen_tokenizer.vocab[word]
    elif word_with_space in qwen_tokenizer.vocab:
        qwen_tokenizer_matches[word_with_space] = qwen_tokenizer.vocab[word_with_space]
    elif word_capitalized in qwen_tokenizer.vocab:
        qwen_tokenizer_matches[word_capitalized] = qwen_tokenizer.vocab[word_capitalized]
    else:
        not_matched.append(word)

end_time = time.time()
elapsed_time = end_time - start_time

print(f"\n✅ Processing completed in {elapsed_time:.2f} seconds")
print(f"📊 Results: {len(qwen_tokenizer_matches):,} matched, {len(not_matched):,} not matched")
print(f"📈 Match rate: {len(qwen_tokenizer_matches)/total_words*100:.1f}%")

# Return the results
len(qwen_tokenizer_matches), len(not_matched) 