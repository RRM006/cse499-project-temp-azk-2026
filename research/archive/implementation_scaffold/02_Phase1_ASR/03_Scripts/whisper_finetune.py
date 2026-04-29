#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Whisper Fine-tuning Script for Bengali ASR
Fine-tunes OpenAI Whisper model on custom Bengali dataset
"""

import os
import json
import glob
import librosa
import torch
import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from tqdm import tqdm

from transformers import (
    WhisperProcessor,
    WhisperForConditionalGeneration,
    WhisperFeatureExtractor,
    WhisperTokenizer,
    TrainingArguments,
    Trainer,
    EvalPrediction,
    DataCollatorSpeechSeq2SeqWithPadding
)
from datasets import Dataset, load_dataset, Audio


@dataclass
class DataConfig:
    """Configuration for data loading."""
    audio_dir: str
    transcription_dir: str
    train_split: List[str] = None
    val_split: List[str] = None
    test_split: List[str] = None
    sample_rate: int = 16000


class WhisperDataset:
    """Dataset class for Whisper fine-tuning."""
    
    def __init__(
        self,
        audio_dir: str,
        transcription_dir: str,
        split: str = "train",
        sample_rate: int = 16000
    ):
        """
        Initialize dataset.
        
        Args:
            audio_dir: Directory containing audio files
            transcription_dir: Directory containing transcription files
            split: Dataset split (train/val/test)
            sample_rate: Target sample rate
        """
        self.audio_dir = audio_dir
        self.transcription_dir = transcription_dir
        self.split = split
        self.sample_rate = sample_rate
        
        # Load data
        self.data = self._load_data()
    
    def _load_data(self) -> List[Dict]:
        """Load audio-transcription pairs."""
        data = []
        
        # Find all audio files
        audio_files = glob.glob(
            os.path.join(self.audio_dir, "**", "*.wav"),
            recursive=True
        )
        
        for audio_path in tqdm(audio_files, desc=f"Loading {self.split} data"):
            # Get relative path
            rel_path = os.path.relpath(audio_path, self.audio_dir)
            
            # Get transcription file path
            base_name = os.path.splitext(os.path.basename(audio_path))[0]
            trans_path = os.path.join(
                self.transcription_dir,
                os.path.dirname(rel_path),
                f"{base_name}.txt"
            )
            
            # Load transcription if exists
            transcription = ""
            if os.path.exists(trans_path):
                with open(trans_path, 'r', encoding='utf-8') as f:
                    transcription = f.read().strip()
            
            data.append({
                "audio": audio_path,
                "transcription": transcription,
                "dialect": os.path.basename(os.path.dirname(rel_path)),
                "filename": os.path.basename(audio_path)
            })
        
        return data
    
    def __len__(self) -> int:
        return len(self.data)
    
    def __getitem__(self, idx: int) -> Dict:
        """Get item by index."""
        return self.data[idx]


def prepare_dataset_common_voice(
    dataset_name: str = "mozilla-foundation/common_voice",
    config: str = "bn",
    split: str = "train"
) -> Dataset:
    """
    Load Mozilla Common Voice Bengali dataset.
    
    Args:
        dataset_name: Dataset name on Hugging Face
        config: Dataset configuration (language)
        split: Dataset split
    
    Returns:
        Dataset object
    """
    # Load dataset
    dataset = load_dataset(dataset_name, config, split=split)
    
    # Keep relevant columns
    dataset = dataset.select_columns(["audio", "sentence"])
    
    return dataset


def prepare_whisper_dataset(
    dataset: Dataset,
    processor: WhisperProcessor,
    sampling_rate: int = 16000
) -> Dataset:
    """
    Prepare dataset for Whisper training.
    
    Args:
        dataset: Raw dataset
        processor: Whisper processor
        sampling_rate: Target sampling rate
    
    Returns:
        Prepared dataset
    """
    # Cast audio to correct sampling rate
    dataset = dataset.cast_column(
        "audio",
        Audio(sampling_rate=sampling_rate)
    )
    
    def prepare_example(example):
        # Load audio
        audio = example["audio"]["array"]
        
        # Process audio
        input_features = processor(
            audio,
            sampling_rate=sampling_rate,
            return_tensors="pt"
        ).input_features[0]
        
        # Process text
        labels = processor.tokenizer(
            example["transcription"],
            return_tensors="pt"
        ).input_ids[0]
        
        return {
            "input_features": input_features,
            "labels": labels
        }
    
    # Map over dataset
    dataset = dataset.map(
        prepare_example,
        remove_columns=dataset.column_names,
        desc="Preparing dataset"
    )
    
    return dataset


def load_custom_audio_dataset(
    audio_dir: str,
    transcription_dir: str,
    sample_rate: int = 16000
) -> Dataset:
    """
    Load custom audio dataset.
    
    Args:
        audio_dir: Directory containing audio files
        transcription_dir: Directory containing transcription files
        sample_rate: Target sample rate
    
    Returns:
        Hugging Face Dataset
    """
    data = []
    
    # Find all audio files
    audio_files = glob.glob(
        os.path.join(audio_dir, "**", "*.wav"),
        recursive=True
    )
    
    for audio_path in tqdm(audio_files, desc="Loading audio"):
        # Get transcription
        base_name = os.path.splitext(os.path.basename(audio_path))[0]
        
        # Try different directory structures
        rel_path = os.path.relpath(audio_path, audio_dir)
        trans_path = os.path.join(
            transcription_dir,
            f"{base_name}.txt"
        )
        
        # Also try with subdirectory
        if not os.path.exists(trans_path):
            trans_path = os.path.join(
                transcription_dir,
                os.path.dirname(rel_path),
                f"{base_name}.txt"
            )
        
        transcription = ""
        if os.path.exists(trans_path):
            with open(trans_path, 'r', encoding='utf-8') as f:
                transcription = f.read().strip()
        
        data.append({
            "audio": audio_path,
            "transcription": transcription
        })
    
    # Create dataset
    dataset = Dataset.from_list(data)
    
    # Cast audio column
    dataset = dataset.cast_column(
        "audio",
        Audio(sampling_rate=sample_rate)
    )
    
    return dataset


def prepare_custom_dataset(
    dataset: Dataset,
    processor: WhisperProcessor,
    sampling_rate: int = 16000
) -> Dataset:
    """
    Prepare custom dataset for Whisper.
    
    Args:
        dataset: Raw dataset
        processor: Whisper processor
        sampling_rate: Target sampling rate
    
    Returns:
        Prepared dataset
    """
    def prepare_example(example):
        # Audio is already loaded by Audio column
        audio = example["audio"]["array"]
        
        # Process audio
        input_features = processor(
            audio,
            sampling_rate=sampling_rate,
            return_tensors="pt"
        ).input_features[0]
        
        # Process text
        labels = processor.tokenizer(
            example["transcription"],
            return_tensors="pt"
        ).input_ids[0]
        
        return {
            "input_features": input_features,
            "labels": labels
        }
    
    # Map over dataset
    dataset = dataset.map(
        prepare_example,
        remove_columns=["audio"],
        desc="Preparing dataset"
    )
    
    return dataset


def train_whisper(
    model_name: str = "openai/whisper-small",
    train_dataset: Dataset = None,
    eval_dataset: Dataset = None,
    output_dir: str = "./whisper_output",
    learning_rate: float = 1e-5,
    num_train_epochs: int = 3,
    per_device_train_batch_size: int = 8,
    per_device_eval_batch_size: int = 8,
    gradient_accumulation_steps: int = 1,
    save_strategy: str = "epoch",
    evaluation_strategy: str = "epoch",
    logging_steps: int = 100,
    warmup_steps: int = 500,
    fp16: bool = True,
    report_to: str = "none",
    **kwargs
) -> Trainer:
    """
    Train Whisper model.
    
    Args:
        model_name: Model name or path
        train_dataset: Training dataset
        eval_dataset: Evaluation dataset
        output_dir: Output directory
        learning_rate: Learning rate
        num_train_epochs: Number of epochs
        per_device_train_batch_size: Batch size for training
        per_device_eval_batch_size: Batch size for evaluation
        gradient_accumulation_steps: Gradient accumulation steps
        save_strategy: Model saving strategy
        evaluation_strategy: Evaluation strategy
        logging_steps: Logging frequency
        warmup_steps: Warmup steps
        fp16: Use mixed precision
        report_to: Reporting destination
    
    Returns:
        Trainer object
    """
    # Load processor and model
    processor = WhisperProcessor.from_pretrained(model_name)
    model = WhisperForConditionalGeneration.from_pretrained(model_name)
    
    # Set model config
    model.config.forced_decoder_ids = None
    model.config.suppress_tokens = []
    
    # Data collator
    data_collator = DataCollatorSpeechSeq2SeqWithPadding(
        processor=processor,
        model=model,
        padding=True
    )
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=output_dir,
        per_device_train_batch_size=per_device_train_batch_size,
        per_device_eval_batch_size=per_device_eval_batch_size,
        gradient_accumulation_steps=gradient_accumulation_steps,
        learning_rate=learning_rate,
        num_train_epochs=num_train_epochs,
        warmup_steps=warmup_steps,
        evaluation_strategy=evaluation_strategy,
        save_strategy=save_strategy,
        logging_steps=logging_steps,
        fp16=fp16,
        report_to=report_to,
        load_best_model_at_end=True,
        metric_for_best_model="wer",
        greater_is_better=False,
        **kwargs
    )
    
    # Create trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        data_collator=data_collator,
        tokenizer=processor.feature_extractor,
    )
    
    return trainer


def compute_metrics(EvalPrediction) -> Dict[str, float]:
    """
    Compute WER metrics.
    
    Args:
        EvalPrediction: Evaluation prediction object
    
    Returns:
        dict: Metrics dictionary
    """
    from jiwer import wer, cer
    
    predictions = EvalPrediction.predictions
    labels = EvalPrediction.labels
    
    # Decode predictions
    pred_str = processor.batch_decode(
        predictions,
        skip_special_tokens=True
    )
    
    # Replace -100 in labels
    labels = np.where(labels != -100, labels, processor.tokenizer.pad_token_id)
    label_str = processor.batch_decode(
        labels,
        skip_special_tokens=True
    )
    
    # Compute metrics
    wer_score = wer(label_str, pred_str)
    cer_score = cer(label_str, pred_str)
    
    return {
        "wer": wer_score,
        "cer": cer_score
    }


def transcribe_audio(
    model_path: str,
    audio_path: str,
    model_name: str = "openai/whisper-small"
) -> str:
    """
    Transcribe audio using fine-tuned Whisper model.
    
    Args:
        model_path: Path to fine-tuned model
        audio_path: Path to audio file
        model_name: Base model name (for processor)
    
    Returns:
        Transcription text
    """
    # Load processor and model
    processor = WhisperProcessor.from_pretrained(model_name)
    model = WhisperForConditionalGeneration.from_pretrained(model_path)
    
    # Load audio
    audio, sr = librosa.load(audio_path, sr=16000)
    
    # Process audio
    input_features = processor(
        audio,
        sampling_rate=16000,
        return_tensors="pt"
    ).input_features
    
    # Generate
    predicted_ids = model.generate(input_features)
    
    # Decode
    transcription = processor.batch_decode(
        predicted_ids,
        skip_special_tokens=True
    )[0]
    
    return transcription


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Fine-tune Whisper")
    parser.add_argument("--model", default="openai/whisper-small")
    parser.add_argument("--output-dir", default="./whisper_output")
    parser.add_argument("--audio-dir", required=True)
    parser.add_argument("--transcription-dir", required=True)
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch-size", type=int, default=8)
    
    args = parser.parse_args()
    
    # This would be run in Google Colab
    print("This script should be run in Google Colab with GPU")
    print(f"Model: {args.model}")
    print(f"Output: {args.output_dir}")
