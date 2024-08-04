import requests
import json
import os
import time

# Fetch the environment variables
NOTION_API_KEY = os.getenv('NOTION_API_KEY')
DATABASE_ID = '41c0d262592f416d8484747d519cdf1e'  # Replace with your actual Notion database ID

# Set up the headers for the API request
headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def query_notion_database():
    response = requests.post(f"https://api.notion.com/v1/databases/{DATABASE_ID}/query", headers=headers)
    return response.json()

# Function to recursively search for a number value
def find_number(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "number" and isinstance(v, (int, float)):
                return v
            result = find_number(v)
            if result is not None:
                return result
    elif isinstance(obj, list):
        for item in obj:
            result = find_number(item)
            if result is not None:
                return result
    return None

# Function to print all property values
def print_all_properties(properties):
    for prop_name, prop_value in properties.items():
        print(f"Property: {prop_name}")
        print(json.dumps(prop_value, indent=2))
        print("---")

# Main execution
print("Querying Notion database...")
data = query_notion_database()

print("API Response:", json.dumps(data, indent=4))

if 'results' in data and len(data['results']) > 0:
    properties = data['results'][0]['properties']
    print("\nAll Properties:")
    print_all_properties(properties)

    count = None
    for prop_name, prop_value in properties.items():
        found_number = find_number(prop_value)
        if found_number is not None:
            print(f"Found number {found_number} in property: {prop_name}")
            if found_number != 0 and found_number != 1000:  # Assuming 0 and 1000 are not the values we're looking for
                count = found_number
                break

    if count is None:
        print("Could not find a suitable number value in any property.")
        count = 0

    print(f"\nFinal Fetched Count: {count}")

    with open('progress.json', 'w') as f:
        json.dump({"count": count}, f)

    # Git commands to commit and push the changes
    os.system('git config --global user.email "sterlingmcj@gmail.com"')
    os.system('git config --global user.name "starfox1230"')
    os.system('git add progress.json')
    os.system('git commit -m "Update progress count"')
    os.system(f'git push https://{os.getenv("PERSONAL_ACCESS_TOKEN")}@github.com/starfox1230/RadPrimer-Progress-Bar.git')
else:
    print("No results found in the Notion database response.")
