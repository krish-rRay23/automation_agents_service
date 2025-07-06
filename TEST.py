import requests

url = "http://localhost:5678/webhook-test/test-webhook"
payload = {"message": "Hello from FastAPI!"}

response = requests.post(url, json=payload)
print(response.text)
