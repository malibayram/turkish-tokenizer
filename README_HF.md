# Turkish Tokenizer - Hugging Face Integration

This repository now includes a Hugging Face compatible Turkish tokenizer that can be seamlessly integrated with the Hugging Face Transformers library.

## Features

- **Full Hugging Face Compatibility**: Inherits from `PreTrainedTokenizer` and implements all required methods
- **Turkish Morphological Analysis**: Leverages the existing Turkish tokenizer's morphological capabilities
- **Special Tokens Support**: Full support for BOS, EOS, PAD, UNK, SEP, CLS, and MASK tokens
- **Batch Processing**: Support for batch tokenization and encoding
- **Save/Load Functionality**: Can save and load tokenizer configurations
- **Model Integration**: Ready to use with Hugging Face models and training pipelines

## Installation

```bash
pip install turkish-tokenizer
```

For development installation:

```bash
git clone https://github.com/malibayram/turkish-tokenizer.git
cd turkish-tokenizer
pip install -e .
```

## Quick Start

### Basic Usage

```python
from turkish_tokenizer import HFTurkishTokenizer

# Initialize the tokenizer
tokenizer = HFTurkishTokenizer()

# Tokenize text
text = "Merhaba dünya! Bu bir test cümlesidir."
tokens = tokenizer.tokenize(text)
print(tokens)

# Encode text
encoded = tokenizer.encode(text, add_special_tokens=True)
print(encoded)

# Decode back to text
decoded = tokenizer.decode(encoded, skip_special_tokens=True)
print(decoded)
```

### Model Input Preparation

```python
# Prepare inputs for a model
model_inputs = tokenizer(
    "Bu cümle model girişi için hazırlanacak.",
    add_special_tokens=True,
    padding=True,
    truncation=True,
    max_length=512,
    return_tensors="pt"  # Return PyTorch tensors
)

print(model_inputs)
# Output: {'input_ids': tensor([[...]]), 'attention_mask': tensor([[...]])}
```

### Batch Processing

```python
texts = [
    "Merhaba dünya!",
    "Bu bir test cümlesidir.",
    "Türkçe dil işleme örneği."
]

# Batch encode
encoded_batch = tokenizer.encode(texts, add_special_tokens=True)
print(encoded_batch)

# Batch decode
decoded_batch = tokenizer.decode(encoded_batch, skip_special_tokens=True)
print(decoded_batch)
```

### Custom Special Tokens

```python
# Initialize with custom special tokens
tokenizer = HFTurkishTokenizer(
    bos_token="<s>",
    eos_token="</s>",
    sep_token="<sep>",
    cls_token="<cls>",
    mask_token="<mask>",
    pad_token="<pad>",
    unk_token="<unk>",
    model_max_length=512
)

# Use the tokenizer
encoded = tokenizer.encode("Test cümlesi", add_special_tokens=True)
print(encoded)
```

### Save and Load

```python
# Save the tokenizer
tokenizer.save_pretrained("./saved_tokenizer")

# Load the tokenizer
loaded_tokenizer = HFTurkishTokenizer.from_pretrained("./saved_tokenizer")

# Test that they work the same
text = "Test cümlesi"
assert tokenizer.encode(text) == loaded_tokenizer.encode(text)
```

## Integration with Hugging Face Models

### Training with Transformers

```python
from transformers import AutoModelForCausalLM, TrainingArguments, Trainer
from turkish_tokenizer import HFTurkishTokenizer

# Initialize tokenizer and model
tokenizer = HFTurkishTokenizer()
model = AutoModelForCausalLM.from_pretrained("gpt2")  # Example model

# Resize model embeddings to match tokenizer vocabulary
model.resize_token_embeddings(len(tokenizer))

# Prepare training data
def tokenize_function(examples):
    return tokenizer(
        examples["text"],
        padding=True,
        truncation=True,
        max_length=512
    )

# Use with Trainer
training_args = TrainingArguments(
    output_dir="./results",
    per_device_train_batch_size=8,
    num_train_epochs=3,
    save_steps=1000,
    save_total_limit=2,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    data_collator=lambda data: {'input_ids': torch.stack([f['input_ids'] for f in data])}
)
```

### Using with AutoTokenizer

```python
from transformers import AutoTokenizer

# Register the tokenizer class
AutoTokenizer.register("turkish-tokenizer", HFTurkishTokenizer)

# Use with AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("path/to/saved/tokenizer")
```

## API Reference

### HFTurkishTokenizer

#### Constructor Parameters

- `vocab_file` (str, optional): Path to the roots vocabulary file
- `suffixes_file` (str, optional): Path to the suffixes vocabulary file
- `bpe_file` (str, optional): Path to the BPE tokens vocabulary file
- `model_max_length` (int, optional): Maximum sequence length
- `padding_side` (str): Side to apply padding ('left' or 'right')
- `truncation_side` (str): Side to apply truncation ('left' or 'right')
- `pad_token` (str): Padding token
- `eos_token` (str): End of sequence token
- `unk_token` (str): Unknown token
- `bos_token` (str, optional): Beginning of sequence token
- `sep_token` (str, optional): Separator token
- `cls_token` (str, optional): Classification token
- `mask_token` (str, optional): Mask token
- `additional_special_tokens` (List[str], optional): Additional special tokens
- `clean_up_tokenization_spaces` (bool): Whether to clean up spaces
- `split_special_tokens` (bool): Whether to split special tokens

#### Methods

- `tokenize(text: str) -> List[str]`: Tokenize text into tokens
- `encode(text, **kwargs) -> List[int]`: Encode text to token IDs
- `decode(token_ids, **kwargs) -> str`: Decode token IDs to text
- `convert_tokens_to_ids(tokens) -> List[int]`: Convert tokens to IDs
- `convert_ids_to_tokens(ids) -> List[str]`: Convert IDs to tokens
- `save_pretrained(save_directory)`: Save tokenizer to directory
- `from_pretrained(pretrained_model_name_or_path)`: Load tokenizer from directory
- `__call__(text, **kwargs) -> BatchEncoding`: Main method for model input preparation

## Examples

See the `examples/hf_tokenizer_example.py` file for comprehensive examples demonstrating all features.

## Differences from Original Tokenizer

The `HFTurkishTokenizer` wraps the original `TurkishTokenizer` and adds:

1. **Hugging Face Interface**: Full compatibility with Hugging Face Transformers
2. **Special Tokens**: Proper handling of BOS, EOS, PAD, etc.
3. **Batch Processing**: Support for processing multiple texts at once
4. **Model Integration**: Ready for use with Hugging Face models
5. **Save/Load**: Persistence of tokenizer configuration
6. **Padding/Truncation**: Built-in support for sequence length management

The underlying Turkish morphological analysis and tokenization logic remains the same, ensuring the same high-quality Turkish language processing.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
