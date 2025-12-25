
import requests
import json
id = "990ac0bb-63e1-4180-9ea3-864983cedaa9"
response  = requests.get(
    f"https://challenge.generatenu.com/api/v1/challenge/algorithm/{id}"
)

if response.status_code == 200:
    data = response.json()

else:
    print("Error:", response.status_code, response.text)

print(data["sensors"][1])
