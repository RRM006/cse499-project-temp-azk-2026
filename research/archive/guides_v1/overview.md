# Project Overview Guide

## CSE499: EHR-Based Pre-Consultation Medical Documentation System

---

## 1. What Is This Project?

### Project Title
**EHR-Based Pre-Consultation Medical Documentation System**

### Problem Statement
When patients visit a doctor, they need to explain their medical history and symptoms. This takes valuable time. The doctor must also document everything manually.

### Our Solution
An AI system that:
1. **Listens** to patient's voice (in Bangla)
2. **Converts** speech to text automatically
3. **Extracts** medical information (symptoms, diseases, medicines)
4. **Creates** a structured Electronic Health Record (EHR)

---

## 2. Why This Project?

### Real-World Need
- Doctors spend too much time on documentation
- Patients in Bangladesh often speak in local dialects
- Bangla-English mixing is common
- Manual documentation is error-prone

### Project Benefits
- Saves doctor time
- Helps patients communicate easily
- Creates accurate records
- Works with multiple Bangla dialects

---

## 3. System Architecture

### Three-Phase Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                         PATIENT INPUT                           │
│              (Voice in Bangla/Dialect/Code-mixed)               │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PHASE 1: SPEECH TO TEXT                      │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Input: Audio File (.wav)                                  │  │
│  │  Process: ASR Model (Whisper, Wav2Vec2, etc.)            │  │
│  │  Output: Bengali Text Transcription                      │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                   PHASE 2: ENTITY EXTRACTION                    │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Input: Bengali Text                                      │  │
│  │  Process: NER Model (BanglaBERT, XLM-R, etc.)            │  │
│  │  Output: Tagged Medical Entities                          │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                      PHASE 3: EHR GENERATION                    │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Input: Extracted Entities                                │  │
│  │  Process: Rule-based Template Filler                       │  │
│  │  Output: Structured EHR (JSON + Human Readable)          │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DOCTOR REVIEW                              │
│              (Structured EHR for Consultation)                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. Key Features

### Language Support
- **Primary**: Bengali (Bangla)
- **Dialects**: Dhaka, Sylhet, Barishal, Standard, Kolkata
- **Code-mixing**: Bengali + English (natural in Bangladesh)

### Medical Entities Extracted
| Entity | Example | Bengali |
|--------|---------|---------|
| Symptoms | Fever, headache | জ্বর, মাথা ঘোরা |
| Diseases | Diabetes, BP | ডায়াবেটিস, উচ্চ রক্তচাপ |
| Medications | Paracetamol | প্যারাসিটামল |
| Duration | 3 days | ৩ দিন |
| Allergies | Penicillin allergy | পেনিসিলিনে অ্যালার্জি |
| Body parts | Chest, stomach | বুক, পেট |

---

## 5. Technical Details

### Phase 1: ASR (Speech Recognition)

**Models Used:**
- Whisper (OpenAI) - Primary model
- Wav2Vec2 (Facebook)
- HuBERT (Facebook)
- WavLM (Microsoft)
- XLSR-53 (Cross-lingual)
- And more...

**Training:**
- Collect audio from YouTube
- Manual transcription
- Fine-tune pre-trained models

**Metric:** Word Error Rate (WER) - Lower is better

---

### Phase 2: NER (Entity Recognition)

**Models Used:**
- BanglaBERT - Primary model
- XLM-RoBERTa
- mBERT
- DistilBERT
- ELECTRA

**Training:**
- Annotate transcriptions with entity labels
- Train token classification model

**Metric:** F1-Score - Higher is better

---

### Phase 3: EHR Generator

**Process:**
1. Take extracted entities from Phase 2
2. Map to EHR template fields
3. Generate structured JSON
4. Create human-readable report

**Output Format:**
```json
{
  "patient_id": "AUTO_001",
  "chief_complaint": {
    "symptoms": [{"name": "জ্বর", "duration": "২ দিন"}],
  },
  "medical_history": {
    "diseases": ["ডায়াবেটিস"],
    "medications": ["ইনসুলিন"],
    "allergies": []
  }
}
```

---

## 6. Dataset

### What We Collect
- **Audio**: 50+ samples per dialect
- **Transcriptions**: Manual text for each audio
- **Annotations**: Entity labels for NER training

