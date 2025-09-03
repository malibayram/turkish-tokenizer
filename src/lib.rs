use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use pyo3::prelude::*;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[pyclass(eq, eq_int)]
pub enum TokenType {
    #[serde(rename = "ROOT")]
    Root,
    #[serde(rename = "SUFFIX")]
    Suffix,
    #[serde(rename = "BPE")]
    Bpe,
}

#[derive(Debug, Clone)]
#[pyclass]
pub struct Token {
    #[pyo3(get)]
    pub token: String,
    #[pyo3(get)]
    pub id: u32,
    #[pyo3(get)]
    pub token_type: TokenType,
}

#[pyclass]
pub struct TurkishTokenizer {
    roots: HashMap<String, u32>,
    suffixes: HashMap<String, u32>,
    bpe_tokens: HashMap<String, u32>,
    vocab: HashMap<String, u32>,
    max_root_len: usize,
    max_suffix_len: usize,
    max_bpe_len: usize,
    uppercase_marker: Token,
    unknown_marker: Token,
    space_marker: Token,
    pub pad_token: String,
    pub eos_token: String,
    pub pad_token_id: u32,
    pub eos_token_id: u32,
}

#[pymethods]
impl TurkishTokenizer {
    #[new]
    pub fn new() -> PyResult<Self> {
        // Load JSON data from embedded files
        let roots_json = include_str!("../turkish_tokenizer/kokler.json");
        let suffixes_json = include_str!("../turkish_tokenizer/ekler.json");
        let bpe_tokens_json = include_str!("../turkish_tokenizer/bpe_tokenler.json");

        let roots: HashMap<String, u32> = serde_json::from_str(roots_json)
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("Failed to parse roots: {}", e)))?;
        let suffixes: HashMap<String, u32> = serde_json::from_str(suffixes_json)
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("Failed to parse suffixes: {}", e)))?;
        let bpe_tokens: HashMap<String, u32> = serde_json::from_str(bpe_tokens_json)
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("Failed to parse BPE tokens: {}", e)))?;

        // Create combined vocab
        let mut vocab = HashMap::new();
        vocab.extend(roots.clone());
        vocab.extend(suffixes.clone());
        vocab.extend(bpe_tokens.clone());

        let max_root_len = roots.keys().map(|k| k.len()).max().unwrap_or(0);
        let max_suffix_len = suffixes.keys().map(|k| k.len()).max().unwrap_or(0);
        let max_bpe_len = bpe_tokens.keys().map(|k| k.len()).max().unwrap_or(0);

        // Create special tokens
        let uppercase_marker = Token {
            token: "<uppercase>".to_string(),
            id: *roots.get("<uppercase>").unwrap(),
            token_type: TokenType::Root,
        };
        let unknown_marker = Token {
            token: "<unknown>".to_string(),
            id: *roots.get("<unknown>").unwrap(),
            token_type: TokenType::Root,
        };
        let space_marker = Token {
            token: " ".to_string(),
            id: *roots.get(" ").unwrap(),
            token_type: TokenType::Root,
        };

        let pad_token = "<pad>".to_string();
        let eos_token = "<eos>".to_string();
        let pad_token_id = *roots.get(&pad_token).unwrap();
        let eos_token_id = *roots.get(&eos_token).unwrap();

        Ok(TurkishTokenizer {
            roots,
            suffixes,
            bpe_tokens,
            vocab,
            max_root_len,
            max_suffix_len,
            max_bpe_len,
            uppercase_marker,
            unknown_marker,
            space_marker,
            pad_token,
            eos_token,
            pad_token_id,
            eos_token_id,
        })
    }

    /// Get the vocabulary as a Python dictionary
    #[pyo3(name = "get_vocab")]
    pub fn py_get_vocab(&self) -> HashMap<String, u32> {
        self.vocab.clone()
    }

    /// Get vocabulary size
    #[pyo3(name = "vocab_size")]
    pub fn py_vocab_size(&self) -> usize {
        self.vocab_size()
    }

    /// Encode text to token IDs
    #[pyo3(name = "encode")]
    pub fn py_encode(&self, text: &str) -> Vec<u32> {
        self.encode(text)
    }

    /// Tokenize text to string tokens
    #[pyo3(name = "tokenize")]
    pub fn py_tokenize(&self, text: &str) -> Vec<String> {
        self.tokenize(text)
    }

    /// Get detailed token information
    #[pyo3(name = "tokenize_text")]
    pub fn py_tokenize_text(&self, text: &str) -> Vec<Token> {
        self.tokenize_text(text)
    }

    /// Convert tokens to IDs
    #[pyo3(name = "convert_tokens_to_ids")]
    pub fn py_convert_tokens_to_ids(&self, tokens: Vec<String>) -> Vec<u32> {
        self.convert_tokens_to_ids(&tokens)
    }

    /// Get token ID for a specific token
    #[pyo3(name = "token_to_id")]
    pub fn py_token_to_id(&self, token: &str) -> Option<u32> {
        self.token_to_id(token)
    }

    /// Check if token exists in vocabulary
    #[pyo3(name = "contains_token")]
    pub fn py_contains_token(&self, token: &str) -> bool {
        self.contains_token(token)
    }

    /// Get pad token
    #[getter]
    pub fn pad_token(&self) -> &str {
        &self.pad_token
    }

    /// Get EOS token
    #[getter]
    pub fn eos_token(&self) -> &str {
        &self.eos_token
    }

    /// Get pad token ID
    #[getter]
    pub fn pad_token_id(&self) -> u32 {
        self.pad_token_id
    }

    /// Get EOS token ID
    #[getter]
    pub fn eos_token_id(&self) -> u32 {
        self.eos_token_id
    }

    /// Python-style call method for compatibility
    pub fn __call__(&self, text: &str) -> HashMap<String, Vec<u32>> {
        let input_ids = self.encode(text);
        let attention_mask = vec![1u32; input_ids.len()];
        
        let mut result = HashMap::new();
        result.insert("input_ids".to_string(), input_ids);
        result.insert("attention_mask".to_string(), attention_mask);
        result
    }
}

