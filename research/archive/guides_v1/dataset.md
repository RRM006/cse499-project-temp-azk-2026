# Dataset Knowledge Guide

## CSE499: EHR-Based Pre-Consultation Medical Documentation System

---

## 1. Understanding Dataset Requirements

### Why Custom Dataset?
- Pre-existing datasets may not have medical context
- Need dialect-specific audio for your project
- Must match your EHR extraction goals
- Code-mixing examples needed

### Dataset Types Needed

| Type | Purpose | Amount |
|------|---------|--------|
| Audio Files | Train ASR model | 200-300 |
| Transcriptions | Train ASR, Evaluate | Same as audio |
| Annotated Text | Train NER model | 500+ samples |
| Test Data | Evaluate system | 50+ samples |

---

## 2. Dialects to Collect

### Target Dialects

| Dialect | Region | Search Keywords |
|---------|--------|------------------|
| Dhaka (Purba) | Dhaka, Narayanganj | ঢাকা স্বাস্থ্য, Dhaka patient |
| Sylhet | Sylhet division | সিলেট ডাক্তার, Sylhet medical |
| Barishal | Barishal division | বরিশাল স্বাস্থ্য, Barishal health |
| Standard Bangla | General | বাংলা স্বাস্থ্য পরামর্শ |
| Kolkata | West Bengal, India | Kolkata doctor, বাংলা চিকিৎসক |

### Priority Order
1. **Standard Bangla** (easiest to find)
2. **Dhaka** (most common)
3. **Sylhet** (distinct accent)
4. **Barishal** (medium difficulty)
5. **Kolkata** (may need Indian sources)

---

## 3. YouTube Data Collection

### Step 1: Install Required Tools

```python
# In Google Colab
!pip install yt-dlp ffmpeg-python
```

### Step 2: Basic YouTube Download

```python
import yt_dlp
import os

def download_audio(youtube_url, output_path, filename):
    """Download audio from YouTube video."""
    os.makedirs(output_path, exist_ok=True)
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_path}/{filename}',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])
```

### Step 3: Search Strategy

**For Dhaka dialect:**
- Search: "ঢাকা রোগী সাক্ষাৎকার", "Dhaka medical interview"
- Look for: Local news health segments, patient interviews
- Channels: Channel i, ATN Bangla, Dhaka News

**For Sylhet dialect:**
- Search: "সিলেট স্বাস্থ্য", "Sylhet doctor advice"
- Look for: Sylhet local news, regional health programs
- Channels: Sylhet News, Meghna News

**For Barishal dialect:**
- Search: "বরিশাল ডাক্তার", "Barishal health"
- Look for: Barishal local news
- Channels: Barishal News, Khola Bhanga

**For Kolkata dialect:**
- Search: "Kolkata medical advice Bengali", "কলকাতা ডাক্তার"
- Look for: ABP Ananda, Zee Bangla health shows
- Channels: ABP, Zee, TV9 Bangla

### Step 4: Batch Download Script

```python
# Download multiple videos
video_urls = [
    "https://youtube.com/watch?v=...",
    "https://youtube.com/watch?v=...",
]

for i, url in enumerate(video_urls):
    filename = f"dhaka_audio_{i+1:03d}.wav"
    try:
        download_audio(url, "/content/drive/MyDrive/CSE499/raw_audio/dhaka", filename)
        print(f"Downloaded: {filename}")
    except Exception as e:
        print(f"Error: {e}")
```

---

## 4. Data Naming Convention

### File Naming Format
```
{dialect}_{category}_{number}.wav
```

### Examples
```
dhaka_symptom_001.wav
sylhet_medication_002.wav
barishal_history_003.wav
kolkata_allergy_004.wav
standard_005.wav
```

### Categories
- symptom: Describing symptoms
- medication: Talking about medicines
- disease: Mentioning diseases
- history: Medical history
- allergy: Allergies
- general: General health talk

---

## 5. Audio Preprocessing

