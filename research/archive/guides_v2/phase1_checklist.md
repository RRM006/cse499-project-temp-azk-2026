# Phase 1 Checklist

## Week 1: Setup

- [ ] Team Lead creates `CSE499_EHR_Project` folder in Google Drive
- [ ] Share folder with both teammates (Editor permission)
- [ ] All teammates add shortcut to Drive
- [ ] Team Lead creates GitHub repo `CSE499-EHR-System` (Private)
- [ ] Invite both teammates as collaborators on GitHub
- [ ] Install GitHub Desktop (no terminal needed for syncing)
- [ ] Open Google Colab → Runtime → Change runtime type → **T4 GPU**
- [ ] Mount Google Drive and confirm it works
- [ ] Run Phase 1 setup notebook to create all folders
- [ ] Confirm GPU: `torch.cuda.is_available()` returns `True`
- [ ] Install packages: `transformers datasets evaluate jiwer librosa noisereduce soundfile yt-dlp accelerate`
- [ ] Create `00_Admin/team_contacts.txt` (names, Gmail, GitHub usernames)

---

## Week 2: Data Collection — Find Audio Sources

- [ ] Search YouTube for **Puran Dhaka** dialect (target: 40–60 clips)
  - Keywords: পুরান ঢাকা, পুরান ঢাকার ভাষা, Dhaka patient interview
- [ ] Search YouTube for **Barishal** dialect (target: 40–60 clips)
  - Keywords: বরিশালের ভাষা, বরিশাল স্বাস্থ্য
- [ ] Search YouTube for **Sylheti** dialect (target: 40–60 clips)
  - Keywords: সিলেটি কথা, সিলেট ডাক্তার
- [ ] Search YouTube for **Normal Bangla** (target: 40–60 clips)
  - Keywords: বাংলা চিকিৎসা, বাংলা স্বাস্থ্য পরামর্শ
- [ ] Search YouTube for **Indian Bangla** (target: 40–60 clips)
  - Keywords: কলকাতার বাংলা, Kolkata doctor Bengali
- [ ] Check OpenSLR.org for free Bangla speech datasets (Shrutilipi, Bengali ASR)
- [ ] Check Mozilla Common Voice for Bangla recordings
- [ ] Create URL spreadsheet — record every source URL before downloading

---

## Week 3: Download and Organize Audio

- [ ] Open notebook: `01_data_download.ipynb`
- [ ] Install yt-dlp: `!pip install yt-dlp`
- [ ] Download Puran Dhaka audio → save to `01_Dataset/raw_audio/puran_dhaka/`
- [ ] Download Barishal audio → save to `01_Dataset/raw_audio/barishal/`
- [ ] Download Sylheti audio → save to `01_Dataset/raw_audio/sylheti/`
- [ ] Download Normal Bangla audio → save to `01_Dataset/raw_audio/normal_bangla/`
- [ ] Download Indian Bangla audio → save to `01_Dataset/raw_audio/indian_bangla/`
- [ ] Rename all files to naming convention: `[dialect]_[001]_[gender]_[age].wav`
  - Example: `br_001_female_30s.wav`, `pd_002_male_40s.wav`
- [ ] Fill in `01_Dataset/metadata/dataset_log.csv`:
  - Columns: filename, dialect, source_url, speaker_gender, age_group, duration_seconds, notes

---

## Week 4: Audio Preprocessing (Notebook: `02_audio_preprocessing.ipynb`)

- [ ] Load each audio file with librosa
- [ ] Resample to **16000 Hz** (required by all ASR models)
- [ ] Convert to **mono** channel
- [ ] Normalize volume
- [ ] Remove background noise with `noisereduce`
- [ ] Trim silence from start and end (`librosa.effects.trim`)
- [ ] Save cleaned WAV files to `01_Dataset/cleaned_audio/[dialect]/`
  - Same filename as the original raw file
- [ ] Play back a few cleaned files to confirm they sound better
- [ ] Verify: every cleaned file is WAV, 16kHz, mono

---

## Week 4–5: Run All 10+ ASR Models (Notebook: `03_model_comparison.ipynb`)

Run each model on **10 test audio samples** (2 from each dialect).

- [ ] **Model 1 — Wav2Vec2** (facebook/wav2vec2-large-xlsr-53-bengali)
  - Save transcripts to `02_Phase1_ASR/model_outputs/wav2vec2_transcripts/`
- [ ] **Model 2 — HuBERT** (facebook/hubert-large-ls960-ft)
  - Save transcripts to `02_Phase1_ASR/model_outputs/hubert_transcripts/`
- [ ] **Model 3 — Data2Vec** (facebook/data2vec-audio-large-960h)
  - Save transcripts to `02_Phase1_ASR/model_outputs/data2vec_transcripts/`
- [ ] **Model 4 — WavLM** (microsoft/wavlm-large)
  - Save transcripts to `02_Phase1_ASR/model_outputs/wavlm_transcripts/`
