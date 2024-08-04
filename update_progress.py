import requests
import json
import os

NOTION_API_KEY = os.getenv('NOTION_API_KEY')
DATABASE_ID = '41c0d262592f416d8484747d519cdf1e'  # Replace with your actual Notion database ID

headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

response = requests.post(f"https://api.notion.com/v1/databases/{DATABASE_ID}/query", headers=headers)
data = response.json()

# Print the API response to inspect its structure
print("API Response:", json.dumps(data, indent=4))

# Assuming there's only one row and the column name is 'Qs Done Number'
try:
    count = data['results'][0]['properties']['Qs Done Number']['number']
    # Debugging: Print the fetched count
    print("Fetched Count:", count)

    # Update progress.json
    with open('progress.json', 'w') as f:
        json.dump({"count": count}, f)
except KeyError as e:
    print(f"KeyError: {e}")
    print("Check the structure of the 'Qs Done Number' property in the API response.")
    count = 0
    with open('progress.json', 'w') as f:
        json.dump({"count": count}, f)

# Commit and push changes
os.system('git config --global user.email "sterlingmcj@gmail.com"')
os.system('git config --global user.name "starfox1230"')
os.system('git add progress.json')
os.system('git commit -m "Update progress count"')
os.system(f'git push https://{os.getenv("PERSONAL_ACCESS_TOKEN")}@github.com/starfox1230/RadPrimer-Progress-Bar.git')