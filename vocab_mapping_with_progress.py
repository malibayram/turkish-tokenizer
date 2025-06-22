from tqdm import tqdm

# Add progress tracking to the vocabulary mapping
vocab_to_qwen_token = {}
for i in tqdm(range(len(vocab_list)), desc="Mapping vocabulary to Qwen tokens"):
    token_ids = qwen_tokenizer.encode(vocab_list[i])
    token_ids0 = qwen_tokenizer.encode(tr_capitalize(vocab_list[i]))
    if (len(token_ids)) > (len(token_ids0)):
        token_ids0.remove(151643)
        vocab_to_qwen_token[vocab_list[i]] = token_ids0
    else:
        token_ids.remove(151643)
        vocab_to_qwen_token[vocab_list[i]] = token_ids

print(f"Completed mapping {len(vocab_to_qwen_token)} vocabulary items")
vocab_to_qwen_token 