#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EHR Pipeline - Complete Integration
Combines Phase 1 (ASR), Phase 2 (NER), and Phase 3 (EHR)
"""

import os
import json
import torch
import librosa
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass


class EHRPipeline:
    """
    Complete EHR generation pipeline.
    
    Pipeline stages:
    1. ASR: Speech → Text
    2. NER: Text → Entities
    3. EHR: Entities → Structured EHR
    """
    
    def __init__(
        self,
        asr_model_path: str = None,
        asr_model_type: str = "whisper",
        ner_model_path: str = None,
        ner_model_name: str = "csebuetnlp/banglabert",
        device: str = None
    ):
        """
        Initialize EHR Pipeline.
        
        Args:
            asr_model_path: Path to ASR model
            asr_model_type: Type of ASR model (whisper, wav2vec2)
            ner_model_path: Path to NER model
            ner_model_name: Base model name for NER
            device: Device to use (cuda/cpu)
        """
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.asr_model_path = asr_model_path
        self.asr_model_type = asr_model_type
        self.ner_model_path = ner_model_path
        self.ner_model_name = ner_model_name
        
        # Components
        self.asr_processor = None
        self.asr_model = None
        self.ner_tokenizer = None
        self.ner_model = None
        
        # Load models if paths provided
        if asr_model_path:
            self._load_asr_model()
        
        if ner_model_path:
            self._load_ner_model()
    
    def _load_asr_model(self):
        """Load ASR model."""
        print(f"Loading ASR model ({self.asr_model_type})...")
        
        if self.asr_model_type == "whisper":
            from transformers import WhisperProcessor, WhisperForConditionalGeneration
            
            self.asr_processor = WhisperProcessor.from_pretrained(
                self.asr_model_path
            )
            self.asr_model = WhisperForConditionalGeneration.from_pretrained(
                self.asr_model_path
            )
        
        elif self.asr_model_type == "wav2vec2":
            from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
            
            self.asr_processor = Wav2Vec2Processor.from_pretrained(
                self.asr_model_path
            )
            self.asr_model = Wav2Vec2ForCTC.from_pretrained(
                self.asr_model_path
            )
        
        self.asr_model.to(self.device)
        self.asr_model.eval()
        print("✓ ASR model loaded")
    
    def _load_ner_model(self):
        """Load NER model."""
        print("Loading NER model...")
        
        from transformers import AutoTokenizer, AutoModelForTokenClassification
        
        self.ner_tokenizer = AutoTokenizer.from_pretrained(self.ner_model_name)
        self.ner_model = AutoModelForTokenClassification.from_pretrained(
            self.ner_model_path
        )
        
        self.ner_model.to(self.device)
        self.ner_model.eval()
        print("✓ NER model loaded")
    
    def transcribe(self, audio_path: str) -> str:
        """
        Phase 1: Convert speech to text.
        
        Args:
            audio_path: Path to audio file
        
        Returns:
            Transcription text
        """
        # Load audio
        audio, sr = librosa.load(audio_path, sr=16000)
        
        if self.asr_model_type == "whisper":
            # Process audio
            input_features = self.asr_processor(
                audio,
                sampling_rate=16000,
                return_tensors="pt"
            ).input_features.to(self.device)
            
            # Generate
            with torch.no_grad():
                predicted_ids = self.asr_model.generate(input_features)
            
            # Decode
            transcription = self.asr_processor.batch_decode(
                predicted_ids,
                skip_special_tokens=True
            )[0]
        
        elif self.asr_model_type == "wav2vec2":
            # Process audio
            input_values = self.asr_processor(
                audio,
                sampling_rate=16000,
                return_tensors="pt"
            ).input_values.to(self.device)
            
            # Generate
            with torch.no_grad():
                logits = self.asr_model(input_values).logits
            
            # Decode
            predicted_ids = torch.argmax(logits, dim=-1)
            transcription = self.asr_processor.batch_decode(
                predicted_ids
            )[0]
        
        return transcription
    
    def extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """
        Phase 2: Extract medical entities from text.
        
        Args:
            text: Input text
        
        Returns:
            List of extracted entities
        """
        # Tokenize
        tokens = text.split()
        inputs = self.ner_tokenizer(
            tokens,
            is_split_into_words=True,
            return_tensors="pt",
            padding=True,
            truncation=True
        ).to(self.device)
        
        # Predict
        with torch.no_grad():
            outputs = self.ner_model(**inputs)
            predictions = torch.argmax(outputs.logits, dim=-1)[0].tolist()
        
        # Map predictions to labels
        word_ids = inputs.word_ids()
        
        # Label mapping (simplified)
        label_ids = [
            "O",
            "B-SYMPTOM", "I-SYMPTOM",
            "B-DISEASE", "I-DISEASE",
            "B-MEDICATION", "I-MEDICATION",
            "B-DURATION", "I-DURATION",
            "B-ALLERGY", "I-ALLERGY",
            "B-BODY_PART", "I-BODY_PART",
            "B-TREATMENT", "I-TREATMENT",
            "B-DOSAGE", "I-DOSAGE"
        ]
        
        # Extract entities
        entities = []
        current_entity = None
        current_type = None
        current_start = None
        
        for i, word_id in enumerate(word_ids):
            if word_id is None:
                continue
            
            pred_id = predictions[i]
            if pred_id < len(label_ids):
                label = label_ids[pred_id]
            else:
                label = "O"
            
            if label.startswith("B-"):
                # Save previous
                if current_entity is not None:
                    entities.append({
                        "text": current_entity,
                        "type": current_type,
                        "start": current_start,
                        "end": i
                    })
                
                # New entity
                current_entity = tokens[word_id] if word_id < len(tokens) else ""
                current_type = label[2:]
                current_start = i
            
            elif label.startswith("I-"):
                entity_type = label[2:]
                if entity_type == current_type and current_entity is not None:
                    current_entity += " " + (tokens[word_id] if word_id < len(tokens) else "")
            
            else:
                # Save previous
                if current_entity is not None:
                    entities.append({
                        "text": current_entity,
                        "type": current_type,
                        "start": current_start,
                        "end": i
                    })
                current_entity = None
                current_type = None
        
        # Save last entity
        if current_entity is not None:
            entities.append({
                "text": current_entity,
                "type": current_type,
                "start": current_start,
                "end": len(tokens)
            })
        
        return entities
    
    def generate_ehr(
        self,
        entities: List[Dict],
        transcription: str = "",
        patient_id: str = None,
        dialect: str = ""
    ) -> Dict:
        """
        Phase 3: Generate EHR from entities.
        
        Args:
            entities: Extracted entities
            transcription: Original transcription
            patient_id: Patient ID
            dialect: Input dialect
        
        Returns:
            EHR dictionary
        """
        # Import EHR generator
        from ehr_generator import EHRGenerator
        
        generator = EHRGenerator()
        ehr = generator.generate(
            entities=entities,
            transcription=transcription,
            patient_id=patient_id,
            dialect=dialect
        )
        
        return ehr
    
    def process(
        self,
        audio_path: str,
        patient_id: str = None,
        dialect: str = ""
    ) -> Dict[str, Any]:
        """
        Process audio file through complete pipeline.
        
        Args:
            audio_path: Path to audio file
            patient_id: Patient ID (optional)
            dialect: Input dialect (optional)
        
        Returns:
            Dictionary containing:
            - transcription: Phase 1 output
            - entities: Phase 2 output
            - ehr: Phase 3 output
            - ehr_text: Human-readable EHR
        """
        print(f"\n{'='*60}")
        print("Processing: {audio_path}")
        print(f"{'='*60}\n")
        
        # Phase 1: ASR
        print("[Phase 1/3] Converting speech to text...")
        transcription = self.transcribe(audio_path)
        print(f"  → Transcribed: {transcription[:100]}...")
        
        # Phase 2: NER
        print("\n[Phase 2/3] Extracting medical entities...")
        entities = self.extract_entities(transcription)
        print(f"  → Found {len(entities)} entities")
        
        for entity in entities[:5]:  # Show first 5
            print(f"    - {entity['text']} ({entity['type']})")
        
        # Phase 3: EHR
        print("\n[Phase 3/3] Generating EHR...")
        ehr = self.generate_ehr(
            entities=entities,
            transcription=transcription,
            patient_id=patient_id,
            dialect=dialect
        )
        print(f"  → Patient ID: {ehr['patient_id']}")
        
        # Generate text version
        from ehr_generator import EHRGenerator
        generator = EHRGenerator()
        ehr_text = generator.to_text(ehr)
        
        print(f"\n{'='*60}")
        print("Processing complete!")
        print(f"{'='*60}\n")
        
        return {
            "transcription": transcription,
            "entities": entities,
            "ehr": ehr,
            "ehr_text": ehr_text
        }
    
    def save_output(
        self,
        result: Dict,
        output_dir: str,
        base_name: str
    ) -> None:
        """
        Save pipeline output to files.
        
        Args:
            result: Pipeline result dictionary
            output_dir: Output directory
            base_name: Base filename
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # Save transcription
        with open(
            os.path.join(output_dir, f"{base_name}_transcription.txt"),
            'w', encoding='utf-8'
        ) as f:
            f.write(result["transcription"])
        
        # Save entities
        with open(
            os.path.join(output_dir, f"{base_name}_entities.json"),
            'w', encoding='utf-8'
        ) as f:
            json.dump(result["entities"], f, ensure_ascii=False, indent=2)
        
        # Save EHR JSON
        with open(
            os.path.join(output_dir, f"{base_name}_ehr.json"),
            'w', encoding='utf-8'
        ) as f:
            json.dump(result["ehr"], f, ensure_ascii=False, indent=2)
        
        # Save EHR text
        with open(
            os.path.join(output_dir, f"{base_name}_ehr.txt"),
            'w', encoding='utf-8'
        ) as f:
            f.write(result["ehr_text"])
        
        print(f"Output saved to {output_dir}/{base_name}_*")


