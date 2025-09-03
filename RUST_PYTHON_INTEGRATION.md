# Turkish Tokenizer - Rust ↔ Python Integration

This guide explains how to use the high-performance Rust implementation of the Turkish tokenizer from Python.

## 🚀 Quick Start

### Prerequisites

```bash
# Install Rust (if not already installed)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Install maturin for building Python extensions
pip install maturin
```

### Option 1: Development Installation

```bash
# Clone and navigate to the project
cd /path/to/turkish-tokenizer

# Build and install in development mode
maturin develop

# Test the installation
python -c "import turkish_tokenizer_rs; print('✅ Success!')"
```

### Option 2: Build and Install Wheel

```bash
# Build the wheel
maturin build --release

# Install the wheel
pip install target/wheels/turkish_tokenizer_rs-*.whl
```

## 📖 Usage from Python

### Basic Usage

```python
import turkish_tokenizer_rs

# Initialize the tokenizer
tokenizer = turkish_tokenizer_rs.TurkishTokenizer()

# Encode text
text = "merhaba dünya"
token_ids = tokenizer.encode(text)
print(f"Token IDs: {token_ids}")  # [4103, 2, 2608]

# Get string tokens
tokens = tokenizer.tokenize(text)
print(f"Tokens: {tokens}")  # ['merhaba', ' ', 'dünya']

# Get detailed token information
detailed_tokens = tokenizer.tokenize_text(text)
for token in detailed_tokens:
    print(f"'{token.token}' (ID: {token.id}, Type: {token.token_type})")
```

### Advanced Features

```python
import turkish_tokenizer_rs

tokenizer = turkish_tokenizer_rs.TurkishTokenizer()

# Access vocabulary
vocab_size = tokenizer.vocab_size()
vocab = tokenizer.get_vocab()  # Returns dict[str, int]

# Special tokens
pad_id = tokenizer.pad_token_id
eos_id = tokenizer.eos_token_id

# Token utilities
token_id = tokenizer.token_to_id("merhaba")  # Returns Optional[int]
exists = tokenizer.contains_token("merhaba")  # Returns bool

# ML framework compatibility
result = tokenizer("merhaba dünya")
input_ids = result["input_ids"]
attention_mask = result["attention_mask"]
```

### Complex Turkish Examples

```python
# Morphologically complex word
tokens = tokenizer.tokenize("kitaplarımızdan")
# Output: ['kitap', 'lar', 'ım', 'ız', 'dan']
# Meaning: "from our books"

# Verb conjugation
tokens = tokenizer.tokenize("geliyormuşsun")
# Output: ['gel', 'i', 'yor', 'muş', 'sun']
# Meaning: "you were apparently coming"

# CamelCase handling
tokens = tokenizer.tokenize("merhabaDünya")
# Output: ['merhaba', '<uppercase>', 'dünya']
```

## ⚡ Performance

The Rust implementation provides significant performance improvements:

- **2.1x faster** than Python implementation
- **1.8M+ tokens/second** throughput
- **~7 microseconds** average per text
- **Zero overhead** for vocabulary lookups
- **Memory efficient** with embedded data

### Benchmark Results

```
Python Implementation:  0.015ms per text,   895K tokens/sec
Rust Implementation:    0.007ms per text, 1,873K tokens/sec
Speedup:               2.1x faster
```

## 🔄 Migration from Python

The Rust implementation is designed to be a drop-in replacement:

```python
# Before (Python)
from turkish_tokenizer import TurkishTokenizer
tokenizer = TurkishTokenizer()

# After (Rust)
import turkish_tokenizer_rs
tokenizer = turkish_tokenizer_rs.TurkishTokenizer()

# Same API
tokens = tokenizer.encode("merhaba dünya")
```

### API Compatibility

| Method                | Python | Rust | Notes                   |
| --------------------- | ------ | ---- | ----------------------- |
| `encode(text)`        | ✅     | ✅   | Identical               |
| `tokenize(text)`      | ✅     | ✅   | Identical               |
| `tokenize_text(text)` | ✅     | ✅   | Returns detailed tokens |
| `get_vocab()`         | ✅     | ✅   | Identical               |
| `vocab_size()`        | ✅     | ✅   | Identical               |
| `pad_token_id`        | ✅     | ✅   | Property access         |
| `eos_token_id`        | ✅     | ✅   | Property access         |
| `__call__(text)`      | ✅     | ✅   | ML framework compat     |

## 🛠 Development

### Building from Source

```bash
# Clone the repository
git clone https://github.com/turkish-nlp/turkish-tokenizer
cd turkish-tokenizer

# Build Rust library
cargo build --release

# Build Python wheel
maturin build --release

# Install for development
maturin develop
```

### Testing

```bash
# Test Rust implementation
cargo test

# Test Python integration
python examples/python_usage.py

# Run performance comparison
python examples/performance_comparison.py
```

### Cross-Platform Builds

```bash
# Build for multiple Python versions
maturin build --release --interpreter python3.8 python3.9 python3.10 python3.11 python3.12

# Build for different architectures
maturin build --release --target x86_64-unknown-linux-gnu
maturin build --release --target aarch64-apple-darwin
```

## 📦 Distribution

### Publishing to PyPI

```bash
# Build wheels for multiple platforms
maturin build --release --universal2

# Publish to PyPI
maturin publish --username __token__ --password your_pypi_token
```

### Local Installation

```bash
# Install from wheel
pip install target/wheels/turkish_tokenizer_rs-*.whl

# Or install in editable mode
maturin develop
```

## 🐛 Troubleshooting

### Common Issues

1. **Import Error**: Make sure maturin is installed and the wheel is built

   ```bash
   pip install maturin
   maturin develop
   ```

2. **Rust Not Found**: Install Rust toolchain

   ```bash
   curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
   ```

3. **Build Errors**: Update dependencies
   ```bash
   cargo update
   pip install --upgrade maturin
   ```

### Performance Notes

- The Rust implementation uses embedded JSON data for zero I/O overhead
- All string operations are optimized for Turkish character handling
- Memory usage is minimized with efficient data structures
- Compilation in release mode (`--release`) is crucial for performance

## 🤝 Contributing

1. Make changes to the Rust code in `src/lib.rs`
2. Update Python bindings if needed
3. Test both Rust and Python functionality
4. Update documentation

### Running Tests

```bash
# Rust tests
cargo test

# Python integration tests
python examples/python_usage.py
python examples/performance_comparison.py
```

## 📄 License

MIT License - see LICENSE file for details.
