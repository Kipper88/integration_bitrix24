from decorators.except_decorators import async_exception_logger
from utils import *

import logging

logger = logging.getLogger("webhook")

@async_exception_logger
async def site_company(data):
    params = {
        #"UF_CRM_1748858141430": UF_CRM_1748858141430_dict.get(data.get("Вид транспортного средства", ""), ""),
        "UF_CRM_1748858141430": data.get("Вид транспортного средства", ""),
        "UF_CRM_1751286410": UF_CRM_1751286410_dict.get(data.get("Вид загрузки", ""), ""),
        "UF_CRM_1756973470428": data.get("Место загрузки", ""),
        "UF_CRM_1756973517577": data.get("Место выгрузки", ""),
        #"UF_CRM_1756973590960": data.get("Наименование товара / груза / Вес и тд.", ""),
        #"UF_CRM_1751286704": data.get("No Label field_15d234f", ""),
        "NAME": data.get("No Label field_945417d", ""),
        "COMPANY_TITLE": ", ".join(
            filter(
                None,
                [
                    data.get("Вид транспортного средства", ""),
                    data.get("No Label field_15d234f", ""),
                    data.get("No Label field_4d9601c", "")
                ]
            )
        ),
        "EMAIL": [{"VALUE": data.get("No Label field_d0bd481", ""), "TYPE": "WORK"}],
        "PHONE": [{"VALUE": data.get("No Label field_289f776", ""), "TYPE": "WORK"}]
    }
    
    print(params)
    logger.info("Отправка данных лида в bx24")
    
    await post_data_site_company_to_lid_bx24(params)
    
    logger.info("Успешная отправка данных в bx24")