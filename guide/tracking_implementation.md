# Implementation Tracking Guide

## CSE499: EHR-Based Pre-Consultation Medical Documentation System

---

## Quick Reference: File Locations

After creating the implementation, files are located at:

```
implementation/
├── 00_Setup/
│   ├── environment_setup.py          # Colab setup script
│   └── drive_mount_helper.py         # Google Drive helper
│
├── 01_Dataset/                        # Dataset (audio, transcriptions)
│   ├── 01_Raw_Audio/                 # Original downloads
│   ├── 02_Transcriptions/           # Manual transcriptions
│   ├── 03_Processed_Audio/           # Preprocessed (16kHz mono)
│   ├── 04_Annotations/              # NER annotations
│   └── 05_Metadata/                 # Collection logs
│
├── 02_Phase1_ASR/                    # Phase 1: Speech Recognition
│   ├── 01_Baseline/                 # Pre-trained model tests
│   ├── 02_Models/                   # Trained models (save here!)
│   ├── 03_Scripts/                   # Training scripts
│   ├── 04_Results/                   # WER scores
│   └── 05_Transcripts/              # Output transcriptions
│
├── 03_Phase2_NER/                    # Phase 2: Entity Recognition
│   ├── 01_Annotation_Tools/          # Guidelines & tools
│   ├── 02_Data/                      # Train/val/test JSON
│   ├── 03_Models/                    # Trained models (save here!)
│   ├── 04_Scripts/                   # Training scripts
│   └── 05_Results/                   # F1 scores
│
├── 04_Phase3_EHR/                    # Phase 3: EHR Generation
│   ├── 01_Templates/                 # JSON templates
│   ├── 02_Mapping_Rules/            # Entity mapping config
│   ├── 03_Scripts/                   # Generator scripts
│   └── 04_Samples/                  # Example outputs
│
├── 05_Integration/                   # Complete Pipeline
│   ├── 01_Pipeline/                 # ehr_pipeline.py
│   ├── 02_Demo/                     # Demo notebooks
│   └── 03_Testing/                  # Tests
│
└── 08_Shared_Resources/             # Utilities
    ├── constants.py                  # Project constants
    └── utilities.py                  # Helper functions
```

---

## Phase 0: Dataset Collection (Weeks 1-3)

### Task Checklist

- [ ] **Week 1**: Set up Google Drive with folder structure
- [ ] **Week 1**: Install packages in Colab
- [ ] **Week 1**: Create YouTube URL spreadsheet
- [ ] **Week 2**: Download audio files (target: 300+)
- [ ] **Week 2**: Create manual transcription workflow
- [ ] **Week 3**: Transcribe all audio files
- [ ] **Week 3**: Preprocess audio (16kHz, mono)
- [ ] **Week 3**: Create train/val/test split

### Files to Use

| Task | Script/File |
|------|-------------|
| Download audio | `implementation/02_Phase1_ASR/03_Scripts/youtube_downloader.py` |
| Preprocess audio | `implementation/02_Phase1_ASR/03_Scripts/data_preprocessing.py` |
| Setup Drive | `implementation/00_Setup/drive_mount_helper.py` |

---

## Phase 1: ASR - Speech Recognition (Weeks 4-12)

### Task Checklist

- [ ] **Week 4**: Test baseline Whisper (no fine-tuning)
- [ ] **Week 4**: Calculate baseline WER
- [ ] **Week 5**: Fine-tune Whisper-small
- [ ] **Week 6**: Fine-tune Wav2Vec2
- [ ] **Week 7**: Fine-tune HuBERT
- [ ] **Week 8**: Fine-tune WavLM
- [ ] **Week 9**: Test additional models (Data2Vec, XLSR-53)
- [ ] **Week 10**: Test inference-only models (Canary, MMS)
- [ ] **Week 11**: Compare all models (create WER table)
- [ ] **Week 12**: Select best model, save checkpoint

### Files to Use

| Task | Script/File |
|------|-------------|
| Fine-tune Whisper | `implementation/02_Phase1_ASR/03_Scripts/whisper_finetune.py` |
| Evaluate WER | `implementation/02_Phase1_ASR/03_Scripts/evaluate_wer.py` |
| Save model | Use: `model.save_pretrained('/content/drive/.../02_Phase1_ASR/02_Models/whisper_finetuned')` |

### Model Comparison Table

Create this table in `implementation/02_Phase1_ASR/04_Results/`:

| Model | WER Dhaka | WER Sylhet | WER Chittagong | WER Barishal | WER Standard | WER Kolkata | Overall |
|-------|-----------|------------|----------------|--------------|--------------|-------------|---------|
| Whisper Baseline | | | | | | | |
| Whisper Fine-tuned | | | | | | | |
| Wav2Vec2 | | | | | | | |
| HuBERT | | | | | | | |
| WavLM | | | | | | | |
| Data2Vec | | | | | | | |
| XLSR-53 | | | | | | | |
| Canary | | | | | | | |
| MMS | | | | | | | |

**Target**: WER < 30%

---

## Phase 2: NER - Entity Extraction (Weeks 13-22)

### Task Checklist

