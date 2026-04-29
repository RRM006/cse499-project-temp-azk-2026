# Skills Required for CSE499 Project

## Overview
This document outlines the technical skills needed to complete the EHR-Based Pre-Consultation Medical Documentation System project.

---

## 1. Python Programming (Essential)

### Beginner Level Required
- Basic Python syntax (variables, loops, functions)
- File handling (read/write text, JSON, CSV)
- Working with libraries

### Intermediate Skills Needed
- Object-oriented programming
- List/dictionary comprehensions
- Error handling
- Virtual environments

### Resources
- Codecademy Python Course
- W3Schools Python Tutorial
- Real Python (realpython.com)

---

## 2. Google Colab

### Must Know
- Creating and running notebooks
- Mounting Google Drive
- Installing libraries (!pip install)
- Using GPU runtime
- Saving files to Drive

### Tips for Free Colab
- Save checkpoints frequently
- Don't leave notebook idle too long
- Use `!nvidia-smi` to check GPU
- Clear memory with `gc.collect()`

---

## 3. Machine Learning Basics

### Concepts to Understand
- What is a neural network
- Training vs inference
- Loss functions
- Epochs and batch size
- Overfitting and underfitting
- Evaluation metrics (WER, F1-score)

### Resources
- 3Blue1Brown Neural Network series (YouTube)
- Andrew Ng's ML course (Coursera)

---

## 4. Deep Learning Frameworks

### PyTorch Basics
- Tensors creation and manipulation
- Loading data with DataLoader
- Building simple models
- Training loops
- Using GPU

### Hugging Face Transformers
- Loading pre-trained models
- Fine-tuning models
- Using pipelines
- Processing data

---

## 5. Audio Processing

### Basic Skills
- Loading audio with librosa
- Resampling audio (to 16kHz)
- Audio normalization
- Removing silence
- Converting formats (wav, mp3)

### Tools
- `librosa` - Audio analysis
- `soundfile` - Audio file I/O
- `ffmpeg` - Audio conversion
- `yt-dlp` - YouTube downloads

---

## 6. Natural Language Processing (NLP)

### Required Knowledge
- Text preprocessing
- Tokenization
- Named Entity Recognition (NER)
- BIO tagging scheme
- Sequence labeling

### BERT-based Models
- Understanding transformer architecture
- Fine-tuning for token classification
- Loading multilingual models

---

## 7. Git and Version Control

### Basic Commands
```bash
git init
git add .
git commit -m "message"
git push origin main
git pull
git status
git branch
```

### Best Practices
- Commit frequently
- Write meaningful messages
- Use .gitignore
- Don't commit large files

---

## 8. Data Collection & Annotation

### YouTube Data Collection
- Using yt-dlp for downloads
- Searching for dialect-specific content
- Respecting copyright
- Organizing downloaded files

### Annotation Skills
- Creating labeled datasets
- BIO format for NER
- Using annotation tools
- Ensuring annotation consistency

---

## 9. Project Management

### Team Collaboration
- Using Google Drive for sharing
- Creating shared folders
- Setting permissions
- Communication tools (WhatsApp, Discord)

### Documentation
- README files
- Code comments
- Experiment logs
- Results documentation

---

## 10. Medical Domain Knowledge

### Basic Understanding
- Common symptoms in Bangla
- Medical terminology in Bengali
- Drug names (generic and brand)
- Common diseases in Bangladesh
- Patient history components

### EHR Structure
- Chief complaint
- Medical history
- Current medications
- Allergies
- Assessment and plan

---

## Skill Learning Order

### Phase 1 (Weeks 1-3)
1. Python basics
2. Google Colab
3. Git basics
4. Audio processing basics

### Phase 2 (Weeks 4-6)
5. PyTorch fundamentals
6. Hugging Face transformers
7. ML concepts

### Phase 3 (Weeks 7+)
8. NER concepts
9. Fine-tuning BERT models
10. Project integration

---

## Quick Reference Commands

### Colab Setup
```python
# Mount Drive
from google.colab import drive
drive.mount('/content/drive')

# Install packages
!pip install transformers datasets torch librosa

# Check GPU
import torch
print(torch.cuda.is_available())
```

### Git Setup
```bash
git init
git add .
git commit -m "initial commit"
git remote add origin <repo-url>
git push -u origin main
```

---

## Checklist: Skills to Verify

- [ ] Can run Python in Colab
- [ ] Can mount Google Drive
- [ ] Can install packages
- [ ] Can load and play audio
- [ ] Can save files to Drive
- [ ] Understands training vs inference
- [ ] Can use git for version control
- [ ] Knows basic ML terms

---

## If You're Stuck

1. **Google it** - Most problems have solutions online
2. **Check documentation** - PyTorch, Hugging Face docs
3. **Ask on forums** - Stack Overflow, Reddit
4. **Ask team members** - Collaborative learning
5. **Ask AI** - Use this project to generate code

---

*This guide helps beginners build necessary skills. Focus on learning one skill at a time and practice with actual code.*
