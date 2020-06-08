import requests
import sys
import json

if len(sys.argv) == 1:
    print("Usage: python3 gen_oauth_token.py <CLIENT_ID> <CLIENT_SECRET>")
    sys.exit()

cid = sys.argv[1]
csecret = sys.argv[2]

url = "https://id.twitch.tv/oauth2/token?client_id="+cid+"&client_secret="+csecret+"&grant_type=client_credentials"

gen_token = requests.post(url)
gt_json = json.loads(gen_token.text)

print("OAuth Access Token:\n"+gt_json["access_token"])
