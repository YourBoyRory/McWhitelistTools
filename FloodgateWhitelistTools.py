import requests
from uuid import UUID

class FloodgateWhitelistTools:

    headers = {'x-api-key': None}

    def __init__(self, API_key):
        self.headers['x-api-key'] = API_key

    def getXUID(self, username):
        try:
            response = requests.get(f"https://mcprofile.io/api/v1/bedrock/gamertag/{username}", headers=self.headers).json()
            uuid = UUID(response['floodgateuid'])
            return str(uuid)
        except:
            print(f"[FloodgateWhitelistTools/WARN] could not find user {username}, skipping...")
            return None
