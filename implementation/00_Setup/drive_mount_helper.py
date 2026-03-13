#!/usr/bin/env python3
"""
Google Drive Mount Helper
Provides easy-to-use functions for mounting and managing Google Drive
"""

import os
import sys


def mount_google_drive(force_remount=False, output_path='/content/drive'):
    """
    Mount Google Drive to the specified path.
    
    Args:
        force_remount: If True, force remount even if already mounted
        output_path: Path where Drive should be mounted
    
    Returns:
        str: Path to the mounted Drive
    """
    from google.colab import drive
    
    if force_remount:
        drive.flush_and_unmount()
        print("Unmounted Google Drive")
    
    try:
        drive.mount(output_path, force_remount=force_remount)
        print(f"✓ Google Drive mounted at {output_path}")
        return output_path
    except Exception as e:
        print(f"⚠ Error mounting Google Drive: {e}")
        return None


def create_project_folders(base_path='/content/drive/MyDrive/CSE499_Project'):
    """
    Create the complete project folder structure in Google Drive.
    
    Args:
        base_path: Base path for the project
    
    Returns:
        dict: Dictionary of folder paths
    """
    folders = {
        # Setup
        'setup': f'{base_path}/00_Setup',
        
        # Dataset
        'dataset': f'{base_path}/01_Dataset',
        'raw_audio': f'{base_path}/01_Dataset/01_Raw_Audio',
        'transcriptions': f'{base_path}/01_Dataset/02_Transcriptions',
        'processed_audio': f'{base_path}/01_Dataset/03_Processed_Audio',
        'annotations': f'{base_path}/01_Dataset/04_Annotations',
        'metadata': f'{base_path}/01_Dataset/05_Metadata',
        
        # Phase 1: ASR
        'phase1': f'{base_path}/02_Phase1_ASR',
        'phase1_baseline': f'{base_path}/02_Phase1_ASR/01_Baseline',
        'phase1_models': f'{base_path}/02_Phase1_ASR/02_Models',
        'phase1_scripts': f'{base_path}/02_Phase1_ASR/03_Scripts',
        'phase1_results': f'{base_path}/02_Phase1_ASR/04_Results',
        'phase1_transcripts': f'{base_path}/02_Phase1_ASR/05_Transcripts',
        
        # Phase 2: NER
        'phase2': f'{base_path}/03_Phase2_NER',
        'phase2_annotations': f'{base_path}/03_Phase2_NER/01_Annotation_Tools',
        'phase2_data': f'{base_path}/03_Phase2_NER/02_Data',
        'phase2_models': f'{base_path}/03_Phase2_NER/03_Models',
        'phase2_scripts': f'{base_path}/03_Phase2_NER/04_Scripts',
        'phase2_results': f'{base_path}/03_Phase2_NER/05_Results',
        
        # Phase 3: EHR
        'phase3': f'{base_path}/04_Phase3_EHR',
        'phase3_templates': f'{base_path}/04_Phase3_EHR/01_Templates',
        'phase3_mapping': f'{base_path}/04_Phase3_EHR/02_Mapping_Rules',
        'phase3_scripts': f'{base_path}/04_Phase3_EHR/03_Scripts',
        'phase3_samples': f'{base_path}/04_Phase3_EHR/04_Samples',
        
        # Integration
        'integration': f'{base_path}/05_Integration',
        'pipeline': f'{base_path}/05_Integration/01_Pipeline',
        'demo': f'{base_path}/05_Integration/02_Demo',
        'testing': f'{base_path}/05_Integration/03_Testing',
        
        # Documentation
        'docs': f'{base_path}/06_Documentation',
        'presentation': f'{base_path}/06_Documentation/PRESENTATION',
        
        # Backups
        'backups': f'{base_path}/07_Backups',
        
        # Shared Resources
        'shared': f'{base_path}/08_Shared_Resources',
    }
    
    # Create dialect subfolders
    dialects = ['dhaka', 'sylhet', 'chittagong', 'barishal', 'standard_bangla', 'kolkata']
    for dialect in dialects:
        folders[f'raw_audio_{dialect}'] = f"{folders['raw_audio']}/{dialect}"
        folders[f'transcriptions_{dialect}'] = f"{folders['transcriptions']}/{dialect}"
    
    # Create folders
    for folder_path in folders.values():
        os.makedirs(folder_path, exist_ok=True)
    
    print(f"✓ Created {len(folders)} project folders")
    return folders


def get_project_paths(base_path='/content/drive/MyDrive/CSE499_Project'):
    """
    Get all project paths as a dictionary.
    
    Args:
        base_path: Base path for the project
    
    Returns:
        dict: Dictionary of folder paths
    """
    return create_project_folders(base_path)


def check_drive_mounted():
    """
    Check if Google Drive is already mounted.
    
    Returns:
        bool: True if mounted, False otherwise
    """
    try:
        from google.colab import drive
        return os.path.exists('/content/drive')
    except ImportError:
        return False


def initialize_project(project_path='/content/drive/MyDrive/CSE499_Project'):
    """
    Initialize the complete project - mount Drive and create folders.
    
    Args:
        project_path: Path for the project
    
    Returns:
        dict: Dictionary of folder paths
    """
    print("=" * 60)
    print("Initializing CSE499 Project")
    print("=" * 60)
    
    # Check if already mounted
    if not check_drive_mounted():
        print("\nMounting Google Drive...")
        mount_google_drive()
    else:
        print("\n✓ Google Drive already mounted")
    
    # Create folders
    print("\nCreating project folder structure...")
    folders = create_project_folders(project_path)
    
    print("\n" + "=" * 60)
    print("✓ Project initialized successfully!")
    print("=" * 60)
    
    return folders


if __name__ == "__main__":
    # Quick initialization
    initialize_project()
