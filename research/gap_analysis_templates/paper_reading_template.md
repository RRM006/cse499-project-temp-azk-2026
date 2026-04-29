# **EHR-Based Pre-Consultation Medical Documentation System (Bangla)**

## **Instructions for the AI Reading the Paper**

You are helping a **beginner ML/NLP team** build a Bangla speech-to-EHR system. Project context:

* **Pipeline:** Patient speaks → ASR → Medical NER → Structured EHR → (optional) differential diagnosis hints for the doctor  
* **Languages:** Bangla (primary) \+ Bangla-English code-mixed  
* **Dialects:** Dhaka, Sylhet, Chittagong, Barishal, etc.  
* **Resources:** Zero budget, Google Colab only (T4 GPU, \~15GB VRAM, \~12h session limit)  
* **Data:** \~200-300 self-collected Bangla medical audio recordings  
* **Entities to extract:** symptoms, diseases, medications, duration, allergies

### **Rules for filling this form**

1. If a field is **not applicable** to the paper → write **N/A**.  
2. If you are **not sure / the paper is ambiguous** → write **"Unsure: \[reason\]"**. Do NOT guess silently.  
3. If an entire section is irrelevant → write **"Not covered in paper"** and skip subfields.  
4. **Be brief.** Bullet points \> paragraphs. **Paraphrase**, do not copy text from the paper.  
5. Always end each major section with a one-line **"Why this matters for our project."**  
6. At the very end, list every place you were unsure (Section 13).

---

## **1\. Basic Information**

* **Title:**  
* **Authors:**  
* **Affiliation / Venue / Journal:**  
* **Year:**  
* **Paper link:**  
* **Code / model link (if any):**

---

## **2\. Quick Relevance Snapshot**

**Primary domain(s) covered (tick all that apply):**

* \[ \] Speech Recognition (ASR)  
* \[ \] Medical NLP / Clinical Information Extraction  
* \[ \] Bangla / Low-Resource NLP  
* \[ \] Accent / Dialect handling  
* \[ \] Code-Switching / Code-Mixing  
* \[ \] EHR / Clinical Documentation  
* \[ \] Differential Diagnosis / Clinical Reasoning  
* \[ \] Other: \_\_\_\_\_\_

**Relevance scores (1 \= irrelevant, 5 \= directly usable in our project):**

| Aspect | Score | One-line reason |
| ----- | ----- | ----- |
| ASR for our pipeline | /5 |  |
| Medical entity extraction | /5 |  |
| Bangla / low-resource techniques | /5 |  |
| Dialect / code-mixing | /5 |  |
| EHR structuring | /5 |  |
| Feasible on free Colab | /5 |  |

**Overall verdict:** Deep-study / Partial-read / Skim / Skip — *why*:

---

## **3\. Problem & Solution**

**A. What problem does the paper solve?** (2–3 sentences, plain English)

**B. Their core approach in 2–4 sentences:**

**C. Connection to our project:**

* Direct application:  
* Technique we can borrow:  
* Where their setting differs from ours:

---

## **4\. Methodology**

Fill ONLY the subsections (4A–4D) that the paper actually covers. Mark the others "Not covered."

### **4A. Speech Recognition *(only if the paper does ASR)***

* ASR model (e.g., Whisper, Wav2Vec2, Conformer, MMS):  
* Pre-trained on what data?  
* Fine-tuned on what data?  
* Language model / decoder used:  
* Data augmentation (SpecAugment, noise, speed perturb, etc.):  
* How they handle **accents / dialects**:  
* How they handle **code-switching**:

### **4B. Medical NLP / NER *(only if the paper does medical IE)***

* Model (BiLSTM-CRF, BERT, mBERT, BanglaBERT, LLM, rule-based, hybrid):  
* Entity types extracted (symptoms, meds, dose, duration, allergies, diagnosis…):  
* Annotation scheme (BIO / BIOES / span / other):  
* Medical terminology source (UMLS / SNOMED / ICD / custom dictionary / learned):  
* Output format (JSON / FHIR / template / other):

### **4C. Low-Resource / Cross-Lingual / Code-Mixing tricks *(only if relevant)***

