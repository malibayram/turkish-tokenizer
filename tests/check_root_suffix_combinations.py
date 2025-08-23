#!/usr/bin/env python3
"""
Comprehensive script to check for root+suffix combinations in the BPE dictionary.

This script addresses the morphological integrity issue where the BPE dictionary
contains tokens that should be decomposed into their morphological components
(root + suffix) instead of being treated as single tokens.

Usage:
    python tests/check_root_suffix_combinations.py
    
    Options:
    --full-check: Check all combinations (may take longer)
    --export-csv: Export results to CSV file
    --show-examples: Show example combinations found
"""

import argparse
import csv
import os
import sys
from typing import Dict, List, Tuple

from turkish_tokenizer import TurkishTokenizer


def get_problematic_combinations(
    tokenizer: TurkishTokenizer,
    full_check: bool = False,
    max_roots: int = 1000,
    max_suffixes: int = 200
) -> List[Dict]:
    """
    Find all root+suffix combinations that exist in the BPE dictionary.
    
    Args:
        tokenizer: TurkishTokenizer instance
        full_check: If True, check all combinations (can be slow)
        max_roots: Maximum number of roots to check if not full_check
        max_suffixes: Maximum number of suffixes to check if not full_check
        
    Returns:
        List of dictionaries containing problematic combinations
    """
    kokler = tokenizer.roots
    ekler = tokenizer.suffixes
    bpe_tokenler = tokenizer.bpe_tokens
    
    # Filter out special tokens from roots
    special_tokens = ["<uppercase>", "<unknown>", " ", "\n", "\t", "<pad>", "<eos>"]
    root_tokens = {k: v for k, v in kokler.items() 
                  if not k.startswith("special_") and k not in special_tokens}
    
    # Determine which roots and suffixes to check
    if full_check:
        roots_to_check = list(root_tokens.keys())
        suffixes_to_check = list(ekler.keys())
    else:
        roots_to_check = list(root_tokens.keys())[:max_roots]
        suffixes_to_check = list(ekler.keys())[:max_suffixes]
    
    print(f"Checking {len(roots_to_check)} roots × {len(suffixes_to_check)} suffixes...")
    
    found_combinations = []
    total_combinations = len(roots_to_check) * len(suffixes_to_check)
    
    for i, root in enumerate(roots_to_check):
        if i % 100 == 0:
            print(f"Progress: {i}/{len(roots_to_check)} roots checked...")
            
        for suffix in suffixes_to_check:
            combination = root + suffix
            if combination in bpe_tokenler:
                found_combinations.append({
                    'root': root,
                    'suffix': suffix,
                    'combination': combination,
                    'root_id': root_tokens[root],
                    'suffix_id': ekler[suffix],
                    'bpe_id': bpe_tokenler[combination]
                })
    
    return found_combinations


def print_summary(combinations: List[Dict], total_checked: int) -> None:
    """Print a summary of the findings."""
    print("\n" + "=" * 80)
    print("ROOT+SUFFIX COMBINATIONS IN BPE DICTIONARY - ANALYSIS SUMMARY")
    print("=" * 80)
    
    print(f"Total combinations checked: {total_checked:,}")
    print(f"Problematic combinations found: {len(combinations):,}")
    
    if combinations:
        print(f"Percentage of problematic combinations: {len(combinations)/total_checked*100:.2f}%")
        
        # Analyze by suffix frequency
        suffix_counts = {}
        for combo in combinations:
            suffix = combo['suffix']
            suffix_counts[suffix] = suffix_counts.get(suffix, 0) + 1
        
        print(f"\nMost problematic suffixes:")
        sorted_suffixes = sorted(suffix_counts.items(), key=lambda x: x[1], reverse=True)
        for suffix, count in sorted_suffixes[:10]:
            print(f"  '{suffix}': {count} combinations")
        
        # Analyze by root frequency  
        root_counts = {}
        for combo in combinations:
            root = combo['root']
            root_counts[root] = root_counts.get(root, 0) + 1
        
        print(f"\nMost problematic roots:")
        sorted_roots = sorted(root_counts.items(), key=lambda x: x[1], reverse=True)
        for root, count in sorted_roots[:10]:
            print(f"  '{root}': {count} combinations")
    
    print("=" * 80)


def show_examples(combinations: List[Dict], count: int = 20) -> None:
    """Show example combinations."""
    if not combinations:
        print("✅ No problematic combinations found!")
        return
        
    print(f"\n❌ Examples of problematic combinations (showing {min(count, len(combinations))}):")
    for i, combo in enumerate(combinations[:count]):
        print(f"{i+1:2d}. '{combo['root']}' + '{combo['suffix']}' = '{combo['combination']}'")
        print(f"     Root ID: {combo['root_id']}, Suffix ID: {combo['suffix_id']}, BPE ID: {combo['bpe_id']}")


def export_to_csv(combinations: List[Dict], filename: str) -> None:
    """Export combinations to CSV file."""
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['root', 'suffix', 'combination', 'root_id', 'suffix_id', 'bpe_id']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for combo in combinations:
            writer.writerow(combo)
    
    print(f"Results exported to: {filename}")


def main():
    parser = argparse.ArgumentParser(description='Check for root+suffix combinations in BPE dictionary')
    parser.add_argument('--full-check', action='store_true', 
                       help='Check all combinations (may take longer)')
    parser.add_argument('--export-csv', type=str, metavar='FILENAME',
                       help='Export results to CSV file')
    parser.add_argument('--show-examples', type=int, default=20, metavar='COUNT',
                       help='Number of examples to show (default: 20)')
    parser.add_argument('--max-roots', type=int, default=1000,
                       help='Maximum number of roots to check (ignored with --full-check)')
    parser.add_argument('--max-suffixes', type=int, default=200,
                       help='Maximum number of suffixes to check (ignored with --full-check)')
    
    args = parser.parse_args()
    
    # Initialize tokenizer
    try:
        tokenizer = TurkishTokenizer()
    except Exception as e:
        print(f"Error initializing tokenizer: {e}")
        return 1
    
    # Find problematic combinations
    combinations = get_problematic_combinations(
        tokenizer,
        full_check=args.full_check,
        max_roots=args.max_roots,
        max_suffixes=args.max_suffixes
    )
    
    # Calculate total combinations checked
    kokler = tokenizer.roots
    ekler = tokenizer.suffixes
    special_tokens = ["<uppercase>", "<unknown>", " ", "\n", "\t", "<pad>", "<eos>"]
    root_tokens = {k: v for k, v in kokler.items() 
                  if not k.startswith("special_") and k not in special_tokens}
    
    if args.full_check:
        total_checked = len(root_tokens) * len(ekler)
    else:
        total_checked = min(args.max_roots, len(root_tokens)) * min(args.max_suffixes, len(ekler))
    
    # Print summary
    print_summary(combinations, total_checked)
    
    # Show examples
    if args.show_examples > 0:
        show_examples(combinations, args.show_examples)
    
    # Export to CSV if requested
    if args.export_csv:
        export_to_csv(combinations, args.export_csv)
    
    # Return exit code based on findings
    return 1 if combinations else 0


if __name__ == "__main__":
    exit(main())