- [ ] **Week 13**: Create annotation guidelines
- [ ] **Week 13**: Set up annotation workflow
- [ ] **Weeks 13-16**: Annotate 500+ samples
- [ ] **Week 17**: Convert annotations to JSON format
- [ ] **Week 17**: Create train/val/test splits
- [ ] **Week 18**: Fine-tune BanglaBERT
- [ ] **Week 19**: Fine-tune XLM-RoBERTa
- [ ] **Week 20**: Fine-tune mBERT
- [ ] **Week 21**: Fine-tune DistilBERT, ELECTRA
- [ ] **Week 22**: Compare models, select best

### Files to Use

| Task | Script/File |
|------|-------------|
| Annotation Guidelines | `implementation/03_Phase2_NER/01_Annotation_Tools/annotation_guidelines.md` |
| Convert to NER format | `implementation/03_Phase2_NER/04_Scripts/convert_to_ner_format.py` |
| Train BanglaBERT | `implementation/03_Phase2_NER/04_Scripts/banglabert_train.py` |
| Save model | Use: `model.save_pretrained('/content/drive/.../03_Phase2_NER/03_Models/banglabert')` |

### Entity Types

| Entity | Example (Bangla) |
|--------|------------------|
| SYMPTOM | জ্বর, কাশি, মাথা ঘুরা |
| DISEASE | ডায়াবেটিস, উচ্চ রক্তচাপ |
| MEDICATION | প্যারাসিটামল, ইনসুলিন |
| DURATION | ৩ দিন, এক সপ্তাহ |
| ALLERGY | পেনিসিলিনে অ্যালার্জি |
| BODY_PART | মাথা, বুক, পেট |
| TREATMENT | অপারেশন, থেরাপি |
| DOSAGE | দুই টি, দিনে তিন বার |

### Model Comparison Table

Create this table in `implementation/03_Phase2_NER/05_Results/`:

| Model | Precision | Recall | F1-Score |
|-------|-----------|--------|----------|
| BanglaBERT | | | |
| XLM-RoBERTa-base | | | |
| XLM-RoBERTa-large | | | |
| mBERT | | | |
| DistilBERT | | | |
| ELECTRA | | | |

**Target**: F1 > 75%

---

## Phase 3: EHR Generation (Weeks 23-28)

### Task Checklist

- [ ] **Week 23**: Review EHR template
- [ ] **Week 23**: Customize entity mapping if needed
- [ ] **Week 24**: Test entity mapper with sample data
- [ ] **Week 25**: Generate human-readable output
- [ ] **Week 26**: Handle edge cases
- [ ] **Week 27**: Integration testing
- [ ] **Week 28**: Final testing

### Files to Use

| Task | Script/File |
|------|-------------|
| EHR Template | `implementation/04_Phase3_EHR/01_Templates/ehr_template.json` |
| Entity Mapping | `implementation/04_Phase3_EHR/02_Mapping_Rules/entity_mapping.json` |
| Generator | `implementation/04_Phase3_EHR/03_Scripts/ehr_generator.py` |

---

## Phase 4: Integration & Demo (Weeks 29-34)

### Task Checklist

- [ ] **Week 29**: Integrate all phases
- [ ] **Week 29**: Test complete pipeline
- [ ] **Week 30**: Create demo notebook
- [ ] **Week 31**: Prepare presentation slides
- [ ] **Week 32**: Final testing
- [ ] **Week 33**: Faculty presentation
- [ ] **Week 34**: Submit documentation

### Files to Use

| Task | Script/File |
|------|-------------|
| Pipeline | `implementation/05_Integration/01_Pipeline/ehr_pipeline.py` |
| Quick Start | `implementation/06_Documentation/QUICK_START.md` |

---

## Daily Tracking Template

```
Date: YYYY-MM-DD
Week: X, Day: Y

TASKS COMPLETED:
- [ ] Task 1
- [ ] Task 2

PROBLEMS ENCOUNTERED:
- Problem 1: [description]

SOLUTIONS:
- Solution 1: [what worked]

NEXT DAY PRIORITY:
- [ ] Priority 1

HOURS WORKED: X hours
```

---

## Weekly Summary Template

```
Week: X
Phase: [Phase 1/2/3]

WEEKLY GOALS:
- [ ] Goal 1

GOALS ACHIEVED:
- [x] Goal 1 - completed

METRICS THIS WEEK:
- WER: X.XX%
- F1-Score: X.XX%
- Samples: X collected/annotated

BLOCKERS:
- [ ] Blocker 1

TEAM CONTRIBUTION:
- Member 1: [tasks]
- Member 2: [tasks]

NOTES:
```

---

## Checkpoint Save Locations

| What | Where to Save |
|------|---------------|
| ASR Checkpoints | `implementation/02_Phase1_ASR/02_Models/[model_name]/` |
| NER Checkpoints | `implementation/03_Phase2_NER/03_Models/[model_name]/` |
| Dataset | `implementation/01_Dataset/` (entire folder on Drive) |
| Results | `implementation/02_Phase1_ASR/04_Results/` or `03_Phase2_NER/05_Results/` |

---

## Important Reminders

1. **Save frequently** - Colab can disconnect anytime
2. **Always save to Google Drive** - don't lose your work
3. **Document results** - write down WER/F1 scores immediately
4. **Test early** - test components as you build them
5. **Keep originals** - don't modify raw data

---

*Implementation tracking complete. Start building!*
