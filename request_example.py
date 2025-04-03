import requests

url = "http://localhost:8000/anonymize/"
files = {"file": open("data/example.jpg", "rb")}

response = requests.post(url, files=files)

if response.status_code == 200:
    with open("anonymized_image.png", "wb") as f:
        f.write(response.content)
else:
    print(f"Error: {response.text}")
