import logging
from logging.handlers import RotatingFileHandler
import asyncio
from fastapi import FastAPI, Request, Response
from utils import *
from cfg import *
import traceback

handler = RotatingFileHandler(
    'webhook.log',
    maxBytes=5 * 1024 * 1024,  # 5 МБ
    backupCount=3,             # храним до 3 старых файлов
    encoding='utf-8'
)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger = logging.getLogger("webhook")
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.propagate = False

ensure_temp_file()

app = FastAPI()

ids_activity_bids = []
ids_activity_deals = []

async def deal(data):
    try:
        id_deal_bx24 = data.get("data[FIELDS][ID]", "")
        logger.info(f"ID сделки: {id_deal_bx24}")

        data_bx24 = await get_data_from_bx24_deal(id_deal_bx24)
        logger.info(f"Получены данные сделки из BX24")

        ###########################################################
        ###########################################################
        ###########################################################

        checkStatus = CheckUpdateStatus()
        status_bx24 = data_bx24.get("STAGE_ID", "")
        if not await checkStatus.checkStatusBx24(id_deal_bx24, status_bx24):
            logger.info(f"Статус не совпадает с необходимым или ID уже передавался")
            return Response(status_code=200)
        
        ###########################################################
        ###########################################################
        ###########################################################

        id_worker_bx24 = str(data_bx24.get("ASSIGNED_BY_ID", "")) or ""
        name_bx24 = str(await get_worker_from_bx24(id_worker_bx24) or "")
        id_worker_rukovoditel = str(await get_worker_from_rukovoditel(name_bx24) or "")

        route_value = data_bx24.get("UF_CRM_683EA5EE6C732", [])
        route = str(routes.get(str(route_value[0]) if route_value else "") or "")

        direction_value = data_bx24.get("UF_CRM_683EA5EE78933", [])
        direction = str(directions.get(str(direction_value[0]) if direction_value else 0, 0) or 0)

        inn = str(await get_inn_bx24(str(data_bx24.get("COMPANY_ID", ""))) or "")
        comment_on_the_deal = str(data_bx24.get("COMMENTS", "") or "").replace("[p]", "").replace("[/p]", "")
        btg_manager_kam = id_worker_rukovoditel

        logger.info(f"Основные поля: route={route}, direction={direction}, inn={inn}")

        f12795 = data_bx24.get("UF_CRM_683EA5EE8F634", "")
        f12796 = f12796_dict.get(str(data_bx24["UF_CRM_685000BC67768"][0]) if data_bx24["UF_CRM_685000BC67768"] else "")
        f12797 = data_bx24.get("UF_CRM_1750405403", "")
        f12798 = f12798_dict.get(data_bx24.get("UF_CRM_1750750718"), "")
        f12799 = f12799_dict.get(data_bx24.get("UF_CRM_1750751963"), "")
        f12800 = data_bx24.get("UF_CRM_1750752148", "")
        f12801 = data_bx24.get("UF_CRM_1750755583", "")
        f12802 = f12802_dict.get(data_bx24.get("UF_CRM_1751609471347", ""), "")
        f12803 = data_bx24.get("UF_CRM_1750755714", "")
        f12804 = data_bx24.get("UF_CRM_1750755728", "")
        f12805 = data_bx24.get("UF_CRM_1750755776", "")
        f12806 = data_bx24.get("UF_CRM_1750755907", "")
        f12807 = data_bx24.get("UF_CRM_1750755925", "")
        f12808 = data_bx24.get("UF_CRM_1750755957", "")
        f12809 = await get_worker_from_rukovoditel(await get_worker_from_bx24(data_bx24.get("UF_CRM_1750756012", "")))
        f12810 = await get_company_from_rukovoditel_btg_company(await get_inn_bx24(data_bx24.get("UF_CRM_1750756090", "")))
        f12811 = data_bx24.get("UF_CRM_1750756250", "")
        f12812 = data_bx24.get("UF_CRM_1750756289", "")
        f12813 = data_bx24.get("UF_CRM_1750756299", "")
        f12814 = data_bx24.get("UF_CRM_1750756532", "")
        f12815 = data_bx24.get("UF_CRM_1750756900", "")
        f12816 = data_bx24.get("UF_CRM_1750756924", "")
        f12817 = "\n".join(f"https://btg24.bitrix24.ru{f['downloadUrl']}" for f in data_bx24.get("UF_CRM_1750756580", []) if isinstance(f, dict) and 'downloadUrl' in f)

        f12837 = data_bx24.get("UF_CRM_1751441910", "")
        f12838 = data_bx24.get("UF_CRM_1751454278870", "")
        f12839 = data_bx24.get("UF_CRM_17516114495", "")
        f12840 = f12840_dict.get(data_bx24.get("UF_CRM_1751607912514", ""), "") #список
        f12841 = f12841_dict.get(data_bx24.get("UF_CRM_1751608473477", ""), "") #список
        f12842 = f12842_dict.get(data_bx24.get("UF_CRM_1751608579368", ""), "") #список
        f12844 = f12844_dict.get(data_bx24.get("UF_CRM_1751609624436", ""), "") #список
        f12845 = f12845_dict.get(data_bx24.get("UF_CRM_1751610742904", ""), "") #список
        f12846 = f12846_dict.get(data_bx24.get("UF_CRM_1751613009219", ""), "") #список 
        f12847 = f12847_dict.get(data_bx24.get("UF_CRM_1751613073416", ""), "") #список 
        f12835 = data_bx24.get("UF_CRM_1751617518", "")
        f12836 = data_bx24.get("UF_CRM_1751617532", "")

        f12848 = data_bx24.get("UF_CRM_1751876826", "")
        f12850 = f"https://btg24.bitrix24.ru/crm/deal/details/{id_deal_bx24}/"

        the_customer_company = await get_company_from_rukovoditel(inn)
        logger.info(f"Отправка данных в Руководитель...")

        id_ruk_deal_resp = await post_data_to_ruk(route, direction, inn, btg_manager_kam, comment_on_the_deal, the_customer_company,
            f12795, f12796, f12797, f12798, f12799, f12800, f12801, f12802, f12803, f12804, f12805, f12806, f12807, f12808,
            f12809, f12810, f12811, f12812, f12813, f12814, f12815, f12816, f12817,
            f12837, f12838, f12839, f12840, f12841, f12842, f12844, f12845, f12846, f12847, f12835, f12836,
            f12848, f12850)
        
        if id_ruk_deal_resp:
            ids_activity_bids.append(id_deal_bx24)
            await post_id_deal_to_bx24(id_deal_bx24, id_ruk_deal_resp)

        logger.info(f"Данные успешно отправлены.")
        return Response(status_code=200)
    
    except Exception as e:
        logger.exception(f"Ошибка при обработке webhook: {e}")
        return Response(status_code=500, content="Ошибка на сервере")
    
