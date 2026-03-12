# Phase-by-Phase Timeline Guide

## CSE499: EHR-Based Pre-Consultation Medical Documentation System

---

## Complete Timeline Overview

| Phase | Duration | Weeks | Key Deliverables |
|-------|----------|-------|------------------|
| Phase 1: ASR | 9 weeks | 1-9 | Working ASR model |
| Phase 2: NER | 6 weeks | 10-15 | Working NER model |
| Phase 3: EHR | 3 weeks | 15-17 | Complete pipeline |
| Buffer | 1-2 weeks | 17-18 | Final testing & docs |

---

# PHASE 1: AUTOMATIC SPEECH RECOGNITION (ASR)

## Week 1: Setup & Initial Data Collection

### Tasks
1. **Environment Setup** (Day 1-2)
   - Create Google Colab account
   - Mount Google Drive
   - Install packages:
   ```python
   !pip install torch transformers datasets librosa soundfile jiwer yt-dlp
   ```

2. **Create Folder Structure** (Day 2)
   - Create: `CSE499_Project/phase1_asr/`
   - Create: `CSE499_Project/dataset/`
   - Set up shared Drive with team

3. **Start Data Collection** (Day 3-7)
   - Search YouTube for dialect samples
   - Create list of 20+ URLs per dialect
   - Begin downloading audio files
   - Use yt-dlp to download

### Daily Schedule
| Day | Task |
|-----|------|
| Mon | Colab setup, Drive mount |
| Tue | Install packages, test |
| Wed | Create folders, naming convention |
| Thu | Search YouTube (Dhaka) |
| Fri | Search YouTube (Sylhet, others) |
| Sat | Start downloads |
| Sun | Review/buffer |

---

## Week 2: Data Collection & Transcription

### Tasks
1. **Continue Downloads** (Day 1-3)
   - Download remaining audio files
   - Target: 50 files per dialect
   - Save to proper folders

2. **Start Transcription** (Day 3-7)
   - Create transcription template
   - Transcribe first 10 files
   - Establish transcription guidelines

### Transcription Guidelines
```
- Write exactly what is spoken
- Use Bengali script
- Include filler words
- Mark unclear parts: [unclear]
```

### Quality Check
- [ ] Audio clearly audible
- [ ] Transcription matches exactly
- [ ] File naming correct
- [ ] Stored in correct folder

---

## Week 3: Preprocessing & Baseline

### Tasks
1. **Audio Preprocessing** (Day 1-3)
   - Resample all to 16kHz
   - Normalize volume
   - Remove silence
   ```python
   import librosa
   import soundfile as sf

   def preprocess(input_path, output_path):
       audio, sr = librosa.load(input_path, sr=16000)
       trimmed, _ = librosa.effects.trim(audio, top_db=20)
       sf.write(output_path, trimmed, 16000)
   ```

2. **Create Train/Val/Test Split** (Day 4-5)
   - Split: 80% train, 10% val, 10% test
   - Stratify by dialect
   - Create manifest file

3. **Baseline Model Test** (Day 6-7)
   - Test pre-trained Whisper
   - Calculate baseline WER
   - Document results

### Output
- Preprocessed audio files
- Split manifests
- Baseline WER score

---

## Week 4: Fine-Tuning Whisper

### Tasks
1. **Prepare Training Data** (Day 1-2)
   - Format data for Whisper
   - Create Dataset class
   ```python
   from datasets import Dataset

   def prepare_dataset(batch):
       audio = load_audio(batch["file"])
       batch["input_features"] = processor.feature_extractor(audio, sampling_rate=16000).input_features[0]
       batch["labels"] = processor.tokenizer(batch["transcription"]).input_ids
       return batch
   ```

2. **Configure Whisper Training** (Day 3-4)
   - Load model: `openai/whisper-small`
   - Set hyperparameters
   ```python
   from transformers import WhisperForConditionalGeneration

   model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-small")
   ```

3. **Start Training** (Day 5-7)
   - Train for 1-3 epochs
   - Save checkpoints
   - Monitor loss

### Training Config
```python
training_args = SpeechTrainingArguments(
    output_dir="./whisper_bengali",
    per_device_train_batch_size=8,
    learning_rate=1e-5,
    num_train_epochs=3,
    save_strategy="epoch",
    evaluation_strategy="epoch",
    report_to="none",
)
```

---

## Week 5: Continue Whisper Training

### Tasks
1. **Complete Training** (Day 1-4)
   - Finish Whisper fine-tuning
   - Save best model
   - Evaluate on validation set

2. **Evaluate Results** (Day 5-6)
   - Calculate WER per dialect
   - Create comparison table
   - Document findings

3. **Backup** (Day 7)
   - Save model to Drive
   - Save all outputs

---

## Week 6: Wav2Vec2 Training

### Tasks
1. **Setup Wav2Vec2** (Day 1-2)
   - Load pre-trained model
   - Prepare data
   ```python
   from transformers import Wav2Vec2ForCTC

   model = Wav2Vec2ForCTC.from_pretrained(
       "facebook/wav2vec2-large-xlsr-53-bengali"
   )
   ```

