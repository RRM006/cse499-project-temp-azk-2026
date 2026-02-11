[Download Presentation Slides (PPT)](../../pitch-doc-ppt/Inconsistency_Aware_Misinformation_Detection.pptx)

# Inconsistency-Aware Multimodal Misinformation Detection Using Vision-Language Models

## Problem Statement

The rapid growth of social media platforms has significantly accelerated the spread of misinformation. While early detection systems focused primarily on text-based fake news, modern misinformation frequently combines images and text to create more persuasive and manipulative narratives.

In many cases, the textual claim and the accompanying image are intentionally mismatched. For example, an old disaster image may be paired with a new political claim, or an unrelated photograph may be used to emotionally reinforce a false narrative.

These cross-modal inconsistencies make misinformation difficult to detect because:

- Text-only models ignore visual context.
- Image-only models ignore semantic claims.
- Existing multimodal systems mainly rely on feature fusion rather than explicitly modeling contradictions between modalities.

Current approaches often use early or late fusion of image and text embeddings (e.g., CLIP-based similarity). However, they do not explicitly quantify logical or semantic inconsistency between modalities. As a result, systems may fail when the image is authentic but contextually misleading.

Therefore, there is a need for a scalable, robust, and explainable AI system capable of detecting cross-modal inconsistencies instead of treating image and text as independent signals.



## Objective

The objective of this project is to design and implement an inconsistency-aware multimodal misinformation detection system that explicitly models semantic misalignment between textual claims and accompanying images.

Specifically, the system aims to:

- Detect misinformation by measuring cross-modal inconsistency.
- Compare performance against text-only and basic multimodal baselines.
- Improve robustness against context manipulation and adversarial pairing.
- Provide explainable reasoning signals indicating why content is flagged.
- Operate using pretrained foundation models without training from scratch.



## Methodology & Technical Approach

### 1. Image Encoder
- CLIP or BLIP for extracting semantic image embeddings.

### 2. Text Encoder
- BERT or a lightweight Large Language Model (LLM) for contextual text embeddings.

### 3. Cross-Modal Inconsistency Module
- Similarity scoring between image and text embeddings.
- Contrastive alignment analysis.
- Optional contradiction classifier trained on paired embeddings.

### 4. Classification Layer
A Multi-Layer Perceptron (MLP) to classify content into:
- Real
- Misleading
- Fake

### 5. Explainability Component (Optional)
- Attention visualization
- Highlighting contradictory keywords
- Similarity heatmap output



## Tools & Implementation

- Framework: PyTorch  
- Libraries: HuggingFace Transformers, OpenCLIP, OpenCV  
- Training Strategy: Fine-tuning pretrained encoders with frozen base layers  
- Deployment: GPU-based training (Google Colab / University Lab GPU)  
- Evaluation: Offline experimental setup  



## Data & Evaluation

### Datasets

The system will be evaluated using recent multimodal misinformation datasets, such as:

- MiRAGeNews (EMNLP 2024)
- MMFakeBench (ICLR 2025)
- Multilingual & Multimodal Political Misinformation Dataset (2025)
- MultiBanFakeDetect (2024)

### Evaluation Metrics

- Accuracy
- Precision
- Recall
- F1-score
- Confusion matrix analysis
- Robustness testing with mismatched image-text pairs

### Baseline Comparisons

- Text-only BERT model
- Image-only CLIP classifier
- Basic multimodal fusion model



## Research Contribution

### 1. Inconsistency-Centric Innovation
Unlike traditional fusion-based approaches, this project explicitly models cross-modal contradiction and semantic misalignment, an underexplored direction in multimodal misinformation detection.

### 2. Robustness Evaluation
The system evaluates adversarial pairing scenarios (e.g., real image + false claim), reflecting real-world manipulation tactics.

### 3. Explainable AI Integration
Instead of producing black-box predictions, the model provides interpretable reasoning signals to assist human moderators.

### 4. Engineering Trade-offs
The project balances:
- Model complexity vs. computational feasibility
- Accuracy vs. interpretability
- Fine-tuning depth vs. overfitting risk

### 5. Real-World Impact
Given the influence of misinformation on elections, public health, and social stability, developing robust multimodal detection systems carries high societal relevance.



## Overall Significance

This project goes beyond a standard classification task by integrating computer vision, natural language processing, cross-modal reasoning, robustness testing, and explainability into a unified framework.

It demonstrates the complete engineering and research lifecycle — from problem identification and literature gap analysis to system design, implementation, evaluation, and baseline comparison — making it a strong and valid Final Year Design Project (FYDP).
