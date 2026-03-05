\# Paper Reading for EHR-Based Pre-Consultation Medical Documentation System

\#\# 1\. Basic Information

\- \*\*Title:\*\* Integrating automatic speech recognition into remote healthcare interpreting: A pilot study of its impact on interpreting quality  
\- \*\*Authors:\*\* Shiyi Tan, Constantin Orasan, Sabine Braun  
\- \*\*Affiliation/Conference/Journal:\*\* University of Surrey, UK / TC46-2024 Proceedings  
\- \*\*Year:\*\* 2024  
\- \*\*Venue:\*\* Translation and interpreting conference  
\- \*\*Paper Link:\*\* https://arxiv.org/pdf/2502.03381

\---

\#\# 2\. Research Context

\*\*Domain:\*\* ☒ Speech Recognition (ASR) ☐ Accent Recognition ☒ Medical NLP   
☐ Bangla/Low-Resource Language ☐ Information Extraction ☒ EHR Systems 

\*\*Specific Sub-domain:\*\* ASR in healthcare settings, ASR for medical dialogue, ASR output presentation formats

\*\*Relevance to Our Project (1-5 scale):\*\*  
\- ASR component: ⭐⭐⭐⭐☆ (4/5)  
\- Medical NLP: ⭐⭐⭐☆☆ (3/5)  
\- Bangla/multilingual: ⭐☆☆☆☆ (1/5)  
\- Accent handling: ⭐☆☆☆☆ (1/5)  
\- EHR integration: ⭐⭐☆☆☆ (2/5)

\*\*Most relevant for: (check all that apply)\*\*  
☒ Understanding ASR architecture    
☒ Fine-tuning strategies    
☐ Medical entity extraction    
☐ Accent adaptation techniques    
☒ Dataset creation methods    
☒ Evaluation metrics    
☐ System integration  

\---

\#\# 3\. Problem Definition

\#\#\# A. What problem does this paper solve?  
This paper investigates whether automatic speech recognition (ASR) technology helps or hinders interpreters when they work in remote healthcare settings. The researchers want to know if showing ASR-generated text (transcripts or summaries) to interpreters improves the quality of their interpreting, especially for medical conversations between doctors and patients.

\#\#\# B. How does this relate to OUR project?  
\- \*\*Direct application:\*\* The paper studies ASR in medical conversations, which is exactly what we need—patients speaking about their health conditions. Their setup (medical dialogue between doctor and patient) is similar to our pre-consultation scenario.  
\- \*\*Inspired approach:\*\* They tested \*\*different types of ASR output\*\* (full transcript vs. only key terms vs. ChatGPT summary) to see what helps most. We could test different ASR outputs for our Bangla patients.  
\- \*\*Technique we can borrow:\*\* Their \*\*error analysis framework (NTR model)\*\* for evaluating how well the ASR output preserves medical meaning could help us evaluate our system's clinical accuracy.

\#\#\# C. What is their solution approach?  
They created a custom interface showing different ASR outputs to interpreters during medical video calls:  
\- \*\*Condition 1:\*\* No ASR (baseline)  
\- \*\*Condition 2:\*\* Only numbers and medical terms  
\- \*\*Condition 3:\*\* Full transcript of the conversation  
\- \*\*Condition 4:\*\* ChatGPT-generated summary of the conversation

They tested these with 4 trainee interpreters doing English-to-Chinese medical interpreting and measured interpreting quality.

\---

\#\# 4\. METHODOLOGY ANALYSIS

\*\*Model/Approach Used:\*\*  
\- \*\*ASR Model:\*\* Microsoft Azure Speech Service API (commercial, not open-source)  
\- \*\*NLP Model:\*\* ChatGPT (GPT model) for summarization  
\- \*\*Architecture details:\*\* Cloud-based API, no custom fine-tuning  
\- \*\*Key innovation:\*\* Comparing different ASR output formats (full transcript vs. summary vs. just terms) to see what helps interpreters most

