from dotenv import dotenv_values

env = dotenv_values()

apiKey = env.get('apiKeyRuk', None)
username = env.get('usernameRuk', None)
passw = env.get('passRuk', None)
keyWebhookBX24 = env.get('keyWebhookBX24', None)
prefix_bx24 = env.get('prefix_bx24', None)
userId_bx24 = env.get('userId_bx24', None)

if not apiKey or not username or not passw or not keyWebhookBX24 or not prefix_bx24 or not userId_bx24:
    raise SystemExit("Не все параметры заполнены в .env")


directions = {
    "214": "6744",
    "216": "6745",
    "218": "6746",
    "220": "6747",
    "222": "6748",
    "224": "6749",
    "226": "6750",
    "228": "6751",
    "230": "6752",
}

routes = {
    "206": "243",
    "208": "5423",
    "210": "244",
    "212": "1295",
}