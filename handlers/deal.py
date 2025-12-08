from utils import *
from fastapi import Response

from decorators.except_decorators import async_exception_logger

import logging

logger = logging.getLogger("webhook")

@async_exception_logger
async def deal(data):
    id_deal_bx24 = data.get("data[FIELDS][ID]", "")
    
    logger.info(f"ID сделки: {id_deal_bx24}")

    data_bx24 = await get_data_from_bx24(f"crm.deal.get?ID={id_deal_bx24}")
    logger.info(f"Получены данные сделки из BX24")

    checkStatus = CheckUpdateStatus()
    status_bx24 = data_bx24.get("STAGE_ID", "")
    if not await checkStatus.checkStatusBx24(id_deal_bx24, status_bx24):
        logger.info(f"Статус не совпадает с необходимым или ID уже передавался")
        return Response(status_code=200)

    id_worker_bx24 = str(data_bx24.get("ASSIGNED_BY_ID", "")) or ""
    name_bx24 = str(await get_worker_from_bx24(id_worker_bx24) or "") if id_worker_bx24 != "" else ""
    id_worker_rukovoditel = str(await get_worker_from_rukovoditel(name_bx24) or "")

    route_value = data_bx24.get("UF_CRM_683EA5EE6C732", [])
    field_12776 = str(routes.get(str(route_value[0]) if route_value else "") or "")
    

    direction_value = data_bx24.get("UF_CRM_683EA5EE78933", [])
    field_12775 = str(directions.get(str(direction_value[0]) if direction_value else 0, 0) or 0)

    field_12778 = str(await get_inn_bx24(str(data_bx24.get("COMPANY_ID", ""))) or "")
    field_12780 = str(data_bx24.get("COMMENTS", "") or "").replace("[p]", "").replace("[/p]", "")
    field_12779 = id_worker_rukovoditel
    field_12782 = await get_company_from_rukovoditel(field_12778) # the customer company

    field_12795 = data_bx24.get("UF_CRM_683EA5EE8F634", "")
    field_12796 = f12796_dict.get(str(data_bx24["UF_CRM_685000BC67768"][0]) if data_bx24["UF_CRM_685000BC67768"] else "", "")
    field_12797 = data_bx24.get("UF_CRM_1750405403", "")
    field_12798 = f12798_dict.get(data_bx24.get("UF_CRM_1750750718"), "")
    field_12799 = f12799_dict.get(data_bx24.get("UF_CRM_1750751963"), "")
    field_12800 = data_bx24.get("UF_CRM_1750752148", "")
    field_12801 = data_bx24.get("UF_CRM_1750755583", "")
    field_12802 = f12802_dict.get(data_bx24.get("UF_CRM_1751609471347", ""), "")
    field_12803 = data_bx24.get("UF_CRM_1750755714", "")
    field_12804 = data_bx24.get("UF_CRM_1750755728", "")
    field_12805 = data_bx24.get("UF_CRM_1750755776", "")
    field_12806 = data_bx24.get("UF_CRM_1750755907", "")
    field_12808 = data_bx24.get("UF_CRM_1750755957", "")
    field_12810 = await get_company_from_rukovoditel_btg_company(await get_inn_bx24(data_bx24.get("UF_CRM_1750756090", "")))
    field_12811 = data_bx24.get("UF_CRM_1750756250", "")
    field_12812 = data_bx24.get("UF_CRM_1750756289", "")
    field_12813 = data_bx24.get("UF_CRM_1750756299", "")
    field_12814 = data_bx24.get("UF_CRM_1750756532", "")
    field_12815 = data_bx24.get("UF_CRM_1750756900", "")
    field_12816 = data_bx24.get("UF_CRM_1750756924", "")
    field_12817 = "\n".join(f"https://btg24.bitrix24.ru{f['downloadUrl']}" for f in data_bx24.get("UF_CRM_1750756580", []) if isinstance(f, dict) and 'downloadUrl' in f)
    field_12837 = data_bx24.get("UF_CRM_1751441910", "")
    field_12838 = data_bx24.get("UF_CRM_1751454278870", "")
    field_12840 = f12840_dict.get(data_bx24.get("UF_CRM_1751607912514", ""), "") #список
    field_12844 = f12844_dict.get(data_bx24.get("UF_CRM_1751609624436", ""), "") #список
    field_12845 = f12845_dict.get(data_bx24.get("UF_CRM_1751610742904", ""), "") #список
    field_12846 = f12846_dict.get(data_bx24.get("UF_CRM_1751613009219", ""), "") #список 
    field_12847 = f12847_dict.get(data_bx24.get("UF_CRM_1751613073416", ""), "") #список 
    field_12848 = data_bx24.get("UF_CRM_1751876826", "")
    field_12850 = f"https://btg24.bitrix24.ru/crm/deal/details/{id_deal_bx24}/"
    field_13139 = field_12810
    field_13136 = f13136_dict_deal.get(data_bx24.get("UF_CRM_1751530362", ""), "")
    field_13503 = await get_worker_from_rukovoditel(await get_worker_from_bx24(data_bx24.get("UF_CRM_1751441910", ""))) if data_bx24.get("UF_CRM_1751441910") not in (None, "") else ""
    field_12839 = data_bx24.get("UF_CRM_1751614495", "")
    field_12835 = data_bx24.get("UF_CRM_1762430319", "")
    field_12836 = data_bx24.get("UF_CRM_1762430335", "")
    field_12841 = f12841_dict.get(data_bx24.get("UF_CRM_1751608473477", ""), "")
    field_12842 = f12842_dict.get(data_bx24.get("UF_CRM_1751608579368", ""), "")
    field_13137 = data_bx24.get("UF_CRM_1763441408", "")
    field_13138 = f13138_dict.get(data_bx24.get("UF_CRM_1751530253", ""), "")
    field_13513 = f13513_dict.get(data_bx24.get("UF_CRM_1763441424", ""))
    field_13254 = data_bx24.get("UF_CRM_1763446014", "")
    field_13256 = f13256_dict.get(data_bx24.get("UF_CRM_1759480026", ""), "")
    field_13255 = f13255_dict.get(data_bx24.get("UF_CRM_1763446027", ""))
    field_13541 = data_bx24.get("UF_CRM_1763459456", "")
    field_13542 = f13542_dict.get(data_bx24.get("UF_CRM_1763459517", ""), "")
    field_13549 = data_bx24.get("UF_CRM_1763534084", "")
    field_13550 = f13550_dict.get(data_bx24.get("SOURCE_ID", ""), "")
    field_12807 = data_bx24.get("UF_CRM_1750755925", "")
    field_13141 = data_bx24.get("UF_CRM_1750752148", "")
    field_13488 = data_bx24.get("UF_CRM_1762430356", "")
    field_13696 = data_bx24.get("UF_CRM_1765195025", "")
    
    
    items = {f"{k}": f"{v}" for k, v in locals().items() if k.startswith("field_")}
        
    logger.info(f"Отправка данных в Руководитель...")

    id_deal_ruk = await post_data_to_ruk("369", items)
    
    logger.info(f"Данные сделки успешно отправлены. ID_RUK - {id_deal_ruk}, ID_BX = {id_deal_bx24}. deal, DEAL")
        
    await checkStatus.addId(id_deal_bx24)
    
    

    return Response(status_code=200)