@app.post("/api")
async def receive_webhook(request: Request):
    try:
        form = await request.form()
        data = dict(form)
        logger.info(f"Получены данные webhook: {data}")
        
        event = data.get("event")
        id = data.get("data[FIELDS][ID]", "")

        if event == "ONCRMDEALUPDATE":
            if id in ids_activity_deals:
                ids_activity_deals.remove(id)
                return
            
            await deal(data)
            
        # if event == "ONCRMQUOTEADD":
        #     if id in ids_activity_bids:
        #         ids_activity_bids.remove(id)
        #         return
            
        #     await bid(data)
        
    except Exception as err:
        logger.error(f"Произошла ошибка в обработчике вебхука: {str(err)}")        
        
    
async def bid(data):
    try:
        id_bid_bx24 = data.get("data[FIELDS][ID]", "")
        logger.info(f"ID сделки: {id_bid_bx24}")
        
        data_bid_bx24 = await get_data_from_bx24_bid(id_bid_bx24)
        logger.info(f"Получены данные предложения из BX24")
        
        # if data_bid_bx24.get("STATUS_ID", "") == ????
        
        id_deal_bx24 = await get_data_from_bx24_deal(data_bid_bx24.get("DEAL_ID"))
        id_deal_bx24 = id_deal_bx24.get("UF_CRM_1753865222", "")
        
        f12974 = f12974_dict.get(data_bid_bx24.get("UF_CRM_1751464237", ""), "")
        f12973 = f12973_dict.get(data_bid_bx24.get("UF_CRM_QUOTE_1751530155", ""), "")
        
        f12975 = await get_company_from_rukovoditel_btg_company(data_bid_bx24.get("UF_CRM_686233DDCE5B7", ""))
        
        f12972 = data_bid_bx24.get("OPPORTUNITY", "")
        
        id_kom_predl_ruk = await post_data_kom_predlojenie_to_ruk(id_deal_bx24)
        id_bid_ruk = await post_data_tech_naimenovanie_to_ruk(f12974, f12973, f12975, f12972, id_kom_predl_ruk)
        
        #await post_id_bid_to_bx24(id_bid_ruk)
        
        
        
        
        
        
        
    except Exception as err:
        traceback.print_exc()