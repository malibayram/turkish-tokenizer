#!/usr/bin/env python3
"""
Build script for the Turkish Tokenizer package.

This script helps with building, testing, and publishing the package.
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(command, description, check=True):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stdout:
            print(f"stdout: {e.stdout}")
        if e.stderr:
            print(f"stderr: {e.stderr}")
        return False


def clean_build():
    """Clean build artifacts."""
    print("🧹 Cleaning build artifacts...")
    dirs_to_clean = ["build", "dist", "*.egg-info"]
    for pattern in dirs_to_clean:
        run_command(f"rm -rf {pattern}", f"Removing {pattern}", check=False)
    print("✅ Clean complete")


def install_dependencies():
    """Install development dependencies."""
    print("📦 Installing development dependencies...")
    if not run_command("pip install -e '.[dev]'", "Installing package in development mode"):
        return False
    return True


def run_tests():
    """Run the test suite."""
    print("🧪 Running tests...")
    if not run_command("pytest tests/ -v", "Running pytest"):
        return False
    return True


def run_linting():
    """Run code linting and formatting checks."""
    print("🔍 Running linting checks...")
    
    # Format code
    if not run_command("black --check turkish_tokenizer/ tests/", "Checking code formatting"):
        print("💡 Run 'black turkish_tokenizer/ tests/' to format code")
        return False
    
    # Import sorting
    if not run_command("isort --check-only turkish_tokenizer/ tests/", "Checking import sorting"):
        print("💡 Run 'isort turkish_tokenizer/ tests/' to sort imports")
        return False
    
    # Type checking
    if not run_command("mypy turkish_tokenizer/", "Running type checking"):
        return False
    
    return True


def build_package():
    """Build the package distribution."""
    print("🔨 Building package...")
    
    # Clean first
    clean_build()
    
    # Build source distribution and wheel
    if not run_command("python -m build", "Building package distribution"):
        return False
    
    print("✅ Package built successfully!")
    return True


def check_package():
    """Check the built package."""
    print("🔍 Checking built package...")
    
    # Check source distribution
    if not run_command("twine check dist/*", "Checking package with twine"):
        return False
    
    print("✅ Package check passed!")
    return True


def publish_to_testpypi():
    """Publish to Test PyPI."""
    print("🚀 Publishing to Test PyPI...")
    
    if not run_command("twine upload --repository testpypi dist/*", "Uploading to Test PyPI"):
        return False
    
    print("✅ Published to Test PyPI successfully!")
    print("💡 Install with: pip install --index-url https://test.pypi.org/simple/ turkish-tokenizer")
    return True


def publish_to_pypi():
    """Publish to PyPI."""
    print("🚀 Publishing to PyPI...")
    
    if not run_command("twine upload dist/*", "Uploading to PyPI"):
        return False
    
    print("✅ Published to PyPI successfully!")
    return True


def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python build_package.py <command>")
        print("\nCommands:")
        print("  clean       - Clean build artifacts")
        print("  install     - Install development dependencies")
        print("  test        - Run tests")
        print("  lint        - Run linting checks")
        print("  build       - Build package")
        print("  check       - Check built package")
        print("  testpypi    - Publish to Test PyPI")
        print("  pypi        - Publish to PyPI")
        print("  all         - Run all checks and build")
        print("  publish     - Build, check, and publish to Test PyPI")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "clean":
        clean_build()
    elif command == "install":
        install_dependencies()
    elif command == "test":
        run_tests()
    elif command == "lint":
        run_linting()
    elif command == "build":
        build_package()
    elif command == "check":
        check_package()
    elif command == "testpypi":
        publish_to_testpypi()
    elif command == "pypi":
        publish_to_pypi()
    elif command == "all":
        success = True
        success &= install_dependencies()
        success &= run_linting()
        success &= run_tests()
        success &= build_package()
        success &= check_package()
        if success:
            print("🎉 All checks passed!")
        else:
            print("❌ Some checks failed!")
            sys.exit(1)
    elif command == "publish":
        success = True
        success &= build_package()
        success &= check_package()
        success &= publish_to_testpypi()
        if not success:
            sys.exit(1)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main() 