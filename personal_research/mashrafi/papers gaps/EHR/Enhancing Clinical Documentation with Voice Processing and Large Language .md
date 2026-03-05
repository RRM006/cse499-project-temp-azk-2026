# Paper Reading: EHR-Based Pre-Consultation Medical Documentation System
**Paper:** Enhancing Clinical Documentation with Voice Processing and Large Language Models: A Study on the LAOS System

---

## 1. Basic Information

| Field | Details |
|---|---|
| **Title** | Enhancing Clinical Documentation with Voice Processing and Large Language Models: A Study on the LAOS System |
| **Authors** | Yupeng Xu, Huixun Jia, Maolin Wang, Jie Feng, Xun Xu, Haiyan Wang, Jieqiong Chen, Zheng Zheng, Xiaoyan Yang, Yue Shen, Jian Wang, Chenyi Zhuang, Peng Wei, Ruocheng Guo, Xiangyu Zhao, Junxiang Fan, Xiaodong Sun |
| **Affiliation** | Shanghai General Hospital, Shanghai Jiao Tong University School of Medicine; City University of Hong Kong; Ant Group |
| **Journal** | npj Digital Medicine |
| **Year** | 2025 (Published online: 28 November 2025) |
| **DOI** | https://doi.org/10.1038/s41746-025-02170-4 |
| **Code** | https://github.com/XWF-AntHos/LAOS |

---

## 2. Research Context

**Domain (checked):**
- ☑ Speech Recognition (ASR)
- ☑ Medical NLP
- ☑ Information Extraction
- ☑ EHR Systems

**Specific Sub-domain:** Voice-to-EHR pipeline using LLM + RAG for clinical documentation; specialty-specific (ophthalmology); bilingual (Mandarin + English medical terminology); code-switching handling.

### Relevance to Our Project (1–5)

| Component | Score | Reason |
|---|---|---|
| ASR component | ★★★★☆ (4/5) | Directly uses a fine-tuned ASR model (Paraformer + LoRA) for medical speech; WER numbers and noise-handling strategies are directly applicable |
| Medical NLP | ★★★★★ (5/5) | The full pipeline (voice → transcript → structured EHR) is nearly identical to our goal |
| Bangla/multilingual | ★★★☆☆ (3/5) | Not Bangla, but the code-switching (Mandarin + English medical terms) problem mirrors our Bangla + English situation |
| Accent handling | ★★☆☆☆ (2/5) | No accent/dialect work done; single-language (Mandarin) clinical setting |
| EHR integration | ★★★★★ (5/5) | End-to-end EHR generation with JSON output and EMR field population is exactly what we are building |

**Most Relevant For:**
- ☑ Understanding ASR architecture
- ☑ Fine-tuning strategies
- ☑ Medical entity extraction
- ☑ Dataset creation methods
- ☑ Evaluation metrics
- ☑ System integration

---

## 3. Problem Definition

### A. What problem does this paper solve?
Doctors spend 36–40% of their work time on EHR documentation instead of patient care. This paper builds LAOS — a system that listens to doctor–patient conversations in real time, converts speech to text, and automatically generates structured clinical documents (admission reports, surgery records, discharge summaries) using a fine-tuned LLM.

### B. How does this relate to OUR project?

| | Detail |
|---|---|
| **Direct application** | Their voice → transcript → structured EHR pipeline is the exact same architecture we are building, just for a different language (Bangla) and a different setting (pre-consultation rather than post-consultation) |
| **Inspired approach** | Using a fine-tuned small LLM (7B parameters) on domain-specific data to generate JSON-formatted EHRs — we can do something similar with BanglaBERT + a rule-based filler |
| **Technique we can borrow** | LoRA fine-tuning for domain adaptation on limited data, RAG for grounding outputs in medical terminology, and their V2T-CES evaluation scale for assessing our ASR module |

### C. What is their solution approach?
Three-stage pipeline: (1) Fine-tuned Paraformer ASR model transcribes clinical speech; (2) Qwen2-7B-SFT (fine-tuned with LoRA) generates structured clinical documents from transcripts with RAG providing domain-specific terminology and clinical precedents; (3) Structured JSON output is populated into EMR fields. Evaluation uses both automated NLP metrics and clinical reader validation by board-certified physicians.

---

## 4. Methodology Analysis

### Model/Approach Used

