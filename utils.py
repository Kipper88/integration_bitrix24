from aiohttp import ClientSession, ClientTimeout
from cfg import *
import json
import logging

logger = logging.getLogger("webhook")

async def get_data_from_bx24(action):
    async with ClientSession() as sess:
        res = await sess.post(url=f"https://btg24.bitrix24.ru/rest/{userId_bx24}/{keyWebhookBX24}/{action}")
        data = await res.json()
        
    return data.get("result", {})

async def post_data_to_bx24(action, data):
    params = {
        "fields": data,
        "params": {"REGISTER_SONET_EVENT": "Y"}
    }
    async with ClientSession() as sess:
        res = await sess.post(url=f"https://btg24.bitrix24.ru/rest/{userId_bx24}/{keyWebhookBX24}/{action}", json=params)
        data = await res.json()
        
        
    return data.get("result", {})

async def post_data_site_company_to_lid_bx24(data: dict):
    await post_data_to_bx24("crm.lead.add", data)
    
    
    
async def get_resp_without_filter(entity_id, select_fields, filters=None, timeout=None):
    params = {
            'key': apiKey,
            'username': username,
            'password': passw,
            'action': 'select',
            'entity_id': entity_id,
            'select_fields': select_fields,
    }
    
    if filters:
       params['filters'] = filters
    
    async with ClientSession(timeout=ClientTimeout(timeout)) as sess:
        resp = await sess.post(
            url="https://btg-sped.ru/crm/api/rest.php",
            json=params,
            ssl=False
        )
        data = await resp.json(content_type='text/html')
        data = data['data']
        
        return data

async def post_data_to_ruk(entity_id, items):
    params = {
        'key': apiKey,
        'username': username,
        'password': passw,
        'action': 'insert',
        'entity_id': entity_id, 
        'items': items
    }
    
    async with ClientSession() as sess:
        res = await sess.post(url="https://btg-sped.ru/crm/api/rest.php", ssl=False, json=params)
        
        if res.status == 200:
            data = await res.json(content_type='text/html')
            data = data['data']
            
            return data.get('id')
        
async def post_data_kp_to_ruk(items, id_deal):
    params = {
        'key': apiKey,
        'username': username,
        'password': passw,
        'action': 'update',
        'entity_id': '369', 
        'data': items,
        'update_by_field': {'id': id_deal}
    }
    
    async with ClientSession() as sess:
        res = await sess.post(url="https://btg-sped.ru/crm/api/rest.php", ssl=False, json=params)
                
        if res.status == 200:
            data = await res.json(content_type='text/html')
            data = data['data']
            
            return data.get('id')
        

async def post_data_kom_predlojenie_to_ruk(id):
    params = {
        'key': apiKey,
        'username': username,
        'password': passw,
        'action': 'insert',
        'entity_id': '372', 
        'items': {
            'field_12971': "",
            'field_12969': "5486",
            'parent_item_id': id
            
        }
    }
    async with ClientSession() as sess:
        res = await sess.post(url="https://btg-sped.ru/crm/api/rest.php", ssl=False, json=params)
        
        if res.status == 200:
            data = await res.json(content_type='text/html')
            data = data['data']
            
            return data.get('id')
        
async def post_id_deal_to_bx24(id_deal_bx24, id_ruk):
    async with ClientSession() as sess:
        params = {
            "ID": id_deal_bx24,
            "FIELDS": {
                "UF_CRM_1753865222": id_ruk
            }
        }
        
        await sess.post(url=f"https://btg24.bitrix24.ru/rest/{userId_bx24}/{keyWebhookBX24}/crm.deal.update", json=params)
             
async def post_id_bid_to_bx24(id):
    async with ClientSession() as sess:
        params = {
            "ID": id,
            "FIELDS": {
                "UF_CRM_1753865270": id
            }
        }
        await sess.post(url=f"https://btg24.bitrix24.ru/rest/{userId_bx24}/{keyWebhookBX24}/crm.quote.update", params=params) 
                 
async def get_worker_from_bx24(id_):
    async with ClientSession() as sess:
        res = await sess.post(url=f"https://btg24.bitrix24.ru/rest/{userId_bx24}/{keyWebhookBX24}/im.user.get.json?ID={id_}")
        data = await res.json()
    
    return data.get("result", {}).get("name", "")
        
async def get_worker_from_rukovoditel(name_bx24):
    data = await get_resp_without_filter('104', '2439,2438,11588,4465')

    for i in data:
        if f"{i['2439']} {i['2438']}" == name_bx24:
            return i['4465_db_value']
        
async def get_company_from_rukovoditel(inn):
    data = await get_resp_without_filter("68", "1004", filters = {"1004": inn})
    
    data2 = await get_resp_without_filter("68", "2650", filters = {"2650": inn})
    
    return (data[0].get("id") if data else None) \
    or (data2[0].get("id") if data2 else None) \
    or "0123456789"
        
async def get_company_from_rukovoditel_btg_company(inn):
    data = await get_resp_without_filter("66", "880", filters = {"880": inn}, timeout=15)
    try:
        return data[0].get('id')
    except:
        return "391"
    
async def get_inn_bx24(id_):
    async with ClientSession() as sess:
        res = await sess.post(url=f"https://{prefix_bx24}.bitrix24.ru/rest/{userId_bx24}/{keyWebhookBX24}/crm.company.get?ID={id_}")
        data = await res.json()
        
        return data.get("result", {}).get("UF_CRM_1749452196788", "")
    

class CheckUpdateStatus:
    def __init__(self): 
        pass

    async def getJson(self):
        with open(temp_json_file, 'r', encoding='utf-8') as f:
            contents = f.read()
            return json.loads(contents)
        
    async def checkStatusBx24(self, id_, status):
        if status in ["UC_E0YGIO"]:
            if await self.checkExist(id_):
                return True
        
    async def checkExist(self, id_):
        j = await self.getJson()
        
        if id_ in j:
            return False
        return True
        
    async def checkStatus(self, id_, status):        
        j = await self.getJson()

        if id_ in j:
            if status == "LOSE":
                return "delete"
            if j[id_] == status:
                return False
            if j[id_] != status:
                return "update"
        else:
            return "add"

    async def addId(self, id_):
        j = await self.getJson()
        
        if id_ not in j:
            j.append(id_)

        with open(temp_json_file, 'w', encoding='utf-8') as f:
            json.dump(j, f, indent=4, ensure_ascii=False)

    async def updateId(self, id_, status: str):
        await self.addId(id_, status)

    async def deleteId(self, id_):
        j = await self.getJson()

        del j[id_]

        with open(temp_json_file, 'w') as f:
            await f.write(json.dumps(j, indent=4))
            
            
def ensure_temp_file():
    logger.info("Инициализация кэша...")
    
    if not os.path.exists(temp_json_file):
        with open(temp_json_file, 'w', encoding='utf-8') as f:
            json.dump({}, f, ensure_ascii=False, indent=4)
            
    logger.info("Инициализация кэша завершена")