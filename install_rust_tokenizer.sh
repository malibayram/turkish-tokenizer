#!/bin/bash
# Installation script for Turkish Tokenizer Rust implementation

set -e

echo "🦀 Turkish Tokenizer - Rust Installation Script"
echo "=============================================="

# Check if Rust is installed
if ! command -v cargo &> /dev/null; then
    echo "❌ Rust is not installed. Installing Rust..."
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    source ~/.cargo/env
    echo "✅ Rust installed successfully!"
else
    echo "✅ Rust is already installed"
fi

# Check if maturin is installed
if ! command -v maturin &> /dev/null; then
    echo "📦 Installing maturin..."
    pip install maturin
    echo "✅ Maturin installed successfully!"
else
    echo "✅ Maturin is already installed"
fi

# Build and install the tokenizer
echo "🔨 Building Turkish tokenizer..."
maturin build --release

echo "📥 Installing Python package..."
pip install target/wheels/turkish_tokenizer_rs-*.whl --force-reinstall

# Test the installation
echo "🧪 Testing installation..."
python -c "
import turkish_tokenizer_rs
tokenizer = turkish_tokenizer_rs.TurkishTokenizer()
result = tokenizer.encode('merhaba dünya')
print(f'✅ Test successful! Token IDs: {result}')
print(f'📊 Vocabulary size: {tokenizer.vocab_size():,}')
"

echo ""
echo "🎉 Installation completed successfully!"
echo ""
echo "Usage:"
echo "  python -c \"import turkish_tokenizer_rs; tokenizer = turkish_tokenizer_rs.TurkishTokenizer(); print(tokenizer.encode('merhaba dünya'))\""
echo ""
echo "Examples:"
echo "  python examples/python_usage.py"
echo "  python examples/performance_comparison.py"
