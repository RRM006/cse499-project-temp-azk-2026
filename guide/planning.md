# Project Planning Guide

## CSE499: EHR-Based Pre-Consultation Medical Documentation System

---

## 1. Project Understanding

### What Are We Building?
A system that:
1. Takes voice input from patients speaking in Bangla (various dialects)
2. Converts speech to text (ASR)
3. Extracts medical information from text (NER)
4. Creates structured Electronic Health Records (EHR)

### Target Users
- Patients (before doctor consultation)
- Doctors (receiving structured EHR)
- Healthcare system (automated documentation)

### Key Requirements
- **Language**: Bangla (primary) + English code-mixing
- **Dialects**: Dhaka, Sylhet, Barishal, Standard, Kolkata
- **Budget**: Zero (free tools only)
- **Timeline**: 3-4 months
- **Team**: 2-3 members

---

## 2. Technical Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    PATIENT VOICE INPUT                         │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 1: AUTOMATIC SPEECH RECOGNITION (ASR)                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │   Whisper   │  │  Wav2Vec2   │  │   HuBERT    │  ...      │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
│  Output: Bangla Text Transcription                             │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 2: MEDICAL NAMED ENTITY RECOGNITION (NER)              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │  BanglaBERT │  │ XLM-RoBERTa │  │    mBERT    │  ...      │
│  └─────────────┐  └─────────────┘  └─────────────┘            │
│  Output: Tagged Medical Entities                               │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 3: RULE-BASED EHR TEMPLATE FILLER                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Entity Mapping → JSON Template → Human Readable EHR   │   │
│  └─────────────────────────────────────────────────────────┘   │
│  Output: Structured EHR Document                              │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Resource Planning

### Free Tools We'll Use

| Tool | Purpose | Link |
|------|---------|------|
| Google Colab | Coding & Training | colab.research.google.com |
| Google Drive | File Storage | drive.google.com |
| GitHub | Code Version Control | github.com |
| Hugging Face | Pre-trained Models | huggingface.co |
| YouTube | Data Collection | youtube.com |

### Budget: ৳0 (Zero Taka)

All resources are free. No paid services required.

---

## 4. Team Division

### Suggested Roles (2-3 Members)

**Member 1: ASR Specialist (Phase 1)**
- Collect audio data from YouTube
- Preprocess audio files
- Train and evaluate ASR models
- Document transcription results

**Member 2: NER Specialist (Phase 2)**
- Create annotated dataset
- Train NER models
- Evaluate entity extraction
- Document NER results

**Member 3: Integration & EHR (Phase 3 + Phase 1-2 Support)**
- Build EHR template system
- Integrate all phases
- Create demonstration
- Documentation

### If Only 2 Members
- Member 1: Phase 1 + Phase 3
- Member 2: Phase 2 + Documentation

---

## 5. Risk Assessment

### Potential Problems

| Risk | Likelihood | Impact | Solution |
|------|------------|--------|----------|
| Can't collect enough data | Medium | High | Use existing datasets + small self-collected |
| Colab disconnects | High | Medium | Save checkpoints frequently |
| Models don't perform well | Medium | Medium | Use pre-trained models + fine-tune |
| Team coordination issues | Medium | Medium | Regular meetings + shared Drive |
| Can't finish on time | Low | High | Prioritize core features |

### Mitigation Strategies

1. **Data Issues**: Start with existing Bangla datasets, supplement with YouTube
2. **Time Issues**: Focus on 1-2 best models instead of all
3. **Technical Issues**: Ask for help early, use online resources
4. **Colab Limits**: Use Kaggle as backup, save everything to Drive

---

## 6. Milestones

### Milestone 1: Foundation (Week 3)
- [ ] Environment setup complete
- [ ] 50 audio samples per dialect collected
- [ ] Basic folder structure created
- [ ] All team members can access Drive

### Milestone 2: ASR Working (Week 7)
- [ ] Whisper model fine-tuned
- [ ] Transcription accuracy acceptable (WER < 30%)
- [ ] At least 2 models compared
- [ ] Phase 1 results documented

### Milestone 3: NER Working (Week 12)
- [ ] 500+ annotated samples ready
- [ ] BanglaBERT fine-tuned
- [ ] Entity extraction working
- [ ] Phase 2 results documented

### Milestone 4: Complete System (Week 15)
- [ ] Phase 3 EHR generator working
- [ ] All phases integrated
- [ ] Demo working
- [ ] Presentation ready

### Milestone 5: Submission (Week 16-18)
- [ ] Final documentation
- [ ] Code cleaned and commented
- [ ] Results compiled
- [ ] Presentation delivered

---

## 7. Weekly Schedule Template

### Weekly Meeting Agenda (30 minutes)
1. What did we accomplish?
2. What problems did we face?
3. What will we do this week?
4. Any blockers?

### Individual Work
- Minimum 5-8 hours per week per member
- Focus on assigned phase
- Document all experiments

---

## 8. File Management

### Google Drive Structure
```
My Drive/CSE499_Project/
├── 01_Dataset/
│   ├── raw_audio/
│   ├── transcripts/
│   └── processed/
├── 02_Phase1_ASR/
│   ├── models/
│   ├── scripts/
│   └── results/
├── 03_Phase2_NER/
│   ├── models/
│   ├── data/
│   └── results/
├── 04_Phase3_EHR/
│   ├── templates/
│   └── scripts/
├── 05_Integration/
├── 06_Documentation/
├── 07_Presentation/
└── 08_Backups/
```

### GitHub Structure
```
cse499-bangla-ehr/
├── .gitignore
├── README.md
├── requirements.txt
├── phase1_asr/
├── phase2_ner/
├── phase3_ehr/
├── notebooks/
└── docs/
```

---

## 9. Decision Points

### What to Decide Before Starting

1. **How many dialects to focus on?**
   - Recommendation: Start with 3 (Standard, Dhaka, Sylhet)
   - Add more if time permits

2. **Which ASR model to prioritize?**
   - Recommendation: Whisper-small (easy, good results)

3. **How much manual transcription?**
   - Minimum: 30 samples per dialect
   - Better: 50-100 per dialect

4. **How to handle code-mixing?**
   - Let models handle naturally
   - Don't separate, keep as spoken

---

## 10. Success Criteria

### Phase 1 Success
- WER < 30% on test set
- Can handle all 5 dialects
- Works with code-mixed speech

### Phase 2 Success
- F1-score > 75% overall
- Can extract 6+ entity types
- Handles unseen medical terms

### Phase 3 Success
- Generates valid JSON output
- Human-readable format available
- Integration works end-to-end

### Overall Success
- Faculty can see live demo
- All phases documented
- Code is reproducible

---

## 11. Questions to Answer Now

Before proceeding, confirm:

- [ ] Do all team members have Google accounts?
- [ ] Do all team members have GitHub accounts?
- [ ] Can everyone access a shared Google Drive?
- [ ] Does each member have Colab access?
- [ ] Have we decided on primary dialects?
- [ ] Have we assigned roles to team members?
- [ ] Do we have a meeting schedule?

---

## Next Steps

1. **This Week**: Set up Google Drive, Colab, GitHub
2. **Week 1-2**: Start collecting YouTube data
3. **Week 3**: Begin manual transcription

---

*Planning complete. Ready to execute.*
