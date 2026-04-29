# Guide2_0 - Quick Reference

## Files in This Folder

| File | Purpose |
|------|---------|
| `quickstart.md` | How to start Phase 1 immediately |
| `phase1_checklist.md` | Complete week-by-week checklist for Phase 1 |
| `commands.md` | Essential commands reference |
| `troubleshooting.md` | Common problems and solutions |

---

## How to Use

1. **Start Here**: Read `quickstart.md` first
2. **Follow Along**: Use `phase1_checklist.md` to track progress
3. **Quick Help**: Use `commands.md` for commands
4. **Problems**: Check `troubleshooting.md` when stuck

---

## Project Overview

**EHR-Based Pre-Consultation Medical Documentation System**
- Team: 3 Members | Deadline: 2 Months | Budget: Zero (Colab + Drive)
- A patient speaks in Bangla (any dialect) → System listens → Produces structured EHR for doctor

## 3-Phase Pipeline

| Phase | Input | Output |
|-------|-------|--------|
| Phase 1 — ASR | Raw audio (.wav) | Bangla text transcripts |
| Phase 2 — NER | Text transcripts | Medical entities (SYMPTOM, DISEASE, MEDICATION...) |
| Phase 3 — EHR | Medical entities | Structured JSON EHR file |

---

## Google Drive Folder Structure

```
CSE499_EHR_Project/               ← Root (shared Drive folder)
├── 00_Admin/
├── 01_Dataset/
│   ├── raw_audio/
│   │   ├── puran_dhaka/
│   │   ├── barishal/
│   │   ├── sylheti/
│   │   ├── normal_bangla/
│   │   └── indian_bangla/
│   ├── cleaned_audio/
│   ├── transcripts/
│   │   ├── manual/
│   │   └── auto/
│   ├── metadata/
│   └── ner_labeled/
├── 02_Phase1_ASR/
│   ├── notebooks/
│   ├── model_outputs/
│   ├── evaluation/
│   └── saved_models/
│       └── whisper_finetuned/
├── 03_Phase2_NER/
├── 04_Phase3_EHR/
├── 05_Pipeline/
└── 06_Presentation/
```

---

## 2-Month Timeline Summary

| Week | Focus |
|------|-------|
| Week 1 | Setup + folder structure + GitHub |
| Week 2 | Data collection — download audio by dialect |
| Week 3 | Run 10+ ASR models, collect transcripts, compare WER |
| Week 4 | Fine-tune Whisper on dialect dataset |
| Week 5 | Final transcripts + start Phase 2 NER dataset |
| Week 6 | Run 6+ NER models, label medical entities, compare F1 |
| Week 7 | Fine-tune BanglaBERT + build EHR JSON filler |
| Week 8 | End-to-end test + demo + presentation slides |

---

## Team Roles

| Member | Role | Main Tasks |
|--------|------|------------|
| Member 1 (Lead) | ASR Engineer | Dataset download, audio cleaning, Phase 1 model comparison, Whisper fine-tuning |
| Member 2 | NLP Engineer | NER dataset labeling, Phase 2 model comparison, BanglaBERT fine-tuning |
| Member 3 | Integration + Presentation | Phase 3 EHR generator, full pipeline notebook, slides, demo video |

---

## Important Rules

- **Save EVERYTHING to Drive** — Colab local storage resets every session
- **Audio files and model weights** → Google Drive
- **Code (notebooks)** → GitHub
- **Save checkpoints every 500 steps** during any training run
- **Never skip a step** — each phase feeds into the next
