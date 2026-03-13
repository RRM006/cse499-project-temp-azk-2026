#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utility Functions for CSE499 Project
Common utility functions used across all phases
"""

import os
import json
import csv
import random
import hashlib
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple


def get_timestamp() -> str:
    """Get current timestamp as string."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def generate_patient_id() -> str:
    """Generate a unique patient ID."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_suffix = str(random.randint(1000, 9999))
    return f"PAT_{timestamp}_{random_suffix}"


def generate_session_id() -> str:
    """Generate a unique session ID."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"SESSION_{timestamp}"


def calculate_cer(reference: str, hypothesis: str) -> float:
    """
    Calculate Character Error Rate (CER).
    
    Args:
        reference: Reference text
        hypothesis: Hypothesis text
    
    Returns:
        float: CER score (0 = perfect, higher is worse)
    """
    try:
        from jiwer import cer
        return cer(reference, hypothesis)
    except ImportError:
        # Fallback implementation
        ref_chars = list(reference)
        hyp_chars = list(hypothesis)
        
        # Simple Levenshtein at character level
        d = [[0] * (len(hyp_chars) + 1) for _ in range(len(ref_chars) + 1)]
        
        for i in range(len(ref_chars) + 1):
            d[i][0] = i
        for j in range(len(hyp_chars) + 1):
            d[0][j] = j
            
        for i in range(1, len(ref_chars) + 1):
            for j in range(1, len(hyp_chars) + 1):
                if ref_chars[i-1] == hyp_chars[j-1]:
                    d[i][j] = d[i-1][j-1]
                else:
                    d[i][j] = min(d[i-1][j], d[i][j-1], d[i-1][j-1]) + 1
        
        return d[len(ref_chars)][len(hyp_chars)] / max(len(ref_chars), 1)


def calculate_wer(reference: str, hypothesis: str) -> float:
    """
    Calculate Word Error Rate (WER).
    
    Args:
        reference: Reference text
        hypothesis: Hypothesis text
    
    Returns:
        float: WER score (0 = perfect, higher is worse)
    """
    try:
        from jiwer import wer
        return wer(reference, hypothesis)
    except ImportError:
        # Fallback - split by spaces
        ref_words = reference.split()
        hyp_words = hypothesis.split()
        
        if len(ref_words) == 0:
            return 0.0 if len(hyp_words) == 0 else 1.0
        
        # Simple word-level edit distance
        d = [[0] * (len(hyp_words) + 1) for _ in range(len(ref_words) + 1)]
        
        for i in range(len(ref_words) + 1):
            d[i][0] = i
        for j in range(len(hyp_words) + 1):
            d[0][j] = j
            
        for i in range(1, len(ref_words) + 1):
            for j in range(1, len(hyp_words) + 1):
                if ref_words[i-1] == hyp_words[j-1]:
                    d[i][j] = d[i-1][j-1]
                else:
                    d[i][j] = min(d[i-1][j], d[i][j-1], d[i-1][j-1]) + 1
        
        return d[len(ref_words)][len(hyp_words)] / len(ref_words)


def load_json(filepath: str) -> Any:
    """Load JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data: Any, filepath: str, indent: int = 2) -> None:
    """Save data to JSON file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)


