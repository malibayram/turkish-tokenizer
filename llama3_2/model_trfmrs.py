import math
from typing import Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F

from .config import LlamaConfig


class LlamaRMSNorm(nn.Module):
    def __init__(self, hidden_size, eps=1e-6):
        """
        LlamaRMSNorm is equivalent to T5LayerNorm
        """
        super().__init__()
        self.weight = nn.Parameter(torch.ones(hidden_size))
        self.variance_epsilon = eps

    def forward(self, hidden_states):
        input_dtype = hidden_states.dtype
        hidden_states = hidden_states.to(torch.float32)
        variance = hidden_states.pow(2).mean(-1, keepdim=True)
        hidden_states = hidden_states * torch.rsqrt(variance + self.variance_epsilon)
        return self.weight * hidden_states.to(input_dtype)

def precompute_freqs_cis(dim:int, seq_len: int, theta: float=10000.0, device: torch.device = torch.device("cpu")):
  # Computing Theta value for each dim pair which is dim/2
  freqs = 1.0 / (theta ** (torch.arange(0, dim, 2,device=device)[:(dim//2)].float()/dim))

  # Computing range of positions(m) in the sequence
  t = torch.arange(seq_len, dtype=torch.float32, device=device)

  # freqs gives all the Theta value range for all the position of tokens in the sequence
  freqs = torch.outer(t, freqs).to(device)

  # This is the rotation matrix which needs to be converted to Polar form in order to perform rotation to the embedding
  freqs_cis = torch.polar(torch.ones_like(freqs).to(device), freqs).to(device)
  return freqs_cis

def reshape_for_broadcast(freqs_cis, x):
  ndim = x.ndim
  assert 0<=1<ndim
  assert freqs_cis.shape == (x.shape[1],x.shape[-1]), "the last two dimension of freqs_cis, x must match"
  shape = [d if i==1 or i==ndim-1 else 1 for i,d in enumerate(x.shape)]
  return freqs_cis.view(*shape)

def apply_rotary_emb(xq: torch.Tensor, xk: torch.Tensor, freqs_cis: torch.Tensor, device: torch.device = torch.device("cpu"))->Tuple[torch.Tensor, torch.Tensor]:
  # Applying rotary positional encoding to both query and key embedding together
  # First: The last dimension of xq and xk embedding needs to be reshaped to make it a pair. As rotation matrix is applied to each pair of dim.
  # Next: convert both xq and xk to complex number as the rotation matrix is only applicable to complex number
  xq_ = torch.view_as_complex(xq.float().reshape(*xq.shape[:-1], -1, 2)).to(device)    #xq_:[bsz, seq_len, n_heads, head_dim/2]
  xk_ = torch.view_as_complex(xk.float().reshape(*xk.shape[:-1], -1, 2)).to(device)    #xk_:[bsz, seq_len, n_heads, head_dim/2]

  # The rotation matrix(freqs_cis) dimensions across seq_len(dim=1) and head_dim(dim=3) should match with the embedding
  # Also, the shape freqs_cis should be the same with xq and xk, hence change the shape of freqs_cis:[seq_len,head_dim] -> freqs_cis:[1,seq_len,1,head_dim]
  freqs_cis = reshape_for_broadcast(freqs_cis, xq_)

  #Finally, perform rotation operation by multiplying with freqs_cis.
  #After the rotation is completed, convert both xq_out and xk_out back to real number and return
  xq_out = torch.view_as_real(xq_ * freqs_cis).flatten(3).to(device) #xq_out:[bsz, seq_len, n_heads, head_dim]
  xk_out = torch.view_as_real(xk_ * freqs_cis).flatten(3).to(device) #xk_out:[bsz, seq_len, n_heads, head_dim]
  return xq_out.type_as(xq), xk_out.type_as(xk)

def repeat_kv(x:torch.Tensor, n_rep: int)-> torch.Tensor:
  bsz, seq_len, n_kv_heads, head_dim = x.shape
  if n_rep == 1:
    return x
  return (
      x[:,:,:,None,:]
      .expand(bsz,seq_len,n_kv_heads,n_rep, head_dim)
      .reshape(bsz,seq_len,n_kv_heads * n_rep, head_dim)
  )

class LlamaMLP(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.hidden_size = config.hidden_size
        self.intermediate_size = config.intermediate_size
        self.gate_proj = nn.Linear(self.hidden_size, self.intermediate_size, bias=config.mlp_bias)
        self.up_proj = nn.Linear(self.hidden_size, self.intermediate_size, bias=config.mlp_bias)
        self.down_proj = nn.Linear(self.intermediate_size, self.hidden_size, bias=config.mlp_bias)
        self.act_fn = nn.SiLU() # nn.functional.silu ACT2FN[config.hidden_act]

    def forward(self, x):
        down_proj = self.down_proj(self.act_fn(self.gate_proj(x)) * self.up_proj(x))
        return down_proj
    
class LlamaAttention(nn.Module):
    """Multi-headed attention from 'Attention Is All You Need' paper"""
    def __init__(self, config: LlamaConfig, layer_idx: int):
        super().__init__()
        self.config = config
        self.layer_idx = layer_idx
        self.head_dim = getattr(config, "head_dim", config.hidden_size // config.num_attention_heads)
        self.num_key_value_groups = config.num_attention_heads // config.num_key_value_heads
        self.scaling = self.head_dim**-0.5
        self.num_attention_heads = config.num_attention_heads
        self.num_key_value_heads = config.num_key_value_heads

        self.q_proj = nn.Linear(
            config.hidden_size, config.num_attention_heads * self.head_dim, bias=config.attention_bias
        )
        self.k_proj = nn.Linear(
            config.hidden_size, config.num_key_value_heads * self.head_dim, bias=config.attention_bias
        )
        self.v_proj = nn.Linear(
            config.hidden_size, config.num_key_value_heads * self.head_dim, bias=config.attention_bias
        )
        self.o_proj = nn.Linear(
            config.num_attention_heads * self.head_dim, config.hidden_size, bias=config.attention_bias
        )
    
    def forward(self, hidden_states: torch.Tensor):
        batch_size, seq_len, _ = hidden_states.shape
        xq = self.q_proj(hidden_states)
        xk = self.k_proj(hidden_states)
        xv = self.v_proj(hidden_states)

        xq = xq.view(batch_size, seq_len, self.num_attention_heads, self.head_dim)
        xk = xk.view(batch_size, seq_len, self.num_key_value_heads, self.head_dim)
        xv = xv.view(batch_size, seq_len, self.num_key_value_heads, self.head_dim)

        # Compute rotation matrix and apply RoPE to queries and keys for for training.
        freqs_cis = precompute_freqs_cis(dim=self.head_dim, seq_len=seq_len, device=hidden_states.device)

        #xq[bsz,seq_len,n_heads, head_dim], xk[bsz,seq_len,n_heads, head_dim]
        xq, xk = apply_rotary_emb(xq, xk, freqs_cis, device=hidden_states.device)

        # Use repeat_kv function to make Keys,Values shape same as the queries shape
        #keys[bsz,seq_len,n_heads,head_dim], #values[bsz,seq_len,n_heads,head_dim]
        keys = repeat_kv(xk, self.num_key_value_groups) #keys[bsz,seq_len,n_heads,head_dim]
        values = repeat_kv(xv, self.num_key_value_groups)

        # For training mode, we'll compute mask and apply to the attention score later
        mask = torch.full((seq_len, seq_len),float("-inf"),device=hidden_states.device)
        mask = torch.triu(mask, diagonal=1).to(hidden_states.device)

        # To compute attention, we'll need to perform a transpose operation to reshape all queries, keys and values bring heads at dim 1 and seq at dim 2
        xq = xq.transpose(1,2)                  #xq[bsz,n_heads,seq_len,head_dim]
        keys = keys.transpose(1,2)              #keys[bsz,n_heads,seq_len,head_dim]
        values = values.transpose(1,2)          #values[bsz,n_heads,seq_len,head_dim]

        # Computing attention score
        scores = torch.matmul(xq, keys.transpose(2,3)).to(hidden_states.device)/math.sqrt(self.head_dim)
        if mask is not None:
          scores = scores + mask

        # Apply softmax to the attention score
        scores = F.softmax(scores.float(), dim=-1).type_as(xq)
        # Matrix multiplication of attention score with the values
        output = torch.matmul(scores, values).to(hidden_states.device)

        # We get the contextual embedding for each head
        # All heads need to be reshaped back and combined to give a single single contextual attention output
        # Shape change: output[bsz,n_heads,seq_len,head_dim] -> output[bsz,seq_len, n_heads,head_dim] -> output[bsz,seq_len, n_heads * head_dim]
        output = output.transpose(1,2).contiguous().view(batch_size, seq_len, -1)

        # shape: output [bsz,seq_len,dim]
        return self.o_proj(output)


class LlamaDecoderLayer(nn.Module):
    def __init__(self, config: LlamaConfig, layer_idx: int):
        super().__init__()
        self.hidden_size = config.hidden_size

        self.self_attn = LlamaAttention(config=config, layer_idx=layer_idx)

        self.mlp = LlamaMLP(config)
        self.input_layernorm = LlamaRMSNorm(config.hidden_size, eps=config.rms_norm_eps)
        self.post_attention_layernorm = LlamaRMSNorm(config.hidden_size, eps=config.rms_norm_eps)

    def forward(self, hidden_states: torch.Tensor):
        residual = hidden_states
        hidden_states = self.input_layernorm(hidden_states)
        hidden_states = self.self_attn(hidden_states)
        hidden_states = hidden_states + residual

        residual = hidden_states
        hidden_states = self.post_attention_layernorm(hidden_states)
        hidden_states = self.mlp(hidden_states)
        hidden_states = hidden_states + residual
        return hidden_states

class LlamaModel(nn.Module):
    def __init__(self, config: LlamaConfig, embedding: torch.Tensor = None):
        super().__init__()
        # self.padding_idx = config.pad_token_id
        self.vocab_size = config.vocab_size

        self.embed_tokens = nn.Embedding(config.vocab_size, config.hidden_size, dtype=config.dtype)
        self.layers = nn.ModuleList(
            [LlamaDecoderLayer(config, layer_idx) for layer_idx in range(config.num_hidden_layers)]
        )
        self.norm = LlamaRMSNorm(config.hidden_size, eps=config.rms_norm_eps)
        # self.rotary_emb = LlamaRotaryEmbedding(config=config)

    def forward(self, input_ids: torch.Tensor):
        hidden_states = self.embed_tokens(input_ids)

        for layer in self.layers:
            hidden_states = layer(hidden_states)

        hidden_states = self.norm(hidden_states)
        return hidden_states

class LlamaForCausalLM(nn.Module):
    def __init__(self, config: LlamaConfig, embedding: torch.Tensor = None):
        super().__init__()
        self.model = LlamaModel(config, embedding)
        self.lm_head = nn.Linear(config.hidden_size, config.vocab_size, bias=config.bias)

    def forward(self, input_ids: torch.Tensor):
        hidden_states = self.model(input_ids)
        return self.lm_head(hidden_states)