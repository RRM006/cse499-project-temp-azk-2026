# -*- coding: utf-8 -*-
"""
Constants and Configuration for CSE499 Project
Contains all project constants, paths, and configurations
"""

# Project Information
PROJECT_NAME = "EHR-Based Pre-Consultation Medical Documentation System"
PROJECT_SHORT_NAME = "Bangla EHR"
COURSE = "CSE499A/B Capstone Project"
UNIVERSITY = "North South University"
SUPERVISOR = "Dr. Mohammad Ashrafuzzaman Khan (AzK)"

# Dialects supported by the project
DIALECTS = [
    "dhaka",
    "sylhet", 
    "chittagong",
    "barishal",
    "standard_bangla",
    "kolkata"
]

DIALECT_DISPLAY_NAMES = {
    "dhaka": "Dhaka Bangla",
    "sylhet": "Sylhet dialect",
    "chittagong": "Chittagong dialect",
    "barishal": "Barishal dialect",
    "standard_bangla": "Standard Bangla",
    "kolkata": "Indian Bangla (Kolkata)"
}

# NER Entity Types
NER_ENTITY_TYPES = [
    "SYMPTOM",
    "DISEASE", 
    "MEDICATION",
    "DURATION",
    "ALLERGY",
    "BODY_PART",
    "TREATMENT",
    "DOSAGE"
]

NER_ENTITY_DISPLAY = {
    "SYMPTOM": "Symptom (লক্ষণ)",
    "DISEASE": "Disease (রোগ)",
    "MEDICATION": "Medication (ওষুধ)",
    "DURATION": "Duration (সময়কাল)",
    "ALLERGY": "Allergy (অ্যালার্জি)",
    "BODY_PART": "Body Part (শরীরের অংশ)",
    "TREATMENT": "Treatment (চিকিৎসা)",
    "DOSAGE": "Dosage (মাত্রা)"
}

# BIO Tags
BIO_PREFIXES = ["B-", "I-", "O"]

# Audio Processing
AUDIO_SAMPLE_RATE = 16000  # Standard for ASR models
AUDIO_CHANNELS = 1  # Mono
AUDIO_MAX_DURATION = 300  # 5 minutes max

# Dataset Split Ratios
TRAIN_RATIO = 0.8
VAL_RATIO = 0.1
TEST_RATIO = 0.1

# Model Names - ASR (Phase 1)
ASR_MODELS = {
    "whisper_small": "openai/whisper-small",
    "whisper_medium": "openai/whisper-medium",
    "whisper_large": "openai/whisper-large-v2",
    "wav2vec2_large": "facebook/wav2vec2-large-xlsr-53-bengali",
    "hubert_base": "facebook/hubert-base-ls960",
    "hubert_large": "facebook/hubert-large-ls960",
    "wavlm_base": "microsoft/wavlm-base",
    "wavlm_large": "microsoft/wavlm-large",
    "data2vec": "facebook/data2vec-audio-base-960h",
    "xlsr_53": "facebook/wav2vec2-xlsr-53-english",
    "canary": "nxdra/canary-1b",
    "mms": "facebook/mms-1b-fl102",
}

# Model Names - NER (Phase 2)
NER_MODELS = {
    "banglabert": "csebuetnlp/banglabert",
    "xlmr_base": "xlm-roberta-base",
    "xlmr_large": "xlm-roberta-large",
    "mbert": "bert-base-multilingual-cased",
    "distilbert": "distilbert-base-multilingual-cased",
    "electra": "google/electra-base-discriminator",
}

# Training Hyperparameters
WHISPER_TRAINING_ARGS = {
    "learning_rate": 1e-5,
    "per_device_train_batch_size": 8,
    "per_device_eval_batch_size": 8,
    "num_train_epochs": 3,
    "save_strategy": "epoch",
    "evaluation_strategy": "epoch",
    "logging_steps": 100,
    "warmup_steps": 500,
    "fp16": True,
}

