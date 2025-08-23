# Development Guide

This document provides information for developers working on the Turkish Tokenizer project.

## Setup

### Prerequisites

- Python 3.8 or higher
- pip
- git

### Installation

1. Clone the repository:

```bash
git clone https://github.com/malibayram/turkish-tokenizer.git
cd turkish-tokenizer
```

2. Install the package in development mode:

```bash
make install-dev
```

This will install the package with all development dependencies.

## Development Workflow

### Available Commands

The project includes a comprehensive Makefile with useful commands:

```bash
# Show all available commands
make help

# Install dependencies
make install-dev

# Run tests
make test

# Run tests with coverage
make test-cov

# Run fast tests (excluding slow tests)
make test-fast

# Format code
make format

# Run linting
make lint

# Run all checks (lint, test, format)
make check

# Clean build artifacts
make clean

# Build the package
make build

# Publish to PyPI
make publish
```

### Version Management

The project includes automatic version management:

```bash
# Show current version
make version-current

# Bump patch version (0.1.11 -> 0.1.12)
make version-bump

# Bump minor version (0.1.11 -> 0.2.0)
make version-minor

# Bump major version (0.1.11 -> 1.0.0)
make version-major

# Set specific version
make version-set VERSION=1.0.0
```

### Git Hooks

The project includes a pre-commit hook that automatically:

- Increments the patch version
- Updates all version files (pyproject.toml, setup.py, **init**.py)
- Stages the updated files for commit

The hook runs automatically on every commit.

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=turkish_tokenizer --cov-report=html

# Run specific test file
pytest tests/test_turkish_tokenizer.py

# Run specific test class
pytest tests/test_turkish_tokenizer.py::TestTurkishTokenizer

# Run specific test method
pytest tests/test_turkish_tokenizer.py::TestTurkishTokenizer::test_tokenizer_initialization
```

### Test Structure

The test suite is organized as follows:

- `tests/test_turkish_tokenizer.py`: Tests for the main TurkishTokenizer class
- `tests/test_turkish_decoder.py`: Tests for the TurkishDecoder class
- `tests/check_intersections.py`: Script to check for token dictionary overlaps
- `tests/check_root_suffix_combinations.py`: Script to check for morphological integrity violations

Test classes include:

- **Unit Tests**: Basic functionality tests
- **Edge Cases**: Tests for unusual inputs and edge conditions
- **Performance Tests**: Tests to ensure reasonable performance
- **Morphological Integrity Tests**: Tests to ensure BPE dictionary doesn't contain root+suffix combinations

### Morphological Integrity

The Turkish tokenizer maintains morphological awareness by properly separating roots and suffixes. A critical test ensures that no root+suffix combinations exist in the BPE dictionary:

```bash
# Run the morphological integrity test
pytest tests/test_turkish_tokenizer.py::TestTurkishTokenizer::test_no_root_suffix_combinations_in_bpe_dictionary

# Comprehensive analysis of morphological violations
python tests/check_root_suffix_combinations.py --full-check
```

For detailed information about morphological integrity principles, see [MORPHOLOGICAL_INTEGRITY.md](MORPHOLOGICAL_INTEGRITY.md).

### Test Coverage

Current test coverage:

- **TurkishTokenizer**: 96% coverage
- **TurkishDecoder**: 51% coverage
- **Overall**: 70% coverage

To improve coverage, focus on the missing lines in the TurkishDecoder class.

## Code Quality

### Linting

The project uses several linting tools:

```bash
# Run all linting checks
make lint

# Run individual tools
flake8 turkish_tokenizer/ tests/ scripts/
mypy turkish_tokenizer/ scripts/
```

### Code Formatting

The project uses Black for code formatting:

```bash
# Format code
make format

# Check formatting without making changes
black --check turkish_tokenizer/ tests/ scripts/
```

## Building and Publishing

### Building

```bash
# Build the package
make build

# Clean build artifacts
make clean
```

### Publishing

```bash
# Build and publish to PyPI
make publish
```

**Note**: Publishing requires PyPI credentials to be configured in `.pypirc`.

## Project Structure

```
turkish-tokenizer/
├── turkish_tokenizer/          # Main package
│   ├── __init__.py
│   ├── turkish_tokenizer.py    # Main tokenizer implementation
│   ├── turkish_decoder.py      # Decoder implementation
│   ├── kokler.json            # Root words dictionary
│   ├── ekler.json             # Suffixes dictionary
│   └── bpe_tokenler.json      # BPE tokens dictionary
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── test_turkish_tokenizer.py
│   └── test_turkish_decoder.py
├── scripts/                    # Development scripts
│   └── version_manager.py
├── .git/hooks/                 # Git hooks
│   └── pre-commit
├── Makefile                    # Development commands
├── pyproject.toml             # Project configuration
├── setup.py                   # Package setup
├── pytest.ini                # Pytest configuration
└── README.md                  # Project documentation
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Add tests for new functionality
5. Run the test suite: `make test`
6. Run linting: `make lint`
7. Format code: `make format`
8. Commit your changes (version will be auto-incremented)
9. Push to your fork
10. Create a pull request

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure you've installed the package in development mode with `make install-dev`

2. **Test failures**: Check that all dependencies are installed and the package is properly set up

3. **Version conflicts**: Use `make clean` to remove build artifacts and rebuild

4. **Git hook not working**: Ensure the pre-commit hook is executable: `chmod +x .git/hooks/pre-commit`

### Getting Help

If you encounter issues:

1. Check the test output for error messages
2. Run `make clean` and try again
3. Check that your Python version is 3.8 or higher
4. Ensure all dependencies are installed

## License

This project is licensed under the MIT License - see the LICENSE file for details.
