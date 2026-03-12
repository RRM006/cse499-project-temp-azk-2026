# Project Tracking Guide

## CSE499: EHR-Based Pre-Consultation Medical Documentation System

---

# COMPLETE TRACKING CHECKLIST

## PHASE 1: AUTOMATIC SPEECH RECOGNITION (ASR)

### Week 1: Foundation Setup
- [ ] Create Google Colab account
- [ ] Verify Google Drive access
- [ ] Install required packages in Colab
- [ ] Test GPU availability
- [ ] Create project folder structure
- [ ] Set up shared Drive with team members

### Week 2: Initial Data Collection
- [ ] Search YouTube for Dhaka dialect videos (minimum 20)
- [ ] Search YouTube for Sylhet dialect videos (minimum 20)
- [ ] Search YouTube for Barishal dialect videos (minimum 20)
- [ ] Search YouTube for Standard Bangla videos (minimum 20)
- [ ] Search YouTube for Kolkata dialect videos (minimum 20)
- [ ] Create spreadsheet with all video URLs
- [ ] Document video details (title, duration, source)

### Week 3: Download Audio Files
- [ ] Install yt-dlp library
- [ ] Install ffmpeg for audio conversion
- [ ] Create download script
- [ ] Download Dhaka audio files (target: 50)
- [ ] Download Sylhet audio files (target: 50)
- [ ] Download Barishal audio files (target: 50)
- [ ] Download Standard Bangla audio files (target: 50)
- [ ] Download Kolkata audio files (target: 50)
- [ ] Verify all downloads completed successfully
- [ ] Create collection log spreadsheet

### Week 4: Manual Transcription - Batch 1
- [ ] Create transcription template
- [ ] Set up transcription workflow
- [ ] Transcribe Dhaka samples (first 20)
- [ ] Transcribe Sylhet samples (first 20)
- [ ] Transcribe Barishal samples (first 20)
- [ ] Review and verify transcriptions
- [ ] Fix any errors found

### Week 5: Manual Transcription - Batch 2
- [ ] Transcribe Dhaka samples (next 20)
- [ ] Transcribe Sylhet samples (next 20)
- [ ] Transcribe Barishal samples (next 20)
- [ ] Transcribe Standard Bangla samples (first 30)
- [ ] Transcribe Kolkata samples (first 30)
- [ ] Quality check all transcriptions

### Week 6: Audio Preprocessing
- [ ] Install librosa and soundfile
- [ ] Create preprocessing script
- [ ] Resample all audio to 16000 Hz
- [ ] Normalize audio volume
- [ ] Remove silence from edges
- [ ] Convert to mono channel
- [ ] Save processed files
- [ ] Verify audio quality

### Week 7: Data Splitting
- [ ] Create train/validation/test split (80/10/10)
- [ ] Ensure stratified split by dialect
- [ ] Create manifest files for each split
- [ ] Verify split ratios
- [ ] Document split statistics

### Week 8: Baseline Model - Whisper
- [ ] Load pre-trained Whisper model
- [ ] Test on sample audio
- [ ] Calculate baseline WER
- [ ] Document baseline results
- [ ] Analyze errors

### Week 9: Whisper Fine-tuning - Round 1
- [ ] Prepare Whisper training data
- [ ] Configure training parameters
- [ ] Set up training loop
- [ ] Train for 1-2 epochs (initial)
- [ ] Save checkpoint
- [ ] Evaluate on validation set

### Week 10: Whisper Fine-tuning - Complete
- [ ] Continue training (3-5 epochs total)
- [ ] Monitor training progress
- [ ] Save best model checkpoint
- [ ] Calculate final WER per dialect
- [ ] Document results

### Week 11: Additional ASR Models - Wav2Vec2
- [ ] Load pre-trained Wav2Vec2 Bengali
- [ ] Prepare data for Wav2Vec2
- [ ] Configure CTC training
- [ ] Train model
- [ ] Evaluate WER
- [ ] Compare with Whisper results

### Week 12: Additional ASR Models - HuBERT
- [ ] Load pre-trained HuBERT model
- [ ] Prepare data
- [ ] Train model
- [ ] Evaluate WER
- [ ] Document comparison

### Week 13: Additional ASR Models - WavLM & XLSR
- [ ] Train WavLM model
- [ ] Evaluate WavLM
- [ ] Train XLSR-53 model
- [ ] Evaluate XLSR-53
- [ ] Create model comparison table

### Week 14: ASR Finalization
- [ ] Select best performing model(s)
- [ ] Fine-tune best model with full data
- [ ] Final WER evaluation
- [ ] Save all model checkpoints to Drive
- [ ] Create Phase 1 documentation
- [ ] Prepare Phase 1 report

---

## PHASE 2: MEDICAL NAMED ENTITY RECOGNITION (NER)

### Week 15: NER Annotation Setup
- [ ] Define entity types (SYMPTOM, DISEASE, etc.)
- [ ] Create annotation guidelines document
- [ ] Set up annotation format (BIO)
- [ ] Choose annotation tool
- [ ] Create annotation interface

