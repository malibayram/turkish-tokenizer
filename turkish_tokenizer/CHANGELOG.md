# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Initial release of Turkish Morphological Tokenizer
- Python implementation with clean API
- Rust implementation for high performance
- Support for root word and suffix detection
- BPE (Byte Pair Encoding) fallback for unknown tokens
- Special token handling (spaces, newlines, tabs, uppercase)
- Command-line interface
- Batch processing capabilities
- Decoding functionality to convert token IDs back to text

### Features

- Morphological tokenization of Turkish text
- Thread-safe parallel processing (Rust implementation)
- Identical output format in both Python and Rust implementations
- Support for Turkish characters and special characters
- Comprehensive dictionary files (roots, suffixes, BPE tokens)

## [0.1.0] - 2024-01-XX

### Added

- Initial release
- Core tokenization functionality
- Python and Rust implementations
- CLI interface
- Documentation and examples
