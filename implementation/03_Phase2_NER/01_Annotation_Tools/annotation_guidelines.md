# NER Annotation Guidelines
# CSE499: EHR-Based Pre-Consultation Medical Documentation System

## Overview

This document defines the annotation guidelines for Medical Named Entity Recognition (NER) in Bengali medical text.

---

## Entity Types

### 1. SYMPTOM (লক্ষণ)
Any physical or mental condition the patient describes.

**Examples:**
- জ্বর (fever)
- কাশি (cough)
- মাথা ঘুরা (dizziness)
- বুকে ব্যথা (chest pain)
- পেটে ব্যথা (stomach pain)

**Annotation:**
```
জ্বর    B-SYMPTOM
আছে    I-SYMPTOM
```

### 2. DISEASE (রোগ)
Any diagnosed medical condition or disease.

**Examples:**
- ডায়াবেটিস (diabetes)
- উচ্চ রক্তচাপ (high blood pressure)
- হাঁপানি (asthma)
- কোভিড (COVID)

**Annotation:**
```
ডায়াবেটিস    B-DISEASE
আছে         I-DISEASE
```

### 3. MEDICATION (ওষুধ)
Any medicine, drug, or pharmaceutical product mentioned.

**Examples:**
- প্যারাসিটামল (paracetamol)
- ইনসুলিন (insulin)
- অ্যাজিথ্রোমাইসিন (azithromycin)
- মেটফর্মিন (metformin)

**Annotation:**
```
প্যারা    B-MEDICATION
সিটা     I-MEDICATION
```

### 4. DURATION (সময়কাল)
Time period or duration of symptoms/illness.

**Examples:**
- ৩ দিন (3 days)
- এক সপ্তাহ (one week)
- গতকাল থেকে (since yesterday)
- দুই মাস (two months)

**Annotation:**
```
গতকাল    B-DURATION
থেকে     I-DURATION
```

### 5. ALLERGY (অ্যালার্জি)
Any allergic reaction or allergy.

**Examples:**
- পেনিসিলিনে অ্যালার্জি (allergy to penicillin)
- ড্রাগ অ্যালার্জি (drug allergy)

**Annotation:**
```
পেনিসিলিনে    B-ALLERGY
অ্যালার্জি   I-ALLERGY
```

### 6. BODY_PART (শরীরের অংশ)
Body parts mentioned in context of symptoms.

**Examples:**
- মাথা (head)
- বুক (chest)
- পেট (stomach)
- গলা (throat)

**Annotation:**
```
মাথায়    B-BODY_PART
ব্যথা     O
```

### 7. TREATMENT (চিকিৎসা)
Medical treatments, procedures, or therapies.

**Examples:**
- অপারেশন (surgery)
- থেরাপি (therapy)
- ইনজেকশন (injection)

**Annotation:**
```
অপারেশন    B-TREATMENT
করতে      I-TREATMENT
```

### 8. DOSAGE (মাত্রা)
Dosage information for medications.

**Examples:**
- দুই টি (two tablets)
- দিনে তিন বার (three times a day)
- সকালে একটা (one in the morning)

**Annotation:**
```
দুই      B-DOSAGE
টি       I-DOSAGE
দিনে     O
তিন     B-DOSAGE
বার     I-DOSAGE
```

---

## BIO Tagging Scheme

### B- (Beginning)
The first token of an entity.

### I- (Inside)
Subsequent tokens of the same entity.

### O (Outside)
Tokens that are not part of any entity.

---

## Annotation Rules

### Rule 1: Single Token Entities
Single-token entities use B- tag only.
```
জ্বর    B-SYMPTOM
```

### Rule 2: Multi-Token Entities
First token gets B-, subsequent tokens get I-.
```
মাথা    B-SYMPTOM
ঘুরা    I-SYMPTOM
```

### Rule 3: Adjacent Entities
Two entities of the same type cannot be adjacent.
```
জ্বর    B-SYMPTOM      কাশি    B-SYMPTOM  (Correct - separate entities)
```

### Rule 4: Code-Mixed Text
English words in Bengali text are annotated normally.
```
ট্যাবলেট    B-MEDICATION
```

### Rule 5: Context Matters
Body parts without symptom context are not annotated.
```
মাথা    B-BODY_PART    (when describing headache location)
মাথা    O              (when just mentioned casually)
```

---

## Examples

### Example 1: Complete Sentence
**Input:**
```
আমার গতকাল থেকে মাথা ঘুরছে এবং জ্বর আছে। আমার ডায়াবেটিস আছে এবং ইনসুলিন খাই।
```

**Annotation:**
```
আমার    O
গতকাল   B-DURATION
থেকে    I-DURATION
মাথা     B-SYMPTOM
ঘুরছে   I-SYMPTOM
এবং     O
জ্বর     B-SYMPTOM
আছে     I-SYMPTOM
।       O
আমার    O
ডায়াবেটিস    B-DISEASE
আছে     I-DISEASE
এবং     O
ইনসুলিন    B-MEDICATION
খাই     O
।       O
```

### Example 2: With Medications
**Input:**
```
আমি প্যারাসিটামল দুই টি করে দিনে তিন বার খাই।
```

**Annotation:**
```
আমি     O
প্যারা   B-MEDICATION
সিটা     I-MEDICATION
দুই     B-DOSAGE
টি      I-DOSAGE
করে     O
দিনে    O
তিন     B-DOSAGE
বার     I-DOSAGE
খাই     O
।       O
```

---

## Quality Guidelines

1. **Consistency**: Be consistent with similar cases
2. **Completeness**: Label all entities
3. **Accuracy**: Use correct entity type
4. **Boundaries**: Mark entity boundaries correctly

---

## File Format

Save annotations in BIO format with tab separation:
```
TOKEN   LABEL
```

Save as .txt file with same name as transcription file.

---

## Contact

For questions about annotations, contact the project team.
