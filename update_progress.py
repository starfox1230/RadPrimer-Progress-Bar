import requests
import json
import os

# Fetch the environment variables
NOTION_API_KEY = os.getenv('NOTION_API_KEY')
DATABASE_ID = '41c0d262592f416d8484747d519cdf1e'  # Replace with your actual Notion database ID

# Set up the headers for the API request
headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# Make the API request to query the database
response = requests.post(f"https://api.notion.com/v1/databases/{DATABASE_ID}/query", headers=headers)
data = response.json()

# Print the API response to inspect the structure
print("API Response:", json.dumps(data, indent=4))

# Fetching the value from 'Qs Done Number' property
try:
    qs_done_number = data['results'][0]['properties']['Qs Done Number']['formula']['string']
    if qs_done_number is not None:
        count = int(qs_done_number)
    else:
        # If 'Qs Done Number' is null, we'll use 'Formula' as a fallback
        count = data['results'][0]['properties']['Formula']['formula']['number']
    
    print("Fetched Count:", count)
    with open('progress.json', 'w') as f:
        json.dump({"count": count}, f)
except (KeyError, ValueError, TypeError) as e:
    print(f"Error: {e}. Check the structure of the 'Qs Done Number' and 'Formula' properties in the API response.")
    count = 0
    with open('progress.json', 'w') as f:
        json.dump({"count": count}, f)

# Git commands to commit and push the changes
os.system('git config --global user.email "sterlingmcj@gmail.com"')
os.system('git config --global user.name "starfox1230"')
os.system('git add progress.json')
os.system('git commit -m "Update progress count"')
os.system(f'git push https://{os.getenv("PERSONAL_ACCESS_TOKEN")}@github.com/starfox1230/RadPrimer-Progress-Bar.git')
