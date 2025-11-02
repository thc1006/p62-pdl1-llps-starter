#!/usr/bin/env python3
"""
Process TCGA Clinical Data
Extracts overall survival, cancer stage, demographics

Input: Raw TCGA clinical XML/JSON files
Output: Clean clinical DataFrame with OS, stage, age, gender

Author: Automated Pipeline
Date: 2025-11-02
"""

import os
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List
import json
import xml.etree.ElementTree as ET

# =============================================================================
# Configuration
# =============================================================================

BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data" / "tcga_raw"
OUTPUT_DIR = BASE_DIR / "outputs" / "tcga_full_cohort_real"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PROJECTS = ['TCGA-LUAD', 'TCGA-LUSC', 'TCGA-SKCM']

# =============================================================================
# Step 1: Parse Clinical XML Files
# =============================================================================

def parse_clinical_xml(xml_path: Path) -> Dict:
    """
    Parse TCGA clinical XML file

    Args:
        xml_path: Path to clinical XML file

    Returns:
        Dict with clinical variables
    """
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # Extract key fields
        data = {}

        # Patient ID
        patient_id = root.findtext('.//{*}bcr_patient_barcode')
        data['submitter_id'] = patient_id
        data['sample_id'] = patient_id[:15] if patient_id else None

        # Demographics
        data['age_at_diagnosis'] = root.findtext('.//{*}age_at_initial_pathologic_diagnosis')
        data['gender'] = root.findtext('.//{*}gender')
        data['race'] = root.findtext('.//{*}race_list/{*}race')

        # Tumor characteristics
        data['tumor_stage'] = root.findtext('.//{*}stage_event/{*}pathologic_stage')
        data['tumor_grade'] = root.findtext('.//{*}neoplasm_histologic_grade')
        data['histology'] = root.findtext('.//{*}histological_type')

        # Overall Survival
        data['vital_status'] = root.findtext('.//{*}vital_status')
        data['days_to_death'] = root.findtext('.//{*}days_to_death')
        data['days_to_last_followup'] = root.findtext('.//{*}days_to_last_followup')

        # Treatment
        data['prior_treatment'] = root.findtext('.//{*}prior_diagnosis')

        return data

    except Exception as e:
        print(f"  [ERROR] Failed to parse {xml_path.name}: {e}")
        return {}

def parse_clinical_json(json_path: Path) -> Dict:
    """
    Parse TCGA clinical JSON file (newer format)

    Args:
        json_path: Path to clinical JSON file

    Returns:
        Dict with clinical variables
    """
    try:
        with open(json_path, 'r') as f:
            data_raw = json.load(f)

        # Extract from nested structure
        data = {}

        if 'submitter_id' in data_raw:
            data['submitter_id'] = data_raw['submitter_id']
            data['sample_id'] = data_raw['submitter_id'][:15]

        # Demographics
        demographic = data_raw.get('demographic', {})
        data['age_at_diagnosis'] = demographic.get('age_at_index')
        data['gender'] = demographic.get('gender')
        data['race'] = demographic.get('race')
        data['vital_status'] = demographic.get('vital_status')
        data['days_to_death'] = demographic.get('days_to_death')

        # Diagnosis
        diagnoses = data_raw.get('diagnoses', [])
        if diagnoses:
            diag = diagnoses[0]
            data['tumor_stage'] = diag.get('tumor_stage')
            data['tumor_grade'] = diag.get('tumor_grade')
            data['days_to_last_followup'] = diag.get('days_to_last_follow_up')

        return data

    except Exception as e:
        print(f"  [ERROR] Failed to parse {json_path.name}: {e}")
        return {}

# =============================================================================
# Step 2: Process Project Clinical Data
# =============================================================================

def process_project_clinical(project_id: str) -> pd.DataFrame:
    """
    Process all clinical files for a project

    Args:
        project_id: TCGA project ID (e.g., 'TCGA-LUAD')

    Returns:
        Clinical DataFrame
    """
    project_dir = DATA_DIR / f"{project_id}_clinical"
    print(f"\n[PROCESS] {project_id} Clinical Data")

    if not project_dir.exists():
        print(f"  [ERROR] Directory not found: {project_dir}")
        return pd.DataFrame()

    # Find clinical files
    xml_files = list(project_dir.glob("**/*.xml"))
    json_files = list(project_dir.glob("**/*.json"))

    print(f"  Found {len(xml_files)} XML files, {len(json_files)} JSON files")

    # Parse all files
    all_data = []

    for xml_file in xml_files:
        data = parse_clinical_xml(xml_file)
        if data:
            all_data.append(data)

    for json_file in json_files:
        data = parse_clinical_json(json_file)
        if data:
            all_data.append(data)

    if not all_data:
        print(f"  [WARN] No clinical data extracted")
        return pd.DataFrame()

    # Create DataFrame
    df = pd.DataFrame(all_data)
    print(f"  Extracted {len(df)} patient records")

    return df

# =============================================================================
# Step 3: Clean and Process Clinical Variables
# =============================================================================