2. **Fine-tune** (Day 3-5)
   - Train for 5-10 epochs
   - Save checkpoints
   - Monitor progress

3. **Evaluate** (Day 6-7)
   - Calculate WER
   - Compare with Whisper

---

## Week 7: Additional Models

### Tasks
1. **HuBERT** (Day 1-3)
   - Fine-tune HuBERT
   - Evaluate WER

2. **WavLM** (Day 4-6)
   - Fine-tune WavLM
   - Evaluate WER

3. **Comparison** (Day 7)
   - Create model comparison table
   - Decide best model(s)

### Model Comparison Format
| Model | WER (Dhaka) | WER (Sylhet) | WER (Barishal) | Overall WER |
|-------|-------------|---------------|----------------|-------------|
| Whisper | 18% | 22% | 20% | 20% |
| Wav2Vec2 | 25% | 28% | 26% | 26% |
| HuBERT | 23% | 26% | 24% | 24% |
| WavLM | 26% | 30% | 28% | 28% |

---

## Week 8: Optimization & Final ASR

### Tasks
1. **Best Model Selection** (Day 1-2)
   - Choose top 1-2 models
   - Possibly ensemble

2. **Final Training Run** (Day 3-5)
   - Train best model with more data
   - Use all available training data

3. **Save Outputs** (Day 6-7)
   - Save best model checkpoint
   - Save evaluation metrics
   - Document Phase 1 results

### Phase 1 Deliverables
- [x] Fine-tuned ASR model
- [x] WER < 30% (target)
- [x] Comparison results
- [x] Documentation

---

## Week 9: Phase 1 Review

### Tasks
1. **Documentation** (Day 1-3)
   - Write Phase 1 report
   - Create README
   - Document all experiments

2. **Transition to Phase 2** (Day 4-7)
   - Prepare transcriptions for NER
   - Start Phase 2 preparation
   - Team meeting: assign Phase 2 roles

---

# PHASE 2: MEDICAL NAMED ENTITY RECOGNITION (NER)

## Week 10: NER Data Preparation

### Tasks
1. **Create Annotation Guidelines** (Day 1-2)
   - Define entity types
   - Create examples
   - Write annotation rules
   ```markdown
   # Entity Types
   - SYMPTOM: Physical conditions (জ্বর, কাশি, ব্যথা)
   - DISEASE: Medical conditions (ডায়াবেটিস, উচ্চ রক্তচাপ)
   - MEDICATION: Drugs (প্যারাসিটামল, ইনসুলিন)
   - DURATION: Time periods (৩ দিন, এক সপ্তাহ)
   - ALLERGY: Allergic reactions
   - BODY_PART: Anatomy (মাথা, বুক, পেট)
   ```

2. **Start Annotation** (Day 3-7)
   - Use Phase 1 transcriptions
   - Annotate in BIO format
   - Target: 100 samples this week

### Annotation Format
```
আমার   O
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

---

## Week 11: More Annotation

### Tasks
1. **Continue Annotation** (Day 1-5)
   - Annotate 200+ more samples
   - Total target: 300+ samples

2. **Quality Check** (Day 6-7)
   - Review annotations
   - Fix errors
   - Ensure consistency

### Annotation Tools
- Google Sheets (simple)
- Label Studio (better)
- Doccano (open source)

---

## Week 12: BanglaBERT Fine-Tuning

### Tasks
1. **Prepare Data** (Day 1-2)
   - Convert to proper format
   - Create train/val/test splits
   ```python
   # Convert to token-classification format
   from transformers import AutoTokenizer

   tokenizer = AutoTokenizer.from_pretrained("csebuetnlp/banglabert")
   
   def tokenize_and_align_labels(examples):
       tokenized_inputs = tokenizer(examples["tokens"], truncation=True, is_split_into_words=True)
       labels = []
       for i, label in enumerate(examples["labels"]):
           word_ids = tokenized_inputs.word_ids(i)
           previous_word_idx = None
           label_ids = []
           for word_idx in word_ids:
               if word_idx is None:
                   label_ids.append(-100)
               elif word_idx != previous_word_idx:
                   label_ids.append(label[word_idx])
               else:
                   label_ids.append(-100)
               previous_word_idx = word_idx
           label_ids.append(label_ids)
       tokenized_inputs["labels"] = label_ids
       return tokenized_inputs
   ```

2. **Setup Training** (Day 3-4)
   - Load BanglaBERT
   - Configure training
   ```python
   from transformers import AutoModelForTokenClassification

   model = AutoModelForTokenClassification.from_pretrained(
       "csebuetnlp/banglabert",
       num_labels=len(label_list),
       id2label=id2label,
       label2id=label2id
   )
   ```

3. **Train** (Day 5-7)
   - Train for 5-10 epochs
   - Save checkpoints

---

## Week 13: More NER Models

### Tasks
1. **XLM-RoBERTa** (Day 1-3)
   - Fine-tune XLM-R
   - Evaluate F1-score

2. **Other Models** (Day 4-6)
   - Try mBERT, DistilBERT
   - Quick experiments

3. **Comparison** (Day 7)
   - Compare all models
   - Select best

### Evaluation Metrics
```python
from seqeval.metrics import classification_report