| Component | Details |
|---|---|
| **ASR Model** | Paraformer (non-autoregressive, end-to-end) + LoRA fine-tuning |
| **NLP/LLM Model** | Qwen2-7B (best performer), also tested ChatGLM2-6B, Baichuan-13B, Qwen-7B |
| **Fine-tuning method** | LoRA (Low-Rank Adaptation) — rank=8, alpha=32, lr=1e-4 |
| **Knowledge retrieval** | RAG with Chroma vector DB + BGE-Large-En embeddings |
| **Key innovation** | First system to combine specialty-specific ASR + LoRA-fine-tuned LLM + RAG in a single clinical documentation pipeline, validated by both NLP metrics AND clinical reader study |

### Pipeline / Workflow

```
Real-time Voice Input
        ↓
[1] Paraformer ASR (LoRA fine-tuned on ophthalmic dictations)
        ↓
    Transcript (Mandarin + English medical terms)
        ↓
[2] LLM Planning Module (Qwen2-7B-SFT)
        ↓       ↑ RAG: retrieves top-5 relevant docs from Chroma DB
[3] Multi-turn Generation (LLM drafts document sections)
        ↓
[4] Automatic Evaluation (BLEU, ROUGE-L, BERTScore) + Manual Feedback
        ↓
[5] Final Structured EMR (JSON format → Admission Report / Surgery Record / Discharge Summary)
```

### Training Strategy

| Step | Detail |
|---|---|
| **Pre-training** | Yes — Paraformer pre-trained on public Mandarin datasets (AISHELL-1, MagicData); Qwen2 pre-trained on large Chinese+English corpus |
| **Fine-tuning** | Yes — Paraformer fine-tuned with LoRA on 50+ hours of de-identified ophthalmology speech; LLM fine-tuned on 1,000 clinical case documents |
| **Transfer learning** | Mandarin → Ophthalmology domain (language stays same, domain shifts); relevant to us: general Bangla model → Medical Bangla domain |

---

### Specific Techniques for Our Use Case

#### 1. Speech Recognition Approach

**ASR Architecture:**
- Paraformer: non-autoregressive (faster than autoregressive models like standard Whisper), end-to-end, supports streaming for real-time transcription
- Self-attention + CNN hybrid for feature extraction from raw audio
- Two-stage noise reduction: (a) spectral subtraction for stationary noise, (b) deep learning denoising autoencoder for non-stationary noise (important: clinical environments are noisy)
- LoRA applied to fine-tune only a subset of parameters → reduces compute, prevents overfitting on small domain dataset

**Data augmentation:** Not explicitly mentioned, but noise reduction pipeline effectively handles noisy environments.

**Fine-tuning approach:** LoRA with rank=8, alpha=32, lr=1e-4, 3 epochs, batch size=128, early stopping on validation perplexity.

> **For us:** Replace Paraformer with Whisper (already supports Bangla). Apply LoRA to fine-tune on our 200–300 Bangla medical recordings. Their noise-handling approach is directly relevant.

#### 2. Code-Switching / Multilingual Handling

- Their clinical speech is ~80% Mandarin + ~20% English medical terms (drug names, abbreviations, diagnoses) — **this mirrors our Bangla + English code-mixed scenario almost exactly**
- Solution: Base Paraformer supports both languages; fine-tuning corpus intentionally includes a "targeted corpus of English medical terminology"
- RAG knowledge base is also ~80% Mandarin + English technical terms

> **For us:** When fine-tuning Whisper on Bangla medical speech, intentionally include code-mixed samples. Build vocabulary/terminology list for medical English terms that Bangladeshi patients commonly use.

**Gap identified:** They don't handle multiple dialects. This is a key differentiator of our project — we need additional dialect-specific data collection.

#### 3. Medical/Domain-Specific Processing

**Information extraction method:** LLM-based (Qwen2-7B-SFT) — not rule-based or CRF; prompts instruct the model to output JSON format directly.

**Medical entities extracted (in their case):**
- Chief complaint
- Present illness history
- Past history
- Physical examination findings
- Auxiliary examination results
- Surgery details (procedure name, intraoperative findings, diagnosis)
- Discharge status, instructions, treatment process

**Structuring approach for EHR:**
- JSON-formatted output specified in prompt: `"Use JSON format for data"`
- RAG retrieves standardized terminology from a curated ophthalmology terminology database
- Default values filled for unmentioned examination fields (e.g., "Right eye visual acuity: 20/40 (Snellen), clear conjunctiva, transparent cornea")

