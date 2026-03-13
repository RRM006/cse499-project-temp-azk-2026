# Quick Start Guide

## CSE499: EHR-Based Pre-Consultation Medical Documentation System

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-repo/cse499-bangla-ehr.git
cd cse499-bangla-ehr
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Google Drive (for Colab)

Mount Google Drive and create project folders:

```python
from 00_Setup.drive_mount_helper import initialize_project

folders = initialize_project()
```

### 4. Start Data Collection (Phase 0)

Use the YouTube downloader to collect audio data:

```python
from 02_Phase1_ASR.scripts.youtube_downloader import YouTubeDownloader

downloader = YouTubeDownloader("./raw_audio")
downloader.download_batch("urls.csv")
```

### 5. Preprocess Audio

```python
from 02_Phase1_ASR.scripts.data_preprocessing import process_directory

process_directory(
    input_dir="./raw_audio",
    output_dir="./processed_audio",
    target_sr=16000
)
```

---

## Project Phases

### Phase 1: ASR (Speech Recognition)

**Goal:** Convert Bangla speech to text

**Models to try:**
- Whisper (recommended - easiest)
- Wav2Vec2
- HuBERT
- WavLM
- Data2Vec

**Training:**
```python
from 02_Phase1_ASR.scripts.whisper_finetune import train_whisper

trainer = train_whisper(
    model_name="openai/whisper-small",
    train_dataset=train_data,
    eval_dataset=eval_data,
    output_dir="./models/whisper_finetuned"
)
trainer.train()
```

**Evaluation:**
```python
from 02_Phase1_ASR.scripts.evaluate_wer import evaluate_single_file

result = evaluate_single_file(
    model_path="./models/whisper_finetuned",
    audio_path="test.wav",
    reference_text="বাংলা টেক্সট",
    model_type="whisper"
)
print(f"WER: {result['wer']}")
```

### Phase 2: NER (Entity Extraction)

**Goal:** Extract medical entities from text

**Entity Types:**
- SYMPTOM
- DISEASE
- MEDICATION
- DURATION
- ALLERGY
- BODY_PART
- TREATMENT
- DOSAGE

**Annotation:** See `03_Phase2_NER/01_Annotation_Tools/annotation_guidelines.md`

**Training:**
```python
from 03_Phase2_NER.scripts.banglabert_train import train_ner_model

trainer = train_ner_model(
    model_name="csebuetnlp/banglabert",
    train_data=train_annotations,
    eval_data=val_annotations,
    output_dir="./models/banglabert_ner"
)
trainer.train()
```

### Phase 3: EHR Generation

**Goal:** Create structured EHR from entities

**Usage:**
```python
from 04_Phase3_EHR.scripts.ehr_generator import EHRGenerator

generator = EHRGenerator()
ehr = generator.generate(
    entities=extracted_entities,
    transcription=transcribed_text,
    patient_id="PAT_001",
    dialect="dhaka"
)

# Get human-readable output
print(generator.to_text(ehr))
```

---

## Complete Pipeline

```python
from 05_Integration.scripts.ehr_pipeline import EHRPipeline

# Initialize pipeline
pipeline = EHRPipeline(
    asr_model_path="./models/whisper_finetuned",
    asr_model_type="whisper",
    ner_model_path="./models/banglabert_ner"
)

# Process audio
result = pipeline.process(
    audio_path="patient_audio.wav",
    patient_id="PAT_001",
    dialect="dhaka"
)

# Get results
print(result["transcription"])  # Phase 1 output
print(result["entities"])       # Phase 2 output  
print(result["ehr"])            # Phase 3 output
```

---

## Colab Setup

### First Time Setup

```python
# Mount Drive
from google.colab import drive
drive.mount('/content/drive')

# Install packages
!pip install -r requirements.txt
```

### Saving Work

Always save to Google Drive:
```python
# Save model
model.save_pretrained('/content/drive/MyDrive/CSE499/models/my_model')

# Save checkpoint during training
trainer.save_model('/content/drive/MyDrive/CSE499/checkpoints/epoch_1')
```

---

## Directory Structure

```
CSE499_Project/
├── 00_Setup/              # Setup scripts
├── 01_Dataset/            # Data (keep on Drive)
├── 02_Phase1_ASR/         # Speech recognition
├── 03_Phase2_NER/        # Entity extraction
├── 04_Phase3_EHR/        # EHR generation
├── 05_Integration/       # Complete pipeline
├── 06_Documentation/     # Reports
└── 08_Shared_Resources/  # Utilities
```

---

## Tips

1. **Save often** - Colab can disconnect unexpectedly
2. **Use GPU** - Training is much faster with GPU
3. **Document** - Keep notes on what works
4. **Test early** - Don't wait until the end to test
5. **Start simple** - Use Whisper first before other models

---

## Support

- Check `guide/` folder for detailed guides
- See `promt.md` for code generation prompts
- Ask your supervisor for clarifications
