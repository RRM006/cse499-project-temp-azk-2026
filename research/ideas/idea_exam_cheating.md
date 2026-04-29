# AI-Powered Exam Integrity Monitoring System

## Problem Statement

Academic examinations rely heavily on human invigilators to maintain integrity. However, manual monitoring is inherently limited due to human fatigue, restricted field of view, and unfavorable invigilator-to-student ratios, especially in large examination halls. These constraints make it difficult to detect subtle and covert cheating behaviors, such as students using smartphones hidden under desks, inside pockets, or within bags.

Existing technical solutions—such as signal jammers, RF detectors, or post-exam video reviews—are either illegal, unreliable, intrusive, or impractical at scale. Pure object-detection-based approaches also fail in real-world scenarios due to occlusion, lighting variation, and the concealment of devices.

As a result, institutions lack a scalable, proactive, and privacy-preserving system capable of assisting invigilators in detecting unauthorized electronic device usage during exams without unfairly accusing honest students.

---

## Objective

The objective of this project is to design and implement a **real-time, AI-powered exam monitoring system** that detects suspicious cheating behavior by analyzing live CCTV video streams using computer vision and temporal behavior modeling.

Specifically, the system aims to:
- Detect **behavioral sequences** associated with smartphone-based cheating rather than relying solely on object detection.
- Operate in **real-time on edge devices**, ensuring low latency and privacy preservation.
- Minimize false positives by prioritizing **high precision over recall**.
- Provide **actionable alerts** to human invigilators through an intuitive dashboard, enabling informed human judgment rather than automated accusations.
- Avoid facial recognition, identity tracking, or cloud-based data transmission to comply with ethical and privacy standards.

---

## Tools & Techniques

### Computer Vision & AI
- **Pose Estimation:** MediaPipe BlazePose for real-time body and hand landmark detection.
- **Object Detection:** YOLOv8n for lightweight detection of smartphones when visible.
- **Behavior Modeling:** Rule-based Finite State Machine (FSM) to model cheating sequences such as:
  - Hand movement toward pocket/bag or desk
  - Sustained downward head pose (>2 seconds)
  - Optional confirmation of phone presence

### System & Deployment
- **Edge Computing:** Raspberry Pi 4 with Google Coral USB Accelerator for on-device inference.
- **Video Processing:** OpenCV for frame handling and preprocessing.
- **Dashboard:** Streamlit-based interface displaying anonymized alerts and short video clips.

### Data & Evaluation
- **Dataset:** Custom-recorded classroom scenarios with consenting volunteers, including both cheating and non-cheating behaviors.
- **Metrics:** Precision, recall, false positive rate, confusion matrix analysis.
- **Validation:** Controlled mock exam deployment with human invigilator feedback.

---

## Why This Is Research-Worthy

This project addresses a **real-world, high-impact problem** that cannot be solved by a single off-the-shelf AI model. Its research significance lies in several key aspects:

- **Behavior-Centric Innovation:** Models cheating as a *temporal behavior sequence* rather than a static object presence, which is a more robust and underexplored approach in exam monitoring.
- **Engineering Trade-offs:** Requires deliberate design decisions balancing precision vs. recall, privacy vs. monitoring effectiveness, and performance vs. hardware constraints.
- **Ethical AI by Design:** Integrates privacy engineering principles, avoids biometric identification, and ensures human oversight in decision-making.
- **System Integration Complexity:** Combines real-time computer vision, embedded systems, temporal logic, and human-computer interaction into a cohesive pipeline.
- **Practical Validation:** Evaluated under realistic conditions (variable lighting, occlusion, natural student behavior), not just curated datasets.

Overall, this project goes beyond a trivial detection task and demonstrates the full engineering lifecycle—from problem formulation and ethical constraints to system deployment and rigorous evaluation—making it a strong and valid Final Year Design Project (FYDP).