### Sources
- YouTube (health interviews, medical consultations)
- Medical talk shows
- Patient interviews (with permission)

### Total Target
- 250+ audio files (50 × 5 dialects)
- 500+ annotated samples for NER

---

## 7. Tools & Resources

### Free Tools Used

| Tool | Purpose |
|------|---------|
| Google Colab | Coding & Training |
| Google Drive | File Storage |
| GitHub | Code Version Control |
| Hugging Face | Pre-trained Models |
| YouTube | Data Source |

### Budget: ৳0 (Zero Taka)
All tools are free for students!

---

## 8. Team Structure

### Members: 2-3 people

**Suggested Roles:**
- **ASR Specialist**: Phase 1 (Speech Recognition)
- **NER Specialist**: Phase 2 (Entity Extraction)
- **Integration Lead**: Phase 3 + Full Pipeline

**Collaboration:**
- Shared Google Drive folder
- GitHub repository
- Weekly meetings

---

## 9. Timeline

### Total Duration: 14-18 weeks (3-4 months)

| Phase | Weeks | Key Milestone |
|-------|-------|---------------|
| Phase 1 | 1-9 | Working ASR model |
| Phase 2 | 10-15 | Working NER model |
| Phase 3 | 15-17 | Complete EHR system |
| Buffer | 17-18 | Final testing & docs |

---

## 10. Success Metrics

### Phase 1 (ASR)
- Word Error Rate (WER) < 30%
- Works on all 5 dialects
- Handles code-mixing

### Phase 2 (NER)
- F1-Score > 75%
- Extracts 6+ entity types
- Works on unseen data

### Phase 3 (EHR)
- Valid JSON output
- Human-readable format
- End-to-end works

### Overall
- Faculty demo successful
- Documentation complete
- Code reproducible

---

## 11. Challenges & Solutions

### Challenge: Limited Data
**Solution:** Use pre-trained models + YouTube data + existing datasets

### Challenge: Multiple Dialects
**Solution:** Collect dialect-specific data, fine-tune per dialect or use dialect-aware models

### Challenge: Code-mixing
**Solution:** Train on code-mixed examples, use multilingual models

### Challenge: Colab Time Limits
**Solution:** Save checkpoints frequently, use Drive for storage

### Challenge: No Budget
**Solution:** Use free tools (Colab, Drive, GitHub, Hugging Face)

---

## 12. Project Deliverables

### For Faculty Submission
1. **Working System**: End-to-end pipeline demo
2. **Code**: Clean, commented, on GitHub
3. **Documentation**: Project report, README files
4. **Presentation**: Slides explaining approach
5. **Results**: WER, F1-scores, sample outputs

### What Faculty Will See
1. Live demo with sample audio
2. System converting speech to EHR
3. Performance metrics
4. Architecture explanation
5. Future improvements

---

## 13. Learning Outcomes

### Skills You'll Gain
- Deep Learning (PyTorch)
- NLP (Transformers, BERT)
- Speech Processing (ASR)
- Data Collection & Annotation
- Project Management
- Team Collaboration

### Knowledge You'll Learn
- How speech recognition works
- How named entity recognition works
- How to build ML pipelines
- Medical NLP basics
- Bengali language processing

---

## 14. Next Steps

### This Week
1. Set up Google Colab account
2. Mount Google Drive
3. Create project folder structure
4. Start YouTube search for data

### This Month
1. Collect 100+ audio samples
2. Complete Phase 1 baseline
3. Start manual transcription

### This Semester
1. Complete all three phases
2. Document everything
3. Present to faculty

---

## Quick Summary

| Aspect | Detail |
|--------|--------|
| **Project** | Voice to EHR for Bangla medical speech |
| **3 Phases** | ASR → NER → EHR Template |
| **Dialects** | Dhaka, Sylhet, Barishal, Standard, Kolkata |
| **Tools** | Free (Colab, Drive, GitHub, HuggingFace) |
| **Timeline** | 3-4 months |
| **Team** | 2-3 members |
| **Budget** | ৳0 |

---

## Questions?

If you have questions about any part of this project:
1. Check this guide first
2. Check the other guide files
3. Ask team members
4. Ask your supervisor

---

*Overview complete. Start your CSE499 journey!*
