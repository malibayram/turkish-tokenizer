#!/usr/bin/env python3
"""
Integration example showing how to use the Turkish tokenizer with Hugging Face models.

This example demonstrates:
1. Using the tokenizer with a pre-trained model
2. Preparing data for training
3. Using with Hugging Face datasets
4. Integration with training pipelines
"""

import os
import sys

# Add the parent directory to the path to import the tokenizer
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import torch
from datasets import Dataset
from transformers import AutoModelForCausalLM, Trainer, TrainingArguments

from turkish_tokenizer import HFTurkishTokenizer


def basic_model_integration():
    """Demonstrate basic integration with a Hugging Face model."""
    print("=== Basic Model Integration ===")
    
    # Initialize tokenizer
    tokenizer = HFTurkishTokenizer()
    
    # Sample Turkish text
    text = "Merhaba dünya! Bu bir test cümlesidir."
    
    # Prepare inputs for a model
    inputs = tokenizer(
        text,
        add_special_tokens=True,
        padding=True,
        truncation=True,
        max_length=512,
        return_tensors="pt"
    )
    
    print(f"Input shape: {inputs['input_ids'].shape}")
    print(f"Attention mask shape: {inputs['attention_mask'].shape}")
    print(f"Input IDs: {inputs['input_ids'][:10].tolist()}...")  # Show first 10 tokens
    
    # Note: In a real scenario, you would load a model here
    # model = AutoModelForCausalLM.from_pretrained("gpt2")
    # outputs = model(**inputs)
    
    print()


def dataset_preparation():
    """Demonstrate preparing a dataset for training."""
    print("=== Dataset Preparation ===")
    
    # Initialize tokenizer
    tokenizer = HFTurkishTokenizer()
    
    # Sample Turkish texts
    texts = [
        "Merhaba dünya!",
        "Bu bir test cümlesidir.",
        "Türkçe dil işleme örneği.",
        "Yapay zeka teknolojileri gelişiyor.",
        "Doğal dil işleme alanında çalışıyoruz."
    ]
    
    # Create a simple dataset
    dataset_dict = {"text": texts}
    dataset = Dataset.from_dict(dataset_dict)
    
    print(f"Dataset size: {len(dataset)}")
    print(f"Sample text: {dataset[0]['text']}")
    
    # Tokenize the dataset
    def tokenize_function(examples):
        return tokenizer(
            examples["text"],
            padding=True,
            truncation=True,
            max_length=128,
            return_tensors=None  # Return lists, not tensors
        )
    
    tokenized_dataset = dataset.map(tokenize_function, batched=True)
    
    print(f"Tokenized dataset features: {tokenized_dataset.features}")
    print(f"Sample input_ids: {tokenized_dataset[0]['input_ids'][:10]}...")
    
    print()


def training_pipeline_example():
    """Demonstrate a training pipeline setup."""
    print("=== Training Pipeline Example ===")
    
    # Initialize tokenizer
    tokenizer = HFTurkishTokenizer()
    
    # Sample training data
    training_texts = [
        "Merhaba dünya!",
        "Bu bir test cümlesidir.",
        "Türkçe dil işleme örneği.",
        "Yapay zeka teknolojileri gelişiyor.",
        "Doğal dil işleme alanında çalışıyoruz."
    ]
    
    # Create dataset
    dataset_dict = {"text": training_texts}
    dataset = Dataset.from_dict(dataset_dict)
    
    # Tokenize dataset
    def tokenize_function(examples):
        return tokenizer(
            examples["text"],
            padding=True,
            truncation=True,
            max_length=128,
            return_tensors=None
        )
    
    tokenized_dataset = dataset.map(tokenize_function, batched=True)
    
    # Data collator function
    def data_collator(features):
        batch = {}
        batch['input_ids'] = torch.tensor([f['input_ids'] for f in features])
        batch['attention_mask'] = torch.tensor([f['attention_mask'] for f in features])
        return batch
    
    # Training arguments (example)
    training_args = TrainingArguments(
        output_dir="./turkish_model_output",
        per_device_train_batch_size=2,
        num_train_epochs=1,
        save_steps=100,
        save_total_limit=2,
        logging_steps=10,
        learning_rate=5e-5,
        warmup_steps=100,
        logging_dir="./logs",
    )
    
    print(f"Training arguments configured:")
    print(f"  - Output directory: {training_args.output_dir}")
    print(f"  - Batch size: {training_args.per_device_train_batch_size}")
    print(f"  - Epochs: {training_args.num_train_epochs}")
    print(f"  - Learning rate: {training_args.learning_rate}")
    
    # Note: In a real scenario, you would initialize a model here
    # model = AutoModelForCausalLM.from_pretrained("gpt2")
    # model.resize_token_embeddings(len(tokenizer))
    
    # And create a trainer
    # trainer = Trainer(
    #     model=model,
    #     args=training_args,
    #     train_dataset=tokenized_dataset,
    #     data_collator=data_collator,
    # )
    
    # trainer.train()
    
    print()


