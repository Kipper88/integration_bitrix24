from utils import *

from decorators.except_decorators import async_exception_logger

import logging

logger = logging.getLogger("webhook")

@async_exception_logger
async def bid(id_bid_bx24, id_deal_ruk):
    logger.info(f"ID предложения: {id_bid_bx24}")
    
    data_bid_bx24 = await get_data_from_bx24(f"crm.quote.get?id={id_bid_bx24}")
    logger.info(f"Получены данные предложения из BX24")
    
    f12974 = f12974_dict.get(data_bid_bx24.get("UF_CRM_1751464237", ""), "")
    f12973 = f12973_dict.get(data_bid_bx24.get("UF_CRM_QUOTE_1751530155", ""), "")
    
    f12975 = await get_company_from_rukovoditel_btg_company(data_bid_bx24.get("UF_CRM_686233DDCE5B7", ""))
    
    f12972 = data_bid_bx24.get("OPPORTUNITY", "")
    
    id_kom_predl_ruk = await post_data_kom_predlojenie_to_ruk(id_deal_ruk)
    await post_data_tech_naimenovanie_to_ruk(f12974, f12973, f12975, f12972, id_kom_predl_ruk)