// Separate implementation block for non-Python methods
impl TurkishTokenizer {
    pub fn new_rust() -> Result<Self, Box<dyn std::error::Error>> {
        // Load JSON data from embedded files
        let roots_json = include_str!("../turkish_tokenizer/kokler.json");
        let suffixes_json = include_str!("../turkish_tokenizer/ekler.json");
        let bpe_tokens_json = include_str!("../turkish_tokenizer/bpe_tokenler.json");

        let roots: HashMap<String, u32> = serde_json::from_str(roots_json)?;
        let suffixes: HashMap<String, u32> = serde_json::from_str(suffixes_json)?;
        let bpe_tokens: HashMap<String, u32> = serde_json::from_str(bpe_tokens_json)?;

        // Create combined vocab
        let mut vocab = HashMap::new();
        vocab.extend(roots.clone());
        vocab.extend(suffixes.clone());
        vocab.extend(bpe_tokens.clone());

        let max_root_len = roots.keys().map(|k| k.len()).max().unwrap_or(0);
        let max_suffix_len = suffixes.keys().map(|k| k.len()).max().unwrap_or(0);
        let max_bpe_len = bpe_tokens.keys().map(|k| k.len()).max().unwrap_or(0);

        // Create special tokens
        let uppercase_marker = Token {
            token: "<uppercase>".to_string(),
            id: *roots.get("<uppercase>").unwrap(),
            token_type: TokenType::Root,
        };
        let unknown_marker = Token {
            token: "<unknown>".to_string(),
            id: *roots.get("<unknown>").unwrap(),
            token_type: TokenType::Root,
        };
        let space_marker = Token {
            token: " ".to_string(),
            id: *roots.get(" ").unwrap(),
            token_type: TokenType::Root,
        };

        let pad_token = "<pad>".to_string();
        let eos_token = "<eos>".to_string();
        let pad_token_id = *roots.get(&pad_token).unwrap();
        let eos_token_id = *roots.get(&eos_token).unwrap();

        Ok(TurkishTokenizer {
            roots,
            suffixes,
            bpe_tokens,
            vocab,
            max_root_len,
            max_suffix_len,
            max_bpe_len,
            uppercase_marker,
            unknown_marker,
            space_marker,
            pad_token,
            eos_token,
            pad_token_id,
            eos_token_id,
        })
    }

    pub fn get_vocab(&self) -> &HashMap<String, u32> {
        &self.vocab
    }

    pub fn vocab_size(&self) -> usize {
        self.vocab.len()
    }

