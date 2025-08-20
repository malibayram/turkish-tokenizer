import json
import os
from typing import Any, Dict, List, Optional, Tuple, Union

try:
    from transformers import PreTrainedTokenizer
    from transformers.tokenization_utils_base import (BatchEncoding,
                                                      TruncationStrategy)
    from transformers.utils import PaddingStrategy
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    # Create dummy classes for when transformers is not available
    class PreTrainedTokenizer:
        def __init__(self, **kwargs):
            # Initialize with basic attributes
            self.vocab_file = kwargs.get('vocab_file')
            self.model_max_length = kwargs.get('model_max_length')
            self.padding_side = kwargs.get('padding_side', 'right')
            self.truncation_side = kwargs.get('truncation_side', 'right')
            self.clean_up_tokenization_spaces = kwargs.get('clean_up_tokenization_spaces', True)
            self.split_special_tokens = kwargs.get('split_special_tokens', False)
            
            # Initialize special tokens
            self.pad_token = None
            self.eos_token = None
            self.unk_token = None
            self.bos_token = None
            self.sep_token = None
            self.cls_token = None
            self.mask_token = None
            self.additional_special_tokens = []
            self.all_special_tokens = []
            
        def add_special_tokens(self, special_tokens_dict):
            """Dummy method for adding special tokens."""
            pass
            
    class BatchEncoding:
        def __init__(self, data, tensor_type=None):
            self.data = data
            self.tensor_type = tensor_type
            
        def __getitem__(self, key):
            return self.data[key]
            
        def __contains__(self, key):
            return key in self.data
            
        def keys(self):
            return self.data.keys()
            
        def values(self):
            return self.data.values()
            
        def items(self):
            return self.data.items()
            
    class TruncationStrategy:
        pass
    class PaddingStrategy:
        pass

from .turkish_tokenizer import TurkishTokenizer


