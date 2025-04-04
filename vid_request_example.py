import requests

url = "http://localhost:8000/anonymize/video"
files = {"file": open("baby-crying.mp4", "rb")}

response = requests.post(url, files=files)

if response.status_code == 200:
    with open("anonymized_video.mp4", "wb") as f:
        f.write(response.content)
else:
    print(f"Error: {response.text}")
