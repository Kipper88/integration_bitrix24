from fastapi import FastAPI, Request, Response
from utils import *
from cfg import directions

app = FastAPI()

@app.post("/api/deal")
async def receive_webhook(request: Request):
    form = await request.form()
    data = dict(form) 
    
    id_deal_bx24 = data.get("data[FIELDS][ID]", "")
    data_bx24 = await get_data_from_bx24(id_deal_bx24)
    
    id_worker_bx24 = data_bx24.get("ASSIGNED_BY_ID", "")
    name_bx24 = await get_worker_from_bx24(id_worker_bx24)
    
    id_worker_rukovoditel = await get_worker_from_rukovoditel(name_bx24)
    
    route =                 routes.get(str(data_bx24.get("UF_CRM_683EA5EE6C732", "")[0]))
    direction =             directions.get(str(data_bx24.get("UF_CRM_683EA5EE78933", "")[0]))
    inn =                   await get_inn_bx24(data_bx24.get("COMPANY_ID", ""))
    btg_manager_kam =       id_worker_rukovoditel
    comment_on_the_deal =   str(data_bx24.get("COMMENTS", "")).replace("[p]", '').replace('[/p]', '')

    the_customer_company =  await get_company_from_rukovoditel(inn)
    
    #print(f"route: {route};\ndirection: {direction};\ninn: {inn};\nbtg_manager_kam: {btg_manager_kam};\ncomment_on_the_deal: {comment_on_the_deal};\nthe_customer_company: {the_customer_company};")
    
    await post_data_to_ruk(route, direction, inn, btg_manager_kam, comment_on_the_deal, the_customer_company)
        
    return Response(status_code=200)