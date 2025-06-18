from aiohttp import ClientSession
from cfg import *

async def get_data_from_bx24(id_):
    async with ClientSession() as sess:
        res = await sess.post(url=f"https://btg24.bitrix24.ru/rest/{userId_bx24}/{keyWebhookBX24}/crm.deal.get?ID={id_}")
        data = await res.json()
        
    return data.get("result", {})
    
async def get_resp_without_filter(entity_id, select_fields, filters=None):
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
    
    async with ClientSession() as sess:
        resp = await sess.post(
            url="https://btg-sped.ru/crm/api/rest.php",
            json=params,
            ssl=False
        )
        data = await resp.json(content_type='text/html')
        data = data['data']
        
        return data

async def post_data_to_ruk(route, direction, inn, btg_manager_kam, comment_on_the_deal, the_customer_company):
    params = {
        'key': apiKey,
        'username': username,
        'password': passw,
        'action': 'insert',
        'entity_id': '369', 
        'items': {
            'field_12776': int(route),
            'field_12775': int(direction),
            'field_12778': inn,
            'field_12779': int(btg_manager_kam),
            'field_12780': comment_on_the_deal,
            'field_12782': (the_customer_company),
            #'field_559': '318',
        }      
    }
    
    async with ClientSession() as sess:
        res = await sess.post(url="https://btg-sped.ru/crm/api/rest.php", ssl=False, json=params)
        
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
    
async def get_inn_bx24(id_):
    async with ClientSession() as sess:
        res = await sess.post(url=f"https://{prefix_bx24}.bitrix24.ru/rest/{userId_bx24}/{keyWebhookBX24}/crm.company.get?ID={id_}")
        data = await res.json()
        
        return data.get("result", {}).get("UF_CRM_1749452196788", "")