WAV2VEC2_TRAINING_ARGS = {
    "learning_rate": 3e-4,
    "per_device_train_batch_size": 8,
    "per_device_eval_batch_size": 8,
    "num_train_epochs": 10,
    "gradient_accumulation_steps": 2,
    "save_strategy": "epoch",
    "evaluation_strategy": "epoch",
}

BERT_TRAINING_ARGS = {
    "learning_rate": 2e-5,
    "per_device_train_batch_size": 16,
    "per_device_eval_batch_size": 16,
    "num_train_epochs": 10,
    "save_strategy": "epoch",
    "evaluation_strategy": "epoch",
    "weight_decay": 0.01,
}

# Evaluation Metrics
ASR_METRICS = ["WER", "CER"]
NER_METRICS = ["Precision", "Recall", "F1-Score"]

# Target Performance
TARGET_WER = 0.30  # 30% Word Error Rate (lower is better)
TARGET_F1 = 0.75  # 75% F1-Score (higher is better)

# File Extensions
AUDIO_EXTENSIONS = [".wav", ".mp3", ".flac", ".ogg"]
TEXT_EXTENSIONS = [".txt", ".json"]
MODEL_EXTENSIONS = [".pt", ".pth", ".bin", ".safetensors"]

# Search Keywords by Dialect
DIALECT_SEARCH_KEYWORDS = {
    "dhaka": {
        "bangla": ["ঢাকা রোগী সাক্ষাৎকার", "ঢাকা স্বাস্থ্য", "ঢাকা ডাক্তার পরামর্শ"],
        "english": ["Dhaka patient interview", "Dhaka medical consultation"]
    },
    "sylhet": {
        "bangla": ["সিলেট স্বাস্থ্য", "সিলেট ডাক্তার", "সিলেট রোগী"],
        "english": ["Sylhet doctor advice", "Sylhet medical interview"]
    },
    "chittagong": {
        "bangla": ["চট্টগ্রাম স্বাস্থ্য", "চট্টগ্রাম ডাক্তার"],
        "english": ["Chittagong health", "Chittagong medical"]
    },
    "barishal": {
        "bangla": ["বরিশাল স্বাস্থ্য", "বরিশাল ডাক্তার"],
        "english": ["Barishal health", "Barishal doctor"]
    },
    "standard_bangla": {
        "bangla": ["স্বাস্থ্য পরামর্শ", "ডাক্তার পরামর্শ", "বাংলা স্বাস্থ্য"],
        "english": ["Bangla health advice", "Bengali medical consultation"]
    },
    "kolkata": {
        "bangla": ["কলকাতা ডাক্তার", "পশ্চিমবঙ্গ স্বাস্থ্য"],
        "english": ["Kolkata doctor", "West Bengal health", "ABP Ananda health"]
    }
}

# Common Bengali Medical Terms
MEDICAL_TERMS_BANGLA = {
    "symptoms": [
        "জ্বর", "কাশি", "সর্দি", "মাথা ঘুরা", "মাথাব্যথা",
        "বুকে ব্যথা", "পেটে ব্যথা", "গলা ব্যথা", "শ্বাসকষ্ট",
        "ডায়রিয়া", "বমি", "শিরায় যন্ত্রণা", "ক্ষুধামান্দ্য"
    ],
    "diseases": [
        "ডায়াবেটিস", "উচ্চ রক্তচাপ", "হাঁপানি", "কোভিড",
        "ক্যান্সার", "হৃদরোগ", "কিডনি রোগ", "লিভার রোগ"
    ],
    "medications": [
        "প্যারাসিটামল", "আইবুপ্রোফেন", "অ্যাজিথ্রোমাইসিন",
        "অ্যামক্সিসিলিন", "ওমেপ্রাজল", "মেটফর্মিন", "ইনসুলিন"
    ]
}

# EHR Template Fields
EHR_TEMPLATE_FIELDS = [
    "patient_id",
    "consultation_date",
    "chief_complaint",
    "medical_history",
    "vital_signs",
    "assessment_and_plan",
    "raw_transcription",
    "extracted_entities"
]

# Version
__version__ = "1.0.0"
__author__ = "CSE499 Team - NSU"
