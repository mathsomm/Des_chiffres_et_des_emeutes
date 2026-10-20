import requests

my_GDELTcloud_key = # à remplacer
url = "https://gdeltcloud.com/api/v2/events"
headers = {"Authorization": "Bearer "+my_GDELTcloud_key}
params = {"country": "France", "days": 7, "limit": 25, "category": "Riots"}

response = requests.get(url, headers=headers, params=params)

with open("resultat.txt", "w", encoding="utf-8") as f:
  print(response.text, file=f)
