#!/usr/bin/env python
"""
Script to validate DPR JSON data against Django models
"""
import os
import django
import sys
import json
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from dpr.models import DailyProgressReport, DPRActivity
from dpr.serializers import DailyProgressReportSerializer

def validate_dpr_json():
    print("Validating DPR JSON data...")
    print("=" * 50)

    # Load JSON data
    with open('thane_project_dpr.json', 'r') as f:
        dpr_data = json.load(f)

    errors = []
    success_count = 0

    for idx, dpr_entry in enumerate(dpr_data):
        print(f"\nValidating DPR {idx + 1}: {dpr_entry.get('report_date')}")

        try:
            # Prepare data for serializer
            serializer_data = {
                'project_name': dpr_entry['project_name'],
                'job_no': dpr_entry['job_no'],
                'report_date': dpr_entry['report_date'],
                'unresolved_issues': dpr_entry.get('unresolved_issues', ''),
                'pending_letters': dpr_entry.get('pending_letters', ''),
                'quality_status': dpr_entry.get('quality_status', ''),
                'next_day_incident': dpr_entry.get('next_day_incident', ''),
                'bill_status': dpr_entry.get('bill_status', ''),
                'gfc_status': dpr_entry.get('gfc_status', ''),
                'issued_by': dpr_entry['issued_by'],
                'designation': dpr_entry['designation'],
                'status': dpr_entry['status'],
                'activities': dpr_entry['activities']
            }

            # Validate using serializer
            serializer = DailyProgressReportSerializer(data=serializer_data)
            if serializer.is_valid():
                print(f"  [OK] Valid")
                success_count += 1
            else:
                print(f"  [ERROR] Invalid: {serializer.errors}")
                errors.append(f"DPR {idx + 1}: {serializer.errors}")

        except Exception as e:
            print(f"  [ERROR] Error: {str(e)}")
            errors.append(f"DPR {idx + 1}: {str(e)}")

    print(f"\n{'=' * 50}")
    print(f"Summary: {success_count}/{len(dpr_data)} DPRs validated successfully")

    if errors:
        print("\nErrors found:")
        for error in errors:
            print(f"  - {error}")
        return False
    else:
        print("All DPRs are valid!")
        return True

if __name__ == "__main__":
    validate_dpr_json()