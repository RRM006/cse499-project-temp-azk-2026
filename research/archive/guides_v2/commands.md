# Essential Commands Reference

---

## Google Colab — Session Start (Run Every Time)

```python
# 1. Mount Google Drive — ALWAYS first cell
from google.colab import drive
drive.mount('/content/drive')

# 2. Set your base path — use this variable everywhere, never hardcode
BASE = '/content/drive/MyDrive/CSE499_EHR_Project'

# 3. Check GPU
import torch
print(f"GPU: {torch.cuda.is_available()}")
print(f"GPU name: {torch.cuda.get_device_name(0)}")

# 4. Check GPU memory
!nvidia-smi

# 5. Install Phase 1 packages
!pip install transformers datasets evaluate jiwer librosa noisereduce soundfile yt-dlp accelerate
```

---

## Folder Structure — Create Phase 1 Folders

```python
import os

BASE = '/content/drive/MyDrive/CSE499_EHR_Project'
DIALECTS = ['puran_dhaka', 'barishal', 'sylheti', 'normal_bangla', 'indian_bangla']

folders = [
    f'{BASE}/00_Admin',
    *[f'{BASE}/01_Dataset/raw_audio/{d}' for d in DIALECTS],
    *[f'{BASE}/01_Dataset/cleaned_audio/{d}' for d in DIALECTS],
    f'{BASE}/01_Dataset/transcripts/manual',
    f'{BASE}/01_Dataset/transcripts/auto',
    f'{BASE}/01_Dataset/metadata',
    f'{BASE}/02_Phase1_ASR/notebooks',
    f'{BASE}/02_Phase1_ASR/evaluation',
    f'{BASE}/02_Phase1_ASR/saved_models/whisper_finetuned',
    f'{BASE}/02_Phase1_ASR/saved_models/whisper_checkpoints',
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)
    
print("✅ All Phase 1 folders created!")
```

---

## YouTube Download (Notebook: `01_data_download.ipynb`)

```python
import yt_dlp

BASE = '/content/drive/MyDrive/CSE499_EHR_Project'
DIALECT = 'barishal'   # change for each dialect: puran_dhaka, sylheti, normal_bangla, indian_bangla
OUTPUT_DIR = f'{BASE}/01_Dataset/raw_audio/{DIALECT}'

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': f'{OUTPUT_DIR}/%(title)s.%(ext)s',
    'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'wav'}],
}

urls = [
    'https://youtube.com/watch?v=YOUR_URL_HERE',
    # add more URLs
]

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(urls)
```

---

## Audio Preprocessing (Notebook: `02_audio_preprocessing.ipynb`)

```python
import librosa
import soundfile as sf
import noisereduce as nr
import os

BASE = '/content/drive/MyDrive/CSE499_EHR_Project'
DIALECT = 'barishal'
INPUT_DIR = f'{BASE}/01_Dataset/raw_audio/{DIALECT}'
OUTPUT_DIR = f'{BASE}/01_Dataset/cleaned_audio/{DIALECT}'

for filename in os.listdir(INPUT_DIR):
    if not filename.endswith('.wav'):
        continue
    
    # Load audio at 16kHz (required by all ASR models)
    audio, sr = librosa.load(os.path.join(INPUT_DIR, filename), sr=16000, mono=True)
    
    # Remove background noise
    audio = nr.reduce_noise(y=audio, sr=sr)
    
    # Trim silence from start and end
    audio, _ = librosa.effects.trim(audio, top_db=20)
    
    # Normalize volume
    audio = audio / max(abs(audio))
    
    # Save cleaned file
    sf.write(os.path.join(OUTPUT_DIR, filename), audio, 16000)
    print(f"✅ Cleaned: {filename}")
```

---

## ASR Models — Load and Transcribe

### Whisper (Main Model — Best for Bangla)

```python
from transformers import pipeline

BASE = '/content/drive/MyDrive/CSE499_EHR_Project'
whisper = pipeline("automatic-speech-recognition", model="openai/whisper-small")

# Transcribe single file
result = whisper(f'{BASE}/01_Dataset/cleaned_audio/barishal/br_001_female_30s.wav', language="bn")
print(result["text"])

# Batch transcribe all files in a dialect folder
import os

DIALECT = 'barishal'
INPUT_DIR = f'{BASE}/01_Dataset/cleaned_audio/{DIALECT}'
OUTPUT_DIR = f'{BASE}/01_Dataset/transcripts/auto'
os.makedirs(OUTPUT_DIR, exist_ok=True)

for filename in os.listdir(INPUT_DIR):
    if not filename.endswith('.wav'):
        continue
    audio_path = os.path.join(INPUT_DIR, filename)
    result = whisper(audio_path, language="bn")
    txt_filename = filename.replace('.wav', '.txt')
    with open(os.path.join(OUTPUT_DIR, txt_filename), 'w', encoding='utf-8') as f:
        f.write(result["text"])
    print(f"✅ Transcribed: {filename}")
```

### Wav2Vec2

```python
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import torch, librosa

processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-xlsr-53-bengali")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-xlsr-53-bengali")

audio, sr = librosa.load("file.wav", sr=16000)
inputs = processor(audio, sampling_rate=16000, return_tensors="pt", padding=True)
with torch.no_grad():
    logits = model(**inputs).logits
predicted_ids = torch.argmax(logits, dim=-1)
transcript = processor.batch_decode(predicted_ids)[0]
print(transcript)
```

### MMS (Meta — covers Bangla dialects)

