# Turkish Tokenizer

A high-performance Turkish tokenizer with Rust backend and Python wrapper, designed for efficient natural language processing of Turkish text.

## Features

- **High Performance**: Rust backend for fast tokenization
- **Turkish Language Support**: Optimized for Turkish morphology and grammar
- **Python Integration**: Easy-to-use Python wrapper
- **Comprehensive Coverage**: Handles Turkish roots, suffixes, and BPE tokens
- **Command Line Interface**: CLI tool for batch processing

## Installation

```bash
pip install turkish-tokenizer
```

## Quick Start

```python
from turkish_tokenizer import TurkishTokenizer

# Initialize the tokenizer
tokenizer = TurkishTokenizer()

# Tokenize text
text = "Merhaba dünya! Bu bir test cümlesidir."
tokens = tokenizer.tokenize(text)
print(tokens)

# Decode tokens back to text
decoded_text = tokenizer.decode(tokens)
print(decoded_text)
```

## Command Line Usage

```bash
# Tokenize a text file
turkish-tokenizer tokenize input.txt output.txt

# Decode tokens back to text
turkish-tokenizer decode input_tokens.txt output_text.txt
```

## API Reference

### TurkishTokenizer

The main tokenizer class.

#### Methods

- `tokenize(text: str) -> List[int]`: Tokenize input text into token IDs
- `decode(tokens: List[int]) -> str`: Decode token IDs back to text
- `encode(text: str) -> List[int]`: Alias for tokenize method

## Development

### Setup

1. Clone the repository
2. Install development dependencies: `pip install -e ".[dev]"`
3. Run tests: `pytest`

### Building

```bash
python -m build
```

## License

MIT License - see LICENSE file for details.

## Changelog

### 0.1.3 (2024-12-19)

- **FIXED**: JSON vocabulary files are now properly included in the package distribution
- **FIXED**: MANIFEST.in corrected to include JSON files from the right directory structure
- **FIXED**: Package data configuration updated to ensure JSON files are bundled

### 0.1.2 (2024-12-19)

- **ADDED**: Command line interface (CLI) for batch processing
- **ADDED**: Comprehensive test suite
- **IMPROVED**: Better error handling and validation
- **IMPROVED**: Enhanced documentation and examples

### 0.1.1 (2024-12-19)

- **FIXED**: Package metadata and dependencies
- **IMPROVED**: Better package structure and organization

### 0.1.0 (2024-12-19)

- **INITIAL**: First release with basic tokenization functionality
- **FEATURES**: Turkish root and suffix matching
- **FEATURES**: BPE tokenization support
- **FEATURES**: Python wrapper for Rust backend

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

Ali Bayram - malibayram20@gmail.com

## Repository

https://github.com/malibayram/turkish-tokenizer
