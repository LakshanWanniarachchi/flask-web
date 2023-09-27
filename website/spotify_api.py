from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


def search_for_artist(token, id):
    url = f"https://api.spotify.com/v1/tracks/{id}"
    headers = get_auth_header(token)
   # query = f"?q={artist_name}&type=artist&limit=1"

   # query_url = url + query
    result = get(url, headers=headers)
    json_result = json.loads(result.content)

    if len(json_result) == 0:
        print("No artist with this name exists....")
        return None

    return json_result


token = get_token()
result = search_for_artist(token, id="2JYIPEjbjdHrYHLFtZ7tvr")
print(result['album']['images'][0]['url'])