def custom_special_tokens_example():
    """Demonstrate using custom special tokens."""
    print("=== Custom Special Tokens Example ===")
    
    # Initialize tokenizer with custom special tokens
    tokenizer = HFTurkishTokenizer(
        bos_token="<s>",
        eos_token="</s>",
        sep_token="<sep>",
        cls_token="<cls>",
        mask_token="<mask>",
        pad_token="<pad>",
        unk_token="<unk>",
        model_max_length=512
    )
    
    # Sample text
    text = "Bu bir test cümlesidir."
    
    # Encode with special tokens
    encoded = tokenizer.encode(text, add_special_tokens=True)
    print(f"Encoded with special tokens: {encoded}")
    
    # Decode with special tokens
    decoded_with_special = tokenizer.decode(encoded, skip_special_tokens=False)
    print(f"Decoded with special tokens: {decoded_with_special}")
    
    # Decode without special tokens
    decoded_without_special = tokenizer.decode(encoded, skip_special_tokens=True)
    print(f"Decoded without special tokens: {decoded_without_special}")
    
    print()


def batch_processing_example():
    """Demonstrate batch processing capabilities."""
    print("=== Batch Processing Example ===")
    
    # Initialize tokenizer
    tokenizer = HFTurkishTokenizer()
    
    # Batch of texts
    texts = [
        "Merhaba dünya!",
        "Bu bir test cümlesidir.",
        "Türkçe dil işleme örneği.",
        "Yapay zeka teknolojileri gelişiyor."
    ]
    
    # Process batch
    batch_inputs = tokenizer(
        texts,
        add_special_tokens=True,
        padding=True,
        truncation=True,
        max_length=128,
        return_tensors="pt"
    )
    
    print(f"Batch input shape: {batch_inputs['input_ids'].shape}")
    print(f"Batch attention mask shape: {batch_inputs['attention_mask'].shape}")
    
    # Show first few tokens of each sequence
    for i, text in enumerate(texts):
        tokens = batch_inputs['input_ids'][i][:10]  # First 10 tokens
        print(f"  {i+1}. {text[:30]}... -> {tokens.tolist()}")
    
    print()


def vocabulary_analysis():
    """Demonstrate vocabulary analysis capabilities."""
    print("=== Vocabulary Analysis ===")
    
    # Initialize tokenizer
    tokenizer = HFTurkishTokenizer()
    
    print(f"Vocabulary size: {tokenizer.vocab_size}")
    
    # Get vocabulary
    vocab = tokenizer.get_vocab()
    
    # Show some sample tokens
    sample_tokens = list(vocab.keys())[:20]
    print(f"Sample vocabulary tokens: {sample_tokens}")
    
    # Test some Turkish words
    turkish_words = ["merhaba", "dünya", "test", "cümle", "dil", "işleme"]
    
    print("\nTurkish word analysis:")
    for word in turkish_words:
        if word in vocab:
            token_id = vocab[word]
            print(f"  '{word}' -> ID: {token_id}")
        else:
            print(f"  '{word}' -> Not in vocabulary")
    
    print()


def main():
    """Run all integration examples."""
    print("Turkish Tokenizer - Hugging Face Integration Examples")
    print("=" * 60)
    print()
    
    try:
        basic_model_integration()
        dataset_preparation()
        training_pipeline_example()
        custom_special_tokens_example()
        batch_processing_example()
        vocabulary_analysis()
        
        print("All integration examples completed successfully!")
        print("\nNote: This example demonstrates the setup and configuration.")
        print("In a real scenario, you would need to:")
        print("1. Load an appropriate pre-trained model")
        print("2. Resize the model's token embeddings to match the tokenizer vocabulary")
        print("3. Prepare your training data")
        print("4. Run the actual training")
        
    except Exception as e:
        print(f"Error running integration examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
