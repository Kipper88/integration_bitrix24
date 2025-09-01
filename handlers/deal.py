from utils import *
from fastapi import Response
from .bid import bid

from decorators.except_decorators import async_exception_logger

import logging
import asyncio

logger = logging.getLogger("webhook")

@async_exception_logger
async def deal(data):
    id_deal_bx24 = data.get("data[FIELDS][ID]", "")
    logger.info(f"ID сделки: {id_deal_bx24}")

    data_bx24 = await get_data_from_bx24(f"crm.deal.get?ID={id_deal_bx24}")
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

    id_deal_ruk = await post_data_to_ruk(route, direction, inn, btg_manager_kam, comment_on_the_deal, the_customer_company,
        f12795, f12796, f12797, f12798, f12799, f12800, f12801, f12802, f12803, f12804, f12805, f12806, f12807, f12808,
        f12809, f12810, f12811, f12812, f12813, f12814, f12815, f12816, f12817,
        f12837, f12838, f12839, f12840, f12841, f12842, f12844, f12845, f12846, f12847, f12835, f12836,
        f12848, f12850)
    
    id_bid_bx24 = data_bx24.get("UF_CRM_1755126562", "")
    
    if id_bid_bx24 != "":
        await bid(id_bid_bx24, id_deal_ruk)
    
    

    logger.info(f"Данные успешно отправлены.")
    return Response(status_code=200)