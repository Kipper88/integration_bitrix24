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
    
    #id_kom_predl_ruk = await post_data_kom_predlojenie_to_ruk(id_deal_ruk)
    
    items = {f"{k}": f"{v}" for k, v in locals().items() if k.startswith("field_")}
    
    logger.info("Отправка предложения в руководитель...")
    id = await post_data_kp_to_ruk(items, id_deal_ruk)
    logger.info("Данные предложения успешно отправлены")