import yaml
from notion_client import Client

with open('.settings.yml', 'r') as f:
    config = yaml.safe_load(f)

notion = Client(auth=config['notion']['secret'])

result = notion.search(query="").get("results")

for item in result:
    if item["object"] == "database":
        print(item["title"][0]["text"]["content"], item["id"])
