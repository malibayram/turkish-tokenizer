import json
import os
from enum import Enum
from typing import Dict, List, Optional, Tuple

from .turkish_decoder import TurkishDecoder


class TokenType(Enum):
    ROOT = "ROOT"
    SUFFIX = "SUFFIX"
    BPE = "BPE"

class TurkishTokenizer:
    def __init__(self):
        # Get the directory where this module is located
        package_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Load JSON files from the package directory
        with open(os.path.join(package_dir, "kokler.json"), "r", encoding="utf-8") as f:
            roots = json.load(f)
        with open(os.path.join(package_dir, "ekler.json"), "r", encoding="utf-8") as f:
            suffixes = json.load(f)
        with open(os.path.join(package_dir, "bpe_tokenler.json"), "r", encoding="utf-8") as f:
            bpe_tokens = json.load(f)
        
        # Store the dictionaries as instance attributes
        self.roots = roots
        self.suffixes = suffixes
        self.bpe_tokens = bpe_tokens
        
        # Now create vocab and reverse dict
        self.vocab = self.get_vocab()
        self.reverse_dict = {}

        for key, value in self.vocab.items():
            if value not in self.reverse_dict:
                self.reverse_dict[value] = []
            self.reverse_dict[value].append(key)

        self.decoder = TurkishDecoder(self.reverse_dict)

        self.vocab_size = len(self.reverse_dict)

        self.max_root_len = max(len(k) for k in roots) if roots else 0
        self.max_suffix_len = max(len(k) for k in suffixes) if suffixes else 0
        self.max_bpe_len = max(len(k) for k in bpe_tokens) if bpe_tokens else 0
        
        self.uppercase_marker = {"token": "<uppercase>", "id": roots["<uppercase>"], "type": TokenType.ROOT}
        self.unknown_marker = {"token": "<unknown>", "id": roots["<unknown>"], "type": TokenType.ROOT}
        self.space_marker = {"token": " ", "id": roots[" "], "type": TokenType.ROOT}

        # added to be compatible with SFTTrainer
        self.pad_token = "<pad>"
        self.eos_token = "<eos>"
        self.pad_token_id = roots[self.pad_token]
        self.eos_token_id = roots[self.eos_token]

    # added to be compatible with SFTTrainer
    def convert_tokens_to_ids(self, tokens: List[str]) -> List[int]:
        return [self.vocab[token] for token in tokens]
    # added to be compatible with SFTTrainer
    def convert_ids_to_tokens(self, ids: List[int]) -> List[str]:
        return [self.reverse_dict[id] for id in ids]
    
    def get_vocab(self) -> Dict[str, int]:
        return {**self.roots, **self.suffixes, **self.bpe_tokens}

    def _tokenize_word(self, word: str) -> Tuple[List[dict], List[int]]:
        uppercase_indices = [i for i, c in enumerate(word) if c.isupper()]
        result = []
        
        segments = self._camel_split_with_positions(word)
        
        for seg, orig_pos in segments:
            if orig_pos < len(word) and word[orig_pos].isupper():
                result.append(self.uppercase_marker)
            
            s = seg
            pos = 0
            
            while pos < len(s):
                substr = s[pos:]
                
                rid, rtok = self._longest_prefix_lookup(substr, self.roots, self.max_root_len)
                if rid is not None:
                    result.append({"token": rtok, "id": rid, "type": TokenType.ROOT})
                    pos += len(rtok)
                    continue
                
                sid, stok = self._longest_prefix_lookup(substr, self.suffixes, self.max_suffix_len)
                if sid is not None:
                    result.append({"token": stok, "id": sid, "type": TokenType.SUFFIX})
                    pos += len(stok)
                    continue
                
                bid, btok = self._longest_prefix_lookup(substr, self.bpe_tokens, self.max_bpe_len)
                if bid is not None:
                    result.append({"token": btok, "id": bid, "type": TokenType.BPE})
                    pos += len(btok)
                    continue
                
                result.append(self.unknown_marker)
                pos += 1
        
        return result, uppercase_indices

    def tokenize_text(self, text: str) -> Tuple[List[dict], List[int]]:
        final_tokens = []
        uppercase_indices = [i for i, c in enumerate(text) if c.isupper()]
        
        parts = text.split(" ")
        for idx, part in enumerate(parts):
            if part.strip():
                tokens, _ = self._tokenize_word(part)
                final_tokens.extend(tokens)
            if idx < len(parts) - 1:
                final_tokens.append(self.space_marker)
        
        return final_tokens, uppercase_indices
    
    def encode(self, text: str) -> List[int]:
        tokens, _ = self.tokenize_text(text)
        return [t["id"] for t in tokens]
    
    def tokenize(self, text: str) -> List[str]:
        tokens, _ = self.tokenize_text(text)
        return [t["token"] for t in tokens]
    
    def _longest_prefix_lookup(self, s: str, table: Dict[str, int], max_len: int = None) -> Tuple[Optional[int], str]:
        end = min(len(s), max_len) if max_len else len(s)
        for i in range(end, 0, -1):
            cand = s[:i]
            if cand in table:
                return table[cand], cand
        return None, ""
    def _tr_lower(self, word: str) -> str:
        if "I" in word or "İ" in word:
            word = word.replace("İ", "i").replace("I", "ı")
        return word.lower()
    
    def _camel_split_with_positions(self, word: str) -> List[Tuple[str, int]]:
        if not word:
            return []
        
        parts = []
        start = 0
        
        for i in range(1, len(word)):
            if word[i].isupper():
                if start < i:
                    parts.append((self._tr_lower(word[start:i]), start))
                start = i
        
        if start < len(word):
            parts.append((self._tr_lower(word[start:]), start))
        
        return parts if parts else [(self._tr_lower(word), 0)]

    def decode(self, ids: List[int]) -> str:
        return self.decoder.decode(ids)

    # added to be compatible with SFTTrainer
    def __call__(self, text: str) -> Dict[str, List[int]]:
        input_ids = self.encode(text)
        attention_mask = [1 for _ in input_ids]
        return {"input_ids": input_ids, "attention_mask": attention_mask}