def clean_clinical_data(clinical_df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and standardize clinical variables

    Args:
        clinical_df: Raw clinical DataFrame

    Returns:
        Cleaned DataFrame
    """
    print("\n[CLEAN] Standardizing clinical variables...")

    initial_n = len(clinical_df)

    # 1. Standardize sample_id
    if 'sample_id' not in clinical_df.columns:
        if 'submitter_id' in clinical_df.columns:
            clinical_df['sample_id'] = clinical_df['submitter_id'].str[:15]
        else:
            print("  [ERROR] No sample ID found")
            return pd.DataFrame()

    # Remove duplicates (keep first)
    clinical_df = clinical_df.drop_duplicates(subset='sample_id', keep='first')
    print(f"  Samples: {initial_n} -> {len(clinical_df)} (removed {initial_n - len(clinical_df)} duplicates)")

    # 2. Process Overall Survival
    clinical_df['OS_status'] = clinical_df['vital_status'].map({
        'Dead': 1,
        'Alive': 0,
        'deceased': 1,
        'alive': 0
    })

    # Calculate OS time
    clinical_df['days_to_death'] = pd.to_numeric(clinical_df['days_to_death'], errors='coerce')
    clinical_df['days_to_last_followup'] = pd.to_numeric(clinical_df['days_to_last_followup'], errors='coerce')

    clinical_df['OS_days'] = clinical_df.apply(
        lambda row: row['days_to_death'] if pd.notna(row['days_to_death'])
                    else row['days_to_last_followup'],
        axis=1
    )

    # Remove invalid OS
    valid_os = (clinical_df['OS_days'].notna()) & (clinical_df['OS_days'] > 0) & (clinical_df['OS_status'].notna())
    clinical_df = clinical_df[valid_os]
    print(f"  Valid OS data: {valid_os.sum()} patients")

    # 3. Process Age
    clinical_df['age_at_diagnosis'] = pd.to_numeric(clinical_df['age_at_diagnosis'], errors='coerce')

    # 4. Process Stage
    # Standardize stage nomenclature
    def standardize_stage(stage):
        if pd.isna(stage):
            return None
        stage_str = str(stage).upper()

        # Extract Roman numerals
        if 'IV' in stage_str or '4' in stage_str:
            return 'Stage IV'
        elif 'III' in stage_str or '3' in stage_str:
            return 'Stage III'
        elif 'II' in stage_str or '2' in stage_str:
            return 'Stage II'
        elif 'I' in stage_str or '1' in stage_str:
            return 'Stage I'
        else:
            return None

    clinical_df['tumor_stage_clean'] = clinical_df['tumor_stage'].apply(standardize_stage)

    # 5. Process Gender
    clinical_df['gender'] = clinical_df['gender'].str.upper()

    # Summary
    print("\n  Clinical variables summary:")
    print(f"    Age: {clinical_df['age_at_diagnosis'].notna().sum()} available")
    print(f"    Gender: {clinical_df['gender'].notna().sum()} available")
    print(f"    Stage: {clinical_df['tumor_stage_clean'].notna().sum()} available")
    print(f"    OS: {(clinical_df['OS_status'].notna() & clinical_df['OS_days'].notna()).sum()} available")

    return clinical_df

# =============================================================================
# Step 4: Combine Projects
# =============================================================================

def combine_all_projects() -> pd.DataFrame:
    """
    Process and combine all projects

    Returns:
        Combined clinical DataFrame
    """
    print("\n[COMBINE] Merging all projects...")

    all_clinical = []

    for project_id in PROJECTS:
        # Process project
        clinical_df = process_project_clinical(project_id)

        if clinical_df.empty:
            continue

        # Clean
        clinical_df = clean_clinical_data(clinical_df)

        # Add cancer type
        clinical_df['cancer_type'] = project_id.replace('TCGA-', '')

        all_clinical.append(clinical_df)

    # Concatenate
    if not all_clinical:
        print("  [ERROR] No clinical data available")
        return pd.DataFrame()

    final_df = pd.concat(all_clinical, axis=0, ignore_index=True)

    print(f"\n[FINAL] Combined clinical data: {len(final_df)} patients")

    # Summary by cancer type
    print("\nSample size by cancer type:")
    for cancer_type in final_df['cancer_type'].unique():
        count = (final_df['cancer_type'] == cancer_type).sum()
        print(f"  {cancer_type}: {count} patients")

    return final_df

# =============================================================================
# Main Pipeline
# =============================================================================

def main():
    """
    Main execution pipeline
    """
    print("\n" + "="*80)
    print("TCGA CLINICAL DATA PROCESSING PIPELINE")
    print("="*80)

    # Process all projects
    clinical_df = combine_all_projects()

    if clinical_df.empty:
        print("\n[ERROR] No clinical data processed")
        return

    # Select key columns
    key_columns = [
        'sample_id', 'cancer_type',
        'OS_status', 'OS_days',
        'age_at_diagnosis', 'gender',
        'tumor_stage', 'tumor_stage_clean', 'tumor_grade'
    ]

    # Keep only available columns
    available_columns = [col for col in key_columns if col in clinical_df.columns]
    clinical_df = clinical_df[available_columns]

    # Save
    output_file = OUTPUT_DIR / "clinical_data_full_real.csv"
    clinical_df.to_csv(output_file, index=False)
    print(f"\n[SAVED] {output_file}")

    # Summary statistics
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Total patients: {len(clinical_df)}")
    print(f"\nOverall Survival:")
    print(f"  Events (deaths): {clinical_df['OS_status'].sum()}")
    print(f"  Median follow-up: {clinical_df['OS_days'].median():.0f} days ({clinical_df['OS_days'].median()/365:.1f} years)")
    print(f"\nAge:")
    print(f"  Mean: {clinical_df['age_at_diagnosis'].mean():.1f} years")
    print(f"  Range: {clinical_df['age_at_diagnosis'].min():.0f}-{clinical_df['age_at_diagnosis'].max():.0f} years")
    print("="*80)

    print("\nNext step:")
    print("  Run: python scripts/excellence_upgrade/AUTOMATE_ALL_FIXES.py")

if __name__ == "__main__":
    main()
