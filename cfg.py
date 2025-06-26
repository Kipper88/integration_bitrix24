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

f12796_dict = {
    "320": "351",
    "322": "352",
    "324": "354",
    "326": "355",
    "328": "5449",
    "330": "5530",
    "332": "6741",
    "502": "6886"
}

f12798_dict = {
    "482": "5447",
    "484": "6058"
}

f12799_dict = {
    "486": "249",
    "488": "250",
    "490": "5531",
    "492": "5532",
    "494": "5533",
    "496": "6742",
    "498": "6743",
    "500": "5563"
}

f12802_dict = {}