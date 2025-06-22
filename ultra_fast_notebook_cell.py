# Copy this into a new notebook cell for ultra-fast matching

import time

print("🚀 Starting ultra-fast set-based matching...")
start_time = time.time()

# Convert to sets for O(1) lookup - this is the key optimization!
qwen_vocab_set = set(qwen_tokenizer.vocab.keys())
turkish_words = set(vocab_dict.keys())

print(f"📊 Processing {len(turkish_words):,} Turkish words against {len(qwen_vocab_set):,} Qwen tokens...")

# Direct matches (exact matches)
direct_matches = turkish_words & qwen_vocab_set

# Space-prefixed matches (Ġword)
space_prefixed = {f"Ġ{word}" for word in turkish_words}
space_matches = space_prefixed & qwen_vocab_set

# Capitalized space-prefixed matches (ĠWord)
capitalized_space = {f"Ġ{word.capitalize()}" for word in turkish_words}
capitalized_matches = capitalized_space & qwen_vocab_set

print(f"✅ Found {len(direct_matches):,} direct matches")
print(f"✅ Found {len(space_matches):,} space-prefixed matches")
print(f"✅ Found {len(capitalized_matches):,} capitalized matches")

# Combine all matches
qwen_tokenizer_matches = {}

# Add direct matches
for word in direct_matches:
    qwen_tokenizer_matches[word] = qwen_tokenizer.vocab[word]

# Add space-prefixed matches
for word in space_matches:
    qwen_tokenizer_matches[word] = qwen_tokenizer.vocab[word]

# Add capitalized matches
for word in capitalized_matches:
    qwen_tokenizer_matches[word] = qwen_tokenizer.vocab[word]

# Find not matched words
all_matched_originals = set()
for word in direct_matches:
    all_matched_originals.add(word)
for word in space_matches:
    all_matched_originals.add(word[1:])  # Remove Ġ prefix
for word in capitalized_matches:
    all_matched_originals.add(word[1:].lower())  # Remove Ġ prefix and lowercase

not_matched = list(turkish_words - all_matched_originals)

end_time = time.time()
elapsed_time = end_time - start_time

print(f"\n✅ Ultra-fast processing completed in {elapsed_time:.2f} seconds")
print(f"📊 Results: {len(qwen_tokenizer_matches):,} matched, {len(not_matched):,} not matched")
print(f"📈 Match rate: {len(qwen_tokenizer_matches)/len(vocab_dict)*100:.1f}%")
print(f"⚡ Speed: {len(vocab_dict)/elapsed_time:.0f} words/second")

# Return results
len(qwen_tokenizer_matches), len(not_matched) 