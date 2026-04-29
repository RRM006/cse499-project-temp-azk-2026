#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NER Data Converter for Phase 2
Converts BIO format annotations to Hugging Face format
"""

import os
import json
import glob
import csv
from typing import List, Dict, Any, Tuple
from tqdm import tqdm


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


def parse_bio_file(filepath: str) -> Tuple[List[str], List[str]]:
    """
    Parse a BIO format annotation file.
    
    Args:
        filepath: Path to BIO file
    
    Returns:
        Tuple of (tokens, labels)
    """
    tokens = []
    labels = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            parts = line.split('\t')
            if len(parts) == 2:
                token, label = parts
                tokens.append(token)
                labels.append(label)
            elif len(parts) == 1:
                # Just token, no label
                tokens.append(parts[0])
                labels.append("O")
    
    return tokens, labels


def convert_bio_to_hf(
    bio_dir: str,
    output_path: str,
    split_name: str = "train"
) -> List[Dict]:
    """
    Convert BIO format to Hugging Face dataset format.
    
    Args:
        bio_dir: Directory containing BIO files
        output_path: Path to save JSON
        split_name: Name of the split
    
    Returns:
        List of data samples
    """
    data = []
    
    # Find all BIO files
    bio_files = glob.glob(os.path.join(bio_dir, "**", "*.txt"), recursive=True)
    
    print(f"Found {len(bio_files)} BIO files in {bio_dir}")
    
    for bio_file in tqdm(bio_files, desc="Converting"):
        tokens, labels = parse_bio_file(bio_file)
        
        if not tokens:
            continue
        
        # Convert labels to IDs
        label_ids = [LABEL2ID.get(label, 0) for label in labels]
        
        data.append({
            "tokens": tokens,
            "labels": labels,
            "label_ids": label_ids,
            "filename": os.path.basename(bio_file)
        })
    
    # Save
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Saved {len(data)} samples to {output_path}")
    
    return data


def create_label_mapping(output_path: str = None) -> Dict:
    """Create label mapping."""
    mapping = {
        "labels": NER_LABELS,
        "label2id": LABEL2ID,
        "id2label": ID2LABEL,
        "num_labels": len(NER_LABELS)
    }
    
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(mapping, f, ensure_ascii=False, indent=2)
    
    return mapping


def load_ner_dataset(json_path: str) -> List[Dict]:
    """Load NER dataset from JSON."""
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def create_train_val_test_split(
    data: List[Dict],
    train_ratio: float = 0.8,
    val_ratio: float = 0.1,
    test_ratio: float = 0.1,
    seed: int = 42
) -> Tuple[List[Dict], List[Dict], List[Dict]]:
    """
    Create train/val/test split.
    
    Args:
        data: List of data samples
        train_ratio: Training ratio
        val_ratio: Validation ratio
        test_ratio: Test ratio
        seed: Random seed
    
    Returns:
        Tuple of (train, val, test)
    """
    import random
    random.seed(seed)
    
    # Shuffle
    data = data.copy()
    random.shuffle(data)
    
    n = len(data)
    n_train = int(n * train_ratio)
    n_val = int(n * val_ratio)
    
    train = data[:n_train]
    val = data[n_train:n_train + n_val]
    test = data[n_train + n_val:]
    
    return train, val, test


def convert_directory(
    input_dir: str,
    output_dir: str,
    train_ratio: float = 0.8,
    val_ratio: float = 0.1,
    test_ratio: float = 0.1
):
    """
    Convert all BIO files in directory to train/val/test splits.
    
    Args:
        input_dir: Input directory with BIO files
        output_dir: Output directory
        train_ratio: Training ratio
        val_ratio: Validation ratio
        test_ratio: Test ratio
    """
    # Collect all data
    all_data = []
    
    bio_files = glob.glob(os.path.join(input_dir, "**", "*.txt"), recursive=True)
    
    for bio_file in tqdm(bio_files, desc="Reading files"):
        tokens, labels = parse_bio_file(bio_file)
        
        if not tokens:
            continue
        
        label_ids = [LABEL2ID.get(label, 0) for label in labels]
        
        all_data.append({
            "tokens": tokens,
            "labels": labels,
            "label_ids": label_ids,
            "filename": os.path.basename(bio_file)
        })
    
    # Split
    train, val, test = create_train_val_test_split(
        all_data, train_ratio, val_ratio, test_ratio
    )
    
    print(f"\nSplit sizes:")
    print(f"  Train: {len(train)}")
    print(f"  Val: {len(val)}")
    print(f"  Test: {len(test)}")
    
    # Save
    os.makedirs(output_dir, exist_ok=True)
    
    with open(os.path.join(output_dir, "train.json"), 'w', encoding='utf-8') as f:
        json.dump(train, f, ensure_ascii=False, indent=2)
    
    with open(os.path.join(output_dir, "validation.json"), 'w', encoding='utf-8') as f:
        json.dump(val, f, ensure_ascii=False, indent=2)
    
    with open(os.path.join(output_dir, "test.json"), 'w', encoding='utf-8') as f:
        json.dump(test, f, ensure_ascii=False, indent=2)
    
    # Save label mapping
    create_label_mapping(os.path.join(output_dir, "label_mapping.json"))
    
    print(f"\nSaved to {output_dir}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Convert NER annotations")
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--train-ratio", type=float, default=0.8)
    parser.add_argument("--val-ratio", type=float, default=0.1)
    parser.add_argument("--test-ratio", type=float, default=0.1)
    
    args = parser.parse_args()
    
    convert_directory(
        args.input_dir,
        args.output_dir,
        args.train_ratio,
        args.val_ratio,
        args.test_ratio
    )
