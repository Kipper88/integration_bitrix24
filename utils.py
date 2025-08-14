from aiohttp import ClientSession, ClientTimeout
from cfg import *
import json

async def get_data_from_bx24_deal(id_):
    async with ClientSession() as sess:
        res = await sess.post(url=f"https://btg24.bitrix24.ru/rest/{userId_bx24}/{keyWebhookBX24}/crm.deal.get?ID={id_}")
        data = await res.json()
        
    return data.get("result", {})

async def get_data_from_bx24_bid(id_):
    async with ClientSession() as sess:
        res = await sess.post(url=f"https://btg24.bitrix24.ru/rest/{userId_bx24}/{keyWebhookBX24}/crm.quote.get?id={id_}")
        data = await res.json()
        
    return data.get("result", {})
    
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

async def post_data_to_ruk(route, direction, inn, btg_manager_kam, comment_on_the_deal, the_customer_company,\
    f12795, f12796, f12797, f12798, f12799, f12800, f12801, f12802, f12803, f12804, f12805, f12806, f12807, f12808, f12809, f12810, f12811, f12812, f12813, f12814, f12815, f12816, f12817,\
    f12837, f12838, f12839, f12840, f12841, f12842, f12844, f12845, f12846, f12847, f12835, f12836,\
    f12848, f12850):
    params = {
        'key': apiKey,
        'username': username,
        'password': passw,
        'action': 'insert',
        'entity_id': '369', 
        'items': {
            'field_12776': route,
            'field_12775': direction,
            'field_12778': inn,
            'field_12779': btg_manager_kam,
            'field_12780': comment_on_the_deal,
            'field_12782': the_customer_company,
            #'field_559': '318',
            
            "field_12795": f12795,
            "field_12796": f12796,
            "field_12797": f12797,
            "field_12798": f12798,
            "field_12799": f12799,
            "field_12800": f12800,
            "field_12801": f12801,
            "field_12802": f12802,
            "field_12803": f12803,
            "field_12804": f12804,
            "field_12805": f12805,
            "field_12806": f12806,
            "field_12807": f12807,
            "field_12808": f12808,
            "field_12809": f12809,
            "field_12810": f12810,
            "field_12811": f12811,
            "field_12812": f12812,
            "field_12813": f12813,
            "field_12814": f12814,
            "field_12815": f12815,
            "field_12816": f12816,
            "field_12817": f12817,

            "field_12837": f12837,
            "field_12838": f12838,
            "field_12839": f12839,
            "field_12840": f12840,
            "field_12841": f12841,
            "field_12842": f12842,
            "field_12844": f12844,
            "field_12845": f12845,
            "field_12846": f12846,
            "field_12847": f12847,
            "field_12835": f12835,
            "field_12836": f12836,

            "field_12848": f12848,
            "field_12850": f12850,
        }      
    }
    
    async with ClientSession() as sess:
        res = await sess.post(url="https://btg-sped.ru/crm/api/rest.php", ssl=False, json=params)
        
        if res.status == 200:
            data = await res.json(content_type='text/html')
            data = data['data']
            
            return data.get('id')
        
async def post_data_tech_naimenovanie_to_ruk(f12974, f12973, f12975, f12972, parent_item_id_bid):
    params = {
        'key': apiKey,
        'username': username,
        'password': passw,
        'action': 'insert',
        'entity_id': '373', 
        'items': {
            'field_12974': f12974,
            'field_12973': f12973,
            'field_12975': f12975,
            'field_12972': f12972,
            'parent_item_id': parent_item_id_bid
            
        }
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

    return data[0].get('id')

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
        else:
            await self.addId(id_)
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
        
        j[id_] = '1'

        with open(temp_json_file, 'w', encoding='utf-8') as f:
            f.write(json.dumps(j, indent=4))

    async def updateId(self, id_, status: str):
        await self.addId(id_, status)

    async def deleteId(self, id_):
        j = await self.getJson()

        del j[id_]

        with open(temp_json_file, 'w') as f:
            await f.write(json.dumps(j, indent=4))
            
            
def ensure_temp_file():
    os.makedirs('temp', exist_ok=True)
    file_path = os.path.join('temp', 'temp_leads.json')
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump({}, f, ensure_ascii=False, indent=4)