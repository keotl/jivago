import requests

res = requests.get("http://localhost:8000/api/stream", stream=True)
# res = requests.get("https://proxy/bbc-radio-four.mp3", stream=True)

print("hello")