class HFTurkishTokenizer(PreTrainedTokenizer):
    """
    Hugging Face compatible Turkish tokenizer that wraps the existing TurkishTokenizer implementation.
    
    This tokenizer is designed for Turkish language processing with morphological analysis capabilities.
    """
    
    vocab_files_names = {
        "vocab_file": "kokler.json",
        "suffixes_file": "ekler.json", 
        "bpe_file": "bpe_tokenler.json"
    }
    
    model_input_names = ["input_ids", "attention_mask"]
    
    def __init__(
        self,
        vocab_file: Optional[str] = None,
        suffixes_file: Optional[str] = None,
        bpe_file: Optional[str] = None,
        model_max_length: Optional[int] = None,
        padding_side: str = "right",
        truncation_side: str = "right",
        pad_token: str = "<pad>",
        eos_token: str = "<eos>",
        unk_token: str = "<unknown>",
        bos_token: Optional[str] = None,
        sep_token: Optional[str] = None,
        cls_token: Optional[str] = None,
        mask_token: Optional[str] = None,
        additional_special_tokens: Optional[List[str]] = None,
        clean_up_tokenization_spaces: bool = True,
        split_special_tokens: bool = False,
        **kwargs
    ):
        """
        Initialize the Turkish tokenizer.
        
        Args:
            vocab_file: Path to the roots vocabulary file
            suffixes_file: Path to the suffixes vocabulary file  
            bpe_file: Path to the BPE tokens vocabulary file
            model_max_length: Maximum sequence length
            padding_side: Side to apply padding ('left' or 'right')
            truncation_side: Side to apply truncation ('left' or 'right')
            pad_token: Padding token
            eos_token: End of sequence token
            unk_token: Unknown token
            bos_token: Beginning of sequence token
            sep_token: Separator token
            cls_token: Classification token
            mask_token: Mask token
            additional_special_tokens: Additional special tokens
            clean_up_tokenization_spaces: Whether to clean up spaces
            split_special_tokens: Whether to split special tokens
        """
        # Set default paths if not provided
        if vocab_file is None:
            package_dir = os.path.dirname(os.path.abspath(__file__))
            vocab_file = os.path.join(package_dir, "kokler.json")
        if suffixes_file is None:
            package_dir = os.path.dirname(os.path.abspath(__file__))
            suffixes_file = os.path.join(package_dir, "ekler.json")
        if bpe_file is None:
            package_dir = os.path.dirname(os.path.abspath(__file__))
            bpe_file = os.path.join(package_dir, "bpe_tokenler.json")
            
        # Initialize the underlying Turkish tokenizer
        self.turkish_tokenizer = TurkishTokenizer()
        
        # Set special tokens
        special_tokens_dict = {
            "pad_token": pad_token,
            "eos_token": eos_token,
            "unk_token": unk_token,
        }
        
        if bos_token is not None:
            special_tokens_dict["bos_token"] = bos_token
        if sep_token is not None:
            special_tokens_dict["sep_token"] = sep_token
        if cls_token is not None:
            special_tokens_dict["cls_token"] = cls_token
        if mask_token is not None:
            special_tokens_dict["mask_token"] = mask_token
            
        # Call parent constructor
        super().__init__(
            vocab_file=vocab_file,
            model_max_length=model_max_length,
            padding_side=padding_side,
            truncation_side=truncation_side,
            clean_up_tokenization_spaces=clean_up_tokenization_spaces,
            split_special_tokens=split_special_tokens,
            **kwargs
        )
        
        # Add special tokens
        self.add_special_tokens(special_tokens_dict)
        
        if additional_special_tokens is not None:
            self.add_special_tokens({"additional_special_tokens": additional_special_tokens})
    
    @property
    def vocab_size(self) -> int:
        """Return the size of the vocabulary."""
        return len(self.get_vocab())
    
    def get_vocab(self) -> Dict[str, int]:
        """Return the vocabulary as a dictionary."""
        return self.turkish_tokenizer.get_vocab()
    
    def _tokenize(self, text: str, **kwargs) -> List[str]:
        """
        Tokenize a text into a list of tokens.
        
        Args:
            text: Text to tokenize
            
        Returns:
            List of tokens
        """
        return self.turkish_tokenizer.tokenize(text)
    
    def _convert_token_to_id(self, token: str) -> int:
        """
        Convert a token to its ID.
        
        Args:
            token: Token to convert
            
        Returns:
            Token ID
        """
        vocab = self.get_vocab()
        return vocab.get(token, vocab.get(self.unk_token, 1))
    
    def _convert_id_to_token(self, index: int) -> str:
        """
        Convert an ID to its token.
        
        Args:
            index: Token ID
            
        Returns:
            Token string
        """
        reverse_dict = self.turkish_tokenizer.reverse_dict
        if index in reverse_dict:
            tokens = reverse_dict[index]
            return tokens[0] if tokens else self.unk_token
        return self.unk_token
    
    def convert_tokens_to_ids(self, tokens: Union[str, List[str]]) -> Union[int, List[int]]:
        """
        Convert tokens to their corresponding IDs.
        
        Args:
            tokens: Token or list of tokens
            
        Returns:
            Token ID or list of token IDs
        """
        if isinstance(tokens, str):
            return self._convert_token_to_id(tokens)
        
        return [self._convert_token_to_id(token) for token in tokens]
    
    def convert_ids_to_tokens(self, ids: Union[int, List[int]], skip_special_tokens: bool = False) -> Union[str, List[str]]:
        """
        Convert IDs to their corresponding tokens.
        
        Args:
            ids: Token ID or list of token IDs
            skip_special_tokens: Whether to skip special tokens
            
        Returns:
            Token or list of tokens
        """
        if isinstance(ids, int):
            token = self._convert_id_to_token(ids)
            if skip_special_tokens and token in self.all_special_tokens:
                return ""
            return token
        
        tokens = []
        for token_id in ids:
            token = self._convert_id_to_token(token_id)
            if skip_special_tokens and token in self.all_special_tokens:
                continue
            tokens.append(token)
        
        return tokens
    
    def encode(
        self,
        text: Union[str, List[str]],
        text_pair: Optional[Union[str, List[str]]] = None,
        add_special_tokens: bool = True,
        padding: Union[bool, str, PaddingStrategy] = False,
        truncation: Union[bool, str, TruncationStrategy] = False,
        max_length: Optional[int] = None,
        stride: int = 0,
        return_tensors: Optional[Union[str, Any]] = None,
        **kwargs
    ) -> Union[List[int], List[List[int]]]:
        """
        Encode text to token IDs.
        
        Args:
            text: Text to encode
            text_pair: Optional second text for sequence pairs
            add_special_tokens: Whether to add special tokens
            padding: Padding strategy
            truncation: Truncation strategy
            max_length: Maximum sequence length
            stride: Stride for overflow handling
            return_tensors: Tensor type to return
            
        Returns:
            Encoded token IDs
        """
        if isinstance(text, str):
            text = [text]
        
        if text_pair is not None and isinstance(text_pair, str):
            text_pair = [text_pair]
        
        # Encode each text
        encoded = []
        for i, t in enumerate(text):
            pair = text_pair[i] if text_pair else None
            
            # Handle empty text
            if not t.strip():
                ids = []
            else:
                # Tokenize
                tokens = self._tokenize(t)
                if pair:
                    pair_tokens = self._tokenize(pair)
                    tokens = tokens + [self.sep_token] + pair_tokens if self.sep_token else tokens + pair_tokens
                
                # Convert to IDs
                ids = self.convert_tokens_to_ids(tokens)
            
            # Add special tokens
            if add_special_tokens:
                if self.bos_token and self.bos_token_id is not None:
                    ids = [self.bos_token_id] + ids
                if self.eos_token and self.eos_token_id is not None:
                    ids = ids + [self.eos_token_id]
            
            encoded.append(ids)
        
        # Handle padding and truncation
        if len(encoded) == 1:
            encoded = encoded[0]
        
        return encoded
    
    def decode(
        self,
        token_ids: Union[int, List[int], List[List[int]]],
        skip_special_tokens: bool = False,
        clean_up_tokenization_spaces: Optional[bool] = None,
        **kwargs
    ) -> str:
        """
        Decode token IDs to text.
        
        Args:
            token_ids: Token IDs to decode
            skip_special_tokens: Whether to skip special tokens
            clean_up_tokenization_spaces: Whether to clean up spaces
            
        Returns:
            Decoded text
        """
        if isinstance(token_ids, int):
            token_ids = [token_ids]
        
        # Handle empty list
        if not token_ids:
            return ""
        
        if isinstance(token_ids[0], list):
            # Batch decoding
            return [self.decode(ids, skip_special_tokens, clean_up_tokenization_spaces) for ids in token_ids]
        
        # Filter out special tokens if requested
        if skip_special_tokens:
            filtered_ids = []
            for token_id in token_ids:
                token = self._convert_id_to_token(token_id)
                if token not in self.all_special_tokens:
                    filtered_ids.append(token_id)
            token_ids = filtered_ids
        
        # Use the Turkish decoder for proper morphological reconstruction
        return self.turkish_tokenizer.decode(token_ids)
    
    def save_pretrained(self, save_directory: str, **kwargs):
        """
        Save the tokenizer to a directory.
        
        Args:
            save_directory: Directory to save to
        """
        os.makedirs(save_directory, exist_ok=True)
        
        # Save vocabulary files
        package_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Copy vocabulary files
        import shutil
        for filename in ["kokler.json", "ekler.json", "bpe_tokenler.json"]:
            src = os.path.join(package_dir, filename)
            dst = os.path.join(save_directory, filename)
            shutil.copy2(src, dst)
        
        # Save tokenizer configuration
        tokenizer_config = {
            "tokenizer_class": self.__class__.__name__,
            "model_max_length": self.model_max_length,
            "padding_side": self.padding_side,
            "truncation_side": self.truncation_side,
            "pad_token": self.pad_token,
            "eos_token": self.eos_token,
            "unk_token": self.unk_token,
            "bos_token": self.bos_token,
            "sep_token": self.sep_token,
            "cls_token": self.cls_token,
            "mask_token": self.mask_token,
            "additional_special_tokens": self.additional_special_tokens,
            "clean_up_tokenization_spaces": self.clean_up_tokenization_spaces,
            "split_special_tokens": self.split_special_tokens,
        }
        
        with open(os.path.join(save_directory, "tokenizer_config.json"), "w", encoding="utf-8") as f:
            json.dump(tokenizer_config, f, indent=2, ensure_ascii=False)
    
    @classmethod
    def from_pretrained(cls, pretrained_model_name_or_path: str, *args, **kwargs):
        """
        Load a tokenizer from a pretrained model or directory.
        
        Args:
            pretrained_model_name_or_path: Path to the pretrained model or directory
            
        Returns:
            Loaded tokenizer
        """
        # Check if it's a local directory
        if os.path.isdir(pretrained_model_name_or_path):
            # Load from local directory
            config_path = os.path.join(pretrained_model_name_or_path, "tokenizer_config.json")
            if os.path.exists(config_path):
                with open(config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                
                # Update kwargs with config values
                for key, value in config.items():
                    if key not in kwargs and key != "tokenizer_class":
                        kwargs[key] = value
                
                return cls(pretrained_model_name_or_path, *args, **kwargs)
        
        # For now, just return a new instance with default settings
        # In a full implementation, you might want to download from Hugging Face Hub
        return cls(*args, **kwargs)
    
    def __call__(
        self,
        text: Union[str, List[str], List[List[str]]] = None,
        text_pair: Union[str, List[str], List[List[str]]] = None,
        text_target: Union[str, List[str], List[List[str]]] = None,
        text_pair_target: Union[str, List[str], List[List[str]]] = None,
        add_special_tokens: bool = True,
        padding: Union[bool, str, PaddingStrategy] = False,
        truncation: Union[bool, str, TruncationStrategy] = False,
        max_length: Optional[int] = None,
        stride: int = 0,
        is_split_into_words: bool = False,
        pad_to_multiple_of: Optional[int] = None,
        return_tensors: Optional[Union[str, Any]] = None,
        return_token_type_ids: Optional[bool] = None,
        return_attention_mask: Optional[bool] = None,
        return_overflowing_tokens: bool = False,
        return_special_tokens_mask: bool = False,
        return_offsets_mapping: bool = False,
        return_length: bool = False,
        verbose: bool = True,
        **kwargs
    ) -> BatchEncoding:
        """
        Main method to tokenize and prepare inputs for the model.
        
        Args:
            text: Text to tokenize
            text_pair: Optional second text for sequence pairs
            text_target: Target text for sequence-to-sequence tasks
            text_pair_target: Optional second target text
            add_special_tokens: Whether to add special tokens
            padding: Padding strategy
            truncation: Truncation strategy
            max_length: Maximum sequence length
            stride: Stride for overflow handling
            is_split_into_words: Whether input is pre-tokenized
            pad_to_multiple_of: Pad to multiple of this value
            return_tensors: Tensor type to return
            return_token_type_ids: Whether to return token type IDs
            return_attention_mask: Whether to return attention mask
            return_overflowing_tokens: Whether to return overflowing tokens
            return_special_tokens_mask: Whether to return special tokens mask
            return_offsets_mapping: Whether to return offset mappings
            return_length: Whether to return sequence lengths
            verbose: Whether to print verbose output
            
        Returns:
            BatchEncoding with tokenized inputs
        """
        # Encode the text
        if text is not None:
            input_ids = self.encode(
                text=text,
                text_pair=text_pair,
                add_special_tokens=add_special_tokens,
                padding=False,  # We'll handle padding manually
                truncation=truncation,
                max_length=max_length,
                stride=stride,
                return_tensors=None,  # Always return lists for manual processing
                **kwargs
            )
        else:
            input_ids = []
        
        # Handle padding manually if requested
        if padding and input_ids:
            if isinstance(input_ids, list) and len(input_ids) > 0 and isinstance(input_ids[0], list):
                # Batch padding
                max_length = max(len(ids) for ids in input_ids)
                if max_length is not None:
                    max_length = min(max_length, max_length)
                
                padded_input_ids = []
                for ids in input_ids:
                    if len(ids) < max_length:
                        padding_length = max_length - len(ids)
                        if self.padding_side == "right":
                            padded_ids = ids + [self.pad_token_id] * padding_length
                        else:
                            padded_ids = [self.pad_token_id] * padding_length + ids
                        padded_input_ids.append(padded_ids)
                    else:
                        padded_input_ids.append(ids[:max_length])
                input_ids = padded_input_ids
            else:
                # Single sequence padding
                if max_length is not None and len(input_ids) < max_length:
                    padding_length = max_length - len(input_ids)
                    if self.padding_side == "right":
                        input_ids = input_ids + [self.pad_token_id] * padding_length
                    else:
                        input_ids = [self.pad_token_id] * padding_length + input_ids
        
        # Prepare the output
        batch_outputs = {}
        
        if input_ids:
            batch_outputs["input_ids"] = input_ids
            
            # Add attention mask
            if return_attention_mask or return_attention_mask is None:
                if isinstance(input_ids, list) and len(input_ids) > 0 and isinstance(input_ids[0], list):
                    attention_mask = [[1 if id != self.pad_token_id else 0 for id in ids] for ids in input_ids]
                else:
                    attention_mask = [1 if id != self.pad_token_id else 0 for id in input_ids]
                batch_outputs["attention_mask"] = attention_mask
        
        return BatchEncoding(batch_outputs, tensor_type=return_tensors)