### Week 16: NER Annotation - Batch 1
- [ ] Annotate Dhaka transcriptions (50)
- [ ] Annotate Sylhet transcriptions (50)
- [ ] Annotate Barishal transcriptions (50)
- [ ] Review annotations
- [ ] Fix errors

### Week 17: NER Annotation - Batch 2
- [ ] Annotate Standard Bangla transcriptions (50)
- [ ] Annotate Kolkata transcriptions (50)
- [ ] Annotate additional samples (100+)
- [ ] Total target: 500+ annotated samples
- [ ] Quality assurance check

### Week 18: NER Data Preparation
- [ ] Convert annotations to required format
- [ ] Create train/validation/test splits
- [ ] Create label mapping
- [ ] Save dataset files
- [ ] Verify data format

### Week 19: BanglaBERT NER Training
- [ ] Load pre-trained BanglaBERT
- [ ] Set up token classification
- [ ] Configure training parameters
- [ ] Train for initial epochs
- [ ] Save checkpoint
- [ ] Evaluate on validation

### Week 20: BanglaBERT NER - Complete
- [ ] Continue training (10+ epochs total)
- [ ] Save best model
- [ ] Evaluate on test set
- [ ] Calculate per-entity F1-scores
- [ ] Create confusion matrix

### Week 21: Additional NER Models
- [ ] Train XLM-RoBERTa model
- [ ] Evaluate XLM-RoBERTa
- [ ] Train mBERT model
- [ ] Evaluate mBERT
- [ ] Create comparison table

### Week 22: Additional NER Models - More
- [ ] Train DistilBERT model
- [ ] Evaluate DistilBERT
- [ ] Train ELECTRA model
- [ ] Evaluate ELECTRA
- [ ] Compare all models

### Week 23: NER Finalization
- [ ] Select best NER model
- [ ] Fine-tune with full dataset
- [ ] Final evaluation
- [ ] Save model to Drive
- [ ] Create Phase 2 documentation
- [ ] Prepare Phase 2 report

---

## PHASE 3: EHR TEMPLATE FILLER

### Week 24: EHR Template Design
- [ ] Research EHR formats
- [ ] Define EHR template structure
- [ ] Create JSON template
- [ ] Define all fields
- [ ] Add sample data

### Week 25: Entity Mapping Rules
- [ ] Map SYMPTOM to EHR field
- [ ] Map DISEASE to EHR field
- [ ] Map MEDICATION to EHR field
- [ ] Map DURATION to EHR field
- [ ] Map ALLERGY to EHR field
- [ ] Map BODY_PART to EHR field
- [ ] Map TREATMENT to EHR field
- [ ] Map DOSAGE to EHR field

### Week 26: EHR Generator Implementation
- [ ] Create entity mapper code
- [ ] Implement field mapping
- [ ] Handle duplicates
- [ ] Handle missing entities
- [ ] Generate JSON output

### Week 27: Human-Readable Output
- [ ] Create text formatter
- [ ] Format JSON as readable text
- [ ] Add section headers
- [ ] Include all fields
- [ ] Save as .txt and .md

### Week 28: Integration Testing
- [ ] Test Phase 1 → Phase 2 connection
- [ ] Test Phase 2 → Phase 3 connection
- [ ] Test complete pipeline
- [ ] Fix integration errors
- [ ] Document test results

---

## COMPLETE SYSTEM INTEGRATION

### Week 29: Full Pipeline
- [ ] Integrate all three phases
- [ ] Create pipeline class
- [ ] Add error handling
- [ ] Add logging
- [ ] Test end-to-end

### Week 30: Demo Preparation
- [ ] Create demo notebook
- [ ] Prepare sample audio files
- [ ] Test live demo
- [ ] Prepare backup demo
- [ ] Create presentation slides

---

## FINALIZATION

### Week 31: Documentation
- [ ] Write final project report
- [ ] Create README files
- [ ] Document all code
- [ ] Add comments to code
- [ ] Create user manual

### Week 32: Testing & Review
- [ ] Final system testing
- [ ] Performance evaluation
- [ ] Fix all known bugs
- [ ] Prepare presentation
- [ ] Rehearse demo

### Week 33: Submission
- [ ] Submit code to GitHub
- [ ] Submit documentation
- [ ] Prepare faculty presentation
- [ ] Review all deliverables
- [ ] Final backup of everything

### Week 34: Presentation
- [ ] Present to faculty
- [ ] Demonstrate live system
- [ ] Answer questions
- [ ] Submit final report
- [ ] Celebrate completion!

---

# DAILY TRACKING TEMPLATE

## Daily Log Format

```
Date: [YYYY-MM-DD]
Day: [Week X, Day Y]

TASKS COMPLETED:
- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

PROBLEMS ENCOUNTERED:
- Problem 1: [description]
- Problem 2: [description]

SOLUTIONS:
- Solution 1: [what worked]
- Solution 2: [what worked]

NEXT DAY PRIORITY:
- [ ] Priority 1
- [ ] Priority 2

HOURS WORKED: [X] hours
NOTES: [any additional notes]
```