```python
from transformers import pipeline
mms = pipeline("automatic-speech-recognition", model="facebook/mms-1b-all")
result = mms("file.wav", generate_kwargs={"language": "ben"})
print(result["text"])
```

### SeamlessM4T (Handles Bangla–English code-mixing)

```python
from transformers import pipeline
seamless = pipeline("automatic-speech-recognition", model="facebook/seamless-m4t-v2-large")
result = seamless("file.wav", generate_kwargs={"tgt_lang": "ben"})
print(result["text"])
```

---

## WER Evaluation (Notebook: `03_model_comparison.ipynb`)

```python
from jiwer import wer
import csv

BASE = '/content/drive/MyDrive/CSE499_EHR_Project'
WER_CSV = f'{BASE}/02_Phase1_ASR/evaluation/wer_scores.csv'

# Calculate WER between reference (manual) and hypothesis (model output)
reference = "আমার মাথা ব্যাথা করছে তিন দিন ধরে"
hypothesis = "আমার মাথা ব্যথা করছে তিন দিন ধরে"

score = wer(reference, hypothesis)
print(f"WER: {score * 100:.2f}%")

# Append result to CSV
with open(WER_CSV, 'a', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['whisper-small', 'barishal', 'br_001_female_30s.wav', f"{score:.4f}", ''])
```

---

## Checkpoint Saving — Whisper Fine-Tuning (Notebook: `04_whisper_finetune.ipynb`)

```python
import glob

BASE = '/content/drive/MyDrive/CSE499_EHR_Project'
CHECKPOINT_DIR = f'{BASE}/02_Phase1_ASR/saved_models/whisper_checkpoints'
FINAL_MODEL_DIR = f'{BASE}/02_Phase1_ASR/saved_models/whisper_finetuned'

# Detect existing checkpoint — auto-resume if found
existing = sorted(glob.glob(f'{CHECKPOINT_DIR}/checkpoint-*'))
RESUME_FROM = existing[-1] if existing else None
print(f"Resuming from: {RESUME_FROM}" if RESUME_FROM else "Starting from scratch")

# Training arguments — paste into Seq2SeqTrainingArguments
training_args = Seq2SeqTrainingArguments(
    output_dir=CHECKPOINT_DIR,
    save_steps=500,           # save checkpoint every 500 steps
    save_total_limit=3,       # keep only 3 checkpoints (saves Drive space)
    evaluation_strategy='steps',
    eval_steps=500,
    logging_steps=100,
    learning_rate=1e-5,
    per_device_train_batch_size=8,
    gradient_accumulation_steps=2,
    warmup_steps=100,
    num_train_epochs=5,
    fp16=True,
    predict_with_generate=True,
    generation_max_length=225,
    load_best_model_at_end=True,
    metric_for_best_model='wer',
    greater_is_better=False,
    report_to='none',
)

# Start or resume training
trainer.train(resume_from_checkpoint=RESUME_FROM)

# Save final model to Drive
trainer.save_model(FINAL_MODEL_DIR)
print(f"✅ Final model saved to {FINAL_MODEL_DIR}")
```

---

## Save and Load Model

```python
BASE = '/content/drive/MyDrive/CSE499_EHR_Project'

# Save fine-tuned Whisper to Drive
model.save_pretrained(f'{BASE}/02_Phase1_ASR/saved_models/whisper_finetuned')
processor.save_pretrained(f'{BASE}/02_Phase1_ASR/saved_models/whisper_finetuned')
print("✅ Model saved to Drive")

# Load saved model in a new session
from transformers import WhisperForConditionalGeneration, WhisperProcessor

model = WhisperForConditionalGeneration.from_pretrained(
    f'{BASE}/02_Phase1_ASR/saved_models/whisper_finetuned'
)
processor = WhisperProcessor.from_pretrained(
    f'{BASE}/02_Phase1_ASR/saved_models/whisper_finetuned'
)
```

---

## Memory Management

```python
import gc
import torch

# Clear GPU memory between experiments
gc.collect()
torch.cuda.empty_cache()

# Check memory usage
!nvidia-smi

# Check Drive storage
!df -h /content/drive/MyDrive
```

---

## JSON Operations (for Phase 3 EHR)

```python
import json

# Read EHR JSON
with open('ehr_output.json', 'r', encoding='utf-8') as f:
    ehr = json.load(f)

# Write EHR JSON
with open('ehr_br_001_female_30s.json', 'w', encoding='utf-8') as f:
    json.dump(ehr, f, ensure_ascii=False, indent=2)
```

---

## Git Commands

```bash
# Initialize (one time)
git init

# Add and commit code
git add .
git commit -m "Add Whisper fine-tune notebook"

# Push to GitHub
git push origin main

# Pull latest from teammates
git pull origin main

# Check status
git status
```

> **Rule:** Push code (`.ipynb`, `.py`, `.json` templates) to GitHub.
> Audio files (`.wav`, `.mp3`) and model weights → Google Drive only.
> Add to `.gitignore`: `*.wav`, `*.mp3`, `models/`, `dataset/`

---

## Common Fixes

| Problem | Solution |
|---------|----------|
| Colab disconnects during training | Checkpoints saved every 500 steps → resume with `RESUME_FROM` |
| CUDA out of memory | Reduce `per_device_train_batch_size` to 4 or 2 |
| File not found | Use absolute paths starting with `BASE` variable |
| Unicode error in Bangla text | Add `encoding='utf-8'` to all file open() calls |
| Drive path not found | Check spelling: `MyDrive` not `My Drive` |
| GPU not available | Runtime → Change runtime type → T4 GPU → Restart |
