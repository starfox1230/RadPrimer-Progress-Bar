import requests
import json
import os

NOTION_API_KEY = os.getenv('NOTION_API_KEY')
DATABASE_ID = 'your_database_id'

headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

response = requests.post(f"https://api.notion.com/v1/databases/{DATABASE_ID}/query", headers=headers)
data = response.json()

# Assuming there's only one row and the column name is 'Qs Done'
count = data['results'][0]['properties']['Qs Done']['number']

# Update progress.json
with open('progress.json', 'w') as f:
    json.dump({"count": count}, f)

# Commit and push changes
os.system('git config --global user.email "your-email@example.com"')
os.system('git config --global user.name "your-username"')
os.system('git add progress.json')
os.system('git commit -m "Update progress count"')
os.system(f'git push https://{os.getenv("PERSONAL_ACCESS_TOKEN")}@github.com/your-username/your-repository.git')
