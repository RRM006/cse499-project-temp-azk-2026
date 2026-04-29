# Troubleshooting Guide

---

## Google Colab Issues

### Colab Disconnects During Training
**Problem**: Runtime disconnects and you lose training progress
**Solution — Checkpoints to Drive every 500 steps:**
```python
import glob

BASE = '/content/drive/MyDrive/CSE499_EHR_Project'
CHECKPOINT_DIR = f'{BASE}/02_Phase1_ASR/saved_models/whisper_checkpoints'

# Check for existing checkpoint before every training run
existing = sorted(glob.glob(f'{CHECKPOINT_DIR}/checkpoint-*'))
RESUME_FROM = existing[-1] if existing else None
print(f"Resuming from: {RESUME_FROM}" if RESUME_FROM else "Starting fresh")

# In Seq2SeqTrainingArguments:
#   output_dir=CHECKPOINT_DIR
#   save_steps=500
#   save_total_limit=3   ← keeps only 3 latest, saves Drive space

# In trainer.train():
trainer.train(resume_from_checkpoint=RESUME_FROM)
```
> **Colab free gives ~4 hours GPU per session.** Plan: start training → save checkpoint → session ends → reconnect → resume. Never start from scratch.

---

### GPU Not Available
**Problem**: `torch.cuda.is_available()` returns `False`
**Solution**:
1. Runtime → Change runtime type → **T4 GPU**
2. Restart runtime
3. Run your setup cells again (mount Drive, install packages)

```python
import torch
print(torch.cuda.is_available())   # must be True
print(torch.cuda.get_device_name(0))  # should show T4
```

---

### Out of Memory (OOM / CUDA Error)
**Problem**: `CUDA out of memory` error during training
**Solutions**:
1. Reduce batch size: change `per_device_train_batch_size=8` → `4` → `2` → `1`
2. Increase gradient accumulation to compensate: `gradient_accumulation_steps=4`
3. Use Whisper-small (not medium or large) for training on free Colab
4. Clear memory between runs:
```python
import gc, torch
gc.collect()
torch.cuda.empty_cache()
```
5. Restart runtime: Runtime → Restart runtime (then re-mount Drive)

---

## Google Drive Issues

### Drive Not Mounted
**Problem**: `FileNotFoundError` when trying to access `/content/drive/...`
**Solution**: Always run mount cell first:
```python
from google.colab import drive
drive.mount('/content/drive')
```

### Wrong Drive Path (Very Common Mistake)
**Problem**: Path works on one person's Colab but not another's
**Solution**: Always use `MyDrive` (no space), not `My Drive`:
```python
# CORRECT
BASE = '/content/drive/MyDrive/CSE499_EHR_Project'

# WRONG — will fail
BASE = '/content/drive/My Drive/CSE499_EHR_Project'
```

### Drive Storage Full
**Problem**: Cannot save model or audio — Drive is full
**Solution**:
- Keep only 3 checkpoints: `save_total_limit=3` in TrainingArguments
- Delete old/failed checkpoints manually from Drive
- Audio files for 5 dialects (40–60 clips each at 16kHz) ≈ 3–4 GB
- Model weights (Whisper-small fine-tuned) ≈ 500 MB
- Plan for at least **10 GB** free before starting

---

## Audio Issues

### Cannot Load Audio File
**Problem**: `librosa.load()` or `soundfile` fails on `.mp3` or `.mp4`
**Solution**: Convert to WAV first
```bash
!apt-get install -y ffmpeg
!ffmpeg -i input.mp3 -ar 16000 -ac 1 output.wav
```
Or in Python:
```python
import os
os.system(f"ffmpeg -i input.mp3 -ar 16000 -ac 1 output.wav")
```

### Audio Too Long (Whisper Max ~30 sec per chunk)
**Problem**: Long interview audio causes memory error or truncation
**Solution**: Use chunking in Whisper pipeline:
```python
whisper = pipeline("automatic-speech-recognition", model="openai/whisper-small",
                   chunk_length_s=30, stride_length_s=5)
result = whisper("long_audio.wav", language="bn")
```

### Poor WER Due to Noisy Audio
**Problem**: Model WER is very high (>60%) on your audio
**Solutions**:
1. Apply noise reduction before transcribing:
```python
import noisereduce as nr
audio_clean = nr.reduce_noise(y=audio, sr=16000)
```
2. Filter out clips with heavy background music — these hurt training
3. Target speech-only clips: interviews, patient testimonies, health programs

### yt-dlp Download Fails
**Problem**: YouTube URL fails to download
**Solutions**:
```bash
# Update yt-dlp (YouTube changes frequently)
!pip install -U yt-dlp

# Try downloading as best audio
!yt-dlp -x --audio-format wav "YOUTUBE_URL"
```
- Some videos are geo-blocked or age-restricted — skip those
- Facebook videos: use `yt-dlp` the same way with the Facebook video URL

---

## Model Training Issues

### Training Loss Not Decreasing
**Problem**: Loss stays high after several epochs
**Solutions**:
- Lower learning rate: try `1e-5` or `5e-6` (current plan uses `1e-5`)
- Check that transcripts exactly match the audio content
- Verify audio is at 16kHz mono WAV
- Train for more epochs (current plan: 3–5 epochs)
- Ensure you have enough data (minimum ~100 labeled pairs for Whisper fine-tune)

