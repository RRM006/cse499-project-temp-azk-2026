# CSE499: EHR-Based Pre-Consultation Medical Documentation System

**North South University | Department of Electrical & Computer Engineering**

---

## Project Overview

This is a CSE499 capstone project that develops an AI system to automatically convert patient voice input in Bangla (including multiple dialects and Bangla-English code-mixed speech) into structured Electronic Health Records (EHR).

### Core Functionality

The system processes patient voice through three phases:
1. **Automatic Speech Recognition (ASR)** - Converts Bangla speech to text
2. **Medical Named Entity Recognition (NER)** - Extracts medical entities from text
3. **Rule-based EHR Template Filler** - Generates structured EHR documents

---

## Academic Information

| Detail | Information |
|--------|-------------|
| **Course** | CSE499A/B Capstone Project |
| **Supervisor** | Dr. Mohammad Ashrafuzzaman Khan (AzK) |
| **Department** | Electrical & Computer Engineering |
| **University** | North South University (NSU), Dhaka, Bangladesh |

---

## Research Team

| Name | Student ID | Role | Email |
|------|-----------|------|-------|
| M.G. Rabbi Hossen | 2222516042 | Team Member | rabbi.hossen@northsouth.edu |
| Israt Zaman Srity | 2211084042 | Team Member | israt.srity@northsouth.edu |
| Rafiur Rahman Mashrafi | 2221971042 | Team Member | rafiurmashrafi@northsouth.edu |

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    PATIENT VOICE INPUT                      │
│         (Bangla / Dialects / Code-mixed Speech)           │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  PHASE 1: ASR (Speech to Text)             │
│  Models: Whisper, Wav2Vec2, HuBERT, WavLM, XLSR-53...    │
│  Output: Bengali Text Transcription                        │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│               PHASE 2: NER (Entity Extraction)             │
│  Models: BanglaBERT, XLM-RoBERTa, mBERT, DistilBERT...    │
│  Output: Tagged Medical Entities                           │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│               PHASE 3: EHR Template Filler                 │
│  Method: Rule-based Entity Mapping                         │
│  Output: Structured EHR (JSON + Human Readable)            │
└─────────────────────────────────────────────────────────────┘
```

---

## Features

### Language Support
- **Primary Language:** Bengali (Bangla)
- **Dialects Supported:** Dhaka, Sylhet, Barishal, Standard Bangla, Kolkata (Indian Bengali)
- **Code-mixing:** Bangla-English (natural in Bangladesh)

### Medical Entities Extracted
| Entity Type | Example (Bangla) |
|-------------|-------------------|
| Symptoms | জ্বর (fever), মাথা ঘুরা (dizziness), কাশি (cough) |
| Diseases | ডায়াবেটিস (diabetes), উচ্চ রক্তচাপ (high BP) |
| Medications | প্যারাসিটামল, ইনসুলিন |
| Duration | ৩ দিন, এক সপ্তাহ |
| Allergies | পেনিসিলিনে অ্যালার্জি |
| Body Parts | মাথা, বুক, পেট |

---

## Technical Details

### Phase 1: ASR Models
- **Whisper** (OpenAI) - Primary model
- **Wav2Vec2** (Facebook AI)
- **HuBERT** (Facebook AI)
- **WavLM** (Microsoft)
- **XLSR-53** (Cross-lingual)
- **Data2Vec** (Meta)
- **Canary** (Nvidia)
- **OLMoASR**
- **Reka Speech**
- **MMS** (Meta - 1000+ languages)

### Phase 2: NER Models
- **BanglaBERT** - Primary model
- **XLM-RoBERTa**
- **mBERT**
- **DistilBERT**
- **ELECTRA**

### Phase 3: EHR Generation
- Rule-based entity mapping
- JSON template filler
- Human-readable output generator

---

## Dataset

### Data Sources
- YouTube (medical interviews, health consultations)
- Self-collected audio recordings
- Mozilla Common Voice (Bengali)

### Target Dataset
| Dialect | Target Samples |
|---------|---------------|
| Dhaka | 50+ |
| Sylhet | 50+ |
| Barishal | 50+ |
| Standard Bangla | 50+ |
| Kolkata | 50+ |
| **Total** | **250+** |

---

## Tools & Resources

### Free Tools Used
| Tool | Purpose |
|------|---------|
| Google Colab | Coding & Training |
| Google Drive | File Storage |
| GitHub | Version Control |
| Hugging Face | Pre-trained Models |
| YouTube | Data Collection |

**Budget:** ৳0 (Zero Taka - All tools are free)

---

## Repository Structure

```
CSE499_Project/
├── guide/                      # Project guides & documentation
│   ├── skill.md               # Skills needed
│   ├── planning.md            # Project planning
│   ├── dataset.md             # Dataset knowledge
│   ├── phase.md               # Phase-by-phase timeline
│   ├── promt.md               # Code generation prompts
│   ├── overview.md            # Project overview
│   └── tracking.md            # Progress tracking
├── phase1_asr/                # Phase 1: Speech Recognition
│   ├── models/               # Trained ASR models
│   ├── data/                 # Training data
│   ├── scripts/               # Training scripts
│   └── results/               # WER scores, outputs
├── phase2_ner/                # Phase 2: Entity Recognition
│   ├── models/               # Trained NER models
│   ├── data/                 # Annotated data
│   ├── scripts/               # Training scripts
│   └── results/               # F1 scores, outputs
├── phase3_ehr/                # Phase 3: EHR Generation
│   ├── templates/            # EHR templates
│   └── scripts/               # Generation scripts
├── dataset/                   # Audio & text datasets
├── notebooks/                 # Jupyter notebooks
├── docs/                      # Documentation
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

---

## Timeline

| Phase | Duration | Key Milestone |
|-------|----------|---------------|
| Phase 1: ASR | Weeks 1-9 | Working speech recognition |
| Phase 2: NER | Weeks 10-15 | Working entity extraction |
| Phase 3: EHR | Weeks 15-17 | Complete pipeline |
| Final | Weeks 17-18 | Documentation & Presentation |

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

### 3. Set Up Google Drive
Mount Google Drive in Colab for dataset and model storage.

### 4. Follow the Guides
See `/guide/` folder for detailed instructions:
- `skill.md` - Skills needed
- `phase.md` - Step-by-step execution
- `tracking.md` - Progress tracking

---

## Evaluation Metrics

### ASR (Lower is Better)
- **Word Error Rate (WER)** - Target: <30%

### NER (Higher is Better)
- **Precision, Recall, F1-Score** - Target: F1 >75%

### System
- End-to-end pipeline functionality
- EHR output accuracy

---

## Contributing

This is an academic project. For questions:
1. Check the guides in `/guide/`
2. Review phase documentation
3. Contact team members

---

## License

This project is for academic purposes.

---

## Acknowledgments

- Dr. Mohammad Ashrafuzzaman Khan (AzK) - Project Supervisor
- North South University - Academic Support
- Hugging Face - Pre-trained Models
- OpenAI - Whisper
- Meta AI - Wav2Vec2, HuBERT, Data2Vec
- Microsoft - WavLM

---

*Last Updated: March 2026*
*CSE499 Capstone Project - North South University*
