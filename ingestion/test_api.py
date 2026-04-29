import requests

url = "https://xkcd.com/info.0.json"

response = requests.get(url, timeout=10)
response.raise_for_status()

comic = response.json()

print("API test successful!")
print("Comic ID:", comic["num"])
print("Title:", comic["title"])
print("Date:", f'{comic["year"]}-{comic["month"]}-{comic["day"]}')
print("Image URL:", comic["img"])