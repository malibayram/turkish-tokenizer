use turkish_tokenizer::{TurkishTokenizer, TokenType};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("Turkish Tokenizer - Basic Usage Example");
    println!("=======================================\n");
    
    // Initialize the tokenizer
    let tokenizer = TurkishTokenizer::new_rust()?;
    
    println!("Tokenizer Info:");
    println!("- Vocabulary size: {}", tokenizer.vocab_size());
    println!("- Pad token: '{}' (ID: {})", tokenizer.pad_token, tokenizer.pad_token_id);
    println!("- EOS token: '{}' (ID: {})", tokenizer.eos_token, tokenizer.eos_token_id);
    println!();
    
    // Test various Turkish texts
    let examples = vec![
        ("Simple text", "merhaba dünya"),
        ("Mixed case", "merhabaDünya"),
        ("Complex morphology", "kitaplarımızdan"),
        ("Verb conjugation", "geliyormuşsun"),
        ("Multiple words", "Türkçe çok güzel bir dil"),
    ];
    
    for (description, text) in examples {
        println!("Example: {} - '{}'", description, text);
        
        // Get detailed tokens
        let detailed_tokens = tokenizer.tokenize_text(text);
        println!("  Detailed tokens:");
        for (i, token) in detailed_tokens.iter().enumerate() {
            println!("    {}: '{}' (ID: {}, Type: {:?})", 
                     i, token.token, token.id, token.token_type);
        }
        
        // Get simple tokens
        let tokens = tokenizer.tokenize(text);
        println!("  Simple tokens: {:?}", tokens);
        
        // Get token IDs
        let token_ids = tokenizer.encode(text);
        println!("  Token IDs: {:?}", token_ids);
        
        println!();
    }
    
    // Demonstrate token type distribution
    println!("Token Type Analysis for 'kitaplarımızdan':");
    let tokens = tokenizer.tokenize_text("kitaplarımızdan");
    let mut root_count = 0;
    let mut suffix_count = 0;
    let mut bpe_count = 0;
    
    for token in &tokens {
        match token.token_type {
            TokenType::Root => root_count += 1,
            TokenType::Suffix => suffix_count += 1,
            TokenType::Bpe => bpe_count += 1,
        }
    }
    
    println!("- Root tokens: {}", root_count);
    println!("- Suffix tokens: {}", suffix_count);
    println!("- BPE tokens: {}", bpe_count);
    
    Ok(())
}
