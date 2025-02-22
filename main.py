import requests

token = ""
version = 5.199
domain = ""
fields = "bdate,activities,city,occupation"

response = requests.get(
    "https://api.vk.com/method/users.get",
    params={
        "user_ids": domain,
        "access_token": token,
        "v": version,
        "fields": fields,
    },
)

data = response.json()

