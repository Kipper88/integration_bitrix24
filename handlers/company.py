from decorators.except_decorators import async_exception_logger
from utils import *

import logging

logger = logging.getLogger("webhook")

@async_exception_logger
async def company(data):
    id_company = data.get('data[FIELDS][ID]', '')
    logger.info(f"ID компании {id_company}")
    
    data_company_bx24 = await get_data_from_bx24(f"crm.company.get?id={id_company}")
    
    logger.info("Получена информация о компании из BX24")
    
    field_1038 = data_company_bx24.get("TITLE", "")
    field_10062 = data_company_bx24.get("COMPANY_TYPE", "")
    field_1016 = data_company_bx24.get("ADDRESS", "")
    field_1015 = data_company_bx24.get("ADDRESS_LEGAL", "")
    field_3617 = data_company_bx24.get("ASSIGNED_BY_ID", "")

    phone = data_company_bx24.get("PHONE", "")
    field_1019 = (
        ', '.join(i.get("VALUE", "") for i in phone) if phone
        else ''
    ) if data_company_bx24.get("HAS_PHONE", "") == "Y" else ''
    
    email = data_company_bx24.get("EMAIL", "")
    has_email = data_company_bx24.get("HAS_EMAIL", "") == "Y"

    if has_email and email:
        email_values = [i.get("VALUE", "") for i in email if i.get("VALUE", "")]
        
        if len(email_values) == 1:
            field_1020 = email_values[0]
            field_7631 = ''
        elif len(email_values) > 1:
            field_7631 = ', '.join(email_values)
            field_1020 = ''
        else:
            field_1020 = ''
            field_7631 = ''
    else:
        field_1020 = ''
        field_7631 = ''
        
        
    web = data_company_bx24.get("WEB", [])
    field_1018 = ', '.join(i.get("VALUE", "") for i in web if i.get("VALUE", ""))
    
    field_1004 = data_company_bx24.get("UF_CRM_1749452196788", "")
    field_6985 = data_company_bx24.get("UF_CRM_1751271111", "")
    field_3676 = data_company_bx24.get("UF_CRM_1752137143", "")
    field_12283 = data_company_bx24.get("UF_CRM_1751888381", "")
    
    field_3676 = f3676_dict.get(data_company_bx24.get("UF_CRM_1752137143", ""), "")
    
    field_5979 = "1"
    
    items = {f"{k}": f"{v}" for k, v in locals().items() if k.startswith("field_")}
    
    await post_data_to_ruk1("68", items)