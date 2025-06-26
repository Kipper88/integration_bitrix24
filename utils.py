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

async def post_data_to_ruk(route, direction, inn, btg_manager_kam, comment_on_the_deal, the_customer_company,\
    f12795, f12796, f12797, f12798, f12799, f12800, f12801, f12802, f12803, f12804, f12805, f12806, f12807, f12808, f12809, f12810, f12811, f12812, f12813, f12814, f12815, f12816, f12817):
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

async def get_company_from_rukovoditel_btg_company(inn):
    data = await get_resp_without_filter("66", "880", filters = {"880": inn})

    return data[0].get('id')
    
async def get_inn_bx24(id_):
    async with ClientSession() as sess:
        res = await sess.post(url=f"https://{prefix_bx24}.bitrix24.ru/rest/{userId_bx24}/{keyWebhookBX24}/crm.company.get?ID={id_}")
        data = await res.json()
        
        return data.get("result", {}).get("UF_CRM_1749452196788", "")