### WER Very High After Fine-Tuning
**Problem**: Fine-tuned model WER is worse than baseline Whisper
**Solutions**:
- Check transcription quality — wrong manual transcripts hurt training
- Increase dataset size (more labeled audio = better results)
- Try lower learning rate
- Verify you loaded the fine-tuned model correctly, not baseline:
```python
# Load YOUR fine-tuned model (not the original)
model = WhisperForConditionalGeneration.from_pretrained(
    f'{BASE}/02_Phase1_ASR/saved_models/whisper_finetuned'
)
```

### HuggingFace Model Download Fails
**Problem**: `OSError` when loading model from HuggingFace
**Solutions**:
```python
# Add trust_remote_code=True for some models
model = AutoModelForCTC.from_pretrained("model-name", trust_remote_code=True)

# Or force re-download if cache is corrupted
model = AutoModelForCTC.from_pretrained("model-name", force_download=True)
```

---

## File and Path Issues

### FileNotFoundError
**Problem**: Cannot find audio or transcript file
**Solutions**:
1. Use the `BASE` variable — never hardcode paths
2. Verify the file exists:
```python
import os
path = f'{BASE}/01_Dataset/cleaned_audio/barishal/br_001_female_30s.wav'
print(os.path.exists(path))  # must be True
print(os.listdir(f'{BASE}/01_Dataset/cleaned_audio/barishal/'))
```

### Unicode / Encoding Error with Bangla Text
**Problem**: Bangla characters show as `?` or raise `UnicodeDecodeError`
**Solution**: Always specify `encoding='utf-8'` when reading/writing text:
```python
# Reading
with open('transcript.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Writing
with open('transcript.txt', 'w', encoding='utf-8') as f:
    f.write(text)

# CSV
import csv
with open('wer_scores.csv', 'a', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([...])
```

---

## GitHub Issues

### Push Rejected
**Problem**: `git push` fails
**Solutions**:
```bash
git pull origin main    # pull first
git push origin main    # then push
```

### Large File Rejected by GitHub
**Problem**: `.wav`, `.mp3`, or model files too large for GitHub
**Solution**: Add `.gitignore` to your repo:
```
# .gitignore — add these rules
*.wav
*.mp3
*.pt
*.bin
models/
dataset/
__pycache__/
```
> Rule from master plan: **Audio and model weights → Google Drive. Code (.ipynb, .py) → GitHub.**

### Two People Edit the Same Notebook
**Problem**: Conflict when both teammates edit the same Colab notebook
**Solution**: Coordinate via WhatsApp/Messenger before editing — only one person edits at a time. After editing, push the `.ipynb` to GitHub so teammates can pull the latest version.

---

## NER Issues (Phase 2 Reference)

### No Entities Found by NER Model
**Problem**: BanglaBERT returns empty entities
**Solutions**:
- Confirm text is Bangla (not Roman transliteration)
- Check model is loaded for token classification (NER), not text classification
- Try with clearly medical text: `"আমার জ্বর আছে ৫ দিন ধরে প্যারাসিটামল খাচ্ছি"`

### Wrong Entity Labels
**Problem**: SYMPTOM labeled as MEDICATION or vice versa
**Solutions**:
- Need more labeled training data
- Check BIO tagging quality in your `.jsonl` files
- Fine-tune for more epochs

---

## Quick Fixes Checklist

| Problem | Quick Fix |
|---------|-----------|
| Colab disconnected | Re-mount Drive → resume from checkpoint |
| CUDA out of memory | Reduce batch size → restart runtime |
| File not found | Print `os.listdir()` to verify exact path |
| Bangla text garbled | Add `encoding='utf-8'` everywhere |
| Drive path error | Use `MyDrive` not `My Drive` |
| GPU not active | Runtime → Change runtime type → T4 GPU |
| yt-dlp fails | `!pip install -U yt-dlp` to update |
| Model download fails | Add `trust_remote_code=True` |
| Push rejected | `git pull` first, then push |

---

## Error Messages Reference

| Error | Meaning | Fix |
|-------|---------|-----|
| `CUDA out of memory` | GPU RAM full | Reduce batch size |
| `FileNotFoundError` | Wrong path | Verify path with `os.path.exists()` |
| `UnicodeDecodeError` | Encoding issue | Add `encoding='utf-8'` |
| `KeyError` | Wrong dict key | Print keys to debug |
| `AttributeError: 'NoneType'` | Variable is None | Check RESUME_FROM before passing |
| `OSError: model not found` | HuggingFace model load failed | Check model name, add `trust_remote_code=True` |
| `RuntimeError: CUDA error` | GPU crash | Restart runtime, re-mount Drive |

---

## Getting Help

1. Check `commands.md` for ready-to-use code snippets
2. Check `phase1_checklist.md` to see which step you are on
3. Search the exact error message on [Stack Overflow](https://stackoverflow.com)
4. Search HuggingFace forums at [discuss.huggingface.co](https://discuss.huggingface.co)
5. Ask teammates first — coordinate via WhatsApp/Messenger
6. Friday team meeting: bring unresolved blockers
