"""
Command-line interface for the Turkish tokenizer.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Optional

from .core import decode_text
from .tokenizer import TurkishTokenizer
from .wrapper import build_tokenizer, is_tokenizer_available


def main(args: Optional[List[str]] = None) -> int:
    """
    Main CLI function.
    
    Args:
        args: Command line arguments (defaults to sys.argv[1:])
        
    Returns:
        Exit code (0 for success, 1 for error)
    """
    parser = argparse.ArgumentParser(
        description="High-performance Turkish tokenizer with Rust backend",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Tokenize text from command line
  turkish-tokenizer "Merhaba dünya!"
  
  # Tokenize text from file
  turkish-tokenizer -f input.txt
  
  # Save output to file
  turkish-tokenizer "Merhaba dünya!" -o output.json
  
  # Build Rust tokenizer
  turkish-tokenizer --build
  
  # Check if Rust tokenizer is available
  turkish-tokenizer --check
        """
    )
    
    parser.add_argument(
        "text",
        nargs="?",
        help="Text to tokenize"
    )
    
    parser.add_argument(
        "-f", "--file",
        help="Read text from file instead of command line argument"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="Output file for results (default: stdout)"
    )
    
    parser.add_argument(
        "--format",
        choices=["json", "text"],
        default="json",
        help="Output format (default: json)"
    )
    
    parser.add_argument(
        "--build",
        action="store_true",
        help="Build the Rust tokenizer binary"
    )
    
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check if Rust tokenizer is available"
    )
    
    parser.add_argument(
        "--decode",
        help="Decode token IDs back to text (comma-separated list)"
    )
    
    parsed_args = parser.parse_args(args)
    
    # Handle special commands
    if parsed_args.build:
        print("Building Rust tokenizer...")
        if build_tokenizer():
            return 0
        else:
            return 1
    
    if parsed_args.check:
        if is_tokenizer_available():
            print("✅ Rust tokenizer is available")
            return 0
        else:
            print("❌ Rust tokenizer is not available")
            print("Run 'turkish-tokenizer --build' to build it")
            return 1
    
    if parsed_args.decode:
        try:
            token_ids = [int(x.strip()) for x in parsed_args.decode.split(",")]
            tokenizer = TurkishTokenizer()
            result = tokenizer.decode(token_ids)
            
            if parsed_args.output:
                with open(parsed_args.output, 'w', encoding='utf-8') as f:
                    f.write(result)
            else:
                print(result)
            return 0
        except Exception as e:
            print(f"Error decoding tokens: {e}", file=sys.stderr)
            return 1
    
    # Get input text
    text = None
    if parsed_args.text:
        text = parsed_args.text
    elif parsed_args.file:
        try:
            with open(parsed_args.file, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            return 1
    else:
        parser.print_help()
        return 1
    
    if not text:
        print("No text provided", file=sys.stderr)
        return 1
    
    # Tokenize
    try:
        tokenizer = TurkishTokenizer()
        tokens, ids = tokenizer.tokenize(text)
        
        # Prepare output
        if parsed_args.format == "json":
            output = {
                "text": text,
                "tokens": tokens,
                "token_ids": ids,
                "token_count": len(tokens)
            }
            result = json.dumps(output, ensure_ascii=False, indent=2)
        else:
            result = f"Tokens: {tokens}\nIDs: {ids}\nCount: {len(tokens)}"
        
        # Write output
        if parsed_args.output:
            with open(parsed_args.output, 'w', encoding='utf-8') as f:
                f.write(result)
        else:
            print(result)
        
        return 0
        
    except Exception as e:
        print(f"Error tokenizing text: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main()) 