"""
Wrapper module for the Rust tokenizer binary.

This module provides a Python interface to the high-performance Rust tokenizer.
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Union

from .core import tokenize as rust_tokenize
from .tokenizer import TurkishTokenizer


def tokenize_text(text: str, tokenizer_path: str = "./target/release/turkish_tokenizer") -> Tuple[List[str], List[int]]:
    """
    Tokenize text using the Turkish tokenizer binary.
    
    Args:
        text: The text to tokenize
        tokenizer_path: Path to the tokenizer binary (relative to turkish_tokenizer directory)
        
    Returns:
        Tuple containing:
            - List of token strings
            - List of token IDs (integers)
            
    Raises:
        FileNotFoundError: If the tokenizer binary is not found
        subprocess.CalledProcessError: If the tokenizer fails to run
        json.JSONDecodeError: If the tokenizer output is not valid JSON
    """
    
    # Get the absolute path to the turkish_tokenizer directory
    script_dir = Path(__file__).parent
    tokenizer_dir = script_dir / "turkish_tokenizer"
    full_tokenizer_path = tokenizer_dir / tokenizer_path
    
    # Check if tokenizer binary exists
    if not full_tokenizer_path.exists():
        raise FileNotFoundError(f"Tokenizer binary not found at: {full_tokenizer_path}")
    
    try:
        # Change to the turkish_tokenizer directory before running the binary
        # This ensures the binary can find its required JSON files
        original_cwd = os.getcwd()
        os.chdir(tokenizer_dir)
        
        # Run the tokenizer with the input text
        result = subprocess.run(
            [tokenizer_path, text],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Restore original working directory
        os.chdir(original_cwd)
        
        # Parse the JSON output
        output = json.loads(result.stdout.strip())
        
        # Validate the output structure
        if not isinstance(output, dict) or 'tokens' not in output or 'ids' not in output:
            raise ValueError("Invalid output format from tokenizer")
        
        return output['tokens'], output['ids']
        
    except subprocess.CalledProcessError as e:
        # Restore original working directory in case of error
        os.chdir(original_cwd)
        raise subprocess.CalledProcessError(
            e.returncode, 
            e.cmd, 
            output=e.stdout, 
            stderr=e.stderr
        )
    except json.JSONDecodeError as e:
        # Restore original working directory in case of error
        os.chdir(original_cwd)
        raise json.JSONDecodeError(f"Failed to parse tokenizer output: {e}", e.doc, e.pos)
    except Exception as e:
        # Restore original working directory in case of error
        os.chdir(original_cwd)
        raise e


def build_tokenizer() -> bool:
    """
    Build the Rust tokenizer binary.
    
    Returns:
        True if build was successful, False otherwise
    """
    try:
        script_dir = Path(__file__).parent
        tokenizer_dir = script_dir / "turkish_tokenizer"
        
        if not tokenizer_dir.exists():
            print(f"Error: Turkish tokenizer directory not found at {tokenizer_dir}")
            return False
        
        # Change to the tokenizer directory and build
        original_cwd = os.getcwd()
        os.chdir(tokenizer_dir)
        
        print("Building Turkish tokenizer...")
        result = subprocess.run(
            ["cargo", "build", "--release"],
            capture_output=True,
            text=True,
            check=True
        )
        
        os.chdir(original_cwd)
        print("✅ Turkish tokenizer built successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        os.chdir(original_cwd)
        print(f"❌ Failed to build tokenizer: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        return False
    except Exception as e:
        os.chdir(original_cwd)
        print(f"❌ Unexpected error during build: {e}")
        return False


def is_tokenizer_available() -> bool:
    """
    Check if the Rust tokenizer binary is available.
    
    Returns:
        True if the tokenizer binary exists and is executable
    """
    script_dir = Path(__file__).parent
    tokenizer_path = script_dir / "turkish_tokenizer" / "target" / "release" / "turkish_tokenizer"
    return tokenizer_path.exists() and os.access(tokenizer_path, os.X_OK) 