use criterion::{black_box, criterion_group, criterion_main, Criterion};
use turkish_tokenizer::TurkishTokenizer;

fn tokenizer_benchmark(c: &mut Criterion) {
    let tokenizer = TurkishTokenizer::new_rust().unwrap();
    
    let test_texts = vec![
        "merhaba dünya",
        "Türkçe tokenizer performans testi",
        "merhabaDünyaTokenizerPerformansTestiÇokUzunKelimelerle",
        "Bu bir test cümlesidir ve tokenizer performansını ölçmek için kullanılır.",
    ];
    
    c.bench_function("encode_short_text", |b| {
        b.iter(|| tokenizer.encode(black_box("merhaba dünya")))
    });
    
    c.bench_function("encode_medium_text", |b| {
        b.iter(|| {
            tokenizer.encode(black_box("Türkçe tokenizer performans testi çok önemlidir"))
        })
    });
    
    c.bench_function("tokenize_various_texts", |b| {
        b.iter(|| {
            for text in &test_texts {
                tokenizer.tokenize(black_box(text));
            }
        })
    });
}

criterion_group!(benches, tokenizer_benchmark);
criterion_main!(benches);