    pub fn encode(&self, text: &str) -> Vec<u32> {
        let tokens = self.tokenize_text(text);
        tokens.into_iter().map(|t| t.id).collect()
    }

    pub fn tokenize(&self, text: &str) -> Vec<String> {
        let tokens = self.tokenize_text(text);
        tokens.into_iter().map(|t| t.token).collect()
    }

    pub fn tokenize_text(&self, text: &str) -> Vec<Token> {
        let mut final_tokens = Vec::new();
        
        let parts: Vec<&str> = text.split(' ').collect();
        for (idx, part) in parts.iter().enumerate() {
            if !part.trim().is_empty() {
                let tokens = self.tokenize_word(part);
                final_tokens.extend(tokens);
            }
            if idx < parts.len() - 1 {
                final_tokens.push(self.space_marker.clone());
            }
        }
        
        final_tokens
    }

    fn tokenize_word(&self, word: &str) -> Vec<Token> {
        let mut result = Vec::new();
        let segments = self.camel_split_with_positions(word);
        
        for (seg, orig_pos) in segments {
            if orig_pos < word.len() && word.chars().nth(orig_pos).unwrap().is_uppercase() {
                result.push(self.uppercase_marker.clone());
            }
            
            let mut pos = 0;
            let seg_chars: Vec<char> = seg.chars().collect();
            
            while pos < seg_chars.len() {
                let substr: String = seg_chars[pos..].iter().collect();
                
                // Try root lookup
                if let Some((id, token)) = self.longest_prefix_lookup(&substr, &self.roots, Some(self.max_root_len)) {
                    let token_len = token.chars().count();
                    result.push(Token {
                        token,
                        id,
                        token_type: TokenType::Root,
                    });
                    pos += token_len;
                    continue;
                }
                
                // Try suffix lookup
                if let Some((id, token)) = self.longest_prefix_lookup(&substr, &self.suffixes, Some(self.max_suffix_len)) {
                    let token_len = token.chars().count();
                    result.push(Token {
                        token,
                        id,
                        token_type: TokenType::Suffix,
                    });
                    pos += token_len;
                    continue;
                }
                
                // Try BPE lookup
                if let Some((id, token)) = self.longest_prefix_lookup(&substr, &self.bpe_tokens, Some(self.max_bpe_len)) {
                    let token_len = token.chars().count();
                    result.push(Token {
                        token,
                        id,
                        token_type: TokenType::Bpe,
                    });
                    pos += token_len;
                    continue;
                }
                
                // No match found, add unknown token
                result.push(self.unknown_marker.clone());
                pos += 1;
            }
        }
        
        result
    }

    fn longest_prefix_lookup(
        &self,
        s: &str,
        table: &HashMap<String, u32>,
        max_len: Option<usize>,
    ) -> Option<(u32, String)> {
        let chars: Vec<char> = s.chars().collect();
        let end = if let Some(max_len) = max_len {
            std::cmp::min(chars.len(), max_len)
        } else {
            chars.len()
        };
        
        for i in (1..=end).rev() {
            let candidate: String = chars[..i].iter().collect();
            if let Some(&id) = table.get(&candidate) {
                return Some((id, candidate));
            }
        }
        None
    }

    fn tr_lower(&self, word: &str) -> String {
        word.replace('İ', "i").replace('I', "ı").to_lowercase()
    }

    fn camel_split_with_positions(&self, word: &str) -> Vec<(String, usize)> {
        if word.is_empty() {
            return Vec::new();
        }
        
        let mut parts = Vec::new();
        let mut start = 0;
        let chars: Vec<char> = word.chars().collect();
        
        for i in 1..chars.len() {
            if chars[i].is_uppercase() {
                if start < i {
                    let segment: String = chars[start..i].iter().collect();
                    parts.push((self.tr_lower(&segment), start));
                }
                start = i;
            }
        }
        
        if start < chars.len() {
            let segment: String = chars[start..].iter().collect();
            parts.push((self.tr_lower(&segment), start));
        }
        
        if parts.is_empty() {
            vec![(self.tr_lower(word), 0)]
        } else {
            parts
        }
    }

    pub fn convert_tokens_to_ids(&self, tokens: &[String]) -> Vec<u32> {
        tokens.iter().map(|token| self.vocab[token]).collect()
    }

