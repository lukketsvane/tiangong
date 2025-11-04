#!/usr/bin/env python3
"""
Validate Notion database configuration.
This script checks if the database has the correct properties and structure.
"""

import os
import sys
from typing import Dict, List, Tuple

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

# Required properties with their expected types
REQUIRED_PROPERTIES = {
    "Name": "title",
    "Station": "select",
    "Discipline": "rich_text",
    "Country/Institution": "rich_text",
    "Timeline Status": "rich_text",
    "Objectives": "rich_text",
    "Expected Outcomes": "rich_text",
    "Principal Investigator": "rich_text",
    "Mission Module": "rich_text"
}

# Required select options for Station property
REQUIRED_STATION_OPTIONS = ["Tiangong", "ISS"]


def validate_config() -> bool:
    """Validate that required configuration is present."""
    if not NOTION_TOKEN:
        print("❌ Error: NOTION_TOKEN not found in environment variables.")
        print("   Please set it in a .env file or as an environment variable.")
        return False
    
    if not NOTION_DATABASE_ID:
        print("❌ Error: NOTION_DATABASE_ID not found in environment variables.")
        print("   Please set it in a .env file or as an environment variable.")
        return False
    
    print("✅ Configuration found")
    print(f"   Token: {NOTION_TOKEN[:10]}..." if len(NOTION_TOKEN) > 10 else f"   Token: {NOTION_TOKEN}")
    print(f"   Database ID: {NOTION_DATABASE_ID}")
    return True


def check_database_properties(notion: Client) -> Tuple[bool, List[str]]:
    """Check if database has all required properties."""
    try:
        database = notion.databases.retrieve(database_id=NOTION_DATABASE_ID)
        properties = database.get("properties", {})
        
        issues = []
        
        # Check each required property
        for prop_name, expected_type in REQUIRED_PROPERTIES.items():
            if prop_name not in properties:
                issues.append(f"Missing property: {prop_name}")
            else:
                actual_type = properties[prop_name].get("type")
                if actual_type != expected_type:
                    issues.append(
                        f"Property '{prop_name}' has wrong type: "
                        f"expected '{expected_type}', got '{actual_type}'"
                    )
        
        # Check Station select options
        if "Station" in properties and properties["Station"].get("type") == "select":
            select_config = properties["Station"].get("select", {})
            options = select_config.get("options", [])
            option_names = [opt.get("name") for opt in options]
            
            for required_option in REQUIRED_STATION_OPTIONS:
                if required_option not in option_names:
                    issues.append(
                        f"Station property missing option: '{required_option}'"
                    )
        
        return len(issues) == 0, issues
        
    except Exception as e:
        return False, [f"Error retrieving database: {str(e)}"]


def test_database_access(notion: Client) -> Tuple[bool, str]:
    """Test if we can access the database."""
    try:
        response = notion.databases.query(database_id=NOTION_DATABASE_ID, page_size=1)
        page_count = len(response.get("results", []))
        return True, f"Successfully accessed database. Found {page_count} existing page(s)."
    except Exception as e:
        return False, f"Error accessing database: {str(e)}"


def validate_database():
    """Main validation function."""
    print("=" * 70)
    print("Notion Database Validation")
    print("=" * 70)
    print()
    
    # Step 1: Validate configuration
    print("Step 1: Checking configuration...")
    if not validate_config():
        sys.exit(1)
    print()
    
    # Step 2: Initialize Notion client
    print("Step 2: Connecting to Notion...")
    try:
        notion = Client(auth=NOTION_TOKEN)
        print("✅ Notion client initialized")
    except Exception as e:
        print(f"❌ Error initializing Notion client: {e}")
        sys.exit(1)
    print()
    
    # Step 3: Check database access
    print("Step 3: Testing database access...")
    success, message = test_database_access(notion)
    if success:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")
        print()
        print("Common issues:")
        print("  - Database ID is incorrect")
        print("  - Integration doesn't have access to the database")
        print("  - Database has been deleted")
        print()
        print("To fix:")
        print("  1. Check the database URL and ID")
        print("  2. Share the database with your integration:")
        print("     - Open the database in Notion")
        print("     - Click '...' → 'Add connections'")
        print("     - Select your integration")
        sys.exit(1)
    print()
    
    # Step 4: Validate properties
    print("Step 4: Validating database properties...")
    success, issues = check_database_properties(notion)
    
    if success:
        print("✅ All required properties are correctly configured!")
        print()
        print("Properties found:")
        for prop_name, prop_type in REQUIRED_PROPERTIES.items():
            print(f"  • {prop_name:<25} ({prop_type})")
    else:
        print("❌ Database configuration issues found:")
        print()
        for issue in issues:
            print(f"  • {issue}")
        print()
        print("To fix these issues:")
        print("  1. Open your database in Notion")
        print("  2. Add/modify properties as needed")
        print("  3. For 'Station', ensure it's a Select property with options:")
        print("     - Tiangong")
        print("     - ISS")
        print("  4. Run this script again to validate")
        sys.exit(1)
    
    print()
    print("=" * 70)
    print("✅ Validation Complete - Database is ready for sync!")
    print("=" * 70)
    print()
    print("Next steps:")
    print("  1. Run: python sync_to_notion.py")
    print("  2. Check your Notion database for synced data")
    print()


if __name__ == "__main__":
    try:
        validate_database()
    except KeyboardInterrupt:
        print()
        print()
        print("Validation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print()
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
