# Packaging Guide for Turkish Tokenizer

This guide will help you package and publish the Turkish Tokenizer to PyPI.

## Prerequisites

Before you start, make sure you have the following tools installed:

1. **Python 3.8+** - The main programming language
2. **pip** - Python package installer
3. **setuptools** - For building packages
4. **wheel** - For creating wheel distributions
5. **twine** - For uploading to PyPI

Install the required tools:

```bash
pip install setuptools wheel twine
```

## Package Structure

The package has been configured with the following files:

- `pyproject.toml` - Modern Python packaging configuration
- `setup.py` - Traditional setup script (alternative)
- `MANIFEST.in` - Specifies which files to include in the package
- `LICENSE` - MIT license
- `CHANGELOG.md` - Version history
- `.gitignore` - Git ignore rules
- `build_package.py` - Automated build script
- `test_tokenizer.py` - Test script

## Quick Start

### 1. Test the Package Locally

First, test that everything works:

```bash
# Run the test script
python test_tokenizer.py

# Or use the automated build script
python build_package.py
```

### 2. Build the Package

```bash
# Clean previous builds
rm -rf build/ dist/ *.egg-info/

# Build source and wheel distributions
python setup.py sdist bdist_wheel

# Or use the automated script
python build_package.py
```

### 3. Check the Package

```bash
# Check the package with twine
python -m twine check dist/*
```

### 4. Test Installation Locally

```bash
# Install the package locally
pip install dist/turkish_tokenizer-0.1.0.tar.gz

# Test the installation
python -c "from turkish_tokenizer import tokenize; print(tokenize('merhaba'))"
```

## Publishing to PyPI

### 1. Create PyPI Account

1. Go to [PyPI](https://pypi.org/account/register/)
2. Create an account
3. Enable two-factor authentication (recommended)

### 2. Test on TestPyPI First

It's recommended to test on TestPyPI before publishing to the main PyPI:

```bash
# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ turkish-tokenizer
```

### 3. Publish to PyPI

Once you're satisfied with the TestPyPI version:

```bash
# Upload to PyPI
twine upload dist/*
```

## Package Configuration

### Key Features

- **Package Name**: `turkish-tokenizer`
- **Version**: `0.1.0` (defined in `version.py`)
- **Python Support**: 3.8+
- **License**: MIT
- **Entry Point**: `turkish-tokenizer` command-line tool

### Included Files

The package includes:

- All Python source files
- JSON dictionary files (`*.json`)
- Rust source files (for reference)
- Documentation files

### Dependencies

Currently, the package has no external dependencies, making it lightweight and easy to install.

## Version Management

To update the package version:

1. Update `version.py`:

   ```python
   __version__ = "0.1.1"
   ```

2. Update `CHANGELOG.md` with the new version

3. Rebuild and publish:
   ```bash
   python build_package.py
   twine upload dist/*
   ```

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure all required files are included in `MANIFEST.in`
2. **Missing Dependencies**: Check that all imports are available
3. **Build Failures**: Clean previous builds with `rm -rf build/ dist/ *.egg-info/`

### Testing

Always test your package before publishing:

```bash
# Test locally
python test_tokenizer.py

# Test installation
pip install dist/turkish_tokenizer-0.1.0.tar.gz
python -c "import turkish_tokenizer; print('Success!')"
```

## Best Practices

1. **Always test on TestPyPI first**
2. **Keep version numbers consistent** across all files
3. **Update CHANGELOG.md** for each release
4. **Use semantic versioning** (MAJOR.MINOR.PATCH)
5. **Test the package** after installation

## Next Steps

After successful publication:

1. Update your GitHub repository with the new release
2. Create a GitHub release with the same version tag
3. Update documentation if needed
4. Monitor for any issues or feedback

## Support

If you encounter issues:

1. Check the [Python Packaging User Guide](https://packaging.python.org/)
2. Review PyPI's [uploading documentation](https://pypi.org/help/#uploading)
3. Check the package's GitHub issues page

---

**Note**: Remember to update the email addresses and GitHub URLs in `pyproject.toml` and `setup.py` before publishing!