\#\#\# Architecture:  
\`\`\`  
Medical consultation video → Microsoft Azure ASR → ASR transcript → (Optional) ChatGPT summary → Display to interpreter → Interpreter produces translation  
\`\`\`

\#\#\# Pipeline/Workflow:  
\`\`\`  
Doctor-patient video → \[ASR transcription\] → \[Optional ChatGPT summarization\] → Text shown on screen → Interpreter reads \+ listens → Final interpretation  
\`\`\`

\#\#\# Training Strategy:  
\- \*\*Pre-training:\*\* No (they used off-the-shelf ASR)  
\- \*\*Fine-tuning:\*\* No (they used Microsoft Azure ASR without customization)  
\- \*\*Transfer learning:\*\* Not applicable

\#\#\# Specific Techniques for OUR Use Case:

\#\#\#\# 1\. Speech Recognition Approach

\*\*For ASR Architecture:\*\*  
\- They used \*\*Microsoft Azure Speech Service API\*\* (cloud-based, commercial)  
\- \*\*How they handle accents/dialects:\*\* Not specified—likely Azure's built-in multi-accent capabilities  
\- \*\*Data augmentation techniques:\*\* None  
\- \*\*Fine-tuning approach:\*\* None—they used generic medical ASR without domain customization

\*\*Acoustic Model Details:\*\* Not provided (proprietary)  
\*\*Language Model:\*\* Not provided (proprietary)  
\*\*Decoder:\*\* Not provided

\#\#\#\# 2\. Accent/Dialect Handling  
\- \*\*Not relevant\*\*—their data is in English, not Bangla  
\- They don't address low-resource languages  
\- No code-mixing handling (their data is English only)

\#\#\#\# 3\. Medical/Domain-Specific Processing

\*\*Medical terminology handling:\*\*   
\- They used Azure's generic medical vocabulary (no custom terminology lists)  
\- ASR errors occurred with medical terms (e.g., "corticosteroids" misrecognized)

\*\*Information extraction methods:\*\*   
\- ☐ Rule-based  
\- ☐ CRF/HMM  
\- ☐ Deep learning  
\- ☒ LLM-based (ChatGPT for summarization)

\*\*Medical entities extracted in summaries:\*\*  
\- Symptoms  
\- Medications (names, dosages)  
\- Test results (numbers, units)  
\- Diagnoses

\*\*Structuring approach for EHR:\*\*  
\- ChatGPT summaries were formatted as \*\*bullet points\*\*  
\- Summaries kept medical terms and numbers but shortened the dialogue

\---

\#\# 5\. Data & Experimental Setup

\- \*\*Dataset name:\*\* Custom-created medical consultation scripts (not public)  
\- \*\*Dataset size:\*\* 4 scripts (approx. 750 words each, 5-7 minutes each)  
\- \*\*Language(s):\*\* English (doctor) and Chinese (patient) for interpreting; ASR was on English  
\- \*\*Domain:\*\* ☒ Medical ☐ General ☐ Other: Healthcare (nephrology/renal disease)  
\- \*\*Accent/Dialect coverage:\*\* Not applicable (scripted, read speech)  
\- \*\*Can I access this data?\*\* ☐ Yes ☒ No   
\- \*\*Link:\*\* None

\*\*Data Collection Method:\*\*  
\- \*\*Clinical recordings?\*\* No—they adapted scripts from real hospital consultations  
\- \*\*Simulated?\*\* Yes—actors played doctor and patient, recordings made in controlled setting  
\- \*\*Crowdsourced?\*\* No  
\- \*\*Scraped?\*\* No

\*\*Annotation process:\*\*  
\- Scripts were manually created based on real medical consultations  
\- Difficulty was controlled (word count, duration, reading ease score)  
\- ASR word error rate (WER) was calculated for each script (14.62% to 19.80%)

\*\*Quality control:\*\*  
\- Flesch Reading Ease score used to ensure consistent difficulty (scores 61-70)  
\- Speed controlled (124-141 words per minute)

\---

\#\# 6\. Evaluation Metrics

\#\#\# 1\. For ASR:  
\- \*\*Word Error Rate (WER):\*\* 14.62% to 19.80% across four scripts  
\- \*\*Character Error Rate (CER):\*\* Not reported  
\- \*\*Other:\*\* They measured WER on English utterances only

\#\#\# 2\. For NLP/ NER:  
\- \*\*Not applicable\*\*—they didn't do NER, only summarization  
\- Summaries were not formally evaluated (just shown to interpreters)

\#\#\# 3\. For EHR/ Clinical:  
\- \*\*Interpreting quality\*\* was measured using the \*\*NTR model\*\* (accuracy rate)  
\- Error types categorized: omission, addition, substitution, style errors  
\- Accuracy scores: 96-99% range across conditions

\*\*Other Metrics:\*\*  
\- \*\*NASA Task Load Index (TLX)\*\*—collected but not analyzed in this paper  
\- \*\*Eye-tracking data\*\*—collected but not analyzed in this paper  
\- \*\*Retrospective reports\*\*—participants described their experience

\#\#\# Experimental Settings:  
\- \*\*Train/Val/Test split:\*\* Not applicable (no training done)  
\- \*\*Hardware:\*\* Not specified (used EyeLink 1000 Plus eye tracker)  
\- \*\*Framework:\*\* Microsoft Azure Speech API, ChatGPT  
\- \*\*Training time:\*\* Not applicable

\---

\#\# 6\. Results & Findings

\*\*Key findings:\*\*  
1\. \*\*Full ASR transcripts\*\* and \*\*ChatGPT summaries\*\* significantly improved interpreting quality compared to no ASR  
2\. \*\*Partial ASR (only numbers \+ terms)\*\* did NOT significantly improve quality  
3\. No significant difference between full transcripts and ChatGPT summaries—both helped equally  
4\. Full transcripts reduced \*\*omission errors\*\* the most (74% reduction)  
5\. But full transcripts also increased \*\*style errors\*\* (disfluency, pauses, fillers)

\*\*Main Results:\*\*  
\- \*\*Best performance:\*\* Full ASR transcript (98.80% accuracy)  
\- \*\*Comparison with baselines:\*\*   
  \- No ASR: 96.60%  
  \- Partial ASR: 97.12%  
  \- Full ASR: 98.80% ⬆️  
  \- ChatGPT summary: 98.72% ⬆️  
\- \*\*Improvement over previous work:\*\* Consistent with studies showing ASR helps with numbers, but extends to overall quality

\*\*Performance on different accents:\*\* Not applicable

\*\*Limitations mentioned:\*\*  
1\. Very small sample size (n=4 trainees) → results are preliminary  
2\. Only evaluated English-to-Chinese interpreting, not bidirectional  
3\. No note-taking allowed (for eye-tracking) → less realistic  
4\. Simulated consultations (no real patients/doctors)  
5\. Custom interface unfamiliar to participants  
6\. Low statistical power (0.141) despite large effect size

\*\*What worked well?\*\*  
\- Full transcripts helped interpreters catch everything  
\- ChatGPT summaries preserved key medical information while being shorter  
\- Both formats helped reduce omissions

\*\*What didn't work?\*\*  
\- Partial ASR (just numbers \+ terms) didn't help overall quality  
\- Some interpreters became too dependent on ASR and made errors when ASR was wrong  
\- Style/fluency suffered with ASR support (more "um"s and pauses)

\*\*Error Analysis:\*\*  
\- \*\*Omission errors:\*\* Drastically reduced with full transcripts  
\- \*\*Substitution errors:\*\* Most reduced with ChatGPT summaries  
\- \*\*Style errors:\*\* Increased with full transcripts and summaries  
\- \*\*Common error:\*\* Interpreters copied ASR mistakes (e.g., "60 minutes" instead of "60 mg")

\---

\#\# 7\. Implementation Notes

\*\*Tools/Libraries used:\*\*  
\- Microsoft Azure Speech Service API (ASR)  
\- ChatGPT (summarization)  
\- EyeLink 1000 Plus (eye tracker)  
\- SPSS Statistics (statistical analysis)  
\- Qualtrics (questionnaires)

\*\*Model parameters/hyperparameters:\*\*  
\- Not provided (used commercial APIs)  
\- ChatGPT prompt: \*"There is the output of an ASR system... Shorten the output to about half length making sure important information is kept... Present using bullet points"\*

\*\*Training details:\*\*  
\- No training—used pre-trained ASR and ChatGPT

\*\*Computational requirements:\*\*  
\- Cloud-based APIs—no local compute needed

\*\*Code Available:\*\* ☐ Yes ☐ No ☒ Partial (interface designed by research team but not shared)  
\*\*Link:\*\* None

\*\*Pre-trained Models Available:\*\* ☒ Yes (Azure ASR, ChatGPT) ☐ No  
\*\*Link:\*\* https://azure.microsoft.com/en-us/products/ai-services/speech-to-text

\*\*Can We Reproduce:\*\* ☐ Fully ☒ Partially ☐ No  
\- We can reproduce the idea (test different ASR outputs) but not the exact setup

\*\*Constraints:\*\*  
\- \*\*Compute:\*\* Low—APIs handle everything  
\- \*\*Data:\*\* Need medical dialogue data  
\- \*\*Time:\*\* Low—no training required

\*\*Computational Requirements:\*\*  
\- \*\*Can we afford this compute?\*\* ☒ Yes ☐ No (Azure and ChatGPT have costs, but small-scale testing is affordable)  
\- \*\*GPU memory needed:\*\* None (cloud-based)  
\- \*\*Training time:\*\* None

\---

\#\# 8\. Relevance to Our Project

\*\*Can I use their approach?\*\* ☐ Yes ☒ Partially ☐ No

\*\*What resources do I need to implement this?\*\*  
1\. Medical dialogue data (simulated or real) in Bangla  
2\. ASR system (we already plan to use Whisper)  
3\. LLM for summarization (optional—could use GPT or open-source like Llama)  
4\. Evaluation framework (NTR model or similar for clinical accuracy)  
5\. Interface to show ASR output (simple web app)

\*\*What is NOT applicable to us?\*\*  
\- Interpreting aspect—we don't have a human interpreter; we have an automated pipeline  
\- English language—our focus is Bangla  
\- Remote interpreting setup—our focus is pre-consultation recording, not live video  
\- Eye-tracking—not needed for MVP

\---

\#\# 9\. QUESTIONS & FOLLOW-UPS

\*\*Confusing parts:\*\*  
1\. Why did partial ASR (just numbers \+ terms) not help, when previous studies said it did?  
   \- Answer: Previous studies only measured number accuracy; this study measured overall quality  
2\. How did they calculate the 96-99% accuracy scores?   
   \- Answer: Using NTR formula: (N \- T \- R \+ EE)/N, but they excluded R (recognition errors) since interpreters didn't see subtitles

\*\*Unclear concepts I need to research:\*\*  
1\. NTR model—how to adapt it for evaluating our ASR+NLP pipeline  
2\. Flesch Reading Ease score—for controlling text difficulty  
3\. NASA-TLX—workload measurement (maybe for user testing with doctors)

\*\*Questions for supervisor AZK:\*\*  
1\. Should we test different ASR output formats like they did (full transcript vs. summary vs. just entities)?  
2\. Is the NTR model useful for evaluating our system's clinical accuracy?  
3\. Can we use ChatGPT for summarization, or should we stick to open-source models?

\*\*Discussion points with the team:\*\*  
1\. Should our system show the full transcript to doctors, or just the structured EHR?  
2\. Do we need to handle both options and let doctors choose?  
3\. How can we measure if our system reduces doctors' workload (like NASA-TLX)?

\---

\#\# 10\. Project Integration Plan

\*\*Which phase of OUR project uses this?\*\*  
☒ ASR baseline setup    
☒ Fine-tuning ASR    
☐ Medical NER    
☐ Accent adaptation    
☒ Data collection strategy    
☒ System integration    
☒ Evaluation  

\*\*Specific action items derived from this paper:\*\*  
1\. \*\*Design multiple output formats for testing\*\*—We should create at least 2 versions of our system: (a) full transcript only, (b) structured EHR only, and test which doctors prefer  
2\. \*\*Collect simulated medical dialogues\*\*—Like this paper, we can create scripts based on real consultations and record volunteers role-playing as patients  
3\. \*\*Calculate WER on our Bangla data\*\*—We need to measure ASR accuracy before moving to NER  
4\. \*\*Track error types\*\*—Omission, substitution, addition—to see where our system fails clinically  
5\. \*\*Include numbers and units in evaluation\*\*—Medical errors often involve dosages, dates, measurements—we must track these separately

\---

\#\# 11\. Keywords & Concepts

\*\*Project-Relevant Keywords:\*\*  
1\. ASR in healthcare  
2\. Medical dialogue transcription  
3\. ASR output presentation formats  
4\. Clinical information preservation  
5\. Error analysis in medical transcription  
6\. Simulated medical data collection

\*\*Technical Terms to Learn:\*\*  
1\. \*\*NTR Model\*\* \- Framework for evaluating accuracy in interpreting/translation by tracking omissions, substitutions, additions  
2\. \*\*Flesch Reading Ease\*\* \- Metric for text difficulty (we could use for controlling our script difficulty)  
3\. \*\*Word Error Rate (WER)\*\* \- Standard ASR accuracy metric  
4\. \*\*NASA-TLX\*\* \- Workload assessment tool (could use for doctor satisfaction studies)  
5\. \*\*Within-subjects design\*\* \- Each participant experiences all conditions (efficient for small samples)
