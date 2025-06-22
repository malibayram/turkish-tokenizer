use clap::Parser;
use indicatif::{ProgressBar, ProgressStyle};
use rayon::prelude::*;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs;
use std::time::Instant;
use anyhow::{Result, Context};

#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Path to the Turkish vocabulary JSON file
    #[arg(short, long)]
    turkish_vocab: String,

    /// Path to the Qwen tokenizer vocabulary JSON file
    #[arg(short, long)]
    qwen_vocab: String,

    /// Output file for matched vocabulary
    #[arg(short, long, default_value = "matched_vocab.json")]
    output: String,

    /// Number of threads to use (default: number of CPU cores)
    #[arg(short, long)]
    threads: Option<usize>,
}

#[derive(Debug, Serialize, Deserialize)]
struct MatchResult {
    matched: HashMap<String, u32>,
    not_matched: Vec<String>,
    stats: MatchStats,
}

#[derive(Debug, Serialize, Deserialize)]
struct MatchStats {
    total_words: usize,
    matched_count: usize,
    not_matched_count: usize,
    match_rate: f64,
    processing_time_ms: u128,
    words_per_second: f64,
}

fn main() -> Result<()> {
    let args = Args::parse();
    
    println!("🚀 Starting ultra-fast vocabulary matching with Rust...");
    
    // Set number of threads
    if let Some(threads) = args.threads {
        rayon::ThreadPoolBuilder::new()
            .num_threads(threads)
            .build_global()
            .context("Failed to set thread count")?;
    }
    
    let start_time = Instant::now();
    
    // Load Turkish vocabulary
    println!("📖 Loading Turkish vocabulary from {}...", args.turkish_vocab);
    let turkish_vocab: HashMap<String, u32> = serde_json::from_str(
        &fs::read_to_string(&args.turkish_vocab)
            .context("Failed to read Turkish vocabulary file")?
    ).context("Failed to parse Turkish vocabulary JSON")?;
    
    // Load Qwen vocabulary
    println!("📖 Loading Qwen vocabulary from {}...", args.qwen_vocab);
    let qwen_vocab: HashMap<String, u32> = serde_json::from_str(
        &fs::read_to_string(&args.qwen_vocab)
            .context("Failed to read Qwen vocabulary file")?
    ).context("Failed to parse Qwen vocabulary JSON")?;
    
    println!("📊 Processing {} Turkish words against {} Qwen tokens...", 
             turkish_vocab.len(), qwen_vocab.len());
    
    // Convert Qwen vocab to HashSet<&str> for O(1) lookup
    let qwen_vocab_set: std::collections::HashSet<&str> = qwen_vocab.keys().map(|k| k.as_str()).collect();
    
    // Create progress bar
    let pb = ProgressBar::new(turkish_vocab.len() as u64);
    pb.set_style(
        ProgressStyle::default_bar()
            .template("{spinner:.green} [{elapsed_precise}] [{bar:40.cyan/blue}] {pos}/{len} ({eta})")
            .unwrap()
            .progress_chars("#>-")
    );
    
    // Process vocabulary matching
    let (matched, not_matched) = process_vocabulary(&turkish_vocab, &qwen_vocab_set, &qwen_vocab, &pb);
    
    let elapsed = start_time.elapsed();
    let words_per_second = turkish_vocab.len() as f64 / elapsed.as_secs_f64();
    
    // Create result
    let result = MatchResult {
        matched: matched.clone(),
        not_matched: not_matched.clone(),
        stats: MatchStats {
            total_words: turkish_vocab.len(),
            matched_count: matched.len(),
            not_matched_count: not_matched.len(),
            match_rate: (matched.len() as f64 / turkish_vocab.len() as f64) * 100.0,
            processing_time_ms: elapsed.as_millis(),
            words_per_second,
        },
    };
    
    // Save results
    println!("💾 Saving results to {}...", args.output);
    fs::write(
        &args.output,
        serde_json::to_string_pretty(&result).context("Failed to serialize results")?
    ).context("Failed to write output file")?;
    
    // Print summary
    println!("\n✅ Processing completed!");
    println!("📊 Results:");
    println!("   • Total words: {}", result.stats.total_words);
    println!("   • Matched: {}", result.stats.matched_count);
    println!("   • Not matched: {}", result.stats.not_matched_count);
    println!("   • Match rate: {:.1}%", result.stats.match_rate);
    println!("   • Processing time: {:.2} seconds", elapsed.as_secs_f64());
    println!("   • Speed: {:.0} words/second", result.stats.words_per_second);
    
    Ok(())
}

fn process_vocabulary(
    turkish_vocab: &HashMap<String, u32>,
    qwen_vocab_set: &std::collections::HashSet<&str>,
    qwen_vocab: &HashMap<String, u32>,
    pb: &ProgressBar,
) -> (HashMap<String, u32>, Vec<String>) {
    let mut matched = HashMap::new();
    let mut not_matched = Vec::new();
    
    // Process in parallel chunks for better performance
    let chunk_size = 1000;
    let turkish_items: Vec<_> = turkish_vocab.iter().collect();
    let chunks: Vec<_> = turkish_items.chunks(chunk_size).collect();
    
    let results: Vec<_> = chunks.par_iter().map(|chunk| {
        let mut chunk_matched = HashMap::new();
        let mut chunk_not_matched = Vec::new();
        
        for (word, _) in chunk.iter() {
            let variations = [
                word.to_string(),
                format!("Ġ{}", word),
                format!("Ġ{}", word.chars().next().unwrap_or('a').to_uppercase().chain(word.chars().skip(1)).collect::<String>()),
            ];
            
            let mut found_match = false;
            for variation in variations.iter() {
                if qwen_vocab_set.contains(variation.as_str()) {
                    chunk_matched.insert(variation.clone(), *qwen_vocab.get(variation.as_str()).unwrap());
                    found_match = true;
                    break;
                }
            }
            
            if !found_match {
                chunk_not_matched.push((*word).clone());
            }
        }
        
        (chunk_matched, chunk_not_matched)
    }).collect();
    
    // Combine results
    for (chunk_matched, chunk_not_matched) in results {
        matched.extend(chunk_matched);
        not_matched.extend(chunk_not_matched);
        pb.inc(chunk_size as u64);
    }
    
    (matched, not_matched)
} 