- [ ] **Model 5 — XLSR-53** (facebook/wav2vec2-large-xlsr-53)
  - Save transcripts to `02_Phase1_ASR/model_outputs/xlsr_transcripts/`
- [ ] **Model 6 — Whisper** (openai/whisper-small) ← expected best for Bangla
  - Save transcripts to `02_Phase1_ASR/model_outputs/whisper_transcripts/`
- [ ] **Model 7 — Canary** (nvidia/canary-1b)
  - Save transcripts to `02_Phase1_ASR/model_outputs/canary_transcripts/`
- [ ] **Model 8 — OLMoASR** (allenai/olmo-asr)
  - Save transcripts to `02_Phase1_ASR/model_outputs/olmosasr_transcripts/`
- [ ] **Model 9 — MMS** (facebook/mms-1b-all)
  - Save transcripts to `02_Phase1_ASR/model_outputs/mms_transcripts/`
- [ ] **Model 10 — SeamlessM4T** (facebook/seamless-m4t-v2-large)
  - Save transcripts to `02_Phase1_ASR/model_outputs/seamless_transcripts/`
- [ ] **Model 11 — Conformer-CTC** (nvidia/stt_bn_conformer_ctc_large)
  - Save transcripts to `02_Phase1_ASR/model_outputs/conformer_transcripts/`
- [ ] Calculate **WER** for each model using `jiwer`
- [ ] Fill in `02_Phase1_ASR/evaluation/wer_scores.csv`: model name, dialect, WER score
- [ ] Identify winner: model with **lowest WER** on Bangla (expected: Whisper)

---

## Week 4: Manual Transcription (Needed for Fine-Tuning)

- [ ] Manually transcribe **~100 audio clips** — write exactly what is spoken
- [ ] Divide: each team member transcribes ~33 clips
- [ ] Save as `.txt` files to `01_Dataset/transcripts/manual/`
- [ ] Name each file identically to the audio: `br_001_female_30s.txt`
- [ ] Quality check: re-read each transcript while listening to the audio

---

## Week 4: Fine-Tune Whisper (Notebook: `04_whisper_finetune.ipynb`)

- [ ] Open notebook: `04_whisper_finetune.ipynb`
- [ ] Mount Drive and confirm GPU is active
- [ ] Check for existing checkpoint:
  ```python
  import glob
  checkpoints = sorted(glob.glob(f'{BASE}/02_Phase1_ASR/saved_models/whisper_checkpoints/checkpoint-*'))
  RESUME_FROM = checkpoints[-1] if checkpoints else None
  print("Resuming from:", RESUME_FROM)
  ```
- [ ] Load Whisper-small from HuggingFace
- [ ] Prepare dataset: audio file + matching transcript text
- [ ] Set training args:
  - `output_dir` → `02_Phase1_ASR/saved_models/whisper_checkpoints`
  - `save_steps=500` ← checkpoint every 500 steps
  - `save_total_limit=3` ← keep only 3 latest checkpoints
  - `num_train_epochs=5`
  - `fp16=True` (faster on GPU)
- [ ] Train: `trainer.train(resume_from_checkpoint=RESUME_FROM)`
- [ ] Train for 3–5 epochs (Colab free: ~4–5 hours per session)
- [ ] After training completes: save final model to `02_Phase1_ASR/saved_models/whisper_finetuned/`
- [ ] Evaluate on test set — record new WER score in `wer_scores.csv`
- [ ] Confirm: fine-tuned WER is **lower** than baseline Whisper WER

---

## Week 5: Generate Final Transcripts for All Audio

- [ ] Use fine-tuned Whisper to transcribe ALL cleaned audio files
- [ ] Save each transcript as `.txt` to `01_Dataset/transcripts/auto/[dialect]/`
- [ ] Name each transcript identically to the audio: `br_001_female_30s.txt`
- [ ] Confirm: every audio file has a matching transcript file
- [ ] These transcripts are the **output of Phase 1** and the **input of Phase 2**

---

## Phase 1 Complete — Checklist

- [ ] All audio cleaned and organized in `01_Dataset/cleaned_audio/` by dialect
- [ ] `dataset_log.csv` filled in for every audio file
- [ ] WER comparison table filled in `wer_scores.csv` for all 10+ models
- [ ] Fine-tuned Whisper model saved to `02_Phase1_ASR/saved_models/whisper_finetuned/`
- [ ] Text transcripts for ALL audio files saved to `01_Dataset/transcripts/auto/`
- [ ] All notebooks pushed to GitHub
- [ ] Weekly progress log updated in `00_Admin/weekly_progress_log.docx`

---

## Metrics to Track

| Milestone | Metric | Target | Actual |
|-----------|--------|--------|--------|
| Baseline Whisper (no fine-tune) | WER | — | |
| After fine-tuning Whisper | WER | < 30% | |
| Best model overall | WER | < 25% | |

---

## Daily Task Template

| Day | Task | Status |
|-----|------|--------|
| Mon | | |
| Tue | | |
| Wed | | |
| Thu | | |
| Fri | Update weekly_progress_log.docx | |
| Sat | | |
| Sun | | |
