use turkish_tokenizer::TurkishTokenizer;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("Turkish Tokenizer - Rust Implementation");
    println!("======================================");
    
    // Initialize the tokenizer
    let tokenizer = TurkishTokenizer::new_rust()?;
    
    println!("Vocabulary size: {}", tokenizer.vocab_size());
    println!("Pad token: {} (ID: {})", tokenizer.pad_token, tokenizer.pad_token_id);
    println!("EOS token: {} (ID: {})", tokenizer.eos_token, tokenizer.eos_token_id);
    println!();
    
    // Test examples
    let examples = vec![
        "merhaba dünya",
        "Türkçe tokenizer",
        "merhabaDünya",
        "geliyorum",
        "kitaplarımı",
    ];
    
    for example in examples {
        println!("Text: '{}'", example);
        
        // Get tokens
        let tokens = tokenizer.tokenize(example);
        println!("Tokens: {:?}", tokens);
        
        // Get token IDs
        let token_ids = tokenizer.encode(example);
        println!("Token IDs: {:?}", token_ids);
        
        println!();
    }
    
    Ok(())
}
