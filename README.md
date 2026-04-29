# CSE499: EHR-Based Pre-Consultation Medical Documentation System

**North South University | Department of Electrical & Computer Engineering**

---

## Project Overview

This is a CSE499 capstone project that develops an AI system to automatically convert patient voice input in Bangla (including multiple dialects and Bangla-English code-mixed speech) into structured Electronic Health Records (EHR).

### Core Functionality

The system operates as a five-stage pipeline:
1. **Patient Speech Capture** - Voice input via kiosk/tablet.
2. **Automatic Speech Recognition (ASR)** - Converts Bangla dialect/code-mixed speech to text.
3. **Medical Named Entity Recognition (NER)** - Extracts symptoms, diseases, medications, etc.
4. **Structured EHR Construction** - Normalizes and structures the data.
5. **Doctor Dashboard** - Displays EHR, original transcript, and differential-diagnosis hints.

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

```text
┌─────────────────────────────────────────────────────────────┐
│                 STAGE 1: PATIENT SPEECH                     │
│         (Bangla / Dialects / Code-mixed Speech)             │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                 STAGE 2: ASR (Speech to Text)               │
│  Models: BengaliAI, Whisper, Wav2Vec2, Qwen3-ASR...         │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                 STAGE 3: Medical NER                        │
│  Extraction: Symptoms, meds, duration, allergies            │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                 STAGE 4: Structured EHR                     │
│  Standard format (JSON + Human Readable)                    │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                 STAGE 5: Doctor Dashboard                   │
│  UI with EHR, transcript, and differential-diagnosis hints  │
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

### ASR Models Evaluated
- **Baseline Models:** Whisper (Small/Medium/Large/Turbo), Wav2Vec2 (XLSR-53, 300M, CV-Bengali), MMS, Vakyansh-Bn, BengaliAI Whisper, BengaliAI Regional, SeamlessM4T. (Strongest: BengaliAI Regional)
- **Larger Multimodal Models:** Qwen2-Audio, Qwen3-ASR-1.7B, Voxtral-Mini, Phi-4 Multimodal, Qwen2.5-Omni. 
- **Fine-Tuning Target:** Qwen3-ASR-1.7B (using LoRA)

### NER & Application Stack
- **NER Model:** BanglaBERT (Token Classification)
- **Planned Backend:** FastAPI, PostgreSQL
- **Planned Frontend:** React / Next.js (Dashboard), Flutter / PWA (Patient App)

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

### Key Software Components
| Tool | Purpose |
|------|---------|
| **Python 3.10 / PyTorch** | Core implementation and deep learning framework |
| **HF Transformers / Datasets** | Model loading, inference, and fine-tuning (PEFT/LoRA) |
| **WhisperX** | Long-form audio segmentation and forced alignment |
| **Librosa / FFmpeg** | Audio I/O and preprocessing |
| **Google Colab (T4, A100)** | Primary GPU compute |
| **yt-dlp** | Public-source audio collection |

**Budget:** ৳0 (Zero Taka - All tools are free)

---

## Repository Structure

```
cse499-project/
├── notebooks/                          # Colab notebooks (active work)
│   ├── 00_project_setup.ipynb         # Environment & Drive setup
│   ├── 01_data_download.ipynb         # YouTube data collection
│   ├── 02_audio_preprocessing.ipynb   # Audio segmentation & cleaning
│   ├── 03_model_comparison.ipynb      # Baseline ASR model evaluation
│   ├── 04_bigger_model_comparison.ipynb # Larger ASR model evaluation
│   └── 05_chatbot_comparison.ipynb    # Phase 5: AI chatbot EHR comparison
│
├── evaluation/                         # Model evaluation results
│   ├── baseline_models/               # WER scores, charts, confusion matrices
│   └── bigger_models/                 # Larger model metrics & comparisons
│
├── docs/                               # Written deliverables
│   ├── submissions/                   # Graded assignment PDFs + LaTeX source
│   └── literature_reviews/            # Paper reviews (EHR + other topics)
│
├── presentations/                      # Slide decks for demos & defenses
│
├── research/                           # Exploratory & background work
│   ├── ideas/                         # Early project idea proposals
│   ├── pitch_decks/                   # Pitch presentations (pre-selection)
│   ├── gap_analysis_templates/        # Templates for paper reading & gaps
│   └── archive/                       # Old drafts, guides, & backups
│
├── context_and_task.md                 # Project context & phase descriptions
├── requirements.txt                    # Python dependencies
└── README.md                           # This file
```

---

## Project Progress / Phases

| Phase | Description | Status |
|-------|-------------|--------|
| **Phase 1** | Audio collection & preprocessing (4.7h multi-dialect Bangla) | Completed |
| **Phase 2** | Baseline ASR benchmark (12 open-source models) | Completed |
| **Phase 3** | Larger multimodal audio LLM benchmark (2B-7B parameters) | Completed |
| **Phase 4** | Qwen3-ASR-1.7B fine-tuning research (LoRA) | In Progress |
| **Phase 5** | Comparative chatbot output study (EHR schema design) | Pending |

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

### 4. Understand the Project
See `context_and_task.md` for the full project description and phase-by-phase progress.
See `docs/` for submissions, literature reviews, and LaTeX sources.
See `notebooks/` for the Colab notebooks (run in order: 00 → 05).

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
1. Read `context_and_task.md` for project context
2. Review `docs/` for submissions and literature reviews
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
