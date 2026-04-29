#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WER Evaluation Script for ASR Models
Calculates Word Error Rate for ASR model outputs
"""

import os
import json
import glob
import csv
import librosa
import torch
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from tqdm import tqdm

from transformers import (
    Wav2Vec2Processor,
    Wav2Vec2ForCTC,
    WhisperProcessor,
    WhisperForConditionalGeneration,
)
import jiwer


class ASREvaluator:
    """Evaluate ASR models using WER metric."""
    
    def __init__(
        self,
        model_path: str,
        model_type: str = "whisper",
        model_name: str = None
    ):
        """
        Initialize evaluator.
        
        Args:
            model_path: Path to model
            model_type: Type of model (whisper, wav2vec2)
            model_name: Base model name for processor
        """
        self.model_path = model_path
        self.model_type = model_type
        self.model_name = model_name
        
        # Load model and processor
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self._load_model()
    
    def _load_model(self):
        """Load model and processor."""
        if self.model_type == "whisper":
            self.processor = WhisperProcessor.from_pretrained(self.model_name or "openai/whisper-small")
            self.model = WhisperForConditionalGeneration.from_pretrained(self.model_path)
        
        elif self.model_type == "wav2vec2":
            self.processor = Wav2Vec2Processor.from_pretrained(self.model_name or "facebook/wav2vec2-large-xlsr-53-bengali")
            self.model = Wav2Vec2ForCTC.from_pretrained(self.model_path)
        
        self.model.to(self.device)
        self.model.eval()
    
    def transcribe(self, audio_path: str) -> str:
        """
        Transcribe a single audio file.
        
        Args:
            audio_path: Path to audio file
        
        Returns:
            Transcription text
        """
        # Load audio
        audio, sr = librosa.load(audio_path, sr=16000)
        
        if self.model_type == "whisper":
            # Process audio
            input_features = self.processor(
                audio,
                sampling_rate=16000,
                return_tensors="pt"
            ).input_features.to(self.device)
            
            # Generate
            with torch.no_grad():
                predicted_ids = self.model.generate(input_features)
            
            # Decode
            transcription = self.processor.batch_decode(
                predicted_ids,
                skip_special_tokens=True
            )[0]
        
        elif self.model_type == "wav2vec2":
            # Process audio
            input_values = self.processor(
                audio,
                sampling_rate=16000,
                return_tensors="pt"
            ).input_values.to(self.device)
            
            # Generate
            with torch.no_grad():
                logits = self.model(input_values).logits
            
            # Get predicted IDs
            predicted_ids = torch.argmax(logits, dim=-1)
            
            # Decode
            transcription = self.processor.batch_decode(
                predicted_ids
            )[0]
        
        return transcription
    
    def evaluate_dataset(
        self,
        audio_dir: str,
        reference_dir: str,
        split: str = "test"
    ) -> Dict[str, Any]:
        """
        Evaluate on a dataset.
        
        Args:
            audio_dir: Directory containing audio files
            reference_dir: Directory containing reference transcriptions
            split: Dataset split name
        
        Returns:
            Evaluation results
        """
        results = {
            "split": split,
            "total_samples": 0,
            "successful": 0,
            "failed": 0,
            "total_wer": 0.0,
            "samples": []
        }
        
        # Find all audio files
        audio_files = glob.glob(
            os.path.join(audio_dir, split, "**", "*.wav"),
            recursive=True
        )
        
        print(f"Evaluating {len(audio_files)} files...")
        
        for audio_path in tqdm(audio_files):
            # Get reference transcription
            base_name = os.path.splitext(os.path.basename(audio_path))[0]
            rel_path = os.path.relpath(audio_path, os.path.join(audio_dir, split))
            
            # Try to find transcription
            ref_path = os.path.join(
                reference_dir,
                split,
                rel_path.replace(".wav", ".txt")
            )
            
            # Try alternate path
            if not os.path.exists(ref_path):
                ref_path = os.path.join(
                    reference_dir,
                    f"{base_name}.txt"
                )
            
            if not os.path.exists(ref_path):
                print(f"Warning: No reference for {audio_path}")
                continue
            
            # Load reference
            with open(ref_path, 'r', encoding='utf-8') as f:
                reference = f.read().strip()
            
            # Transcribe
            try:
                hypothesis = self.transcribe(audio_path)
                
                # Calculate WER
                wer = jiwer.wer(reference, hypothesis)
                
                results["samples"].append({
                    "audio": audio_path,
                    "reference": reference,
                    "hypothesis": hypothesis,
                    "wer": wer
                })
                
                results["total_wer"] += wer
                results["successful"] += 1
            
            except Exception as e:
                print(f"Error processing {audio_path}: {e}")
                results["failed"] += 1
            
            results["total_samples"] += 1
        
        # Calculate average WER
        if results["successful"] > 0:
            results["average_wer"] = results["total_wer"] / results["successful"]
        else:
            results["average_wer"] = 1.0
        
        return results


def calculate_wer_per_dialect(
    results: List[Dict],
    dialect_key: str = "dialect"
) -> Dict[str, Dict[str, float]]:
    """
    Calculate WER per dialect.
    
    Args:
        results: List of evaluation results
        dialect_key: Key for dialect in metadata
    
    Returns:
        Dictionary of WER by dialect
    """
    dialect_results = {}
    
    for result in results:
        # Extract dialect from filename or path
        filename = result.get("audio", "")
        
        # Try to determine dialect from path
        dialect = "unknown"
        for d in ["dhaka", "sylhet", "chittagong", "barishal", "standard", "kolkata"]:
            if d in filename.lower():
                dialect = d
                break
        
        if dialect not in dialect_results:
            dialect_results[dialect] = {
                "samples": [],
                "total_wer": 0.0
            }
        
        dialect_results[dialect]["samples"].append(result)
        dialect_results[dialect]["total_wer"] += result.get("wer", 0.0)
    
    # Calculate averages
    dialect_wer = {}
    for dialect, data in dialect_results.items():
        n = len(data["samples"])
        if n > 0:
            dialect_wer[dialect] = {
                "wer": data["total_wer"] / n,
                "samples": n
            }
    
    return dialect_wer


def compare_models(
    model_results: Dict[str, Dict[str, float]],
    output_path: str = None
) -> str:
    """
    Create comparison table for multiple models.
    
    Args:
        model_results: Dictionary of model name -> WER scores
        output_path: Path to save comparison CSV
    
    Returns:
        Comparison table as string
    """
    # Build table
    lines = []
    lines.append("Model Comparison")
    lines.append("=" * 60)
    lines.append("")
    lines.append(f"{'Model':<30} {'WER':>10} {'Status':>15}")
    lines.append("-" * 60)
    
    for model_name, metrics in model_results.items():
        wer = metrics.get("overall", {}).get("wer", 0.0)
        status = "✓ Pass" if wer < 0.30 else "⚠ Needs Improvement"
        lines.append(f"{model_name:<30} {wer:>9.2%} {status:>15}")
    
    table = "\n".join(lines)
    print(table)
    
    # Save to CSV if path provided
    if output_path:
        with open(output_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Model", "WER", "Status"])
            for model_name, metrics in model_results.items():
                wer = metrics.get("overall", {}).get("wer", 0.0)
                status = "Pass" if wer < 0.30 else "Needs Improvement"
                writer.writerow([model_name, f"{wer:.4f}", status])
    
    return table


def evaluate_single_file(
    model_path: str,
    audio_path: str,
    reference_text: str,
    model_type: str = "whisper",
    model_name: str = None
) -> Dict[str, Any]:
    """
    Evaluate a single audio file.
    
    Args:
        model_path: Path to model
        audio_path: Path to audio file
        reference_text: Reference transcription
        model_type: Type of model
        model_name: Base model name
    
    Returns:
        Evaluation result
    """
    # Create evaluator
    evaluator = ASREvaluator(model_path, model_type, model_name)
    
    # Transcribe
    hypothesis = evaluator.transcribe(audio_path)
    
    # Calculate WER
    wer = jiwer.wer(reference_text, hypothesis)
    cer = jiwer.cer(reference_text, hypothesis)
    
    return {
        "reference": reference_text,
        "hypothesis": hypothesis,
        "wer": wer,
        "cer": cer
    }


def batch_evaluate(
    model_path: str,
    test_data: List[Dict],
    model_type: str = "whisper",
    model_name: str = None,
    output_path: str = None
) -> Dict[str, Any]:
    """
    Evaluate on a batch of test data.
    
    Args:
        model_path: Path to model
        test_data: List of test samples
        model_type: Type of model
        model_name: Base model name
        output_path: Path to save results
    
    Returns:
        Evaluation results
    """
    # Create evaluator
    evaluator = ASREvaluator(model_path, model_type, model_name)
    
    results = {
        "total": len(test_data),
        "successful": 0,
        "failed": 0,
        "total_wer": 0.0,
        "samples": []
    }
    
    for sample in tqdm(test_data, desc="Evaluating"):
        try:
            hypothesis = evaluator.transcribe(sample["audio"])
            reference = sample["transcription"]
            
            wer = jiwer.wer(reference, hypothesis)
            
            results["samples"].append({
                "audio": sample["audio"],
                "reference": reference,
                "hypothesis": hypothesis,
                "wer": wer
            })
            
            results["total_wer"] += wer
            results["successful"] += 1
        
        except Exception as e:
            print(f"Error: {e}")
            results["failed"] += 1
    
    results["average_wer"] = results["total_wer"] / max(results["successful"], 1)
    
    # Save results
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
    
    return results


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Evaluate ASR models")
    parser.add_argument("--model-path", required=True)
    parser.add_argument("--audio-dir", required=True)
    parser.add_argument("--reference-dir", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--model-type", default="whisper")
    parser.add_argument("--model-name", default=None)
    
    args = parser.parse_args()
    
    # Evaluate
    evaluator = ASREvaluator(args.model_path, args.model_type, args.model_name)
    results = evaluator.evaluate_dataset(args.audio_dir, args.reference_dir)
    
    # Save results
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\nResults saved to {args.output}")
    print(f"Average WER: {results['average_wer']:.4f}")