---

# WEEKLY TRACKING TEMPLATE

## Week X Summary

```
Week: [X]
Phase: [Phase 1/2/3]
Dates: [Start - End]

WEEKLY GOALS:
- [ ] Goal 1
- [ ] Goal 2
- [ ] Goal 3

GOALS ACHIEVED:
- [x] Goal 1 - [status]
- [x] Goal 2 - [status]
- [ ] Goal 3 - [status/not done]

METRICS THIS WEEK:
- [ ] WER: [value]
- [ ] F1-Score: [value]
- [ ] Samples transcribed: [X]
- [ ] Models trained: [X]

BLOCKERS:
- [ ] Blocker 1
- [ ] Blocker 2

TEAM CONTRIBUTION:
- Member 1: [tasks]
- Member 2: [tasks]
- Member 3: [tasks]

OVERALL WEEK RATING: [1-5]
NOTES:
```

---

# MILESTONE CHECKLIST

## Milestone 1: Foundation (Week 3)
- [ ] Environment ready
- [ ] 50+ audio samples collected
- [ ] Folder structure created
- [ ] Team access verified

## Milestone 2: Data Ready (Week 6)
- [ ] 200+ audio files downloaded
- [ ] 100+ transcriptions complete
- [ ] Data preprocessed
- [ ] Train/val/test split done

## Milestone 3: ASR Working (Week 10)
- [ ] Whisper fine-tuned
- [ ] WER < 40% achieved
- [ ] At least 2 models compared
- [ ] Phase 1 documented

## Milestone 4: NER Working (Week 20)
- [ ] 500+ samples annotated
- [ ] BanglaBERT trained
- [ ] F1 > 70% achieved
- [ ] Phase 2 documented

## Milestone 5: Complete System (Week 30)
- [ ] All phases integrated
- [ ] End-to-end pipeline works
- [ ] Demo ready
- [ ] Documentation complete

## Milestone 6: Submission (Week 34)
- [ ] Code on GitHub
- [ ] Report submitted
- [ ] Presentation done
- [ ] Project complete!

---

# METRICS TRACKING

## ASR Metrics (Lower is Better)

| Model | Week | WER Dhaka | WER Sylhet | WER Barishal | WER Standard | WER Kolkata | Overall |
|-------|------|------------|------------|--------------|--------------|-------------|---------|
| Baseline | 8 | - | - | - | - | - | - |
| Whisper | 10 | | | | | | |
| Wav2Vec2 | 11 | | | | | | |
| HuBERT | 12 | | | | | | |
| WavLM | 13 | | | | | | |
| XLSR-53 | 13 | | | | | | |

## NER Metrics (Higher is Better)

| Model | Week | Precision | Recall | F1-Score |
|-------|------|-----------|--------|----------|
| BanglaBERT | 20 | | | |
| XLM-RoBERTa | 21 | | | |
| mBERT | 21 | | | |
| DistilBERT | 22 | | | |
| ELECTRA | 22 | | | |

## Dataset Statistics

| Dialect | Audio Files | Transcribed | Annotated |
|---------|-------------|-------------|-----------|
| Dhaka | | | |
| Sylhet | | | |
| Barishal | | | |
| Standard | | | |
| Kolkata | | | |
| **TOTAL** | | | |

---

# TEAM TRACKING

## Member 1: [Name]
Role: [ASR/NER/EHR Lead]

| Week | Tasks | Hours | Notes |
|------|-------|-------|-------|
| 1 | | | |
| 2 | | | |
| ... | | | |

## Member 2: [Name]
Role: [NER/EHR/ASR Support]

| Week | Tasks | Hours | Notes |
|------|-------|-------|-------|
| 1 | | | |
| 2 | | | |
| ... | | | |

## Member 3: [Name]
Role: [Integration/Documentation]

| Week | Tasks | Hours | Notes |
|------|-------|-------|-------|
| 1 | | | |
| 2 | | | |
| ... | | | |

---

# FILE VERSION TRACKING

| File | Version | Date | Changes | Author |
|------|---------|------|---------|--------|
| | | | | |
| | | | | |

---

# CHECKPOINT TRACKING

## Model Checkpoints

| Model | Checkpoint | Date | Path | Status |
|-------|------------|------|------|--------|
| Whisper | epoch_1 | | | |
| Whisper | epoch_2 | | | |
| Whisper | best | | | |
| Wav2Vec2 | epoch_1 | | | |
| BanglaBERT | epoch_5 | | | |
| BanglaBERT | best | | | |

---

# PROBLEM TRACKING

| Issue | Date | Phase | Severity | Status | Solution |
|-------|------|-------|----------|--------|----------|
| | | | | | |
| | | | | | |

---

# NOTES SECTION

## Important Findings
-

## Lessons Learned
-

## Future Improvements
-

## Resources Found Useful
-

---

*Tracking guide complete. Use this to monitor your project progress!*
