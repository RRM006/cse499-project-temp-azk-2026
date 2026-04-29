# Quick Start Guide - Phase 1

## Before You Begin

1. One team member (Team Lead) creates the shared Google Drive folder
2. Share it with both teammates with **Editor** permission
3. All teammates click **"Add shortcut to Drive"**
4. Team Lead creates GitHub repo `CSE499-EHR-System` (Private) and invites teammates
5. Make sure Google Drive has at least **10GB free** (audio + models take space)

---

## Step 1: Open Google Colab and Set GPU

1. Go to [colab.research.google.com](https://colab.research.google.com)
2. Create a new notebook — name it `phase1_setup.ipynb`
3. **Runtime → Change runtime type → T4 GPU** ← do this first, before any code

```python
# Confirm GPU is active
import torch
print(f"GPU available: {torch.cuda.is_available()}")
print(f"GPU name: {torch.cuda.get_device_name(0)}")
```

---

## Step 2: Mount Google Drive

**Run this at the top of EVERY notebook, every session.**

```python
from google.colab import drive
drive.mount('/content/drive')

# Your project base path — use this variable everywhere
BASE = '/content/drive/MyDrive/CSE499_EHR_Project'
print(f"Drive mounted. Project path: {BASE}")
```

> ⚠️ **Important:** Always use `/content/drive/MyDrive/` (not `/content/drive/My Drive/` — no space)

---

## Step 3: Install Required Packages for Phase 1

```python
# Run this at the start of every Phase 1 Colab session
!pip install torch transformers datasets evaluate jiwer librosa noisereduce soundfile yt-dlp accelerate
```

> Colab already has: `numpy`, `pandas`, `matplotlib`. Do not reinstall those.

---

## Step 4: Create Phase 1 Folder Structure in Drive

Run once. If folders already exist, `exist_ok=True` skips them safely.

```python
import os

BASE = '/content/drive/MyDrive/CSE499_EHR_Project'

DIALECTS = ['puran_dhaka', 'barishal', 'sylheti', 'normal_bangla', 'indian_bangla']

MODEL_NAMES = [
    'wav2vec2_transcripts', 'hubert_transcripts', 'whisper_transcripts',
    'data2vec_transcripts', 'wavlm_transcripts', 'xlsr_transcripts',
    'canary_transcripts', 'olmosasr_transcripts', 'mms_transcripts',
    'seamless_transcripts', 'conformer_transcripts'
]

folders = [
    f'{BASE}/00_Admin',
    *[f'{BASE}/01_Dataset/raw_audio/{d}' for d in DIALECTS],
    *[f'{BASE}/01_Dataset/cleaned_audio/{d}' for d in DIALECTS],
    f'{BASE}/01_Dataset/transcripts/manual',
    f'{BASE}/01_Dataset/transcripts/auto',
    f'{BASE}/01_Dataset/metadata',
    f'{BASE}/02_Phase1_ASR/notebooks',
    *[f'{BASE}/02_Phase1_ASR/model_outputs/{m}' for m in MODEL_NAMES],
    f'{BASE}/02_Phase1_ASR/evaluation',
    f'{BASE}/02_Phase1_ASR/saved_models/whisper_finetuned',
    f'{BASE}/02_Phase1_ASR/saved_models/whisper_checkpoints',
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

print("✅ All Phase 1 folders created!")
```

---

## Step 5: Download Audio Data (Notebook: `01_data_download.ipynb`)

### Target: 40–60 audio clips per dialect

| Dialect Folder | Search Keywords (YouTube / Facebook) |
|----------------|--------------------------------------|
| `puran_dhaka/` | পুরান ঢাকা, পুরান ঢাকার ভাষা, Dhaka patient interview |
| `barishal/` | বরিশালের ভাষা, বরিশাল স্বাস্থ্য |
| `sylheti/` | সিলেটি কথা, সিলেট ডাক্তার |
| `normal_bangla/` | বাংলা চিকিৎসা, বাংলা স্বাস্থ্য পরামর্শ |
| `indian_bangla/` | কলকাতার বাংলা, Kolkata doctor Bengali |

> Also check: **OpenSLR.org** (Shrutilipi, Bengali ASR) and **Mozilla Common Voice** (free Bangla recordings)

```python
import yt_dlp, os

BASE = '/content/drive/MyDrive/CSE499_EHR_Project'
DIALECT = 'barishal'   # ← change this for each dialect
OUTPUT_DIR = f'{BASE}/01_Dataset/raw_audio/{DIALECT}'

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': f'{OUTPUT_DIR}/%(title)s.%(ext)s',
    'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'wav'}],
}

urls = [
    'https://youtube.com/watch?v=REPLACE_WITH_REAL_URL',
    # add more URLs here
]

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(urls)

print(f"✅ Downloaded to {OUTPUT_DIR}")
```

### Audio File Naming — REQUIRED FORMAT

Rename each file after downloading:

```
[dialect_code]_[3-digit number]_[gender]_[age group].[ext]
```

| Dialect Code | Example Filename |
|---|---|
| `pd` = Puran Dhaka | `pd_001_male_40s.wav` |
| `br` = Barishal | `br_001_female_30s.wav` |
| `sy` = Sylheti | `sy_001_male_25s.wav` |
| `nb` = Normal Bangla | `nb_001_female_30s.wav` |
| `ib` = Indian Bangla | `ib_001_male_40s.wav` |

---

## Step 6: Test Baseline Whisper (Quick Sanity Check)

Before any fine-tuning, verify Whisper works on your audio:

```python
from transformers import pipeline

whisper = pipeline("automatic-speech-recognition", model="openai/whisper-small")

# Test with one of your downloaded files
test_file = f'{BASE}/01_Dataset/raw_audio/barishal/br_001_female_30s.wav'
result = whisper(test_file, language="bn")
print("Transcript:", result["text"])
```

---

## What Comes Next (Phase 1 Full Steps)

| Step | Notebook | What You Do |
|------|----------|-------------|
| 1 | `01_data_download.ipynb` | Download audio from YouTube by dialect |
| 2 | `02_audio_preprocessing.ipynb` | Clean noise, convert to 16kHz mono WAV |
| 3 | `03_model_comparison.ipynb` | Run 10+ ASR models, record WER scores |
| 4 | `04_whisper_finetune.ipynb` | Fine-tune Whisper on your dialect dataset |
| 5 | (in notebook 4) | Batch transcribe all audio with fine-tuned Whisper |

Save all notebooks to: `02_Phase1_ASR/notebooks/` in Drive.

---

## Colab Golden Rules

| Rule | What To Do |
|------|-----------|
| Always mount Drive first | First cell of every notebook |
| Save to Drive, not Colab | Never save to `/content/` — it disappears |
| Save checkpoints often | Every 500 steps during training |
| Use GPU only for training | Switch to CPU for data prep (saves GPU quota) |
| One notebook per task | Do not combine all steps in one notebook |
