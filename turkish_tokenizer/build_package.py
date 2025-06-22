#!/usr/bin/env python3
"""
Build script for Turkish Tokenizer package.
This script helps you build and test the package before publishing.
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Command: {cmd}")
        print(f"   Error: {e.stderr}")
        return False

def check_prerequisites():
    """Check if required tools are available."""
    print("🔍 Checking prerequisites...")
    
    tools = [
        ("python", "Python interpreter"),
        ("pip", "Python package installer"),
        ("twine", "PyPI upload tool"),
    ]
    
    missing = []
    for tool, description in tools:
        if not run_command(f"which {tool}", f"Checking {description}"):
            missing.append(tool)
    
    if missing:
        print(f"❌ Missing required tools: {', '.join(missing)}")
        print("Please install them before proceeding.")
        return False
    
    return True

def clean_build():
    """Clean previous build artifacts."""
    print("🧹 Cleaning build artifacts...")
    
    dirs_to_clean = ["build", "dist", "*.egg-info"]
    for dir_pattern in dirs_to_clean:
        if "*" in dir_pattern:
            # Handle glob patterns
            for path in Path(".").glob(dir_pattern):
                if path.is_dir():
                    run_command(f"rm -rf {path}", f"Removing {path}")
        else:
            run_command(f"rm -rf {dir_pattern}", f"Removing {dir_pattern}")
    
    return True

def build_package():
    """Build the package."""
    print("📦 Building package...")
    
    # Build using setuptools
    if not run_command("python setup.py sdist bdist_wheel", "Building source and wheel distributions"):
        return False
    
    return True

def test_package():
    """Test the built package."""
    print("🧪 Testing built package...")
    
    # Run the test script
    if not run_command("python test_tokenizer.py", "Running tokenizer tests"):
        return False
    
    return True

def check_package():
    """Check the built package for issues."""
    print("🔍 Checking package...")
    
    # Check wheel
    if not run_command("python -m twine check dist/*", "Checking package with twine"):
        return False
    
    return True

def main():
    """Main build process."""
    print("🚀 Turkish Tokenizer Package Builder")
    print("=" * 40)
    
    # Check prerequisites
    if not check_prerequisites():
        sys.exit(1)
    
    # Clean previous builds
    if not clean_build():
        sys.exit(1)
    
    # Build package
    if not build_package():
        sys.exit(1)
    
    # Test package
    if not test_package():
        sys.exit(1)
    
    # Check package
    if not check_package():
        sys.exit(1)
    
    print("\n🎉 Package built successfully!")
    print("\n📋 Next steps:")
    print("1. Test the package locally:")
    print("   pip install dist/turkish_tokenizer-0.1.0.tar.gz")
    print("   python -c \"from turkish_tokenizer import tokenize; print(tokenize('merhaba'))\"")
    print("\n2. Upload to PyPI (if ready):")
    print("   twine upload dist/*")
    print("\n3. Upload to TestPyPI (for testing):")
    print("   twine upload --repository testpypi dist/*")

if __name__ == "__main__":
    main() 