    /// Get the token ID for a specific token string
    pub fn token_to_id(&self, token: &str) -> Option<u32> {
        self.vocab.get(token).copied()
    }

    /// Check if a token exists in the vocabulary
    pub fn contains_token(&self, token: &str) -> bool {
        self.vocab.contains_key(token)
    }

    /// Encode text and return both tokens and IDs for compatibility
    pub fn encode_plus(&self, text: &str) -> EncodingResult {
        let tokens = self.tokenize_text(text);
        let token_strings: Vec<String> = tokens.iter().map(|t| t.token.clone()).collect();
        let token_ids: Vec<u32> = tokens.iter().map(|t| t.id).collect();
        let attention_mask: Vec<u32> = vec![1; token_ids.len()];
        
        EncodingResult {
            input_ids: token_ids,
            tokens: token_strings,
            attention_mask,
        }
    }
}

/// Result structure for encoding operations
#[derive(Debug, Clone)]
pub struct EncodingResult {
    pub input_ids: Vec<u32>,
    pub tokens: Vec<String>,
    pub attention_mask: Vec<u32>,
}

impl Default for TurkishTokenizer {
    fn default() -> Self {
        Self::new_rust().expect("Failed to create TurkishTokenizer")
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_tokenizer_creation() {
        let tokenizer = TurkishTokenizer::new_rust().unwrap();
        assert!(tokenizer.vocab_size() > 0);
        assert_eq!(tokenizer.pad_token, "<pad>");
        assert_eq!(tokenizer.eos_token, "<eos>");
    }

    #[test]
    fn test_basic_encoding() {
        let tokenizer = TurkishTokenizer::new_rust().unwrap();
        let text = "merhaba dünya";
        let tokens = tokenizer.encode(text);
        assert!(!tokens.is_empty());
    }

    #[test]
    fn test_tokenization() {
        let tokenizer = TurkishTokenizer::new_rust().unwrap();
        let text = "merhaba dünya";
        let tokens = tokenizer.tokenize(text);
        assert!(!tokens.is_empty());
        println!("Tokens: {:?}", tokens);
    }

    #[test]
    fn test_camel_case() {
        let tokenizer = TurkishTokenizer::new_rust().unwrap();
        let text = "merhabaDünya";
        let tokens = tokenizer.tokenize(text);
        assert!(!tokens.is_empty());
        println!("CamelCase tokens: {:?}", tokens);
    }

    #[test]
    fn test_encode_plus() {
        let tokenizer = TurkishTokenizer::new_rust().unwrap();
        let text = "merhaba dünya";
        let result = tokenizer.encode_plus(text);
        
        assert_eq!(result.input_ids.len(), result.tokens.len());
        assert_eq!(result.input_ids.len(), result.attention_mask.len());
        assert!(result.attention_mask.iter().all(|&x| x == 1));
    }

    #[test]
    fn test_token_utilities() {
        let tokenizer = TurkishTokenizer::new_rust().unwrap();
        
        // Test token_to_id
        assert_eq!(tokenizer.token_to_id("<pad>"), Some(tokenizer.pad_token_id));
        assert_eq!(tokenizer.token_to_id("<eos>"), Some(tokenizer.eos_token_id));
        assert_eq!(tokenizer.token_to_id("nonexistent_token"), None);
        
        // Test contains_token
        assert!(tokenizer.contains_token("<pad>"));
        assert!(tokenizer.contains_token("<eos>"));
        assert!(!tokenizer.contains_token("nonexistent_token"));
    }

    #[test]
    fn test_turkish_morphology() {
        let tokenizer = TurkishTokenizer::new_rust().unwrap();
        
        // Test complex Turkish word with multiple suffixes
        let tokens = tokenizer.tokenize_text("kitaplarımızdan");
        
        // Should have: kitap (root) + lar (suffix) + ım (suffix) + ız (suffix) + dan (suffix)
        assert_eq!(tokens.len(), 5);
        assert_eq!(tokens[0].token, "kitap");
        assert_eq!(tokens[0].token_type, TokenType::Root);
        assert_eq!(tokens[1].token, "lar");
        assert_eq!(tokens[1].token_type, TokenType::Suffix);
    }
}

/// Python module definition
#[pymodule]
fn turkish_tokenizer_rs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<TurkishTokenizer>()?;
    m.add_class::<Token>()?;
    m.add_class::<TokenType>()?;
    Ok(())
}