print(classification_report(true_labels, predicted_labels))
```

### Results Table
| Model | Precision | Recall | F1-Score |
|-------|-----------|--------|----------|
| BanglaBERT | 85% | 82% | 83% |
| XLM-RoBERTa | 83% | 80% | 81% |
| mBERT | 81% | 79% | 80% |

---

## Week 14: Phase 2 Finalization

### Tasks
1. **Best Model** (Day 1-3)
   - Train final best model
   - Save model and tokenizer
   - Document results

2. **Test Set Evaluation** (Day 4-5)
   - Final evaluation on test set
   - Create error analysis

3. **Save Outputs** (Day 6-7)
   - Save model to Drive
   - Save annotations
   - Document Phase 2

### Phase 2 Deliverables
- [x] Annotated dataset (500+)
- [x] Fine-tuned NER model
- [x] F1-score > 75%
- [x] Documentation

---

# PHASE 3: EHR TEMPLATE FILLER

## Week 15: EHR System Design

### Tasks
1. **Design EHR Template** (Day 1-2)
   ```json
   {
     "patient_id": "auto",
     "consultation_date": "auto",
     "chief_complaint": {
       "symptoms": [],
       "duration": ""
     },
     "medical_history": {
       "diseases": [],
       "current_medications": [],
       "allergies": []
     },
     "assessment_and_plan": {
       "impression": "",
       "treatments": []
     }
   }
   ```

2. **Entity Mapping Rules** (Day 3-4)
   - Map NER labels to EHR fields
   ```python
   ENTITY_TO_FIELD = {
       "SYMPTOM": "chief_complaint.symptoms",
       "DISEASE": "medical_history.diseases",
       "MEDICATION": "medical_history.current_medications",
       "ALLERGY": "medical_history.allergies",
       "DURATION": "chief_complaint.duration",
       "TREATMENT": "assessment_and_plan.treatments"
   }
   ```

3. **Implement Mapper** (Day 5-7)
   - Write entity extraction code
   - Map entities to template

---

## Week 16: Integration & Testing

### Tasks
1. **Complete Pipeline** (Day 1-3)
   - Integrate Phase 1 + 2 + 3
   - End-to-end testing

2. **Error Handling** (Day 4-5)
   - Handle missing entities
   - Handle unknown cases

3. **Human-Readable Output** (Day 6-7)
   - Create text format
   - Format JSON nicely

### Pipeline Code
```python
def process_audio(audio_file):
    # Phase 1: ASR
    transcription = asr_model.transcribe(audio_file)
    
    # Phase 2: NER
    entities = ner_model.extract(transcription["text"])
    
    # Phase 3: EHR
    ehr = generate_ehr(entities)
    
    return ehr
```

---

## Week 17: Complete Integration

### Tasks
1. **Final Integration** (Day 1-3)
   - All phases working together
   - Clean code
   - Proper documentation

2. **Demo Preparation** (Day 4-6)
   - Create demo notebook
   - Test with sample audio
   - Prepare presentation

3. **Final Testing** (Day 7)
   - End-to-end test
   - Error analysis
   - Fix critical bugs

### Phase 3 Deliverables
- [x] EHR template
- [x] Entity mapper
- [x] Complete pipeline
- [x] Demo ready

---

# BUFFER WEEK (Week 18)

## Final Tasks

### Documentation
- Write final report
- Create README files
- Clean code comments

### Presentation
- Prepare slides
- Practice demo
- Anticipate questions

### Submission
- Submit code
- Submit documentation
- Present to faculty

---

## Quick Reference: Week Numbers

| Week | Phase | Key Task |
|------|-------|----------|
| 1 | P1 | Setup + Data Collection Start |
| 2 | P1 | More Data + Transcription |
| 3 | P1 | Preprocessing + Baseline |
| 4-5 | P1 | Whisper Fine-tuning |
| 6-7 | P1 | Wav2Vec2, HuBERT, WavLM |
| 8 | P1 | Optimization |
| 9 | P1 | Phase 1 Review |
| 10-11 | P2 | Annotation |
| 12 | P2 | BanglaBERT Training |
| 13 | P2 | More Models |
| 14 | P2 | Phase 2 Finalize |
| 15 | P3 | EHR Design |
| 16 | P3 | Integration |
| 17 | P3 | Complete |
| 18 | Buffer | Final Testing & Docs |

---

## Team Assignment Suggestion

| Weeks | Member 1 | Member 2 | Member 3 |
|-------|----------|----------|----------|
| 1-9 | Phase 1 ASR | Phase 1 Support | Phase 1 Support |
| 10-14 | Phase 2 NER | Phase 2 NER | Phase 1 Documentation |
| 15-17 | Phase 3 | Integration | Integration |
| 18 | Final Docs | Final Docs | Final Docs |

---

*Timeline complete. Follow this guide week by week.*