### Why Preprocess?
- Standardize sample rate (16kHz for ASR)
- Reduce file size
- Remove noise
- Consistent format

### Preprocessing Code

```python
import librosa
import soundfile as sf
import os

def preprocess_audio(input_path, output_path, target_sr=16000):
    """Preprocess audio file."""
    # Load audio
    audio, sr = librosa.load(input_path, sr=target_sr)
    
    # Remove silence from beginning and end
    trimmed, _ = librosa.effects.trim(audio, top_db=20)
    
    # Normalize volume
    max_val = max(abs(trimmed))
    if max_val > 0:
        normalized = trimmed / max_val
    else:
        normalized = trimmed
    
    # Save
    sf.write(output_path, normalized, target_sr)
    print(f"Saved: {output_path}")

# Process all files in folder
def preprocess_folder(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    
    for filename in os.listdir(input_folder):
        if filename.endswith('.wav'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            preprocess_audio(input_path, output_path)
```

### Preprocessing Steps
1. Resample to 16kHz
2. Convert to mono
3. Normalize volume
4. Remove silence
5. Trim to reasonable length (max 5 min)

---

## 6. Manual Transcription

### What is Transcription?
Writing down exactly what is spoken in the audio.

### Transcription Guidelines
- Write exactly what you hear
- Include filler words (আমি মানে, এটা...)
- Keep spelling as pronounced
- Mark unclear parts with [unclear]
- Use Bengali script

### Example
**Audio:** "আমার গতকাল থেকে মাথা ঘুরছে, আর বুকে একটা ব্যথা হচ্ছে"

**Transcription:**
```
আমার গতকাল থেকে মাথা ঘুরছে এবং বুকে ব্যথা হচ্ছে
```

### Save Transcription Format
```text
File: dhaka_symptom_001.wav
Transcription: আমার গতকাল থেকে মাথা ঘুরছে এবং বুকে ব্যথা হচ্ছে
Duration: 15 seconds
Date: 2024-01-15
Notes: Clear audio, standard Dhaka dialect
```

---

## 7. NER Annotation

### What is NER Annotation?
Labeling entities in text (symptoms, diseases, medications, etc.)

### BIO Format

| Tag | Meaning | Example |
|-----|---------|---------|
| O | Outside (no entity) | আমার |
| B-TYPE | Begin entity | মাথা (B-SYMPTOM) |
| I-TYPE | Inside entity | ঘুরছে (I-SYMPTOM) |

### Example Annotation
```
আমার    O
গতকাল  O
থেকে   O
মাথা   B-SYMPTOM
ঘুরছে  I-SYMPTOM
এবং    O
জ্বর   B-SYMPTOM
।      O
প্যারা  B-MEDICATION
সিটা   I-MEDICATION
মল    I-MEDICATION
খেয়েছি O
```

### Entity Types
- SYMPTOM: শ্বাসকষ্ট, কাশি, জ্বর
- DISEASE: ডায়াবেটিস, উচ্চ রক্তচাপ
- MEDICATION: প্যারাসিটামল, ইনসুলিন
- DURATION: ৩ দিন, এক সপ্তাহ
- ALLERGY: পেনিসিলিনে অ্যালার্জি
- BODY_PART: মাথা, বুক, পেট
- TREATMENT: অপারেশন, থেরাপি
- DOSAGE: দুই টি, দিনে তিন বার

### Annotation Tool
Use Google Sheets or Label Studio for annotation.

---

## 8. Dataset Organization

### Folder Structure

```
CSE499_Dataset/
├── raw_audio/
│   ├── dhaka/
│   │   ├── dhaka_001.wav
│   │   ├── dhawa_002.wav
│   │   └── ...
│   ├── sylhet/
│   ├── barishal/
│   ├── standard/
│   └── kolkata/
├── transcripts/
│   ├── dhawa/
│   │   ├── dhawa_001.txt
│   │   └── ...
│   └── ...
├── annotations/
│   ├── train.json
│   ├── validation.json
│   └── test.json
├── metadata/
│   ├── collection_log.csv
│   ├── dialect_distribution.csv
│   └── dataset_manifest.json
└── processed/
    ├── train/
    ├── validation/
    └── test/
```