> **For us:** Our rule-based template filler approach is simpler and more feasible given zero budget. However, we can borrow their JSON output prompt strategy if we eventually use any LLM (even via free API). Their entity categories map well to our target: symptoms, diseases, medications, duration, allergies.

---

## 5. Data & Experimental Setup

| Field | Details |
|---|---|
| **Dataset — ASR** | Public: AISHELL-1 (178 hrs Mandarin), MagicData-RAMC; Proprietary: 50+ hours annotated ophthalmology dictations from Shanghai General Hospital |
| **Dataset — LLM Fine-tuning** | 1,000 high-quality clinical cases; split: Admission Reports (200 train / 50 val / 50 test), Surgery Records (150/38/38), Discharge Summaries (200/50/50) |
| **Dataset — RAG KB** | 10,000+ de-identified historical EHRs + ophthalmology textbooks + clinical guidelines + structural templates |
| **Language** | Mandarin (~80%) + English medical terms (~20%) |
| **Domain** | ☑ Medical (ophthalmology / cataract-heavy) |
| **Accent/Dialect coverage** | None — single-dialect (standard Mandarin) |
| **Can I access this data?** | ☒ No — proprietary hospital data, not publicly released (de-identified data available on reasonable request from IRB) |
| **Data Collection Method** | Clinical recordings from operating rooms and outpatient consultations; annotated by clinical staff; de-identified per IRB approval |
| **Preprocessing** | 512-token chunks with 50-token overlap for RAG; noise reduction pipeline for audio; formatting standardization for clinical text comparison |

---

## 6. Evaluation Metrics

### ASR Performance

| Metric | Value | Environment |
|---|---|---|
| WER (Mandarin) | **4.2%** | Clinical setting (50 hrs of recordings) |
| WER (English medical terms) | **5.1%** | Clinical setting |
| Accuracy Index (V2T-CES) | 83.2% | General |
| Efficiency Index | 87.6% (62% reduction in doc time) | General |
| System Compatibility | 81.4% | EMR integration |
| Accuracy in noisy conditions | ~12% drop from peak (91.3% → ~80%) | Operating room |
| Average latency | 0.3s | Operating room |

### NLP / EHR Generation Performance (Best model: Qwen2-7B-SFT-RAG)

| Document Type | BERTScore | ROUGE-L | BLEU |
|---|---|---|---|
| Admission Report | 86–88 | 48–52 | 20–24 |
| Surgery Record | 80–84 | 35–45 | 10–16 |
| Discharge Summary | 82–86 | 45–55 | 16–22 |

### Clinical Reader Study (Qwen2-7B-SFT-RAG vs human expert)

| Document | Completeness | Correctness | Conciseness |
|---|---|---|---|
| Admission Records | 2.8 ± 2.8* | 2.7 ± 2.9* | 3.2 ± 3.0** |
| Surgery Records | 1.7 ± 5.1** | 0.7 ± 3.8* | 0.6 ± 3.6* |
| Discharge Summaries | 2.9 ± 3.0* | 2.7 ± 3.4* | 3.3 ± 3.4** |

*Positive scores = LLM outperforms human expert; p < 0.05*

### Error Rates: LLM vs Human

| Error Type | Human | LLM |
|---|---|---|
| Total unusable rate | 7.8% | 6.4% |
| Ambiguity misinterpretation | 4.8% | 3.5% |
| Factual inaccuracies | 3.9% | 2.8% |
| Hallucinations | 2.7% | 2.4% |

### Correlation: NLP Metrics vs Clinical Preference
Low correlations (~0.2) — meaning NLP metrics alone are insufficient. **Clinical reader studies are essential.**

### Experimental Settings

| Setting | Value |
|---|---|
| Train/Val/Test | ~70/15/15 (approximate) |
| LLM temperature | 0.1 (minimize randomness) |
| Top-p / Top-k | 0.9 / 40 |
| Max sequence length | 2048 tokens |
| LoRA rank / alpha | 8 / 32 |
| RAG chunk size / overlap | 512 tokens / 50 tokens |
| RAG top-k retrieval | 5 documents |
| Framework | LLaMA-Factory (hiyouga), Chroma, Qwen2 |
| Hardware | Not specified (likely GPU cluster at hospital) |

