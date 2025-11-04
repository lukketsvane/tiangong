#!/usr/bin/env python3
"""
Test script to verify CSV parsing and Notion property creation.
This runs without connecting to Notion.
"""

import csv
import sys
from sync_to_notion import read_csv_data, create_notion_page_properties

def test_csv_parsing():
    """Test that CSV can be read and parsed correctly."""
    print("Testing CSV parsing...")
    
    try:
        data = read_csv_data()
        print(f"✓ Successfully read {len(data)} rows from CSV")
        
        if len(data) > 0:
            print(f"✓ First experiment: {data[0].get('Experiment_Name', 'N/A')}")
            print(f"✓ Last experiment: {data[-1].get('Experiment_Name', 'N/A')}")
        
        return True
    except Exception as e:
        print(f"✗ Error reading CSV: {e}")
        return False

def test_property_creation():
    """Test that Notion properties are created correctly."""
    print("\nTesting Notion property creation...")
    
    try:
        data = read_csv_data()
        if len(data) == 0:
            print("✗ No data to test")
            return False
        
        # Test with first row
        row = data[0]
        properties = create_notion_page_properties(row)
        
        print(f"✓ Created properties for: {row.get('Experiment_Name', 'N/A')}")
        print(f"  - Station: {row.get('Station', 'N/A')}")
        print(f"  - Discipline: {row.get('Discipline', 'N/A')}")
        print(f"  - Timeline Status: {row.get('Timeline_Status', 'N/A')}")
        
        # Verify property structure
        assert "Name" in properties
        assert "title" in properties["Name"]
        assert "Station" in properties
        assert "select" in properties["Station"]
        
        print("✓ Property structure is correct")
        
        return True
    except Exception as e:
        print(f"✗ Error creating properties: {e}")
        return False

def test_csv_completeness():
    """Test that all required columns are present."""
    print("\nTesting CSV completeness...")
    
    required_columns = [
        "Station",
        "Experiment_Name",
        "Discipline",
        "Country_Institution",
        "Timeline_Status",
        "Objectives",
        "Expected_Outcomes",
        "Principal_Investigator",
        "Mission_Module"
    ]
    
    try:
        with open('planned_research_main.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            columns = reader.fieldnames
            
            missing_columns = [col for col in required_columns if col not in columns]
            
            if missing_columns:
                print(f"✗ Missing columns: {', '.join(missing_columns)}")
                return False
            
            print(f"✓ All required columns present: {len(required_columns)}")
            return True
            
    except Exception as e:
        print(f"✗ Error checking CSV: {e}")
        return False

if __name__ == "__main__":
    print("="*60)
    print("Tiangong Database - Notion Sync Test Suite")
    print("="*60)
    
    results = []
    
    results.append(("CSV Parsing", test_csv_parsing()))
    results.append(("Property Creation", test_property_creation()))
    results.append(("CSV Completeness", test_csv_completeness()))
    
    print("\n" + "="*60)
    print("Test Results:")
    print("="*60)
    
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n✓ All tests passed! Ready to sync to Notion.")
        print("\nNext steps:")
        print("1. Create a Notion integration at https://www.notion.so/my-integrations")
        print("2. Create a Notion database with the required properties")
        print("3. Copy .env.example to .env and add your credentials")
        print("4. Run: python sync_to_notion.py")
    else:
        print("\n✗ Some tests failed. Please fix the issues before syncing.")
        sys.exit(1)
