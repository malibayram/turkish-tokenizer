import torch

LLAMA32_CONFIG_1B = {
    "vocab_size": 128_256,           # Vocabulary size
    "context_length": 131_072,       # Context length that was used to train the model
    "emb_dim": 2048,                 # Embedding dimension
    "n_heads": 32,                   # Number of attention heads
    "n_layers": 16,                  # Number of layers
    "hidden_dim": 8192,              # Size of the intermediate dimension in FeedForward
    "n_kv_groups": 8,                # Key-Value groups for grouped-query attention
    "rope_base": 500_000.0,          # The base in RoPE's "theta"
    "dtype": torch.bfloat16,         # Lower-precision dtype to reduce memory usage
    "rope_freq": {                   # RoPE frequency scaling
        "factor": 32.0,
        "low_freq_factor": 1.0,
        "high_freq_factor": 4.0,
        "original_context_length": 8192,
    }
}

class LlamaConfig():
  def __init__(
          self,
          vocab_size: int = 128_256,
          context_length: int = 131_072,
          emb_dim: int = 2048,
          n_heads: int = 32,
          n_layers: int = 16,
          hidden_dim: int = 8192,
          n_kv_groups: int = 8,
          head_dim: int | None = None,
          dtype: torch.dtype = torch.float32,
          mlp_bias: bool = False,
          rms_norm_eps: float = 1e-6,
          bias: bool = False,
          attention_bias: bool = False,
        ):
      self.vocab_size = vocab_size
      self.max_position_embeddings = context_length
      self.hidden_size = emb_dim
      self.num_attention_heads = n_heads
      self.num_hidden_layers = n_layers
      self.num_key_value_heads = n_kv_groups
      self.head_dim = head_dim if head_dim is not None else self.hidden_size // self.num_attention_heads
      self.dtype = dtype
      self.intermediate_size = hidden_dim
      self.mlp_bias = mlp_bias
      self.rms_norm_eps = rms_norm_eps
      self.bias = bias
      self.attention_bias = attention_bias
