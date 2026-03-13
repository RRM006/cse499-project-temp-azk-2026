#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EHR Generator for Phase 3
Converts extracted entities to structured EHR
"""

import json
import copy
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path


# Default EHR template
DEFAULT_TEMPLATE = {
    "patient_id": "AUTO_GENERATED",
    "consultation_date": "AUTO_GENERATED",
    "chief_complaint": {
        "symptoms": [],
        "duration": "",
        "severity": ""
    },
    "medical_history": {
        "diseases": [],
        "current_medications": [],
        "allergies": [],
        "past_surgeries": [],
        "family_history": []
    },
    "vital_signs": {
        "blood_pressure": None,
        "heart_rate": None,
        "temperature": None,
        "respiratory_rate": None,
        "oxygen_saturation": None
    },
    "assessment_and_plan": {
        "impression": "",
        "recommendations": [],
        "follow_up": "",
        "referrals": []
    },
    "raw_transcription": "",
    "extracted_entities": {
        "symptoms": [],
        "diseases": [],
        "medications": [],
        "durations": [],
        "allergies": [],
        "body_parts": [],
        "treatments": [],
        "dosages": []
    },
    "metadata": {
        "source": "voice_input",
        "dialect": "",
        "language": "bn"
    }
}


# Entity to field mapping
ENTITY_TO_EHR = {
    "SYMPTOM": {
        "field": "chief_complaint.symptoms",
        "type": "array",
        "item_template": {
            "name": "",
            "duration": "",
            "body_part": ""
        }
    },
    "DISEASE": {
        "field": "medical_history.diseases",
        "type": "array",
        "item_template": ""
    },
    "MEDICATION": {
        "field": "medical_history.current_medications",
        "type": "array",
        "item_template": {
            "name": "",
            "dosage": ""
        }
    },
    "DURATION": {
        "field": "chief_complaint.duration",
        "type": "single"
    },
    "ALLERGY": {
        "field": "medical_history.allergies",
        "type": "array",
        "item_template": ""
    },
    "TREATMENT": {
        "field": "assessment_and_plan.recommendations",
        "type": "array",
        "item_template": ""
    },
    "BODY_PART": {
        "field": "extracted_entities.body_parts",
        "type": "array",
        "item_template": ""
    },
    "DOSAGE": {
        "field": "extracted_entities.dosages",
        "type": "array",
        "item_template": ""
    }
}


class EHRGenerator:
    """Generate EHR from extracted entities."""
    
    def __init__(self, template: Dict = None):
        """
        Initialize EHR generator.
        
        Args:
            template: Custom template (optional)
        """
        self.template = template or copy.deepcopy(DEFAULT_TEMPLATE)
    
    def generate(
        self,
        entities: List[Dict[str, Any]],
        transcription: str = "",
        patient_id: str = None,
        dialect: str = ""
    ) -> Dict:
        """
        Generate EHR from entities.
        
        Args:
            entities: List of extracted entities
            transcription: Original transcription text
            patient_id: Patient ID (optional)
            dialect: Dialect of input (optional)
        
        Returns:
            EHR dictionary
        """
        # Create fresh copy of template
        ehr = copy.deepcopy(self.template)
        
        # Add metadata
        ehr["patient_id"] = patient_id or self._generate_patient_id()
        ehr["consultation_date"] = datetime.now().strftime("%Y-%m-%d")
        ehr["raw_transcription"] = transcription
        ehr["metadata"]["dialect"] = dialect
        
        # Process entities
        self._process_entities(ehr, entities)
        
        return ehr
    
    def _process_entities(self, ehr: Dict, entities: List[Dict]) -> None:
        """
        Process entities and map to EHR fields.
        
        Args:
            ehr: EHR dictionary (modified in place)
            entities: List of extracted entities
        """
        # Group entities by type
        entity_groups = {}
        for entity in entities:
            entity_type = entity.get("type", "")
            if entity_type not in entity_groups:
                entity_groups[entity_type] = []
            entity_groups[entity_type].append(entity)
        
        # Map to EHR fields
        for entity_type, mapping in ENTITY_TO_EHR.items():
            if entity_type not in entity_groups:
                continue
            
            entities_of_type = entity_groups[entity_type]
            field = mapping["field"]
            mapping_type = mapping["type"]
            
            if mapping_type == "array":
                # Handle array fields
                for entity in entities_of_type:
                    item = copy.deepcopy(mapping.get("item_template", ""))
                    
                    if isinstance(item, dict):
                        # Template dict - fill values
                        if "name" in item:
                            item["name"] = entity.get("text", "")
                        if "duration" in item:
                            # Try to find linked duration
                            item["duration"] = self._find_linked_value(
                                entities, entity, "DURATION"
                            )
                        if "dosage" in item:
                            item["dosage"] = self._find_linked_value(
                                entities, entity, "DOSAGE"
                            )
                        if "body_part" in item:
                            item["body_part"] = self._find_linked_value(
                                entities, entity, "BODY_PART"
                            )
                    else:
                        # Simple string
                        item = entity.get("text", "")
                    
                    # Add to EHR (avoid duplicates)
                    self._add_to_field(ehr, field, item)
            
            elif mapping_type == "single":
                # Handle single value fields
                if entities_of_type:
                    # Use first entity
                    value = entities_of_type[0].get("text", "")
                    self._set_field(ehr, field, value)
        
        # Also add all entities to extracted_entities
        self._populate_extracted_entities(ehr, entity_groups)
    
    def _find_linked_value(
        self,
        entities: List[Dict],
        source_entity: Dict,
        target_type: str
    ) -> str:
        """Find linked entity value (e.g., duration for a symptom)."""
        # Find entities of target type that appear near source entity
        source_idx = source_entity.get("start", 0)
        
        candidates = []
        for entity in entities:
            if entity.get("type") == target_type:
                entity_idx = entity.get("start", 0)
                distance = abs(entity_idx - source_idx)
                candidates.append((distance, entity.get("text", "")))
        
        if candidates:
            candidates.sort(key=lambda x: x[0])
            return candidates[0][1]
        
        return ""
    
    def _add_to_field(self, ehr: Dict, field: str, value: Any) -> None:
        """Add value to nested array field."""
        # Parse field path
        parts = field.split(".")
        
        # Navigate to parent
        current = ehr
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        
        # Get field name
        field_name = parts[-1]
        
        # Initialize if needed
        if field_name not in current:
            current[field_name] = []
        
        # Add value if not duplicate
        if value not in current[field_name]:
            current[field_name].append(value)
    
    def _set_field(self, ehr: Dict, field: str, value: Any) -> None:
        """Set value to nested single field."""
        parts = field.split(".")
        
        current = ehr
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        
        current[parts[-1]] = value
    
    def _populate_extracted_entities(
        self,
        ehr: Dict,
        entity_groups: Dict
    ) -> None:
        """Populate extracted_entities section."""
        extracted = ehr.get("extracted_entities", {})
        
        type_to_key = {
            "SYMPTOM": "symptoms",
            "DISEASE": "diseases",
            "MEDICATION": "medications",
            "DURATION": "durations",
            "ALLERGY": "allergies",
            "BODY_PART": "body_parts",
            "TREATMENT": "treatments",
            "DOSAGE": "dosages"
        }
        
        for entity_type, key in type_to_key.items():
            if entity_type in entity_groups:
                extracted[key] = [
                    e.get("text", "") for e in entity_groups[entity_type]
                ]
        
        ehr["extracted_entities"] = extracted
    
    def _generate_patient_id(self) -> str:
        """Generate unique patient ID."""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        import random
        return f"PAT_{timestamp}_{random.randint(1000, 9999)}"
    
    def to_text(self, ehr: Dict) -> str:
        """
        Convert EHR to human-readable text.
        
        Args:
            ehr: EHR dictionary
        
        Returns:
            Human-readable text
        """
        lines = []
        
        lines.append("=" * 60)
        lines.append("ELECTRONIC HEALTH RECORD")
        lines.append("=" * 60)
        lines.append("")
        
        # Patient Info
        lines.append(f"Patient ID: {ehr.get('patient_id', 'N/A')}")
        lines.append(f"Consultation Date: {ehr.get('consultation_date', 'N/A')}")
        lines.append("")
        
        # Chief Complaint
        lines.append("CHIEF COMPLAINT")
        lines.append("-" * 40)
        
        symptoms = ehr.get("chief_complaint", {}).get("symptoms", [])
        if symptoms:
            for symptom in symptoms:
                if isinstance(symptom, dict):
                    name = symptom.get("name", "")
                    duration = symptom.get("duration", "")
                    text = f"  - {name}"
                    if duration:
                        text += f" (Duration: {duration})"
                    lines.append(text)
                else:
                    lines.append(f"  - {symptom}")
        else:
            lines.append("  No symptoms recorded")
        
        duration = ehr.get("chief_complaint", {}).get("duration", "")
        if duration:
            lines.append(f"Duration: {duration}")
        
        lines.append("")
        
        # Medical History
        lines.append("MEDICAL HISTORY")
        lines.append("-" * 40)
        
        diseases = ehr.get("medical_history", {}).get("diseases", [])
        if diseases:
            lines.append("Diseases:")
            for disease in diseases:
                lines.append(f"  - {disease}")
        else:
            lines.append("Diseases: None recorded")
        
        medications = ehr.get("medical_history", {}).get("current_medications", [])
        if medications:
            lines.append("Current Medications:")
            for med in medications:
                if isinstance(med, dict):
                    text = f"  - {med.get('name', '')}"
                    if med.get('dosage'):
                        text += f" ({med.get('dosage')})"
                    lines.append(text)
                else:
                    lines.append(f"  - {med}")
        
        allergies = ehr.get("medical_history", {}).get("allergies", [])
        if allergies:
            lines.append("Allergies:")
            for allergy in allergies:
                lines.append(f"  - {allergy}")
        
        lines.append("")
        
        # Assessment & Plan
        lines.append("ASSESSMENT & PLAN")
        lines.append("-" * 40)
        
        impression = ehr.get("assessment_and_plan", {}).get("impression", "")
        if impression:
            lines.append(f"Impression: {impression}")
        
        recommendations = ehr.get("assessment_and_plan", {}).get("recommendations", [])
        if recommendations:
            lines.append("Recommendations:")
            for rec in recommendations:
                lines.append(f"  - {rec}")
        
        follow_up = ehr.get("assessment_and_plan", {}).get("follow_up", "")
        if follow_up:
            lines.append(f"Follow-up: {follow_up}")
        
        lines.append("")
        
        # Metadata
        lines.append("-" * 40)
        lines.append(f"Dialect: {ehr.get('metadata', {}).get('dialect', 'Unknown')}")
        lines.append(f"Language: {ehr.get('metadata', {}).get('language', 'bn')}")
        
        return "\n".join(lines)
    
    def to_markdown(self, ehr: Dict) -> str:
        """Convert EHR to Markdown format."""
        md = []
        
        md.append("# Electronic Health Record\n")
        
        md.append("## Patient Information")
        md.append(f"- **Patient ID**: {ehr.get('patient_id', 'N/A')}")
        md.append(f"- **Consultation Date**: {ehr.get('consultation_date', 'N/A')}")
        md.append("")
        
        md.append("## Chief Complaint")
        symptoms = ehr.get("chief_complaint", {}).get("symptoms", [])
        if symptoms:
            for symptom in symptoms:
                if isinstance(symptom, dict):
                    text = f"- {symptom.get('name', '')}"
                    if symptom.get('duration'):
                        text += f" ({symptom.get('duration')})"
                    md.append(text)
                else:
                    md.append(f"- {symptom}")
        else:
            md.append("*No symptoms recorded*")
        md.append("")
        
        md.append("## Medical History")
        
        diseases = ehr.get("medical_history", {}).get("diseases", [])
        md.append("**Diseases:**")
        if diseases:
            for d in diseases:
                md.append(f"- {d}")
        else:
            md.append("*None recorded*")
        
        medications = ehr.get("medical_history", {}).get("current_medications", [])
        md.append("**Current Medications:**")
        if medications:
            for m in medications:
                if isinstance(m, dict):
                    text = f"- {m.get('name', '')}"
                    if m.get('dosage'):
                        text += f" ({m.get('dosage')})"
                    md.append(text)
                else:
                    md.append(f"- {m}")
        else:
            md.append("*None recorded*")
        
        allergies = ehr.get("medical_history", {}).get("allergies", [])
        md.append("**Allergies:**")
        if allergies:
            for a in allergies:
                md.append(f"- {a}")
        else:
            md.append("*None recorded*")
        
        md.append("")
        
        md.append("## Assessment & Plan")
        
        impression = ehr.get("assessment_and_plan", {}).get("impression", "")
        if impression:
            md.append(f"**Impression:** {impression}")
        
        recommendations = ehr.get("assessment_and_plan", {}).get("recommendations", [])
        if recommendations:
            md.append("**Recommendations:**")
            for r in recommendations:
                md.append(f"- {r}")
        
        follow_up = ehr.get("assessment_and_plan", {}).get("follow_up", "")
        if follow_up:
            md.append(f"**Follow-up:** {follow_up}")
        
        return "\n".join(md)


def save_ehr(
    ehr: Dict,
    output_path: str,
    format: str = "json"
) -> None:
    """
    Save EHR to file.
    
    Args:
        ehr: EHR dictionary
        output_path: Output file path
        format: Output format (json/text/markdown)
    """
    generator = EHRGenerator()
    
    if format == "json":
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(ehr, f, ensure_ascii=False, indent=2)
    
    elif format == "text":
        text = generator.to_text(ehr)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
    
    elif format == "markdown":
        md = generator.to_markdown(ehr)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md)


if __name__ == "__main__":
    # Example usage
    entities = [
        {"text": "মাথা ঘুরা", "type": "SYMPTOM", "start": 0, "end": 10},
        {"text": "জ্বর", "type": "SYMPTOM", "start": 15, "end": 18},
        {"text": "গতকাল থেকে", "type": "DURATION", "start": 20, "end": 30},
        {"text": "ডায়াবেটিস", "type": "DISEASE", "start": 35, "end": 43},
        {"text": "ইনসুলিন", "type": "MEDICATION", "start": 48, "end": 55},
        {"text": "পেনিসিলিন", "type": "ALLERGY", "start": 60, "end": 69},
    ]
    
    transcription = "আমার মাথা ঘুরা এবং জ্বর আছে। গতকাল থেকে ডায়াবেটিস আছে এবং ইনসুলিন খাই। পেনিসিলিনে অ্যালার্জি আছে।"
    
    generator = EHRGenerator()
    ehr = generator.generate(entities, transcription, dialect="dhaka")
    
    print(generator.to_text(ehr))
