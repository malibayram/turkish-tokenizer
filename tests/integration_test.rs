use turkish_tokenizer::{TurkishTokenizer, TokenType};

#[test]
fn test_comprehensive_tokenization() {
    let tokenizer = TurkishTokenizer::new_rust().unwrap();
    
    // Test various Turkish linguistic features
    let test_cases = vec![
        // Simple words
        ("ev", vec!["ev"]),
        ("evler", vec!["ev", "ler"]),
        
        // Complex morphology
        ("kitaplarımızdan", vec!["kitap", "lar", "ım", "ız", "dan"]),
        
        // Verb conjugations
        ("geliyorum", vec!["gel", "i", "yorum"]),
        ("gelmiştim", vec!["gel", "miş", "tim"]),
        
        // Mixed case
        ("merhabaDünya", vec!["merhaba", "<uppercase>", "dünya"]),
        
        // Multiple words
        ("merhaba dünya", vec!["merhaba", " ", "dünya"]),
    ];
    
    for (input, expected_tokens) in test_cases {
        let tokens = tokenizer.tokenize(input);
        assert_eq!(
            tokens, expected_tokens,
            "Failed for input '{}': expected {:?}, got {:?}",
            input, expected_tokens, tokens
        );
    }
}

#[test]
fn test_special_tokens() {
    let tokenizer = TurkishTokenizer::new_rust().unwrap();
    
    // Test that special tokens are properly handled
    assert!(tokenizer.contains_token("<pad>"));
    assert!(tokenizer.contains_token("<eos>"));
    assert!(tokenizer.contains_token("<uppercase>"));
    assert!(tokenizer.contains_token("<unknown>"));
    assert!(tokenizer.contains_token(" "));
    
    // Test special token IDs
    assert_eq!(tokenizer.token_to_id("<pad>"), Some(tokenizer.pad_token_id));
    assert_eq!(tokenizer.token_to_id("<eos>"), Some(tokenizer.eos_token_id));
}

#[test]
fn test_token_type_distribution() {
    let tokenizer = TurkishTokenizer::new_rust().unwrap();
    
    // Test a word that should have different token types
    let tokens = tokenizer.tokenize_text("kitaplarımı");
    
    let mut has_root = false;
    let mut has_suffix = false;
    
    for token in tokens {
        match token.token_type {
            TokenType::Root => has_root = true,
            TokenType::Suffix => has_suffix = true,
            TokenType::Bpe => {},
        }
    }
    
    assert!(has_root, "Should have at least one root token");
    assert!(has_suffix, "Should have at least one suffix token");
}

#[test]
fn test_encoding_consistency() {
    let tokenizer = TurkishTokenizer::new_rust().unwrap();
    
    let text = "Türkçe çok güzel";
    
    // Test that encode() and tokenize_text() produce consistent results
    let token_ids = tokenizer.encode(text);
    let detailed_tokens = tokenizer.tokenize_text(text);
    let detailed_ids: Vec<u32> = detailed_tokens.iter().map(|t| t.id).collect();
    
    assert_eq!(token_ids, detailed_ids);
    
    // Test encode_plus consistency
    let encode_plus_result = tokenizer.encode_plus(text);
    assert_eq!(token_ids, encode_plus_result.input_ids);
    
    let simple_tokens = tokenizer.tokenize(text);
    assert_eq!(simple_tokens, encode_plus_result.tokens);
}

#[test]
fn test_empty_and_edge_cases() {
    let tokenizer = TurkishTokenizer::new_rust().unwrap();
    
    // Empty string
    let tokens = tokenizer.tokenize("");
    assert!(tokens.is_empty());
    
    let ids = tokenizer.encode("");
    assert!(ids.is_empty());
    
    // Single space
    let tokens = tokenizer.tokenize(" ");
    assert_eq!(tokens, vec![" "]);
    
    // Multiple spaces
    let tokens = tokenizer.tokenize("  ");
    assert_eq!(tokens, vec![" ", " "]);
    
    // Single character
    let tokens = tokenizer.tokenize("a");
    assert!(!tokens.is_empty());
}
