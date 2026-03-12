# Prompt Guide for Code Generation

## CSE499: EHR-Based Pre-Consultation Medical Documentation System

---

## How to Use This Guide

These prompts are designed to help you generate code for each part of your project. Copy the prompt, modify the parts in brackets `[]`, and use it with an AI to get the code you need.

---

# PART 1: ASR (PHASE 1) PROMPTS

## 1.1 YouTube Audio Download

### Prompt: Basic YouTube Download
```
Write a Python script using yt-dlp to download audio from YouTube videos. 
The script should:
1. Take a YouTube URL as input
2. Download the audio in WAV format
3. Save to a specified output folder
4. Handle errors gracefully
5. Use Google Colab compatible code

Output folder: [e.g., /content/drive/MyDrive/CSE499/raw_audio]
```

### Prompt: Batch YouTube Download
```
Create a Python script that:
1. Reads a list of YouTube URLs from a CSV file
2. Downloads each audio file using yt-dlp
3. Names files using the pattern: {dialect}_{number}.wav
4. Saves to Google Drive
5. Logs progress and errors
6. Handles rate limiting

CSV columns: [url, dialect, filename]
```

---

## 1.2 Audio Preprocessing

### Prompt: Audio Resampling
```
Write Python code to:
1. Load all WAV files from a folder
2. Resample each to 16000 Hz sample rate using librosa
3. Normalize the audio volume
4. Remove silence from beginning and end
5. Save processed files to a new folder
6. Run on Google Colab

Input folder: [path/to/input]
Output folder: [path/to/output]
```

---

## 1.3 Transcription

### Prompt: Manual Transcription Template
```
Create a Python script that:
1. Creates a transcription template CSV
2. Lists all audio files in a folder
3. For each file, creates a row with:
   - filename
   - transcription (empty for manual entry)
   - duration
   - dialect
   - status (pending/completed)
4. Saves to Google Sheets compatible format
```

---

## 1.4 Whisper Fine-tuning

### Prompt: Whisper Training Setup
```
Write complete Python code to fine-tune OpenAI Whisper (small model) 
on Bengali audio data using Hugging Face Transformers.

Requirements:
1. Load Mozilla Common Voice Bengali dataset
2. Use WhisperForConditionalGeneration
3. Set up training with Accelerate
4. Use SpeechTrainingArguments with:
   - learning_rate: 1e-5
   - per_device_train_batch_size: 8
   - num_train_epochs: 3
5. Save checkpoints to Google Drive
6. Calculate WER on validation set

Dataset location: [path/to/your/data]
Output: [path/to/save/model]
```

### Prompt: Whisper Inference
```
Write Python code to:
1. Load fine-tuned Whisper model from Google Drive
2. Transcribe an audio file in Bengali
3. Return the transcription text
4. Return confidence score if available
5. Handle long audio files (chunking if needed)

Model path: [path/to/model]
Audio file: [path/to/audio.wav]
```

---

## 1.5 Wav2Vec2 Training

### Prompt: Wav2Vec2 Fine-tuning
```
Create Python code to fine-tune Wav2Vec2 for Bengali ASR:
1. Load facebook/wav2vec2-large-xlsr-53-bengali
2. Prepare custom dataset from your audio files and transcriptions
3. Set up CTC training
4. Train for 10 epochs
5. Evaluate using WER metric
6. Save best model to Drive

Audio folder: [path/to/audio]
Transcription folder: [path/to/text]
```

---

## 1.6 Model Evaluation

### Prompt: WER Calculation
```
Write Python code to:
1. Load multiple ASR models (Whisper, Wav2Vec2, HuBERT)
2. Evaluate each on test dataset
3. Calculate Word Error Rate (WER) using jiwer
4. Create comparison table showing WER per model
5. Save results to CSV

Models to evaluate: [list of model paths]
Test data: [path/to/test/set]
```

---

# PART 2: NER (PHASE 2) PROMPTS

## 2.1 Annotation Tool

### Prompt: Simple NER Annotator
```
Create a Python script for NER annotation:
1. Load text from a file
2. Display text one sentence at a time
3. Allow user to select entity type (SYMPTOM, DISEASE, MEDICATION, etc.)
4. Highlight selected entity in text
5. Save annotations in BIO format
6. Save to JSON file

Text file: [path/to/input.txt]
Output: [path/to/annotations.json]
```

---

## 2.2 Data Preparation

### Prompt: NER Data Converter
```
Write Python code to:
1. Read annotation data from JSON format
2. Convert to token-classification format for Hugging Face
3. Split into train/validation/test sets (80/10/10)
4. Save as JSON files
5. Create label mapping

Input: [path/to/annotations]
Output folder: [path/to/output]
```

---

## 2.3 BanglaBERT Training

### Prompt: BanglaBERT NER Training
```
Create complete Python code to fine-tune BanglaBERT for medical NER:
1. Load csebuetnlp/banglabert model
2. Add token classification head
3. Prepare dataset from your annotations
4. Train with these settings:
   - learning_rate: 2e-5
   - num_train_epochs: 10
   - batch_size: 16
5. Evaluate using seqeval (precision, recall, F1)
6. Save best model to Drive

Entity types: [SYMPTOM, DISEASE, MEDICATION, DURATION, ALLERGY, BODY_PART, TREATMENT, DOSAGE]
```

---

## 2.4 NER Inference

### Prompt: NER Entity Extraction
```
Write Python code to:
1. Load fine-tuned NER model from Google Drive
2. Input a Bengali medical text
3. Extract named entities using token classification
4. Return entities with their types and positions
5. Output in JSON format

Model path: [path/to/model]
Input text: [Bengali text string]
```

---

