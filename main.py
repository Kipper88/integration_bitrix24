import logging
from logging.handlers import RotatingFileHandler
from fastapi import FastAPI, Request
from utils import *
from cfg import *

from handlers.deal import deal
from handlers.company import company

handler = RotatingFileHandler(
    'temp/log/webhook.log',
    maxBytes = 3 * 1024 * 1024,
    backupCount=3,
    encoding='utf-8'
)

formatter = logging.Formatter(
    '%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
handler.setFormatter(formatter)

logger = logging.getLogger("webhook")
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.propagate = False

ensure_temp_file()

app = FastAPI()
    
@app.post("/api")
async def receive_webhook(request: Request):
    try:
        form = await request.form()
        data = dict(form)
        logger.info(f"Получены данные webhook: {data}")
        
        event = data.get("event")
        
        match event:
            case "ONCRMDEALUPDATE":
                await deal(data)
            case "ONCRMCOMPANYADD":
                await company(data)
        
    except Exception as err:
        logger.error(f"Произошла ошибка в обработчике вебхука: {str(err)}")        
        
logger.info("Программа успешно запущена")