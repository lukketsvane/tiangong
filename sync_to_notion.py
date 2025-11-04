#!/usr/bin/env python3
"""
Sync Tiangong research database (CSV) to Notion database.

This script reads the planned_research_main.csv file and syncs it to a Notion database.
Each row in the CSV becomes a page in the Notion database with corresponding properties.
"""

import csv
import os
import sys
from datetime import datetime
from typing import Dict, List, Any

try:
    from notion_client import Client
    from dotenv import load_dotenv
except ImportError:
    print("Error: Required packages not installed.")
    print("Please install them with: pip install notion-client python-dotenv")
    sys.exit(1)

# Load environment variables
load_dotenv()

# Configuration
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
CSV_FILE = "planned_research_main.csv"


def validate_config():
    """Validate that required configuration is present."""
    if not NOTION_TOKEN:
        print("Error: NOTION_TOKEN not found in environment variables.")
        print("Please set it in a .env file or as an environment variable.")
        sys.exit(1)
    
    if not NOTION_DATABASE_ID:
        print("Error: NOTION_DATABASE_ID not found in environment variables.")
        print("Please set it in a .env file or as an environment variable.")
        sys.exit(1)
    
    if not os.path.exists(CSV_FILE):
        print(f"Error: CSV file '{CSV_FILE}' not found.")
        sys.exit(1)


def read_csv_data() -> List[Dict[str, str]]:
    """Read data from the CSV file."""
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)


def create_notion_page_properties(row: Dict[str, str]) -> Dict[str, Any]:
    """Convert CSV row to Notion page properties."""
    properties = {
        "Name": {
            "title": [
                {
                    "text": {
                        "content": row.get("Experiment_Name", "")
                    }
                }
            ]
        },
        "Station": {
            "select": {
                "name": row.get("Station", "")
            }
        },
        "Discipline": {
            "rich_text": [
                {
                    "text": {
                        "content": row.get("Discipline", "")
                    }
                }
            ]
        },
        "Country/Institution": {
            "rich_text": [
                {
                    "text": {
                        "content": row.get("Country_Institution", "")
                    }
                }
            ]
        },
        "Timeline Status": {
            "rich_text": [
                {
                    "text": {
                        "content": row.get("Timeline_Status", "")
                    }
                }
            ]
        },
        "Objectives": {
            "rich_text": [
                {
                    "text": {
                        "content": row.get("Objectives", "")
                    }
                }
            ]
        },
        "Expected Outcomes": {
            "rich_text": [
                {
                    "text": {
                        "content": row.get("Expected_Outcomes", "")
                    }
                }
            ]
        },
        "Principal Investigator": {
            "rich_text": [
                {
                    "text": {
                        "content": row.get("Principal_Investigator", "")
                    }
                }
            ]
        },
        "Mission Module": {
            "rich_text": [
                {
                    "text": {
                        "content": row.get("Mission_Module", "")
                    }
                }
            ]
        }
    }
    
    return properties


def get_existing_pages(notion: Client, database_id: str) -> Dict[str, str]:
    """Get all existing pages from the Notion database."""
    existing_pages = {}
    has_more = True
    start_cursor = None
    
    while has_more:
        params = {"database_id": database_id}
        if start_cursor:
            params["start_cursor"] = start_cursor
        
        response = notion.databases.query(**params)
        
        for page in response["results"]:
            # Use experiment name as key
            title_property = page["properties"].get("Name", {})
            if title_property.get("title") and len(title_property["title"]) > 0:
                name = title_property["title"][0]["text"]["content"]
                existing_pages[name] = page["id"]
        
        has_more = response["has_more"]
        start_cursor = response.get("next_cursor")
    
    return existing_pages


def sync_to_notion():
    """Main sync function."""
    validate_config()
    
    print("Starting sync to Notion...")
    print(f"CSV file: {CSV_FILE}")
    print(f"Database ID: {NOTION_DATABASE_ID}")
    
    # Initialize Notion client
    notion = Client(auth=NOTION_TOKEN)
    
    # Read CSV data
    csv_data = read_csv_data()
    print(f"Found {len(csv_data)} experiments in CSV")
    
    # Get existing pages
    print("Fetching existing pages from Notion...")
    existing_pages = get_existing_pages(notion, NOTION_DATABASE_ID)
    print(f"Found {len(existing_pages)} existing pages in Notion")
    
    # Sync each row
    created_count = 0
    updated_count = 0
    error_count = 0
    errors = []
    
    for row in csv_data:
        experiment_name = row.get("Experiment_Name", "")
        if not experiment_name:
            continue
        
        properties = create_notion_page_properties(row)
        
        if experiment_name in existing_pages:
            # Update existing page
            page_id = existing_pages[experiment_name]
            try:
                notion.pages.update(page_id=page_id, properties=properties)
                updated_count += 1
                print(f"✓ Updated: {experiment_name}")
            except Exception as e:
                error_count += 1
                error_msg = f"Error updating {experiment_name}: {e}"
                errors.append(error_msg)
                print(f"✗ {error_msg}")
        else:
            # Create new page
            try:
                notion.pages.create(
                    parent={"database_id": NOTION_DATABASE_ID},
                    properties=properties
                )
                created_count += 1
                print(f"+ Created: {experiment_name}")
            except Exception as e:
                error_count += 1
                error_msg = f"Error creating {experiment_name}: {e}"
                errors.append(error_msg)
                print(f"✗ {error_msg}")
    
    print("\n" + "="*60)
    print(f"Sync complete!")
    print(f"Created: {created_count} pages")
    print(f"Updated: {updated_count} pages")
    print(f"Errors: {error_count}")
    print("="*60)
    
    # If all operations failed, show common issues and exit with error
    if created_count == 0 and updated_count == 0 and len(csv_data) > 0:
        print("\n⚠️  WARNING: No pages were created or updated!")
        print("\nCommon issues:")
        print("1. Database not shared with integration")
        print("   → Open database in Notion → Click '...' → 'Add connections' → Select integration")
        print("\n2. Property type mismatch")
        print("   → Ensure 'Station' property is type 'Select' (not 'Text')")
        print("   → Ensure 'Station' has options: 'Tiangong' and 'ISS'")
        print("\n3. Invalid database ID or token")
        print("   → Verify NOTION_DATABASE_ID in secrets")
        print("   → Verify NOTION_TOKEN is valid and not expired")
        
        if errors:
            print("\nFirst few errors:")
            for error in errors[:3]:
                print(f"  • {error}")
        
        sys.exit(1)
    
    # If some operations failed but not all, show warning but don't exit
    if error_count > 0:
        print(f"\n⚠️  Warning: {error_count} operation(s) failed")
        if errors:
            print("\nFirst few errors:")
            for error in errors[:5]:
                print(f"  • {error}")


if __name__ == "__main__":
    sync_to_notion()
