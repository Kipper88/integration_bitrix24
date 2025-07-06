import logging
from fastapi import FastAPI, Request, Response
from utils import *
from cfg import directions, f12796_dict, f12798_dict, f12799_dict, f12802_dict

import sys

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger = logging.getLogger("webhook")
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.propagate = False

app = FastAPI()

@app.post("/api/deal")
async def receive_webhook(request: Request):
    try:
        form = await request.form()
        data = dict(form)
        logger.info(f"Получены данные webhook: {data}")

        id_deal_bx24 = data.get("data[FIELDS][ID]", "")
        logger.info(f"ID сделки: {id_deal_bx24}")

        data_bx24 = await get_data_from_bx24(id_deal_bx24)
        logger.info(f"Получены данные сделки из BX24")

        ###########################################################
        ###########################################################
        ###########################################################

        checkStatus = CheckUpdateStatus()
        status_bx24 = data_bx24.get("STAGE_ID", "")
        if not checkStatus.checkStatusBx24(id_deal_bx24, status_bx24):
            logger.info(f"Статус не совпадает с необходимыми")
            return Response(status_code=200)
        
        ###########################################################
        ###########################################################
        ###########################################################

        id_worker_bx24 = data_bx24.get("ASSIGNED_BY_ID", "")
        name_bx24 = await get_worker_from_bx24(id_worker_bx24)
        id_worker_rukovoditel = await get_worker_from_rukovoditel(name_bx24)
        
        route = routes.get(str(data_bx24["UF_CRM_683EA5EE6C732"][0]) if data_bx24["UF_CRM_683EA5EE6C732"] else "")
        direction = directions.get(str(data_bx24["UF_CRM_683EA5EE78933"][0]) if data_bx24["UF_CRM_683EA5EE78933"] else "")
        inn = await get_inn_bx24(data_bx24.get("COMPANY_ID", ""))
        comment_on_the_deal = str(data_bx24.get("COMMENTS", "")).replace("[p]", '').replace('[/p]', '')
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

        the_customer_company = await get_company_from_rukovoditel(inn)
        logger.info(f"Отправка данных в Руково...")

        await post_data_to_ruk(route, direction, inn, btg_manager_kam, comment_on_the_deal, the_customer_company,
            f12795, f12796, f12797, f12798, f12799, f12800, f12801, f12802, f12803, f12804, f12805, f12806, f12807, f12808,
            f12809, f12810, f12811, f12812, f12813, f12814, f12815, f12816, f12817,
            f12837, f12838, f12839, f12840, f12841, f12842, f12844, f12845, f12846, f12847, f12835, f12836)

        logger.info(f"Данные успешно отправлены.")
        return Response(status_code=200)
    
    except Exception as e:
        logger.exception(f"Ошибка при обработке webhook: {e}")
        return Response(status_code=500, content="Ошибка на сервере")