* Data-scarcity solutions (transfer learning, augmentation, synthetic data, back-translation, self-training):  
* Cross-lingual transfer (source → target language):  
* Code-mix handling:

### **4D. Differential Diagnosis / Clinical Reasoning *(only if covered)***

* Method (rule-based, knowledge graph, ML classifier, LLM, retrieval):  
* Knowledge source (ICD, textbooks, expert rules, curated dataset):

### **4E. Pipeline diagram (in text)**

Input → \[Step 1\] → \[Step 2\] → … → Output

**Why this matters for our project:**

---

## **5\. Data**

* **Dataset name:**  
* **Size** (hours of audio / number of samples):  
* **Language(s):**  
* **Domain:** general / medical / other  
* **Dialect / accent coverage:**  
* **Publicly available?** Yes / No / Restricted — link:  
* **Collection method:** clinical / crowdsourced / simulated / scraped  
* **Annotation process** (who annotated, inter-annotator agreement, guidelines):  
* **Preprocessing steps:**

**Can we use this dataset?** Yes / No / Partial — *why*:

---

## **6\. Evaluation**

Only fill metrics actually reported in the paper. Others \= N/A.

| Category | Metric | Score |
| ----- | ----- | ----- |
| ASR | WER |  |
| ASR | CER |  |
| NER / IE | Precision |  |
| NER / IE | Recall |  |
| NER / IE | F1 |  |
| NER / IE | Entity-level F1 |  |
| Clinical / EHR | clinical accuracy / doctor satisfaction / time saved |  |
| Other |  |  |

* **Train / Val / Test split:**  
* **Hardware used:**  
* **Framework** (PyTorch, HuggingFace, ESPnet, Kaldi, other):

---

## **7\. Key Results & Findings**

* **Best result achieved:**  
* **Compared to which baselines?** By how much better?  
* **What worked well:**  
* **What didn't work / failure cases:**  
* **Error analysis highlights:**  
* **Authors' stated limitations:**

---

## **8\. Reproducibility & Feasibility for Us**

* **Code available?** Yes / No / Partial — link:  
* **Pre-trained models available?** Yes / No — link:  
* **Rough GPU need:**  
* **Will this run on free Colab (T4, \~15GB VRAM, 12h)?** Yes / Maybe / No — *why*:  
* **Data accessible to us?** Yes / No / Partial:  
* **Estimated time to reproduce a small/demo version:** hours / days / weeks  
* **Feasibility verdict:** Fully reproducible / Partial / Demo only / Not feasible

---

## **9\. Direct Takeaways for Our Project**

**Things we can copy / adapt directly:** 1\. 2\. 3\.

**Things to avoid / not applicable to us:** 1\. 2\.

**Open questions this paper raises for us:** 1\. 2\.

**Which phase of our project does this help?** (tick all)

* \[ \] ASR baseline setup (Whisper / Wav2Vec2 / etc.)  
* \[ \] Bangla ASR fine-tuning  
* \[ \] Dialect / code-mix handling  
* \[ \] Data collection & annotation strategy  
* \[ \] Medical NER  
* \[ \] EHR structuring (JSON / template)  
* \[ \] Differential diagnosis hints  
* \[ \] Evaluation methodology  
* \[ \] System integration

---

## **10\. Action Items**

Concrete next steps after reading this paper: 1\. 2\. 3\.

---

## **11\. Questions for Supervisor / Team**

## **For supervisor (AZK):**

* 

## **For team discussion:**

* 

---

## **12\. Keywords & Concepts**

**Keywords from the paper relevant to our project (≥5):** 1\. 2\. 3\. 4\. 5\.

**Technical terms our team needs to learn:** 1\. 2\. 3\.

---

## **13\. AI Reader's Confidence Note (REQUIRED)**

List every place you were unsure, guessed, or where the paper was ambiguous. Be honest — this helps the team know which fields to double-check.

* Section \_\_\_ : unsure because \_\_\_  
* Section \_\_\_ : paper didn't clearly state \_\_\_  
* Section \_\_\_ : my guess based on context, not stated explicitly \_\_\_

*(If everything was clear, write: "All sections answered with high confidence.")*