### Metadata Format (collection_log.csv)
```csv
filename,dialect,source,source_url,download_date,duration_sec,transcription_status
dhawa_001.wav,dhawa,YouTube,https://youtube.com/...,2024-01-15,15,completed
sylhet_001.wav,sylhet,YouTube,https://youtube.com/...,2024-01-16,20,pending
```

---

## 9. Existing Bangla Datasets

### Free Available Datasets

| Dataset | Description | Link |
|---------|-------------|------|
| Mozilla Common Voice (Bengali) | ~400 hours Bengali speech | commonvoice.mozilla.org |
| OpenSLR Bengali | Speech corpus for Bengali | openslr.org |
| BanglaLDC | Bengali speech dataset | (register for access) |
| Bangla-HealthNER | Medical NER dataset | Hugging Face |

### How to Use Existing Datasets

```python
from datasets import load_dataset

# Load Mozilla Common Voice Bengali
dataset = load_dataset("mozilla-foundation/common_voice", "bn")
print(dataset)
```

### Supplement with Your Data
Use existing datasets for:
- Pre-training / base model training
- Adding diversity
- Testing generalization

Your custom data for:
- Medical domain adaptation
- Dialect-specific training
- End-to-end evaluation

---

## 10. Data Split

### Train/Validation/Test Split

| Split | Percentage | Purpose |
|-------|------------|---------|
| Train | 80% | Model training |
| Validation | 10% | Hyperparameter tuning |
| Test | 10% | Final evaluation |

### Example
```
Total: 300 samples
- Train: 240 samples
- Validation: 30 samples
- Test: 30 samples
```

### Stratified Split
Ensure each dialect is represented proportionally in each split.

---

## 11. Data Quality Guidelines

### Audio Quality Checklist
- [ ] Clear speech, minimal background noise
- [ ] Single speaker (no overlapping voices)
- [ ] No music or sound effects
- [ ] Duration between 10 seconds - 5 minutes
- [ ] Proper volume levels

### Transcription Quality Checklist
- [ ] Exactly matches audio
- [ ] Uses correct Bengali spelling
- [ ] Includes all spoken words
- [ ] No additions or omissions
- [ ] Proper punctuation

### Annotation Quality Checklist
- [ ] Consistent labeling
- [ ] Correct entity boundaries
- [ ] All entities labeled
- [ ] No overlapping entities
- [ ] Follows BIO format

---

## 12. Sharing Dataset with Team

### Google Drive Sharing
1. Create folder "CSE499_Dataset"
2. Right-click → Share
3. Add team members with "Editor" access
4. Use consistent folder structure

### Download/Upload Workflow
```
Member A downloads files → works locally → uploads to Drive
Member B syncs Drive → downloads files → works locally
```

### Important Notes
- Don't upload large files to GitHub
- Keep master copy on Google Drive
- Document any changes made to dataset

---

## 13. Legal Considerations

### YouTube Terms
- YouTube TOS allows personal use
- Don't redistribute copyrighted content
- Use for research/education purposes
- Credit original sources if possible

### Data Privacy
- Don't collect real patient data without consent
- Anonymize any personal information
- Follow ethical guidelines

---

## Summary

### Key Points
1. Collect 50+ samples per dialect
2. Use consistent naming
3. Preprocess all audio to 16kHz
4. Transcribe manually for training
5. Annotate entities in BIO format
6. Keep metadata organized
7. Share via Google Drive

### Next Steps
1. Start YouTube search for each dialect
2. Download first 10 samples
3. Transcribe first batch
4. Preprocess audio
5. Begin model training

---

*Dataset knowledge complete. Ready to collect data.*
