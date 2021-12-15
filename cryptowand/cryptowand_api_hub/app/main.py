from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json

from model.marketdata.getdata import get_coins_for_category

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
async def startup_event():
    print('started')

@app.on_event("shutdown")
async def startup_event():
    print('shutdown')
    


#print(cryptocatinfo)



@app.get("/cryptos/home", response_class=HTMLResponse)
async def read_item(request: Request):
    #Load Current Json for Marketscan EndPoint
    json_file_name= "../../cryptowand_data_hub/output/CryptoWand-current.json"
    
    with open(json_file_name, 'r') as myfile:
            data=myfile.read()
        
    cryptoinfo = json.loads(data)
  
    #Load Current Json for Categories EndPoint
    json_categories_file_name= "../../cryptowand_data_hub/output/CryptoWand-Categories.json"
    
    with open(json_categories_file_name, 'r') as my_cfile:
            datac=my_cfile.read()
    cryptocatinfo = json.loads(datac)

    #Load Current Json for Exchanges EndPoint
    json_exchanges_file_name= "../../cryptowand_data_hub/output/CryptoWand-Exchanges.json"
    
    with open(json_exchanges_file_name, 'r') as my_efile:
            datae=my_efile.read()
    cryptoexchangeinfo = json.loads(datae)
  
    return templates.TemplateResponse("homepage.html", 
    {
        "request": request, 
        "cryptoinfo": cryptoinfo,
        "cryptocatinfo": cryptocatinfo,
        "cryptoexchangeinfo": cryptoexchangeinfo
        
    }
    )

@app.get("/cryptos/categories/{cat_id}",response_class=HTMLResponse)
async def read_category(request: Request,cat_id: str):
    #Load Current Json for Marketscan EndPoint
    cryptocatinfo=get_coins_for_category(cat_id)
    return templates.TemplateResponse("cat_coins.html", 
        {
            "request": request, 
            "cryptocatinfo" : cryptocatinfo
        }
        )

