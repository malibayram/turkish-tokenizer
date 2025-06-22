#!/usr/bin/env python3
"""
Turkish Tokenizer Wrapper

This script provides a Python interface to the Turkish tokenizer binary.
It takes text input and returns a dictionary containing tokens and their IDs.
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Union


def tokenize_text(text: str, tokenizer_path: str = "./target/release/turkish_tokenizer") -> Dict[str, Union[List[str], List[int]]]:
    """
    Tokenize text using the Turkish tokenizer binary.
    
    Args:
        text (str): The text to tokenize
        tokenizer_path (str): Path to the tokenizer binary (relative to turkish_tokenizer directory)
        
    Returns:
        Dict containing:
            - 'tokens': List of token strings
            - 'ids': List of token IDs (integers)
            
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


def main():
    """Main function for command line usage."""
    if len(sys.argv) < 2:
        print("Usage: python turkish_tokenizer_wrapper.py <text>")
        print("Example: python turkish_tokenizer_wrapper.py 'merhaba dünya'")
        sys.exit(1)
    
    text = sys.argv[1]
    
    try:
        result = tokenize_text(text)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main() 