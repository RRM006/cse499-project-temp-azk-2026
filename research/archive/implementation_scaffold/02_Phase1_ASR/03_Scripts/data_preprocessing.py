#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Audio Preprocessing Script for Phase 1: ASR
Processes raw audio files: resample, normalize, trim silence
"""

import os
import glob
import librosa
import soundfile as sf
import argparse
from tqdm import tqdm


def load_audio(audio_path: str, target_sr: int = 16000):
    """
    Load audio file and resample to target sample rate.
    
    Args:
        audio_path: Path to audio file
        target_sr: Target sample rate (default: 16000)
    
    Returns:
        tuple: (audio_array, sample_rate)
    """
    try:
        audio, sr = librosa.load(audio_path, sr=target_sr)
        return audio, sr
    except Exception as e:
        print(f"Error loading {audio_path}: {e}")
        return None, None


def trim_silence(audio, top_db: int = 20):
    """
    Remove silence from beginning and end of audio.
    
    Args:
        audio: Audio array
        top_db: Threshold in dB below reference to consider silence
    
    Returns:
        Trimmed audio array
    """
    trimmed, _ = librosa.effects.trim(audio, top_db=top_db)
    return trimmed


def normalize_audio(audio):
    """
    Normalize audio to maximum amplitude.
    
    Args:
        audio: Audio array
    
    Returns:
        Normalized audio array
    """
    max_val = max(abs(audio))
    if max_val > 0:
        return audio / max_val
    return audio


def convert_to_mono(audio):
    """
    Convert audio to mono if stereo.
    
    Args:
        audio: Audio array
    
    Returns:
        Mono audio array
    """
    if len(audio.shape) > 1:
        return librosa.to_mono(audio)
    return audio


def process_audio_file(
    input_path: str,
    output_path: str,
    target_sr: int = 16000,
    normalize: bool = True,
    trim_sil: bool = True,
    top_db: int = 20
):
    """
    Process a single audio file.
    
    Args:
        input_path: Input audio file path
        output_path: Output audio file path
        target_sr: Target sample rate
        normalize: Whether to normalize audio
        trim_sil: Whether to trim silence
        top_db: Silence threshold in dB
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Load audio
        audio, sr = load_audio(input_path, target_sr)
        if audio is None:
            return False
        
        # Convert to mono
        audio = convert_to_mono(audio)
        
        # Trim silence
        if trim_sil:
            audio = trim_silence(audio, top_db)
        
        # Normalize
        if normalize:
            audio = normalize_audio(audio)
        
        # Save
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        sf.write(output_path, audio, sr)
        
        return True
    
    except Exception as e:
        print(f"Error processing {input_path}: {e}")
        return False


def process_directory(
    input_dir: str,
    output_dir: str,
    target_sr: int = 16000,
    file_pattern: str = "*.wav",
    normalize: bool = True,
    trim_sil: bool = True,
    top_db: int = 20
):
    """
    Process all audio files in a directory.
    
    Args:
        input_dir: Input directory
        output_dir: Output directory
        target_sr: Target sample rate
        file_pattern: File pattern to match
        normalize: Whether to normalize audio
        trim_sil: Whether to trim silence
        top_db: Silence threshold in dB
    
    Returns:
        dict: Statistics of processing
    """
    # Find all files
    input_files = glob.glob(os.path.join(input_dir, file_pattern))
    
    stats = {
        "total": len(input_files),
        "success": 0,
        "failed": 0,
        "failed_files": []
    }
    
    print(f"Found {len(input_files)} audio files")
    print(f"Input: {input_dir}")
    print(f"Output: {output_dir}")
    print(f"Target sample rate: {target_sr} Hz")
    print()
    
    for input_file in tqdm(input_files, desc="Processing"):
        # Get relative path
        rel_path = os.path.relpath(input_file, input_dir)
        output_file = os.path.join(output_dir, rel_path)
        
        # Process
        success = process_audio_file(
            input_file, output_file,
            target_sr, normalize, trim_sil, top_db
        )
        
        if success:
            stats["success"] += 1
        else:
            stats["failed"] += 1
            stats["failed_files"].append(input_file)
    
    return stats


def get_audio_info(audio_path: str) -> dict:
    """
    Get information about an audio file.
    
    Args:
        audio_path: Path to audio file
    
    Returns:
        dict: Audio information
    """
    try:
        info = {}
        audio, sr = librosa.load(audio_path, sr=None)
        
        info["sample_rate"] = sr
        info["duration"] = len(audio) / sr
        info["channels"] = 1 if len(audio.shape) == 1 else audio.shape[0]
        info["samples"] = len(audio)
        
        # Check for silence
        trimmed, (start, end) = librosa.effects.trim(audio, top_db=20)
        info["silence_removed_start"] = start / sr
        info["silence_removed_end"] = (len(audio) - end) / sr
        
        return info
    
    except Exception as e:
        return {"error": str(e)}


def batch_audio_info(directory: str, file_pattern: str = "*.wav") -> list:
    """
    Get information about all audio files in a directory.
    
    Args:
        directory: Directory path
        file_pattern: File pattern to match
    
    Returns:
        list: List of audio info dictionaries
    """
    files = glob.glob(os.path.join(directory, file_pattern))
    results = []
    
    for f in tqdm(files, desc="Getting info"):
        info = get_audio_info(f)
        info["filename"] = os.path.basename(f)
        results.append(info)
    
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Preprocess audio files for ASR"
    )
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Input directory or file"
    )
    parser.add_argument(
        "--output", "-o",
        required=True,
        help="Output directory"
    )
    parser.add_argument(
        "--sample-rate", "-sr",
        type=int,
        default=16000,
        help="Target sample rate (default: 16000)"
    )
    parser.add_argument(
        "--pattern", "-p",
        default="*.wav",
        help="File pattern (default: *.wav)"
    )
    parser.add_argument(
        "--no-normalize",
        action="store_true",
        help="Skip normalization"
    )
    parser.add_argument(
        "--no-trim",
        action="store_true",
        help="Skip silence trimming"
    )
    parser.add_argument(
        "--top-db",
        type=int,
        default=20,
        help="Silence threshold in dB (default: 20)"
    )
    
    args = parser.parse_args()
    
    if os.path.isdir(args.input):
        stats = process_directory(
            args.input,
            args.output,
            args.sample_rate,
            args.pattern,
            not args.no_normalize,
            not args.no_trim,
            args.top_db
        )
        
        print("\n" + "=" * 50)
        print("Processing Complete!")
        print(f"Total: {stats['total']}")
        print(f"Success: {stats['success']}")
        print(f"Failed: {stats['failed']}")
        
        if stats['failed_files']:
            print("\nFailed files:")
            for f in stats['failed_files']:
                print(f"  - {f}")
    else:
        success = process_audio_file(
            args.input,
            args.output,
            args.sample_rate,
            not args.no_normalize,
            not args.no_trim,
            args.top_db
        )
        print(f"Processing {'successful' if success else 'failed'}")
