import requests

client_id = "30797"
client_secret = "CYsypK7pwPUgsvzSWnBSIA(("
redirect_uri = "http://localhost:8000/callback"
code = "yiYwehnV3uORDPMniV1VGA))"

token_url = "https://stackoverflow.com/oauth/access_token/json"

data = {
    "client_id": client_id,
    "client_secret": client_secret,
    "code": code,
    "redirect_uri": redirect_uri,
    "grant_type": "authorization_code",
}

response = requests.post(token_url, data=data)

# 🔴 Ajoute cette ligne pour voir la réponse exacte de l'API
print("Réponse brute :", response.text)

if response.status_code == 200:
    token_info = response.json()
    print("Access Token :", token_info.get("access_token"))
else:
    print("Erreur :", response.text)