def load_csv(filepath: str) -> List[Dict]:
    """Load CSV file as list of dictionaries."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def save_csv(data: List[Dict], filepath: str) -> None:
    """Save data to CSV file."""
    if not data:
        return
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


def ensure_dir(directory: str) -> None:
    """Ensure directory exists."""
    os.makedirs(directory, exist_ok=True)


def list_files(directory: str, extension: Optional[str] = None) -> List[str]:
    """
    List files in directory.
    
    Args:
        directory: Directory path
        extension: File extension filter (e.g., '.wav')
    
    Returns:
        List of file paths
    """
    if not os.path.exists(directory):
        return []
    
    files = []
    for item in os.listdir(directory):
        path = os.path.join(directory, item)
        if os.path.isfile(path):
            if extension is None or item.endswith(extension):
                files.append(path)
    return sorted(files)


def get_file_hash(filepath: str) -> str:
    """Get MD5 hash of a file."""
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def get_audio_duration(filepath: str) -> float:
    """
    Get duration of audio file in seconds.
    
    Args:
        filepath: Path to audio file
    
    Returns:
        Duration in seconds
    """
    try:
        import librosa
        info = librosa.load(filepath, sr=None)
        return len(info[0]) / info[1]
    except Exception as e:
        print(f"Error getting duration: {e}")
        return 0.0


def create_log_entry(action: str, details: Dict[str, Any]) -> Dict:
    """Create a standardized log entry."""
    return {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "details": details
    }


def append_log(log_file: str, action: str, details: Dict[str, Any]) -> None:
    """Append entry to log file."""
    entry = create_log_entry(action, details)
    logs = []
    if os.path.exists(log_file):
        logs = load_json(log_file)
    logs.append(entry)
    save_json(logs, log_file)


def format_bengali_number(num: int) -> str:
    """Convert number to Bengali numerals."""
    bengali_digits = ['০', '১', '২', '৩', '৪', '৫', '৬', '৭', '৮', '৯']
    return ''.join([bengali_digits[int(d)] for d in str(num)])


def normalize_bengali_text(text: str) -> str:
    """Normalize Bengali text."""
    # Remove extra whitespace
    text = ' '.join(text.split())
    # Remove common transcription artifacts
    text = text.replace('[unclear]', '')
    text = text.replace('[]', '')
    return text.strip()


def split_train_val_test(
    items: List[Any],
    train_ratio: float = 0.8,
    val_ratio: float = 0.1,
    test_ratio: float = 0.1,
    shuffle: bool = True,
    seed: int = 42
) -> Tuple[List[Any], List[Any], List[Any]]:
    """
    Split items into train/val/test sets.
    
    Args:
        items: List of items to split
        train_ratio: Ratio for training set
        val_ratio: Ratio for validation set
        test_ratio: Ratio for test set
        shuffle: Whether to shuffle before splitting
        seed: Random seed
    
    Returns:
        Tuple of (train, val, test) lists
    """
    assert abs(train_ratio + val_ratio + test_ratio - 1.0) < 0.001, \
        "Ratios must sum to 1.0"
    
    items = items.copy()
    if shuffle:
        random.seed(seed)
        random.shuffle(items)
    
    n = len(items)
    n_train = int(n * train_ratio)
    n_val = int(n * val_ratio)
    
    train = items[:n_train]
    val = items[n_train:n_train + n_val]
    test = items[n_train + n_val:]
    
    return train, val, test


def stratified_split_by_dialect(
    data: List[Dict],
    dialect_key: str = "dialect",
    train_ratio: float = 0.8,
    val_ratio: float = 0.1,
    test_ratio: float = 0.1,
    seed: int = 42
) -> Tuple[List[Dict], List[Dict], List[Dict]]:
    """
    Stratified split by dialect to ensure equal representation.
    
    Args:
        data: List of data items with dialect key
        dialect_key: Key containing dialect information
        train_ratio: Ratio for training set
        val_ratio: Ratio for validation set
        test_ratio: Ratio for test set
        seed: Random seed
    
    Returns:
        Tuple of (train, val, test) lists
    """
    # Group by dialect
    dialect_groups = {}
    for item in data:
        dialect = item.get(dialect_key, "unknown")
        if dialect not in dialect_groups:
            dialect_groups[dialect] = []
        dialect_groups[dialect].append(item)
    
    # Split each group
    train, val, test = [], [], []
    
    for dialect, items in dialect_groups.items():
        t, v, s = split_train_val_test(
            items, train_ratio, val_ratio, test_ratio, seed=seed
        )
        train.extend(t)
        val.extend(v)
        test.extend(s)
    
    return train, val, test


class ProgressTracker:
    """Track progress of tasks."""
    
    def __init__(self, total: int, description: str = "Processing"):
        self.total = total
        self.current = 0
        self.description = description
    
    def update(self, n: int = 1) -> None:
        self.current += n
        percent = (self.current / self.total) * 100
        print(f"\r{self.description}: {self.current}/{self.total} ({percent:.1f}%)", end="")
    
    def finish(self) -> None:
        print()


class DatasetStatistics:
    """Calculate and store dataset statistics."""
    
    def __init__(self):
        self.stats = {}
    
    def add(self, key: str, value: Any) -> None:
        self.stats[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        return self.stats.get(key, default)
    
    def summary(self) -> Dict:
        return self.stats
    
    def save(self, filepath: str) -> None:
        save_json(self.stats, filepath)
    
    def load(self, filepath: str) -> None:
        self.stats = load_json(filepath)
