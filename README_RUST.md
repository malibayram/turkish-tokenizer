# Turkish Tokenizer - Rust Implementation

A high-performance Rust implementation of the Turkish language tokenizer for morphologically rich text processing.

## Features

- **Fast Encoding**: Efficient tokenization of Turkish text into token IDs
- **Morphological Awareness**: Handles Turkish roots, suffixes, and BPE tokens
- **CamelCase Support**: Properly handles mixed-case text
- **Zero-Copy Design**: Optimized for performance with minimal allocations
- **Embedded Vocabulary**: All vocabulary data embedded in the binary

## Installation

Add this to your `Cargo.toml`:

```toml
[dependencies]
turkish-tokenizer = "0.1.0"
```

## Usage

### Basic Usage

```rust
use turkish_tokenizer::TurkishTokenizer;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Initialize the tokenizer
    let tokenizer = TurkishTokenizer::new()?;

    // Encode text to token IDs
    let text = "merhaba dünya";
    let token_ids = tokenizer.encode(text);
    println!("Token IDs: {:?}", token_ids);

    // Get string tokens
    let tokens = tokenizer.tokenize(text);
    println!("Tokens: {:?}", tokens);

    Ok(())
}
```

### Advanced Usage

```rust
use turkish_tokenizer::{TurkishTokenizer, TokenType};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let tokenizer = TurkishTokenizer::new()?;

    // Get detailed token information
    let tokens = tokenizer.tokenize_text("kitaplarımı");
    for token in tokens {
        println!("Token: '{}', ID: {}, Type: {:?}",
                 token.token, token.id, token.token_type);
    }

    // Access vocabulary
    let vocab = tokenizer.get_vocab();
    println!("Vocabulary size: {}", vocab.len());

    // Special tokens
    println!("Pad token ID: {}", tokenizer.pad_token_id);
    println!("EOS token ID: {}", tokenizer.eos_token_id);

    Ok(())
}
```

## Performance

The Rust implementation is optimized for performance:

- **Zero-copy string operations** where possible
- **Embedded vocabulary** eliminates file I/O overhead
- **Efficient prefix matching** with length-bounded searches
- **Memory-efficient data structures**

Run benchmarks:

```bash
cargo bench
```

## API Reference

### `TurkishTokenizer`

The main tokenizer struct.

#### Methods

- `new() -> Result<Self, Box<dyn std::error::Error>>`: Create a new tokenizer instance
- `encode(&self, text: &str) -> Vec<u32>`: Encode text into token IDs
- `tokenize(&self, text: &str) -> Vec<String>`: Tokenize text into string tokens
- `tokenize_text(&self, text: &str) -> Vec<Token>`: Get detailed token information
- `get_vocab(&self) -> &HashMap<String, u32>`: Access the vocabulary
- `vocab_size(&self) -> usize`: Get vocabulary size
- `convert_tokens_to_ids(&self, tokens: &[String]) -> Vec<u32>`: Convert tokens to IDs

#### Fields

- `pad_token: String`: Padding token
- `eos_token: String`: End-of-sequence token
- `pad_token_id: u32`: Padding token ID
- `eos_token_id: u32`: End-of-sequence token ID

### `Token`

Represents a tokenized segment with metadata.

#### Fields

- `token: String`: The token text
- `id: u32`: The token ID
- `token_type: TokenType`: The type of token (Root, Suffix, or Bpe)

### `TokenType`

Enum representing different token types:

- `Root`: Turkish word roots
- `Suffix`: Turkish morphological suffixes
- `Bpe`: Byte-pair encoding tokens

## Examples

### Turkish Morphology

```rust
let tokenizer = TurkishTokenizer::new()?;

// Complex Turkish word with suffixes
let tokens = tokenizer.tokenize("kitaplarımı");
// Output: ["kitap", "lar", "ım", "ı"]
// Meaning: "my books" (accusative)
```

### CamelCase Handling

```rust
let tokenizer = TurkishTokenizer::new()?;

// Mixed case text
let tokens = tokenizer.tokenize("merhabaDünya");
// Output: ["merhaba", "<uppercase>", "dünya"]
```

### Special Tokens

```rust
let tokenizer = TurkishTokenizer::new()?;

// Unknown characters get special handling
let tokens = tokenizer.tokenize("hello@world");
// Contains "<unknown>" tokens for unsupported characters
```

## Building

```bash
# Build the library
cargo build --release

# Run tests
cargo test

# Run benchmarks
cargo bench

# Run example
cargo run
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
