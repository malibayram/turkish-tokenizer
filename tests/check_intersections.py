#!/usr/bin/env python3
"""
Script to check for intersections between token dictionaries.
This is similar to the demo notebook code but as a standalone script.
Can be run independently to verify token dictionary integrity.
"""

from turkish_tokenizer import TurkishTokenizer


def main():
    tokenizer = TurkishTokenizer()
    
    kokler = tokenizer.roots
    ekler = tokenizer.suffixes
    bpe_tokenler = tokenizer.bpe_tokens
    
    print("Checking for intersections between token dictionaries...")
    print("=" * 60)
    
    # Check kokler vs ekler
    print("\nChecking kokler vs ekler:")
    kokler_ekler_intersection = set(kokler.keys()) & set(ekler.keys())
    if kokler_ekler_intersection:
        print(f"❌ Found {len(kokler_ekler_intersection)} overlapping keys:")
        for k in sorted(kokler_ekler_intersection):
            print(f"   - '{k}' (kokler: {kokler[k]}, ekler: {ekler[k]})")
    else:
        print("✅ No overlapping keys between kokler and ekler")
    
    # Check kokler vs bpe_tokenler
    print("\nChecking kokler vs bpe_tokenler:")
    kokler_bpe_intersection = set(kokler.keys()) & set(bpe_tokenler.keys())
    if kokler_bpe_intersection:
        print(f"❌ Found {len(kokler_bpe_intersection)} overlapping keys:")
        for k in sorted(kokler_bpe_intersection):
            print(f"   - '{k}' (kokler: {kokler[k]}, bpe: {bpe_tokenler[k]})")
    else:
        print("✅ No overlapping keys between kokler and bpe_tokenler")
    
    # Check ekler vs bpe_tokenler
    print("\nChecking ekler vs bpe_tokenler:")
    ekler_bpe_intersection = set(ekler.keys()) & set(bpe_tokenler.keys())
    if ekler_bpe_intersection:
        print(f"❌ Found {len(ekler_bpe_intersection)} overlapping keys:")
        for k in sorted(ekler_bpe_intersection):
            print(f"   - '{k}' (ekler: {ekler[k]}, bpe: {bpe_tokenler[k]})")
    else:
        print("✅ No overlapping keys between ekler and bpe_tokenler")
    
    # Summary
    print("\n" + "=" * 60)
    total_intersections = len(kokler_ekler_intersection) + len(kokler_bpe_intersection) + len(ekler_bpe_intersection)
    if total_intersections == 0:
        print("🎉 All token dictionaries are properly separated!")
        return 0
    else:
        print(f"⚠️  Found {total_intersections} total overlapping keys across all dictionaries")
        return 1

if __name__ == "__main__":
    exit(main())