def create_demo_pipeline() -> EHRPipeline:
    """
    Create a demo pipeline with sample configuration.
    
    Returns:
        Configured EHRPipeline
    """
    # This would load actual models in practice
    pipeline = EHRPipeline(
        asr_model_path="openai/whisper-small",
        asr_model_type="whisper",
        ner_model_path=None,  # Would be set to trained model
        ner_model_name="csebuetnlp/banglabert"
    )
    
    return pipeline


if __name__ == "__main__":
    # Example usage
    import argparse
    
    parser = argparse.ArgumentParser(description="EHR Pipeline")
    parser.add_argument("--audio", required=True, help="Audio file path")
    parser.add_argument("--asr-model", help="ASR model path")
    parser.add_argument("--ner-model", help="NER model path")
    parser.add_argument("--output", default="./output", help="Output directory")
    parser.add_argument("--patient-id", help="Patient ID")
    parser.add_argument("--dialect", default="dhaka", help="Input dialect")
    
    args = parser.parse_args()
    
    # Create pipeline
    pipeline = EHRPipeline(
        asr_model_path=args.asr_model,
        asr_model_type="whisper",
        ner_model_path=args.ner_model
    )
    
    # Process
    result = pipeline.process(
        args.audio,
        patient_id=args.patient_id,
        dialect=args.dialect
    )
    
    # Save
    base_name = os.path.splitext(os.path.basename(args.audio))[0]
    pipeline.save_output(result, args.output, base_name)
