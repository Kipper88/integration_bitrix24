from utils import *

from decorators.except_decorators import async_exception_logger

import logging

logger = logging.getLogger("webhook")

@async_exception_logger
async def bid(id_bid_bx24, id_deal_ruk):
    logger.info(f"ID предложения: {id_bid_bx24}")
    
    data_bid_bx24 = await get_data_from_bx24(f"crm.quote.get?id={id_bid_bx24}")
    logger.info(f"Получены данные предложения из BX24")
    
    field_13136 = f13136_dict.get(data_bid_bx24.get("UF_CRM_1751464237", ""), "")
    field_13138 = f13138_dict.get(data_bid_bx24.get("UF_CRM_QUOTE_1751530155", ""), "")
    
    field_13139 = await get_company_from_rukovoditel_btg_company(data_bid_bx24.get("UF_CRM_686233DDCE5B7", ""))
    
    field_13137 = data_bid_bx24.get("OPPORTUNITY", "")
    
    #######################################################
    #######################################################
    # валюты. Строка вида "100|EUR"
    field_13254 = ""
    field_13255 = ""

    value = data_bid_bx24.get("UF_CRM_QUOTE_1752152869", "")

    try:
        parts = str(value).split("|")
        field_13254 = parts[0].strip() if len(parts) > 0 else ""
        field_13255 = parts[1].strip() if len(parts) > 1 else ""
    except Exception:
        # В случае любой ошибки оставляем пустые строки
        field_13254 = ""
        field_13255 = ""

    #######################################################
    #######################################################
    
    field_13256 = f13256_dict.get(data_bid_bx24.get("UF_CRM_QUOTE_1752559708298", ""))
    
        
    items = {f"{k}": f"{v}" for k, v in locals().items() if k.startswith("field_")}
    
    logger.info("Отправка предложения в руководитель...")
    id = await post_data_kp_to_ruk(items, id_deal_ruk)
    logger.info(f"Данные предложения успешно отправлены. id: {id}")