---

## 7. Key Results & Findings

**What worked well:**
- LoRA fine-tuning gave statistically significant improvement (p < 0.005) over baseline Qwen2-7B
- RAG improved performance notably (p = 0.036) — reduced hallucinations by grounding in medical terminology
- Discharge summaries were easiest to generate (structured, standardized format)
- LLM outperformed human experts in error rates across all categories
- System saved 62% documentation time on average

**What didn't work:**
- Surgery records performed worst (real-time procedural descriptions, more specialized terminology, less training data)
- 12% accuracy drop in noisy environments
- NLP metrics (BLEU, ROUGE-L, BERTScore) correlate weakly (~0.2) with clinical quality — can't rely on them alone
- LLM sometimes verbose or omitted concise but critical details

**Common error patterns:**
- Ambiguity misinterpretations: model misunderstands unclear speech/input
- Hallucinations: model invents details not in input (still lower than human rate)
- Compound technical terms were harder for ASR to transcribe

**Limitations mentioned:**
- Dataset focused only on ophthalmology / cataract cases (performance likely drops on other specialties)
- Small LLM (7B) used due to compute constraints
- Single institution, single dialect
- RAG depends on structured knowledge base — may degrade with incomplete/unstructured patient data

---

## 8. Implementation Notes

| Item | Detail |
|---|---|
| **Frameworks** | LLaMA-Factory, Qwen2, Chroma, BGE-Large-En, bge-reranker-large, Paraformer |
| **LoRA config** | rank=8, alpha=32, target modules: self-attention Q/K/V, dense layers, FFN |
| **RAG config** | Chroma vector DB, 512-token chunks, 50-token overlap, top-5 retrieval, reranked by bge-reranker-large |
| **LLM inference** | temperature=0.1, top-p=0.9, top-k=40, max_seq=2048, sliding window=1024 |
| **Training** | lr=1e-4, batch size=128, 3 epochs, early stopping (patience=3, min PPL improvement=0.01) |
| **Code available** | ☑ Yes — https://github.com/XWF-AntHos/LAOS |
| **Pre-trained models** | ☑ Yes (Qwen2-7B, Paraformer publicly available; fine-tuned versions not released) |
| **Can we reproduce?** | ☑ Partially |

**Constraints for us:**
- Compute: We use Google Colab (free tier). They likely used hospital GPU cluster. LoRA at rank=8 with 7B model needs ~16GB VRAM — too heavy for free Colab. **For us: use smaller model (BanglaBERT is 110M params, feasible) or use Whisper small/medium for ASR.**
- Data: Their proprietary 50hr ASR dataset and 1,000 clinical cases are not available. We have ~200–300 recordings.
- RAG: ChromaDB is free and open-source — we can implement this if we have a medical terminology resource in Bangla/English.

---

## 9. Relevance to Our Project

**Can I use their approach?** ☑ Partially

| What is applicable | What is NOT applicable |
|---|---|
| LoRA fine-tuning strategy for ASR (directly applicable to Whisper) | Paraformer model (not available/supported for Bangla) |
| Code-switching (Mandarin+English) solutions mirror our Bangla+English need | Their LLM models (Chinese-focused: Qwen, Baichuan, ChatGLM) don't support Bangla |
| RAG architecture with Chroma + medical terminology KB | Their proprietary dataset (not available) |
| JSON output format for EHR structuring | Their ophthalmology-specific templates |
| V2T-CES evaluation scale (can adapt for our project) | Large compute for full LLM fine-tuning (we must use rule-based NER instead) |
| Noise reduction pipeline concepts | 7B+ LLM deployment on free Colab |
| Clinical reader study methodology | Their RAG knowledge base (ophthalmology; we need general medicine in Bangla) |
| BLEU / ROUGE-L / BERTScore as evaluation metrics | — |

---

## 10. Questions & Follow-ups

