use turkish_tokenizer::TurkishTokenizer;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let tokenizer = TurkishTokenizer::new_rust()?;
    
    // Debug specific cases that failed
    println!("Debugging tokenization results:");
    
    let test_cases = vec![
        "gelmiştim",
        "  ",
        " ",
        "",
        "evler",
        "kitaplarımızdan",
    ];
    
    for case in test_cases {
        println!("\nInput: '{}'", case);
        let tokens = tokenizer.tokenize(case);
        println!("Tokens: {:?}", tokens);
        let detailed = tokenizer.tokenize_text(case);
        for (i, token) in detailed.iter().enumerate() {
            println!("  {}: '{}' (ID: {}, Type: {:?})", i, token.token, token.id, token.token_type);
        }
    }
    
    Ok(())
}
