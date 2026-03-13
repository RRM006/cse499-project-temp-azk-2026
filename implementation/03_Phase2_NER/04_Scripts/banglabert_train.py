#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BanglaBERT NER Training Script
Fine-tunes BanglaBERT for medical NER
"""

import os
import json
import torch
import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from tqdm import tqdm

from transformers import (
    AutoTokenizer,
    AutoModelForTokenClassification,
    TrainingArguments,
    Trainer,
    DataCollatorForTokenClassification,
    EvalPrediction
)
from datasets import Dataset
import seqeval.metrics as seqeval_metrics


NER_LABELS = [
    "O",
    "B-SYMPTOM", "I-SYMPTOM",
    "B-DISEASE", "I-DISEASE",
    "B-MEDICATION", "I-MEDICATION",
    "B-DURATION", "I-DURATION",
    "B-ALLERGY", "I-ALLERGY",
    "B-BODY_PART", "I-BODY_PART",
    "B-TREATMENT", "I-TREATMENT",
    "B-DOSAGE", "I-DOSAGE"
]

LABEL2ID = {label: i for i, label in enumerate(NER_LABELS)}
ID2LABEL = {i: label for i, label in enumerate(NER_LABELS)}


def load_ner_data(json_path: str) -> List[Dict]:
    """Load NER data from JSON."""
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def tokenize_and_align_labels(examples, tokenizer, label2id, max_length=512):
    """
    Tokenize and align labels with tokenized input.
    
    Args:
        examples: Batch of examples
        tokenizer: Tokenizer
        label2id: Label to ID mapping
        max_length: Maximum sequence length
    
    Returns:
        Tokenized inputs with labels
    """
    # Tokenize
    tokenized = tokenizer(
        examples["tokens"],
        truncation=True,
        max_length=max_length,
        is_split_into_words=True,
        padding="max_length"
    )
    
    # Align labels
    labels = []
    for i, label in enumerate(examples["labels"]):
        word_ids = tokenized.word_ids(i)
        
        # Map labels to tokens
        label_ids = []
        previous_word_idx = None
        
        for word_idx in word_ids:
            if word_idx is None:
                # Special token
                label_ids.append(-100)
            elif word_idx != previous_word_idx:
                # First token of word
                label_ids.append(label2id.get(label[word_idx], 0))
            else:
                # Subsequent token of word
                label_ids.append(-100)
            previous_word_idx = word_idx
        
        labels.append(label_ids)
    
    tokenized["labels"] = labels
    
    return tokenized


def prepare_dataset(data, tokenizer, label2id, max_length=512):
    """
    Prepare dataset for training.
    
    Args:
        data: List of data samples
        tokenizer: Tokenizer
        label2id: Label mapping
        max_length: Maximum length
    
    Returns:
        Hugging Face Dataset
    """
    # Create dataset
    dataset = Dataset.from_list(data)
    
    # Tokenize
    def tokenize(examples):
        return tokenize_and_align_labels(examples, tokenizer, label2id, max_length)
    
    dataset = dataset.map(
        tokenize,
        batched=True,
        remove_columns=["tokens", "labels", "filename"],
        desc="Tokenizing"
    )
    
    return dataset


def compute_metrics_seqeval(p: EvalPrediction) -> Dict[str, float]:
    """
    Compute metrics using seqeval.
    
    Args:
        p: Prediction object
    
    Returns:
        Metrics dictionary
    """
    predictions, labels = p.predictions, p.label_ids
    
    # Get predicted labels
    predictions = np.argmax(predictions, axis=2)
    
    # Remove padding
    true_predictions = []
    true_labels = []
    
    for pred, label in zip(predictions, labels):
        pred_seq = []
        label_seq = []
        
        for p, l in zip(pred, label):
            if l != -100:
                pred_seq.append(ID2LABEL[p])
                label_seq.append(ID2LABEL[l])
        
        true_predictions.append(pred_seq)
        true_labels.append(label_seq)
    
    # Compute metrics
    precision = seqeval_metrics.precision_score(true_labels, true_predictions)
    recall = seqeval_metrics.recall_score(true_labels, true_predictions)
    f1 = seqeval_metrics.f1_score(true_labels, true_predictions)
    
    return {
        "precision": precision,
        "recall": recall,
        "f1": f1
    }


def train_ner_model(
    model_name: str = "csebuetnlp/banglabert",
    train_data: List[Dict] = None,
    eval_data: List[Dict] = None,
    output_dir: str = "./ner_output",
    num_train_epochs: int = 10,
    per_device_train_batch_size: int = 16,
    per_device_eval_batch_size: int = 16,
    learning_rate: float = 2e-5,
    max_length: int = 512,
    warmup_steps: int = 500,
    weight_decay: float = 0.01,
    logging_steps: int = 100,
    save_strategy: str = "epoch",
    evaluation_strategy: str = "epoch",
    **kwargs
) -> Trainer:
    """
    Train NER model.
    
    Args:
        model_name: Model name or path
        train_data: Training data
        eval_data: Evaluation data
        output_dir: Output directory
        num_train_epochs: Number of epochs
        per_device_train_batch_size: Training batch size
        per_device_eval_batch_size: Evaluation batch size
        learning_rate: Learning rate
        max_length: Maximum sequence length
        warmup_steps: Warmup steps
        weight_decay: Weight decay
        logging_steps: Logging frequency
        save_strategy: Saving strategy
        evaluation_strategy: Evaluation strategy
    
    Returns:
        Trainer object
    """
    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    # Prepare datasets
    train_dataset = prepare_dataset(train_data, tokenizer, LABEL2ID, max_length)
    eval_dataset = prepare_dataset(eval_data, tokenizer, LABEL2ID, max_length)
    
    # Load model
    model = AutoModelForTokenClassification.from_pretrained(
        model_name,
        num_labels=len(NER_LABELS),
        id2label=ID2LABEL,
        label2id=LABEL2ID
    )
    
    # Data collator
    data_collator = DataCollatorForTokenClassification(
        tokenizer=tokenizer,
        padding=True
    )
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=num_train_epochs,
        per_device_train_batch_size=per_device_train_batch_size,
        per_device_eval_batch_size=per_device_eval_batch_size,
        learning_rate=learning_rate,
        warmup_steps=warmup_steps,
        weight_decay=weight_decay,
        logging_steps=logging_steps,
        save_strategy=save_strategy,
        evaluation_strategy=evaluation_strategy,
        load_best_model_at_end=True,
        metric_for_best_model="f1",
        greater_is_better=True,
        **kwargs
    )
    
    # Create trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        tokenizer=tokenizer,
        data_collator=data_collator,
        compute_metrics=compute_metrics_seqeval
    )
    
    return trainer


def extract_entities_from_predictions(
    tokens: List[str],
    predictions: List[str]
) -> List[Dict[str, Any]]:
    """
    Extract entities from model predictions.
    
    Args:
        tokens: List of tokens
        predictions: List of predicted labels
    
    Returns:
        List of extracted entities
    """
    entities = []
    current_entity = None
    current_type = None
    current_start = None
    
    for i, (token, label) in enumerate(zip(tokens, predictions)):
        if label.startswith("B-"):
            # Save previous entity
            if current_entity is not None:
                entities.append({
                    "text": current_entity,
                    "type": current_type,
                    "start": current_start,
                    "end": i
                })
            
            # Start new entity
            current_entity = token
            current_type = label[2:]
            current_start = i
        
        elif label.startswith("I-") and current_entity is not None:
            entity_type = label[2:]
            if entity_type == current_type:
                # Continue entity
                current_entity += " " + token
            else:
                # Save previous, start new
                entities.append({
                    "text": current_entity,
                    "type": current_type,
                    "start": current_start,
                    "end": i
                })
                current_entity = token
                current_type = entity_type
                current_start = i
        else:
            # Save previous entity
            if current_entity is not None:
                entities.append({
                    "text": current_entity,
                    "type": current_type,
                    "start": current_start,
                    "end": i
                })
                current_entity = None
                current_type = None
                current_start = None
    
    # Save last entity
    if current_entity is not None:
        entities.append({
            "text": current_entity,
            "type": current_type,
            "start": current_start,
            "end": len(tokens)
        })
    
    return entities


def predict_ner(
    model_path: str,
    text: str,
    model_name: str = "csebuetnlp/banglabert"
) -> List[Dict[str, Any]]:
    """
    Predict NER entities for text.
    
    Args:
        model_path: Path to trained model
        text: Input text
        model_name: Base model name for tokenizer
    
    Returns:
        List of extracted entities
    """
    import torch
    
    # Load tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForTokenClassification.from_pretrained(model_path)
    model.eval()
    
    # Tokenize
    tokens = text.split()
    inputs = tokenizer(
        tokens,
        is_split_into_words=True,
        return_tensors="pt",
        padding=True,
        truncation=True
    )
    
    # Predict
    with torch.no_grad():
        outputs = model(**inputs)
        predictions = torch.argmax(outputs.logits, dim=-1)[0].tolist()
    
    # Map predictions to labels
    word_ids = inputs.word_ids()
    pred_labels = []
    
    for i, word_id in enumerate(word_ids):
        if word_id is not None:
            pred_labels.append(ID2LABEL[predictions[i]])
        else:
            pred_labels.append("O")
    
    # Extract entities
    entities = extract_entities_from_predictions(tokens, pred_labels)
    
    return entities


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Train BanglaBERT NER")
    parser.add_argument("--model", default="csebuetnlp/banglabert")
    parser.add_argument("--train-data", required=True)
    parser.add_argument("--eval-data", required=True)
    parser.add_argument("--output-dir", default="./ner_output")
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--learning-rate", type=float, default=2e-5)
    
    args = parser.parse_args()
    
    print("This script should be run in Google Colab with GPU")
    print(f"Model: {args.model}")
    print(f"Output: {args.output_dir}")
