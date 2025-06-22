# Turkish Tokenizer

A high-performance Turkish tokenizer with Rust backend and Python wrapper. This package combines linguistic rules with BPE (Byte Pair Encoding) for optimal tokenization of Turkish text.

## 🚀 Features

- **High Performance**: Rust backend for ultra-fast tokenization
- **Linguistic Rules**: Root and suffix matching based on Turkish morphology
- **BPE Support**: Byte Pair Encoding for unknown words
- **Special Tokens**: Handles spaces, newlines, tabs, and case sensitivity
- **Decoding**: Convert token IDs back to readable text
- **Easy Integration**: Simple Python API and command-line interface

## 📦 Installation

### From PyPI (Recommended)

```bash
pip install turkish-tokenizer
```

### From Source

```bash
git clone https://github.com/malibayram/turkish-tokenizer.git
cd turkish-tokenizer
pip install -e .
```

### Prerequisites

- Python 3.8 or higher
- Rust (for building the backend): Install from [rustup.rs](https://rustup.rs/)

## 🔧 Quick Start

### Python API

```python
from turkish_tokenizer import TurkishTokenizer

# Initialize the tokenizer
tokenizer = TurkishTokenizer()

# Tokenize text
text = "Merhaba dünya! Bu bir test cümlesidir."
tokens, token_ids = tokenizer.tokenize(text)

print("Tokens:", tokens)
print("Token IDs:", token_ids)

# Decode back to text
decoded_text = tokenizer.decode(token_ids)
print("Decoded:", decoded_text)
```

### Command Line

```bash
# Tokenize text
turkish-tokenizer "Merhaba dünya!"

# Tokenize from file
turkish-tokenizer -f input.txt

# Save output to file
turkish-tokenizer "Merhaba dünya!" -o output.json

# Build Rust backend
turkish-tokenizer --build

# Check if Rust backend is available
turkish-tokenizer --check
```

## 📚 API Reference

### TurkishTokenizer Class

#### `__init__()`

Initialize the tokenizer. No parameters required.

#### `tokenize(text: str) -> Tuple[List[str], List[int]]`

Tokenize the input text.

**Parameters:**

- `text` (str): The text to tokenize

**Returns:**

- `tokens` (List[str]): List of token strings
- `token_ids` (List[int]): List of token IDs

#### `decode(token_ids: List[int]) -> str`

Decode a list of token IDs back to text.

**Parameters:**

- `token_ids` (List[int]): List of token IDs to decode

**Returns:**

- `str`: The decoded text

#### `tokenize_batch(texts: List[str]) -> List[Tuple[List[str], List[int]]]`

Tokenize a batch of texts.

**Parameters:**

- `texts` (List[str]): List of texts to tokenize

**Returns:**

- List of tuples, each containing (tokens, token_ids)

#### `get_vocab_size() -> int`

Get the vocabulary size.

**Returns:**

- `int`: Total number of tokens in the vocabulary

#### `get_special_tokens() -> Dict[str, int]`

Get the special tokens and their IDs.

**Returns:**

- `Dict[str, int]`: Dictionary mapping special token names to their IDs

### Convenience Functions

#### `tokenize(text: str) -> Tuple[List[str], List[int]]`

Quick tokenization function for simple use cases.

```python
from turkish_tokenizer import tokenize

tokens, ids = tokenize("Merhaba dünya!")
```

## 🛠️ Development

### Setup Development Environment

```bash
git clone https://github.com/malibayram/turkish-tokenizer.git
cd turkish-tokenizer
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black turkish_tokenizer/
isort turkish_tokenizer/
```

### Type Checking

```bash
mypy turkish_tokenizer/
```

## 📦 Building and Publishing

### Building the Package

```bash
# Build source distribution
python -m build --sdist

# Build wheel
python -m build --wheel

# Build both
python -m build
```

### Publishing to PyPI

1. **Register on PyPI** (if you haven't already):

   ```bash
   pip install twine
   ```

2. **Upload to Test PyPI first**:

   ```bash
   twine upload --repository testpypi dist/*
   ```

3. **Upload to PyPI**:
   ```bash
   twine upload dist/*
   ```

### Publishing to Test PyPI

```bash
# Upload to Test PyPI
twine upload --repository testpypi dist/*

# Install from Test PyPI
pip install --index-url https://test.pypi.org/simple/ turkish-tokenizer
```

## 🔍 How It Works

The tokenizer uses a multi-stage approach:

1. **Special Token Detection**: Identifies spaces, newlines, tabs, and case changes
2. **Root Matching**: Matches words against a comprehensive Turkish root dictionary
3. **Suffix Matching**: Applies Turkish morphological rules for suffixes
4. **BPE Tokenization**: Uses Byte Pair Encoding for unknown words
5. **Decoding**: Applies reverse transformations to reconstruct text

### Token Types

- **Roots**: Base Turkish words (e.g., "kitab", "defter")
- **Suffixes**: Turkish grammatical suffixes (e.g., "ler", "i", "nin")
- **BPE Tokens**: Subword units for unknown words
- **Special Tokens**: `<space>`, `<newline>`, `<tab>`, `<uppercase>`, `<unknown>`

## 📊 Performance

| Method           | Speed              | Time for 1K words |
| ---------------- | ------------------ | ----------------- |
| Python (pure)    | ~100 words/sec     | ~10 seconds       |
| **Rust backend** | **~10K words/sec** | **~0.1 seconds**  |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Turkish linguistic resources and vocabulary
- Rust programming language and ecosystem
- Python packaging community

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/malibayram/turkish-tokenizer/issues)
- **Discussions**: [GitHub Discussions](https://github.com/malibayram/turkish-tokenizer/discussions)
- **Email**: malibayram20@gmail.com

## 🔄 Changelog

### 0.1.0 (2024-01-XX)

- Initial release
- Python API with Rust backend
- Command-line interface
- Comprehensive Turkish tokenization
- Decoding functionality
