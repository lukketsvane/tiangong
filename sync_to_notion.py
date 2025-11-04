import csv
import os
from notion_client import Client

# Initialize Notion client
notion = Client(auth=os.environ.get("NOTION_API_KEY"))
DATABASE_ID = os.environ.get("NOTION_DATABASE_ID")

def parse_csv(file_path):
    """Read and parse the CSV file"""
    experiments = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='|')
        for row in reader:
            # Clean up whitespace
            experiments.append({k.strip(): v.strip() if v else "" for k, v in row.items()})
    return experiments

def create_or_update_notion_page(experiment):
    """Create or update a Notion database entry"""
    properties = {
        "Name": {"title": [{"text": {"content": experiment.get("Experiment_Name", "")[:2000]}}]},
        "Station": {"select": {"name": experiment.get("Station", "Unknown")}},
        "Discipline": {"select": {"name": experiment.get("Discipline", "")[:100] if experiment.get("Discipline") else "Other"}},
        "Country/Institution": {"rich_text": [{"text": {"content": experiment.get("Country_Institution", "")[:2000]}}]},
        "Status": {"select": {"name": experiment.get("Timeline_Status", "")[:100] if experiment.get("Timeline_Status") else "Unknown"}},
        "Objectives": {"rich_text": [{"text": {"content": experiment.get("Objectives", "")[:2000]}}]},
        "Expected Outcomes": {"rich_text": [{"text": {"content": experiment.get("Expected_Outcomes", "")[:2000]}}]},
        "Principal Investigator": {"rich_text": [{"text": {"content": experiment.get("Principal_Investigator", "")[:2000]}}]},
        "Mission/Module": {"rich_text": [{"text": {"content": experiment.get("Mission_Module", "")[:2000]}}]},
    }
    
    # Search for existing page by name
    existing_pages = notion.databases.query(
        database_id=DATABASE_ID,
        filter={
            "property": "Name",
            "title": {
                "equals": experiment.get("Experiment_Name", "")[:2000]
            }
        }
    )
    
    if existing_pages["results"]:
        # Update existing page
        page_id = existing_pages["results"][0]["id"]
        notion.pages.update(page_id=page_id, properties=properties)
        print(f"✓ Updated: {experiment.get('Experiment_Name', '')}")
    else:
        # Create new page
        notion.pages.create(parent={"database_id": DATABASE_ID}, properties=properties)
        print(f"✓ Created: {experiment.get('Experiment_Name', '')}")

def sync_to_notion(csv_file):
    """Main sync function"""
    print("Starting sync to Notion...")
    experiments = parse_csv(csv_file)
    print(f"Found {len(experiments)} experiments in CSV")
    
    for i, experiment in enumerate(experiments, 1):
        try:
            create_or_update_notion_page(experiment)
        except Exception as e:
            print(f"✗ Error with experiment {i}: {str(e)}")
    
    print("Sync completed!")

if __name__ == "__main__":
    sync_to_notion("planned_research_main.csv")