# PART 3: EHR (PHASE 3) PROMPTS

## 3.1 EHR Template

### Prompt: EHR Template Generator
```
Create a Python script that:
1. Defines an EHR template with fields:
   - patient_id (auto-generated)
   - consultation_date (auto)
   - chief_complaint (symptoms, duration)
   - medical_history (diseases, medications, allergies)
   - assessment_and_plan (impression, treatments)
2. Saves template as JSON
3. Includes sample data

Output: [path/to/template.json]
```

---

## 3.2 Entity to EHR Mapping

### Prompt: Entity Mapper
```
Write Python code to:
1. Take NER output (entities with types)
2. Map each entity type to EHR fields:
   - SYMPTOM -> chief_complaint.symptoms
   - DISEASE -> medical_history.diseases
   - MEDICATION -> medical_history.current_medications
   - ALLERGY -> medical_history.allergies
   - DURATION -> chief_complaint.duration
   - TREATMENT -> assessment_and_plan.treatments
3. Generate complete EHR JSON
4. Handle duplicate entities

Input: [NER output JSON]
Output: [EHR JSON]
```

---

## 3.3 Human-Readable Output

### Prompt: EHR Formatter
```
Create Python code to:
1. Read EHR JSON
2. Format as human-readable text report
3. Use clear section headers
4. Include all fields nicely formatted
5. Save as both .txt and .md files

Input: [EHR JSON file]
Output: [formatted text file]
```

---

# PART 4: INTEGRATION PROMPTS

## 4.1 Complete Pipeline

### Prompt: End-to-End Pipeline
```
Write Python code for complete EHR pipeline:
1. Class EHRPipeline with methods:
   - __init__: load ASR and NER models
   - process(audio_file): 
     a. Transcribe audio using ASR
     b. Extract entities using NER
     c. Generate EHR JSON
     d. Generate human-readable report
2. Handle errors gracefully
3. Return both JSON and text outputs
4. Include progress logging

ASR model: [path/to/asr/model]
NER model: [path/to/ner/model]
```

---

## 4.2 Demo Interface

### Prompt: Colab Demo Interface
```
Create a Google Colab demo using ipywidgets:
1. File upload button for audio
2. Dropdown for model selection
3. Run button
4. Display areas for:
   - Transcription
   - Extracted entities
   - EHR JSON
   - Human-readable report
5. Style nicely with markdown

Make it work in Google Colab environment.
```

---

# PART 5: UTILITY PROMPTS

## 5.1 Google Drive Setup

### Prompt: Drive Mount Helper
```
Write Python code to:
1. Mount Google Drive in Colab
2. Create project folder structure if not exists:
   - /drive/CSE499_Project/dataset/
   - /drive/CSE499_Project/phase1_asr/
   - /drive/CSE499_Project/phase2_ner/
   - /drive/CSE499_Project/phase3_ehr/
3. Return paths to each folder
4. Handle already-mounted case
```

---

## 5.2 Data Splitting

### Prompt: Dataset Splitter
```
Create Python code to:
1. Read audio files and transcriptions from folders
2. Split into train/val/test (80/10/10)
3. Ensure stratified split by dialect
4. Create manifest files for each split
5. Save to respective folders
6. Print statistics

Input folder: [path/to/data]
Output: [train/, val/, test/ folders]
```

---

## 5.3 Checkpoint Saving

### Prompt: Checkpoint Manager
```
Write Python code to:
1. Save model checkpoint to Google Drive
2. Include model weights, config, tokenizer
3. Create backup with timestamp
4. Load checkpoint function
5. Track best model based on metric

Model: [model object]
Save path: [path/to/save]
Metric value: [WER or F1 score]
```

---

# PART 6: COLLABORATION PROMPTS

## 6.1 GitHub Setup

### Prompt: Git Initialize
```
Write bash commands to:
1. Initialize git repository
2. Create .gitignore for:
   - __pycache__/
   - *.pyc
   - .env
   - large model files
   - dataset files
3. Create initial commit
4. Add remote origin
5. Push to GitHub

Repository URL: [your-repo-url]
```

---

## 6.2 Requirements File

### Prompt: Requirements Generator
```
Create requirements.txt for this project:
- Python 3.8+
- torch>=2.0.0
- transformers>=4.30.0
- datasets>=2.0.0
- librosa>=0.10.0
- soundfile>=0.12.0
- jiwer
- yt-dlp
- pandas
- numpy
- matplotlib
- seqeval

Include version numbers and brief comments.
```

---

# HOW TO USE THESE PROMPTS

## Steps:
1. **Find the prompt** that matches your need
2. **Copy** the prompt text
3. **Modify** the parts in brackets `[...]` with your specific paths/names
4. **Paste** to AI (like me, ChatGPT, Claude, etc.)
5. **Review** the generated code
6. **Test** in your Colab environment
7. **Save** to your project folder

## Tips:
- Start with simpler prompts if you're a beginner
- Test each piece before combining
- Save working code for reuse
- Don't skip error handling
- Add comments to understand later

---

## Common Modifications Needed

| Replace | With |
|---------|------|
| [path/to/input] | /content/drive/MyDrive/CSE499/data/input |
| [path/to/output] | /content/drive/MyDrive/CSE499/models/output |
| [path/to/model] | /content/drive/MyDrive/CSE499/models/whisper-finetuned |
| [path/to/audio.wav] | actual audio file path |
| [Bengali text string] | actual Bengali text |

---

## If Code Doesn't Work

1. Check all paths are correct
2. Verify packages are installed
3. Look for typos in filenames
4. Check GPU is available
5. Try restarting Colab runtime

---

*Prompts ready. Use these to generate code for your project.*