**Confusing parts:**
- The paper says Qwen2-7B-SFT-RAG "outperformed medical expert summaries" — but the reader scores are positive (LLM better), which seems to contradict typical expectations. Need to re-read how scores are calculated. *(Answer: positive scores = LLM is preferred; the scale is relative)*
- How exactly is the RAG knowledge base separated from fine-tuning data to prevent leakage? (They mention it but don't give full details)

**Unclear concepts to research:**
- Paraformer architecture (non-autoregressive ASR) — how does it compare to Whisper for speed/accuracy?
- BGE-Large-En embedding model — is there a multilingual or Bangla version?
- Perplexity (PPL) as a training metric — what is a "good" PPL for medical text?

**Questions for supervisor AZK:**
1. Given our Bangla focus, should we use Whisper (multilingual, supports Bangla) or explore alternatives like wav2vec2-based Bangla models? This paper shows Paraformer works well for Mandarin — is there an equivalent non-autoregressive model for Bangla?
2. Since we can't run a 7B LLM fine-tuning on Colab, our rule-based EHR filler approach is justified — but should we consider using a free LLM API (e.g., Gemini free tier) for the generation step instead of pure rule-based?
3. Can we adapt their V2T-CES evaluation scale for our project's ASR evaluation? What would be the Bangla medical equivalent of their ophthalmology terminology?

**Discussion points with team:**
- Should our pipeline use a small LLM via API (zero local compute) for EHR structuring, like LAOS does, or stick with rule-based filler?
- We need a medical terminology list in Bangla + English — this paper shows it's critical for both RAG and for ASR fine-tuning. Who on the team can compile this?
- Their dataset had 50 hours of audio. We have 200–300 samples (~6–10 hours likely). How do we compensate? Augmentation? Cross-lingual transfer?

---

## 11. Project Integration Plan

**Which phase of OUR project uses this?**
- ☑ ASR baseline setup (Whisper architecture informed by this paper's Paraformer + LoRA approach)
- ☑ Fine-tuning ASR (LoRA strategy, training hyperparameters directly applicable)
- ☑ Medical NER (entity types and structuring approach)
- ☑ Data collection strategy (their 50hr corpus design informs our volunteer recording protocol)
- ☑ System integration (JSON output, API interface design)
- ☑ Evaluation (V2T-CES scale, BLEU/ROUGE-L/BERTScore metrics, clinical reader study design)

**Specific action items:**
1. Adapt their LoRA fine-tuning config (rank=8, alpha=32, lr=1e-4) for fine-tuning Whisper on our 200–300 Bangla medical recordings
2. Build a simple Bangla medical terminology list (symptoms, drugs, diseases) to use as our lightweight "RAG" equivalent — a lookup dictionary that BanglaBERT NER can be grounded in
3. Adapt their V2T-CES evaluation scale into a Bangla-appropriate clinical evaluation form for our volunteer pilot study
4. Use JSON output format for our EHR template (their prompt design with explicit JSON instruction is directly copyable)
5. Plan for multi-domain robustness from the start — their model degraded heavily on less-common disease types; we should collect balanced symptom/disease coverage in our recordings

---

## 12. Keywords & Concepts

**Project-Relevant Keywords:**
1. Voice-to-EHR pipeline
2. LoRA (Low-Rank Adaptation) fine-tuning
3. Retrieval-Augmented Generation (RAG)
4. Code-switching ASR (bilingual medical speech)
5. Clinical documentation automation
6. Paraformer / non-autoregressive ASR
7. BERTScore / ROUGE-L / BLEU (NLP evaluation metrics)
8. Medical Named Entity Recognition (NER)
9. JSON-structured EHR output
10. Domain-specific LLM fine-tuning

**Technical Terms to Learn:**
1. **LoRA (Low-Rank Adaptation):** A method to fine-tune only a small set of additional parameters (rank-decomposed matrices) instead of the full model weights. Saves GPU memory and reduces overfitting on small datasets — critical for us.
2. **RAG (Retrieval-Augmented Generation):** Instead of the model relying only on what it learned during training, it first retrieves relevant documents from a database and uses them as context. Reduces hallucinations. We could implement a simple version with a Bangla medical dictionary.
3. **Perplexity (PPL):** A metric for language models — lower = model is more confident/accurate on the text. Used for early stopping during training.
4. **Non-autoregressive ASR:** Unlike standard models that generate tokens one by one (slow), Paraformer predicts all tokens simultaneously — much faster for real-time use.
5. **BERTScore:** Uses BERT embeddings to measure semantic similarity between generated text and reference text. Better than BLEU for medical text because it understands synonyms and paraphrases.

---

*Completed reading: March 2026 | Relevance score: 4.2/5 overall | Priority: HIGH for ASR fine-tuning and EHR pipeline design*
